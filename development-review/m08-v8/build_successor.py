from pathlib import Path
import copy, hashlib, json, shutil

ROOT = Path(__file__).resolve().parent
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')

machines = {f'M{i:02d}': json.loads((ROOT/'inputs/specification-drafts-v3'/f'M{i:02d}.proposal.json').read_bytes()) for i in range(1,20)}
fixtures = json.loads((ROOT/'inputs/adversarial_fixtures_v2.json').read_bytes())
# Independent review reference starts from the preserved predecessor, never the successor's declarations.
expected = {v['id']: v['expected_classification'] for c in fixtures['cases'] for v in c['variants']}
for row in machines['M08']['legal_transitions']:
    if row['to']=='STALE' or row['gate_outcome']!='SATISFIED':
        row['ordinary_access_eligibility']='CLOSED'
    if row['to']=='DERIVED' and row['gate_outcome']=='SATISFIED':
        row['ordinary_access_eligibility']='ONLY_IF_EXACT_VIEW_FRESH_AND_SEPARATE_CURRENT_SCOPE_VALID'
        row['required_predicates'].append('M08.exact_view_freshness=SATISFIED')
    if row['event']=='denial_with_intervening_drift' and row['gate_outcome']=='SATISFIED':
        row['side_effect']='DENY_ONLY_NO_PROTECTED_EFFECT'
    if row['event']=='detect_root_drift' and row['gate_outcome']=='SATISFIED':
        row['authorizer']='GOVERNED_FAIL_SAFE_EXECUTOR_NO_REOPENING_GRANT; actual adoption unresolved'
machines['M08']['machine_specific_semantics']['stale_access']='The identified stale view remains ineligible even with valid scope. Rebuild produces a separately identified fresh view; equality alone is not freshness. No new acquisition service is implied.'

definitions = {
 'abort_evidence': {
  'status':'UNADOPTED_FINITE_REFERENCE_SEMANTICS_NOT_REAL_AUTHORITY',
  'components':{'binding':['MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'], 'proof':['FAIL','PASS','UNKNOWN','MISSING','INVALID','CONTRADICTORY'], 'occurrence':['NOT_OCCURRED','OCCURRED','UNKNOWN','MISSING','CONTRADICTORY']},
  'required_evidence':['exact attempt ID and fenced generation on proof and occurrence evidence','failed shadow/rollback proof identity and result','durable journal/current-root observation establishing cutover occurrence'],
  'precedence':['invalid/contradictory/mismatched binding or proof/occurrence: BLOCKED','observed OCCURRED: BLOCKED','missing binding/proof or unknown/missing occurrence: UNRESOLVED','MATCH + FAIL + NOT_OCCURRED: SATISFIED','MATCH + PASS + NOT_OCCURRED: BLOCKED'],
  'finding_retention':'retain each original component even when BLOCKED precedes UNRESOLVED; no absent receipt proves NOT_OCCURRED',
  'permitted_result':'SATISFIED permits only pre-cutover workflow abort, never canonical-root rollback or a fresh grant'
 },
 'atlas_root_comparison': {
  'status':'UNADOPTED_FINITE_REFERENCE_SEMANTICS_NOT_REAL_AUTHORITY',
  'components':{'binding':['MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'],'comparability':['MATCH','MISMATCH','MISSING','UNKNOWN'],'relation':['EQUAL','DIFFERENT','UNKNOWN','CONTRADICTORY'],'freshness':['CURRENT','STALE','UNKNOWN']},
  'required_evidence':['exact view ID, original/current root digests and lengths','same root identity/schema/hash profile and tenant/object scope','trusted observation identity, generation/epoch and current read/disclosure fence','separate exact-view freshness and scope findings'],
  'precedence':['invalid/contradictory/mismatched bindings, incomparable profiles or contradictory relation: BLOCKED','missing/unknown binding, comparability or relation: UNRESOLVED','MATCH binding and comparability + determinate relation: SATISFIED comparison, retaining EQUAL or DIFFERENT'],
  'ordinary_access':'Only SATISFIED comparison + EQUAL + CURRENT + separately valid exact scope can qualify this reference view. All other combinations CLOSED. Equality never supplies freshness.',
  'finding_retention':'preserve comparison and freshness independently; comparison may be SATISFIED while stale access remains CLOSED'
 }
}
machines['M08']['predicate_definitions']['atlas_root_comparison']=copy.deepcopy(definitions['atlas_root_comparison'])
machines['M08']['predicate_definitions']['exact_view_freshness']={'bindings':['exact view ID/root, tenant/object, generation/epoch, observed freshness and actual disclosure fence'],'SATISFIED':'Trusted fresh observation binds this exact view at disclosure fence.','BLOCKED':'Known stale/mismatched/revoked view.','UNRESOLVED':'Missing or unknown trusted freshness; access CLOSED.'}
machines['M16']['predicate_definitions']['abort_evidence']=copy.deepcopy(definitions['abort_evidence'])
for row in machines['M16']['legal_transitions']:
    if row['event']=='abort_before_cutover':
        row['required_predicates']=[f"M16.abort_before_cutover.abort_evidence={row['gate_outcome']}"]
        row['state_update']='ABORTED workflow only for SATISFIED same-attempt/generation failed proof plus proven NOT_OCCURRED; otherwise retain prior lifecycle and all findings. Canonical roots unchanged.'

