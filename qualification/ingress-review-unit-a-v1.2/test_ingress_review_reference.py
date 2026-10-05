"""Focused structural/fixture tests; no runtime authorization claims."""
import dataclasses
import hashlib
import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('review_under_test', ROOT/'ingress_review_reference.py')
r = importlib.util.module_from_spec(spec); sys.modules[spec.name] = r; spec.loader.exec_module(r)

class IngressReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.buffers = {label:(ROOT/'inputs'/'code'/(label+'.py')).read_bytes() for label in r.SOURCE_PINS}
        cls.contract = (ROOT/'M04-S1-QUALIFICATION-DRAFT.md').read_bytes()
        cls.deps = r.load_dependencies(cls.buffers, cls.contract, r.sha(cls.contract))
        cls.brain = (ROOT/'fixture_first_brain.json').read_bytes()
        cls.producer = (ROOT/'fixture_first_producer.json').read_bytes()
        if r.sha(cls.brain) != '2820de81d3e4699f8086f18655e3a23f38b0aa9460e03fbb097bcea0cbd27d84' or r.sha(cls.producer) != 'ce2042084b61b562dcc5cb750365579a25ab48d4475c7deec562889f296b8763':
            raise ValueError('TEST_FIXTURE_DRIFT')
        p=json.loads(cls.brain)['proposal']; e=json.loads(cls.producer)
        cls.subject=r.ReferenceSubject(r.sha(cls.brain),r.sha(cls.producer),p['database_sha256'],p['source_candidate_id'],p['source_record_version'],e['scope'])
        cls.snapshot=r.Snapshot('a'*64,'a'*64,1,1,'OFFLINE_FIXTURE_ONLY')

    def check(self, brain=None, producer=None, subject=None, snapshot=None, deps=None):
        return r.evaluate(self.brain if brain is None else brain,self.producer if producer is None else producer,self.subject if subject is None else subject,self.snapshot if snapshot is None else snapshot,self.deps if deps is None else deps)

    def pin_changed(self, raw):
        return dataclasses.replace(self.subject,brain_document_sha256=r.sha(raw))

    def test_positive_no_effect_or_truth(self):
        result=self.check()
        self.assertEqual(result.disposition,'QUALIFICATION_SATISFIED')
        self.assertEqual(result.profile,'STRUCTURE_PROVENANCE_SCOPE_ONLY')
        self.assertFalse(result.protected_effect); self.assertFalse(result.runtime_crossing_permitted); self.assertFalse(result.canonical_membership)
        self.assertEqual(result.semantic_resolution,'UNRESOLVED'); self.assertEqual(result.content_admission,'UNRESOLVED'); self.assertEqual(result.operative_authority,'UNRESOLVED')
        self.assertEqual(result.runtime_m04_state,'CANDIDATE'); self.assertEqual(result.ordinary_access,'CLOSED')
        self.assertEqual(dict(result.m03_description)['operation_effect'],'NONE')
        self.assertEqual(dict(result.m08_description)['ordinary_access'],'CLOSED')

    def test_deterministic(self):
        self.assertEqual(self.check(),self.check())

    def test_matching_changed_fixture_context_has_distinct_identity(self):
        original=self.check()
        for snapshot in [dataclasses.replace(self.snapshot,expected_root_sha256='b'*64,observed_root_sha256='b'*64),dataclasses.replace(self.snapshot,expected_epoch=2,observed_epoch=2)]:
            changed=self.check(snapshot=snapshot)
            self.assertEqual(changed.disposition,'QUALIFICATION_SATISFIED')
            self.assertNotEqual(changed.context_sha256,original.context_sha256)
            self.assertNotEqual(changed,original)
            self.assertEqual(changed.reference_subject_sha256,original.reference_subject_sha256)
            self.assertEqual(changed.dependency_identity_sha256,original.dependency_identity_sha256)
            self.assertFalse(changed.protected_effect)

    def test_invalid_context_has_no_reflected_identity(self):
        result=self.check(snapshot=dataclasses.replace(self.snapshot,profile='secret-profile'))
        self.assertIsNone(result.context_sha256)
        self.assertNotIn('secret-profile',repr(result))

    def test_subject_and_contract_identity_changes_invalidate_reuse(self):
        original=self.check()
        other_contract=b'independently pinned fixture contract'
        deps=r.load_dependencies(self.buffers,other_contract,r.sha(other_contract))
        self.assertNotEqual(self.check(deps=deps).dependency_identity_sha256,original.dependency_identity_sha256)
        subject=dataclasses.replace(self.subject,producer_scope='different-finite-scope')
        changed=self.check(subject=subject)
        self.assertEqual(changed.disposition,'QUALIFICATION_BLOCKED')
        self.assertNotEqual(changed.reference_subject_sha256,original.reference_subject_sha256)

    def test_frozen_subject_snapshot_and_output(self):
        for obj,field,value in [(self.subject,'producer_scope','x'),(self.snapshot,'observed_epoch',9),(self.check(),'protected_effect',True)]:
            with self.assertRaises(dataclasses.FrozenInstanceError):setattr(obj,field,value)

    def test_frozen_dependency_bundle_rejects_ordinary_reassignment(self):
        for field,value in [('source_pins',()),('qualification_contract_sha256','0'*64),('mapping',None)]:
            with self.assertRaises(dataclasses.FrozenInstanceError):setattr(self.deps,field,value)

    def test_exact_canonical_fixture_context_and_dependencies(self):
        # Literal identities were independently calculated outside the evaluator.
        result=self.check()
        self.assertEqual(result.context_sha256,'65dc1de83ac60ceaaca66cd9cb16204268313b5243d3b47df5287124439b1baf')
        fixture_contract=b'fixture contract'
        deps=r.load_dependencies(self.buffers,fixture_contract,hashlib.sha256(fixture_contract).hexdigest())
        self.assertEqual(self.check(deps=deps).dependency_identity_sha256,'70735a24e3e658827b602cbac68d34091d2f479f3c4facc18f55a62edbd45049')

    def test_exact_canonical_unicode_subject_identity(self):
        subject=dataclasses.replace(self.subject,producer_scope='scope-脑-é')
        result=self.check(subject=subject)
        self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')
        self.assertEqual(result.reference_subject_sha256,'141dc266ee0c335360573b285c8271c9a9ab09455be447c7cf77496eaf5fc62f')
        self.assertFalse(result.runtime_crossing_permitted)

    def test_lone_surrogate_subject_strings_reject_without_exception(self):
        for field in ['source_candidate_id','producer_scope']:
            for value in ['\ud800','prefix\udfff']:
                result=self.check(subject=dataclasses.replace(self.subject,**{field:value}))
                self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')
                self.assertEqual(dict(result.findings)['exact_subject'],'BLOCKED')
                self.assertIsNone(result.reference_subject_sha256)
                self.assertFalse(result.protected_effect)
                self.assertNotIn('prefix',repr(result))

    def test_all_source_pins_before_execution(self):
        for label in self.buffers:
            buffers=dict(self.buffers); buffers[label]+=b'\nraise RuntimeError("MUST_NOT_EXECUTE")\n'
            with self.assertRaisesRegex(ValueError,'DEPENDENCY_SOURCE_DRIFT'):r.load_dependencies(buffers,self.contract,r.sha(self.contract))

    def test_dependency_membership(self):
        for buffers in [{},dict(self.buffers,unknown=b'pass'),{k:v for k,v in self.buffers.items() if k!='custody'}]:
            with self.assertRaisesRegex(ValueError,'DEPENDENCY_MEMBERSHIP'):r.load_dependencies(buffers,self.contract,r.sha(self.contract))

    def test_contract_external_pin(self):
        with self.assertRaisesRegex(ValueError,'QUALIFICATION_CONTRACT_DRIFT'):r.load_dependencies(self.buffers,self.contract,'0'*64)

    def test_drift_preserves_other_unresolved_findings(self):
        result=self.check(brain=self.brain+b' ')
        self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')
        self.assertEqual(dict(result.findings)['exact_subject'],'BLOCKED')
        self.assertEqual(dict(result.findings)['mapping'],'UNRESOLVED')
        self.assertFalse(result.protected_effect)

    def test_bound_empty_wrong_type(self):
        for raw in [b'',b'x'*(r.MAX_BYTES+1),'text',bytearray(self.brain)]:
            self.assertEqual(dict(self.check(brain=raw).findings)['resource_bounds'],'BLOCKED')

    def test_subject_bad_types_and_independent_coordinates(self):
        for field,value in [('source_record_version',True),('source_record_version',0),('source_record_version',r.MAX_COORDINATE+1),('source_candidate_id',''),('producer_scope','x'*513),('source_database_sha256','X'*64),('producer_scope','other-scope'),('source_candidate_id','other-candidate')]:
            result=self.check(subject=dataclasses.replace(self.subject,**{field:value}))
            self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')

    def test_missing_snapshot_is_unresolved(self):
        for snapshot in [dataclasses.replace(self.snapshot,observed_epoch=None),dataclasses.replace(self.snapshot,observed_root_sha256=None)]:
            self.assertEqual(self.check(snapshot=snapshot).disposition,'QUALIFICATION_UNRESOLVED')

    def test_stale_and_conflicting_fixture(self):
        for snapshot in [dataclasses.replace(self.snapshot,observed_epoch=2),dataclasses.replace(self.snapshot,observed_root_sha256='b'*64)]:
            result=self.check(snapshot=snapshot)
            self.assertEqual(dict(result.findings)['fixture_freshness'],'BLOCKED')
            self.assertEqual(dict(result.m08_description)['ordinary_access'],'CLOSED')

    def test_fixture_profiles_and_types(self):
        for field,value in [('profile','CURRENT_ROOT_AUTHENTICATED'),('expected_epoch',True),('expected_epoch',-1),('expected_epoch',r.MAX_COORDINATE+1),('observed_epoch',True),('observed_epoch',r.MAX_COORDINATE+1),('expected_root_sha256','bad'),('observed_root_sha256','bad')]:
            self.assertEqual(self.check(snapshot=dataclasses.replace(self.snapshot,**{field:value})).disposition,'QUALIFICATION_BLOCKED')

    def test_profile_requires_exact_str_even_with_custom_equality(self):
        class ClaimsEquality:
            def __eq__(self,other):return True
        class StringSubclass(str):pass
        for profile in [ClaimsEquality(),StringSubclass('OFFLINE_FIXTURE_ONLY'),True,{},None]:
            result=self.check(snapshot=dataclasses.replace(self.snapshot,profile=profile))
            self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')
            self.assertEqual(dict(result.findings)['fixture_freshness'],'BLOCKED')
            self.assertIsNone(result.context_sha256)
            self.assertFalse(result.protected_effect)

    def test_unknown_outer_fields(self):
        doc=json.loads(self.brain);doc['unknown']='private'
        raw=json.dumps(doc).encode()
        result=self.check(brain=raw,subject=self.pin_changed(raw))
        self.assertEqual(dict(result.findings)['structure'],'BLOCKED')
        self.assertNotIn('private',repr(result))

    def test_schema_value_and_boolean_cannot_override(self):
        for key,value in [('schema_version',True),('schema_id','other'),('serialization_profile','OTHER')]:
            doc=json.loads(self.brain);doc[key]=value;raw=json.dumps(doc).encode()
            self.assertEqual(dict(self.check(brain=raw,subject=self.pin_changed(raw)).findings)['structure'],'BLOCKED')

    def test_unknown_payload_fields(self):
        doc=json.loads(self.brain);doc['proposal']['authority_granted']=True;raw=json.dumps(doc).encode()
        self.assertEqual(dict(self.check(brain=raw,subject=self.pin_changed(raw)).findings)['structure'],'BLOCKED')

    def test_duplicate_fields(self):
        raw=b'{"schema_id":"x","schema_id":"y"}'
        self.assertEqual(dict(self.check(brain=raw,subject=self.pin_changed(raw)).findings)['structure'],'BLOCKED')

    def test_depth_nodes_and_json_types(self):
        for raw in [b'['*66+b'0'+b']'*66,b'['+b'0,'*100000+b'0]',b'{"x":1.5}',b'{"x":NaN}',b'\xff']:
            self.assertEqual(dict(self.check(brain=raw,subject=self.pin_changed(raw)).findings)['structure'],'BLOCKED')

    def test_provenance_tampering_and_no_reflection(self):
        doc=json.loads(self.brain);doc['proposal']['source_exact_record_sha256']='0'*64
        raw=json.dumps(doc).encode();result=self.check(brain=raw,subject=self.pin_changed(raw))
        self.assertEqual(dict(result.findings)['provenance'],'BLOCKED')
        self.assertEqual(result.disposition,'QUALIFICATION_BLOCKED')
        self.assertEqual(dict(result.findings)['fixture_freshness'],'SATISFIED')

    def test_dependencies_required(self):
        self.assertEqual(self.check(deps='unverified').disposition,'QUALIFICATION_BLOCKED')

if __name__=='__main__':unittest.main()
