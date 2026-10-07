"""Custody and schema qualification for the unadopted Unit C design package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


PACKAGE_NAME = "qualification/unit-c-durable-claim-reference-v0.1-draft"
UNIT_B_CATALOG_SHA256 = "e51c99c81c61cc1cc69ddbfd193503a1b659fcf694ffcc2d5d76cc47ba6d5792"
EXPECTED_FILES = (
    ".gitattributes",
    "IMPLEMENTATION-WORK-ORDER-DRAFT.md",
    "ORDERING-CONFLICT-REVIEW.md",
    "REFERENCE-CONTRACT-DRAFT.md",
    "journal-record-draft.schema.json",
    "qualify_unit_c.py",
    "recheck-evidence-draft.schema.json",
    "target-evidence-draft.schema.json",
    "test_qualification.py",
    "unit_canonical.py",
)
SCHEMA_FILES = tuple(name for name in EXPECTED_FILES if name.endswith(".schema.json"))
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SCHEMA_MAP_KEYWORDS = (
    "$defs", "definitions", "properties", "patternProperties", "dependentSchemas",
)
SCHEMA_ARRAY_KEYWORDS = ("allOf", "anyOf", "oneOf", "prefixItems")
SCHEMA_SINGLE_KEYWORDS = (
    "additionalItems", "additionalProperties", "contentSchema", "contains", "else",
    "if", "items", "not", "propertyNames", "then", "unevaluatedItems",
    "unevaluatedProperties",
)
SCHEMA_OBJECT_KEYWORDS = (
    "additionalProperties", "dependentRequired", "dependentSchemas", "maxProperties",
    "minProperties", "patternProperties", "properties", "propertyNames", "required",
    "unevaluatedProperties",
)


class QualificationError(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise QualificationError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _read_json(path: Path):
    if path.stat().st_size > 1024 * 1024:
        raise QualificationError("JSON_INPUT_TOO_LARGE")
    raw = path.read_bytes()
    if len(raw) > 1024 * 1024:
        raise QualificationError("JSON_INPUT_TOO_LARGE")
    try:
        return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise QualificationError("INVALID_JSON") from exc


def _check_closed_schema(node, location="$", depth=0):
    if depth > 64:
        raise QualificationError("SCHEMA_DEPTH_LIMIT")
    if not isinstance(node, dict):
        return
    schema_type = node.get("type")
    includes_object = schema_type == "object" or (
        isinstance(schema_type, list) and "object" in schema_type
    )
    may_validate_objects = includes_object or (
        "type" not in node and any(keyword in node for keyword in SCHEMA_OBJECT_KEYWORDS)
    )
    object_is_closed = (
        node.get("additionalProperties") is False
        or node.get("unevaluatedProperties") is False
    )
    if may_validate_objects and not object_is_closed:
        raise QualificationError(f"OPEN_OBJECT_SCHEMA:{location}")
    for keyword in SCHEMA_MAP_KEYWORDS:
        children = node.get(keyword, {})
        if isinstance(children, dict):
            for name, child in children.items():
                _check_closed_schema(child, f"{location}.{keyword}.{name}", depth + 1)
    for keyword in SCHEMA_SINGLE_KEYWORDS:
        if keyword in node:
            _check_closed_schema(node[keyword], f"{location}.{keyword}", depth + 1)
    for keyword in SCHEMA_ARRAY_KEYWORDS:
        branches = node.get(keyword, [])
        if isinstance(branches, list):
            for index, child in enumerate(branches):
                _check_closed_schema(child, f"{location}.{keyword}[{index}]", depth + 1)


def _within_package(package: Path, relative_path: str) -> Path:
    if not isinstance(relative_path, str) or "\\" in relative_path:
        raise QualificationError("INVALID_PACKAGE_PATH")
    pure = PurePosixPath(relative_path)
    if pure.is_absolute() or not pure.parts or any(part in (".", "..") for part in pure.parts):
        raise QualificationError("INVALID_PACKAGE_PATH")
    candidate = package.joinpath(*pure.parts)
    current = package
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise QualificationError("SYMLINK_PACKAGE_INPUT")
    try:
        candidate.resolve(strict=True).relative_to(package.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise QualificationError("PACKAGE_PATH_ESCAPE") from exc
    if not candidate.is_file():
        raise QualificationError("PACKAGE_FILE_MISSING")
    return candidate


def verify(package: Path, repo: Path, expected_manifest_sha256: str):
    package = package.resolve(strict=True)
    repo = repo.resolve(strict=True)
    if not HEX64.fullmatch(expected_manifest_sha256):
        raise QualificationError("INVALID_EXTERNAL_MANIFEST_PIN")
    expected_entries = {"candidate-manifest.json", *EXPECTED_FILES}
    try:
        actual_entries = {
            entry.relative_to(package).as_posix()
            for entry in package.rglob("*")
        }
    except OSError as exc:
        raise QualificationError("PACKAGE_CONTENT_ENUMERATION_FAILED") from exc
    if actual_entries != expected_entries:
        raise QualificationError("PACKAGE_CONTENT_SET_MISMATCH")
    manifest_path = _within_package(package, "candidate-manifest.json")
    if manifest_path.stat().st_size > 1024 * 1024:
        raise QualificationError("MANIFEST_TOO_LARGE")
    manifest_bytes = manifest_path.read_bytes()
    if len(manifest_bytes) > 1024 * 1024:
        raise QualificationError("MANIFEST_TOO_LARGE")
    if hashlib.sha256(manifest_bytes).hexdigest() != expected_manifest_sha256:
        raise QualificationError("SOURCE_DIGEST_MISMATCH:candidate-manifest.json")
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise QualificationError("INVALID_MANIFEST_SHAPE")
    if set(manifest) != {
        "candidate", "status", "contract_order", "unit_b_accepted_catalog_sha256", "files"
    }:
        raise QualificationError("MANIFEST_FIELDS_MISMATCH")
    if manifest["candidate"] != "Unit C durable-claim reference v0.1":
        raise QualificationError("CANDIDATE_ID_MISMATCH")
    if manifest["status"] != "PROPOSED_NOT_ADOPTED":
        raise QualificationError("CANDIDATE_DISPOSITION_MISMATCH")
    if manifest["contract_order"] != "UNRESOLVED":
        raise QualificationError("ORDER_MUST_REMAIN_UNRESOLVED")
    if manifest["unit_b_accepted_catalog_sha256"] != UNIT_B_CATALOG_SHA256:
        raise QualificationError("UNIT_B_PIN_MISMATCH")
    catalog = repo / "qualification" / "authority-unit-b-v1.3" / "unit-b-catalog.json"
    if not catalog.is_file() or hashlib.sha256(catalog.read_bytes()).hexdigest() != UNIT_B_CATALOG_SHA256:
        raise QualificationError("UNIT_B_ACCEPTED_CATALOG_DIGEST_MISMATCH")

    rows = manifest["files"]
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_FILES):
        raise QualificationError("MANIFEST_FILE_SET_MISMATCH")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256"}:
            raise QualificationError("INVALID_MANIFEST_FILE_ENTRY")
        relative = row["path"]
        digest = row["sha256"]
        if not isinstance(relative, str) or relative in seen or relative not in EXPECTED_FILES or not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise QualificationError("MANIFEST_FILE_SET_MISMATCH")
        seen.add(relative)
        path = _within_package(package, relative)
        if path.stat().st_size > 1024 * 1024:
            raise QualificationError("PACKAGE_FILE_TOO_LARGE")
        raw = path.read_bytes()
        if len(raw) > 1024 * 1024:
            raise QualificationError("PACKAGE_FILE_TOO_LARGE")
        if len(raw) > 1024 * 1024:
            raise QualificationError("PACKAGE_FILE_TOO_LARGE")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise QualificationError(f"SOURCE_DIGEST_MISMATCH:{relative}")
        if relative in SCHEMA_FILES:
            schema = _read_json(path)
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:
                raise QualificationError(f"INVALID_JSON_SCHEMA:{relative}") from exc
            _check_closed_schema(schema)
    if seen != set(EXPECTED_FILES):
        raise QualificationError("MANIFEST_FILE_SET_MISMATCH")
    return {
        "candidate": manifest["candidate"],
        "result": "PASS",
        "scope": "SOURCE_CUSTODY_AND_DRAFT_SCHEMA_ONLY",
        "contract_order": "UNRESOLVED",
        "runtime_authority": False,
        "effect_permitted": False,
        "durable_consumption": False,
        "production_ready": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        result = verify(args.package, args.repo, args.manifest_sha256)
    except (OSError, QualificationError) as exc:
        print(json.dumps({"candidate": "Unit C durable-claim reference v0.1", "result": "FAIL", "reason": str(exc), "production_ready": False}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
