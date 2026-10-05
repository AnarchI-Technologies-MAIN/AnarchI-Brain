"""Pure draft mapping reference. No transport, state transition or authority grant."""
from dataclasses import dataclass

PROFILE='EPI-BRAIN-FILAMENT-MAPPING-DRAFT-1.3'
BASELINE_CATALOG='421b5d5bab28a32afe557e17970a14beb75a99eddc9f536a75bb1bcda9d26eb3'

BASELINE_ACCEPTANCE='10bd8c050b4a39553a553bdad868f14a4f680709cb4c2b9669d01084ab3fd2bc'
BASELINE_RETENTION='8aa2d5af0c3f46d0fba46e784d86d459d104954467552a9dad0a6b8849da8742'

@dataclass(frozen=True)
class ReferenceSubject:
    brain_document_sha256:str
    epistemaddy_proposal_sha256:str
    source_database_sha256:str
    source_candidate_id:str
    source_record_version:int
    producer_scope:str

@dataclass(frozen=True)
class MappingResult:
    disposition:str
    reason:str
    runtime_crossing_permitted:bool=False
    content_admission:str='UNRESOLVED'
    semantic_resolution:str='UNRESOLVED'
    visibility_resolution:str='UNRESOLVED'
    operative_authority:str='UNRESOLVED'
    canonical_membership:bool=False

def check_mapping(request, subject, mapping_contract_sha256):
    """Caller supplies a reference subject; this function authenticates no principal."""
    def reject(reason):return MappingResult('MAPPING_REJECTED',reason)
    if type(mapping_contract_sha256)is not str or len(mapping_contract_sha256)!=64 or any(c not in '0123456789abcdef'for c in mapping_contract_sha256):return reject('INVALID_MAPPING_CONTRACT_DIGEST')
    if type(subject) is not ReferenceSubject:return reject('UNSUPPORTED_REFERENCE_SUBJECT')
    for value in [subject.brain_document_sha256,subject.epistemaddy_proposal_sha256,subject.source_database_sha256]:
        if type(value) is not str or len(value)!=64 or any(c not in '0123456789abcdef'for c in value):return reject('INVALID_REFERENCE_DIGEST')
    if type(subject.source_record_version) is not int or subject.source_record_version<1:return reject('INVALID_REFERENCE_VERSION')
    if any(type(value)is not str or not value or len(value)>512 for value in [subject.source_candidate_id,subject.producer_scope]):return reject('INVALID_REFERENCE_IDENTITY')
    if type(request)is not dict:return reject('UNSUPPORTED_MAPPING_REQUEST')
    expected_fields={'profile','mapping_contract_sha256','baseline_catalog_sha256','baseline_acceptance_sha256','baseline_retention_sha256','direction','operation','source_boundary','source_cortex_role','target_boundary','target_cortex_role','purpose','subject','requested_ingress_scope','producer_principal_resolution','submission_permission_resolution','requested_visibility_resolution','source_provenance_resolution','governing_baseline_adopted','runtime_activation','canonical_membership','attachment_handling','receipt_kind'}
    if set(request)!=expected_fields:return reject('MAPPING_FIELDS')
    fixed={
        'profile':PROFILE,'mapping_contract_sha256':mapping_contract_sha256,'baseline_catalog_sha256':BASELINE_CATALOG,'baseline_acceptance_sha256':BASELINE_ACCEPTANCE,'baseline_retention_sha256':BASELINE_RETENTION,
        'direction':'EPISTEMADDY_TO_BRAIN','operation':'SUBMIT_NONCANONICAL_PROPOSAL',
        'source_boundary':'epistemaddy.filament','source_cortex_role':'ACTIVE_COGNITIVE_JURISDICTION',
        'target_boundary':'brain.Cortex.ingress','target_cortex_role':'GOVERNED_INGRESS_BOUNDARY',
        'purpose':'noncanonical.offline.candidate-review',
        'producer_principal_resolution':'UNRESOLVED','submission_permission_resolution':'UNRESOLVED',
        'requested_visibility_resolution':'UNRESOLVED',
        'source_provenance_resolution':'REFERENCE_BYTES_BOUND_NOT_PRINCIPAL_AUTHENTICATED',
        'attachment_handling':'OPAQUE_PINNED_NO_EXECUTION','receipt_kind':'NO_RUNTIME_RECEIPT'}
    for field,value in fixed.items():
        if type(request[field])is not str or request[field]!=value:return reject('MAPPING_VALUE:'+field)
    if request['governing_baseline_adopted'] is not True:return reject('BASELINE_CONTEXT_MISMATCH')
    for field in ['runtime_activation','canonical_membership']:
        if request[field] is not False:return reject('FORBIDDEN_EFFECT_CLAIM:'+field)
    scope=request['requested_ingress_scope']
    if type(scope)is not str or not scope or len(scope)>512:return reject('INVALID_REQUESTED_SCOPE')
    values=request['subject']
    if type(values)is not dict or set(values)!=set(subject.__dataclass_fields__):return reject('SUBJECT_FIELDS')
    for field in subject.__dataclass_fields__:
        expected=getattr(subject,field)
        if type(values[field])is not type(expected) or values[field]!=expected:return reject('SUBJECT_MISMATCH:'+field)
    return MappingResult('MAPPING_SHAPE_COMPATIBLE','RUNTIME_PREREQUISITES_UNRESOLVED')

def fixture_request(subject, requested_scope, mapping_contract_sha256):
    """Reference fixture only; requested scope is not derived as an authority grant."""
    return {'profile':PROFILE,'mapping_contract_sha256':mapping_contract_sha256,'baseline_catalog_sha256':BASELINE_CATALOG,'baseline_acceptance_sha256':BASELINE_ACCEPTANCE,'baseline_retention_sha256':BASELINE_RETENTION,
        'direction':'EPISTEMADDY_TO_BRAIN','operation':'SUBMIT_NONCANONICAL_PROPOSAL',
        'source_boundary':'epistemaddy.filament','source_cortex_role':'ACTIVE_COGNITIVE_JURISDICTION',
        'target_boundary':'brain.Cortex.ingress','target_cortex_role':'GOVERNED_INGRESS_BOUNDARY',
        'purpose':'noncanonical.offline.candidate-review',
        'subject':{field:getattr(subject,field)for field in subject.__dataclass_fields__},
        'requested_ingress_scope':requested_scope,
        'producer_principal_resolution':'UNRESOLVED','submission_permission_resolution':'UNRESOLVED',
        'requested_visibility_resolution':'UNRESOLVED',
        'source_provenance_resolution':'REFERENCE_BYTES_BOUND_NOT_PRINCIPAL_AUTHENTICATED',
        'governing_baseline_adopted':True,'runtime_activation':False,'canonical_membership':False,
        'attachment_handling':'OPAQUE_PINNED_NO_EXECUTION','receipt_kind':'NO_RUNTIME_RECEIPT'}
