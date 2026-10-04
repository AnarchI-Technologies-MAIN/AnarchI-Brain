#!/usr/bin/env python3
"""SW0-010 M01 repair candidate, isolated reference models and fresh qualification.

Python 3.10+, standard library. This file does not write to the AnarchI repository.
No authority resolver, effect executor, cryptographic validator, or receipt issuer.
--model-only explicitly omits the local-repository and native-PowerShell checks.
--repo requires both checks and reads the pinned repository before and after tests.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse
from dataclasses import dataclass, asdict, replace
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Callable, Sequence

HEAD = '79fd607b3b8983fdd2d0254f3af59df9a92257b8'
TREE = '2bc508ef199311208cc4b7c68398f61b22d4adf1'
C9_SHA = '29f5caf40e6c94c01030ab444ab06420498ca8e1b28ec1b2fdb59e917d8afa60'
C13_SHA = 'd1f1009d11eb0a18fce6ec66372f2d5a4340b9dc48e0eb9c9d13445d8388a54b'
FAILED_C14_SHA = '294741d89a907dd32e6bb51cb278b8a911d1452dd5dc325ddb62b4a1c91a97e7'
DOMAIN = ('SATISFIED', 'BLOCKED', 'UNRESOLVED')
S, B, U = DOMAIN
MISSING = 'MISSING_REPORT'

C9_ROWS = (
'C01|CI0_PRESENTED>CI1_OBSERVED|PREDICATES=P01,P11|UNRESOLVED=U05,U06',
'C02|CI1_OBSERVED>CI2_PROPOSAL_AVAILABLE|PREDICATES=P02,P10|UNRESOLVED=NONE',
'C03|CI1_OBSERVED>CI3_ACTION_GATED|PREDICATES=NONE|UNRESOLVED=U01,U02,U03,U04',
'C04|CI2_PROPOSAL_AVAILABLE>CI3_ACTION_GATED|PREDICATES=P10|UNRESOLVED=U01,U02,U03,U04',
'C05|CI3_ACTION_GATED>CI4_BOUNDARY_EXECUTED|PREDICATES=P03,P04,P05,P06,P07,P08|UNRESOLVED=U01,U02,U03,U04,U08',
'C06|CI0_PRESENTED>CI5_BLOCKED|PREDICATES=P09|UNRESOLVED=NONE',
'C07|CI1_OBSERVED>CI5_BLOCKED|PREDICATES=P09|UNRESOLVED=NONE',
'C08|CI2_PROPOSAL_AVAILABLE>CI5_BLOCKED|PREDICATES=P09,P10|UNRESOLVED=NONE',
'C09|CI3_ACTION_GATED>CI5_BLOCKED|PREDICATES=P09|UNRESOLVED=U01,U02,U03,U04',
'C10|CI0_PRESENTED>CI6_UNRESOLVED|PREDICATES=P08|UNRESOLVED=NONE',
'C11|CI1_OBSERVED>CI6_UNRESOLVED|PREDICATES=P08|UNRESOLVED=NONE',
'C12|CI2_PROPOSAL_AVAILABLE>CI6_UNRESOLVED|PREDICATES=P08,P10|UNRESOLVED=NONE',
'C13|CI3_ACTION_GATED>CI6_UNRESOLVED|PREDICATES=P08|UNRESOLVED=U01,U02,U03,U04',
'C14|CI4_BOUNDARY_EXECUTED>CI7_CLOSED|PREDICATES=P12|UNRESOLVED=U07,U08',
'C15|CI5_BLOCKED>CI7_CLOSED|PREDICATES=P12|UNRESOLVED=U07',
'C16|CI6_UNRESOLVED>CI7_CLOSED|PREDICATES=P08,P12|UNRESOLVED=U07',
)
C9_HEADER = (
'SW0-010-M01-C9-EDGE-GUARD-COMPOSITION-CANDIDATE-v1',
'HEAD=' + HEAD,
'C6=80b8bef02d4429b20bcb79157fda33417bba4a35a72f40d36b8d1a09499a5292',
'C7=740c75530c073f64599c73f0299c7e2f4a06b6063ee63822096394373a7640c9',
'C8_R1=fba74e5bccfa13b50a528e8cceed422059cb1e7f31c63d3d697373c7cb930ea7',
'COMPOSITION_OPERATOR=UNRESOLVED', 'PRECEDENCE=UNRESOLVED',
'EVALUATION_ORDER=UNRESOLVED', 'EDGE_OUTCOME_MAPPING=UNRESOLVED',
'EMPTY_PREDICATE_SET_MEANS_UNCONDITIONAL=False', '--- EDGE COMPOSITIONS ---',
)
INPUTS = (
'IR01|TRANSITION_CONTEXT|Logical control context identifying the M01 candidate edge and relevant source and target state; control context supplies no semantic authority, authorization, permission, Evidence status, canonicality, truth, or predicate result.',
'IR02|AUTHORITY_APPLICABILITY_CONTEXT|Logical context sufficient to evaluate whether the authority dimension applicable to the predicate is established and, where bounded, whether the evaluated operation is within that bound; this role does not create authority and does not define the authority-resolution mechanism.',
'IR03|ESTABLISHED_PREREQUISITE_CONTEXT|Logical context limited to prerequisites already established as required for the evaluated transition and their resolvability; presence in this context creates no new prerequisite and absence does not mean permission.',
'IR04|SOURCE_SUBSTITUTION_CONTEXT|Logical context sufficient to evaluate whether execution is being used as a source or substitute for an already-required authorization, permission, effective capability, qualification, or canonicalization prerequisite; this role creates none of those prerequisites.',
'IR05|BLOCKING_CONDITION_CONTEXT|Logical context sufficient to evaluate whether a determinate forbidden, out-of-scope, or unsatisfied required condition is established; indeterminate status is not converted to BLOCKED.',
'IR06|SEMANTIC_TREATMENT_CONTEXT|Logical context sufficient to evaluate whether observation, proposal, or closure is being assigned a forbidden semantic elevation; this role does not itself assign Evidence status, authorization, canonicality, truth, success, effect, or downstream admission.',
)
INPUT_BINDINGS = (
'P01|INPUTS=IR01,IR02', 'P02|INPUTS=IR01,IR02', 'P03|INPUTS=IR01,IR02',
'P04|INPUTS=IR01,IR03,IR04', 'P05|INPUTS=IR01,IR03,IR04',
'P06|INPUTS=IR01,IR03,IR04', 'P07|INPUTS=IR01,IR03,IR04',
'P08|INPUTS=IR01,IR03', 'P09|INPUTS=IR01,IR05',
'P10|INPUTS=IR01,IR06', 'P11|INPUTS=IR01,IR06', 'P12|INPUTS=IR01,IR06',
)
INPUT_QUESTIONS = (
'IQ01|Concrete serialization or schema for IR01-IR06 remains unresolved.',
'IQ02|The authoritative source and resolution mechanism for IR02 remains unresolved.',
'IQ03|The mechanism by which a prerequisite becomes established as required before appearing in IR03 remains unresolved.',
'IQ04|The representation and provenance of IR04 source-substitution determinations remains unresolved.',
'IQ05|The representation and provenance of IR05 blocking-condition determinations remains unresolved.',
'IQ06|The representation and provenance of IR06 semantic-treatment determinations remains unresolved.',
'IQ07|Whether any input role is represented by an Artifact, Receipt, reference, computed view, or other structure remains unresolved.',
'IQ08|Whether predicate inputs are persisted, cached, reconstructed, or transition-local remains unresolved.',
'IQ09|Composition operator, precedence, evaluation order, short-circuit behavior, and edge outcome mapping remain unresolved.',
'IQ10|U01-U08 remain unresolved and are not resolved by predicate input visibility.',
)
C13_HEADER = (
'SW0-010-M01-C13-PREDICATE-INPUT-ENVELOPE-CANDIDATE-v1', 'HEAD=' + HEAD,
'C11=88405caaf336b77ea20aeadbe0a6fb38e3083c49dbdfe59df6e909953e95ef54',
'C12=c3360e309abc869d8cd0d3988893f820a4c27478ffddbbe78e1177222eda0d78',
'INPUT_ROLE_KIND=LOGICAL_VISIBILITY_ROLE', 'INPUT_SCHEMA=UNRESOLVED',
'INPUT_PERSISTENCE=UNRESOLVED', 'PREDICATE_GLOBAL_READ_AUTHORITY=False', '--- INPUT ROLES ---',
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(value: object) -> bytes:
    # This is a test-report encoding, not a replacement product serialization profile.
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')


def lines_sha(lines: Sequence[str]) -> str:
    return sha(('\n'.join(lines) + '\n').encode('utf-8'))


class Rejected(ValueError):
    """Reference input validation error, not a fabricated BLOCKED predicate result."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise Rejected(reason)


