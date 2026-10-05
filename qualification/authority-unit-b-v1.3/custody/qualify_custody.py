"""Offline documentary custody only; no authority enrollment or runtime effects."""
import argparse,hashlib,json,pathlib,os
ROOT=pathlib.Path(__file__).resolve().parent.parent
EXPECTED_PIN='c6fe32a4a58ce7775ddc2433f29c6f9259f76b6055606249d9b9cd262df1f172'
REGISTER_SPECS={
 'input-register.json':('UNIT-B-PREDECESSOR-CAPTURE-1',{'lyra_direction','procedure','procedure_acceptance','baseline_catalog','baseline_acceptance','unit_a_catalog','unit_a_matrix','unit_a_acceptance','unit_a_retention','unit_a_retention_publication','historical_m09','historical_m12','historical_grant_v1'}),
 'chain-supplement-register.json':('UNIT-B-CHAIN-SUPPLEMENT-1',{'baseline_retention','mapping_contract','mapping_acceptance','mapping_retention','mapping_question_supplement','mapping_supplement_retention','semantic_language','authority_dimensions','cortex_contract','baseline_matrix'}),
 'custody/matrix-support-register.json':('UNIT-B-MATRIX-SUPPORT-1',{'unit_a_crosswalk'}),
}
ENTRY_KEYS={'label','path','bytes','sha256','role','source'}
MAX_BYTES=1048576
def require(value,reason):
 if not value:raise ValueError(reason)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load_json(raw):
 def pairs(items):
  result={}
  for key,value in items:
   if key in result:raise ValueError('DUPLICATE_JSON_KEY:'+key)
   result[key]=value
  return result
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda value:(_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
def safe_read(root,name):
 require(type(name)is str,'BOUND_PATH')
 path=pathlib.PurePosixPath(name)
 require(bool(name) and not path.is_absolute() and path.as_posix()==name and ':' not in name and '\\' not in name and all(v not in ('.','..','.git')for v in path.parts),'BOUND_PATH')
 resolved=(root/name).resolve(strict=True)
 require(resolved.is_relative_to(root.resolve()),'BOUND_PATH_ESCAPE')
 require(resolved.is_file() and 0<resolved.stat().st_size<=MAX_BYTES,'CAPTURE_RESOURCE_BOUND')
 raw=resolved.read_bytes();require(0<len(raw)<=MAX_BYTES,'CAPTURE_RESOURCE_BOUND');return raw
def same_descriptor(raw,descriptor,reason):
 require(type(descriptor)is dict and descriptor.get('sha256')==sha(raw) and type(descriptor.get('bytes'))is int and descriptor['bytes']==len(raw),reason)
def read_captures(root):
 expected_raw=safe_read(root,'custody/expected-capture-identities.json');require(sha(expected_raw)==EXPECTED_PIN,'EXPECTED_CAPTURE_IDENTITY_DRIFT')
 expected=load_json(expected_raw);captured={}
 for filename,(schema,labels)in REGISTER_SPECS.items():
  register=load_json(safe_read(root,filename))
  require(type(register)is dict and set(register)=={'schema','status','runtime_authority','files'},'REGISTER_FIELDS')
  require(register['schema']==schema and register['status']=='DRAFT_NOT_ADOPTED' and register['runtime_authority'] is False,'REGISTER_SCOPE')
  entries=register['files'];require(type(entries)is list and len(entries)==len(labels),'REGISTER_CARDINALITY')
  require(all(type(e)is dict and set(e)==ENTRY_KEYS for e in entries),'REGISTER_ENTRY_FIELDS')
  require({e['label']for e in entries}==labels and len({e['label']for e in entries})==len(entries),'REGISTER_LABEL_MEMBERSHIP')
  for entry in entries:
   label=entry['label'];require(label not in captured,'DUPLICATE_CAPTURE_LABEL')
   require(entry==expected[label] and type(entry['bytes'])is int,'REGISTER_IDENTITY_DRIFT:'+label)
   raw=safe_read(root,entry['path']);same_descriptor(raw,entry,'CAPTURE_BYTES:'+label);captured[label]=raw
 require(set(captured)==set(expected) and len(captured)==24,'EXACT_CAPTURE_MEMBERSHIP')
 return captured
def retained_member(receipt,raw,suffix,reason):
 members=[v for v in receipt['verified_files']if v['path'].endswith(suffix)]
 require(len(members)==1,reason);same_descriptor(raw,members[0],reason)
def verify_chain(c):
 p=load_json(c['procedure_acceptance']);baseline=load_json(c['baseline_acceptance']);br=load_json(c['baseline_retention']);bc=load_json(c['baseline_catalog'])
 mapping=load_json(c['mapping_acceptance']);mr=load_json(c['mapping_retention']);ms=load_json(c['mapping_supplement_retention']);mq=load_json(c['mapping_question_supplement'])
 unit=load_json(c['unit_a_acceptance']);ur=load_json(c['unit_a_retention']);up=load_json(c['unit_a_retention_publication']);uc=load_json(c['unit_a_catalog'])
 require(p['schema']=='BRAIN-FORWARD-PROCEDURE-ACCEPTANCE-1' and p['actor']=='Alexander Gudde' and p['disposition']=='ACCEPTED_FORWARD_PROCEDURE_ONLY','PROCEDURE_DECISION_SCOPE')
 require(p['procedure_sha256']==sha(c['procedure']) and p['procedure_bytes']==len(c['procedure']) and p['effective_not_before_utc']=='2026-10-04T06:28:55Z','PROCEDURE_SUBJECT_FLOOR')
 require(baseline['procedure']['sha256']==sha(c['procedure']) and baseline['procedure']['acceptance_record_sha256']==sha(c['procedure_acceptance']),'PROCEDURE_CHAIN')
 require(baseline['procedure']['designated_procedural_authority']=='Alexander Gudde' and baseline['decision']['actor']=='Alexander Gudde' and baseline['decision']['decision_disposition']=='ACCEPT_ALL_FOUR_ATOMICALLY','BASELINE_AUTHORITY_SCOPE')
 require(baseline['proposal']['sha256']==sha(c['baseline_catalog']) and baseline['proposal']['selected_candidate_artifacts']==bc['selected_candidate_artifacts'],'BASELINE_ATOMIC_MEMBERSHIP')
 member_labels={'semantic-language.md':'semantic_language','authority-dimensions.md':'authority_dimensions','cortex-contract.md':'cortex_contract','authority-matrix.md':'baseline_matrix'}
 require(set(bc['selected_candidate_artifacts'])==set(member_labels),'BASELINE_SELECTED_MEMBERSHIP')
 for name,label in member_labels.items():same_descriptor(c[label],bc['selected_candidate_artifacts'][name],'BASELINE_SELECTED_BYTES:'+name)
 require(br['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED' and br['acceptance_sha256']==sha(c['baseline_acceptance']) and br['catalog_sha256']==sha(c['baseline_catalog']),'BASELINE_RETENTION_LINK')
 require(br['effective_not_before_utc']=='2026-10-04T20:00:46Z' and br['independent_remote_retrieval_verified_at_utc']==br['effective_not_before_utc'],'BASELINE_EFFECTIVE_FLOOR')
 retained_member(br,c['procedure'],'/predecessor/accepted-procedure.md','PROCEDURE_RETENTION')
 retained_member(br,c['procedure_acceptance'],'/predecessor/acceptance.json','PROCEDURE_ACCEPTANCE_RETENTION')
 for label,key in {'procedure':'accepted_procedure','procedure_acceptance':'procedure_acceptance','baseline_catalog':'baseline_catalog','baseline_acceptance':'baseline_acceptance','baseline_retention':'baseline_external_retention'}.items():same_descriptor(c[label],mapping['predecessors'][key],'MAPPING_PREDECESSOR:'+label)
 require(mapping['decision']['actor']=='Alexander Gudde' and mapping['decision']['decision_disposition']=='ACCEPT_EXACT_MAPPING_V1_3','MAPPING_DECISION_SCOPE')
 same_descriptor(c['mapping_contract'],mapping['adoption_unit'],'MAPPING_SUBJECT')
 require(mapping['predecessors']['baseline_effective_not_before_utc']==br['effective_not_before_utc'],'MAPPING_BASELINE_FLOOR')
 require(mr['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED' and mr['acceptance_sha256']==sha(c['mapping_acceptance']) and mr['mapping_contract_sha256']==sha(c['mapping_contract']),'MAPPING_RETENTION_LINK')
 require(mr['effective_not_before_utc']=='2026-10-04T20:55:00Z' and mr['independent_remote_retrieval_verified_at_utc']==mr['effective_not_before_utc'],'MAPPING_EFFECTIVE_FLOOR')
 require(mq['acceptance_record_sha256']==sha(c['mapping_acceptance']) and mq['acceptance_record_unchanged'] is True,'MAPPING_QUESTION_LINK')
 require(ms['first_verified_external_retention_effective_not_before_utc']==mr['effective_not_before_utc'] and ms['original_acceptance_and_retention_receipt_unchanged'] is True,'MAPPING_SUPPLEMENT_FLOOR')
 retained_member(ms,c['mapping_question_supplement'],'/question-context-supplement.json','MAPPING_QUESTION_RETENTION')
 retained_member(ms,c['mapping_retention'],'/external-retention-receipt.json','MAPPING_RECEIPT_RETENTION')
 links={'procedure':'accepted_procedure','procedure_acceptance':'procedure_acceptance','baseline_catalog':'baseline_catalog','baseline_acceptance':'baseline_acceptance','baseline_retention':'baseline_retention','mapping_contract':'mapping_contract','mapping_acceptance':'mapping_acceptance','mapping_retention':'mapping_retention','mapping_supplement_retention':'mapping_retention_supplement'}
 for label,key in links.items():same_descriptor(c[label],unit['predecessor_linkage'][key],'UNIT_A_PREDECESSOR:'+label)
 same_descriptor(c['unit_a_catalog'],unit['catalog'],'UNIT_A_CATALOG_LINK')
 require(unit['decision']['actor']=='Alexander Gudde' and unit['decision']['decision_disposition']=='ACCEPT_ALL_ELEVEN_ATOMICALLY' and unit['atomic_all_eleven_or_none'] is True,'UNIT_A_ATOMIC_SCOPE')
 require(unit['selected_artifacts']==uc['selected_artifacts'] and len(uc['selected_artifacts'])==11,'UNIT_A_SELECTED_MEMBERSHIP')
 for label,key in [('unit_a_matrix','authority_matrix'),('unit_a_crosswalk','authority_crosswalk')]:same_descriptor(c[label],uc['selected_artifacts'][key],'UNIT_A_MEMBER:'+label)
 require(ur['disposition']=='EXTERNAL_GITHUB_RETENTION_VERIFIED' and ur['acceptance_sha256']==sha(c['unit_a_acceptance']) and ur['catalog_sha256']==sha(c['unit_a_catalog']),'UNIT_A_RETENTION_LINK')
 require(ur['effective_not_before_utc']=='2026-10-04T22:28:23Z' and ur['independent_remote_retrieval_verified_at_utc']==ur['effective_not_before_utc'],'UNIT_A_EFFECTIVE_FLOOR')
 retained_member(ur,c['unit_a_catalog'],'/unit-a-catalog.json','UNIT_A_CATALOG_RETENTION')
 retained_member(ur,c['unit_a_acceptance'],'/adoption/acceptance.json','UNIT_A_ACCEPTANCE_RETENTION')
 retained_member(ur,c['unit_a_matrix'],'/AUTHORITY-MATRIX-SUCCESSOR-DRAFT.md','UNIT_A_MATRIX_RETENTION')
 retained_member(ur,c['unit_a_crosswalk'],'/authority-crosswalk-unit-a.json','UNIT_A_CROSSWALK_RETENTION')
 require(up['receipt_sha256']==sha(c['unit_a_retention']) and up['original_acceptance_and_receipt_unchanged'] is True and up['prospective_effective_not_before_utc']==ur['effective_not_before_utc'],'UNIT_A_PUBLICATION_LINK')
 retained_member(up,c['unit_a_retention'],'/adoption/external-retention-receipt.json','UNIT_A_RECEIPT_PUBLICATION')
 return {'baseline':br['effective_not_before_utc'],'mapping':mr['effective_not_before_utc'],'unit_a':ur['effective_not_before_utc']}
def matrix_cells(raw):
 lines=[line.decode('utf-8').strip()for line in raw.splitlines()if line.startswith(b'|')]
 require(len(lines)>=13,'MATRIX_SHAPE');header=[v.strip()for v in lines[0].split('|')[1:-1]][1:]
 require(len(header)==12 and len(set(header))==12,'MATRIX_DIMENSIONS');rows={}
 for line in lines[2:]:
  values=[v.strip()for v in line.split('|')[1:-1]]
  if len(values)!=13:continue
  require(values[0]not in rows,'MATRIX_DUPLICATE_PRINCIPAL');rows[values[0]]=dict(zip(header,values[1:]))
 require(len(rows)==11,'MATRIX_PRINCIPALS');return rows
def verify_matrix(c,proof_raw,crosswalk_raw):
 old=load_json(c['unit_a_crosswalk']);cells=matrix_cells(c['unit_a_matrix']);proof=load_json(proof_raw);crosswalk=load_json(crosswalk_raw)
 require(set(proof)=={'schema','status','authority_granted_by_crosswalk','cell_count','context','matrix_cell_changes','notice','proposed_successor_cells','s3_authorize','selected_predecessor_crosswalk','selected_predecessor_matrix'},'UNIT_B_PROOF_FIELDS')
 require(set(crosswalk)=={'schema','status','authority_granted_by_crosswalk','cell_count','changes','context','organs','predecessor_crosswalk_sha256','predecessor_matrix_sha256','runtime_activation','s3_authorize','unit_b_scope'},'UNIT_B_CROSSWALK_FIELDS')
 require(crosswalk['schema']=='UNIT-B-AUTHORITY-CROSSWALK-DRAFT-1' and crosswalk['status']=='PROPOSED_NOT_ADOPTED' and crosswalk['unit_b_scope']=='FINITE_EXTERNAL_AUTHORIZATION_INTERPRETATION_ONLY','UNIT_B_CROSSWALK_SCOPE')
 require(old['organs']==cells and old['matrix_sha256']==sha(c['unit_a_matrix']) and old['cell_count']==132,'UNIT_A_MATRIX_CROSSWALK')
 context={'unit_a_catalog_sha256':sha(c['unit_a_catalog']),'unit_a_acceptance_sha256':sha(c['unit_a_acceptance']),'unit_a_retention_sha256':sha(c['unit_a_retention'])}
 require(proof['context']==context and crosswalk['context']==context,'UNIT_B_MATRIX_CONTEXT')
 require(proof['schema']=='UNIT-B-UNCHANGED-132-CELL-PROOF-1' and proof['status']=='LOCAL_SOURCE_COMPARISON_NOT_ADOPTION','UNIT_B_PROOF_SCOPE')
 require(proof['proposed_successor_cells']==cells and proof['cell_count']==132 and proof['matrix_cell_changes']==[] and proof['authority_granted_by_crosswalk'] is False,'UNIT_B_MATRIX_CHANGED')
 same_descriptor(c['unit_a_matrix'],proof['selected_predecessor_matrix'],'UNIT_B_MATRIX_PREDECESSOR')
 require(proof['selected_predecessor_crosswalk']['sha256']==sha(c['unit_a_crosswalk']),'UNIT_B_CROSSWALK_PREDECESSOR')
 require(crosswalk['organs']==cells and crosswalk['cell_count']==132 and crosswalk['changes']==[] and crosswalk['authority_granted_by_crosswalk'] is False and crosswalk['runtime_activation'] is False,'UNIT_B_CROSSWALK_CHANGED')
 require(crosswalk['predecessor_matrix_sha256']==sha(c['unit_a_matrix']) and crosswalk['predecessor_crosswalk_sha256']==sha(c['unit_a_crosswalk']),'UNIT_B_CROSSWALK_IDENTITY')
 require(cells['S3']['Authorize']=='unresolved' and proof['s3_authorize']=='unresolved' and crosswalk['s3_authorize']=='unresolved','S3_AUTHORITY_ESCALATION')
 return 132
def qualify(root=ROOT):
 c=read_captures(root);floors=verify_chain(c)
 documents={path:safe_read(root,path)for path in ('contracts/UNCHANGED-MATRIX-PROOF-DRAFT.json','contracts/AUTHORITY-CROSSWALK-UNIT-B-DRAFT.json')}
 count=verify_matrix(c,*documents.values())
 return {'schema':'UNIT-B-DOCUMENTARY-CUSTODY-RESULT-1','status':'PASS','captured_inputs':24,'predecessor_matrix_cells':count,'matrix_changes':0,'effectiveness_floors':floors,'checked_draft_documents':{path:{'bytes':len(raw),'sha256':sha(raw)}for path,raw in documents.items()},'runtime_authority':False,'operative_grant':False,'effect_permitted':False,'durable_consumption':False,'production_ready':False,'limits':'Verified exact23rootcaptures plusonecapturedUnitAcrosswalk, documentary decision/retention chain and selectedmatrix/crosswalk membership. Does not reexecute or inspect all11UnitAselectedcontent bodies; no current remote availability, cryptographic authority, runtime enrollment, or UnitB adoption is established. UnitBdraftmatrixproof/crosswalk lack enclosingcatalog pin here; latercatalogqualification must supply it.'}
def qualify_predecessors(unit: pathlib.Path)->dict:
 """Raise on failed custody; return documentary-only summary for catalog wrapper."""
 return qualify(unit)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=pathlib.Path,default=ROOT);parser.add_argument('--out',type=pathlib.Path);args=parser.parse_args();result=qualify(args.root);raw=(json.dumps(result,indent=2)+'\n').encode()
 if args.out:
  with args.out.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 print(raw.decode(),end='')
if __name__=='__main__':main()
