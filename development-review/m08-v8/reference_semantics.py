"""Pure, unadopted review model. No grants, database, network, or machine executor."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REFERENCE_PIN='f575ea159b4318b353d45f029e6613ec34ccdbaa37f627cc3545a073288bf988'
def require(value,reason):
    if not value: raise ValueError(reason)

def abort_evidence(binding,proof,occurrence):
    require(binding in ('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),'ABORT_BINDING_ENUM')
    require(proof in ('FAIL','PASS','UNKNOWN','MISSING','INVALID','CONTRADICTORY'),'ABORT_PROOF_ENUM')
    require(occurrence in ('NOT_OCCURRED','OCCURRED','UNKNOWN','MISSING','CONTRADICTORY'),'ABORT_OCCURRENCE_ENUM')
    findings={'binding':binding,'proof':proof,'occurrence':occurrence}
    if binding in ('MISMATCH','INVALID','CONTRADICTORY') or proof in ('INVALID','CONTRADICTORY') or occurrence in ('OCCURRED','CONTRADICTORY'):
        return {'classification':'BLOCKED','findings':findings,'abort_allowed':False}
    if binding=='MISSING' or proof in ('UNKNOWN','MISSING') or occurrence in ('UNKNOWN','MISSING'):
        return {'classification':'UNRESOLVED','findings':findings,'abort_allowed':False}
    classification='SATISFIED' if proof=='FAIL' else 'BLOCKED'
    return {'classification':classification,'findings':findings,'abort_allowed':classification=='SATISFIED'}

def atlas_comparison(binding,comparability,relation,freshness,scope):
    require(binding in ('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),'ATLAS_BINDING_ENUM')
    require(comparability in ('MATCH','MISMATCH','MISSING','UNKNOWN'),'ATLAS_COMPARABILITY_ENUM')
    require(relation in ('EQUAL','DIFFERENT','UNKNOWN','CONTRADICTORY'),'ATLAS_RELATION_ENUM')
    require(freshness in ('CURRENT','STALE','UNKNOWN'),'ATLAS_FRESHNESS_ENUM')
    require(scope in ('SATISFIED','BLOCKED','UNRESOLVED'),'ATLAS_SCOPE_ENUM')
    findings=dict(binding=binding,comparability=comparability,relation=relation,freshness=freshness,scope=scope)
    classification='SATISFIED'
    if binding in ('MISMATCH','INVALID','CONTRADICTORY') or comparability=='MISMATCH' or relation=='CONTRADICTORY':classification='BLOCKED'
    elif binding=='MISSING' or comparability in ('MISSING','UNKNOWN') or relation=='UNKNOWN':classification='UNRESOLVED'
    allowed=classification=='SATISFIED' and relation=='EQUAL' and freshness=='CURRENT' and scope=='SATISFIED'
    return {'classification':classification,'findings':findings,'ordinary_access':'ALLOWED' if allowed else 'CLOSED'}


def atlas_denial_route(binding,comparability,relation,freshness,scope):
    """Pure route description for an already observed maintenance denial."""
    comparison=atlas_comparison(binding,comparability,relation,freshness,scope)
    classification=comparison['classification']
    event='denial_preserves_atlas';outcome=classification
    target='PROPOSED' if classification=='BLOCKED' else 'STALE'
    if classification=='SATISFIED':
        target='DERIVED'
        if relation=='DIFFERENT':event='denial_with_intervening_drift';target='STALE'
        elif freshness!='CURRENT':
            event='denial_with_insufficient_freshness';target='STALE'
            outcome='SATISFIED' if freshness=='STALE' else 'UNRESOLVED'
    return dict(comparison_classification=classification,route_event=event,route_outcome=outcome,target_state=target,ordinary_access=comparison['ordinary_access'] if target=='DERIVED' else 'CLOSED',findings=comparison['findings'])

def check_proposals(machines,fixtures,expected):
    require(set(machines)=={f'M{i:02d}' for i in range(1,20)},'MACHINE_INVENTORY')
    for name,m in machines.items():
        require('UNADOPTED' in m['status'] and 'UNRESOLVED' in m['authority_resolution'],'ADOPTION_PROMOTION')
        keys=[(r['from'],r['event'],r['gate_outcome']) for r in m['legal_transitions']]
        require(len(keys)==len(set(keys)),'DUPLICATE_ROUTE')
        require(all(k[2] in ('SATISFIED','BLOCKED','UNRESOLVED') for k in keys),'GATE_OUTCOME_ENUM')
    # Carry forward the previously reviewed lifecycle invariants rather than
    # replacing them with the new four-finding checks.
    for row in machines['M12']['legal_transitions']:
        if row['event'] in ('consume_exact_grant','delegate_bounded_subset'):
            require(row['to']=='GRANTED','M12_VALIDITY_REPLACED_BY_USE')
    require('entire bounded ancestor chain' in machines['M12']['delegation_rule'],'M12_ANCESTOR_FRESHNESS')
    for row in machines['M18']['legal_transitions']:
        if row['event'] in ('recognized_compromise','trust_unknown'):
            require(row['to']=='CLOSED' and row['ordinary_access_eligibility']=='CLOSED','M18_CLOSURE_DOES_NOT_CLOSE')
            require('no positive reopening' in row['authorizer'],'M18_CLOSURE_REQUIRES_REOPENING')
    for row in machines['M10']['legal_transitions']:
        if row['event']=='expire_or_revoke':require(row['ordinary_access_eligibility']=='CLOSED','M10_UNKNOWN_LEASE_ACCESS')
    route_groups={'M08':(('ABSENT','rebuild_from_receipts'),('DERIVED','detect_root_drift'),('STALE','rebuild_from_receipts'),('DERIVED','submit_maintenance_proposal'),('PROPOSED','denial_preserves_atlas'),('PROPOSED','denial_with_intervening_drift'),('PROPOSED','denial_with_insufficient_freshness')),'M16':(('PROPOSED','authorize_migration'),('AUTHORIZED','verify_shadow_reconstruction'),('VERIFIED','guarded_cutover'),('AUTHORIZED','abort_before_cutover'),('VERIFIED','abort_before_cutover'))}
    route_groups.update({'M10': [('AUTHORIZED', 'create_bounded_projection'), ('EXPIRED', 'deconstruct'), ('LIVE', 'complete_job'), ('LIVE', 'expire_or_revoke')], 'M12': [('ENROLLED', 'replace_governance_root'), ('GRANTED', 'consume_exact_grant'), ('GRANTED', 'delegate_bounded_subset'), ('GRANTED', 'expire'), ('GRANTED', 'revoke'), ('GRANTED', 'rotate_issuer'), ('PROPOSED', 'enroll_identity'), ('PROPOSED', 'independent_issuer_grant')], 'M18': [('CLOSED', 'independently_verify_recovery'), ('OPEN', 'recognized_compromise'), ('OPEN', 'trust_unknown'), ('RECOVERY_VERIFIED', 'publish_fresh_epoch'), ('RECOVERY_VERIFIED', 'trust_unknown')]})
    for name,groups in route_groups.items():
        expected_routes={(state,event,outcome) for state,event in groups for outcome in ('SATISFIED','BLOCKED','UNRESOLVED')}
        actual_routes={(r['from'],r['event'],r['gate_outcome']) for r in machines[name]['legal_transitions']}
        require(actual_routes==expected_routes,'TRANSITION_INVENTORY:'+name)
    success_targets={'M08':{'rebuild_from_receipts':'DERIVED','detect_root_drift':'STALE','submit_maintenance_proposal':'PROPOSED','denial_preserves_atlas':'DERIVED','denial_with_intervening_drift':'STALE','denial_with_insufficient_freshness':'STALE'},'M16':{'authorize_migration':'AUTHORIZED','verify_shadow_reconstruction':'VERIFIED','guarded_cutover':'COMMITTED','abort_before_cutover':'ABORTED'}}
    for name,events in success_targets.items():
        for row in machines[name]['legal_transitions']:
            require(row['event'] in events,'UNEXPECTED_TRANSITION_EVENT:'+name)
            target=events[row['event']] if row['gate_outcome']=='SATISFIED' else row['from']
            if name=='M08' and row['event'] in ('denial_preserves_atlas','denial_with_intervening_drift','denial_with_insufficient_freshness') and row['gate_outcome']=='UNRESOLVED':target='STALE'
            require(row['to']==target,'TRANSITION_TARGET:'+name)
    for row in machines['M08']['legal_transitions']:
        if row['from']=='PROPOSED' and row['event'].startswith('denial_'):
            expected_binding=[f"M08.denial_route.event={row['event']}",f"M08.denial_route.outcome={row['gate_outcome']}"]
            if row['event']=='denial_preserves_atlas' and row['gate_outcome']=='SATISFIED':
                expected_binding.append('M08.exact_view_freshness=SATISFIED')
            require(row['required_predicates']==expected_binding,'M08_DENIAL_ROUTE_BINDING')
        if row['to']=='STALE' or row['gate_outcome']!='SATISFIED':require(row['ordinary_access_eligibility']=='CLOSED','M08_STALE_ACCESS')
        if row['gate_outcome']=='SATISFIED' and row['ordinary_access_eligibility']!='CLOSED':
            require('M08.exact_view_freshness=SATISFIED' in row['required_predicates'],'M08_FRESHNESS_OMITTED')
            require(row['ordinary_access_eligibility']=='ONLY_IF_EXACT_VIEW_FRESH_AND_SEPARATE_CURRENT_SCOPE_VALID','M08_FRESH_SCOPE')
    for row in machines['M16']['legal_transitions']:
        if row['event']=='abort_before_cutover':require(row['required_predicates']==[f"M16.abort_before_cutover.abort_evidence={row['gate_outcome']}"],'M16_COMPOSITE_BYPASS')
    case_ids=[c['id'] for c in fixtures['cases']]
    require(len(case_ids)==len(set(case_ids)) and set(case_ids)=={f'T{i:02d}' for i in range(1,14)},'CASE_INVENTORY')
    variants=[v for c in fixtures['cases'] for v in c['variants']]
    ids=[v['id'] for v in variants]
    require(len(ids)==len(set(ids)),'DUPLICATE_VARIANT')
    require(set(ids)==set(expected),'VARIANT_COVERAGE')
    for v in variants:
        require(all(k in v for k in ('expected_classification','expected_receipt','expected_canonical_root','forbidden_effects','causal_oracle','resource_oracle')),'VARIANT_ORACLE_OMISSION')
        require(v['expected_classification']==expected[v['id']],'CLASSIFICATION:'+v['id'])
    require(len(next(c for c in fixtures['cases'] if c['id']=='T01')['variants'])==7,'T01_REVOCATION_COVERAGE')
    t04=next(c for c in fixtures['cases'] if c['id']=='T04')
    require('never demote committed state' in ' '.join(t04['oracles']),'T04_COMMIT_DEMOTION')
    for v in t04['variants']:
        require(v['ordinary_data_authorization']=='BLOCKED' and v['expected_ordinary_access']=='DENIED','T04_DATA_SCOPE_ESCALATION')
        require(all(k in v for k in ('expected_state','expected_ack','receipt_disclosure_authorization','expected_receipt_disclosure')),'T04_AXIS_OMISSION')
        if v['id']=='T04-V05':
            require(v['receipt_disclosure_authorization']=='SATISFIED_EXACT_CURRENT_RECEIPT_ONLY' and v['expected_receipt_disclosure']=='ORIGINAL_ACK_RECEIPT_ONLY','T04_EXACT_RECEIPT_SCOPE')
            require(v['expected_state']=='ACKNOWLEDGED_RESPONSE_LOST' and v['expected_canonical_root']=='R1','T04_COMMIT_DEMOTION')
            require(v['expected_ack']=='DURABLY_ACKNOWLEDGED_RESPONSE_LOST','T04_ACK_HISTORY')
        if v['id'] in ('T04-V06','T04-V07','T04-V08','T04-V09'):
            require(v['expected_receipt_disclosure']=='NONE','T04_UNAUTHORIZED_DISCLOSURE')
            require(v['expected_state']=='ACKNOWLEDGED_RESPONSE_LOST' and v['expected_canonical_root']=='R1','T04_COMMIT_DEMOTION')
            require(v['expected_ack']=='DURABLY_ACKNOWLEDGED_RESPONSE_LOST','T04_ACK_HISTORY')
        if v['id'] in ('T04-V01','T04-V02','T04-V03','T04-V04'):
            require(v['expected_ack']=='ABSENT_OR_UNRESOLVED','T04_PREMATURE_ACK')
    for name,key in [('M08','atlas_root_comparison'),('M16','abort_evidence')]:
        definition=machines[name]['predicate_definitions'].get(key,{})
        require(all(k in definition for k in ('components','required_evidence','precedence','finding_retention')),'COMPOSITE_DEFINITION:'+key)
    return {'machines':len(machines),'cases':len(case_ids),'variants':len(ids)}

def validate_reference(raw, expected_digest):
    require(expected_digest==REFERENCE_PIN and hashlib.sha256(raw).hexdigest()==REFERENCE_PIN,'EXPECTED_REFERENCE_EXTERNAL_PIN')
    return json.loads(raw)['classifications']

def load_reference(expected_digest):
    return validate_reference((ROOT/'successor/expected-classifications.json').read_bytes(),expected_digest)