def valid_id(value: object) -> bool:
    return type(value) is str and re.fullmatch(r'[A-Za-z0-9_.:-]+', value) is not None


@dataclass(frozen=True)
class Frame:
    lifecycle: str
    evaluation: str
    operation: str
    policy_snapshot: str
    edge: str


@dataclass(frozen=True)
class Row:
    frame: Frame
    identity: str
    result: str


@dataclass(frozen=True)
class Findings:
    frame: Frame
    expected: tuple[str, ...]
    rows: tuple[Row, ...]
    satisfied: tuple[str, ...]
    blocked: tuple[str, ...]
    unresolved: tuple[str, ...]
    missing: tuple[str, ...]
    coverage: str
    all_reported_members_satisfied: bool


def aggregate(frame: Frame, expected: Sequence[str], rows: Sequence[Row]) -> Findings:
    require(type(frame) is Frame and all(valid_id(x) for x in asdict(frame).values()), 'INVALID_FRAME')
    require(re.fullmatch(r'C(?:0[1-9]|1[0-6])',frame.edge) is not None,'UNKNOWN_M01_EDGE')
    require(type(expected) in (tuple, list) and type(rows) in (tuple, list), 'EXPECTED_ARRAYS')
    expected_set: set[str] = set()
    for identity in expected:
        require(valid_id(identity), 'INVALID_EXPECTED_ID')
        require(identity not in expected_set, 'DUPLICATE_EXPECTED_ID')
        expected_set.add(identity)
    found: dict[str, Row] = {}
    buckets: dict[str, list[str]] = {key: [] for key in DOMAIN}
    for row in rows:
        require(type(row) is Row, 'INVALID_ROW')
        require(row.frame == frame, 'ROW_CONTEXT_MISMATCH')
        require(type(row.identity) is str and row.identity in expected_set, 'UNEXPECTED_ID')
        require(type(row.result) is str and row.result in DOMAIN, 'INVALID_RESULT')
        require(row.identity not in found, 'DUPLICATE_RESULT')
        found[row.identity] = row
        buckets[row.result].append(row.identity)
    missing = tuple(sorted(expected_set.difference(found)))
    coverage = 'COVERED'
    if missing:
        coverage = 'INCOMPLETE'
    if not expected_set:
        coverage = 'EMPTY'
    return Findings(frame, tuple(sorted(expected_set)), tuple(found[x] for x in sorted(found)),
                    tuple(sorted(buckets[S])), tuple(sorted(buckets[B])), tuple(sorted(buckets[U])),
                    missing, coverage, bool(expected_set) and len(buckets[S]) == len(expected_set))


def validate_findings(report: Findings) -> None:
    require(type(report) is Findings, 'FINDINGS_REQUIRED')
    require(report == aggregate(report.frame, report.expected, report.rows), 'FORGED_FINDINGS_SUMMARY')


def merge(left: Findings, right: Findings) -> Findings:
    validate_findings(left)
    validate_findings(right)
    require((left.frame, left.expected) == (right.frame, right.expected), 'MERGE_CONTEXT_MISMATCH')
    return aggregate(left.frame, left.expected, left.rows + right.rows)


def sources() -> dict[str, tuple[str, str, tuple[str, ...], tuple[str, ...]]]:
    require(lines_sha(C9_HEADER + C9_ROWS) == C9_SHA, 'C9_SOURCE_IDENTITY')
    c13 = C13_HEADER + INPUTS + ('--- PREDICATE INPUT BINDINGS ---',) + INPUT_BINDINGS + ('--- UNRESOLVED INPUT QUESTIONS ---',) + INPUT_QUESTIONS
    require(lines_sha(c13) == C13_SHA, 'C13_SOURCE_IDENTITY')
    result = {}
    for row in C9_ROWS:
        fields = row.split('|')
        require(len(fields) == 4, 'C9_FIELD_COUNT')
        edge, topology, pfield, ufield = fields
        require(pfield.startswith('PREDICATES=') and ufield.startswith('UNRESOLVED='), 'C9_FIELDS')
        start, target = topology.split('>')
        pvalue = pfield.removeprefix('PREDICATES=')
        uvalue = ufield.removeprefix('UNRESOLVED=')
        pids, uids = (), ()
        if pvalue != 'NONE':
            pids = tuple(pvalue.split(','))
        if uvalue != 'NONE':
            uids = tuple(uvalue.split(','))
        require(edge not in result and len(pids) == len(set(pids)), 'C9_DUPLICATE')
        require(all(re.fullmatch(r'P(?:0[1-9]|1[0-2])', p) for p in pids), 'C9_PREDICATE_ID')
        result[edge] = start, target, pids, uids
    require(len(result) == 16 and sum(len(x[2]) for x in result.values()) == 25, 'C9_GEOMETRY')
    return result


@dataclass(frozen=True)
class GovernedRequirementSet:
    """External admitted assessment, NOT a rule-resolution or trust implementation.

    These expected IDs must come from the governing rule boundary, not result rows.
    Completeness and scope are explicit claims here; their authentication is external.
    """
    frame: Frame
    rule_basis: str | None
    established: str
    required: tuple[str, ...]


@dataclass(frozen=True)
class AttemptReview:
    frame: Frame
    source_state: str
    predicates: Findings
    requirements: Findings
    requirement_set: GovernedRequirementSet
    known_blocks: tuple[str, ...]
    unresolved_findings: tuple[str, ...]
    missing_reports: tuple[str, ...]
    positive_conditions_met: bool


