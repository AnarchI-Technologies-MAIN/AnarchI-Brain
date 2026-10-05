"""Unadopted finite M03 routing model. Fixture findings are not authenticated grants."""
REQUIRED={'normalize_with_provenance':('Observe','Propose'),'propose_neighborhood':('Propose',)}
SOURCE={'normalize_with_provenance':'RECEIVED','propose_neighborhood':'NORMALIZED_CANDIDATE'}
TARGET={'normalize_with_provenance':'NORMALIZED_CANDIDATE','propose_neighborhood':'PROPOSED'}
PREDICATES=('exact_subject','applicable_semantics','current_predecessor','authority_root_freshness','resource_bounds')
def describe_transition(event,grants,predicates):
    if event not in REQUIRED:raise ValueError('UNKNOWN_EVENT')
    if set(predicates)-set(PREDICATES):raise ValueError('UNEXPECTED_PREDICATE')
    findings={'authority.'+dimension:grants.get(dimension,'UNRESOLVED') for dimension in REQUIRED[event]}
    findings.update({'predicate.'+name:predicates.get(name,'UNRESOLVED') for name in PREDICATES})
    if any(value not in ('SATISFIED','BLOCKED','UNRESOLVED') for value in findings.values()):raise ValueError('FINDING_ENUM')
    # This model consumes fixture findings only. It cannot authenticate or issue authority.
    outcome='BLOCKED' if 'BLOCKED' in findings.values() else 'UNRESOLVED' if 'UNRESOLVED' in findings.values() else 'SATISFIED'
    return dict(outcome=outcome,state=TARGET[event] if outcome=='SATISFIED' else SOURCE[event],operation_effect=('NONCANONICAL_NORMALIZATION' if event=='normalize_with_provenance' else 'NONCANONICAL_PROPOSAL') if outcome=='SATISFIED' else 'NONE',receipt_boundary='BOUNDED_NONAUTHORITATIVE_ATTEMPT_ONLY_SCHEMA_UNRESOLVED',ordinary_access='CLOSED',canonical_membership=False,findings=findings)
