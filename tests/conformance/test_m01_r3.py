"""Integrated counterexamples. Fixture admission is not authentication."""
import sys
sys.dont_write_bytecode = True
import copy
from dataclasses import asdict, replace
import hashlib
import itertools
import json
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[2]
from qualification.m01_r3 import model as m
from schemas.conformance import boundary_r3 as b

class FixtureVerifier:
    """Exact admitted-fixture allowlist; no issuer or authority authentication."""
    def __init__(self):
        self.allowed = set()
    def register(self, context, role, payload):
        self.allowed.add((context, role, m.report_digest(payload)))
    def verify(self, context, role, digest):
        return m.S if (context, role, digest) in self.allowed else m.U

def context(edge='C03', evaluation='attempt'):
    return m.Context(m.Frame('lifecycle', evaluation, 'operation', 'policy.1', edge), 'subject.1', 'epoch.1')

def rows(frame, ids, states=None):
    states = states if states is not None else (m.S,) * len(ids)
    return tuple(m.Row(frame, key, state) for key, state in zip(ids, states) if state != m.MISSING)

def fixture(edge='C03', entry_states=None, requirement_states=(m.S,), catalog_state=m.S):
    v = FixtureVerifier()
    ctx = context(edge)
    ids = tuple('required.' + str(i) for i in range(len(requirement_states)))
    cat = m.Catalog(ctx, 'basis', catalog_state, ids)
    prows, rrows = rows(ctx.frame, m.topology()[edge][2]), rows(ctx.frame, ids, requirement_states)
    source = m.SourceWitness(ctx, m.topology()[edge][0], 'source.basis')
    entry = None
    if edge in ('C03', 'C04'):
        ec = replace(ctx, frame=replace(ctx.frame, evaluation='entry'))
        entry = m.Assessment(ec, 'entry.basis', rows(ec.frame, m.ENTRY_CHECKS, entry_states))
        v.register(ec, 'entry', asdict(entry))
    for role, payload in [('catalog', asdict(cat)), ('source', asdict(source)),
                          ('predicates', asdict(m.aggregate(ctx.frame, m.topology()[edge][2], prows))),
                          ('requirements', asdict(m.aggregate(ctx.frame, ids, rrows)))]:
        v.register(ctx, role, payload)
    return m.evaluate_attempt(ctx, cat, prows, rrows, entry, source, v), v

def recording(a, edge, evaluation, v, bad=None, predecessor=None):
    ctx = replace(a.context, frame=replace(a.context.frame, edge=edge, evaluation=evaluation))
    states = (bad,) + (m.S,) * (len(m.RECORD_CHECKS) - 1) if bad is not None else None
    kind = 'DIAGNOSTIC'
    if edge in ('C14', 'C15', 'C16'):
        kind = 'CLOSURE'
    target = m.recording_target(a, kind, predecessor if predecessor is not None else a)
    assessment = m.Assessment(ctx, 'record.basis', rows(ctx.frame, m.RECORD_CHECKS, states), target=target)
    v.register(ctx, 'recording', asdict(assessment))
    return ctx, assessment

