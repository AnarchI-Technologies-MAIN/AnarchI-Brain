"""R3 reference decisions over explicitly admitted fixtures. Default admission fails closed.

No authority resolver, cryptographic verifier, durable recorder or transition executor.
Original R1 is preserved as historical evidence and compiled from the exact byte buffer checked against its historical hash.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from dataclasses import asdict, dataclass
import hashlib
import types
import json
from pathlib import Path

R1_SHA = 'cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c'
R1_PATH = Path(__file__).resolve().parents[1] / 'm01_r2/history/repair_r1.py'

class Rejected(ValueError):
    pass

def require(condition, reason):
    if not condition:
        raise Rejected(reason)

# One read, one verified buffer, one compilation. Never delegate to a cache loader.
_r1_bytes = R1_PATH.read_bytes()
require(hashlib.sha256(_r1_bytes).hexdigest() == R1_SHA, 'HISTORICAL_RUNNER_IDENTITY')
_r1_name = '_m01_r3_verified_historical_r1'
require(_r1_name not in sys.modules, 'HISTORICAL_MODULE_ALREADY_LOADED')
historical = types.ModuleType(_r1_name)
historical.__file__ = str(R1_PATH)
historical.__package__ = ''
sys.modules[_r1_name] = historical
try:
    exec(compile(_r1_bytes, str(R1_PATH), 'exec', dont_inherit=True), historical.__dict__)
except BaseException:
    sys.modules.pop(_r1_name, None)
    raise
Frame, Row, Findings = historical.Frame, historical.Row, historical.Findings
S, B, U = historical.DOMAIN
DOMAIN = S, B, U
MISSING = historical.MISSING
ENTRY_CHECKS = ('entry.source_state', 'entry.bound_scope', 'entry.applicable_gate',
                'entry.no_semantic_promotion', 'entry.no_protected_effect')
RECORD_CHECKS = ('record.bound_scope', 'record.provenance', 'record.no_semantic_promotion',
                 'record.authority', 'record.required_conditions', 'record.effect_scope')
SELECTION_POLICY = 'UNRESOLVED_PRESERVING_BLOCKS-v1'

def topology():
    """Verified historical memberships; no caller topology parameter on active APIs."""
    return historical.sources()

def valid_id(value):
    return historical.valid_id(value)

def aggregate(frame, expected, rows):
    try:
        return historical.aggregate(frame, expected, rows)
    except historical.Rejected as exc:
        raise Rejected(str(exc)) from None

def validate_findings(report):
    require(type(report) is Findings, 'FINDINGS_REQUIRED')
    require(report == aggregate(report.frame, report.expected, report.rows), 'FORGED_FINDINGS_SUMMARY')

def report_digest(value):
    """Reference-test report identity only; not an ACBP semantic digest."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=True).encode()).hexdigest()

@dataclass(frozen=True)
class Context:
    frame: Frame
    subject_version: str
    epoch: str

def validate_context(context):
    require(type(context) is Context and type(context.frame) is Frame, 'CONTEXT_REQUIRED')
    require(all(valid_id(x) for x in asdict(context.frame).values()), 'FRAME_IDENTIFIERS')
    require(valid_id(context.subject_version) and valid_id(context.epoch), 'VERSION_EPOCH_REQUIRED')
    require(context.frame.edge in topology(), 'UNKNOWN_EDGE')

def same_scope(left, right):
    validate_context(left)
    validate_context(right)
    require((left.frame.lifecycle, left.frame.operation, left.frame.policy_snapshot,
             left.subject_version, left.epoch) ==
            (right.frame.lifecycle, right.frame.operation, right.frame.policy_snapshot,
             right.subject_version, right.epoch), 'ASSESSMENT_SCOPE_MISMATCH')

@dataclass(frozen=True)
class Catalog:
    context: Context
    basis: str | None
    established: str
    required: tuple[str, ...]

@dataclass(frozen=True)
class RecordingTarget:
    """Reference correlation identity, not authorization or durable idempotency."""
    kind: str
    attempt_digest: str
    predecessor_digest: str

@dataclass(frozen=True)
class Assessment:
    context: Context
    basis: str
    rows: tuple[Row, ...]
    permitted_effects: tuple[str, ...] = ('reference_report',)
    target: RecordingTarget | None = None

