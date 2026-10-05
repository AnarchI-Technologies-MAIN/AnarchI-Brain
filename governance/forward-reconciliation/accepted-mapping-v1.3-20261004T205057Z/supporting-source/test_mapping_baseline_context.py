import copy,hashlib,importlib.util,json,pathlib,tempfile,unittest
from unittest.mock import patch

base=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('baseline_qualifier',base/'qualify_mapping_reference.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

class BaselineEvidenceTests(unittest.TestCase):
    def run_context(self,mutator=None,external_wrong=False):
        register=json.loads((base/'source-register.json').read_bytes())
        catalog=json.loads((base/'inputs/forward_baseline_catalog.source').read_bytes())
        a=json.loads((base/'inputs/forward_baseline_acceptance.source').read_bytes())
        r=json.loads((base/'inputs/forward_baseline_retention.source').read_bytes())
        if mutator:mutator(a,r)
        with tempfile.TemporaryDirectory(dir=base,prefix='baseline-evidence-')as folder:
            root=pathlib.Path(folder);(root/'inputs').mkdir()
            # Controlled repinned evidence challenges exercise semantic checks beyond byte drift.
            for label,obj in [('forward_baseline_acceptance',a),('forward_baseline_retention',r)]:
                original=(base/register[label]['path']).read_bytes()
                raw=original if obj==json.loads(original) else json.dumps(obj).encode()
                (root/register[label]['path']).write_bytes(raw)
                register[label]['sha256']=q.sha(raw)
            ap=register['forward_baseline_acceptance']['sha256'];rp=register['forward_baseline_retention']['sha256']
            mapping=type('FixtureMapping',(),{'BASELINE_CATALOG':register['forward_baseline_catalog']['sha256'],'BASELINE_ACCEPTANCE':ap,'BASELINE_RETENTION':rp})
            # Updating only evidence bytes still rejects through independently retained body identity.
            if mutator is None:
                for label in ['forward_baseline_acceptance','forward_baseline_retention']:
                    raw=(base/register[label]['path']).read_bytes();(root/register[label]['path']).write_bytes(raw);register[label]['sha256']=q.sha(raw)
                ap=register['forward_baseline_acceptance']['sha256'];rp=register['forward_baseline_retention']['sha256']
                mapping.BASELINE_ACCEPTANCE=ap;mapping.BASELINE_RETENTION=rp
            with patch.object(q,'ROOT',root):return q.verify_baseline_context(mapping,register,catalog,'0'*64 if external_wrong else ap,rp)

    def test_real_retained_context_has_no_runtime_effect(self):
        result=self.run_context()
        self.assertEqual(result['scope'],'FORWARD_INTERPRETIVE_FOUNDATION_ONLY_NOT_RUNTIME_AUTHORITY')
        receipt=q.qualification_receipt(b'source',b'contract',b'register',{}, {},[],result)
        self.assertIs(receipt['governing_baseline_adopted'],True)
        self.assertIs(receipt['mapping_adopted'],False)
        self.assertIs(receipt['production_ready'],False)
        self.assertEqual(receipt['runtime_crossings'],0)
        self.assertEqual(receipt['canonical_admissions'],0)

    def test_external_pin_cannot_be_overridden_by_captured_register(self):
        with self.assertRaisesRegex(ValueError,'BASELINE_CONTEXT_PIN'):self.run_context(external_wrong=True)

    def test_repinned_semantic_evidence_tampering_rejected(self):
        cases=[
            (lambda a,r:a['decision'].__setitem__('actor','Another actor'),'BASELINE_DECISION_ACTOR'),
            (lambda a,r:a['decision'].__setitem__('decision_disposition','ACCEPT_ONE'),'BASELINE_ATOMIC_DECISION'),
            (lambda a,r:a['proposal'].__setitem__('sha256','0'*64),'BASELINE_ACCEPTANCE_CATALOG'),
            (lambda a,r:a['proposal']['selected_candidate_artifacts'].pop('semantic-language.md'),'BASELINE_ACCEPTANCE_SELECTED_SET'),
            (lambda a,r:a['procedure'].__setitem__('sha256','0'*64),'BASELINE_PROCEDURE_IDENTITY'),
            (lambda a,r:a['predecessor_linkage'].__setitem__('procedure_acceptance_record_sha256','0'*64),'BASELINE_PROCEDURE_ACCEPTANCE'),
            (lambda a,r:r.__setitem__('disposition','PENDING'),'BASELINE_RETENTION_DISPOSITION'),
            (lambda a,r:r.__setitem__('acceptance_record_unchanged',False),'BASELINE_RETAINED_ACCEPTANCE'),
            (lambda a,r:r.__setitem__('commit','0'*40),'BASELINE_REMOTE_IDENTITY'),
        ]
        for mutate,reason in cases:
            with self.subTest(reason=reason),self.assertRaisesRegex(ValueError,reason):self.run_context(mutate)

    def test_actual_capture_bytes_cannot_drift(self):
        register=json.loads((base/'source-register.json').read_bytes())
        catalog=json.loads((base/'inputs/forward_baseline_catalog.source').read_bytes())
        m=type('Mapping',(),{'BASELINE_CATALOG':register['forward_baseline_catalog']['sha256'],'BASELINE_ACCEPTANCE':register['forward_baseline_acceptance']['sha256'],'BASELINE_RETENTION':register['forward_baseline_retention']['sha256']})
        for label,reason in [('forward_baseline_acceptance','BASELINE_ACCEPTANCE_DRIFT'),('forward_baseline_retention','BASELINE_RETENTION_DRIFT')]:
            with self.subTest(label=label),tempfile.TemporaryDirectory(dir=base)as folder:
                root=pathlib.Path(folder);(root/'inputs').mkdir()
                for item in ['forward_baseline_acceptance','forward_baseline_retention']:(root/register[item]['path']).write_bytes((base/register[item]['path']).read_bytes())
                (root/register[label]['path']).write_bytes(b'{}')
                with patch.object(q,'ROOT',root),self.assertRaisesRegex(ValueError,reason):q.verify_baseline_context(m,register,catalog,m.BASELINE_ACCEPTANCE,m.BASELINE_RETENTION)

if __name__=='__main__':unittest.main()
