"""Documentary custody attacks; in-memory altered records are not adoption evidence."""
import copy,importlib.util,json,os,pathlib,shutil,sys,tempfile,unittest
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('unit_b_custody_tested',HERE/'qualify_custody.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
def encoded(value):return json.dumps(value).encode()
class CustodyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=q.read_captures(ROOT);cls.proof=(ROOT/'contracts/UNCHANGED-MATRIX-PROOF-DRAFT.json').read_bytes();cls.crosswalk=(ROOT/'contracts/AUTHORITY-CROSSWALK-UNIT-B-DRAFT.json').read_bytes()
 def temp_copy(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);root=pathlib.Path(t.name)/'candidate';root.mkdir()
  for name in ('input-register.json','chain-supplement-register.json'):
   shutil.copyfile(ROOT/name,root/name)
  for name in ('custody','inputs','contracts'):shutil.copytree(ROOT/name,root/name)
  return root
 def changed(self,label,change):
  c=self.c.copy();value=q.load_json(c[label]);change(value);c[label]=encoded(value);return c
 def test_positive_exact_chain_and_unchanged_matrix(self):
  self.assertEqual(q.verify_chain(self.c)['unit_a'],'2026-10-04T22:28:23Z')
  self.assertEqual(q.verify_matrix(self.c,self.proof,self.crosswalk),132)
  result=q.qualify(ROOT)
  for key in ('runtime_authority','operative_grant','effect_permitted','durable_consumption','production_ready'):self.assertIs(result[key],False)
 def test_duplicate_and_nonfinite_json_rejected(self):
  for raw,reason in [(b'{"x":1,"x":2}','DUPLICATE_JSON_KEY'),(b'{"x":NaN}','NONFINITE_JSON'),(b'{"x":Infinity}','NONFINITE_JSON')]:
   with self.subTest(raw=raw),self.assertRaisesRegex(ValueError,reason):q.load_json(raw)
 def test_changed_captured_receipt_bytes_rejected(self):
  root=self.temp_copy();p=root/'inputs/unit_a_retention.json';p.write_bytes(p.read_bytes()+b'\n')
  with self.assertRaisesRegex(ValueError,'CAPTURE_BYTES:unit_a_retention'):q.read_captures(root)
 def test_unknown_register_metadata_and_labels_rejected(self):
  root=self.temp_copy();p=root/'chain-supplement-register.json';original=q.load_json(p.read_bytes())
  for change,reason in [(lambda d:d.update(operative=True),'REGISTER_FIELDS'),(lambda d:d['files'][0].update(extra_permission=True),'REGISTER_ENTRY_FIELDS'),(lambda d:d['files'][0].update(label='unknown'),'REGISTER_LABEL_MEMBERSHIP')]:
   doc=copy.deepcopy(original);change(doc);p.write_bytes(encoded(doc))
   with self.assertRaisesRegex(ValueError,reason):q.read_captures(root)
 def test_register_scope_and_rebinding_rejected(self):
  root=self.temp_copy();p=root/'input-register.json';original=q.load_json(p.read_bytes())
  for change,reason in [(lambda d:d.update(runtime_authority=True),'REGISTER_SCOPE'),(lambda d:d['files'][0].update(sha256='0'*64),'REGISTER_IDENTITY_DRIFT')]:
   doc=copy.deepcopy(original);change(doc);p.write_bytes(encoded(doc))
   with self.assertRaisesRegex(ValueError,reason):q.read_captures(root)
 def test_duplicate_register_json_rejected(self):
  root=self.temp_copy();p=root/'input-register.json';p.write_bytes(b'{"runtime_authority":true,'+p.read_bytes()[1:])
  with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY:runtime_authority'):q.read_captures(root)
 def test_expected_identity_registry_cannot_be_rewritten(self):
  root=self.temp_copy();p=root/'custody/expected-capture-identities.json';p.write_bytes(p.read_bytes()+b'\n')
  with self.assertRaisesRegex(ValueError,'EXPECTED_CAPTURE_IDENTITY_DRIFT'):q.read_captures(root)
 def test_unsafe_paths_rejected(self):
  for name in ('../escape','/absolute','C:/absolute','inputs\\file','inputs/../file','inputs//file'):
   with self.subTest(name=name),self.assertRaisesRegex(ValueError,'BOUND_PATH'):q.safe_read(ROOT,name)
 def test_symlink_escape_rejected(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);base=pathlib.Path(t.name);root=base/'candidate';root.mkdir();outside=base/'outside';outside.write_bytes(b'outside')
  try:os.symlink(outside,root/'link')
  except (OSError,NotImplementedError)as error:self.skipTest('Host cannot create symlink: '+str(error))
  with self.assertRaisesRegex(ValueError,'BOUND_PATH_ESCAPE'):q.safe_read(root,'link')
 def test_baseline_selected_member_binding_rejected(self):
  c=self.c.copy();c['cortex_contract']+=b'\n'
  with self.assertRaisesRegex(ValueError,'BASELINE_SELECTED_BYTES:cortex-contract.md'):q.verify_chain(c)
 def test_procedure_subject_and_decision_cannot_be_substituted(self):
  for field,value,reason in [('actor','Other','PROCEDURE_DECISION_SCOPE'),('procedure_sha256','0'*64,'PROCEDURE_SUBJECT_FLOOR')]:
   c=self.changed('procedure_acceptance',lambda doc:doc.update({field:value}))
   with self.assertRaisesRegex(ValueError,reason):q.verify_chain(c)
 def test_effectiveness_floor_cannot_be_backdated(self):
  for label,reason in [('baseline_retention','BASELINE_EFFECTIVE_FLOOR'),('mapping_retention','MAPPING_EFFECTIVE_FLOOR'),('unit_a_retention','UNIT_A_EFFECTIVE_FLOOR')]:
   c=self.changed(label,lambda doc:doc.update(effective_not_before_utc='2000-01-01T00:00:00Z'))
   with self.assertRaisesRegex(ValueError,reason):q.verify_chain(c)
 def test_mapping_subject_and_question_links_rejected(self):
  c=self.changed('mapping_acceptance',lambda doc:doc['adoption_unit'].update(sha256='0'*64))
  with self.assertRaisesRegex(ValueError,'MAPPING_SUBJECT'):q.verify_chain(c)
  c=self.changed('mapping_question_supplement',lambda doc:doc.update(acceptance_record_sha256='0'*64))
  with self.assertRaisesRegex(ValueError,'MAPPING_QUESTION_LINK'):q.verify_chain(c)
 def test_unit_a_atomic_members_and_publication_rejected(self):
  c=self.changed('unit_a_acceptance',lambda doc:doc.update(atomic_all_eleven_or_none=False))
  with self.assertRaisesRegex(ValueError,'UNIT_A_ATOMIC_SCOPE'):q.verify_chain(c)
  c=self.changed('unit_a_retention_publication',lambda doc:doc.update(receipt_sha256='0'*64))
  with self.assertRaisesRegex(ValueError,'UNIT_A_PUBLICATION_LINK'):q.verify_chain(c)
 def test_matrix_proof_and_crosswalk_cannot_change_cells(self):
  proof=q.load_json(self.proof);proof['proposed_successor_cells']['S3']['Authorize']='bounded'
  with self.assertRaisesRegex(ValueError,'UNIT_B_MATRIX_CHANGED'):q.verify_matrix(self.c,encoded(proof),self.crosswalk)
  crosswalk=q.load_json(self.crosswalk);crosswalk['organs']['Cortex']['Authorize']='yes'
  with self.assertRaisesRegex(ValueError,'UNIT_B_CROSSWALK_CHANGED'):q.verify_matrix(self.c,self.proof,encoded(crosswalk))
 def test_unknown_proof_metadata_and_runtime_escalation_rejected(self):
  proof=q.load_json(self.proof);proof['operative_grant']=True
  with self.assertRaisesRegex(ValueError,'UNIT_B_PROOF_FIELDS'):q.verify_matrix(self.c,encoded(proof),self.crosswalk)
  crosswalk=q.load_json(self.crosswalk);crosswalk['runtime_activation']=True
  with self.assertRaisesRegex(ValueError,'UNIT_B_CROSSWALK_CHANGED'):q.verify_matrix(self.c,self.proof,encoded(crosswalk))
if __name__=='__main__':unittest.main()
