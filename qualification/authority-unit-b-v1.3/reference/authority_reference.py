"""Pure documentary fixture model: no cryptographic authentication or runtime effects."""
import hashlib,json
from dataclasses import dataclass
SPEC=json.loads(r'''{
  "status": "PROPOSED_INTERFACE_FOR_COORDINATION",
  "profile": "OFFLINE_FIXTURE_ONLY",
  "limits": {
    "bytes": 65536,
    "depth": 32,
    "nodes": 5000,
    "text_chars": 512,
    "description_chars": 2048,
    "list_items": 64,
    "lineage_items": 8,
    "integer_max": 9223372036854775807
  },
  "operations": [
    "CONSUME_PROJECTION_AUTHORIZATION",
    "CONSUME_MAINTENANCE_AUTHORIZATION"
  ],
  "objects": {
    "bundle": {
      "profile": "profile",
      "grant": "grant",
      "requested_effect": "requested_effect",
      "governance_selection": "governance_selection",
      "bootstrap": "bootstrap",
      "principals": "principals",
      "key_bindings": "key_bindings",
      "issuer_attestation": "issuer_attestation",
      "verifier_admission": "verifier_admission",
      "current_observation": "current_observation",
      "consumption": "consumption",
      "authorization": "authorization",
      "grant_attestation": "grant_attestation"
    },
    "grant": {
      "grant_id": "text",
      "grant_version": "positive_int",
      "issuer_principal_id": "text",
      "issuer_key_id": "text",
      "grantee_principal_id": "text",
      "authority_dimension": "text",
      "operation": "operation",
      "subject_id": "text",
      "subject_version": "positive_int",
      "subject_digest": "digest",
      "tenant": "text",
      "consumer": "text",
      "job": "text",
      "purpose": "text",
      "recipient": "text",
      "resource_id": "text",
      "resource_version": "positive_int",
      "resource_class": "text",
      "effect_class": "text",
      "effect_description_digest": "digest",
      "policy_digest": "digest",
      "contract_digest": "digest",
      "predecessor_digest": "digest_or_none_tag",
      "root_id": "text",
      "root_digest": "digest",
      "root_lineage": "lineage",
      "generation": "nonnegative_int",
      "epoch": "nonnegative_int",
      "not_before": "nonnegative_int",
      "expires_at": "nonnegative_int",
      "revocation_ref": "text",
      "delegation": "bool",
      "verifier_admission_ref": "text",
      "revocation_generation": "nonnegative_int",
      "revocation_state": "revocation_state",
      "evidence_time": "nonnegative_int",
      "effect_actor_principal_id": "text",
      "schema_id": "text",
      "schema_version": "positive_int",
      "schema_digest": "digest",
      "supersedes_grant_id": "text"
    },
    "requested_effect": {
      "operation": "operation",
      "subject_id": "text",
      "subject_version": "positive_int",
      "subject_digest": "digest",
      "tenant": "text",
      "consumer": "text",
      "job": "text",
      "purpose": "text",
      "recipient": "text",
      "resource_id": "text",
      "resource_version": "positive_int",
      "resource_class": "text",
      "effect_class": "text",
      "effect_description": "description",
      "effect_description_digest": "digest",
      "policy_digest": "digest",
      "contract_digest": "digest",
      "predecessor_digest": "digest_or_none_tag",
      "grantee_principal_id": "text",
      "effect_actor_principal_id": "text",
      "schema_id": "text",
      "schema_version": "positive_int",
      "schema_digest": "digest"
    },
    "governance_selection": {
      "kind": "governance_kind",
      "selection_origin": "selection_origin",
      "decision_ref": "text",
      "selected_bootstrap_sha256": "digest",
      "status": "selection_status"
    },
    "bootstrap": {
      "documentary_status": "documentary_status",
      "selection_ref": "text",
      "bootstrap_procedure_digest": "digest",
      "root_class": "text",
      "root_id": "text",
      "root_digest": "digest",
      "root_generation": "nonnegative_int",
      "root_lineage": "lineage",
      "genesis_predecessor": "digest_or_none_tag",
      "effective_not_before": "nonnegative_int",
      "authority_dimensions": "texts",
      "minimum_generation": "nonnegative_int",
      "minimum_epoch": "nonnegative_int",
      "minimum_revocation_generation": "nonnegative_int",
      "maximum_evidence_age": "nonnegative_int",
      "admitted_principals": "principals",
      "admitted_key_bindings": "key_bindings"
    },
    "principals": {
      "issuer": "principal",
      "verifier": "principal",
      "grantee": "principal",
      "grant_issuer": "principal"
    },
    "principal": {
      "principal_id": "text",
      "principal_class": "text",
      "authority_purpose": "text",
      "jurisdiction": "text",
      "effective_controller_id": "text",
      "admin_domain_id": "text",
      "signing_custody_domain_id": "text",
      "evidence_provenance_domain_id": "text",
      "authority_lineage_ref": "text"
    },
    "key_bindings": {
      "issuer": "key_binding",
      "verifier": "key_binding",
      "grantee": "key_binding",
      "grant_issuer": "key_binding"
    },
    "key_binding": {
      "principal_id": "text",
      "key_id": "text",
      "key_fingerprint": "digest",
      "generation": "nonnegative_int",
      "activation_time": "nonnegative_int",
      "predecessor_key_id": "text",
      "issuer_authority_ref": "text",
      "verifier_admission_ref": "text"
    },
    "issuer_attestation": {
      "attestation_kind": "attestation_kind",
      "issuer_principal_id": "text",
      "issuer_key_id": "text",
      "issuer_key_fingerprint": "digest",
      "grant_sha256": "digest",
      "selection_ref": "text",
      "evidence_time": "nonnegative_int",
      "authorization_sha256": "digest"
    },
    "verifier_admission": {
      "admission_kind": "admission_kind",
      "admission_ref": "text",
      "verifier_principal_id": "text",
      "verifier_key_id": "text",
      "verifier_key_fingerprint": "digest",
      "root_id": "text",
      "root_digest": "digest",
      "selection_ref": "text"
    },
    "current_observation": {
      "root_status": "observation_status",
      "root_id": "nullable_text",
      "root_digest": "nullable_digest",
      "root_generation": "nullable_int",
      "generation": "nullable_int",
      "epoch": "nullable_int",
      "revocation_generation": "nullable_int",
      "verifier_status": "verifier_status",
      "time_status": "observation_status",
      "now_earliest": "nullable_int",
      "now_latest": "nullable_int",
      "principal_key_generations": "observed_key_generations",
      "revocation_feed_status": "feed_status",
      "revoked_refs": "texts",
      "denial_feed_status": "feed_status",
      "denials": "denials",
      "authorization_revocation_feed_status": "feed_status",
      "revoked_authorization_refs": "texts"
    },
    "observed_key_generations": {
      "issuer": "nullable_int",
      "verifier": "nullable_int",
      "grantee": "nullable_int",
      "grant_issuer": "nullable_int"
    },
    "denial": {
      "denial_id": "text",
      "scope": "requested_effect",
      "source_ref": "text"
    },
    "consumption": {
      "state": "consumption_state",
      "grant_id": "text",
      "grant_digest": "digest",
      "request_digest": "digest",
      "context_digest": "digest",
      "generation": "nonnegative_int",
      "evaluation_digest": "digest",
      "effect_observation": "effect_observation",
      "terminal_receipt_digest": "nullable_digest",
      "authorization_id": "text",
      "authorization_version": "positive_int",
      "authorization_digest": "digest"
    },
    "lineage_entry": {
      "root_id": "text",
      "root_digest": "digest",
      "predecessor_root_digest": "digest_or_none_tag"
    },
    "grant_attestation": {
      "attestation_kind": "attestation_kind",
      "issuer_principal_id": "text",
      "issuer_key_id": "text",
      "issuer_key_fingerprint": "digest",
      "grant_sha256": "digest",
      "selection_ref": "text",
      "evidence_time": "nonnegative_int"
    },
    "authorization": {
      "operation": "operation",
      "subject_id": "text",
      "subject_version": "positive_int",
      "subject_digest": "digest",
      "tenant": "text",
      "consumer": "text",
      "job": "text",
      "purpose": "text",
      "recipient": "text",
      "resource_id": "text",
      "resource_version": "positive_int",
      "resource_class": "text",
      "effect_class": "text",
      "effect_description_digest": "digest",
      "policy_digest": "digest",
      "contract_digest": "digest",
      "predecessor_digest": "digest_or_none_tag",
      "authorization_id": "text",
      "authorization_version": "positive_int",
      "issuer_principal_id": "text",
      "issuer_key_id": "text",
      "consumer_principal_id": "text",
      "verifier_principal_id": "text",
      "verifier_admission_ref": "text",
      "decision_disposition": "authorization_disposition",
      "grant_digest": "digest",
      "requested_effect_digest": "digest",
      "root_id": "text",
      "root_digest": "digest",
      "generation": "nonnegative_int",
      "epoch": "nonnegative_int",
      "revocation_generation": "nonnegative_int",
      "evidence_time": "nonnegative_int",
      "issued_at": "nonnegative_int",
      "not_before": "nonnegative_int",
      "expires_at": "nonnegative_int",
      "conditions": "authorization_conditions",
      "effect_actor_principal_id": "text",
      "schema_id": "text",
      "schema_version": "positive_int",
      "schema_digest": "digest",
      "revocation_ref": "text",
      "revocation_state": "revocation_state",
      "supersedes_authorization_id": "text"
    },
    "authorization_conditions": {
      "generation": "text",
      "epoch": "text",
      "revocation": "text",
      "time": "text",
      "prior_consumption": "text",
      "extra_conditions": "text"
    }
  },
  "enums": {
    "profile": [
      "OFFLINE_FIXTURE_ONLY"
    ],
    "operation": [
      "CONSUME_PROJECTION_AUTHORIZATION",
      "CONSUME_MAINTENANCE_AUTHORIZATION"
    ],
    "governance_kind": [
      "MODELED_GOVERNANCE_SELECTION_NOT_ADOPTED"
    ],
    "selection_origin": [
      "EXTERNAL_MODELED_GOVERNANCE",
      "ROOT_SELF_ATTESTATION"
    ],
    "selection_status": [
      "SELECTED",
      "UNKNOWN",
      "CONFLICT"
    ],
    "documentary_status": [
      "PRESENT_FIXTURE",
      "MISSING",
      "CONFLICT"
    ],
    "revocation_state": [
      "ACTIVE",
      "REVOKED",
      "UNKNOWN"
    ],
    "attestation_kind": [
      "DOCUMENTARY_FIXTURE_BINDING",
      "SELF_ATTESTED_ROOT"
    ],
    "admission_kind": [
      "DOCUMENTARY_FIXTURE_ADMISSION",
      "SELF_ADMISSION"
    ],
    "observation_status": [
      "KNOWN_FIXTURE",
      "UNKNOWN",
      "CONFLICT"
    ],
    "feed_status": [
      "COMPLETE_FIXTURE",
      "UNKNOWN"
    ],
    "consumption_state": [
      "NOT_CONSUMED",
      "PREPARED",
      "CONSUMED",
      "UNKNOWN"
    ],
    "effect_observation": [
      "NOT_OCCURRED",
      "OCCURRED",
      "UNKNOWN",
      "PARTIAL_EFFECT",
      "RECEIPT_WITHOUT_EFFECT",
      "EFFECT_WITHOUT_RECEIPT",
      "CRASH_AFTER_FENCE"
    ],
    "verifier_status": [
      "KNOWN_FIXTURE",
      "UNKNOWN",
      "COMPROMISED"
    ],
    "authorization_disposition": [
      "AUTHORIZE"
    ]
  }
}
''')
REQUIRED_INDEPENDENCE_PAIRS=(('grant_issuer','verifier'),('issuer','verifier'),('grantee','issuer'))
def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

