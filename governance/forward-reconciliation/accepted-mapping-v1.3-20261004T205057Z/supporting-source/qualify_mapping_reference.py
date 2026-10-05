"""Bind a draft mapping reference to the previously qualified offline corpus."""
import argparse,hashlib,importlib.util,json,pathlib,sys
from dataclasses import asdict

ROOT=pathlib.Path(__file__).parent
REPAIR_REPORT_PIN='5826e6b8cce74a5554d6045f45ac7ac71971a13f19f61754dbff6139f57e54a8'

def require(condition,reason):
    if not condition:raise ValueError(reason)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def captured_module(name,raw,path):
    module=importlib.util.module_from_spec(importlib.util.spec_from_loader(name,loader=None))
    module.__file__=str(path);sys.modules[name]=module
    exec(compile(raw,str(path),'exec',dont_inherit=True),module.__dict__)
    return module

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapping-sha256',required=True)
    parser.add_argument('--mapping-contract-sha256',required=True)
    parser.add_argument('--source-register-sha256',required=True)
    parser.add_argument('--baseline-acceptance-sha256',required=True)
    parser.add_argument('--baseline-retention-sha256',required=True)
    parser.add_argument('--out',type=pathlib.Path,required=True)
    args=parser.parse_args()
    mapping_raw=(ROOT/'mapping_reference.py').read_bytes()
    require(sha(mapping_raw)==args.mapping_sha256,'MAPPING_SOURCE_DRIFT')
    m=captured_module('captured_mapping',mapping_raw,ROOT/'mapping_reference.py')
    contract_raw=(ROOT/'CORTEX-FILAMENT-MAPPING-DRAFT.md').read_bytes()
    require(sha(contract_raw)==args.mapping_contract_sha256,'MAPPING_CONTRACT_DRIFT')
    register_raw=(ROOT/'source-register.json').read_bytes()
    require(sha(register_raw)==args.source_register_sha256,'SOURCE_REGISTER_DRIFT')
    upstream=json.loads(register_raw)
    require(set(upstream)=={'brain_cortex_candidate','brain_dimensions_candidate','forward_baseline_catalog','epistemaddy_main_contract','epistemaddy_junction_contract','qualified_offline_handoff','brain_m01_reference','forward_baseline_acceptance','forward_baseline_retention'},'UPSTREAM_REGISTER_MEMBERSHIP')
    for label,entry in upstream.items():
        require(entry['path']=='inputs/'+label+'.source','UPSTREAM_PATH_MAPPING')
        upstream_path=(ROOT/entry['path']).resolve(strict=True)
        require(upstream_path.is_relative_to(ROOT.resolve()),'UPSTREAM_PATH_ESCAPE')
        upstream_raw=upstream_path.read_bytes()
        require(len(upstream_raw)==entry['bytes'] and sha(upstream_raw)==entry['sha256'],'UPSTREAM_SOURCE_DRIFT:'+label)
    catalog=json.loads((ROOT/upstream['forward_baseline_catalog']['path']).read_bytes())
    verify_dependency_membership(m,upstream,catalog)
    baseline_context=verify_baseline_context(m,upstream,catalog,args.baseline_acceptance_sha256,args.baseline_retention_sha256)
    atlas=ROOT.parent/'atlas-ubuntu-substrate-20261004'
    report_raw=(atlas/'FINAL-HANDOFF-REPAIR-RESULT.json').read_bytes()
    require(sha(report_raw)==REPAIR_REPORT_PIN,'PRIOR_REPAIR_REPORT_DRIFT')
    prior=json.loads(report_raw)
    verifier_raw=(atlas/'verify_handoff_v5_1.py').read_bytes()
    verifier_pin=prior['focused_results']['source_pins']['verify_handoff_v5_1.py']
    require(sha(verifier_raw)==verifier_pin,'CUSTODY_VERIFIER_DRIFT')
    v=captured_module('captured_handoff_verifier',verifier_raw,atlas/'verify_handoff_v5_1.py')
    descriptor=next(r for r in prior['full_corpus_runs']if r['producer_version']=='v5.1')
    output=atlas/descriptor['output']
    custody=v.verify_output(output,descriptor['qualification_sha256'])
    checked=0;decisions=[]
    with (output/'proposals.jsonl').open('rb')as stream:
        for line in stream:
            brain_raw=line[:-1];doc=json.loads(brain_raw);payload=doc['proposal']
            subject=m.ReferenceSubject(sha(brain_raw),payload['epistemaddy_proposal_sha256'],payload['database_sha256'],payload['source_candidate_id'],payload['source_record_version'],json.loads(__import__('base64').b64decode(payload['epistemaddy_proposal_utf8_base64']))['scope'])
            request=m.fixture_request(subject,'brain-offline-candidate-review',args.mapping_contract_sha256)
            result=m.check_mapping(request,subject,args.mapping_contract_sha256)
            require(result.disposition=='MAPPING_SHAPE_COMPATIBLE','CORPUS_MAPPING_REJECTION')
            require(result.runtime_crossing_permitted is False and result.canonical_membership is False,'MAPPING_EFFECT_ESCALATION')
            decisions.append({'subject_sha256':subject.brain_document_sha256,'result':asdict(result)})
            checked+=1
    require(checked==2736,'CORPUS_CARDINALITY')
    result=qualification_receipt(mapping_raw,contract_raw,register_raw,upstream,custody,decisions,baseline_context)
    with args.out.open('x',encoding='utf-8')as destination:destination.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key]for key in ['status','checked_subjects','canonical_admissions','runtime_crossings','production_ready']}))