def evaluate_attempt(frame: Frame, catalog: GovernedRequirementSet,
                     predicate_rows: Sequence[Row], requirement_rows: Sequence[Row],
                     topology: dict) -> AttemptReview:
    require(frame.edge in ('C01', 'C02', 'C03', 'C04', 'C05'), 'NOT_PROGRESS_EDGE')
    require(type(catalog) is GovernedRequirementSet and catalog.frame == frame, 'CATALOG_CONTEXT_MISMATCH')
    require(type(catalog.established) is str and catalog.established in DOMAIN, 'CATALOG_RESULT')
    require(type(catalog.required) is tuple, 'CATALOG_REQUIRED_LIST')
    if catalog.established in (S, B):
        require(valid_id(catalog.rule_basis), 'DETERMINATE_CATALOG_NEEDS_BASIS')
    predicates = aggregate(frame, topology[frame.edge][2], predicate_rows)
    requirements = aggregate(frame, catalog.required, requirement_rows)
    blocks = ['predicate:' + x for x in predicates.blocked] + ['requirement:' + x for x in requirements.blocked]
    unknown = ['predicate:' + x for x in predicates.unresolved] + ['requirement:' + x for x in requirements.unresolved]
    missing = ['predicate:' + x for x in predicates.missing] + ['requirement:' + x for x in requirements.missing]
    if catalog.established == B:
        blocks.append('requirement_set:governing_basis_rejected')
    if catalog.established == U:
        unknown.append('requirement_set:not_established')
    # A resolved governed empty requirement set is different from an absent catalog.
    required_satisfied = (not requirements.blocked and not requirements.unresolved and not requirements.missing)
    positive = catalog.established == S and predicates.all_reported_members_satisfied and required_satisfied
    # C03's missing guard membership is not silently completed by this repair.
    return AttemptReview(frame, topology[frame.edge][0], predicates, requirements, catalog,
                         tuple(sorted(blocks)), tuple(sorted(unknown)), tuple(sorted(missing)), positive)


def validate_attempt(attempt: AttemptReview, topology: dict) -> None:
    require(type(attempt) is AttemptReview, 'ATTEMPT_REVIEW_REQUIRED')
    replayed = evaluate_attempt(attempt.frame, attempt.requirement_set,
                                attempt.predicates.rows, attempt.requirements.rows, topology)
    require(replayed == attempt, 'FORGED_ATTEMPT_SUMMARY')


def p08_reference(catalog: GovernedRequirementSet, outcomes: Findings) -> str:
    """Resolvability only. Known failure is determinate, not successful."""
    if catalog.established != S or outcomes.unresolved or outcomes.missing:
        return U
    return S


RECORD_CHECKS = ('record.bound_scope', 'record.provenance', 'record.no_semantic_promotion', 'record.no_protected_effect')


@dataclass(frozen=True)
class ControlReview:
    frame: Frame
    target_state: str
    carried_attempt: AttemptReview
    record_checks: Findings
    witness_present: bool
    control_conditions_met: bool
    grants_protected_operation_authority: bool = False


def record_assessment(frame: Frame, attempt: AttemptReview, rows: Sequence[Row]) -> Findings:
    require(type(frame) is Frame, 'RECORD_FRAME_REQUIRED')
    require((frame.lifecycle, frame.operation, frame.policy_snapshot) ==
            (attempt.frame.lifecycle, attempt.frame.operation, attempt.frame.policy_snapshot), 'RECORD_ATTEMPT_SCOPE_MISMATCH')
    require(frame.evaluation != attempt.frame.evaluation, 'RECORD_REUSES_OPERATION_ASSESSMENT')
    return aggregate(frame, RECORD_CHECKS, rows)


def evaluate_diagnostic(frame: Frame, attempt: AttemptReview, rows: Sequence[Row], topology: dict) -> ControlReview:
    validate_attempt(attempt, topology)
    require(type(frame) is Frame, 'RECORD_FRAME_REQUIRED')
    require(frame.edge in ('C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13'), 'NOT_DIAGNOSTIC_EDGE')
    source, target = topology[frame.edge][:2]
    require(attempt.source_state == source, 'DIAGNOSTIC_SOURCE_STATE_MISMATCH')
    record = record_assessment(frame, attempt, rows)
    witness = bool(attempt.known_blocks)
    if target == 'CI6_UNRESOLVED':
        witness = bool(attempt.unresolved_findings or attempt.missing_reports)
    eligible = witness and record.all_reported_members_satisfied
    # Negative/unknown operation results are witnesses, not failures of recording permission.
    return ControlReview(frame, target, attempt, record, witness, eligible)


@dataclass(frozen=True)
class OccurrenceAssessment:
    frame: Frame
    result: str
    basis_ref: str | None


def evaluate_closure(frame: Frame, attempt: AttemptReview, rows: Sequence[Row], topology: dict,
                     prior_diagnostic: ControlReview | None = None, occurrence: OccurrenceAssessment | None = None) -> ControlReview:
    validate_attempt(attempt, topology)
    require(type(frame) is Frame, 'RECORD_FRAME_REQUIRED')
    require(frame.edge in ('C14', 'C15', 'C16'), 'NOT_CLOSURE_EDGE')
    record = record_assessment(frame, attempt, rows)
    source, target = topology[frame.edge][:2]
    witness = False
    if frame.edge == 'C14':
        require(type(occurrence) is OccurrenceAssessment, 'EXECUTION_OCCURRENCE_ASSESSMENT_REQUIRED')
        require(attempt.frame.edge == 'C05', 'EXECUTION_ATTEMPT_REQUIRED')
        require(type(occurrence.frame) is Frame, 'OCCURRENCE_FRAME_REQUIRED')
        require((occurrence.frame.lifecycle, occurrence.frame.operation, occurrence.frame.policy_snapshot, occurrence.frame.edge) ==
                (attempt.frame.lifecycle, attempt.frame.operation, attempt.frame.policy_snapshot, 'C05'), 'OCCURRENCE_CONTEXT_MISMATCH')
        require(type(occurrence.result) is str and occurrence.result in DOMAIN, 'OCCURRENCE_RESULT')
        if occurrence.result in (S, B):
            require(valid_id(occurrence.basis_ref), 'DETERMINATE_OCCURRENCE_NEEDS_BASIS')
        require(prior_diagnostic is None, 'UNEXPECTED_PRIOR_DIAGNOSTIC')
        witness = occurrence.result == S
    if frame.edge in ('C15', 'C16'):
        require(type(prior_diagnostic) is ControlReview, 'PRIOR_DIAGNOSTIC_REQUIRED')
        require(occurrence is None, 'OCCURRENCE_NOT_FAILURE_WITNESS')
        require(prior_diagnostic.carried_attempt == attempt, 'CLOSURE_ATTEMPT_MISMATCH')
        replayed = evaluate_diagnostic(prior_diagnostic.frame, attempt, prior_diagnostic.record_checks.rows, topology)
        require(replayed == prior_diagnostic, 'FORGED_DIAGNOSTIC_SUMMARY')
        require(prior_diagnostic.target_state == source, 'CLOSURE_SOURCE_STATE_MISMATCH')
        witness = prior_diagnostic.control_conditions_met
    return ControlReview(frame, target, attempt, record, witness,
                         witness and record.all_reported_members_satisfied)


