import base64,contextlib,hashlib,importlib.util,io,json,pathlib,sys,tempfile,unittest
from unittest.mock import patch

base=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('custody_qualifier',base/'qualify_mapping_reference.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

class CustodyRejection(unittest.TestCase):
    def make_fixture(self,folder):
        root=folder/'mapping';root.mkdir()
        atlas=folder/'atlas-ubuntu-substrate-20261004';atlas.mkdir()
        for name in ['mapping_reference.py','CORTEX-FILAMENT-MAPPING-DRAFT.md','source-register.json']:
            (root/name).write_bytes((base/name).read_bytes())
        (root/'inputs').mkdir()
        for source in (base/'inputs').iterdir():(root/'inputs'/source.name).write_bytes(source.read_bytes())
        # Controlled prior-custody fixture, not a claim of actual Atlas qualification.
        verifier=b"def verify_output(root,pin):\n return {'verified_pairs':2736,'fixture_only':True}\n"
        (atlas/'verify_handoff_v5_1.py').write_bytes(verifier)
        prior={'focused_results':{'source_pins':{'verify_handoff_v5_1.py':hashlib.sha256(verifier).hexdigest()}},'full_corpus_runs':[{'producer_version':'v5.1','output':'fixture-output','qualification_sha256':'1'*64}]}
        prior_raw=json.dumps(prior).encode();(atlas/'FINAL-HANDOFF-REPAIR-RESULT.json').write_bytes(prior_raw)
        output=atlas/'fixture-output';output.mkdir()
        with (output/'proposals.jsonl').open('wb')as stream:
            for index in range(2736):
                producer=base64.b64encode(json.dumps({'scope':'fixture-producer-scope'}).encode()).decode()
                payload={'epistemaddy_proposal_sha256':'2'*64,'database_sha256':'3'*64,'source_candidate_id':'fixture-'+str(index),'source_record_version':1,'epistemaddy_proposal_utf8_base64':producer}
                stream.write(json.dumps({'proposal':payload}).encode()+b'\n')
        pins={name:hashlib.sha256((root/name).read_bytes()).hexdigest()for name in ['mapping_reference.py','CORTEX-FILAMENT-MAPPING-DRAFT.md','source-register.json']}
        argv=['qualifier','--mapping-sha256',pins['mapping_reference.py'],'--mapping-contract-sha256',pins['CORTEX-FILAMENT-MAPPING-DRAFT.md'],'--source-register-sha256',pins['source-register.json'],'--baseline-acceptance-sha256',q.json.loads((base/'source-register.json').read_bytes())['forward_baseline_acceptance']['sha256'],'--baseline-retention-sha256',q.json.loads((base/'source-register.json').read_bytes())['forward_baseline_retention']['sha256'],'--out',str(root/'result.json')]
        return root,atlas,argv,hashlib.sha256(prior_raw).hexdigest(),pins

    def test_full_qualifier_control_with_declared_custody_fixture(self):
        with tempfile.TemporaryDirectory(dir=base,prefix='positive-fixture-')as temporary:
            root,atlas,argv,prior_pin,pins=self.make_fixture(pathlib.Path(temporary))
            with patch.object(q,'ROOT',root),patch.object(q,'REPAIR_REPORT_PIN',prior_pin),patch.object(sys,'argv',argv),contextlib.redirect_stdout(io.StringIO()):q.main()
            receipt=json.loads((root/'result.json').read_bytes())
            self.assertEqual(receipt['reference_source_sha256'],pins['mapping_reference.py'])
            self.assertEqual(receipt['mapping_contract_sha256'],pins['CORTEX-FILAMENT-MAPPING-DRAFT.md'])
            self.assertEqual(receipt['source_register_sha256'],pins['source-register.json'])
            self.assertEqual(receipt['checked_subjects'],2736)
            self.assertEqual(receipt['runtime_crossings'],0)
            self.assertEqual(receipt['canonical_admissions'],0)
            self.assertIs(receipt['production_ready'],False)

    def test_cli_requires_each_external_pin_and_output(self):
        with tempfile.TemporaryDirectory(dir=base,prefix='cli-fixture-')as temporary:
            root,atlas,argv,prior_pin,pins=self.make_fixture(pathlib.Path(temporary))
            for flag in ['--mapping-sha256','--mapping-contract-sha256','--source-register-sha256','--baseline-acceptance-sha256','--baseline-retention-sha256','--out']:
                changed=list(argv);index=changed.index(flag);del changed[index:index+2]
                with self.subTest(flag=flag),patch.object(q,'ROOT',root),patch.object(q,'REPAIR_REPORT_PIN',prior_pin),patch.object(sys,'argv',changed),contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):q.main()

    def test_prior_verifier_and_portable_path_substitution(self):
        for target,reason in [('prior','PRIOR_REPAIR_REPORT_DRIFT'),('verifier','CUSTODY_VERIFIER_DRIFT'),('path','UPSTREAM_PATH_MAPPING'),('captured_source','UPSTREAM_SOURCE_DRIFT')]:
            with self.subTest(target=target),tempfile.TemporaryDirectory(dir=base,prefix='chain-fixture-')as temporary:
                root,atlas,argv,prior_pin,pins=self.make_fixture(pathlib.Path(temporary))
                if target=='prior':(atlas/'FINAL-HANDOFF-REPAIR-RESULT.json').write_bytes(b'{}')
                if target=='verifier':(atlas/'verify_handoff_v5_1.py').write_bytes(b'changed verifier')
                if target=='captured_source':(root/'inputs/brain_cortex_candidate.source').write_bytes(b'changed upstream')
                if target=='path':
                    register=json.loads((root/'source-register.json').read_bytes())
                    register['brain_cortex_candidate']['path']='../outside'
                    (root/'source-register.json').write_text(json.dumps(register))
                    argv[argv.index('--source-register-sha256')+1]=hashlib.sha256((root/'source-register.json').read_bytes()).hexdigest()
                with patch.object(q,'ROOT',root),patch.object(q,'REPAIR_REPORT_PIN',prior_pin),patch.object(sys,'argv',argv):
                    with self.assertRaisesRegex(ValueError,reason):q.main()
                self.assertFalse((root/'result.json').exists())

    def test_internally_bound_but_unselected_upstream_rejected(self):
        for label,reason in [('brain_cortex_candidate','BASELINE_SELECTED_MEMBER:cortex-contract.md'),('brain_dimensions_candidate','BASELINE_SELECTED_MEMBER:authority-dimensions.md')]:
            with self.subTest(label=label),tempfile.TemporaryDirectory(dir=base,prefix='splice-fixture-')as temporary:
                root,atlas,argv,prior_pin,pins=self.make_fixture(pathlib.Path(temporary))
                register=json.loads((root/'source-register.json').read_bytes())
                raw=b'validly hashed unrelated contract'
                (root/register[label]['path']).write_bytes(raw)
                register[label]['sha256']=hashlib.sha256(raw).hexdigest();register[label]['bytes']=len(raw)
                (root/'source-register.json').write_text(json.dumps(register))
                argv[argv.index('--source-register-sha256')+1]=hashlib.sha256((root/'source-register.json').read_bytes()).hexdigest()
                with patch.object(q,'ROOT',root),patch.object(q,'REPAIR_REPORT_PIN',prior_pin),patch.object(sys,'argv',argv):
                    with self.assertRaisesRegex(ValueError,reason):q.main()
                self.assertFalse((root/'result.json').exists())

    def test_baseline_catalog_constant_matches_registered_catalog(self):
        mapping=type('FixtureMapping',(),{'BASELINE_CATALOG':'0'*64})
        register=json.loads((base/'source-register.json').read_bytes())
        catalog=json.loads((base/'inputs/forward_baseline_catalog.source').read_bytes())
        with self.assertRaisesRegex(ValueError,'BASELINE_CATALOG_MEMBERSHIP'):
            q.verify_dependency_membership(mapping,register,catalog)

    def test_source_contract_register_and_upstream_substitution(self):
        for target,reason in [('source','MAPPING_SOURCE_DRIFT'),('contract','MAPPING_CONTRACT_DRIFT'),('register','SOURCE_REGISTER_DRIFT'),('upstream','UPSTREAM_SOURCE_DRIFT'),('membership','UPSTREAM_REGISTER_MEMBERSHIP')]:
            with self.subTest(target=target),tempfile.TemporaryDirectory(dir=base,prefix='custody-fixture-')as temporary:
                root=pathlib.Path(temporary)
                self.assertTrue(root.resolve().is_relative_to(base.resolve()))
                for name in ['mapping_reference.py','CORTEX-FILAMENT-MAPPING-DRAFT.md','source-register.json']:
                    (root/name).write_bytes((base/name).read_bytes())
                (root/'inputs').mkdir()
                for source in (base/'inputs').iterdir():(root/'inputs'/source.name).write_bytes(source.read_bytes())
                if target=='upstream':
                    register=json.loads((root/'source-register.json').read_bytes())
                    register['brain_cortex_candidate']['sha256']='0'*64
                    (root/'source-register.json').write_text(json.dumps(register))
                if target=='membership':(root/'source-register.json').write_text('{}')
                pins={name:hashlib.sha256((root/name).read_bytes()).hexdigest()for name in ['mapping_reference.py','CORTEX-FILAMENT-MAPPING-DRAFT.md','source-register.json']}
                if target=='source':pins['mapping_reference.py']='0'*64
                if target=='contract':pins['CORTEX-FILAMENT-MAPPING-DRAFT.md']='0'*64
                if target=='register':pins['source-register.json']='0'*64
                argv=['qualifier','--mapping-sha256',pins['mapping_reference.py'],'--mapping-contract-sha256',pins['CORTEX-FILAMENT-MAPPING-DRAFT.md'],'--source-register-sha256',pins['source-register.json'],'--baseline-acceptance-sha256',q.json.loads((base/'source-register.json').read_bytes())['forward_baseline_acceptance']['sha256'],'--baseline-retention-sha256',q.json.loads((base/'source-register.json').read_bytes())['forward_baseline_retention']['sha256'],'--out',str(root/'result.json')]
                with patch.object(q,'ROOT',root),patch.object(sys,'argv',argv):
                    with self.assertRaisesRegex(ValueError,reason):q.main()
                self.assertFalse((root/'result.json').exists())

if __name__=='__main__':unittest.main()