def digest(value):
    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)

@dataclass(frozen=True)
class ValidationFailure:
    reason: str
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False
    actual_root_resolution: str='ROOT_UNRESOLVED'
    profile: str='OFFLINE_FIXTURE_ONLY'

@dataclass(frozen=True)
class ValidatedFixture:
    raw: bytes
    expected_sha256: str
    fixture_sha256: str
    canonical_document: bytes

@dataclass(frozen=True)
class GrantEvaluation:
    disposition: str
    findings: tuple
    grant_digest: str | None
    profile: str='OFFLINE_FIXTURE_ONLY'
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False

@dataclass(frozen=True)
class AuthorizationEvaluation:
    disposition: str
    findings: tuple
    authorization_digest: str | None
    parent_grant_digest: str | None
    profile: str='OFFLINE_FIXTURE_ONLY'
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False

@dataclass(frozen=True)
class ConsumptionEvaluation:
    disposition: str
    findings: tuple
    authorization_digest: str | None
    context_digest: str | None
    profile: str='OFFLINE_FIXTURE_ONLY'
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False

@dataclass(frozen=True)
class Decision:
    disposition: str
    findings: tuple
    fixture_sha256: str | None
    context_digest: str | None
    grant_digest: str | None
    request_digest: str | None
    base_evaluation_digest: str | None
    authorization_digest: str | None
    root_model_satisfied: bool=False
    grant_evaluation: GrantEvaluation | None=None
    authorization_evaluation: AuthorizationEvaluation | None=None
    consumption_evaluation: ConsumptionEvaluation | None=None
    evaluator_version: str='UNIT_B_DOCUMENTARY_REFERENCE_1'
    actual_root_resolution: str='ROOT_UNRESOLVED'
    actual_issuer_authentication: str='UNRESOLVED'
    actual_control_independence: str='UNRESOLVED'
    signature_verification: str='NOT_PERFORMED'
    profile: str='OFFLINE_FIXTURE_ONLY'
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False