class Suite:
    def __init__(self):
        self.assertions = 0
        self.transcript = hashlib.sha256()
        self.results: list[tuple[str, bool]] = []

    def check(self, value: bool, label: str) -> None:
        self.assertions += 1
        if not value:
            raise AssertionError(label)
        self.transcript.update((label + '\n').encode())

    def record(self, label: str, value: object) -> None:
        self.transcript.update(encode((label, value)) + b'\n')

    def case(self, label: str, body: Callable[[], None]) -> None:
        self.check(label not in {x[0] for x in self.results}, 'UNIQUE_CASE:' + label)
        body()
        self.results.append((label, True))


def oracle(frame: Frame, expected: tuple[str, ...], rows: tuple[Row, ...]) -> Findings:
    ids = tuple(sorted(expected))
    matched = lambda label: tuple(x for x in ids if any(r.identity == x and r.result == label for r in rows))
    s, b, u = matched(S), matched(B), matched(U)
    missing = tuple(x for x in ids if not any(r.identity == x for r in rows))
    coverage = 'COVERED'
    if missing:
        coverage = 'INCOMPLETE'
    if not ids:
        coverage = 'EMPTY'
    return Findings(frame, ids, tuple(sorted(rows, key=lambda x: x.identity)), s, b, u, missing, coverage,
                    len(ids) > 0 and len(s) == len(ids))


def make_rows(frame: Frame, ids: Sequence[str], statuses: Sequence[str]) -> tuple[Row, ...]:
    return tuple(Row(frame, identity, result) for identity, result in zip(ids, statuses) if result != MISSING)


def all_rows(frame: Frame, ids: Sequence[str]) -> tuple[Row, ...]:
    return tuple(Row(frame, identity, S) for identity in ids)


def c14_replay(inputs=INPUTS, bindings=INPUT_BINDINGS, questions=INPUT_QUESTIONS) -> tuple[tuple[str, bool], ...]:
    """Fresh execution of all 74 historical TEXT checks, with only the three known corrections.
    This does not relabel prose checks as runtime safety or adversarial-input proof.
    """
    match = lambda value, pattern: re.search(pattern, value, re.I) is not None
    ir01, ir02, ir03, ir04, ir05, ir06 = inputs
    p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12 = bindings
    bt, qt = '\n'.join(bindings), '\n'.join(questions)
    ledger = C13_HEADER + tuple(inputs) + ('--- PREDICATE INPUT BINDINGS ---',) + tuple(bindings) + ('--- UNRESOLVED INPUT QUESTIONS ---',) + tuple(questions)
    checks = [
    lines_sha(ledger) == C13_SHA, len(inputs)==6, len(bindings)==12, len(questions)==10,
    match(ir01,'supplies no semantic authority'), match(ir01,'no .*authorization'),
    match(ir01,'permission'),match(ir01,'Evidence status'),match(ir01,'canonicality'),match(ir01,'truth'),match(ir01,'predicate result'),
    match(ir02,'does not create authority'),match(ir02,'does not define the authority-resolution mechanism'),
    match(ir03,'already established as required'),match(ir03,'creates no new prerequisite'),match(ir03,'absence does not mean permission'),
    match(ir04,'already-required authorization'),match(ir04,'permission, effective capability, qualification, or canonicalization'),match(ir04,'creates none of those prerequisites'),
    match(ir05,'determinate forbidden, out-of-scope, or unsatisfied required condition'),match(ir05,'indeterminate status is not converted to BLOCKED'),
    match(ir06,'forbidden semantic elevation'),match(ir06,'does not itself assign Evidence status'),match(ir06,'authorization, canonicality, truth, success, effect, or downstream admission'),
    p01=='P01|INPUTS=IR01,IR02',p02=='P02|INPUTS=IR01,IR02',p03=='P03|INPUTS=IR01,IR02',
    p04=='P04|INPUTS=IR01,IR03,IR04',p05=='P05|INPUTS=IR01,IR03,IR04',p06=='P06|INPUTS=IR01,IR03,IR04',p07=='P07|INPUTS=IR01,IR03,IR04',
    p08=='P08|INPUTS=IR01,IR03',p09=='P09|INPUTS=IR01,IR05',p10=='P10|INPUTS=IR01,IR06',p11=='P11|INPUTS=IR01,IR06',p12=='P12|INPUTS=IR01,IR06',
    not match(p08,'IR02'),not match(p08,'IR04'),not match(p08,'IR05'),not match(p08,'IR06'),
    not match(p09,'IR02'),not match(p09,'IR03'),not match(p09,'IR04'),not match(p09,'IR06'),
    not match(p10,'IR02|IR03|IR04|IR05'),not match(p11,'IR02|IR03|IR04|IR05'),not match(p12,'IR02|IR03|IR04|IR05'),
    not match(p01,'IR03|IR04|IR05|IR06'),not match(p02,'IR03|IR04|IR05|IR06'),not match(p03,'IR03|IR04|IR05|IR06'),
    not match(bt,'all context'),not match(bt,'global context'),not match(bt,'all prerequisites'),not match(bt,'entire state'),
    not match(bt,r'\bAND\b'),not match(bt,r'\bOR\b'),not match(bt,'precedence|priority'),not match(bt,'evaluation order'),not match(bt,'short.?circuit'),not match(bt,'edge allowed|edge denied|edge outcome'),
    questions[1]=='IQ02|The authoritative source and resolution mechanism for IR02 remains unresolved.',
    match(qt,'IQ03.*prerequisite.*unresolved'),match(qt,'IQ04.*provenance.*unresolved'),match(qt,'IQ05.*provenance.*unresolved'),match(qt,'IQ06.*provenance.*unresolved'),match(qt,'IQ09.*Composition operator.*unresolved'),match(qt,'IQ10.*U01-U08 remain unresolved'),
    not match(bt,'artifact|receipt'),not match(bt,'schema|serialization'),not match(bt,'persist|cache|store'),
    ir05.endswith('indeterminate status is not converted to BLOCKED.'),
    ir03.endswith('absence does not mean permission.'),
    not match(ir06,'assigns Evidence'),not match(ir02,r'creates authority\.$'),
    ]
    require(len(checks) == 74, 'C14_TEST_COLLECTION')
    return tuple((f'C14.A{i:02d}', bool(value)) for i,value in enumerate(checks,1))