@dataclass(frozen=True)
class SourceWitness:
    context: Context
    state: str
    basis: str

def admitted(context, role, payload, verifier):
    """Verifier is a separately governed dependency; no verifier means unresolved."""
    validate_context(context)
    if verifier is None:
        return U
    outcome = verifier.verify(context, role, report_digest(payload))
    require(type(outcome) is str and outcome in DOMAIN, 'ADMISSION_OUTCOME')
    return outcome

@dataclass(frozen=True)
class AttemptReview:
    context: Context
    source_state: str
    catalog: Catalog
    predicates: Findings
    requirements: Findings
    entry_assessment: Assessment | None
    entry: Findings | None
    source_witness: SourceWitness | None
    admissions: tuple[tuple[str, str], ...]
    known_blocks: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    missing_reports: tuple[str, ...]
    positive_conditions_met: bool

def evaluate_attempt(context, catalog, predicate_rows, requirement_rows,
                     entry_assessment=None, source_witness=None, verifier=None):
    validate_context(context)
    frame = context.frame
    require(frame.edge in ('C01', 'C02', 'C03', 'C04', 'C05'), 'PROGRESS_EDGE_REQUIRED')
    require(type(catalog) is Catalog and catalog.context == context, 'CATALOG_CONTEXT')
    require(type(catalog.established) is str and catalog.established in DOMAIN, 'CATALOG_RESULT')
    require(type(catalog.required) is tuple, 'REQUIRED_MEMBERSHIP_TUPLE')
    if catalog.established != U:
        require(valid_id(catalog.basis), 'CATALOG_BASIS_REQUIRED')
    source = topology()[frame.edge][0]
    predicates = aggregate(frame, topology()[frame.edge][2], predicate_rows)
    requirements = aggregate(frame, catalog.required, requirement_rows)
    reports = [('predicate', predicates), ('requirement', requirements)]
    admissions = [ ('catalog', admitted(context, 'catalog', asdict(catalog), verifier)),
                   ('predicates', admitted(context, 'predicates', asdict(predicates), verifier)),
                   ('requirements', admitted(context, 'requirements', asdict(requirements), verifier)) ]
    entry = None
    if frame.edge in ('C03', 'C04'):
        if entry_assessment is None:
            entry = aggregate(frame, ENTRY_CHECKS, ())
            admissions.append(('entry', U))
        if entry_assessment is not None:
            require(type(entry_assessment) is Assessment, 'ENTRY_ASSESSMENT_REQUIRED')
            same_scope(entry_assessment.context, context)
            require(entry_assessment.context.frame.edge == frame.edge, 'ENTRY_EDGE_MISMATCH')
            require(entry_assessment.context.frame.evaluation != frame.evaluation, 'ENTRY_EVALUATION_REUSED')
            require(valid_id(entry_assessment.basis), 'ENTRY_BASIS_REQUIRED')
            require(entry_assessment.target is None, 'ENTRY_HAS_RECORDING_TARGET')
            require(entry_assessment.permitted_effects == ('reference_report',), 'ENTRY_EFFECT_SCOPE')
            entry = aggregate(entry_assessment.context.frame, ENTRY_CHECKS, entry_assessment.rows)
            admissions.append(('entry', admitted(entry_assessment.context, 'entry', asdict(entry_assessment), verifier)))
        reports.append(('entry', entry))
    if frame.edge not in ('C03', 'C04'):
        require(entry_assessment is None, 'UNEXPECTED_ENTRY_ASSESSMENT')
    if source_witness is None:
        admissions.append(('source', U))
    if source_witness is not None:
        require(type(source_witness) is SourceWitness and source_witness.context == context,
                'SOURCE_CONTEXT')
        require(source_witness.state == source and valid_id(source_witness.basis), 'SOURCE_STATE_OR_BASIS')
        admissions.append(('source', admitted(context, 'source', asdict(source_witness), verifier)))
    blocks, unknown, missing = [], [], []
    for prefix, report in reports:
        blocks.extend(prefix + ':' + x for x in report.blocked)
        unknown.extend(prefix + ':' + x for x in report.unresolved)
        missing.extend(prefix + ':' + x for x in report.missing)
    if catalog.established == B:
        blocks.append('catalog:governing_basis_rejected')
    if catalog.established == U:
        unknown.append('catalog:not_established')
    for role, outcome in admissions:
        if outcome == B:
            blocks.append('admission:' + role)
        if outcome == U:
            unknown.append('admission:' + role)
    # C03 empty historical membership can pass only through its mandatory full entry assessment.
    predicate_ok = predicates.all_reported_members_satisfied
    if frame.edge == 'C03':
        predicate_ok = predicates.expected == ()
    entry_ok = entry is None or entry.all_reported_members_satisfied
    positive = (catalog.established == S and predicate_ok and entry_ok
                and not blocks and not unknown and not missing)
    return AttemptReview(context, source, catalog, predicates, requirements, entry_assessment,
                         entry, source_witness, tuple(admissions), tuple(sorted(blocks)),
                         tuple(sorted(unknown)), tuple(sorted(missing)), positive)

