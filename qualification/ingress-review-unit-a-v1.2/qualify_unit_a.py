"""Offline Unit A custody and finite reference qualification; no runtime effects."""
import argparse,base64,hashlib,importlib.util,json,pathlib,sys,itertools
from dataclasses import asdict

ROOT=pathlib.Path(__file__).parent
BASELINE='421b5d5bab28a32afe557e17970a14beb75a99eddc9f536a75bb1bcda9d26eb3'
MAPPING='61411344381e31149a1b652a34e75f65438a4e18c98970115454ab3ad785d9a4'
BASELINE_ACCEPTANCE='10bd8c050b4a39553a553bdad868f14a4f680709cb4c2b9669d01084ab3fd2bc'
MAPPING_ACCEPTANCE='810fd63b517c513c9dfead469368d5d01938daaac66b35826fb6fb68cce5f5ee'
MAPPING_RETENTION='7ecc3c446680deb959f9fa9873bd3670f44c18e64c141c741217721f4790bfa1'
PRIOR_REPORT='5826e6b8cce74a5554d6045f45ac7ac71971a13f19f61754dbff6139f57e54a8'
CATALOG_SCOPE={
    'schema':'PROPOSED-NON-EFFECTING-INGRESS-REVIEW-FOUNDATION-1',
    'status':'PROPOSED_NOT_ADOPTED','adoption_record':None,'atomic_adoption':True,
    'adoption_unit':'All eleven selected artifacts atomically or none; scoped only to M03 Route B, M04 bounded noncanonical qualification and M08 routing/freshness semantics. Full captured package and other machines are supporting evidence, not adopted.',
    'runtime_activation':False,'canonical_membership':False,'operative_authority':'UNRESOLVED','production_ready':False,'input_count':24,
    'exclusions':['M09/S3 authorization','M12 root/issuer/verifier enrollment','M14 runtime receipts and durable effects','S2 canonical adjudication','readiness profile','runtime-machine state transitions','transport','canonical commit','deployment'],
    'authority_delta':{'principal':'S1','dimension':'Qualify','predecessor':'unresolved','successor':'bounded','named_bound':'YES_BOUNDED_NONCANONICAL_QUALIFICATION','other_cells_unchanged':131},
    'limits':'Constitutional eligibility constraints and pure finite reference only. No actor principal authentication or operation-specific grant. Fixture freshness is not live authority freshness.',
}
REQUIRED_INPUT_LABELS={'accepted_procedure','procedure_acceptance','baseline_catalog','baseline_acceptance','baseline_retention','mapping_contract','mapping_acceptance','mapping_retention','mapping_retention_supplement','prior_handoff_report','baseline_semantic-language.md','baseline_authority-dimensions.md','baseline_cortex-contract.md','baseline_authority-matrix.md','code_m03','code_m08','code_mapping','code_custody','m03_M03.proposal.json','m03_obligations.json','m08_successor/machines/M08.proposal.json','m08_successor/m08-denial-routing-table.json','m03_bindings','m08_package_manifest'}
HISTORICAL_PACKAGE_ANCHORS={'m03_bindings':'93d20d6cb5ab43a8d859560f5ef82ecab881173079024a904dc4ba9dd903cc4a','m08_package_manifest':'a44def170668cf17d25c51f50fcbf4556f491dfc69d4bc5e4cea0d2ff0102f79'}

def load_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('DUPLICATE_JSON_KEY:'+key)
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda value:(_ for _ in ()).throw(ValueError('NONFINITE_JSON')))

def verify_catalog_scope(catalog):
    require(type(catalog)is dict and set(catalog)==set(CATALOG_SCOPE)|{'input_register','selected_artifacts','supporting_artifacts'},'CATALOG_FIELD_MEMBERSHIP')
    for key,expected in CATALOG_SCOPE.items():
        actual=catalog.get(key)
        require(type(actual)is type(expected) and actual==expected,'CATALOG_SCOPE:'+key)

