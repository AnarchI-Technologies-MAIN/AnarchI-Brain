import copy, hashlib, itertools, json
from pathlib import Path
from reference_semantics import abort_evidence,atlas_comparison,atlas_denial_route,check_proposals,load_reference,validate_reference,require

ROOT=Path(__file__).resolve().parent
def run(expected_pin, buffers):
    def captured(name):
        require(name in buffers,"UNBOUND_INPUT:"+name)
        return buffers[name]
    machines={f'M{i:02d}':json.loads(captured(f'successor/machines/M{i:02d}.proposal.json')) for i in range(1,20)}
    fixtures=json.loads(captured('successor/adversarial-fixtures.json'))
    expected=validate_reference(captured('successor/expected-classifications.json'),expected_pin)
    baseline=check_proposals(machines,fixtures,expected)
    # Execute the unchanged historical checker function in a disposable in-memory namespace.
    historical=captured('inputs/check_review_proposals_v3.py').decode('utf-8').split("machines={f'M{i:02d}'",1)[0]
    namespace={'__file__':str(ROOT/'inputs/check_review_proposals_v3.py')}
    exec(compile(historical,'captured_v3_checker','exec'),namespace)
    old_m={f'M{i:02d}':json.loads(captured(f'inputs/specification-drafts-v3/M{i:02d}.proposal.json')) for i in range(1,20)}
    old_f=json.loads(captured('inputs/adversarial_fixtures_v2.json'))
    historical_results=[]
    for identifier in ('T01-V06','T01-V07'):
        mutant=copy.deepcopy(old_f)
        next(v for c in mutant['cases'] for v in c['variants'] if v['id']==identifier)['expected_classification']='SATISFIED'
        namespace['verify'](old_m,mutant)
        historical_results.append({'variant':identifier,'incorrect_classification':'SATISFIED','historical_checker_accepted':True,'scope':'STATIC_CHECKER_GAP_REPRODUCED_NOT_RUNTIME'})
    abort_count=0
    for b,p,o in itertools.product(('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),('FAIL','PASS','UNKNOWN','MISSING','INVALID','CONTRADICTORY'),('NOT_OCCURRED','OCCURRED','UNKNOWN','MISSING','CONTRADICTORY')):
        result=abort_evidence(b,p,o);abort_count+=1
        require(result['findings']==dict(binding=b,proof=p,occurrence=o),'LOSSY_ABORT_FINDINGS')
        require(result['abort_allowed']==((b,p,o)==('MATCH','FAIL','NOT_OCCURRED')),'UNSAFE_ABORT_COMPOSITION')
        if o=='OCCURRED':require(result['classification']=='BLOCKED','POSTCUTOVER_ABORT')
        if (b,p,o)==('MATCH','FAIL','UNKNOWN'):require(result['classification']=='UNRESOLVED','UNKNOWN_CUTOVER')
    atlas_count=0
    for b,c,r,f,s in itertools.product(('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),('MATCH','MISMATCH','MISSING','UNKNOWN'),('EQUAL','DIFFERENT','UNKNOWN','CONTRADICTORY'),('CURRENT','STALE','UNKNOWN'),('SATISFIED','BLOCKED','UNRESOLVED')):
        result=atlas_comparison(b,c,r,f,s);atlas_count+=1
        require(result['ordinary_access']=='ALLOWED' if (b,c,r,f,s)==('MATCH','MATCH','EQUAL','CURRENT','SATISFIED') else result['ordinary_access']=='CLOSED','UNSAFE_ATLAS_ACCESS')
        require(result['findings']==dict(binding=b,comparability=c,relation=r,freshness=f,scope=s),'LOSSY_ATLAS_FINDINGS')
    route_raw=captured('successor/m08-denial-routing-table.json')
    require(hashlib.sha256(route_raw).hexdigest()=='23de4796fa572bae329ce1de1117418d50fe9e01b3485ec3bff23f234f507ade','M08_ROUTING_ORACLE_PIN')
    route_rows=json.loads(route_raw)['rows']
    require(len(route_rows)==720 and len({tuple(row['components']) for row in route_rows})==720,'M08_ROUTING_ORACLE_INVENTORY')
    for row in route_rows:
        actual=atlas_denial_route(*row['components'])
        require({k:actual[k] for k in row['expected']}==row['expected'],'M08_JOINT_ROUTING_PARITY')
        selected=[r for r in machines['M08']['legal_transitions'] if (r['from'],r['event'],r['gate_outcome'])==('PROPOSED',actual['route_event'],actual['route_outcome'])]
        require(len(selected)==1 and selected[0]['to']==actual['target_state'],'M08_SELECTED_ROUTE_TARGET')
        access=selected[0]['ordinary_access_eligibility']
        require(access=='CLOSED' if actual['target_state']!='DERIVED' else access=='ONLY_IF_EXACT_VIEW_FRESH_AND_SEPARATE_CURRENT_SCOPE_VALID','M08_SELECTED_ROUTE_ACCESS')
        require(all(p in selected[0]['required_predicates'] for p in ('M08.denial_route.event='+actual['route_event'],'M08.denial_route.outcome='+actual['route_outcome'])),'M08_RESULT_TO_ROUTE_BINDING')
    positives=[abort_evidence('MATCH','FAIL','NOT_OCCURRED'),atlas_comparison('MATCH','MATCH','EQUAL','CURRENT','SATISFIED')]
    require(positives[0]['abort_allowed'] and positives[1]['ordinary_access']=='ALLOWED','REJECT_ALL')
    mutations=[]
    def variant(f,identifier):return next(v for c in f['cases'] for v in c['variants'] if v['id']==identifier)
    attacks=[
      ('proposal_scope_without_freshness',lambda m,f:next(r for r in m['M08']['legal_transitions'] if r['event']=='submit_maintenance_proposal' and r['gate_outcome']=='SATISFIED').update(ordinary_access_eligibility='ONLY_IF_SEPARATE_CURRENT_SCOPE_VALID'),'M08_FRESH_SCOPE'),
      ('missing_m08_route',lambda m,f:m['M08']['legal_transitions'].pop(),'TRANSITION_INVENTORY:M08'),
      ('missing_m16_route',lambda m,f:m['M16']['legal_transitions'].pop(),'TRANSITION_INVENTORY:M16'),
      ('invalid_gate_outcome',lambda m,f:m['M08']['legal_transitions'][0].update(gate_outcome='ACCEPT'),'GATE_OUTCOME_ENUM'),
      ('substituted_source_state',lambda m,f:m['M16']['legal_transitions'][0].update(**{'from':'COMMITTED'}),'TRANSITION_INVENTORY:M16'),
      ('legacy_resource_oracle_omission',lambda m,f:variant(f,'T01-V01').pop('resource_oracle'),'VARIANT_ORACLE_OMISSION'),
      ('legacy_consume_hides_validity',lambda m,f:next(r for r in m['M12']['legal_transitions'] if r['event']=='consume_exact_grant').update(to='IN_USE'),'M12_VALIDITY_REPLACED_BY_USE'),
      ('legacy_delegation_hides_validity',lambda m,f:next(r for r in m['M12']['legal_transitions'] if r['event']=='delegate_bounded_subset').update(to='DELEGATED'),'M12_VALIDITY_REPLACED_BY_USE'),
      ('legacy_unknown_lease_access',lambda m,f:next(r for r in m['M10']['legal_transitions'] if r['event']=='expire_or_revoke').update(ordinary_access_eligibility='LIVE'),'M10_UNKNOWN_LEASE_ACCESS'),
      ('legacy_closure_reopening_grant',lambda m,f:next(r for r in m['M18']['legal_transitions'] if r['event']=='trust_unknown').update(authorizer='UNRESOLVED_REOPENING_GRANT'),'M18_CLOSURE_REQUIRES_REOPENING'),
      ('legacy_closure_target',lambda m,f:next(r for r in m['M18']['legal_transitions'] if r['event']=='recognized_compromise').update(to='OPEN'),'M18_CLOSURE_DOES_NOT_CLOSE'),
      ('abort_target_commits',lambda m,f:next(r for r in m['M16']['legal_transitions'] if r['event']=='abort_before_cutover').update(to='COMMITTED'),'TRANSITION_TARGET:M16'),
      ('drift_target_reopens',lambda m,f:next(r for r in m['M08']['legal_transitions'] if r['event']=='denial_with_intervening_drift').update(to='DERIVED'),'TRANSITION_TARGET:M08'),
      ('ack_history_demoted',lambda m,f:variant(f,'T04-V05').update(expected_ack='ABSENT'),'T04_ACK_HISTORY'),
      ('unauthorized_ack_history_demoted',lambda m,f:variant(f,'T04-V06').update(expected_ack='ABSENT'),'T04_ACK_HISTORY'),
      ('precommit_ack_invented',lambda m,f:variant(f,'T04-V01').update(expected_ack='DURABLY_ACKNOWLEDGED_RESPONSE_LOST'),'T04_PREMATURE_ACK'),
      ('consumed_revocation_classification',lambda m,f:variant(f,'T01-V06').update(expected_classification='SATISFIED'),'CLASSIFICATION:T01-V06'),
      ('parent_revocation_classification',lambda m,f:variant(f,'T01-V07').update(expected_classification='SATISFIED'),'CLASSIFICATION:T01-V07'),
      ('stale_scope_reopens_access',lambda m,f:next(r for r in m['M08']['legal_transitions'] if r['event']=='denial_with_intervening_drift' and r['gate_outcome']=='SATISFIED').update(ordinary_access_eligibility='ONLY_IF_SEPARATE_CURRENT_SCOPE_VALID'),'M08_STALE_ACCESS'),
      ('receipt_scope_grants_data',lambda m,f:variant(f,'T04-V05').update(expected_ordinary_access='ALLOWED'),'T04_DATA_SCOPE_ESCALATION'),
      ('expired_receipt_disclosure',lambda m,f:variant(f,'T04-V08').update(expected_receipt_disclosure='ORIGINAL_ACK_RECEIPT_ONLY'),'T04_UNAUTHORIZED_DISCLOSURE'),
      ('wrong_receipt_disclosure',lambda m,f:variant(f,'T04-V07').update(expected_receipt_disclosure='ORIGINAL_ACK_RECEIPT_ONLY'),'T04_UNAUTHORIZED_DISCLOSURE'),
      ('revoked_receipt_disclosure',lambda m,f:variant(f,'T04-V09').update(expected_receipt_disclosure='ORIGINAL_ACK_RECEIPT_ONLY'),'T04_UNAUTHORIZED_DISCLOSURE'),
      ('local_commit_demoted',lambda m,f:variant(f,'T04-V06').update(expected_state='CANDIDATE'),'T04_COMMIT_DEMOTION'),
      ('missing_variant',lambda m,f:f['cases'][0]['variants'].pop(),'VARIANT_COVERAGE'),
      ('duplicate_variant',lambda m,f:f['cases'][0]['variants'].append(copy.deepcopy(f['cases'][0]['variants'][0])),'DUPLICATE_VARIANT'),
      ('abort_composite_bypassed',lambda m,f:next(r for r in m['M16']['legal_transitions'] if r['event']=='abort_before_cutover').update(required_predicates=['always_true']),'M16_COMPOSITE_BYPASS'),
      ('composite_binding_definition_omitted',lambda m,f:m['M08']['predicate_definitions']['atlas_root_comparison'].pop('required_evidence'),'COMPOSITE_DEFINITION:atlas_root_comparison'),
      ('freshness_predicate_omitted',lambda m,f:next(r for r in m['M08']['legal_transitions'] if r['to']=='DERIVED' and r['gate_outcome']=='SATISFIED')['required_predicates'].remove('M08.exact_view_freshness=SATISFIED'),'M08_FRESHNESS_OMITTED')
    ]
    for machine in ('M10','M12','M18'):
        for index,row in enumerate(machines[machine]['legal_transitions']):
            attacks.append((f'omission_{machine}_{index}',lambda m,f,n=machine,i=index:m[n]['legal_transitions'].pop(i),'TRANSITION_INVENTORY:'+machine))
    for row_index,row in enumerate(machines['M08']['legal_transitions']):
        if row['from']=='PROPOSED' and row['event'].startswith('denial_'):
            for predicate_index,predicate in enumerate(row['required_predicates']):
                if predicate.startswith('M08.denial_route.'):
                    def mutate_binding(m,f,i=row_index,j=predicate_index):
                        m['M08']['legal_transitions'][i]['required_predicates'].pop(j)
                    attacks.append((f'omission_M08_denial_binding_{row_index}_{predicate_index}',mutate_binding,'M08_DENIAL_ROUTE_BINDING'))
            for binding_index in (0,1):
                def wrong_binding(m,f,i=row_index,j=binding_index):
                    m['M08']['legal_transitions'][i]['required_predicates'][j]='M08.denial_route.'+('event=unmapped_denial' if j==0 else 'outcome=UNKNOWN')
                attacks.append((f'wrong_M08_denial_binding_{row_index}_{binding_index}',wrong_binding,'M08_DENIAL_ROUTE_BINDING'))
                def contradictory_binding(m,f,i=row_index,j=binding_index):
                    m['M08']['legal_transitions'][i]['required_predicates'].append('M08.denial_route.'+('event=unmapped_denial' if j==0 else 'outcome=UNKNOWN'))
                attacks.append((f'contradictory_M08_denial_binding_{row_index}_{binding_index}',contradictory_binding,'M08_DENIAL_ROUTE_BINDING'))
                def duplicate_binding(m,f,i=row_index,j=binding_index):
                    row=m['M08']['legal_transitions'][i]
                    row['required_predicates'].append(row['required_predicates'][j])
                attacks.append((f'duplicate_M08_denial_binding_{row_index}_{binding_index}',duplicate_binding,'M08_DENIAL_ROUTE_BINDING'))
            def substitute_binding(m,f,i=row_index):
                m['M08']['legal_transitions'][i]['required_predicates']=['always_true']
            attacks.append((f'substitution_M08_denial_binding_{row_index}',substitute_binding,'M08_DENIAL_ROUTE_BINDING'))
    for name,mutate,reason in attacks:
        m=copy.deepcopy(machines);f=copy.deepcopy(fixtures);mutate(m,f)
        # Rebinding this temporary candidate's digest establishes semantic rejection,
        # rather than relying on the original candidate checksum becoming stale.
        data=json.dumps({'machines':m,'fixtures':f},sort_keys=True).encode()
        rebound={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        require(hashlib.sha256(data).hexdigest()==rebound['sha256'],'MUTANT_CUSTODY')
        try:check_proposals(m,f,expected)
        except ValueError as exc:
            require(str(exc)==reason,'WRONG_SEMANTIC_GATE')
            mutations.append({'name':name,'rejected_at':reason,'test_local_binding':rebound,'classification_stage':'SEMANTIC_NOT_CUSTODY'})
            continue
        raise ValueError('MUTANT_ACCEPTED:'+name)
    substituted=json.loads(captured('successor/expected-classifications.json'))
    substituted['classifications']['T01-V06']='SATISFIED'
    substituted_raw=json.dumps(substituted,sort_keys=True).encode()
    try:validate_reference(substituted_raw,hashlib.sha256(substituted_raw).hexdigest())
    except ValueError as exc:require(str(exc)=='EXPECTED_REFERENCE_EXTERNAL_PIN','WRONG_REFERENCE_GATE')
    else:raise ValueError('SUBSTITUTED_REFERENCE_ACCEPTED')
    return {'scope':'EXECUTED_PURE_REFERENCE_AND_STATIC_PROPOSAL_CHECKS_NOT_MACHINE_RUNTIME_OR_AUTHORITY','baseline':baseline,'historical_gap_reproductions':historical_results,'abort_component_combinations':abort_count,'atlas_component_combinations':atlas_count,'m08_joint_routes_checked':len(route_rows),'positive_controls':positives,'semantic_mutations':mutations,'expected_reference_substitution_rejected_at':'EXPECTED_REFERENCE_EXTERNAL_PIN (reference custody, separate from semantic mutants)','production_ready':False,'runtime_machine_transitions':0,'authority_resolved':False}
