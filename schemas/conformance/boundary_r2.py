"""Candidate structural/admissibility boundary. No authority or secret admission service."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import copy
from jsonschema import Draft202012Validator

MAX_BYTES = 1048576
MAX_DEPTH = 64
MAX_NODES = 100000
RESERVED = ('serialization_profile', 'schema_id', 'schema_version')
REGISTRY_SHA = '0df9a474c006a75c0e56d672e6a6a13d6cdb991b91eda818896eea7d6eb8f509'

class Rejected(ValueError):
    pass

def require(condition, reason):
    if not condition:
        raise Rejected(reason)

def admissible(value):
    """Exact ACS value classes, Unicode and deterministic resource bounds."""
    active = set()
    nodes = 0
    def visit(item, depth):
        nonlocal nodes
        nodes += 1
        require(nodes <= MAX_NODES and depth <= MAX_DEPTH, 'ACS_RESOURCE_LIMIT')
        kind = type(item)
        require(kind in (type(None), bool, int, str, list, dict), 'ACS_UNSUPPORTED_TYPE')
        if kind is str:
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in item), 'ACS_UNPAIRED_SURROGATE')
        if kind in (list, dict):
            require(id(item) not in active, 'ACS_CYCLE')
            active.add(id(item))
            if kind is dict:
                require(all(type(k) is str for k in item), 'ACS_NON_STRING_KEY')
                for key, child in item.items():
                    visit(key, depth + 1)
                    visit(child, depth + 1)
            if kind is list:
                for child in item:
                    visit(child, depth + 1)
            active.remove(id(item))
    visit(value, 0)

def parse_transport(raw):
    require(type(raw) is bytes and len(raw) <= MAX_BYTES, 'INPUT_BYTES_OR_SIZE')
    require(not raw.startswith(b'\xef\xbb\xbf'), 'BOM_FORBIDDEN')
    def pairs(items):
        value = {}
        for key, child in items:
            require(key not in value, 'DUPLICATE_DECODED_KEY')
            value[key] = child
        return value
    def no_float(_):
        raise Rejected('ACS_NATIVE_FLOAT_FORBIDDEN')
    def integer(token):
        require(re.fullmatch(r'(?:0|[1-9][0-9]*|-[1-9][0-9]*)', token) is not None,
                'NONCANONICAL_INTEGER')
        return int(token)
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                           parse_float=no_float, parse_constant=no_float, parse_int=integer)
    except Rejected:
        raise
    except (ValueError, UnicodeError, RecursionError):
        raise Rejected('MALFORMED_TRANSPORT') from None
    admissible(value)
    return value

def encode_value(value):
    admissible(value)
    def encode(item):
        kind = type(item)
        if item is None:
            return b'null'
        if kind is bool:
            return b'true' if item else b'false'
        if kind is int:
            try:
                return str(item).encode('ascii')
            except ValueError:
                raise Rejected('INTEGER_RESOURCE_LIMIT') from None
        if kind is str:
            return json.dumps(item, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        if kind is list:
            return b'[' + b','.join(encode(x) for x in item) + b']'
        return b'{' + b','.join(encode(k) + b':' + encode(item[k])
                               for k in sorted(item, key=lambda x: x.encode('utf-8'))) + b'}'
    result = encode(value)
    require(len(result) <= MAX_BYTES, 'ENCODED_SIZE_LIMIT')
    return result

def encode_document(value):
    require(type(value) is dict, 'DOCUMENT_OBJECT_REQUIRED')
    require(all(type(value.get(k)) is str and bool(value[k]) for k in RESERVED), 'DOCUMENT_BINDING_REQUIRED')
    require(value['serialization_profile'] == 'ACS-1', 'UNKNOWN_SERIALIZATION_PROFILE')
    return encode_value(value)

def canonical_document(raw):
    value = parse_transport(raw)
    require(encode_document(value) == raw, 'NONCANONICAL_DOCUMENT')
    return value

def reject_secret_shapes(value):
    """Admission safeguard for recognized shapes; never claims universal secret detection."""
    admissible(value)
    forbidden_keys = {'privatekey', 'secretkey', 'privatekeymaterial', 'privatekeybytes',
                      'password', 'apikey', 'accesstoken', 'refreshtoken', 'clientsecret'}
    def walk(item):
        if type(item) is dict:
            for key, child in item.items():
                normalized = re.sub(r'[^a-z0-9]', '', key.lower())
                require(normalized not in forbidden_keys, 'SECRET_SHAPE_FORBIDDEN')
                walk(child)
        if type(item) is list:
            for child in item:
                walk(child)
        if type(item) is str:
            require(re.search(r'-----BEGIN [A-Z ]*PRIVATE KEY-----', item) is None,
                    'PRIVATE_KEY_MARKER_FORBIDDEN')
    walk(value)

@dataclass(frozen=True)
class Resolution:
    status: str
    schema_id: str | None
    schema_version: str | None

@dataclass(frozen=True)
class BoundaryReview:
    resolution: Resolution
    structural: str
    content_admission: str
    semantic_resolution: str = 'UNRESOLVED'
    effective_authority: bool = False

class Registry:
    def __init__(self, repo):
        self.repo = Path(repo).resolve()
        registry_bytes = (self.repo / 'schemas/registry.v1.json').read_bytes()
        require(hashlib.sha256(registry_bytes).hexdigest() == REGISTRY_SHA, 'REGISTRY_DIGEST_MISMATCH')
        raw = parse_transport(registry_bytes)
        require(raw.get('registry_version') == '1' and raw.get('schema_count') == 18,
                'REGISTRY_IDENTITY')
        require(raw.get('schema_dialect') == 'https://json-schema.org/draft/2020-12/schema',
                'REGISTRY_DIALECT')
        self._schemas = {}
        for entry in raw['schemas']:
            key = entry['schema_id'], entry['schema_version']
            require(key not in self._schemas, 'DUPLICATE_REGISTRY_BINDING')
            path = (self.repo / entry['schema_path']).resolve()
            require(path.is_relative_to(self.repo / 'schemas/root'), 'SCHEMA_PATH_OUTSIDE_ROOT')
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == entry['schema_sha256'], 'SCHEMA_DIGEST_MISMATCH')
            schema = parse_transport(data)
            require(schema.get('$schema') == raw['schema_dialect'], 'SCHEMA_DIALECT')
            require(schema['properties']['schema_id']['const'] == key[0]
                    and schema['properties']['schema_version']['const'] == key[1], 'REGISTRY_SCHEMA_CONFUSION')
            Draft202012Validator.check_schema(schema)
            self._schemas[key] = schema
        require(len(self._schemas) == 18, 'REGISTRY_MEMBERSHIP')

    @property
    def schemas(self):
        return copy.deepcopy(self._schemas)

    def resolve(self, value):
        require(type(value) is dict, 'DOCUMENT_OBJECT_REQUIRED')
        sid, version = value.get('schema_id'), value.get('schema_version')
        if type(sid) is not str or type(version) is not str or (sid, version) not in self._schemas:
            return Resolution('UNRESOLVED', sid if type(sid) is str else None,
                              version if type(version) is str else None)
        return Resolution('VALID_CONTEXT', sid, version)

    def review(self, value, content_verifier=None, semantic_verifier=None):
        """No effective admission from structural PASS; absent secret-free proof stays unresolved."""
        resolution = self.resolve(value)
        if resolution.status != 'VALID_CONTEXT':
            return BoundaryReview(resolution, 'INTERPRETATION_UNRESOLVED', 'UNRESOLVED')
        try:
            admissible(value)
            reject_secret_shapes(value)
            encode_document(value)
        except Rejected:
            return BoundaryReview(resolution, 'STRUCTURALLY_INVALID', 'NOT_CHECKED')
        schema = self._schemas[resolution.schema_id, resolution.schema_version]
        if not Draft202012Validator(schema).is_valid(value):
            return BoundaryReview(resolution, 'STRUCTURALLY_INVALID', 'NOT_CHECKED')
        admission = 'UNRESOLVED'
        if content_verifier is not None:
            # This is a reference binding, not an ACBP semantic digest or proof of issuer authority.
            digest = hashlib.sha256(encode_document(value)).hexdigest()
            admission = content_verifier.verify_secret_free(digest)
            require(type(admission) is str and admission in ('SATISFIED', 'BLOCKED', 'UNRESOLVED'),
                    'INVALID_CONTENT_ADMISSION')
        semantic = 'UNRESOLVED'
        if semantic_verifier is not None:
            digest = hashlib.sha256(encode_document(value)).hexdigest()
            semantic = semantic_verifier.verify_interpretation(resolution.schema_id,
                                                              resolution.schema_version, digest)
            require(type(semantic) is str and semantic in ('SATISFIED', 'BLOCKED', 'UNRESOLVED'),
                    'INVALID_SEMANTIC_RESOLUTION')
        return BoundaryReview(resolution, 'STRUCTURALLY_VALID', admission, semantic)