def model_suite() -> tuple[dict, dict]:
    topology = sources()
    suite = Suite()
    vector_count = 0
    for edge, (_, _, ids, _) in topology.items():
        frame = Frame('fixture', 'aggregate', 'operation', 'policy.v1', edge)
        for status in itertools.product(DOMAIN + (MISSING,), repeat=len(ids)):
            rows = make_rows(frame, ids, status)
            actual = aggregate(frame, ids, rows)
            expected = oracle(frame, ids, rows)
            suite.check(actual == expected, 'AGGREGATE_ORACLE')
            suite.check(aggregate(frame, tuple(reversed(ids)), tuple(reversed(rows))) == actual, 'ORDER_INDEPENDENCE')
            parts = tuple(aggregate(frame, ids, rows[i::3]) for i in range(3))
            suite.check(merge(merge(parts[0],parts[1]),parts[2]) == actual, 'DISJOINT_MERGE')
            suite.check(merge(parts[0],merge(parts[1],parts[2])) == actual, 'ASSOCIATIVE_MERGE')
            suite.check(merge(parts[0],parts[1]) == merge(parts[1],parts[0]), 'COMMUTATIVE_MERGE')
            suite.record('AGGREGATE',asdict(actual))
            vector_count += 1
    suite.check(vector_count == sum(4**len(x[2]) for x in topology.values()), 'AGGREGATE_EXHAUSTION_COUNT')

    frame = Frame('fixture','attempt','operation','policy.v1','C05')
    ids = topology['C05'][2]
    set_states = DOMAIN
    operation_cases = 0
    for p_states in itertools.product(DOMAIN + (MISSING,), repeat=len(ids)):
        p_rows = make_rows(frame, ids, p_states)
        for req_state, set_state in itertools.product(DOMAIN + (MISSING,), set_states):
            catalog = GovernedRequirementSet(frame, 'policy.rule.authorization', set_state, ('authorization',))
            q_rows = make_rows(frame, ('authorization',), (req_state,))
            actual = evaluate_attempt(frame,catalog,p_rows,q_rows,topology)
            expected = all(x == S for x in p_states) and req_state == S and set_state == S
            suite.check(actual.positive_conditions_met == expected,'C05_ACTUAL_SATISFACTION_ORACLE')
            suite.check(actual.requirements == oracle(frame,('authorization',),q_rows),'REQUIREMENT_REPORT_PRESERVED')
            suite.record('C05', (p_states, req_state, set_state, actual.positive_conditions_met,
                                  actual.known_blocks, actual.unresolved_findings, actual.missing_reports))
            operation_cases += 1
    suite.check(operation_cases == 4**6*4*3,'C05_EXHAUSTION_COUNT')

    catalog = GovernedRequirementSet(frame,'policy.rule.authorization',S,('authorization',))
    p_rows = all_rows(frame, ids)
    missing_auth = evaluate_attempt(frame,catalog,p_rows,(Row(frame,'authorization',B),),topology)
    good = evaluate_attempt(frame,catalog,p_rows,(Row(frame,'authorization',S),),topology)
    pending = evaluate_attempt(frame,catalog,p_rows,(Row(frame,'authorization',U),),topology)
    mixed_catalog = replace(catalog,required=('authorization','capability'))
    mixed = evaluate_attempt(frame,mixed_catalog,p_rows,(Row(frame,'authorization',B),Row(frame,'capability',U)),topology)
    diagnostics: dict[str, object] = {}

    def counterexample():
        suite.check(missing_auth.predicates.all_reported_members_satisfied,'LEGACY_ALL_SAT_COUNTEREXAMPLE')
        suite.check(p08_reference(catalog, missing_auth.requirements)==S,'P08_KNOWN_ABSENCE_REMAINS_RESOLVABLE')
        suite.check(not missing_auth.positive_conditions_met,'MISSING_AUTHORIZATION_BYPASS_CLOSED')
    suite.case('R01_ALL_PREDICATES_SAT_WITH_REQUIRED_AUTH_ABSENT_REJECTED',counterexample)
    suite.case('R02_ALL_ACTUAL_REQUIRED_CONDITIONS_SAT_ACCEPTED_IN_MODEL',lambda:suite.check(good.positive_conditions_met,'GOOD_C05'))
    suite.case('R03_MIXED_BLOCK_AND_UNKNOWN_RETAINED',lambda:suite.check(bool(mixed.known_blocks) and bool(mixed.unresolved_findings) and not mixed.positive_conditions_met,'MIXED_FINDINGS'))
    suite.case('R04_ABSENT_RESULT_NOT_FABRICATED_UNKNOWN',lambda:suite.check(bool(evaluate_attempt(frame,catalog,p_rows,(),topology).missing_reports),'MISSING_REPORT_RETAINED'))
    no_extra = GovernedRequirementSet(frame,'policy.rule.local-operation',S,())
    suite.case('R05_EXPLICIT_GOVERNED_NO_EXTRA_REQUIREMENT_NOT_GLOBAL_AUTH_MANDATE',lambda:suite.check(evaluate_attempt(frame,no_extra,p_rows,(),topology).positive_conditions_met,'NO_GLOBAL_AUTH_MANDATE'))
    suite.case('R06_UNRESOLVED_REQUIREMENT_SET_CANNOT_USE_EMPTY_SUCCESS',lambda:suite.check(not evaluate_attempt(frame,replace(no_extra,established=U),p_rows,(),topology).positive_conditions_met,'UNKNOWN_CATALOG'))
    suite.case('R09_NEW_GOVERNED_REQUIREMENT_CANNOT_BE_OMITTED_FROM_RESULTS',lambda:suite.check(not evaluate_attempt(frame,replace(catalog,required=('authorization','permission')),p_rows,(Row(frame,'authorization',S),),topology).positive_conditions_met,'EXPANDED_CATALOG_REQUIRES_NEW_RESULT'))

    diag_checks = 0
    # Exercise each diagnostic edge with an assessed operation at its matching source state.
    progress_by_state = {'CI0_PRESENTED':'C01','CI1_OBSERVED':'C02','CI2_PROPOSAL_AVAILABLE':'C04','CI3_ACTION_GATED':'C05'}
    for edge in ('C06','C07','C08','C09','C10','C11','C12','C13'):
        progress = progress_by_state[topology[edge][0]]
        f = replace(frame, edge=progress, evaluation='attempt.'+edge)
        cat = GovernedRequirementSet(f,'policy.rule.required',S,('condition',))
        label = B
        if topology[edge][1] == 'CI6_UNRESOLVED':
            label = U
        attempt = evaluate_attempt(f,cat,all_rows(f,topology[progress][2]),(Row(f,'condition',label),),topology)
        record_frame = replace(f,edge=edge,evaluation='record.'+edge)
        control = evaluate_diagnostic(record_frame,attempt,all_rows(record_frame,RECORD_CHECKS),topology)
        suite.check(control.control_conditions_met and not attempt.positive_conditions_met,'DIAGNOSTIC_NEGATIVE_RESULT_IS_WITNESS:'+edge)
        suite.check(control.carried_attempt == attempt and not control.grants_protected_operation_authority,'DIAGNOSTIC_NO_RETROAUTH:'+edge)
        for bad in (B,U,MISSING):
            rows = make_rows(record_frame, RECORD_CHECKS, (bad,S,S,S))
            suite.check(not evaluate_diagnostic(record_frame,attempt,rows,topology).control_conditions_met,'RECORD_OWN_GUARD_REQUIRED:'+edge+bad)
        diag_checks += 1
    suite.check(diag_checks==8,'ALL_DIAGNOSTIC_EDGES')

    block_frame = replace(frame,edge='C09',evaluation='record.block')
    unknown_frame = replace(frame,edge='C13',evaluation='record.unknown')
    recorded_block = evaluate_diagnostic(block_frame,mixed,all_rows(block_frame,RECORD_CHECKS),topology)
    recorded_unknown = evaluate_diagnostic(unknown_frame,mixed,all_rows(unknown_frame,RECORD_CHECKS),topology)
    suite.case('R07_MIXED_FINDINGS_DO_NOT_IMPLICITLY_SELECT_A_ROUTE',lambda:suite.check(recorded_block.control_conditions_met and recorded_unknown.control_conditions_met,'BOTH_ROUTE_WITNESSES'))
    closures = []
    for edge, prior in (('C15',recorded_block),('C16',recorded_unknown)):
        cf = replace(frame,edge=edge,evaluation='record.close.'+edge)
        closed = evaluate_closure(cf,mixed,all_rows(cf,RECORD_CHECKS),topology,prior_diagnostic=prior)
        suite.check(closed.control_conditions_met,'CLOSURE_MAY_PRESERVE_FAILURE:'+edge)
        suite.check(closed.carried_attempt == mixed and not closed.carried_attempt.positive_conditions_met,'CLOSURE_DOES_NOT_FIX_ORIGINAL_OPERATION:'+edge)
        suite.check(not closed.grants_protected_operation_authority,'CLOSURE_NO_RETROAUTH:'+edge)
        closures.append(closed)
    cf = replace(frame,edge='C14',evaluation='record.close.execution')
    for occurred in DOMAIN:
        closed = evaluate_closure(cf,good,all_rows(cf,RECORD_CHECKS),topology,occurrence=OccurrenceAssessment(replace(frame,evaluation='occurrence'),occurred,'fixture.occurrence'))
        suite.check(closed.control_conditions_met == (occurred==S),'C14_REQUIRES_OCCURRENCE_NOT_GATE_SUCCESS')
    suite.case('R08_UNRESOLVED_OPERATION_CAN_CLOSE_WITH_UNRESOLVED_FINDINGS_INTACT',lambda:suite.check(closures[1].carried_attempt.unresolved_findings == mixed.unresolved_findings,'UNKNOWN_NOT_CLEARED'))

    # Report-order invariance, all permutations of a six-result mixed fixture.
    mixed_rows = make_rows(frame, ids, (S,B,U,S,B,U))
    reference = aggregate(frame,ids,mixed_rows)
    permutations = 0
    for perm in itertools.permutations(mixed_rows):
        suite.check(aggregate(frame,ids,perm)==reference,'SIX_RESULT_PERMUTATION')
        permutations += 1
    suite.check(permutations==720,'PERMUTATION_COUNT')

    rejects = (
      ('UNKNOWN_EDGE',lambda:aggregate(replace(frame,edge='C99'),ids,())),
      ('UNKNOWN_RESULT',lambda:aggregate(frame,ids,(Row(frame,'P03','TRUE'),))),
      ('LOWERCASE_RESULT',lambda:aggregate(frame,ids,(Row(frame,'P03','satisfied'),))),
      ('NULL_RESULT',lambda:aggregate(frame,ids,(Row(frame,'P03',None),))),
      ('UNEXPECTED_ID',lambda:aggregate(frame,ids,(Row(frame,'P99',S),))),
      ('DUPLICATE_SAME_RESULT',lambda:aggregate(frame,ids,(Row(frame,'P03',S),Row(frame,'P03',S)))),
      ('DUPLICATE_CONFLICTING_RESULT',lambda:aggregate(frame,ids,(Row(frame,'P03',B),Row(frame,'P03',U)))),
      ('DUPLICATE_EXPECTED_ID',lambda:aggregate(frame,('P03','P03'),())),
      ('SCALAR_EXPECTED',lambda:aggregate(frame,'P03',())),
      ('SCALAR_ROWS',lambda:aggregate(frame,ids,'P03')),
      ('MALFORMED_ROW',lambda:aggregate(frame,ids,('P03=SATISFIED',))),
      ('FOREIGN_EVALUATION',lambda:aggregate(frame,ids,(Row(replace(frame,evaluation='other'),'P03',S),))),
      ('FOREIGN_POLICY_SNAPSHOT',lambda:aggregate(frame,ids,(Row(replace(frame,policy_snapshot='policy.v0'),'P03',S),))),
      ('FOREIGN_OPERATION',lambda:aggregate(frame,ids,(Row(replace(frame,operation='other'),'P03',S),))),
      ('FOREIGN_EDGE',lambda:aggregate(frame,ids,(Row(replace(frame,edge='C04'),'P03',S),))),
      ('FOREIGN_CATALOG',lambda:evaluate_attempt(frame,replace(catalog,frame=replace(frame,policy_snapshot='policy.v0')),p_rows,(),topology)),
      ('NO_GOVERNED_BASIS',lambda:evaluate_attempt(frame,replace(catalog,rule_basis=None),p_rows,(),topology)),
      ('OMITTED_EXPECTATION_WRONG_ID',lambda:evaluate_attempt(frame,catalog,p_rows,(Row(frame,'different_requirement',S),),topology)),
      ('RECORD_REUSES_OPERATION_ASSESSMENT',lambda:evaluate_diagnostic(replace(block_frame,evaluation=frame.evaluation),mixed,(),topology)),
      ('DIAGNOSTIC_SOURCE_STATE_MISMATCH',lambda:evaluate_diagnostic(replace(block_frame,edge='C06'),mixed,(),topology)),
      ('FORGED_OPERATION_POSITIVE_FLAG',lambda:evaluate_diagnostic(block_frame,replace(mixed,positive_conditions_met=True),(),topology)),
      ('FORGED_OPERATION_BLOCKING_FINDING',lambda:evaluate_diagnostic(block_frame,replace(good,known_blocks=('invented',)),(),topology)),
      ('FORGED_AGGREGATE_SUMMARY',lambda:merge(replace(reference,blocked=()),aggregate(frame,ids,()))),
      ('FORGED_DIAGNOSTIC_POSITIVE_FLAG',lambda:evaluate_closure(replace(cf,edge='C15'),mixed,(),topology,prior_diagnostic=replace(recorded_block,witness_present=False))),
      ('FOREIGN_OCCURRENCE',lambda:evaluate_closure(cf,good,(),topology,occurrence=OccurrenceAssessment(replace(frame,operation='other'),S,'fixture.other'))),
      ('OCCURRENCE_WITHOUT_BASIS',lambda:evaluate_closure(cf,good,(),topology,occurrence=OccurrenceAssessment(frame,S,None))),
      ('CLOSURE_WITHOUT_FAILURE_WITNESS',lambda:evaluate_closure(replace(cf,edge='C16'),mixed,(),topology)),
      ('CLOSURE_WRONG_DIAGNOSTIC_STATE',lambda:evaluate_closure(replace(cf,edge='C16'),mixed,(),topology,prior_diagnostic=recorded_block)),
    )
    rejected = 0
    for name, call in rejects:
        caught = False
        try:
            call()
        except Rejected as exc:
            caught = True
            suite.record('REJECTION',(name,str(exc)))
        suite.check(caught,'INVALID_REJECTED:'+name)
        rejected += int(caught)

    # Fresh, complete C14 text replay. No prior pass count is imported.
    replay = c14_replay()
    for name, value in replay:
        suite.check(value,'FRESH_TEXT_CHECK:'+name)
        suite.record('FRESH_TEXT_RESULT',(name,value))
    suite.check(len(replay)==74,'C14_ALL_CHECKS_REEXECUTED')
    text_controls = 0
    for index, old, new, test_index in (
        (4,'is not converted to BLOCKED','is converted to BLOCKED',70),
        (2,'absence does not mean permission','absence means permission',71),
        (1,'does not create authority','creates authority',11),
    ):
        changed = list(INPUTS)
        require(old in changed[index],'NEGATIVE_CONTROL_PREIMAGE')
        changed[index] = changed[index].replace(old,new,1)
        suite.check(not c14_replay(tuple(changed))[test_index][1],'NEGATION_MUTATION_REJECTED')
        text_controls += 1
    changed_q = list(INPUT_QUESTIONS)
    changed_q[1] = changed_q[1].replace('remains unresolved','is resolved')
    suite.check(not c14_replay(questions=tuple(changed_q))[60][1],'RESOLUTION_PROMOTION_MUTATION_REJECTED')
    text_controls += 1

    # Actual faulty variants evaluated against the regression oracles.
    mutant_results = []
    bad_unknown_wins = replace(reference,blocked=())
    mutant_results.append(('UNKNOWN_ERASES_BLOCK',bad_unknown_wins != oracle(frame,ids,mixed_rows)))
    bad_block_wins = replace(reference,unresolved=())
    mutant_results.append(('BLOCK_ERASES_UNKNOWN',bad_block_wins != oracle(frame,ids,mixed_rows)))
    empty = aggregate(replace(frame,edge='C03'),(),())
    mutant_results.append(('EMPTY_SET_ASSUMED_SATISFIED',replace(empty,all_reported_members_satisfied=True) != empty))
    partial = aggregate(frame,ids,(Row(frame,'P03',S),))
    mutant_results.append(('MISSING_ROWS_DROPPED',replace(partial,missing=(),coverage='COVERED') != oracle(frame,ids,partial.rows)))
    legacy_all_sat = missing_auth.predicates.all_reported_members_satisfied
    mutant_results.append(('PREDICATE_ALL_SAT_AS_COMPLETE_EXECUTION_GUARD',legacy_all_sat != missing_auth.positive_conditions_met))
    legacy_known_is_good = not missing_auth.requirements.unresolved and not missing_auth.requirements.missing
    mutant_results.append(('RESOLVABLE_REQUIREMENTS_AS_SATISFIED',legacy_known_is_good != missing_auth.positive_conditions_met))
    unknown_catalog_attempt = evaluate_attempt(frame,replace(no_extra,established=U),p_rows,(),topology)
    mutant_results.append(('UNRESOLVED_EMPTY_CATALOG_ACCEPTED',True != unknown_catalog_attempt.positive_conditions_met))
    mutant_results.append(('OPERATION_MUST_SUCCEED_BEFORE_RECORDING_BLOCK',mixed.positive_conditions_met != recorded_block.control_conditions_met))
    mutant_results.append(('OPERATION_MUST_SUCCEED_BEFORE_CLOSING_UNKNOWN',mixed.positive_conditions_met != closures[1].control_conditions_met))
    no_safe_record = evaluate_diagnostic(block_frame,mixed,make_rows(block_frame,RECORD_CHECKS,(B,S,S,S)),topology)
    mutant_results.append(('DIAGNOSTIC_WITNESS_BYPASSES_OWN_RECORD_GUARD',bool(mixed.known_blocks) != no_safe_record.control_conditions_met))
    false_occurrence = evaluate_closure(cf,good,all_rows(cf,RECORD_CHECKS),topology,occurrence=OccurrenceAssessment(replace(frame,evaluation='occurrence'),U,None))
    mutant_results.append(('GUARD_SUCCESS_TREATED_AS_EXECUTION_OCCURRENCE',good.positive_conditions_met != false_occurrence.control_conditions_met))
    mutant_results.append(('CLOSURE_ERASES_UNKNOWN_FINDINGS',replace(mixed,unresolved_findings=()) != closures[1].carried_attempt))
    for label,detected in mutant_results:
        suite.check(detected,'FAULTY_VARIANT_DETECTED:'+label)
        suite.record('FAULTY_VARIANT',(label,detected))

    diagnostics.update({
      'legacy_all_predicates_satisfied': legacy_all_sat,
      'p08_known_absent_authorization': p08_reference(catalog,missing_auth.requirements),
      'repaired_c05_conditions_met': missing_auth.positive_conditions_met,
      'required_authorization_outcome': missing_auth.requirements.blocked,
      'mixed_known_blocks': mixed.known_blocks,
      'mixed_unresolved_findings': mixed.unresolved_findings,
      'record_block_conditions_met': recorded_block.control_conditions_met,
      'record_unknown_conditions_met': recorded_unknown.control_conditions_met,
      'close_unknown_conditions_met': closures[1].control_conditions_met,
      'original_attempt_still_not_eligible': not closures[1].carried_attempt.positive_conditions_met,
      'diagnostic_authority_grant_created': recorded_block.grants_protected_operation_authority,
    })
    metrics = {
      'aggregate_vectors_executed': vector_count,
      'c05_acceptance_vectors_executed': operation_cases,
      'six_result_permutations_executed': permutations,
      'diagnostic_edge_families_checked': diag_checks,
      'invalid_input_cases_executed': len(rejects), 'invalid_inputs_rejected': rejected,
      'c14_text_checks_executed_fresh': len(replay), 'c14_text_checks_passed_fresh': sum(v for _,v in replay),
      'c14_prior_passes_carried': 0, 'text_negative_controls_executed': text_controls,
      'faulty_reference_variants_exercised': len(mutant_results), 'faulty_reference_variants_detected': sum(v for _,v in mutant_results),
      'named_regression_cases_executed': len(suite.results), 'assertions_executed': suite.assertions,
      'qualification_transcript_sha256': suite.transcript.hexdigest(),
    }
    return metrics,diagnostics


