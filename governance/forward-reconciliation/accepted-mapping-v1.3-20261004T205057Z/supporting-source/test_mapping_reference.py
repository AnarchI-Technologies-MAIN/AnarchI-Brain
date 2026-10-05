import copy,importlib.util,pathlib,sys,unittest
from dataclasses import FrozenInstanceError,replace

path=pathlib.Path(__file__).parent/'mapping_reference.py'
spec=importlib.util.spec_from_file_location('mapping_reference',path)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

class MappingTests(unittest.TestCase):
    def setUp(self):
        self.subject=m.ReferenceSubject('1'*64,'2'*64,'3'*64,'fixture-candidate',1,'producer-local-scope')
        self.contract_pin='a'*64
        self.request=m.fixture_request(self.subject,'separately-requested-brain-scope',self.contract_pin)

    def test_compatible_shape_never_activates(self):
        for scope in ['producer-local-scope','separately-requested-brain-scope']:
            request=m.fixture_request(self.subject,scope,self.contract_pin)
            result=m.check_mapping(request,self.subject,self.contract_pin)
            self.assertEqual(result.disposition,'MAPPING_SHAPE_COMPATIBLE')
            self.assertFalse(result.runtime_crossing_permitted)
            self.assertFalse(result.canonical_membership)
            for field in ['content_admission','semantic_resolution','visibility_resolution','operative_authority']:
                self.assertEqual(getattr(result,field),'UNRESOLVED')

    def test_fixed_claim_substitution(self):
        for field,value in list(self.request.items()):
            if type(value)is str and field!='requested_ingress_scope':
                changed=copy.deepcopy(self.request);changed[field]='substituted'
                with self.subTest(field=field):
                    self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'MAPPING_VALUE:'+field)

    def test_effect_claims_and_boolean_impostors(self):
        for field in ['runtime_activation','canonical_membership']:
            for value in [True,0,1,None,'false']:
                changed=copy.deepcopy(self.request);changed[field]=value
                with self.subTest(field=field,value=value):
                    self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'FORBIDDEN_EFFECT_CLAIM:'+field)

    def test_false_baseline_context_rejected(self):
        for value in [False,0,1,None,'true']:
            changed=copy.deepcopy(self.request);changed['governing_baseline_adopted']=value
            self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'BASELINE_CONTEXT_MISMATCH')

    def test_subject_substitutions(self):
        for field in self.subject.__dataclass_fields__:
            changed=copy.deepcopy(self.request)
            changed['subject'][field]=2 if field=='source_record_version' else 'substituted'
            with self.subTest(field=field):
                self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'SUBJECT_MISMATCH:'+field)
        changed=copy.deepcopy(self.request);changed['subject']['source_record_version']=True
        self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'SUBJECT_MISMATCH:source_record_version')

    def test_unknown_fields_rejected_not_discarded(self):
        for field in ['authorization','canonical_write','execute_attachment','scope_grant']:
            changed=copy.deepcopy(self.request);changed[field]='claimed'
            self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'MAPPING_FIELDS')
        changed=copy.deepcopy(self.request);changed['subject']['authority']='claimed'
        self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'SUBJECT_FIELDS')

    def test_scope_request_not_permission(self):
        for scope in ['',None,True,{},'s'*513]:
            changed=copy.deepcopy(self.request);changed['requested_ingress_scope']=scope
            self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'INVALID_REQUESTED_SCOPE')

    def test_missing_field_and_bad_subject(self):
        for field in self.request:
            changed=copy.deepcopy(self.request);del changed[field]
            self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'MAPPING_FIELDS')
        self.assertEqual(m.check_mapping(self.request,object(),self.contract_pin).reason,'UNSUPPORTED_REFERENCE_SUBJECT')

    def test_subject_and_result_reject_ordinary_reassignment(self):
        with self.assertRaises(FrozenInstanceError):
            self.subject.brain_document_sha256='4'*64
        result=m.check_mapping(self.request,self.subject,self.contract_pin)
        with self.assertRaises(FrozenInstanceError):
            result.runtime_crossing_permitted=True

    def test_malformed_reference_subjects(self):
        for digest in ['1'*63,'1'*65,'A'*64,True,None]:
            subject=replace(self.subject,brain_document_sha256=digest)
            self.assertEqual(m.check_mapping(self.request,subject,self.contract_pin).reason,'INVALID_REFERENCE_DIGEST')
        for version in [True,0,-1,'1']:
            subject=replace(self.subject,source_record_version=version)
            self.assertEqual(m.check_mapping(self.request,subject,self.contract_pin).reason,'INVALID_REFERENCE_VERSION')
        for identity in ['',True,None,'x'*513]:
            subject=replace(self.subject,source_candidate_id=identity)
            self.assertEqual(m.check_mapping(self.request,subject,self.contract_pin).reason,'INVALID_REFERENCE_IDENTITY')

    def test_contract_identity_not_inferred_from_profile(self):
        changed=copy.deepcopy(self.request);changed['mapping_contract_sha256']='b'*64
        self.assertEqual(m.check_mapping(changed,self.subject,self.contract_pin).reason,'MAPPING_VALUE:mapping_contract_sha256')
        for pin in ['',True,'a'*63,'A'*64]:
            self.assertEqual(m.check_mapping(self.request,self.subject,pin).reason,'INVALID_MAPPING_CONTRACT_DIGEST')

if __name__=='__main__':unittest.main()
