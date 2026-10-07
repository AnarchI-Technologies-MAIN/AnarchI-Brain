"""Strict bounded JSON and digest primitives for the proposed Unit C profile."""

from __future__ import annotations

import hashlib
import json


MAX_RAW_BYTES = 1024 * 1024
MAX_DEPTH = 64
MAX_NODES = 100_000
MIN_INTEGER = -(2**63)
MAX_INTEGER = 2**63 - 1
DIGEST_DOMAINS = frozenset(
    {
        "UNIT-C:BINDING:v1",
        "UNIT-C:EVENT:v1",
        "UNIT-C:TARGET:v1",
        "UNIT-C:RECHECK:v1",
    }
)


class CanonicalJSONError(ValueError):
    pass


def _reject_float(_value):
    raise CanonicalJSONError("FLOAT_NOT_ALLOWED")


def _reject_constant(_value):
    raise CanonicalJSONError("NONFINITE_NUMBER_NOT_ALLOWED")


def _parse_integer(token):
    if len(token) > 20:
        raise CanonicalJSONError("INTEGER_OUT_OF_RANGE")
    value = int(token)
    if value < MIN_INTEGER or value > MAX_INTEGER:
        raise CanonicalJSONError("INTEGER_OUT_OF_RANGE")
    return value


def _object_from_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalJSONError("DUPLICATE_OBJECT_KEY")
        result[key] = value
    return result


def _validate_value(value):
    nodes = 0
    active = set()

    def visit(item, depth):
        nonlocal nodes
        nodes += 1
        if nodes > MAX_NODES:
            raise CanonicalJSONError("NODE_LIMIT_EXCEEDED")
        if depth > MAX_DEPTH:
            raise CanonicalJSONError("DEPTH_LIMIT_EXCEEDED")
        kind = type(item)
        if item is None or kind is bool:
            return
        if kind is int:
            if item < MIN_INTEGER or item > MAX_INTEGER:
                raise CanonicalJSONError("INTEGER_OUT_OF_RANGE")
            return
        if kind is str:
            try:
                item.encode("utf-8", "strict")
            except UnicodeEncodeError as exc:
                raise CanonicalJSONError("INVALID_UNICODE_SCALAR") from exc
            return
        if kind is list:
            identity = id(item)
            if identity in active:
                raise CanonicalJSONError("CYCLIC_VALUE")
            active.add(identity)
            try:
                for child in item:
                    visit(child, depth + 1)
            finally:
                active.remove(identity)
            return
        if kind is dict:
            identity = id(item)
            if identity in active:
                raise CanonicalJSONError("CYCLIC_VALUE")
            active.add(identity)
            try:
                for key, child in item.items():
                    if type(key) is not str:
                        raise CanonicalJSONError("OBJECT_KEY_NOT_STRING")
                    visit(key, depth + 1)
                    visit(child, depth + 1)
            finally:
                active.remove(identity)
            return
        raise CanonicalJSONError("UNSUPPORTED_JSON_VALUE")

    visit(value, 0)


def canonical_bytes(value):
    _validate_value(value)
    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8", "strict")
    except (TypeError, ValueError, UnicodeError, RecursionError) as exc:
        raise CanonicalJSONError("CANONICALIZATION_FAILED") from exc
    if len(encoded) > MAX_RAW_BYTES:
        raise CanonicalJSONError("CANONICAL_BYTES_LIMIT_EXCEEDED")
    return encoded


def parse_bytes(raw):
    if type(raw) is not bytes:
        raise CanonicalJSONError("RAW_INPUT_MUST_BE_BYTES")
    if len(raw) > MAX_RAW_BYTES:
        raise CanonicalJSONError("RAW_INPUT_TOO_LARGE")
    try:
        decoded = raw.decode("utf-8", "strict")
        value = json.loads(
            decoded,
            object_pairs_hook=_object_from_pairs,
            parse_float=_reject_float,
            parse_int=_parse_integer,
            parse_constant=_reject_constant,
        )
        _validate_value(value)
    except CanonicalJSONError:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise CanonicalJSONError("INVALID_BOUNDED_JSON") from exc
    return value


def digest_bytes(domain, payload):
    if type(domain) is not str or domain not in DIGEST_DOMAINS:
        raise CanonicalJSONError("INVALID_DIGEST_DOMAIN")
    if type(payload) is not bytes:
        raise CanonicalJSONError("DIGEST_PAYLOAD_MUST_BE_BYTES")
    if len(payload) > MAX_RAW_BYTES:
        raise CanonicalJSONError("DIGEST_PAYLOAD_TOO_LARGE")
    try:
        prefix = domain.encode("ascii", "strict")
    except UnicodeEncodeError as exc:
        raise CanonicalJSONError("INVALID_DIGEST_DOMAIN") from exc
    return hashlib.sha256(prefix + b"\0" + payload).hexdigest()


def digest_object(domain, value):
    return digest_bytes(domain, canonical_bytes(value))
