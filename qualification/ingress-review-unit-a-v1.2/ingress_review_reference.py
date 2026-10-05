"""Trusted-first-party pure fixture composition; no runtime authority or effects."""
import base64
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass

SOURCE_PINS = {
    'm03': '4d95d6dd4f002936ef23780c083758703cb2cf30fbaff352caf16dad5d38dfa2',
    'm08': 'deb4282ece47e0ee2e390b8ed9604a05765a0bb24f309712756c18dbfe536bcc',
    'mapping': '7561f2222762fca9904e4f1e8494d21b8b5b99dfc87d48d572922d52db5ac162',
    'custody': 'af44421bd22f753bcb5c3a8a87f3e290becd94e5f14dff9fe3684c92ac2d5670',
}
MAPPING_CONTRACT_PIN = '61411344381e31149a1b652a34e75f65438a4e18c98970115454ab3ad785d9a4'
MAX_BYTES = 1048576
MAX_DEPTH = 64
MAX_NODES = 100000
MAX_COORDINATE = 9223372036854775807
FINDINGS = ('resource_bounds', 'exact_subject', 'structure', 'provenance', 'mapping', 'fixture_freshness')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def digest(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)

@dataclass(frozen=True)
class ReferenceSubject:
    brain_document_sha256: str
    epistemaddy_proposal_sha256: str
    source_database_sha256: str
    source_candidate_id: str
    source_record_version: int
    producer_scope: str

@dataclass(frozen=True)
class Snapshot:
    expected_root_sha256: str
    observed_root_sha256: str | None
    expected_epoch: int
    observed_epoch: int | None
    profile: str

@dataclass(frozen=True)
class Dependencies:
    m03: object
    m08: object
    mapping: object
    custody: object
    source_pins: tuple
    qualification_contract_sha256: str

@dataclass(frozen=True)
class ReviewResult:
    disposition: str
    findings: tuple
    m03_description: tuple
    m08_description: tuple
    subject_sha256: str | None
    producer_sha256: str | None
    qualification_contract_sha256: str | None
    context_sha256: str | None
    reference_subject_sha256: str | None
    dependency_identity_sha256: str | None
    profile: str = 'STRUCTURE_PROVENANCE_SCOPE_ONLY'
    content_admission: str = 'UNRESOLVED'
    semantic_resolution: str = 'UNRESOLVED'
    operative_authority: str = 'UNRESOLVED'
    runtime_crossing_permitted: bool = False
    canonical_membership: bool = False
    ordinary_access: str = 'CLOSED'
    runtime_m04_state: str = 'CANDIDATE'
    protected_effect: bool = False

def load_dependencies(buffers, qualification_contract_raw, qualification_contract_sha256):
    """Verify the entire known first-party set BEFORE any source execution."""
    if not digest(qualification_contract_sha256) or type(qualification_contract_raw) is not bytes or not 0 < len(qualification_contract_raw) <= MAX_BYTES or sha(qualification_contract_raw) != qualification_contract_sha256:
        raise ValueError('QUALIFICATION_CONTRACT_DRIFT')
    if type(buffers) is not dict or set(buffers) != set(SOURCE_PINS):
        raise ValueError('DEPENDENCY_MEMBERSHIP')
    for label, pin in SOURCE_PINS.items():
        raw = buffers[label]
        if type(raw) is not bytes or len(raw) > MAX_BYTES or sha(raw) != pin:
            raise ValueError('DEPENDENCY_SOURCE_DRIFT')
    modules = {}
    for label, raw in buffers.items():
        name = '_ingress_unit_a_' + label
        module = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader=None))
        module.__file__ = label + '.captured'
        sys.modules[name] = module
        exec(compile(raw, module.__file__, 'exec', dont_inherit=True), module.__dict__)
        modules[label] = module
    return Dependencies(modules['m03'], modules['m08'], modules['mapping'], modules['custody'], tuple(sorted(SOURCE_PINS.items())), qualification_contract_sha256)