def validate_attempt(review, verifier=None):
    require(type(review) is AttemptReview, 'ATTEMPT_REVIEW_REQUIRED')
    replay = evaluate_attempt(review.context, review.catalog, review.predicates.rows,
                              review.requirements.rows, review.entry_assessment,
                              review.source_witness, verifier)
    require(replay == review, 'FORGED_ATTEMPT_REVIEW')

def p08_reference(catalog, outcomes):
    require(type(catalog) is Catalog, 'CATALOG_REQUIRED')
    validate_context(catalog.context)
    validate_findings(outcomes)
    require(outcomes.frame == catalog.context.frame and outcomes.expected == tuple(sorted(catalog.required)),
            'P08_REPORT_CATALOG_MISMATCH')
    require(catalog.established in DOMAIN, 'CATALOG_RESULT')
    if catalog.established != S or outcomes.unresolved or outcomes.missing:
        return U
    return S

@dataclass(frozen=True)
class RouteDecision:
    policy: str
    attempt_digest: str
    edge: str | None
    target: str | None
    retains_both: bool

def select_route(attempt, verifier=None):
    validate_attempt(attempt, verifier)
    b = bool(attempt.known_blocks)
    u = bool(attempt.unresolved_findings or attempt.missing_reports)
    target = None
    if b:
        target = 'CI5_BLOCKED'
    if u:
        target = 'CI6_UNRESOLVED'
    matches = tuple(edge for edge, row in topology().items()
                    if row[0] == attempt.source_state and row[1] == target) if target else ()
    require(len(matches) <= 1, 'AMBIGUOUS_ROUTE')
    edge = matches[0] if matches else None
    return RouteDecision(SELECTION_POLICY, report_digest(asdict(attempt)), edge, target, b and u)

@dataclass(frozen=True)
class ControlReview:
    context: Context
    target_state: str
    carried_attempt: AttemptReview
    assessment: Assessment
    record_checks: Findings
    decision: RouteDecision | None
    predecessor_digest: str
    conditions_met: bool
    record_admission: str
    prior_diagnostic: ControlReview | None = None
    occurrence: Occurrence | None = None
    grants_protected_operation_authority: bool = False

def recording_target(attempt, kind, predecessor):
    """Build a request target; the transition function still verifies all underlying reviews."""
    require(type(attempt) is AttemptReview, 'ATTEMPT_REVIEW_REQUIRED')
    require(kind in ('DIAGNOSTIC', 'CLOSURE'), 'RECORDING_TARGET_KIND')
    return RecordingTarget(kind, report_digest(asdict(attempt)), report_digest(asdict(predecessor)))

def recording(context, attempt, assessment, forbidden_evaluations, target, verifier):
    same_scope(context, attempt.context)
    require(context.frame.evaluation not in forbidden_evaluations, 'CONTROL_EVALUATION_REUSED')
    require(type(assessment) is Assessment and assessment.context == context, 'RECORD_ASSESSMENT_CONTEXT')
    require(type(assessment.target) is RecordingTarget and assessment.target == target,
            'RECORDING_TARGET_MISMATCH')
    require(valid_id(assessment.basis), 'RECORD_BASIS_REQUIRED')
    require(assessment.permitted_effects == ('reference_report',), 'RECORD_EFFECT_SCOPE')
    report = aggregate(context.frame, RECORD_CHECKS, assessment.rows)
    outcome = admitted(context, 'recording', asdict(assessment), verifier)
    return report, outcome