@dataclass(frozen=True)
class Preparation:
    disposition: str
    intent_digest: str | None
    fixture_sha256: str | None
    effect_outcome: str
    evaluator_version: str='UNIT_B_DOCUMENTARY_REFERENCE_1'
    profile: str='OFFLINE_FIXTURE_ONLY'
    runtime_authority: bool=False
    operative_grant: bool=False
    effect_permitted: bool=False
    durable_consumption: bool=False
    production_ready: bool=False

def bounded_parse(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('DUPLICATE_FIELD')
            result[key]=value
        return result
    def invalid_constant(value):raise ValueError('NONFINITE_JSON')
    value=json.loads(raw.decode('utf-8',errors='strict'),object_pairs_hook=pairs,parse_constant=invalid_constant)
    pending=[(value,0)];nodes=0
    while pending:
        current,depth=pending.pop();nodes+=1
        if nodes>SPEC['limits']['nodes'] or depth>SPEC['limits']['depth']:raise ValueError('RESOURCE_BOUND')
        if type(current) is dict:
            for key,item in current.items():
                key.encode('utf-8',errors='strict')
                if len(key)>SPEC['limits']['text_chars']:raise ValueError('KEY_BOUND')
                pending.append((item,depth+1))
        elif type(current) is list:
            if len(current)>SPEC['limits']['list_items']:raise ValueError('LIST_BOUND')
            pending.extend((item,depth+1)for item in current)
        elif type(current) is str:
            current.encode('utf-8',errors='strict')
            if len(current)>SPEC['limits']['description_chars']:raise ValueError('TEXT_BOUND')
        elif type(current) not in (int,bool,type(None)):raise ValueError('JSON_TYPE')
    return value

def check_type(value,kind):
    if kind in SPEC['objects']:
        fields=SPEC['objects'][kind]
        if type(value) is not dict or set(value)!=set(fields):raise ValueError('CLOSED_FIELDS')
        for field,field_kind in fields.items():check_type(value[field],field_kind)
    elif kind in SPEC['enums']:
        if type(value) is not str or value not in SPEC['enums'][kind]:raise ValueError('ENUM')
    elif kind in ('text','description'):
        bound=SPEC['limits']['description_chars']if kind=='description'else SPEC['limits']['text_chars']
        if type(value) is not str or not value or len(value)>bound:raise ValueError('TEXT_TYPE')
        value.encode('utf-8',errors='strict')
    elif kind=='digest':
        if not digest(value):raise ValueError('DIGEST_TYPE')
    elif kind=='digest_or_none_tag':
        if value!='NONE' and not digest(value):raise ValueError('PREDECESSOR_TYPE')
    elif kind in ('positive_int','nonnegative_int'):
        minimum=1 if kind=='positive_int'else 0
        if type(value) is not int or not minimum<=value<=SPEC['limits']['integer_max']:raise ValueError('INTEGER_TYPE')
    elif kind=='bool':
        if type(value) is not bool:raise ValueError('BOOLEAN_TYPE')
    elif kind.startswith('nullable_'):
        if value is not None:check_type(value,{'nullable_text':'text','nullable_digest':'digest','nullable_int':'nonnegative_int'}[kind])
    elif kind in ('texts','lineage','denials'):
        if type(value) is not list or len(value)>SPEC['limits']['list_items']:raise ValueError('ARRAY_TYPE')
        if kind=='lineage' and not 1<=len(value)<=SPEC['limits']['lineage_items']:raise ValueError('LINEAGE_BOUND')
        child={'texts':'text','lineage':'lineage_entry','denials':'denial'}[kind]
        for item in value:check_type(item,child)
        if kind=='texts' and len(set(value))!=len(value):raise ValueError('DUPLICATE_COORDINATE')
    else:raise ValueError('UNKNOWN_SCHEMA_TYPE')

def validate(raw,expected_sha256):
    if type(raw) is not bytes or not 0<len(raw)<=SPEC['limits']['bytes']:return ValidationFailure('BYTE_BOUND')
    if not digest(expected_sha256) or sha(raw)!=expected_sha256:return ValidationFailure('EXTERNAL_FIXTURE_PIN_MISMATCH')
    try:
        document=bounded_parse(raw);check_type(document,'bundle')
        if document['grant']['grant_version']!=1:raise ValueError('UNSUPPORTED_GRANT_VERSION')
        if document['authorization']['authorization_version']!=1:raise ValueError('UNSUPPORTED_AUTHORIZATION_VERSION')
        observation=document['current_observation']
        if observation['time_status']=='KNOWN_FIXTURE' and (observation['now_earliest'] is None or observation['now_latest'] is None or observation['now_earliest']>observation['now_latest']):raise ValueError('KNOWN_TIME_REQUIRES_ORDERED_BOUNDS')
        return ValidatedFixture(raw,expected_sha256,sha(raw),canonical(document))
    except (ValueError,TypeError,KeyError,UnicodeError,RecursionError):
        return ValidationFailure('INVALID_CLOSED_FIXTURE')

def revalidate(value):
    if type(value) is not ValidatedFixture:return None
    checked=validate(value.raw,value.expected_sha256)
    if type(checked) is not ValidatedFixture or checked!=value:return None
    return json.loads(checked.canonical_document)

def combine(findings):
    values=tuple(value for _,value in findings)
    for outcome in ('DENY','CONFLICT','UNRESOLVED'):
        if outcome in values:return outcome
    return 'ALLOW'

def evaluate(validated):
    document=revalidate(validated)
    if document is None:return Decision('DENY',(('validation','DENY'),),None,None,None,None,None,None,grant_evaluation=GrantEvaluation('UNRESOLVED',(('validation','UNRESOLVED'),),None),authorization_evaluation=AuthorizationEvaluation('UNRESOLVED',(('validation','UNRESOLVED'),),None,None),consumption_evaluation=ConsumptionEvaluation('DENY',(('validation','DENY'),),None,None))
    g=document['grant'];r=document['requested_effect'];b=document['bootstrap'];s=document['governance_selection']
    p=document['principals'];keys=document['key_bindings'];a=document['issuer_attestation'];ga=document['grant_attestation'];authorization=document['authorization'];v=document['verifier_admission'];o=document['current_observation'];c=document['consumption']
    findings=[]
    def add(name,value):findings.append((name,value))
    def match(name,left,right,mismatch='DENY'):add(name,'ALLOW' if left==right else mismatch)
    grant_digest=sha(canonical(g));request_digest=sha(canonical(r))
    authorization_digest=sha(canonical(authorization))
    context_digest=sha(canonical({key:value for key,value in document.items()if key!='consumption'}))
    add('validation','ALLOW')
    add('governance_selection','DENY' if s['selection_origin']=='ROOT_SELF_ATTESTATION'else 'CONFLICT' if s['status']=='CONFLICT'else 'UNRESOLVED' if s['status']=='UNKNOWN'else 'ALLOW')
    match('selected_bootstrap',s['selected_bootstrap_sha256'],sha(canonical(b)),'CONFLICT')
    match('selection_reference',s['decision_ref'],b['selection_ref'],'CONFLICT')
    add('bootstrap_presence',{'PRESENT_FIXTURE':'ALLOW','MISSING':'UNRESOLVED','CONFLICT':'CONFLICT'}[b['documentary_status']])
    match('root_class',b['root_class'],'DOCUMENTARY_REFERENCE_ROOT')
    match('grant_root',(g['root_id'],g['root_digest'],g['root_lineage']),(b['root_id'],b['root_digest'],b['root_lineage']),'CONFLICT')
    lineage=b['root_lineage']
    lineage_status='ALLOW' if len(lineage)==1 else 'UNRESOLVED'
    if lineage[0]['predecessor_root_digest']!='NONE' or b['genesis_predecessor']!='NONE':lineage_status='UNRESOLVED'
    if len({entry['root_id']for entry in lineage})!=len(lineage) or len({entry['root_digest']for entry in lineage})!=len(lineage):lineage_status='CONFLICT'
    if any(lineage[index]['predecessor_root_digest']!=lineage[index-1]['root_digest']for index in range(1,len(lineage))):lineage_status='CONFLICT'
    if (lineage[-1]['root_id'],lineage[-1]['root_digest'])!=(b['root_id'],b['root_digest']):lineage_status='CONFLICT'
    add('root_lineage',lineage_status)
    add('dimension','ALLOW' if g['authority_dimension']=='Authorize' and g['authority_dimension']in b['authority_dimensions']else 'DENY')
    for field in SPEC['objects']['requested_effect']:
        if field not in ('effect_description','grantee_principal_id'):
            match('grant_scope.'+field,g[field],r[field])
            match('authorization_scope.'+field,authorization[field],r[field])
    match('effect_description',sha(r['effect_description'].encode('utf-8')),r['effect_description_digest'])
    match('grant_effect_actor_admission',g['effect_actor_principal_id'],p['grantee']['principal_id'])
    match('authorization_effect_actor_admission',(authorization['effect_actor_principal_id'],r['effect_actor_principal_id']),(p['grantee']['principal_id'],p['grantee']['principal_id']))
    expected_class={'CONSUME_PROJECTION_AUTHORIZATION':('NONCANONICAL_PROJECTION','PROJECTION_AUTHORIZATION_REFERENCE'),'CONSUME_MAINTENANCE_AUTHORIZATION':('DERIVED_ATLAS_MAINTENANCE','MAINTENANCE_AUTHORIZATION_REFERENCE')}[r['operation']]
    match('effect_resource_class',(r['resource_class'],r['effect_class']),expected_class)
    add('delegation','DENY' if g['delegation']else 'ALLOW')
    add('grant_supersession','ALLOW' if g['supersedes_grant_id']=='NONE'else 'UNRESOLVED')
    expected_roles={
        'grant_issuer':('DOCUMENTARY_GRANT_ISSUER','ISSUE_DOCUMENTARY_AUTHORIZE_GRANT'),
        'issuer':('EXTERNAL_DOCUMENTARY_AUTHORIZER','ISSUE_DOCUMENTARY_AUTHORIZATION'),
        'verifier':('INDEPENDENT_DOCUMENTARY_VERIFIER','VERIFY_DOCUMENTARY_CONSUMPTION'),
        'grantee':('DOCUMENTARY_CONSUMER','CONSUME_DOCUMENTARY_AUTHORIZATION')}
    add('stable_principal_identity','ALLOW' if len({principal['principal_id']for principal in p.values()})==4 else 'DENY')
    for role in ('grant_issuer','issuer','verifier','grantee'):
        principal=p[role];key=keys[role]
        match('principal_selection.'+role,principal,b['admitted_principals'][role],'CONFLICT')
        match('principal_class.'+role,(principal['principal_class'],principal['authority_purpose'],principal['jurisdiction']),(*expected_roles[role],'UNIT_B_REFERENCE_ONLY'))
        match('key_selection.'+role,key,b['admitted_key_bindings'][role],'CONFLICT')
        match('key_principal.'+role,key['principal_id'],principal['principal_id'])
        match('key_authority_reference.'+role,key['issuer_authority_ref'],b['selection_ref'])
        match('key_verifier_reference.'+role,key['verifier_admission_ref'],g['verifier_admission_ref'])
        add('key_genesis.'+role,'ALLOW' if key['predecessor_key_id']=='NONE'else 'UNRESOLVED')
        observed=o['principal_key_generations'][role]
        add('key_freshness.'+role,'UNRESOLVED' if observed is None else 'ALLOW' if key['generation']==observed else 'CONFLICT')
    match('grant_issuer',g['issuer_principal_id'],p['grant_issuer']['principal_id'])
    match('grant_issuer_key',g['issuer_key_id'],keys['grant_issuer']['key_id'])
    match('grant_grantee_authorizer',g['grantee_principal_id'],p['issuer']['principal_id'])
    match('authorization_issuer_grant_grantee',authorization['issuer_principal_id'],g['grantee_principal_id'])
    match('authorization_issuer_key',authorization['issuer_key_id'],keys['issuer']['key_id'])
    match('authorization_consumer',(authorization['consumer_principal_id'],r['grantee_principal_id']),(p['grantee']['principal_id'],p['grantee']['principal_id']))
    match('authorization_verifier',(authorization['verifier_principal_id'],authorization['verifier_admission_ref']),(p['verifier']['principal_id'],g['verifier_admission_ref']))
    match('authorization_basis',(authorization['grant_digest'],authorization['requested_effect_digest']),(grant_digest,request_digest))
    match('authorization_context',(authorization['root_id'],authorization['root_digest'],authorization['generation'],authorization['epoch'],authorization['revocation_generation']),(g['root_id'],g['root_digest'],g['generation'],g['epoch'],g['revocation_generation']))
    add('issued_authorization_disposition','ALLOW'if authorization['decision_disposition']=='AUTHORIZE'else 'DENY')
    match('authorization_conditions',authorization['conditions'],{'generation':'EXACT','epoch':'EXACT','revocation':'COMPLETE_FIXTURE','time':'BOUNDED_FIXTURE_WINDOW','prior_consumption':'NOT_CONSUMED','extra_conditions':'NONE'})
    add('authorization_supersession','ALLOW' if authorization['supersedes_authorization_id']=='NONE'else 'UNRESOLVED')
    controls=('effective_controller_id','admin_domain_id','signing_custody_domain_id','evidence_provenance_domain_id','authority_lineage_ref')
    for left_role,right_role in REQUIRED_INDEPENDENCE_PAIRS:
        pair=left_role+'.'+right_role
        add('role_pair_identity.'+pair,'DENY' if p[left_role]['principal_id']==p[right_role]['principal_id'] or keys[left_role]['key_id']==keys[right_role]['key_id'] or keys[left_role]['key_fingerprint']==keys[right_role]['key_fingerprint']else 'ALLOW')
        for field in controls:
            left=p[left_role][field];right=p[right_role][field]
            add('independence.'+pair+'.'+field,'UNRESOLVED' if 'UNKNOWN'in (left,right)else 'CONFLICT' if left==right else 'ALLOW')
        left_controls={p[left_role][field]for field in controls if p[left_role][field]!='UNKNOWN'}
        right_controls={p[right_role][field]for field in controls if p[right_role][field]!='UNKNOWN'}
        add('cross_control_overlap.'+pair,'CONFLICT' if left_controls&right_controls else 'ALLOW')
    match('grant_attestation_binding',(ga['issuer_principal_id'],ga['issuer_key_id'],ga['issuer_key_fingerprint'],ga['grant_sha256'],ga['selection_ref'],ga['evidence_time']),(p['grant_issuer']['principal_id'],keys['grant_issuer']['key_id'],keys['grant_issuer']['key_fingerprint'],grant_digest,b['selection_ref'],g['evidence_time']))
    add('grant_attestation_kind','ALLOW' if ga['attestation_kind']=='DOCUMENTARY_FIXTURE_BINDING'else 'DENY')
    match('attestation_binding',(a['issuer_principal_id'],a['issuer_key_id'],a['issuer_key_fingerprint'],a['grant_sha256'],a['authorization_sha256'],a['selection_ref'],a['evidence_time']),(p['issuer']['principal_id'],keys['issuer']['key_id'],keys['issuer']['key_fingerprint'],grant_digest,authorization_digest,b['selection_ref'],authorization['evidence_time']))
    add('attestation_kind','ALLOW' if a['attestation_kind']=='DOCUMENTARY_FIXTURE_BINDING'else 'DENY')
    match('verifier_admission_binding',(v['admission_ref'],v['verifier_principal_id'],v['verifier_key_id'],v['verifier_key_fingerprint'],v['root_id'],v['root_digest'],v['selection_ref']),(g['verifier_admission_ref'],p['verifier']['principal_id'],keys['verifier']['key_id'],keys['verifier']['key_fingerprint'],b['root_id'],b['root_digest'],b['selection_ref']))
    add('verifier_admission_kind','ALLOW' if v['admission_kind']=='DOCUMENTARY_FIXTURE_ADMISSION'else 'DENY')
    add('verifier_observation',{'KNOWN_FIXTURE':'ALLOW','UNKNOWN':'UNRESOLVED','COMPROMISED':'DENY'}[o['verifier_status']])
    root_observed=(o['root_id'],o['root_digest'],o['root_generation'])
    root_expected=(b['root_id'],b['root_digest'],b['root_generation'])
    add('observed_root','UNRESOLVED' if o['root_status']=='UNKNOWN' or None in root_observed else 'CONFLICT' if o['root_status']=='CONFLICT' or root_observed!=root_expected else 'ALLOW')
    for field,floor in [('generation','minimum_generation'),('epoch','minimum_epoch'),('revocation_generation','minimum_revocation_generation')]:
        observed=o[field]
        add('current.'+field,'UNRESOLVED' if observed is None else 'CONFLICT' if observed<b[floor]else 'ALLOW' if g[field]==observed else 'DENY')
    time_status='ALLOW';earliest=o['now_earliest'];latest=o['now_latest']
    if o['time_status']=='CONFLICT' or earliest is not None and latest is not None and earliest>latest:time_status='CONFLICT'
    elif o['time_status']=='UNKNOWN' or earliest is None or latest is None:time_status='UNRESOLVED'
    add('time_observation',time_status)
    def temporal(name,start,end):
        if start>=end:add(name,'DENY')
        elif time_status!='ALLOW':add(name,'UNRESOLVED')
        elif latest<start or earliest>=end:add(name,'DENY')
        elif earliest<start or latest>=end:add(name,'UNRESOLVED')
        else:add(name,'ALLOW')
    temporal('grant_validity_window',g['not_before'],g['expires_at'])
    grant_authority_activation=max(b['effective_not_before'],keys['grant_issuer']['activation_time'])
    add('grant_evidence_authority_activation','ALLOW' if g['evidence_time']>=grant_authority_activation and g['not_before']>=grant_authority_activation else 'DENY')
    temporal('authorization_validity_window',authorization['not_before'],authorization['expires_at'])
    add('authorization_validity_subset','ALLOW' if g['not_before']<=authorization['not_before']<authorization['expires_at']<=g['expires_at']else 'DENY')
    add('authorization_issuance_order','ALLOW' if g['evidence_time']<=authorization['evidence_time']<=authorization['issued_at'] and g['not_before']<=authorization['issued_at']<g['expires_at'] and authorization['not_before']>=authorization['issued_at'] else 'DENY')
    add('authorization_issuance_key_activation','ALLOW' if keys['issuer']['activation_time']<=authorization['evidence_time']<=authorization['issued_at'] and g['not_before']<=authorization['evidence_time']<g['expires_at'] else 'DENY')
    add('authorization_issuance_observation','UNRESOLVED' if time_status!='ALLOW' else 'DENY' if authorization['issued_at']>latest else 'UNRESOLVED' if authorization['issued_at']>earliest else 'ALLOW')
    for role in keys:temporal('key_activation.'+role,keys[role]['activation_time'],SPEC['limits']['integer_max'])
    temporal('root_activation',b['effective_not_before'],SPEC['limits']['integer_max'])
    if time_status!='ALLOW':evidence_status='UNRESOLVED'
    elif g['evidence_time']>latest or earliest-g['evidence_time']>b['maximum_evidence_age']:evidence_status='DENY'
    elif g['evidence_time']>earliest or latest-g['evidence_time']>b['maximum_evidence_age']:evidence_status='UNRESOLVED'
    else:evidence_status='ALLOW'
    add('evidence_time',evidence_status)
    if time_status!='ALLOW':authorization_evidence_status='UNRESOLVED'
    elif authorization['evidence_time']>latest or earliest-authorization['evidence_time']>b['maximum_evidence_age']:authorization_evidence_status='DENY'
    elif authorization['evidence_time']>earliest or latest-authorization['evidence_time']>b['maximum_evidence_age']:authorization_evidence_status='UNRESOLVED'
    else:authorization_evidence_status='ALLOW'
    add('authorization_evidence_time',authorization_evidence_status)
    revocable_refs={g['revocation_ref'],g['grant_id'],g['root_id'],g['verifier_admission_ref']}|{p[role]['principal_id']for role in p}|{keys[role]['key_id']for role in keys}
    add('grant_revocation','DENY' if g['revocation_state']=='REVOKED' or revocable_refs&set(o['revoked_refs'])else 'UNRESOLVED' if g['revocation_state']=='UNKNOWN' or o['revocation_feed_status']=='UNKNOWN'else 'ALLOW')
    authorization_refs={authorization['authorization_id'],authorization['revocation_ref'],authorization['consumer_principal_id'],authorization['issuer_principal_id'],authorization['verifier_principal_id']}
    add('authorization_revocation','DENY' if authorization['revocation_state']=='REVOKED' or authorization_refs&set(o['revoked_authorization_refs'])else 'UNRESOLVED' if authorization['revocation_state']=='UNKNOWN' or o['authorization_revocation_feed_status']=='UNKNOWN'else 'ALLOW')
    add('explicit_denial','DENY' if any(record['scope']==r for record in o['denials'])else 'UNRESOLVED' if o['denial_feed_status']=='UNKNOWN'else 'ALLOW')
    authorization_names={'effect_description','effect_resource_class','attestation_binding','attestation_kind','issued_authorization_disposition','explicit_denial'}
    authorization_prefixes=('authorization_','independence.issuer.verifier.','independence.grantee.issuer.','role_pair_identity.issuer.verifier','role_pair_identity.grantee.issuer','cross_control_overlap.issuer.verifier','cross_control_overlap.grantee.issuer')
    grant_findings=tuple((name,value)for name,value in findings if name not in authorization_names and not name.startswith(authorization_prefixes))
    authorization_findings=tuple((name,value)for name,value in findings if name in authorization_names or name.startswith(authorization_prefixes))
    grant_evaluation=GrantEvaluation(combine(grant_findings),grant_findings,grant_digest)
    authorization_findings+=(('parent_grant_effectiveness',grant_evaluation.disposition),)
    add('parent_grant_effectiveness',grant_evaluation.disposition)
    authorization_evaluation=AuthorizationEvaluation(combine(authorization_findings),authorization_findings,authorization_digest,grant_digest)
    base_evaluation_digest=sha(canonical({'evaluator_version':'UNIT_B_DOCUMENTARY_REFERENCE_1','context_digest':context_digest,'grant_digest':grant_digest,'authorization_digest':authorization_digest,'request_digest':request_digest,'findings':findings,'disposition':combine(findings)}))
    consumption_expected=(g['grant_id'],grant_digest,authorization['authorization_id'],authorization['authorization_version'],authorization_digest,request_digest,context_digest,g['generation'],base_evaluation_digest)
    consumption_actual=(c['grant_id'],c['grant_digest'],c['authorization_id'],c['authorization_version'],c['authorization_digest'],c['request_digest'],c['context_digest'],c['generation'],c['evaluation_digest'])
    match('consumption_identity',consumption_actual,consumption_expected,'CONFLICT')
    state=c['state'];effect=c['effect_observation'];receipt=c['terminal_receipt_digest']
    if effect in ('UNKNOWN','PARTIAL_EFFECT','RECEIPT_WITHOUT_EFFECT','EFFECT_WITHOUT_RECEIPT','CRASH_AFTER_FENCE') or state in ('PREPARED','UNKNOWN') or state=='CONSUMED'and (receipt is None or effect!='OCCURRED'):
        consumed_status='UNRESOLVED'
    elif state=='CONSUMED':consumed_status='DENY'
    elif state=='NOT_CONSUMED'and (effect!='NOT_OCCURRED' or receipt is not None):consumed_status='CONFLICT'
    else:consumed_status='ALLOW'
    add('consumption_state',consumed_status)
    add('parent_authorization_effectiveness',authorization_evaluation.disposition)
    consumption_findings=tuple((name,value)for name,value in findings if name in ('consumption_identity','consumption_state','parent_authorization_effectiveness'))
    consumption_evaluation=ConsumptionEvaluation(combine(consumption_findings),consumption_findings,authorization_digest,context_digest)
    root_model_satisfied=all(value=='ALLOW'for name,value in findings if name in ('governance_selection','selected_bootstrap','selection_reference','bootstrap_presence','root_class','grant_root','root_lineage','observed_root','root_activation'))
    return Decision(combine(findings),tuple(findings),validated.fixture_sha256,context_digest,grant_digest,request_digest,base_evaluation_digest,authorization_digest,root_model_satisfied,grant_evaluation,authorization_evaluation,consumption_evaluation)

def prepare_consumption(validated,decision):
    fresh=evaluate(validated)
    if type(decision) is not Decision or decision!=fresh:return Preparation('DENY',None,fresh.fixture_sha256,'EFFECT_OUTCOME_UNRESOLVED')
    document=revalidate(validated)
    if fresh.disposition!='ALLOW' or document is None:
        return Preparation(fresh.disposition,None,fresh.fixture_sha256,'EFFECT_OUTCOME_UNRESOLVED')
    identity={'evaluator_version':fresh.evaluator_version,'fixture_sha256':fresh.fixture_sha256,'context_digest':fresh.context_digest,'grant_digest':fresh.grant_digest,'authorization_id':document['authorization']['authorization_id'],'authorization_version':document['authorization']['authorization_version'],'authorization_digest':fresh.authorization_digest,'request_digest':fresh.request_digest,'evaluation_digest':fresh.base_evaluation_digest,'generation':document['grant']['generation'],'operation':document['requested_effect']['operation'],'stage':'PREPARE_REFERENCE_ONLY_NOT_DURABLE_CONSUMPTION'}
    return Preparation('PREPARATION_READY_REFERENCE_ONLY',sha(canonical(identity)),fresh.fixture_sha256,'REFERENCE_ONLY_NO_EFFECT_ATTEMPTED')