def native_powershell_check() -> dict:
    """Actual scalar/array regression in the user's PowerShell, not an emulated count."""
    executable = shutil.which('pwsh')
    require(executable is not None,'PWSH_NOT_FOUND_FOR_NATIVE_REGRESSION')
    ps_rows = ','.join("'"+row+"'" for row in C9_ROWS)
    code = (
      "$ErrorActionPreference='Stop'; $rows=@("+ps_rows+"); "
      "$sample=$rows[0].Split('|'); $old=($sample | Where-Object { $_ -like 'PREDICATES=*' })[0]; "
      "$safe=@($sample | Where-Object { $_ -like 'PREDICATES=*' }); "
      "$pairs=[System.Collections.Generic.List[string]]::new(); "
      "foreach($row in $rows) { $parts=$row.Split('|'); $fields=@($parts | Where-Object { $_ -like 'PREDICATES=*' }); "
      "if($fields.Count -ne 1) { throw 'PREDICATE_FIELD_CARDINALITY' }; "
      "$value=$fields[0].Substring(11); if($value -ceq 'NONE') { continue }; "
      "foreach($id in $value.Split(',')) { $pairs.Add($parts[0]+'>'+$id) } }; "
      "$result=[ordered]@{old_scalar=[string]$old;old_type=$old.GetType().FullName;array_safe_field=$safe[0];bindings=@($pairs.ToArray())}; "
      "ConvertTo-Json -InputObject $result -Depth 4 -Compress"
    )
    run = subprocess.run([executable,'-NoLogo','-NoProfile','-NonInteractive','-Command',code],
                         capture_output=True,check=False,timeout=30)
    require(run.returncode==0,'NATIVE_POWERSHELL_FAILED:'+run.stderr.decode('utf-8','replace'))
    data = json.loads(run.stdout.decode('utf-8-sig'))
    expected = []
    for edge,(_,_,ids,_) in sources().items():
        expected.extend(edge+'>'+identity for identity in ids)
    require(data['old_scalar']=='P' and data['old_type']=='System.Char','SCALAR_BUG_NOT_REPRODUCED')
    require(data['array_safe_field']=='PREDICATES=P01,P11','ARRAY_SAFE_FIELD_FAILURE')
    require(data['bindings']==expected and len(data['bindings'])==25,'NATIVE_DERIVATION_FAILURE')
    require(not any(row.startswith('C03>') for row in data['bindings']),'NATIVE_NONE_NOT_EMPTY')
    return {'old_scalar_bug_reproduced':True,'native_bindings_derived':len(data['bindings']),
            'native_c03_binding_count':0,'native_regression':'PASS'}