def evaluate_diagnostic(context, attempt, assessment, decision, verifier=None):
    validate_attempt(attempt, verifier)
    validate_context(context)
    require(type(decision) is RouteDecision and decision == select_route(attempt, verifier), 'ROUTE_DECISION_REQUIRED')
    require(decision.edge is not None and context.frame.edge == decision.edge, 'ROUTE_NOT_SELECTED')
    require(context.frame.edge in ('C06','C07','C08','C09','C10','C11','C12','C13'), 'DIAGNOSTIC_EDGE')
    forbidden = {attempt.context.frame.evaluation}
    if attempt.entry_assessment:
        forbidden.add(attempt.entry_assessment.context.frame.evaluation)
    target = recording_target(attempt, 'DIAGNOSTIC', attempt)
    report, admission = recording(context, attempt, assessment, forbidden, target, verifier)
    eligible = report.all_reported_members_satisfied and admission == S
    return ControlReview(context, decision.target, attempt, assessment, report, decision,
                         report_digest(asdict(attempt)), eligible, admission)

@dataclass(frozen=True)
class Occurrence:
    context: Context
    assessed_attempt: str
    result: str
    basis: str | None
    fence_result: str

def evaluate_closure(context, attempt, assessment, prior=None, occurrence=None, verifier=None):
    validate_attempt(attempt, verifier)
    validate_context(context)
    edge = context.frame.edge
    require(edge in ('C14', 'C15', 'C16'), 'CLOSURE_EDGE_REQUIRED')
    forbidden = {attempt.context.frame.evaluation}
    if attempt.entry_assessment:
        forbidden.add(attempt.entry_assessment.context.frame.evaluation)
    predecessor = None
    witness = False
    if edge in ('C15', 'C16'):
        require(type(prior) is ControlReview and occurrence is None, 'DIAGNOSTIC_PREDECESSOR_REQUIRED')
        require(prior.carried_attempt == attempt, 'PREDECESSOR_ATTEMPT_MISMATCH')
        replay = evaluate_diagnostic(prior.context, attempt, prior.assessment, prior.decision, verifier)
        require(replay == prior, 'FORGED_PREDECESSOR')
        require(prior.target_state == topology()[edge][0], 'CLOSURE_SOURCE_MISMATCH')
        forbidden.add(prior.context.frame.evaluation)
        predecessor = asdict(prior)
        witness = prior.conditions_met
    if edge == 'C14':
        require(prior is None and type(occurrence) is Occurrence, 'OCCURRENCE_REQUIRED')
        require(attempt.context.frame.edge == 'C05', 'EXECUTION_ATTEMPT_REQUIRED')
        same_scope(occurrence.context, attempt.context)
        require(occurrence.context.frame.edge == 'C05', 'OCCURRENCE_EDGE')
        require(occurrence.assessed_attempt == attempt.context.frame.evaluation, 'OCCURRENCE_ATTEMPT_MISMATCH')
        require(occurrence.context.frame.evaluation not in forbidden, 'OCCURRENCE_EVALUATION_REUSED')
        require(type(occurrence.result) is str and occurrence.result in DOMAIN
                and type(occurrence.fence_result) is str and occurrence.fence_result in DOMAIN, 'OCCURRENCE_RESULT')
        if occurrence.result != U:
            require(valid_id(occurrence.basis), 'OCCURRENCE_BASIS_REQUIRED')
        admission = admitted(occurrence.context, 'occurrence', asdict(occurrence), verifier)
        # Records can describe unauthorized occurrences. Closure never legitimizes them.
        witness = occurrence.result == S and occurrence.fence_result == S and admission == S
        forbidden.add(occurrence.context.frame.evaluation)
        predecessor = asdict(occurrence)
    target = RecordingTarget('CLOSURE', report_digest(asdict(attempt)), report_digest(predecessor))
    report, admission = recording(context, attempt, assessment, forbidden, target, verifier)
    own_conditions = report.all_reported_members_satisfied and admission == S
    return ControlReview(context, topology()[edge][1], attempt, assessment, report, None,
                         report_digest(predecessor), witness and own_conditions, admission, prior, occurrence)
