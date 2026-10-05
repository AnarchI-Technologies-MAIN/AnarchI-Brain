"""Finite documentary authority interpretation, not issuer enrollment or execution."""
import copy,dataclasses,importlib.util,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('fixture_factory_for_tests',ROOT/'fixture_factory.py')
f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)
r=f.ref

class AuthorityReferenceTests(unittest.TestCase):
    def fixture(self):return f.positive()
    def evaluate(self,document,rebind=True):
        if rebind:f.bind_consumption(document)
        data=f.raw(document);valid=r.validate(data,r.sha(data))
        return valid,r.evaluate(valid)
    def assert_held(self,value):
        for field in ('runtime_authority','operative_grant','effect_permitted','durable_consumption','production_ready'):
            self.assertIs(getattr(value,field),False)

    def test_both_positive_operations_all_stages_nonoperative(self):
        for operation in r.SPEC['operations']:
            valid,decision=self.evaluate(f.positive(operation))
            self.assertEqual(decision.disposition,'ALLOW')
            self.assertEqual(decision.grant_evaluation.disposition,'ALLOW')
            self.assertEqual(decision.authorization_evaluation.disposition,'ALLOW')
            self.assertEqual(decision.consumption_evaluation.disposition,'ALLOW')
            for stage in (decision.grant_evaluation,decision.authorization_evaluation,decision.consumption_evaluation):
                self.assertEqual(stage.profile,'OFFLINE_FIXTURE_ONLY');self.assert_held(stage)
            self.assertTrue(decision.root_model_satisfied)
            self.assertEqual(decision.actual_root_resolution,'ROOT_UNRESOLVED')
            self.assertEqual(decision.signature_verification,'NOT_PERFORMED')
            self.assertEqual(decision.actual_control_independence,'UNRESOLVED')
            prepared=r.prepare_consumption(valid,decision)
            self.assertEqual(prepared.disposition,'PREPARATION_READY_REFERENCE_ONLY')
            self.assertEqual(prepared.evaluator_version,decision.evaluator_version)
            self.assertIsNotNone(prepared.intent_digest)
            self.assert_held(decision);self.assert_held(prepared)

    def test_invalid_validation_outputs_all_five_holds(self):
        for raw,pin in [(b'', '0'*64),(b'{}','0'*64),(b'x'*(r.SPEC['limits']['bytes']+1),'0'*64)]:
            invalid=r.validate(raw,pin);self.assertIs(type(invalid),r.ValidationFailure);self.assert_held(invalid)
            decision=r.evaluate(invalid);self.assertEqual(decision.disposition,'DENY');self.assert_held(decision)

    def test_digest_and_input_types_fail_closed(self):
        data=f.raw(self.fixture())
        for raw,pin in [(bytearray(data),r.sha(data)),(data,'A'*64),(data,'0'*64),(data,True)]:
            self.assertIs(type(r.validate(raw,pin)),r.ValidationFailure)

    def test_json_boundaries_no_payload_reflection(self):
        samples=[b'{"profile":"x","profile":"secret"}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1.5}',b'\xff',b'['*40+b'0'+b']'*40,b'{"x":"\\ud800"}']
        for raw in samples:
            invalid=r.validate(raw,r.sha(raw));self.assertIs(type(invalid),r.ValidationFailure)
            self.assertNotIn('secret',repr(invalid))

    def test_unknown_missing_null_and_version_fields(self):
        samples=[]
        d=self.fixture();d['unknown']=True;samples.append(d)
        d=self.fixture();del d['authorization'];samples.append(d)
        d=self.fixture();d['grant']['grant_version']=2;samples.append(d)
        d=self.fixture();d['authorization']['authorization_version']=2;samples.append(d)
        for field in r.SPEC['objects']['requested_effect']:
            d=self.fixture();d['requested_effect'][field]=None;samples.append(d)
        for d in samples:
            data=f.raw(d);self.assertIs(type(r.validate(data,r.sha(data))),r.ValidationFailure)

    def test_boolean_ints_negative_large_and_utf8_surrogates(self):
        for section,field in [('grant','generation'),('grant','grant_version'),('authorization','subject_version'),('requested_effect','resource_version')]:
            for value in [True,-1,9223372036854775808]:
                d=self.fixture();d[section][field]=value
                data=f.raw(d);self.assertIs(type(r.validate(data,r.sha(data))),r.ValidationFailure)
        raw=b'{"profile":"\\ud800"}'
        self.assertIs(type(r.validate(raw,r.sha(raw))),r.ValidationFailure)

    def test_repeated_validation_rejects_constructed_or_replaced_values(self):
        d=self.fixture();data=f.raw(d);valid=r.validate(data,r.sha(data))
        for forged in [dataclasses.replace(valid,canonical_document=b'{}'),dataclasses.replace(valid,fixture_sha256='0'*64),dataclasses.replace(valid,expected_sha256='0'*64),r.ValidatedFixture(b'{}',r.sha(b'{}'),r.sha(b'{}'),b'{}')]:
            self.assertEqual(r.evaluate(forged).disposition,'DENY')
        with self.assertRaises(dataclasses.FrozenInstanceError):valid.raw=b'{}'

    def test_grant_is_not_authorization_and_consumer_is_not_authorizer(self):
        d=self.fixture();del d['authorization']
        raw=f.raw(d);invalid=r.validate(raw,r.sha(raw));self.assertIsInstance(invalid,r.ValidationFailure)
        self.assertEqual(r.evaluate(invalid).disposition,'DENY')
        d=self.fixture();d['current_observation']['authorization_revocation_feed_status']='UNKNOWN'
        _,decision=self.evaluate(d)
        self.assertEqual(decision.grant_evaluation.disposition,'ALLOW')
        self.assertEqual(decision.authorization_evaluation.disposition,'UNRESOLVED')
        self.assertEqual(decision.consumption_evaluation.disposition,'UNRESOLVED')
        d=self.fixture();d['grant']['grantee_principal_id']=d['principals']['grantee']['principal_id'];f.rebind_attestation(d)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')
        self.assertEqual(dict(decision.findings)['authorization_issuer_grant_grantee'],'DENY')

    def test_issued_authorization_is_positive_only_negative_objects_rejected(self):
        for operation in r.SPEC['operations']:
            for disposition in ('DENY','DEFER'):
                d=f.positive(operation);d['authorization']['decision_disposition']=disposition
                raw=f.raw(d);invalid=r.validate(raw,r.sha(raw))
                self.assertIs(type(invalid),r.ValidationFailure);self.assert_held(invalid)
                decision=r.evaluate(invalid);self.assertEqual(decision.disposition,'DENY');self.assert_held(decision)
                prepared=r.prepare_consumption(invalid,decision)
                self.assertIsNone(prepared.intent_digest);self.assert_held(prepared)

    def test_negative_evaluation_remains_distinct_from_positive_issued_object(self):
        for feed,outcome in [('COMPLETE_FIXTURE','DENY'),('UNKNOWN','UNRESOLVED')]:
            d=self.fixture();d['current_observation']['authorization_revocation_feed_status']=feed
            if feed=='COMPLETE_FIXTURE':d['current_observation']['revoked_authorization_refs']=[d['authorization']['authorization_id']]
            valid,decision=self.evaluate(d)
            self.assertIs(type(valid),r.ValidatedFixture)
            self.assertEqual(d['authorization']['decision_disposition'],'AUTHORIZE')
            self.assertEqual(decision.grant_evaluation.disposition,'ALLOW')
            self.assertEqual(decision.authorization_evaluation.disposition,outcome)
            self.assertEqual(decision.consumption_evaluation.disposition,outcome)

    def test_every_request_scope_coordinate_exact_no_prefix_wildcards(self):
        for field,kind in r.SPEC['objects']['requested_effect'].items():
            if field=='operation':value='CONSUME_MAINTENANCE_AUTHORIZATION'
            elif kind=='positive_int':value=2
            elif kind=='digest':value='0'*64
            else:value='different:'+field
            d=self.fixture();d['requested_effect'][field]=value
            _,decision=self.evaluate(d)
            self.assertEqual(decision.disposition,'DENY',field)
            self.assert_held(decision)

    def test_grant_and_authorization_digests_bind_full_bytes(self):
        for section,field,value in [('grant','purpose','different'),('authorization','authorization_id','different-id'),('authorization','issued_at',7)]:
            d=self.fixture();d[section][field]=value
            _,decision=self.evaluate(d)
            self.assertEqual(decision.disposition,'DENY')
            self.assertTrue(any(name in ('attestation_binding','grant_attestation_binding')and status=='DENY'for name,status in decision.findings))

    def test_doc_root_self_attestation_cannot_bootstrap(self):
        d=self.fixture();d['governance_selection']['selection_origin']='ROOT_SELF_ATTESTATION'
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY');self.assertFalse(decision.root_model_satisfied)

    def test_selection_missing_conflict_and_wrong_bootstrap_pin(self):
        for state,expected in [('UNKNOWN','UNRESOLVED'),('CONFLICT','CONFLICT')]:
            d=self.fixture();d['governance_selection']['status']=state
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,expected)
        d=self.fixture();d['governance_selection']['selected_bootstrap_sha256']='0'*64
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'CONFLICT')

    def test_synchronized_multiroot_lineage_still_unsupported(self):
        d=self.fixture();b=d['bootstrap'];old=b['root_digest'];new=f.h('fixture-replacement-root')
        b['root_id']='replacement-root';b['root_digest']=new;b['root_generation']=2
        b['root_lineage'].append({'root_id':b['root_id'],'root_digest':new,'predecessor_root_digest':old})
        d['grant'].update(root_id=b['root_id'],root_digest=new,root_lineage=copy.deepcopy(b['root_lineage']))
        d['authorization'].update(root_id=b['root_id'],root_digest=new)
        d['verifier_admission'].update(root_id=b['root_id'],root_digest=new)
        d['current_observation'].update(root_id=b['root_id'],root_digest=new,root_generation=2)
        d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(b));f.rebind_attestation(d)
        _,decision=self.evaluate(d)
        self.assertEqual(dict(decision.findings)['root_lineage'],'UNRESOLVED')
        self.assertEqual(decision.disposition,'UNRESOLVED');self.assertFalse(decision.root_model_satisfied)

    def test_replacement_keys_generations_and_role_class_hold(self):
        for role in d_roles():
            for field,value in [('key_id','replacement'),('key_fingerprint','0'*64),('generation',2),('predecessor_key_id','unadmitted-predecessor')]:
                d=self.fixture();d['key_bindings'][role][field]=value
                _,decision=self.evaluate(d);self.assertNotEqual(decision.disposition,'ALLOW')
        d=self.fixture();d['principals']['issuer']['principal_class']='DOCUMENTARY_CONSUMER'
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')

    def test_issuer_verifier_identity_and_shared_control_domains(self):
        for field in ['effective_controller_id','admin_domain_id','signing_custody_domain_id','evidence_provenance_domain_id','authority_lineage_ref']:
            d=self.fixture();d['principals']['verifier'][field]=d['principals']['issuer'][field]
            d['bootstrap']['admitted_principals']=copy.deepcopy(d['principals'])
            d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(d['bootstrap']))
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'CONFLICT')
        d=self.fixture();d['principals']['verifier']['principal_id']=d['principals']['issuer']['principal_id']
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')

    def test_all_required_role_pairs_control_independence(self):
        for left_role,right_role in [('grant_issuer','verifier'),('issuer','verifier'),('grantee','issuer')]:
            for field in ['effective_controller_id','admin_domain_id','signing_custody_domain_id','evidence_provenance_domain_id','authority_lineage_ref']:
                d=self.fixture();d['principals'][right_role][field]=d['principals'][left_role][field]
                d['bootstrap']['admitted_principals']=copy.deepcopy(d['principals'])
                d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(d['bootstrap']))
                _,decision=self.evaluate(d)
                self.assertEqual(decision.disposition,'CONFLICT')
                self.assertIn(('independence.'+left_role+'.'+right_role+'.'+field,'CONFLICT'),decision.findings)

    def test_unadmitted_actor_cannot_pass_by_three_way_echo(self):
        d=self.fixture()
        for section in ('grant','authorization','requested_effect'):d[section]['effect_actor_principal_id']='unadmitted-actor'
        f.rebind_attestation(d);_,decision=self.evaluate(d)
        self.assertEqual(decision.disposition,'DENY')
        self.assertIn(('grant_effect_actor_admission','DENY'),decision.findings)
        self.assertIn(('authorization_effect_actor_admission','DENY'),decision.findings)

    def test_authorizer_key_valid_now_but_not_when_issued_rejects(self):
        d=self.fixture();d['key_bindings']['issuer']['activation_time']=8
        d['bootstrap']['admitted_key_bindings']=copy.deepcopy(d['key_bindings'])
        d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(d['bootstrap']))
        _,decision=self.evaluate(d)
        self.assertIn(('key_activation.issuer','ALLOW'),decision.findings)
        self.assertIn(('authorization_issuance_key_activation','DENY'),decision.findings)
        self.assertEqual(decision.disposition,'DENY')

    def test_grant_evidence_cannot_precede_grant_issuer_key_or_root(self):
        for target in ['grant_issuer_key','root']:
            d=self.fixture()
            if target=='grant_issuer_key':
                d['key_bindings']['grant_issuer']['activation_time']=6
                d['bootstrap']['admitted_key_bindings']=copy.deepcopy(d['key_bindings'])
            if target=='root':d['bootstrap']['effective_not_before']=6
            d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(d['bootstrap']))
            f.rebind_attestation(d);_,decision=self.evaluate(d)
            self.assertIn(('grant_evidence_authority_activation','DENY'),decision.findings)
            self.assertEqual(decision.grant_evaluation.disposition,'DENY')
            self.assertEqual(decision.authorization_evaluation.disposition,'DENY')

    def test_grant_may_be_documented_before_future_own_activation(self):
        d=self.fixture();d['grant']['not_before']=8
        d['authorization'].update(evidence_time=9,issued_at=9,not_before=9)
        f.rebind_attestation(d);_,decision=self.evaluate(d)
        self.assertEqual(decision.disposition,'ALLOW')
        self.assertLess(d['grant']['evidence_time'],d['grant']['not_before'])

    def test_grant_generation_epoch_revocation_rollback_future_and_missing(self):
        for field in ['generation','epoch','revocation_generation']:
            for value,expected in [(0,'CONFLICT'),(2,'DENY'),(None,'UNRESOLVED')]:
                d=self.fixture();d['current_observation'][field]=value
                _,decision=self.evaluate(d);self.assertEqual(decision.disposition,expected)
                self.assertNotEqual(decision.authorization_evaluation.disposition,'ALLOW')
        d=self.fixture();d['current_observation']['root_generation']=0
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'CONFLICT')

    def test_verifier_unknown_compromised_and_self_admission(self):
        for status,expected in [('UNKNOWN','UNRESOLVED'),('COMPROMISED','DENY')]:
            d=self.fixture();d['current_observation']['verifier_status']=status
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,expected)
        d=self.fixture();d['verifier_admission']['admission_kind']='SELF_ADMISSION'
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')

    def test_parent_revocation_invalidates_child_no_grandfathering(self):
        d=self.fixture();d['current_observation']['revoked_refs']=[d['grant']['grant_id']]
        _,decision=self.evaluate(d)
        self.assertEqual(decision.grant_evaluation.disposition,'DENY');self.assertEqual(decision.authorization_evaluation.disposition,'DENY')
        self.assertEqual(decision.consumption_evaluation.disposition,'DENY')

    def test_authorization_revocation_separate_from_parent_feed(self):
        d=self.fixture();d['current_observation']['revoked_authorization_refs']=[d['authorization']['authorization_id']]
        _,decision=self.evaluate(d)
        self.assertEqual(decision.grant_evaluation.disposition,'ALLOW');self.assertEqual(decision.authorization_evaluation.disposition,'DENY')
        d=self.fixture();d['current_observation']['authorization_revocation_feed_status']='UNKNOWN'
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')

    def test_empty_complete_feed_and_missing_feed_are_distinct(self):
        for field in ['revocation_feed_status','authorization_revocation_feed_status','denial_feed_status']:
            d=self.fixture();d['current_observation'][field]='UNKNOWN'
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')

    def test_time_bounds_expiry_uncertainty_future_and_evidence_age(self):
        for earliest,latest,expected in [(10,10,'ALLOW'),(17,19,'UNRESOLVED'),(20,20,'DENY'),(1,2,'DENY')]:
            d=self.fixture();d['current_observation'].update(now_earliest=earliest,now_latest=latest)
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,expected)
        d=self.fixture();d['current_observation'].update(time_status='UNKNOWN',now_earliest=None,now_latest=None)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')
        d=self.fixture();d['current_observation'].update(now_earliest=11,now_latest=10)
        data=f.raw(d);self.assertIs(type(r.validate(data,r.sha(data))),r.ValidationFailure)

    def test_authorization_interval_subset_and_conditions(self):
        for field,value in [('expires_at',21),('not_before',0),('issued_at',25),('evidence_time',30),('generation',2),('subject_version',2)]:
            d=self.fixture();d['authorization'][field]=value;f.rebind_attestation(d)
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')
        d=self.fixture();d['authorization']['conditions']['extra_conditions']='UNKNOWN_PREDICATE';f.rebind_attestation(d)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')

    def test_delegation_supersession_and_dimension(self):
        d=self.fixture();d['grant']['delegation']=True;f.rebind_attestation(d)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')
        d=self.fixture();d['grant']['authority_dimension']='Consume';f.rebind_attestation(d)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY')
        for section,field in [('grant','supersedes_grant_id'),('authorization','supersedes_authorization_id')]:
            d=self.fixture();d[section][field]='earlier-identity';f.rebind_attestation(d)
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')

    def test_deny_conflict_unresolved_precedence_preserves_all_findings(self):
        d=self.fixture();d['current_observation']['denials']=[{'denial_id':'fixture-denial','scope':copy.deepcopy(d['requested_effect']),'source_ref':'fixture-denial-source'}]
        d['current_observation']['root_generation']=0;d['current_observation']['revocation_feed_status']='UNKNOWN'
        _,decision=self.evaluate(d)
        self.assertEqual(decision.disposition,'DENY')
        self.assertIn(('observed_root','CONFLICT'),decision.findings);self.assertIn(('grant_revocation','UNRESOLVED'),decision.findings)
        self.assertIn(('explicit_denial','DENY'),decision.findings)

    def test_wrong_scope_denial_does_not_match_and_unknown_feed_holds(self):
        d=self.fixture();scope=copy.deepcopy(d['requested_effect']);scope['tenant']='other-tenant'
        d['current_observation']['denials']=[{'denial_id':'other-denial','scope':scope,'source_ref':'fixture-source'}]
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'ALLOW')
        d['current_observation']['denial_feed_status']='UNKNOWN'
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')

    def test_consumed_replay_and_crash_ambiguities_never_reexecute(self):
        d=self.fixture();d['consumption'].update(state='CONSUMED',effect_observation='OCCURRED',terminal_receipt_digest='a'*64)
        valid,decision=self.evaluate(d);self.assertEqual(decision.disposition,'DENY');self.assert_held(r.prepare_consumption(valid,decision))
        for effect in ['UNKNOWN','PARTIAL_EFFECT','RECEIPT_WITHOUT_EFFECT','EFFECT_WITHOUT_RECEIPT','CRASH_AFTER_FENCE']:
            d=self.fixture();d['consumption']['effect_observation']=effect
            valid,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')
            prepared=r.prepare_consumption(valid,decision);self.assertEqual(prepared.effect_outcome,'EFFECT_OUTCOME_UNRESOLVED');self.assertIsNone(prepared.intent_digest)
        d=self.fixture();d['consumption'].update(state='CONSUMED',effect_observation='OCCURRED',terminal_receipt_digest=None)
        _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'UNRESOLVED')

    def test_consumption_identity_binds_all_layers_and_generation(self):
        for field in ['grant_digest','authorization_digest','request_digest','context_digest','evaluation_digest','authorization_id','authorization_version','generation']:
            d=self.fixture();d['consumption'][field]=2 if field in ('authorization_version','generation')else 'wrong-id'if field=='authorization_id'else '0'*64
            _,decision=self.evaluate(d,rebind=False);self.assertEqual(decision.disposition,'CONFLICT',field)

    def test_prepare_recomputes_fresh_context_and_rejects_forged_decisions(self):
        valid,decision=self.evaluate(self.fixture())
        with self.assertRaises(dataclasses.FrozenInstanceError):decision.runtime_authority=True
        for forged in [dataclasses.replace(decision,runtime_authority=True),dataclasses.replace(decision,base_evaluation_digest='0'*64),dataclasses.replace(decision,authorization_digest='0'*64)]:
            prepared=r.prepare_consumption(valid,forged);self.assertEqual(prepared.disposition,'DENY');self.assert_held(prepared)
        d=self.fixture();d['current_observation']['revoked_authorization_refs']=[d['authorization']['authorization_id']]
        current,_=self.evaluate(d)
        self.assertEqual(r.prepare_consumption(current,decision).disposition,'DENY')

    def test_all_public_stage_outputs_and_validation_are_frozen(self):
        valid,decision=self.evaluate(self.fixture())
        prepared=r.prepare_consumption(valid,decision)
        invalid=r.validate(b'', '0'*64)
        for value,field,replacement in [(valid,'expected_sha256','0'*64),(invalid,'reason','forged'),(decision,'runtime_authority',True),(decision.grant_evaluation,'runtime_authority',True),(decision.authorization_evaluation,'runtime_authority',True),(decision.consumption_evaluation,'runtime_authority',True),(prepared,'runtime_authority',True)]:
            with self.assertRaises(dataclasses.FrozenInstanceError):setattr(value,field,replacement)

    def test_changed_authorization_identity_invalidates_intent_even_valid(self):
        valid,decision=self.evaluate(self.fixture());first=r.prepare_consumption(valid,decision)
        d=self.fixture();d['authorization']['authorization_id']='new-issued-authorization';f.rebind_attestation(d)
        valid,decision=self.evaluate(d);second=r.prepare_consumption(valid,decision)
        self.assertEqual(decision.disposition,'ALLOW');self.assertNotEqual(first.intent_digest,second.intent_digest)

    def test_deterministic_unicode_context_and_no_secret_echo(self):
        d=self.fixture();d['requested_effect']['job']='secret-job-脑';d['grant']['job']=d['requested_effect']['job'];d['authorization']['job']=d['requested_effect']['job'];f.rebind_attestation(d)
        _,first=self.evaluate(d);_,second=self.evaluate(copy.deepcopy(d))
        self.assertEqual(first,second);self.assertEqual(first.disposition,'ALLOW');self.assertNotIn('secret-job',repr(first))

    def test_canonical_bytes_have_independent_sorted_utf8_oracle(self):
        expected=bytes.fromhex('7b2261223a22e88491222c227a223a317d')
        self.assertEqual(r.canonical({'z':1,'a':'脑'}),expected)
        self.assertEqual(r.sha(expected),'16c5ae6429347537f81865be0f28f66b3376823369180078746ea96a96af706f')
        self.assertEqual(r.sha(r.canonical({'z':1,'a':'脑'})),'16c5ae6429347537f81865be0f28f66b3376823369180078746ea96a96af706f')

    def test_description_and_identity_exact_distinct_length_bounds(self):
        for length in (513,2048):
            d=self.fixture();description='x'*length
            d['requested_effect']['effect_description']=description
            digest=r.sha(description.encode('utf-8'))
            for section in ('grant','authorization','requested_effect'):d[section]['effect_description_digest']=digest
            f.rebind_attestation(d)
            _,decision=self.evaluate(d);self.assertEqual(decision.disposition,'ALLOW')
        for length,accepted in ((512,True),(513,False)):
            d=self.fixture()
            for section in ('grant','authorization','requested_effect'):d[section]['job']='j'*length
            f.rebind_attestation(d);raw=f.raw(d);value=r.validate(raw,r.sha(raw))
            self.assertEqual(isinstance(value,r.ValidatedFixture),accepted)
        d=self.fixture();d['requested_effect']['effect_description']='x'*2049
        raw=f.raw(d);self.assertIsInstance(r.validate(raw,r.sha(raw)),r.ValidationFailure)

    def test_cross_coordinate_control_collisions_for_all_required_pairs(self):
        for left,right in (('grant_issuer','verifier'),('issuer','verifier'),('grantee','issuer')):
            for left_field,right_field in (('effective_controller_id','admin_domain_id'),('signing_custody_domain_id','evidence_provenance_domain_id')):
                d=self.fixture();d['principals'][right][right_field]=d['principals'][left][left_field]
                d['bootstrap']['admitted_principals']=copy.deepcopy(d['principals'])
                d['governance_selection']['selected_bootstrap_sha256']=r.sha(r.canonical(d['bootstrap']))
                f.rebind_attestation(d);valid,decision=self.evaluate(d)
                self.assertEqual(decision.disposition,'CONFLICT',(left,right,left_field,right_field))
                self.assertIsNone(r.prepare_consumption(valid,decision).intent_digest)

    def test_not_consumed_terminal_receipt_contradiction(self):
        d=self.fixture();d['consumption']['terminal_receipt_digest']='a'*64
        valid,decision=self.evaluate(d)
        self.assertEqual(decision.disposition,'CONFLICT')
        self.assertEqual(decision.consumption_evaluation.disposition,'CONFLICT')
        prepared=r.prepare_consumption(valid,decision);self.assertIsNone(prepared.intent_digest);self.assert_held(prepared)

def d_roles():return ('grant_issuer','issuer','verifier','grantee')
if __name__=='__main__':unittest.main()