case=next(c for c in fixtures['cases'] if c['id']=='T04')
v=next(v for v in case['variants'] if v['id']=='T04-V05')
v.update(receipt_disclosure_authorization='SATISFIED_EXACT_CURRENT_RECEIPT_ONLY', ordinary_data_authorization='BLOCKED', expected_receipt_disclosure='ORIGINAL_ACK_RECEIPT_ONLY', expected_ack='DURABLY_ACKNOWLEDGED_RESPONSE_LOST')
v['expected_receipt']='ORIGINAL_ACK_RECEIPT_AFTER_EXACT_FRESH_DISCLOSURE_AUTHORIZATION; no new ACK or transition'
v['causal_oracle']='Lost response does not change COMMITTED R1 or durable ACK. Exact fresh receipt-disclosure authorization is checked before releasing only the original receipt. Ordinary data remains denied.'
for identifier,auth,classification in [('T04-V06','MISSING','UNRESOLVED'),('T04-V07','OTHER_RECEIPT','BLOCKED'),('T04-V08','EXPIRED','BLOCKED'),('T04-V09','REVOKED','BLOCKED')]:
    variant=copy.deepcopy(v)
    variant.update(id=identifier,mutation='response lost after durable ACK; disclosure authorization '+auth,receipt_disclosure_authorization=auth,expected_classification=classification,expected_receipt_disclosure='NONE',expected_receipt='ATTEMPT_'+classification+'_NO_PROTECTED_RECEIPT_OR_REFERENCE')
    variant['causal_oracle']='Known COMMITTED R1 and durable ACK preserved; refused disclosure cannot create duplicate transition, expose protected receipt/reference, or grant ordinary data access.'
    case['variants'].append(variant);expected[identifier]=classification
for variant in case['variants']:
    if variant['id']!='T04-V05' and 'receipt_disclosure_authorization' not in variant:
        variant.update(receipt_disclosure_authorization='NOT_REQUESTED',ordinary_data_authorization='BLOCKED',expected_receipt_disclosure='NONE',expected_ack='ABSENT_OR_UNRESOLVED')

write(ROOT/'successor/expected-classifications.json',{'status':'INDEPENDENT_UNADOPTED_REVIEW_REFERENCE','derivation':'Original v2 classifications preserved; four new explicit receipt-disclosure denials added. Not derived from successor declarations.','classifications':expected})
write(ROOT/'successor/composite-predicates.json',definitions)
write(ROOT/'successor/adversarial-fixtures.json',fixtures)
for name,machine in machines.items():
    # Unchanged machines retain exact predecessor bytes.
    dest=ROOT/'successor/machines'/f'{name}.proposal.json';dest.parent.mkdir(parents=True,exist_ok=True)
    if name in ('M08','M16'):write(dest,machine)
    if name not in ('M08','M16'):shutil.copyfile(ROOT/'inputs/specification-drafts-v3'/dest.name,dest)
print('Prepared narrow unadopted successor: two machine files, fixture distinctions, finite composite definitions and independent classifications.')
