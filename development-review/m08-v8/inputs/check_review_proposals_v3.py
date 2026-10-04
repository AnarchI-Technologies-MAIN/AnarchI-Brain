from pathlib import Path
from datetime import datetime,timezone
import copy
import hashlib
import json

ROOT=Path(__file__).absolute().parent
def require(condition,reason):
    if not condition:raise ValueError(reason)
def verify(machines,fixtures):
    for machine,draft in machines.items():
        rows=draft['legal_transitions']
        keys=[(row['from'],row['event'],row['gate_outcome']) for row in rows]
        require(len(keys)==len(set(keys)),machine+':duplicate_route')
        require(draft['status']=='REVISED_V3_PROPOSAL_UNADOPTED_NOT_RUNTIME',machine+':adoption_promotion')
    def rows(machine,event):return [row for row in machines[machine]['legal_transitions'] if row['event']==event]
    for row in rows('M12','consume_exact_grant')+rows('M12','delegate_bounded_subset'):
        require(row['to']=='GRANTED','M12:validity_replaced_by_use')
    require('entire bounded ancestor chain' in machines['M12']['delegation_rule'],'M12:ancestor_freshness_unmapped')
    for row in rows('M18','recognized_compromise')+rows('M18','trust_unknown'):
        require(row['to']=='CLOSED' and row['ordinary_access_eligibility']=='CLOSED','M18:closure_does_not_close')
        require('no positive reopening' in row['authorizer'],'M18:closure_requires_reopening_authority')
    for row in rows('M10','expire_or_revoke'):
        require(row['ordinary_access_eligibility']=='CLOSED','M10:unknown_lease_retains_access')
    for row in rows('M16','abort_before_cutover'):
        if row['gate_outcome']=='SATISFIED':
            require(any('shadow_or_rollback_evidence=BLOCKED' in predicate for predicate in row['required_predicates']),'M16:abort_requires_successful_shadow')
            require(any('cutover_occurrence=NOT_OCCURRED' in predicate for predicate in row['required_predicates']),'M16:unknown_cutover_treated_absent')
    case={row['id']:row for row in fixtures['cases']}
    require(len(case)==13,'fixture_case_count')
    require('never demote committed state' in ' '.join(case['T04']['oracles']),'T04:unacknowledged_demoted')
    require(len(case['T01']['variants'])==7,'T01:missing_consumed_delegated_revocation')
    for c in case.values():
        require(len({v['id'] for v in c['variants']})==len(c['variants']),'duplicate_variant')
        for variant in c['variants']:
            require(all(key in variant for key in ('expected_classification','expected_receipt','expected_canonical_root','forbidden_effects','causal_oracle','resource_oracle')),'variant_oracle_omission')
    return {'machines':19,'cases':13,'variants':sum(len(case['variants']) for case in fixtures['cases'])}
machines={f'M{i:02d}':json.loads((ROOT/'specification-drafts-v3'/f'M{i:02d}.proposal.json').read_bytes()) for i in range(1,20)}
fixtures=json.loads((ROOT/'adversarial_fixtures_v2.json').read_bytes())
baseline=verify(machines,fixtures)
controls=[]
attacks=[('consumption_hides_expiry',lambda m,f:next(r for r in m['M12']['legal_transitions'] if r['event']=='consume_exact_grant').update(to='IN_USE'),'M12:validity_replaced_by_use'),
         ('unknown_lease_leaks',lambda m,f:next(r for r in m['M10']['legal_transitions'] if r['event']=='expire_or_revoke').update(ordinary_access_eligibility='LIVE'),'M10:unknown_lease_retains_access'),
         ('closure_requires_recovery',lambda m,f:next(r for r in m['M18']['legal_transitions'] if r['event']=='trust_unknown').update(authorizer='UNRESOLVED_GOVERNING_AUTHORITY'),'M18:closure_requires_reopening_authority'),
         ('demote_local_commit',lambda m,f:next(c for c in f['cases'] if c['id']=='T04').update(oracles=['unacknowledged means candidate']),'T04:unacknowledged_demoted')]
for name,mutate,expected in attacks:
    altered_m=copy.deepcopy(machines);altered_f=copy.deepcopy(fixtures)
    mutate(altered_m,altered_f)
    try:verify(altered_m,altered_f)
    except ValueError as exc:
        require(str(exc)==expected,'wrong_counterexample_gate')
        controls.append({'counterexample':name,'rejected_at':str(exc)})
        continue
    raise ValueError('counterexample_accepted')
result={'scope':'STATIC_REVIEW_PROPOSAL_CONTRADICTION_CHECKS_NOT_EXECUTABLE_MACHINE_SEMANTICS',
        'finished_at':datetime.now(timezone.utc).isoformat(),'baseline':baseline,'controls':controls,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'runtime_transitions_executed':0,
        'production_ready':False,'semantic_issuer_contracts_resolved':False}
with (ROOT/'evidence/review-proposals-v3-checks.json').open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
print(json.dumps(result,indent=2))