class M01Tests(unittest.TestCase):
    def test_entry_vectors_both_routes_and_diagnostic_coverage(self):
        count = 0
        for edge in ('C03', 'C04'):
            for states in itertools.product((*m.DOMAIN, m.MISSING), repeat=5):
                for requirement in (*m.DOMAIN, m.MISSING):
                    a, v = fixture(edge, states, (requirement,))
                    expected = states == (m.S,) * 5 and requirement == m.S
                    self.assertEqual(a.positive_conditions_met, expected)
                    decision = m.select_route(a, v)
                    self.assertEqual(decision.edge is None, expected)
                    count += 1
        self.assertEqual(count, 8192)

    def test_entry_failure_findings_and_missing_assessment(self):
        for edge in ('C03', 'C04'):
            a, v = fixture(edge, (m.S, m.B, m.U, m.MISSING, m.S))
            self.assertIn('entry:entry.bound_scope', a.known_blocks)
            self.assertIn('entry:entry.applicable_gate', a.unresolved_findings)
            self.assertIn('entry:entry.no_semantic_promotion', a.missing_reports)
            missing = m.evaluate_attempt(a.context, a.catalog, a.predicates.rows, a.requirements.rows,
                                         None, a.source_witness, v)
            self.assertFalse(missing.positive_conditions_met)
            self.assertEqual(len(missing.entry.missing), 5)

    def test_catalog_admission_and_default_failure(self):
        a, v = fixture('C05', requirement_states=(m.B,))
        result = m.evaluate_attempt(a.context, replace(a.catalog, required=()), a.predicates.rows, (),
                                     source_witness=a.source_witness, verifier=v)
        self.assertFalse(result.positive_conditions_met)
        self.assertIn('admission:catalog', result.unresolved_findings)
        good, _ = fixture('C05')
        result = m.evaluate_attempt(good.context, good.catalog, good.predicates.rows,
                                     good.requirements.rows, source_witness=good.source_witness)
        self.assertFalse(result.positive_conditions_met)
        self.assertIn('admission:source', result.unresolved_findings)

    def test_topology_and_p08_summary_attacks(self):
        a, v = fixture('C05', requirement_states=(m.B, m.U))
        self.assertEqual(m.p08_reference(a.catalog, a.requirements), m.U)
        with self.assertRaises(m.Rejected):
            m.p08_reference(a.catalog, replace(a.requirements, unresolved=(), blocked=()))
        with self.assertRaises(m.Rejected):
            m.p08_reference(replace(a.catalog, context=context('C04')), a.requirements)
        with self.assertRaises(TypeError):
            m.evaluate_attempt(a.context, a.catalog, a.predicates.rows, a.requirements.rows, topology={})
        changed = m.topology()
        changed['C05'] = ('CI0_PRESENTED', 'CI7_CLOSED', ('P03',), ())
        self.assertEqual(len(m.topology()['C05'][2]), 6)
        partial = m.evaluate_attempt(a.context, a.catalog, a.predicates.rows[:1], a.requirements.rows,
                                      source_witness=a.source_witness, verifier=v)
        self.assertFalse(partial.positive_conditions_met)
        self.assertEqual(len(partial.predicates.missing), 5)

    def test_mixed_selection_enforced_and_closure_lossless(self):
        a, v = fixture('C05', requirement_states=(m.B, m.U))
        decision = m.select_route(a, v)
        self.assertEqual(decision.edge, 'C13')
        self.assertTrue(decision.retains_both)
        rc, ra = recording(a, 'C09', 'record.block', v)
        with self.assertRaises(m.Rejected):
            m.evaluate_diagnostic(rc, a, ra, decision, v)
        rc, ra = recording(a, 'C13', 'record.unknown', v)
        for bad in (None, replace(decision, attempt_digest='forged')):
            with self.assertRaises(m.Rejected):
                m.evaluate_diagnostic(rc, a, ra, bad, v)
        prior = m.evaluate_diagnostic(rc, a, ra, decision, v)
        cc, ca = recording(a, 'C16', 'close', v, predecessor=prior)
        closed = m.evaluate_closure(cc, a, ca, prior=prior, verifier=v)
        self.assertTrue(closed.conditions_met)
        self.assertEqual(closed.carried_attempt, a)
        self.assertFalse(closed.grants_protected_operation_authority)
        self.assertFalse(closed.carried_attempt.positive_conditions_met)

    def test_each_diagnostic_edge_and_recording_guard(self):
        for progress in ('C01', 'C02', 'C04', 'C05'):
            for condition in (m.B, m.U):
                a, v = fixture(progress, requirement_states=(condition,))
                decision = m.select_route(a, v)
                for own in (m.S, m.B, m.U, m.MISSING):
                    rc, ra = recording(a, decision.edge, 'record', v, own)
                    review = m.evaluate_diagnostic(rc, a, ra, decision, v)
                    self.assertEqual(review.conditions_met, own == m.S)
                    self.assertEqual(review.carried_attempt, a)

    def test_identity_predecessor_epoch_and_effect_scope(self):
        a, v = fixture('C05', requirement_states=(m.B,))
        decision = m.select_route(a, v)
        rc, ra = recording(a, decision.edge, 'record', v)
        prior = m.evaluate_diagnostic(rc, a, ra, decision, v)
        cc, ca = recording(a, 'C15', 'record', v, predecessor=prior)
        with self.assertRaises(m.Rejected):
            m.evaluate_closure(cc, a, ca, prior=prior, verifier=v)
        for changed in (replace(rc, epoch='epoch.0'), replace(rc, subject_version='subject.0')):
            with self.assertRaises(m.Rejected):
                m.evaluate_diagnostic(changed, a, replace(ra, context=changed), decision, v)
        with self.assertRaises(m.Rejected):
            m.evaluate_diagnostic(rc, a, replace(ra, permitted_effects=('database_write',)), decision, v)
        cc, ca = recording(a, 'C15', 'close', v, predecessor=prior)
        with self.assertRaises(m.Rejected):
            m.evaluate_closure(cc, a, ca, prior=replace(prior, conditions_met=False), verifier=v)

    def test_occurrence_binding_and_unknown_occurrence(self):
        a, v = fixture('C05')
        oc = replace(a.context, frame=replace(a.context.frame, evaluation='occurrence'))
        occurrence = m.Occurrence(oc, 'attempt', m.S, 'occurrence.basis', m.S)
        v.register(oc, 'occurrence', asdict(occurrence))
        cc, ca = recording(a, 'C14', 'close', v, predecessor=occurrence)
        self.assertTrue(m.evaluate_closure(cc, a, ca, occurrence=occurrence, verifier=v).conditions_met)
        for changed in (replace(occurrence, assessed_attempt='old'),
                        replace(occurrence, context=replace(oc, epoch='epoch.0'))):
            with self.assertRaises(m.Rejected):
                m.evaluate_closure(cc, a, ca, occurrence=changed, verifier=v)
        unknown = replace(occurrence, result=m.U, basis=None)
        v.register(oc, 'occurrence', asdict(unknown))
        cc, ca = recording(a, 'C14', 'close', v, predecessor=unknown)
        self.assertFalse(m.evaluate_closure(cc, a, ca, occurrence=unknown, verifier=v).conditions_met)

    def test_forged_reviews_and_unadmitted_source(self):
        a, v = fixture('C03', (m.S, m.B, m.S, m.S, m.S))
        for changed in (replace(a, positive_conditions_met=True), replace(a, known_blocks=()),
                        replace(a, missing_reports=('invented',))):
            with self.assertRaises(m.Rejected):
                m.select_route(changed, v)
        good, v = fixture()
        bad_source = replace(good.source_witness, basis='forged')
        unadmitted = m.evaluate_attempt(good.context, good.catalog, (), good.requirements.rows,
                                         good.entry_assessment, bad_source, v)
        self.assertFalse(unadmitted.positive_conditions_met)

