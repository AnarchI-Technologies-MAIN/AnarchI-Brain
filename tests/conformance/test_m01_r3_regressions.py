"""Executable regressions for R2-REV-01 through R2-REV-06; dummy data only."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import copy
from dataclasses import asdict, replace, FrozenInstanceError
import hashlib
import importlib
import importlib.util
import json
import marshal
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
from qualification.m01_r3 import model as m, rescan
from schemas.conformance import boundary_r3 as b
from tests.conformance.test_m01_r3 import FixtureVerifier, context, rows, fixture, recording

REPO = Path(__file__).resolve().parents[2]
# Public supported child entry: check and compile the same launcher buffer.
VERIFIED_STUB = (
    "import hashlib,sys; p=sys.argv[1]; expected=sys.argv[2]; b=open(p,'rb').read(); "
    "actual=hashlib.sha256(b).hexdigest(); "
    "actual==expected or sys.exit('LAUNCHER_IDENTITY_MISMATCH'); "
    "sys.argv=[p]+sys.argv[3:]; "
    "exec(compile(b,p,'exec',dont_inherit=True),{'__name__':'__main__','__file__':p})"
)

def child_command(root, manifest_digest, optimization=(), task='probe-code'):
    original = json.loads((REPO/'evidence/stonewall-0/m01-r3/repair-manifest.json').read_bytes())
    pin = original['bound_files']['qualify_m01_r3.py']
    return [sys.executable, '-I', '-B', *optimization, '-c', VERIFIED_STUB,
            str(root/'qualify_m01_r3.py'), pin, '--repo', str(root),
            '--manifest-sha256', manifest_digest, '--task', task]

def attempt(evaluation, states=(m.B,), verifier=None):
    v = verifier if verifier is not None else FixtureVerifier()
    c = context('C05', evaluation)
    ids = tuple('required.' + str(i) for i in range(len(states)))
    catalog = m.Catalog(c, 'basis', m.S, ids)
    pr, rr = rows(c.frame, m.topology()['C05'][2]), rows(c.frame, ids, states)
    witness = m.SourceWitness(c, m.topology()['C05'][0], 'source.basis')
    for role, payload in [('catalog', asdict(catalog)), ('source', asdict(witness)),
                           ('predicates', asdict(m.aggregate(c.frame, m.topology()['C05'][2], pr))),
                           ('requirements', asdict(m.aggregate(c.frame, ids, rr)))]:
        v.register(c, role, payload)
    return m.evaluate_attempt(c, catalog, pr, rr, source_witness=witness, verifier=v), v

class RecordingTargetTests(unittest.TestCase):
    def test_diagnostic_cross_attempt_reuse_rejected(self):
        a, v = attempt('attempt.A')
        other, v = attempt('attempt.B', verifier=v)
        dc, assessment = recording(a, 'C09', 'record.shared', v)
        result = m.evaluate_diagnostic(dc, a, assessment, m.select_route(a, v), v)
        self.assertTrue(result.conditions_met)
        with self.assertRaisesRegex(m.Rejected, 'RECORDING_TARGET_MISMATCH'):
            m.evaluate_diagnostic(dc, other, assessment, m.select_route(other, v), v)
        changed = replace(assessment, target=m.recording_target(other, 'DIAGNOSTIC', other))
        result = m.evaluate_diagnostic(dc, other, changed, m.select_route(other, v), v)
        self.assertFalse(result.conditions_met)
        self.assertEqual(result.record_admission, m.U)

    def test_diagnostic_same_input_replay_deterministic_and_lossless(self):
        a, v = attempt('mixed', (m.B, m.U))
        decision = m.select_route(a, v)
        dc, assessment = recording(a, decision.edge, 'record', v)
        one = m.evaluate_diagnostic(dc, a, assessment, decision, v)
        two = m.evaluate_diagnostic(dc, a, assessment, decision, v)
        self.assertEqual(one, two)
        self.assertTrue(one.conditions_met)
        self.assertEqual(one.carried_attempt.known_blocks, a.known_blocks)
        self.assertEqual(one.carried_attempt.unresolved_findings, a.unresolved_findings)
        self.assertFalse(one.grants_protected_operation_authority)

    def test_closure_cross_predecessor_reuse_rejected(self):
        a, v = attempt('attempt.A')
        decision = m.select_route(a, v)
        c1, s1 = recording(a, decision.edge, 'diagnostic.A', v)
        c2, s2 = recording(a, decision.edge, 'diagnostic.B', v)
        one = m.evaluate_diagnostic(c1, a, s1, decision, v)
        two = m.evaluate_diagnostic(c2, a, s2, decision, v)
        cc, assessment = recording(a, 'C15', 'closure.shared', v, predecessor=one)
        self.assertTrue(m.evaluate_closure(cc, a, assessment, prior=one, verifier=v).conditions_met)
        with self.assertRaisesRegex(m.Rejected, 'RECORDING_TARGET_MISMATCH'):
            m.evaluate_closure(cc, a, assessment, prior=two, verifier=v)
        changed = replace(assessment, target=m.recording_target(a, 'CLOSURE', two))
        self.assertFalse(m.evaluate_closure(cc, a, changed, prior=two, verifier=v).conditions_met)

    def test_occurrence_target_cannot_be_swapped(self):
        a, v = attempt('attempt.A', (m.S,))
        oc1 = replace(a.context, frame=replace(a.context.frame, evaluation='occurrence.A'))
        oc2 = replace(oc1, frame=replace(oc1.frame, evaluation='occurrence.B'))
        one = m.Occurrence(oc1, 'attempt.A', m.S, 'basis', m.S)
        two = replace(one, context=oc2)
        for item in (one, two):
            v.register(item.context, 'occurrence', asdict(item))
        cc, assessment = recording(a, 'C14', 'close', v, predecessor=one)
        result = m.evaluate_closure(cc, a, assessment, occurrence=one, verifier=v)
        self.assertTrue(result.conditions_met)
        with self.assertRaisesRegex(m.Rejected, 'RECORDING_TARGET_MISMATCH'):
            m.evaluate_closure(cc, a, assessment, occurrence=two, verifier=v)

    def test_missing_wrong_kind_and_foreign_target_rejected(self):
        a, v = attempt('attempt')
        decision = m.select_route(a, v)
        c, item = recording(a, decision.edge, 'record', v)
        for target in (None, 'TARGET', replace(item.target, kind='CLOSURE'),
                       replace(item.target, attempt_digest='0'*64),
                       replace(item.target, predecessor_digest='0'*64)):
            with self.subTest(target=target):
                with self.assertRaises(m.Rejected):
                    m.evaluate_diagnostic(c, a, replace(item, target=target), decision, v)

    def test_entry_cannot_carry_recording_target(self):
        a, v = fixture('C03')
        changed = replace(a.entry_assessment,
                          target=m.RecordingTarget('DIAGNOSTIC', '0'*64, '0'*64))
        with self.assertRaisesRegex(m.Rejected, 'ENTRY_HAS_RECORDING_TARGET'):
            m.evaluate_attempt(a.context, a.catalog, a.predicates.rows, a.requirements.rows,
                               changed, a.source_witness, v)

class SnapshotBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.registry = b.Registry(REPO)
        self.value = json.loads((REPO/'schemas/conformance/positive/observation.v1.fixture.json').read_bytes())

    def test_reentrant_mutation_preserves_original_subject(self):
        value = self.value
        digest = hashlib.sha256(b.encode_document(value)).hexdigest()
        seen = []
        class Content:
            def verify_secret_free(self, subject):
                seen.append(subject)
                value.pop('source')
                return m.S if subject.document_sha256 == digest else m.U
        class Semantic:
            def verify_interpretation(self, subject):
                seen.append(subject)
                return m.S if subject.document_sha256 == digest else m.U
        result = self.registry.review(value, Content(), Semantic())
        self.assertEqual(result.structural, 'STRUCTURALLY_VALID')
        self.assertEqual(result.content_admission, m.S)
        self.assertEqual(result.semantic_resolution, m.S)
        self.assertEqual(result.subject.document_sha256, digest)
        self.assertIs(seen[0], seen[1])
        self.assertIs(seen[0], result.subject)
        self.assertEqual(self.registry.review(value).structural, 'STRUCTURALLY_INVALID')
        self.assertFalse(result.effective_authority)

    def test_split_snapshot_approvals_not_combined(self):
        value = self.value
        digest_a = hashlib.sha256(b.encode_document(value)).hexdigest()
        seen = []
        class Content:
            def verify_secret_free(self, subject):
                seen.append(subject.document_sha256)
                value['source'] = 'different.source'
                return m.S if subject.document_sha256 == digest_a else m.U
        class Semantic:
            def verify_interpretation(self, subject):
                seen.append(subject.document_sha256)
                digest_b = hashlib.sha256(b.encode_document(value)).hexdigest()
                return m.S if subject.document_sha256 == digest_b else m.U
        result = self.registry.review(value, Content(), Semantic())
        self.assertEqual(result.content_admission, m.S)
        self.assertEqual(result.semantic_resolution, m.U)
        self.assertEqual(seen, [digest_a, digest_a])
        self.assertNotEqual(digest_a, hashlib.sha256(b.encode_document(value)).hexdigest())

    def test_subject_is_immutable_and_interpretation_bound(self):
        result = self.registry.review(self.value)
        subject = result.subject
        self.assertEqual(subject.schema_id, self.value['schema_id'])
        self.assertEqual(subject.schema_version, self.value['schema_version'])
        self.assertEqual(subject.registry_sha256, b.REGISTRY_SHA)
        self.assertEqual(len(subject.schema_sha256), 64)
        with self.assertRaises(FrozenInstanceError):
            subject.document_sha256 = 'forged'

    def test_content_rejection_is_not_structural_rejection(self):
        self.value['observation'] = {'private_key':'DUMMY_TEST_ONLY_NOT_A_SECRET'}
        called = []
        class Never:
            def verify_secret_free(self, subject):
                called.append(subject)
                return m.S
        result = self.registry.review(self.value, Never())
        self.assertEqual(result.structural, 'STRUCTURALLY_VALID')
        self.assertEqual(result.content_admission, m.B)
        self.assertEqual(result.semantic_resolution, 'NOT_CHECKED')
        self.assertEqual(result.content_screening, 'RECOGNIZED_SHAPE_REJECTED')
        self.assertEqual(result.reason, 'CONTENT_SCREEN_REJECTED')
        self.assertEqual(called, [])
        self.assertNotIn('DUMMY_TEST_ONLY', str(result))
        self.value.pop('source')
        invalid = self.registry.review(self.value)
        self.assertEqual(invalid.structural, 'STRUCTURALLY_INVALID')
        self.assertEqual(invalid.content_admission, 'NOT_CHECKED')
        self.assertEqual(invalid.content_screening, 'NOT_CHECKED')

    def test_absent_content_admission_remains_unresolved(self):
        result = self.registry.review(self.value)
        self.assertEqual(result.content_admission, m.U)
        self.assertEqual(result.content_screening, 'NO_RECOGNIZED_SHAPE')
        self.assertEqual(result.semantic_resolution, m.U)

    def test_custom_copy_hooks_are_not_called(self):
        calls = []
        class Strange(dict):
            def __deepcopy__(self, memo):
                calls.append('copy')
                return dict(self)
        self.value['observation'] = Strange(value='dummy')
        result = self.registry.review(self.value)
        self.assertEqual(result.structural, 'STRUCTURALLY_INVALID')
        self.assertEqual(calls, [])

    def test_cycles_and_deep_inputs_fail_without_payload(self):
        self.value['observation'] = self.value
        result = self.registry.review(self.value)
        self.assertEqual(result.structural, 'STRUCTURALLY_INVALID')
        self.assertEqual(result.reason, 'REPRESENTATION_REJECTED')
        value = 0
        for _ in range(70):
            value = [value]
        self.value['observation'] = value
        self.assertEqual(self.registry.review(self.value).structural, 'STRUCTURALLY_INVALID')

    def test_invalid_verifier_result_rejected(self):
        class Bad:
            def verify_secret_free(self, subject):
                return True
        with self.assertRaises(b.Rejected):
            self.registry.review(self.value, Bad())

class HistoricalCoverageTests(unittest.TestCase):
    def setUp(self):
        root = REPO/'evidence/stonewall-0'
        self.preservation = json.loads((root/'m01-r2/preservation.json').read_bytes())
        self.r2 = json.loads((root/'m01-r2/repair-manifest.json').read_bytes())
        self.mapping = json.loads((root/'m01-r3/historical-map.json').read_bytes())
    def test_exact_relative_coverage_at_current_root(self):
        result = rescan.verify_history(REPO, self.preservation, self.r2, self.mapping)
        self.assertEqual(result['original_identity_set'],56)
        self.assertEqual(result['unchanged_originals_checked'],49)
        self.assertEqual(result['preserved_copies_checked'],9)
    def test_relocated_roots_verify_all_files(self):
        for name in ('relocated-Brain', 'AnarchI-Brain-copy'):
            with self.subTest(root=name), tempfile.TemporaryDirectory(prefix='m01-r3-history-') as temp:
                target = Path(temp)/name
                shutil.copytree(REPO, target, ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
                result = rescan.verify_history(target, self.preservation, self.r2, self.mapping)
                self.assertEqual(result['unchanged_originals_checked'],49)
                victim = next(x['path'] for x in self.mapping['originals'] if x['comparison']=='UNCHANGED_ORIGINAL')
                (target/victim).unlink()
                with self.assertRaises((rescan.Rejected, OSError)):
                    rescan.verify_history(target, self.preservation, self.r2, self.mapping)
    def test_missing_duplicate_unmapped_and_outside_rows_rejected(self):
        variants = []
        missing=copy.deepcopy(self.mapping); missing['originals'].pop(); variants.append(missing)
        duplicate=copy.deepcopy(self.mapping); duplicate['originals'][-1]=duplicate['originals'][0]; variants.append(duplicate)
        for name in ('not-mapped.txt','../outside.txt','/absolute.txt','C:/outside.txt','a\\b.txt'):
            changed=copy.deepcopy(self.mapping); changed['originals'][0]['path']=name; variants.append(changed)
        for variant in variants:
            with self.subTest(variant=variant['originals'][0]['path']):
                with self.assertRaises(rescan.Rejected):
                    rescan.verify_history(REPO,self.preservation,self.r2,variant)
    def test_origin_root_mismatch_cannot_zero_coverage(self):
        changed=copy.deepcopy(self.preservation)
        changed['original_sources']={k.replace('C:\\AnarchI-Brain','D:\\AnarchI-Brain'):v
                                     for k,v in changed['original_sources'].items()}
        with self.assertRaisesRegex(rescan.Rejected,'COVERAGE_INCOMPLETE'):
            rescan.verify_history(REPO,changed,self.r2,self.mapping)
    def test_changed_historical_bytes_rejected(self):
        with tempfile.TemporaryDirectory(prefix='m01-r3-changed-') as temp:
            target=Path(temp)/'repo'; shutil.copytree(REPO,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
            victim=next(x['path'] for x in self.mapping['originals'] if x['comparison']=='UNCHANGED_ORIGINAL')
            (target/victim).write_bytes((target/victim).read_bytes()+b'\nTEST\n')
            with self.assertRaises(rescan.Rejected):
                rescan.verify_history(target,self.preservation,self.r2,self.mapping)

class VerifiedSourceTests(unittest.TestCase):
    def test_only_verified_repository_modules_can_be_imported(self):
        with self.assertRaises(ImportError):
            importlib.import_module('qualification.m01_r2.model')

    def test_conflicting_timestamp_caches_are_not_executed(self):
        if sys.implementation.name != 'cpython':
            self.fail('CPYTHON_CACHE_REGRESSION_REQUIRES_CPYTHON')
        with tempfile.TemporaryDirectory(prefix='m01-r3-cache-') as temp:
            target=Path(temp)/'repo'
            shutil.copytree(REPO,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
            names=['qualification/m01_r3/__init__.py','qualification/m01_r3/model.py',
                   'qualification/m01_r3/rescan.py','schemas/conformance/boundary_r3.py',
                   'tests/conformance/test_m01_r3.py','tests/conformance/test_m01_r3_regressions.py',
                   'qualification/m01_r2/history/repair_r1.py']
            for name in names:
                source=target/name
                code=compile("raise RuntimeError('DELIBERATE_CONFLICTING_CACHE')",str(source),'exec')
                header=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(source.stat().st_mtime),source.stat().st_size)
                for optimization in ('','1'):
                    cache=Path(importlib.util.cache_from_source(str(source),optimization=optimization))
                    cache.parent.mkdir(parents=True,exist_ok=True)
                    cache.write_bytes(header+marshal.dumps(code))
            manifest=hashlib.sha256((target/'evidence/stonewall-0/m01-r3/repair-manifest.json').read_bytes()).hexdigest()
            for optimization in ([],['-O']):
                # Prove the deliberately conflicting cache is executable by an ordinary
                # source loader, so a malformed/inert cache cannot create a false pass.
                control_code = ("import importlib.util,sys; "
                    "s=importlib.util.spec_from_file_location('cache_control',sys.argv[1]); "
                    "m=importlib.util.module_from_spec(s); s.loader.exec_module(m)")
                control=subprocess.run([sys.executable,'-I','-B',*optimization,'-c',control_code,
                    str(target/'qualification/m01_r2/history/repair_r1.py')],
                    capture_output=True,text=True,timeout=30)
                self.assertNotEqual(control.returncode,0)
                self.assertIn('DELIBERATE_CONFLICTING_CACHE',control.stderr)
                proc=subprocess.run(child_command(target,manifest,optimization),
                                    capture_output=True,text=True,timeout=30)
                self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
                data=json.loads(proc.stdout.strip().splitlines()[-1])
                self.assertEqual(data['details']['C05_predicates'],['P03','P04','P05','P06','P07','P08'])
                self.assertFalse(data['details']['cache_loader_used'])

    def test_changed_source_or_wrong_manifest_rejected(self):
        with tempfile.TemporaryDirectory(prefix='m01-r3-source-') as temp:
            target=Path(temp)/'repo'; shutil.copytree(REPO,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
            pin=hashlib.sha256((target/'evidence/stonewall-0/m01-r3/repair-manifest.json').read_bytes()).hexdigest()
            bad=subprocess.run(child_command(target,'0'*64,['-O']),capture_output=True,text=True,timeout=30)
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('R3_MANIFEST_DIGEST_MISMATCH',bad.stdout)
            source=target/'qualification/m01_r3/model.py'
            source.write_bytes(source.read_bytes()+b'\n# DELIBERATE CHANGED SOURCE\n')
            bad=subprocess.run(child_command(target,pin,['-O']),capture_output=True,text=True,timeout=30)
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('SOURCE_DIGEST_MISMATCH',bad.stdout)

    def test_changed_launcher_rejected_before_execution(self):
        with tempfile.TemporaryDirectory(prefix='m01-r3-bootstrap-') as temp:
            target=Path(temp)/'repo'; shutil.copytree(REPO,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
            pin=hashlib.sha256((target/'evidence/stonewall-0/m01-r3/repair-manifest.json').read_bytes()).hexdigest()
            (target/'qualify_m01_r3.py').write_text("print('UNVERIFIED_BOOTSTRAP_EXECUTED')",encoding='utf-8')
            bad=subprocess.run(child_command(target,pin,['-O']),capture_output=True,text=True,timeout=30)
            self.assertNotEqual(bad.returncode,0)
            self.assertIn('LAUNCHER_IDENTITY_MISMATCH',bad.stderr)
            self.assertNotIn('UNVERIFIED_BOOTSTRAP_EXECUTED',bad.stdout)