FORBIDDEN_GIT_ENV=('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_COMMON_DIR','GIT_NAMESPACE')


def git_read(repo:Path,args:Sequence[str])->bytes:
    require(not any(os.environ.get(key) for key in FORBIDDEN_GIT_ENV),'GIT_CONTEXT_OVERRIDE')
    env=os.environ.copy(); env['GIT_OPTIONAL_LOCKS']='0'
    result=subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false','-C',str(repo),*args],
                          capture_output=True,check=False,timeout=30,env=env)
    require(result.returncode==0,'GIT_READ_FAILED:'+result.stderr.decode('utf-8','replace').strip())
    return result.stdout


def snapshot(repo:Path,head=HEAD,tree=TREE)->dict:
    require(repo.is_dir(),'REPOSITORY_NOT_FOUND')
    actual_head=git_read(repo,('rev-parse','HEAD')).decode('ascii').strip()
    actual_tree=git_read(repo,('rev-parse','HEAD^{tree}')).decode('ascii').strip()
    require(actual_head==head and actual_tree==tree,'REPOSITORY_IDENTITY_DRIFT:'+actual_head)
    status=git_read(repo,('status','--porcelain=v1','--untracked-files=all'))
    require(not status,'REPOSITORY_NOT_CLEAN:'+status.decode('utf-8','replace').strip())
    index=Path(git_read(repo,('rev-parse','--git-path','index')).decode('utf-8').strip())
    if not index.is_absolute():
        index=repo/index
    require(index.is_file(),'INDEX_UNAVAILABLE')
    return {'head':actual_head,'tree':actual_tree,'index_sha256':sha(index.read_bytes()),'worktree':'CLEAN'}


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--model-only',action='store_true')
    mode.add_argument('--repo',type=Path)
    args=parser.parse_args()
    output=['=== ANARCHI BRAIN :: SW0-010 M01 REPAIR R1 :: FRESH REFERENCE QUALIFICATION ===',
            'STATUS=REPAIR_CANDIDATE_NOT_FROZEN','RUNNER_SHA256='+sha(Path(__file__).read_bytes()),
            'EXPECTED_HEAD='+HEAD,'C9_SOURCE_SHA256='+C9_SHA,'C13_SOURCE_SHA256='+C13_SHA,
            'FAILED_C14_HISTORICAL_REFERENCE='+FAILED_C14_SHA]
    local=False
    try:
        before=None
        if args.repo is not None:
            before=snapshot(args.repo)
            output.extend(('HEAD_BEFORE='+before['head'],'INDEX_SHA256_BEFORE='+before['index_sha256'],'WORKTREE_CLEAN_BEFORE=True'))
        metrics,examples=model_suite()
        output.extend(('C9_SOURCE_RECONSTRUCTION_EXACT=True','C13_SOURCE_RECONSTRUCTION_EXACT=True','MODEL_QUALIFICATION=PASS'))
        output.append('--- EXECUTED CHECKS ---')
        output.extend(key.upper()+'='+str(value) for key,value in metrics.items())
        output.append('--- DEFECT REGRESSIONS ---')
        output.extend(key.upper()+'='+encode(value).decode('ascii') for key,value in examples.items())
        if args.repo is not None:
            native=native_powershell_check()
            output.extend(key.upper()+'='+str(value) for key,value in native.items())
            after=snapshot(args.repo)
            require(before==after,'REPOSITORY_OBSERVED_SNAPSHOT_CHANGED')
            local=True
            output.extend(('HEAD_AFTER='+after['head'],'INDEX_SHA256_AFTER='+after['index_sha256'],
                           'HEAD_TREE_INDEX_UNCHANGED=True','WORKTREE_CLEAN_AFTER=True'))
        if args.model_only:
            output.extend(('NATIVE_POWERSHELL_REGRESSION=NOT_RUN_MODEL_ONLY','LOCAL_REPOSITORY_CHECK=NOT_RUN_MODEL_ONLY'))
        output.extend(('--- CLAIM BOUNDARY ---','HISTORICAL_CANDIDATES_REWRITTEN=False','EARLIER_PASS_COUNTS_IMPORTED=0',
                       'RECORDING_FAILURE_DOES_NOT_REQUIRE_OPERATION_SUCCESS=True',
                       'REQUIRED_CONDITION_SATISFACTION_SEPARATE_FROM_RESOLVABILITY=True',
                       'MIXED_DIAGNOSTIC_ROUTE_ARBITRATION_IMPLEMENTED=False',
                       'C03_GATE_ENTRY_ACCEPTANCE_COMPLETED=False',
                       'UPSTREAM_GOVERNANCE_AUTHENTICATION_IMPLEMENTED=False',
                       'POLICY_RESOLVER_IMPLEMENTED=False','LIVE_PROVENANCE_OR_FRESHNESS_VERIFICATION_IMPLEMENTED=False',
                       'PROTECTED_OPERATION_EXECUTED=False','AUTHORITY_GRANT_CREATED=False','REPOSITORY_WRITE_COMMANDS_EXECUTED=False',
                       'LOCAL_QUALIFICATION_COMPLETE='+str(local),'M01_FREEZE_READY=False','RESULT=PASS'))
        print('\n'.join(output)); return 0
    except Exception as exc:
        output.extend(('LOCAL_QUALIFICATION_COMPLETE='+str(local),'M01_FREEZE_READY=False','RESULT=FAIL',
                       'FAILURE='+type(exc).__name__+':'+str(exc)))
        print('\n'.join(output)); return 1


if __name__=='__main__':
    raise SystemExit(main())
