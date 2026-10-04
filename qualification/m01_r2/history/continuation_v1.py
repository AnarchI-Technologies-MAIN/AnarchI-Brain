"""Unfrozen C03 entry and diagnostic selection reference candidate; no effects."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import itertools
from dataclasses import dataclass, replace
from pathlib import Path

PIN = 'cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c'
CHECKS = ('entry.source_observed', 'entry.bound_scope', 'entry.applicable_gate',
          'entry.no_semantic_promotion', 'entry.no_protected_effect')

@dataclass(frozen=True)
class EntryAssessment:
    frame: object
    basis: str
    rows: tuple

def entry_conditions(r, attempt, assessment):
    r.validate_attempt(attempt, r.sources())
    r.require(attempt.frame.edge == 'C03', 'ENTRY_REQUIRES_C03')
    r.require(type(assessment) is EntryAssessment, 'ENTRY_ASSESSMENT_REQUIRED')
    f, a = assessment.frame, attempt.frame
    r.require(type(f) is r.Frame, 'ENTRY_FRAME_REQUIRED')
    r.require((f.lifecycle, f.operation, f.policy_snapshot, f.edge) ==
              (a.lifecycle, a.operation, a.policy_snapshot, a.edge), 'ENTRY_SCOPE_MISMATCH')
    r.require(f.evaluation != a.evaluation, 'ENTRY_EVALUATION_NOT_DISTINCT')
    r.require(r.valid_id(assessment.basis), 'ENTRY_BASIS_REQUIRED')
    report = r.aggregate(f, CHECKS, assessment.rows)
    req = attempt.requirements
    return (report.all_reported_members_satisfied
            and attempt.requirement_set.established == r.S
            and not req.blocked and not req.unresolved and not req.missing)

def selection_report(r, attempt):
    r.validate_attempt(attempt, r.sources())
    b = bool(attempt.known_blocks)
    u = bool(attempt.unresolved_findings or attempt.missing_reports)
    labels = {(False, False): 'NO_DIAGNOSTIC_WITNESS',
              (True, False): 'BLOCKED_WITNESS_ONLY',
              (False, True): 'UNRESOLVED_WITNESS_ONLY',
              (True, True): 'DECISION_REQUIRED'}
    return labels[b, u], attempt.known_blocks, attempt.unresolved_findings, attempt.missing_reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    assert hashlib.sha256(args.runner.read_bytes()).hexdigest() == PIN, 'RUNNER_HASH'
    spec = importlib.util.spec_from_file_location('m01_r1', args.runner)
    r = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = r
    spec.loader.exec_module(r)
    before = r.snapshot(args.repo)
    count = 0
    rejected = 0
    def check(value):
        nonlocal count
        assert value
        count += 1
    def reject(fn):
        nonlocal rejected
        try:
            fn()
        except r.Rejected:
            rejected += 1
            return
        raise AssertionError('INVALID_INPUT_ACCEPTED')
    f = r.Frame('lifecycle', 'attempt', 'operation', 'policy', 'C03')
    ef = replace(f, evaluation='entry')
    catalog = r.GovernedRequirementSet(f, 'basis', r.S, ('entry_permission',))
    def attempt(status):
        rows = () if status == r.MISSING else (r.Row(f, 'entry_permission', status),)
        return r.evaluate_attempt(f, catalog, (), rows, r.sources())
    a = attempt(r.S)
    rows = tuple(r.Row(ef, key, r.S) for key in CHECKS)
    good = EntryAssessment(ef, 'entry_basis', rows)
    check(entry_conditions(r, a, good))
    check(not a.positive_conditions_met)
    vectors = 0
    for statuses in itertools.product((*r.DOMAIN, r.MISSING), repeat=5):
        erows = tuple(r.Row(ef, key, status) for key, status in zip(CHECKS, statuses) if status != r.MISSING)
        for requirement in (*r.DOMAIN, r.MISSING):
            actual = entry_conditions(r, attempt(requirement), EntryAssessment(ef, 'entry_basis', erows))
            check(actual == (all(x == r.S for x in statuses) and requirement == r.S))
            vectors += 1
    for established in (r.B, r.U):
        bad = r.evaluate_attempt(f, replace(catalog, established=established), (), (r.Row(f, 'entry_permission', r.S),), r.sources())
        check(not entry_conditions(r, bad, good))
    empty = r.evaluate_attempt(f, replace(catalog, required=()), (), (), r.sources())
    check(entry_conditions(r, empty, good))
    for key in ('lifecycle', 'operation', 'policy_snapshot', 'edge', 'evaluation'):
        value = 'other'
        if key == 'edge':
            value = 'C04'
        if key == 'evaluation':
            value = f.evaluation
        reject(lambda key=key, value=value: entry_conditions(r, a, replace(good, frame=replace(ef, **{key: value}))))
    reject(lambda: entry_conditions(r, a, replace(good, basis='')))
    reject(lambda: entry_conditions(r, a, replace(good, rows=rows + (rows[0],))))
    reject(lambda: entry_conditions(r, a, replace(good, rows=(r.Row(ef, 'invented', r.S),))))
    reject(lambda: entry_conditions(r, replace(a, positive_conditions_met=True), good))
    route_vectors = 0
    for statuses in itertools.product((*r.DOMAIN, r.MISSING), repeat=2):
        ids = ('authorization', 'capability')
        cat = replace(catalog, required=ids)
        rr = tuple(r.Row(f, key, status) for key, status in zip(ids, statuses) if status != r.MISSING)
        review = r.evaluate_attempt(f, cat, (), rr, r.sources())
        selected = selection_report(r, review)
        b = r.B in statuses
        u = r.U in statuses or r.MISSING in statuses
        expected = 'NO_DIAGNOSTIC_WITNESS'
        if b: expected = 'BLOCKED_WITNESS_ONLY'
        if u: expected = 'UNRESOLVED_WITNESS_ONLY'
        if b and u: expected = 'DECISION_REQUIRED'
        check(selected[0] == expected)
        check(selected[1:] == (review.known_blocks, review.unresolved_findings, review.missing_reports))
        route_vectors += 1
    reject(lambda: selection_report(r, replace(a, known_blocks=('invented',))))
    check(before == r.snapshot(args.repo))
    print('CANDIDATE_STATUS=UNFROZEN\nC03_ENTRY_VECTORS=' + str(vectors))
    print('DIAGNOSTIC_SELECTION_VECTORS=' + str(route_vectors))
    print('INVALID_INPUTS_REJECTED=' + str(rejected))
    print('ASSERTIONS=' + str(count))
    print('HEAD_TREE_INDEX_UNCHANGED=True\nWORKTREE_CLEAN_AFTER=True')
    print('MIXED_ROUTE_POLICY_COMPLETED=False\nGOVERNANCE_AUTHENTICATION_IMPLEMENTED=False')
    print('PROTECTED_EFFECT_EXECUTED=False\nM01_FREEZE_READY=False\nRESULT=PASS')

if __name__ == '__main__':
    main()