def require(value,reason):
    if not value:raise ValueError(reason)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def read_bound(root,entry):
    name=entry['path'];p=pathlib.PurePosixPath(name)
    require(type(name)is str and not p.is_absolute() and p.as_posix()==name and ':' not in name and '\\' not in name and all(v not in ('.','..','.git')for v in p.parts),'BOUND_PATH')
    path=(root/name).resolve(strict=True)
    require(path.is_relative_to(root.resolve()),'BOUND_PATH_ESCAPE')
    raw=path.read_bytes()
    require(len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],'BOUND_BYTES:'+name)
    return raw

def matrix_cells(raw):
    lines=[line.decode().strip() for line in raw.splitlines() if line.startswith(b'|')]
    header=[value.strip() for value in lines[0].split('|')[1:-1]][1:]
    require(len(header)==12 and len(set(header))==12,'MATRIX_DIMENSIONS')
    rows={}
    for line in lines[2:]:
        values=[value.strip() for value in line.split('|')[1:-1]]
        if len(values)!=13:continue
        require(values[0] not in rows,'DUPLICATE_MATRIX_PRINCIPAL')
        rows[values[0]]=dict(zip(header,values[1:]))
    require(len(rows)==11,'MATRIX_PRINCIPALS')
    return rows

def verify_matrix_context(before,after,crosswalk):
    old=matrix_cells(before);new=matrix_cells(after)
    require(set(old)==set(new),'MATRIX_PRINCIPAL_DRIFT')
    changes=[(principal,dim,old[principal][dim],new[principal][dim])for principal,row in old.items()for dim in row if old[principal][dim]!=new[principal][dim]]
    require(changes==[('S1','Qualify','unresolved','bounded')],'EXACT_SINGLE_CELL_DELTA')
    require(crosswalk['organs']==new and crosswalk['cell_count']==132,'CROSSWALK_MATRIX_DRIFT')
    require(crosswalk['matrix_sha256']==sha(after) and crosswalk['predecessor_matrix_sha256']==sha(before),'CROSSWALK_MATRIX_IDENTITY')
    require(crosswalk['named_bound']=='YES_BOUNDED_NONCANONICAL_QUALIFICATION' and crosswalk['authority_granted_by_crosswalk'] is False,'QUALIFY_BOUND')
    machine_rows=crosswalk['selected_machine_dimension_rows']
    require(type(machine_rows)is list and len(machine_rows)==3 and len({row['machine']for row in machine_rows})==3,'UNIQUE_MACHINE_ROWS')
    rows={row['machine']:row for row in machine_rows}
    require(set(rows)=={'M03','M04','M08'},'UNIT_MACHINE_MEMBERSHIP')
    require(rows['M03']['required_dimensions_from_candidate_map']==['Observe','Propose'],'M03_ROUTE_B_DIMENSIONS')
    require(rows['M04']['declared_owner_cells']=={'Qualify':'bounded'} and rows['M04']['named_qualification_bound']==crosswalk['named_bound'],'M04_BOUND')
    expected={'M03':('Cartologist',['Observe','Propose']),'M04':('S1',['Qualify']),'M08':('Librarian',['Observe','Propose'])}
    for machine,(owner,dimensions) in expected.items():
        row=rows[machine]
        require(row['specification_owner']==owner and row['owner_is_matrix_organ'] is True,'MACHINE_OWNER_BINDING')
        require(row['required_dimensions_from_candidate_map']==dimensions and row['declared_owner_cells']=={dimension:new[owner][dimension]for dimension in dimensions},'MACHINE_OWNER_CELL_BINDING')
    require(all(row['authority_granted_by_crosswalk'] is False for row in rows.values()),'CROSSWALK_GRANT')
    return changes