def verify_dependency_membership(mapping,upstream,catalog):
    require(mapping.BASELINE_CATALOG==upstream['forward_baseline_catalog']['sha256'],'BASELINE_CATALOG_MEMBERSHIP')
    selected=catalog['selected_candidate_artifacts']
    for member,label in [('cortex-contract.md','brain_cortex_candidate'),('authority-dimensions.md','brain_dimensions_candidate')]:
        require(selected[member]['sha256']==upstream[label]['sha256'],'BASELINE_SELECTED_MEMBER:'+member)

def qualification_receipt(mapping_raw,contract_raw,register_raw,upstream,custody,decisions,baseline_context=None):
    """Source identities are independent of per-subject decision ordering/content."""
    return {'scope':'OFFLINE_MAPPING_RELATION_QUALIFICATION_NOT_RUNTIME_INGRESS','status':'PASS','reference_source_sha256':sha(mapping_raw),'mapping_contract_sha256':sha(contract_raw),'source_register_sha256':sha(register_raw),'upstream_sources':upstream,'previous_repair_report_sha256':REPAIR_REPORT_PIN,'custody_verification':custody,'checked_subjects':len(decisions),'decisions':decisions,'canonical_admissions':0,'runtime_crossings':0,'governing_baseline_adopted':baseline_context is not None,'baseline_context':baseline_context,'mapping_adopted':False,'production_ready':False}

def verify_baseline_context(mapping,upstream,catalog,acceptance_pin,retention_pin):
    # External pins are caller-selected custody inputs; this is not issuer authentication.
    for label,pin,source_pin in [('forward_baseline_acceptance',acceptance_pin,mapping.BASELINE_ACCEPTANCE),('forward_baseline_retention',retention_pin,mapping.BASELINE_RETENTION)]:
        require(pin==source_pin==upstream[label]['sha256'],'BASELINE_CONTEXT_PIN:'+label)
    acceptance_raw=(ROOT/upstream['forward_baseline_acceptance']['path']).read_bytes()
    retention_raw=(ROOT/upstream['forward_baseline_retention']['path']).read_bytes()
    require(sha(acceptance_raw)==acceptance_pin,'BASELINE_ACCEPTANCE_DRIFT')
    require(sha(retention_raw)==retention_pin,'BASELINE_RETENTION_DRIFT')
    a=json.loads(acceptance_raw);r=json.loads(retention_raw)
    require(a['schema']=='FORWARD-BASELINE-HUMAN-ACCEPTANCE-RECORD-1','BASELINE_ACCEPTANCE_SCHEMA')
    require(a['decision']['decision_disposition']=='ACCEPT_ALL_FOUR_ATOMICALLY','BASELINE_ATOMIC_DECISION')
    require(a['decision']['actor']==a['procedure']['designated_procedural_authority']=='Alexander Gudde','BASELINE_DECISION_ACTOR')
    require(a['proposal']['sha256']==mapping.BASELINE_CATALOG==r['catalog_sha256'],'BASELINE_ACCEPTANCE_CATALOG')
    require(a['proposal']['selected_candidate_artifacts']==catalog['selected_candidate_artifacts'],'BASELINE_ACCEPTANCE_SELECTED_SET')
    require(a['procedure']['sha256']=='3f6f9393be17bcd448fdebc1e65f4195b700036cdb200d5f435fd90f6f558992','BASELINE_PROCEDURE_IDENTITY')
    require(a['procedure']['acceptance_record_sha256']==a['predecessor_linkage']['procedure_acceptance_record_sha256']=='e813b8242f84fc0b6c6bb4cbf08ee8d0794c703f512c8bb8ad18d0f8aa42eac0','BASELINE_PROCEDURE_ACCEPTANCE')
    require(r['schema']=='FORWARD-BASELINE-EXTERNAL-RETENTION-RECEIPT-1' and r['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED','BASELINE_RETENTION_DISPOSITION')
    require(r['acceptance_sha256']==acceptance_pin and r['acceptance_record_unchanged'] is True,'BASELINE_RETAINED_ACCEPTANCE')
    require(r['repository']=='https://github.com/AnarchI-Technologies-MAIN/AnarchI-Brain' and r['commit']=='7a23a5edba4f814991db604f8f85e02df1adc1ad','BASELINE_REMOTE_IDENTITY')
    require(r['effective_not_before_utc']=='2026-10-04T20:00:46Z' and r['independent_remote_retrieval_verified_at_utc']==r['effective_not_before_utc'],'BASELINE_EFFECTIVE_FLOOR')
    files={item['path']:item for item in r['verified_files']}
    prefix='governance/forward-reconciliation/accepted-baseline-v1.2-20261004T195646Z/'
    required={'acceptance.json':(acceptance_pin,len(acceptance_raw)),'proposal-inventory.json':(mapping.BASELINE_CATALOG,upstream['forward_baseline_catalog']['bytes'])}
    for name,entry in catalog['selected_candidate_artifacts'].items():required['candidate/'+name]=(entry['sha256'],entry['bytes'])
    for name,(pin,length) in required.items():
        require(prefix+name in files and files[prefix+name]['sha256']==pin and files[prefix+name]['bytes']==length,'BASELINE_REMOTE_MEMBER:'+name)
    return {'acceptance_sha256':acceptance_pin,'external_retention_sha256':retention_pin,'catalog_sha256':mapping.BASELINE_CATALOG,'effective_not_before_utc':r['effective_not_before_utc'],'repository':r['repository'],'commit':r['commit'],'scope':'FORWARD_INTERPRETIVE_FOUNDATION_ONLY_NOT_RUNTIME_AUTHORITY'}

if __name__=='__main__':main()

