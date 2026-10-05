import hashlib,importlib.util,pathlib,unittest

base=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('qualifier',base/'qualify_mapping_reference.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

class ReceiptBinding(unittest.TestCase):
    def test_source_pin_survives_corpus_reorder_and_content_change(self):
        source=(base/'mapping_reference.py').read_bytes()
        expected=hashlib.sha256(source).hexdigest()
        first={'subject_sha256':'1'*64};second={'subject_sha256':'2'*64}
        for decisions in [[first,second],[second,first],[{'subject_sha256':'3'*64}]]:
            with self.subTest(decisions=decisions):
                receipt=q.qualification_receipt(source,b'contract',b'register',{}, {},decisions)
                self.assertEqual(receipt['reference_source_sha256'],expected)
                self.assertNotEqual(receipt['reference_source_sha256'],decisions[-1]['subject_sha256'])
                self.assertEqual(receipt['mapping_contract_sha256'],hashlib.sha256(b'contract').hexdigest())
                self.assertEqual(receipt['source_register_sha256'],hashlib.sha256(b'register').hexdigest())
                for field in ['governing_baseline_adopted','mapping_adopted','production_ready']:
                    self.assertIs(receipt[field],False)
                self.assertEqual(receipt['canonical_admissions'],0)
                self.assertEqual(receipt['runtime_crossings'],0)

    def test_changed_mapping_bytes_change_source_receipt(self):
        original=q.qualification_receipt(b'source A',b'contract',b'register',{}, {},[])
        changed=q.qualification_receipt(b'source B',b'contract',b'register',{}, {},[])
        self.assertNotEqual(original['reference_source_sha256'],changed['reference_source_sha256'])

if __name__=='__main__':unittest.main()