def verify_adoption_ancestry(captured,approval):
    links={'accepted_procedure':'accepted_procedure','procedure_acceptance':'procedure_acceptance','baseline_catalog':'baseline_catalog','baseline_acceptance':'baseline_acceptance','baseline_retention':'baseline_external_retention'}
    for label,member in links.items():
        raw=captured[label]; descriptor=approval['predecessors'][member]
        require(sha(raw)==descriptor['sha256'] and len(raw)==descriptor['bytes'],'ADOPTION_PREDECESSOR_DRIFT:'+label)
    baseline=load_json(captured['baseline_acceptance']);retention=load_json(captured['baseline_retention'])
    require(baseline['decision']['actor']=='Alexander Gudde' and baseline['decision']['decision_disposition']=='ACCEPT_ALL_FOUR_ATOMICALLY','BASELINE_DECISION_SCOPE')
    require(baseline['procedure']['sha256']==sha(captured['accepted_procedure']) and baseline['procedure']['acceptance_record_sha256']==sha(captured['procedure_acceptance']),'BASELINE_PROCEDURE_LINK')
    require(baseline['proposal']['sha256']==sha(captured['baseline_catalog']),'BASELINE_CATALOG_LINK')
    require(retention['acceptance_sha256']==sha(captured['baseline_acceptance']) and retention['catalog_sha256']==sha(captured['baseline_catalog']) and retention['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED','BASELINE_RETENTION_LINK')
    require(retention['effective_not_before_utc']==approval['predecessors']['baseline_effective_not_before_utc'],'BASELINE_EFFECTIVE_FLOOR')
    selected=load_json(captured['baseline_catalog'])['selected_candidate_artifacts']
    require(baseline['proposal']['selected_candidate_artifacts']==selected,'BASELINE_ATOMIC_MEMBER_LINK')

def verify_catalog(root,catalog_pin):
    raw=(root/'unit-a-catalog.json').read_bytes()
    require(sha(raw)==catalog_pin,'UNIT_CATALOG_DRIFT')
    catalog=load_json(raw)
    verify_catalog_scope(catalog)
    require(catalog['status']=='PROPOSED_NOT_ADOPTED' and catalog['runtime_activation'] is False and catalog['canonical_membership'] is False,'UNIT_SCOPE')
    require(catalog['atomic_adoption'] is True and catalog['adoption_record'] is None,'UNIT_ATOMICITY')
    register_raw=read_bound(root,catalog['input_register']);register=load_json(register_raw)
    require(set(register)==REQUIRED_INPUT_LABELS and len(register)==catalog['input_count'],'EXACT_INPUT_MEMBERSHIP')
    captured={label:read_bound(root,entry)for label,entry in register.items()}
    for label,pin in HISTORICAL_PACKAGE_ANCHORS.items():require(sha(captured[label])==pin,'HISTORICAL_PACKAGE_ANCHOR:'+label)
    selected={name:read_bound(root,entry)for name,entry in catalog['selected_artifacts'].items()}
    require(set(selected)=={'M04_contract','authority_delta','authority_matrix','authority_crosswalk','M03_selection','M03_machine','M03_obligations','M08_selection','M08_machine','M08_denial_routing_table','reference'},'EXACT_SELECTED_MEMBERSHIP')
    for entry in catalog['supporting_artifacts'].values():read_bound(root,entry)
    require(sha(captured['baseline_catalog'])==BASELINE and sha(captured['mapping_contract'])==MAPPING,'GOVERNING_CONTEXT_IDENTITY')
    require(sha(captured['baseline_acceptance'])==BASELINE_ACCEPTANCE and sha(captured['mapping_acceptance'])==MAPPING_ACCEPTANCE and sha(captured['mapping_retention'])==MAPPING_RETENTION,'DECISION_CUSTODY')
    base=load_json(captured['baseline_catalog'])
    for name,entry in base['selected_candidate_artifacts'].items():require(sha(captured['baseline_'+name])==entry['sha256'],'BASELINE_SELECTED:'+name)
    approval=load_json(captured['mapping_acceptance']);retention=load_json(captured['mapping_retention'])
    verify_adoption_ancestry(captured,approval)
    require(approval['adoption_unit']['sha256']==MAPPING and approval['decision']['decision_disposition']=='ACCEPT_EXACT_MAPPING_V1_3','MAPPING_ACCEPTANCE_SCOPE')
    require(retention['acceptance_sha256']==MAPPING_ACCEPTANCE and retention['mapping_contract_sha256']==MAPPING and retention['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED','MAPPING_RETENTION_SCOPE')
    require(retention['effective_not_before_utc']=='2026-10-04T20:55:00Z','MAPPING_EFFECTIVE_FLOOR')
    changes=verify_matrix_context(captured['baseline_authority-matrix.md'],selected['authority_matrix'],load_json(selected['authority_crosswalk']))
    for machine,label in [('M03','m03_M03.proposal.json'),('M08','m08_successor/machines/M08.proposal.json')]:
        selection=load_json(selected[machine+'_selection'])
        require(selected[machine+'_machine']==captured[label] and selection['selected_artifact']==catalog['selected_artifacts'][machine+'_machine'],'SELECTED_MACHINE_SUBSTITUTION')
        require(selection['machine']==machine and selection['runtime_activation'] is False and selection['other_18_m08_package_machines_adopted'] is False,'MACHINE_SELECTION_SCOPE')
        require(selection['selected_artifact']['sha256']==sha(captured[label]),'MACHINE_SELECTED_BYTES')
        require(selection['forward_context']['baseline_catalog_sha256']==BASELINE and selection['forward_context']['mapping_acceptance_sha256']==MAPPING_ACCEPTANCE,'MACHINE_FORWARD_CONTEXT')
    routing=load_json(selected['M08_selection'])['selected_denial_routing_table']
    routing_identity={key:routing[key]for key in ('path','bytes','sha256')}
    require(selected['M08_denial_routing_table']==captured['m08_successor/m08-denial-routing-table.json'] and routing_identity==catalog['selected_artifacts']['M08_denial_routing_table'],'M08_ROUTING_TABLE_SUBSTITUTION')
    require(routing['rows']==720 and len(load_json(selected['M08_denial_routing_table'])['rows'])==720,'M08_ROUTING_TABLE_CARDINALITY')
    require(routing['role']=='FINITE_M08_ROUTING_SEMANTICS_ONLY' and routing['allowed_fixture_finding_is_not_operative_permission'] is True and routing['unit_a_scope_input']=='UNRESOLVED_ORDINARY_ACCESS_ALWAYS_CLOSED','M08_ROUTING_TABLE_SCOPE')
    obligations=load_json(selected['M03_obligations']); source=load_json(captured['m03_obligations.json'])
    indices=[i for i,row in enumerate(source['machines']) if row['id']=='M03']
    require(len(indices)==1,'M03_OBLIGATION_MEMBERSHIP')
    require(obligations['source_obligations_sha256']==sha(captured['m03_obligations.json']) and obligations['source_pointer']=='/machines/'+str(indices[0]) and obligations['selected_obligation']==source['machines'][indices[0]],'M03_OBLIGATION_SUBSTITUTION')
    require(obligations['scope']=='M03_ROW_ONLY_NO_OTHER_MACHINE_ADOPTION' and obligations['status']=='PROPOSED_NOT_ADOPTED' and obligations['runtime_authority']=='UNRESOLVED' and obligations['runtime_activation'] is False,'M03_OBLIGATION_SCOPE')
    return catalog,captured,selected,changes

def captured_module(name,raw,path):
    module=importlib.util.module_from_spec(importlib.util.spec_from_loader(name,loader=None));module.__file__=str(path);sys.modules[name]=module
    exec(compile(raw,str(path),'exec',dont_inherit=True),module.__dict__)
    return module

def verify_routing_table(raw,m08):
    rows=load_json(raw)['rows']
    domains=(('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),('MATCH','MISMATCH','MISSING','UNKNOWN'),('EQUAL','DIFFERENT','UNKNOWN','CONTRADICTORY'),('CURRENT','STALE','UNKNOWN'),('SATISFIED','BLOCKED','UNRESOLVED'))
    expected_components=set(itertools.product(*domains))
    require(len(rows)==720 and {tuple(row['components'])for row in rows}==expected_components,'M08_ROUTING_CASE_MEMBERSHIP')
    fields={'comparison_classification','ordinary_access','route_event','route_outcome','target_state'}
    for row in rows:
        require(set(row['expected'])==fields,'M08_ROUTING_EXPECTED_FIELDS')
        actual=m08.atlas_denial_route(*row['components'])
        require({key:actual[key]for key in fields}==row['expected'],'M08_ROUTING_SOURCE_MISMATCH')
    return len(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog-sha256',required=True);parser.add_argument('--out',required=True,type=pathlib.Path)
    args=parser.parse_args()
    catalog,captured,selected,changes=verify_catalog(ROOT,args.catalog_sha256)
    ref=captured_module('captured_unit_a',selected['reference'],ROOT/'ingress_review_reference.py')
    deps=ref.load_dependencies({name:captured['code_'+name]for name in ('m03','m08','mapping','custody')},selected['M04_contract'],sha(selected['M04_contract']))
    routing_cases=verify_routing_table(selected['M08_denial_routing_table'],deps.m08)
    require(sha(captured['prior_handoff_report'])==PRIOR_REPORT,'PRIOR_CUSTODY_REPORT')
    prior=load_json(captured['prior_handoff_report']);descriptor=next(item for item in prior['full_corpus_runs']if item['producer_version']=='v5.1')
    atlas=ROOT.parent/'atlas-ubuntu-substrate-20261004';output=atlas/descriptor['output']
    custody=deps.custody.verify_output(output,descriptor['qualification_sha256'])
    corpus_receipt_raw=(output/'qualification.json').read_bytes()
    require(sha(corpus_receipt_raw)==descriptor['qualification_sha256'],'CORPUS_RECEIPT_DRIFT')
    corpus_receipt=load_json(corpus_receipt_raw)
    root_digest=sha(('UNIT_A_OFFLINE_FIXTURE_ONLY:'+corpus_receipt['proposal_stream_sha256']).encode())
    fixture=ref.Snapshot(root_digest,root_digest,1,1,'OFFLINE_FIXTURE_ONLY')
    checked=0;decisions=[]
    with (output/'proposals.jsonl').open('rb')as stream:
        for line in stream:
            brain_raw=line[:-1];doc=load_json(brain_raw);p=doc['proposal'];producer_raw=base64.b64decode(p['epistemaddy_proposal_utf8_base64'],validate=True);producer=load_json(producer_raw)
            require(checked<len(corpus_receipt['document_sha256']),'CORPUS_EXTRA_DOCUMENT')
            expected_brain=corpus_receipt['document_sha256'][checked]
            require(sha(brain_raw)==expected_brain,'CORPUS_ORDERED_DOCUMENT_DRIFT')
            subject=ref.ReferenceSubject(expected_brain,p['epistemaddy_proposal_sha256'],p['database_sha256'],p['source_candidate_id'],p['source_record_version'],producer['scope'])
            result=ref.evaluate(brain_raw,producer_raw,subject,fixture,deps)
            require(result.disposition=='QUALIFICATION_SATISFIED','CORPUS_QUALIFICATION:'+str(checked)+':'+result.disposition)
            require(result.runtime_crossing_permitted is False and result.canonical_membership is False and result.protected_effect is False and result.operative_authority=='UNRESOLVED' and result.runtime_m04_state=='CANDIDATE','EFFECT_ESCALATION')
            decisions.append(asdict(result));checked+=1
    require(checked==2736,'CORPUS_CARDINALITY')
    receipt={'scope':'OFFLINE_STRUCTURE_PROVENANCE_FIXTURE_QUALIFICATION_NOT_RUNTIME','status':'PASS','catalog_sha256':args.catalog_sha256,'input_register_sha256':catalog['input_register']['sha256'],'selected_artifacts':catalog['selected_artifacts'],'changed_matrix_cells':changes,'prior_custody':custody,'fixture_profile':'OFFLINE_FIXTURE_ONLY','routing_cases':routing_cases,'checked_subjects':checked,'decisions':decisions,'unit_adopted':False,'mapping_contract_adopted':True,'runtime_crossings':0,'canonical_admissions':0,'production_ready':False}
    with args.out.open('x',encoding='utf-8',newline='\n')as f:f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({key:receipt[key]for key in ('status','scope','checked_subjects','unit_adopted','runtime_crossings','canonical_admissions','production_ready')}))

if __name__=='__main__':main()