class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = b.Registry(REPO)
        cls.fixtures = tuple(json.loads(p.read_text()) for p in sorted(
            (REPO / 'schemas/conformance/positive').glob('*.json')))

    def test_all_fixtures_and_each_required_member_omission(self):
        count = 0
        for fixture in self.fixtures:
            review = self.registry.review(fixture)
            self.assertEqual(review.structural, 'STRUCTURALLY_VALID')
            self.assertEqual(review.content_admission, 'UNRESOLVED')
            self.assertFalse(review.effective_authority)
            schema = self.registry.schemas[fixture['schema_id'], fixture['schema_version']]
            for member in schema['required']:
                omitted = copy.deepcopy(fixture)
                del omitted[member]
                self.assertNotEqual(self.registry.review(omitted).structural, 'STRUCTURALLY_VALID')
                count += 1
        self.assertEqual(count, 91)

    def test_recursive_value_and_secret_shapes_in_all_roots(self):
        for fixture in self.fixtures:
            schema = self.registry.schemas[fixture['schema_id'], fixture['schema_version']]
            field = next(x for x in schema['required'] if x not in b.RESERVED and x not in (
                'authority_dimension', 'governed_schema_id', 'governed_schema_version'))
            if field == 'subjects':
                field = 'relationship'
            for invalid in ({'value':0.5}, 1.0, '\ud800'):
                changed = copy.deepcopy(fixture)
                changed[field] = invalid
                self.assertEqual(self.registry.review(changed).structural, 'STRUCTURALLY_INVALID')
            for forbidden in ({'private_key':'DUMMY'}, {'nested':['-----BEGIN PRIVATE KEY-----']}):
                changed = copy.deepcopy(fixture)
                changed[field] = forbidden
                review = self.registry.review(changed)
                self.assertEqual(review.structural, 'STRUCTURALLY_VALID')
                self.assertEqual(review.content_admission, 'BLOCKED')
                self.assertEqual(review.content_screening, 'RECOGNIZED_SHAPE_REJECTED')
                self.assertEqual(review.semantic_resolution, 'NOT_CHECKED')

    def test_duplicate_escape_keys_and_malformed_input(self):
        for raw in (b'{"schema_id":"wrong","schema_id":"right"}',
                    b'{"schema_id":"wrong","\\u0073chema_id":"right"}',
                    b'{"x":1.0}', b'{"x":NaN}', b'{"x":-0}', b'\xef\xbb\xbf{}',
                    b'{"x":"\\ud800"}', b'{}{}', b'\xff'):
            with self.assertRaises(b.Rejected):
                b.parse_transport(raw)

    def test_complete_document_canonical_bytes_and_types(self):
        for invalid in ({'x':1}, [], {'serialization_profile':'ACS-2','schema_id':'x','schema_version':'1'}):
            with self.assertRaises(b.Rejected):
                b.encode_document(invalid)
        for fixture in self.fixtures:
            raw = b.encode_document(fixture)
            self.assertEqual(b.canonical_document(raw), fixture)
            self.assertEqual(raw, b.encode_document(dict(reversed(tuple(fixture.items())))))
            with self.assertRaises(b.Rejected):
                b.canonical_document(raw + b'\n')
        value = {'serialization_profile':'ACS-1','schema_id':'example','schema_version':'1',
                 'unicode':'é','typed':[False,0,'',[],{},None],'large':2**100,'line':'a\r\nb'}
        self.assertEqual(b.canonical_document(b.encode_document(value)), value)
        self.assertIn('é'.encode(), b.encode_document(value))

    def test_registry_copies_and_resolution_do_not_collapse(self):
        fixture = next(x for x in self.fixtures if x['schema_id'] == 'anarchi.brain.observation')
        schema_copy = self.registry.schemas
        schema_copy[fixture['schema_id'],'1']['required'].remove('source')
        invalid = copy.deepcopy(fixture)
        del invalid['source']
        self.assertEqual(self.registry.resolve(invalid).status, 'VALID_CONTEXT')
        self.assertEqual(self.registry.review(invalid).structural, 'STRUCTURALLY_INVALID')
        unknown = copy.deepcopy(fixture)
        unknown['schema_version'] = 'unknown'
        self.assertEqual(self.registry.resolve(unknown).status, 'UNRESOLVED')

    def test_content_admission_is_exact_and_does_not_create_authority(self):
        fixture = self.fixtures[0]
        digest = hashlib.sha256(b.encode_document(fixture)).hexdigest()
        class FixtureContent:
            def verify_secret_free(self, value):
                return m.S if value.document_sha256 == digest else m.U
        result = self.registry.review(fixture, FixtureContent())
        self.assertEqual(result.content_admission, m.S)
        self.assertFalse(result.effective_authority)
        changed = copy.deepcopy(fixture)
        changed['source'] = 'other'
        self.assertNotEqual(self.registry.review(changed, FixtureContent()).content_admission, m.S)

if __name__ == '__main__':
    unittest.main(verbosity=2)