def bounded_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('DUPLICATE_FIELD')
            result[key] = value
        return result
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
    pending = [(value, 0)]
    nodes = 0
    while pending:
        current, depth = pending.pop()
        nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            raise ValueError('JSON_RESOURCE_BOUND')
        if type(current) is dict:
            pending.extend((item, depth + 1) for item in current.values())
        elif type(current) is list:
            pending.extend((item, depth + 1) for item in current)
        elif type(current) not in (str, int, bool, type(None)):
            raise ValueError('JSON_TYPE')
    return value

def evaluate(brain_bytes, producer_bytes, subject, snapshot, dependencies):
    """Expected subject/pins come from independent qualified custody, not this input."""
    findings = {key: 'UNRESOLVED' for key in FINDINGS}
    m03_summary = (); m08_summary = ()
    verified_brain = None; verified_producer = None
    context_pin = None; subject_pin = None; dependency_pin = None
    def finish():
        values = tuple(findings.values())
        disposition = 'QUALIFICATION_BLOCKED' if 'BLOCKED' in values else 'QUALIFICATION_UNRESOLVED' if 'UNRESOLVED' in values else 'QUALIFICATION_SATISFIED'
        contract_pin = dependencies.qualification_contract_sha256 if type(dependencies) is Dependencies else None
        return ReviewResult(disposition, tuple(findings.items()), m03_summary, m08_summary, verified_brain, verified_producer, contract_pin, context_pin, subject_pin, dependency_pin)
    if type(dependencies) is not Dependencies or dependencies.source_pins != tuple(sorted(SOURCE_PINS.items())):
        findings['provenance'] = 'BLOCKED'
        return finish()
    dependency_pin = sha(json.dumps({'source_pins':dependencies.source_pins,'qualification_contract_sha256':dependencies.qualification_contract_sha256,'mapping_contract_sha256':MAPPING_CONTRACT_PIN,'baseline_catalog_sha256':dependencies.mapping.BASELINE_CATALOG},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
    if type(brain_bytes) is not bytes or type(producer_bytes) is not bytes or not 0 < len(brain_bytes) <= MAX_BYTES or not 0 < len(producer_bytes) <= MAX_BYTES:
        findings['resource_bounds'] = 'BLOCKED'
        return finish()
    findings['resource_bounds'] = 'SATISFIED'
    if type(subject) is not ReferenceSubject or not all(digest(v) for v in (subject.brain_document_sha256, subject.epistemaddy_proposal_sha256, subject.source_database_sha256)) or type(subject.source_record_version) is not int or not 1 <= subject.source_record_version <= MAX_COORDINATE or any(type(v) is not str or not v or len(v) > 512 for v in (subject.source_candidate_id, subject.producer_scope)):
        findings['exact_subject'] = 'BLOCKED'
        return finish()
    try:
        subject.source_candidate_id.encode('utf-8', errors='strict')
        subject.producer_scope.encode('utf-8', errors='strict')
    except UnicodeError:
        findings['exact_subject'] = 'BLOCKED'
        return finish()
    if sha(brain_bytes) != subject.brain_document_sha256 or sha(producer_bytes) != subject.epistemaddy_proposal_sha256:
        findings['exact_subject'] = 'BLOCKED'
        return finish()
    subject_pin = sha(json.dumps({field:getattr(subject,field) for field in ReferenceSubject.__dataclass_fields__},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
    verified_brain = sha(brain_bytes); verified_producer = sha(producer_bytes)
    findings['exact_subject'] = 'SATISFIED'
    try:
        brain = bounded_json(brain_bytes); producer = bounded_json(producer_bytes)
        if type(brain) is not dict or set(brain) != {'proposal', 'schema_id', 'schema_version', 'serialization_profile'}:
            raise ValueError('BRAIN_FIELDS')
        if any(type(brain[key]) is not str or brain[key] != value for key, value in {'schema_id':'anarchi.brain.proposal','schema_version':'1','serialization_profile':'ACS-1'}.items()):
            raise ValueError('BRAIN_SCHEMA')
        if type(producer) is not dict or set(producer) != {'content','contract','identity','jurisdiction','lineage','operation','producer','provenance','scope','source_identity','subject_identity','temporal_context'}:
            raise ValueError('PRODUCER_FIELDS')
        payload = brain['proposal']
        if type(payload) is not dict or set(payload) != {'adapter_profile','admission_state','attachment_resolution','authority_resolution','canonical_membership','database_sha256','epistemaddy_proposal_sha256','epistemaddy_proposal_utf8_base64','governing_baseline_adopted','producer_provenance','purpose','required_cycle','source_authenticity','source_candidate_id','source_exact_record_sha256','source_normalization_profile','source_normalized_record_sha256','source_package_id','source_record_utf8_base64','source_record_version','visibility_resolution'}:
            raise ValueError('PAYLOAD_FIELDS')
        original = base64.b64decode(payload['source_record_utf8_base64'], validate=True)
        bounded_json(original)
        findings['structure'] = 'SATISFIED'
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError):
        findings['structure'] = 'BLOCKED'
        return finish()
    try:
        dependencies.custody.verify_pair(brain_bytes, producer_bytes, subject.brain_document_sha256, subject.epistemaddy_proposal_sha256)
        findings['provenance'] = 'SATISFIED'
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError):
        findings['provenance'] = 'BLOCKED'
    try:
        expected = dependencies.mapping.ReferenceSubject(*(getattr(subject, field) for field in ReferenceSubject.__dataclass_fields__))
        observed = dependencies.mapping.ReferenceSubject(sha(brain_bytes), payload['epistemaddy_proposal_sha256'], payload['database_sha256'], payload['source_candidate_id'], payload['source_record_version'], producer['scope'])
        request = dependencies.mapping.fixture_request(observed, 'brain-offline-candidate-review', MAPPING_CONTRACT_PIN)
        mapped = dependencies.mapping.check_mapping(request, expected, MAPPING_CONTRACT_PIN)
        findings['mapping'] = 'SATISFIED' if mapped.disposition == 'MAPPING_SHAPE_COMPATIBLE' and mapped.runtime_crossing_permitted is False and mapped.canonical_membership is False else 'BLOCKED'
    except (ValueError, TypeError, KeyError, AttributeError):
        findings['mapping'] = 'BLOCKED'
    if type(snapshot) is not Snapshot or type(snapshot.profile) is not str or snapshot.profile != 'OFFLINE_FIXTURE_ONLY' or not digest(snapshot.expected_root_sha256) or snapshot.observed_root_sha256 is not None and not digest(snapshot.observed_root_sha256) or type(snapshot.expected_epoch) is not int or not 0 <= snapshot.expected_epoch <= MAX_COORDINATE or snapshot.observed_epoch is not None and (type(snapshot.observed_epoch) is not int or not 0 <= snapshot.observed_epoch <= MAX_COORDINATE):
        findings['fixture_freshness'] = 'BLOCKED'
        return finish()
    context_pin = sha(json.dumps({field:getattr(snapshot,field) for field in Snapshot.__dataclass_fields__},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
    relation = 'UNKNOWN' if snapshot.observed_root_sha256 is None else 'EQUAL' if snapshot.observed_root_sha256 == snapshot.expected_root_sha256 else 'DIFFERENT'
    freshness = 'UNKNOWN' if snapshot.observed_epoch is None else 'CURRENT' if snapshot.observed_epoch == snapshot.expected_epoch else 'STALE'
    routed = dependencies.m08.atlas_denial_route('MATCH', 'MATCH', relation, freshness, 'UNRESOLVED')
    m08_summary = tuple((key, routed[key]) for key in ('route_event', 'route_outcome', 'target_state', 'ordinary_access'))
    findings['fixture_freshness'] = 'BLOCKED' if relation == 'DIFFERENT' or freshness == 'STALE' else 'UNRESOLVED' if relation == 'UNKNOWN' or freshness == 'UNKNOWN' else 'SATISFIED'
    predicates = {'exact_subject': findings['exact_subject'], 'applicable_semantics': 'UNRESOLVED', 'current_predecessor': findings['fixture_freshness'], 'authority_root_freshness': 'UNRESOLVED', 'resource_bounds': findings['resource_bounds']}
    described = dependencies.m03.describe_transition('normalize_with_provenance', {}, predicates)
    m03_summary = tuple((key, described[key]) for key in ('outcome','state','operation_effect','ordinary_access','canonical_membership'))
    return finish()
