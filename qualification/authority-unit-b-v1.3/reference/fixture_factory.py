"""Synthetic documentary fixtures; no roots, principals, signatures or grants enrolled."""
import copy,hashlib,json,pathlib,importlib.util,sys
ROOT=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('unit_b_fixture_reference',ROOT/'authority_reference.py')
ref=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ref;spec.loader.exec_module(ref)

def h(value):return hashlib.sha256(value.encode()).hexdigest()
def raw(document):return ref.canonical(document)
def interpret(document):
    data=raw(document)
    return ref.evaluate(ref.validate(data,ref.sha(data)))
def bind_consumption(document):
    result=interpret(document)
    if result.context_digest is not None:
        c=document['consumption'];g=document['grant']
        authorization=document['authorization']
        c.update(grant_id=g['grant_id'],grant_digest=result.grant_digest,authorization_id=authorization['authorization_id'],authorization_version=authorization['authorization_version'],authorization_digest=result.authorization_digest,request_digest=result.request_digest,context_digest=result.context_digest,generation=g['generation'],evaluation_digest=result.base_evaluation_digest)
    return document

def positive(operation='CONSUME_PROJECTION_AUTHORIZATION'):
    principal_specs={
        'grant_issuer':('DOCUMENTARY_GRANT_ISSUER','ISSUE_DOCUMENTARY_AUTHORIZE_GRANT'),
        'issuer':('EXTERNAL_DOCUMENTARY_AUTHORIZER','ISSUE_DOCUMENTARY_AUTHORIZATION'),
        'verifier':('INDEPENDENT_DOCUMENTARY_VERIFIER','VERIFY_DOCUMENTARY_CONSUMPTION'),
        'grantee':('DOCUMENTARY_CONSUMER','CONSUME_DOCUMENTARY_AUTHORIZATION')}
    principals={role:{'principal_id':'fixture-principal-'+role,'principal_class':values[0],'authority_purpose':values[1],'jurisdiction':'UNIT_B_REFERENCE_ONLY','effective_controller_id':'fixture-controller-'+role,'admin_domain_id':'fixture-admin-'+role,'signing_custody_domain_id':'fixture-custody-'+role,'evidence_provenance_domain_id':'fixture-evidence-'+role,'authority_lineage_ref':'fixture-authority-lineage-'+role}for role,values in principal_specs.items()}
    keys={role:{'principal_id':principals[role]['principal_id'],'key_id':'fixture-key-'+role,'key_fingerprint':h('fixture-key-bytes-'+role),'generation':1,'activation_time':0,'predecessor_key_id':'NONE','issuer_authority_ref':'fixture-model-selection','verifier_admission_ref':'fixture-verifier-admission'}for role in principals}
    root_id='fixture-model-root';root_digest=h('fixture-model-root-bytes')
    lineage=[{'root_id':root_id,'root_digest':root_digest,'predecessor_root_digest':'NONE'}]
    projection=operation=='CONSUME_PROJECTION_AUTHORIZATION'
    request={'operation':operation,'subject_id':'fixture-subject','subject_version':1,'subject_digest':h('fixture-subject-bytes'),'tenant':'fixture-tenant','consumer':'fixture-consumer','job':'fixture-job','purpose':'fixture-noncanonical-review','recipient':'fixture-recipient','resource_id':'fixture-resource','resource_version':1,'resource_class':'NONCANONICAL_PROJECTION'if projection else'DERIVED_ATLAS_MAINTENANCE','effect_class':'PROJECTION_AUTHORIZATION_REFERENCE'if projection else'MAINTENANCE_AUTHORIZATION_REFERENCE','effect_description':'Prepare only a non-effecting documentary consumption reference.','effect_description_digest':h('Prepare only a non-effecting documentary consumption reference.'),'policy_digest':h('fixture-policy'),'contract_digest':h('fixture-reference-contract'),'predecessor_digest':'NONE','grantee_principal_id':principals['grantee']['principal_id']}
    request.update(effect_actor_principal_id=principals['grantee']['principal_id'],schema_id='fixture-effect-schema',schema_version=1,schema_digest=h('fixture-schema-bytes'))
    grant={key:value for key,value in request.items()if key!='effect_description'}
    grant.update(grant_id='fixture-grant',grant_version=1,issuer_principal_id=principals['grant_issuer']['principal_id'],issuer_key_id=keys['grant_issuer']['key_id'],grantee_principal_id=principals['issuer']['principal_id'],authority_dimension='Authorize',root_id=root_id,root_digest=root_digest,root_lineage=copy.deepcopy(lineage),generation=1,epoch=1,not_before=0,expires_at=20,revocation_ref='fixture-revocation-ref',delegation=False,verifier_admission_ref='fixture-verifier-admission',revocation_generation=1,revocation_state='ACTIVE',evidence_time=5,supersedes_grant_id='NONE')
    bootstrap={'documentary_status':'PRESENT_FIXTURE','selection_ref':'fixture-model-selection','bootstrap_procedure_digest':h('fixture-modeled-bootstrap-procedure'),'root_class':'DOCUMENTARY_REFERENCE_ROOT','root_id':root_id,'root_digest':root_digest,'root_generation':1,'root_lineage':copy.deepcopy(lineage),'genesis_predecessor':'NONE','effective_not_before':0,'authority_dimensions':['Authorize'],'minimum_generation':1,'minimum_epoch':1,'minimum_revocation_generation':1,'maximum_evidence_age':100,'admitted_principals':copy.deepcopy(principals),'admitted_key_bindings':copy.deepcopy(keys)}
    selection={'kind':'MODELED_GOVERNANCE_SELECTION_NOT_ADOPTED','selection_origin':'EXTERNAL_MODELED_GOVERNANCE','decision_ref':bootstrap['selection_ref'],'selected_bootstrap_sha256':ref.sha(ref.canonical(bootstrap)),'status':'SELECTED'}
    authorization={field:value for field,value in request.items()if field not in ('effect_description','grantee_principal_id')}
    authorization.update(authorization_id='fixture-issued-authorization',authorization_version=1,issuer_principal_id=principals['issuer']['principal_id'],issuer_key_id=keys['issuer']['key_id'],consumer_principal_id=principals['grantee']['principal_id'],verifier_principal_id=principals['verifier']['principal_id'],verifier_admission_ref='fixture-verifier-admission',decision_disposition='AUTHORIZE',grant_digest=ref.sha(ref.canonical(grant)),requested_effect_digest=ref.sha(ref.canonical(request)),root_id=root_id,root_digest=root_digest,generation=1,epoch=1,revocation_generation=1,evidence_time=6,issued_at=6,not_before=6,expires_at=18,conditions={'generation':'EXACT','epoch':'EXACT','revocation':'COMPLETE_FIXTURE','time':'BOUNDED_FIXTURE_WINDOW','prior_consumption':'NOT_CONSUMED','extra_conditions':'NONE'},revocation_ref='fixture-authorization-revocation',revocation_state='ACTIVE',supersedes_authorization_id='NONE')
    grant_attestation={'attestation_kind':'DOCUMENTARY_FIXTURE_BINDING','issuer_principal_id':grant['issuer_principal_id'],'issuer_key_id':grant['issuer_key_id'],'issuer_key_fingerprint':keys['grant_issuer']['key_fingerprint'],'grant_sha256':ref.sha(ref.canonical(grant)),'selection_ref':bootstrap['selection_ref'],'evidence_time':grant['evidence_time']}
    attestation={'attestation_kind':'DOCUMENTARY_FIXTURE_BINDING','issuer_principal_id':authorization['issuer_principal_id'],'issuer_key_id':authorization['issuer_key_id'],'issuer_key_fingerprint':keys['issuer']['key_fingerprint'],'grant_sha256':ref.sha(ref.canonical(grant)),'authorization_sha256':ref.sha(ref.canonical(authorization)),'selection_ref':bootstrap['selection_ref'],'evidence_time':authorization['evidence_time']}
    admission={'admission_kind':'DOCUMENTARY_FIXTURE_ADMISSION','admission_ref':grant['verifier_admission_ref'],'verifier_principal_id':principals['verifier']['principal_id'],'verifier_key_id':keys['verifier']['key_id'],'verifier_key_fingerprint':keys['verifier']['key_fingerprint'],'root_id':root_id,'root_digest':root_digest,'selection_ref':bootstrap['selection_ref']}
    observation={'root_status':'KNOWN_FIXTURE','root_id':root_id,'root_digest':root_digest,'root_generation':1,'generation':1,'epoch':1,'revocation_generation':1,'verifier_status':'KNOWN_FIXTURE','time_status':'KNOWN_FIXTURE','now_earliest':10,'now_latest':10,'principal_key_generations':{role:1 for role in principals},'revocation_feed_status':'COMPLETE_FIXTURE','revoked_refs':[],'denial_feed_status':'COMPLETE_FIXTURE','denials':[]}
    observation.update(authorization_revocation_feed_status='COMPLETE_FIXTURE',revoked_authorization_refs=[])
    consumption={'state':'NOT_CONSUMED','grant_id':grant['grant_id'],'grant_digest':'0'*64,'authorization_id':authorization['authorization_id'],'authorization_version':1,'authorization_digest':'0'*64,'request_digest':'0'*64,'context_digest':'0'*64,'generation':1,'evaluation_digest':'0'*64,'effect_observation':'NOT_OCCURRED','terminal_receipt_digest':None}
    return bind_consumption({'profile':'OFFLINE_FIXTURE_ONLY','grant':grant,'authorization':authorization,'requested_effect':request,'governance_selection':selection,'bootstrap':bootstrap,'principals':principals,'key_bindings':keys,'grant_attestation':grant_attestation,'issuer_attestation':attestation,'verifier_admission':admission,'current_observation':observation,'consumption':consumption})

def rebind_attestation(document):
    document['grant_attestation']['grant_sha256']=ref.sha(ref.canonical(document['grant']))
    document['grant_attestation']['evidence_time']=document['grant']['evidence_time']
    document['authorization']['grant_digest']=ref.sha(ref.canonical(document['grant']))
    document['authorization']['requested_effect_digest']=ref.sha(ref.canonical(document['requested_effect']))
    document['issuer_attestation']['grant_sha256']=ref.sha(ref.canonical(document['grant']))
    document['issuer_attestation']['authorization_sha256']=ref.sha(ref.canonical(document['authorization']))
    document['issuer_attestation']['evidence_time']=document['authorization']['evidence_time']
    return bind_consumption(document)

if __name__=='__main__':
    for operation in ref.SPEC['operations']:
        fixture=positive(operation);decision=interpret(fixture)
        print(json.dumps({'operation':operation,'disposition':decision.disposition,'nonallow_findings':[(name,value)for name,value in decision.findings if value!='ALLOW']}))
