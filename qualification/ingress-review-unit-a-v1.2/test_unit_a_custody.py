"""Adversarial single-cell and relationship custody checks, not runtime proof."""
import copy,importlib.util,json,pathlib,sys,unittest,tempfile,shutil
ROOT=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('unit_custody_under_test',ROOT/'qualify_unit_a.py')
q=importlib.util.module_from_spec(spec);sys.modules[spec.name]=q;spec.loader.exec_module(q)

class UnitCustodyTests(unittest.TestCase):
    def setUp(self):
        self.old=(ROOT/'inputs/baseline/authority-matrix.md').read_bytes()
        self.new=(ROOT/'AUTHORITY-MATRIX-SUCCESSOR-DRAFT.md').read_bytes()
        self.crosswalk=json.loads((ROOT/'authority-crosswalk-unit-a.json').read_bytes())

    def test_positive_exact_cell_with_no_grant(self):
        self.assertEqual(q.verify_matrix_context(self.old,self.new,self.crosswalk),[('S1','Qualify','unresolved','bounded')])
        self.assertFalse(self.crosswalk['authority_granted_by_crosswalk'])

    def test_other_cell_change_even_with_updated_hash_rejected(self):
        changed=self.new.replace(b'| S3 | yes | no | unresolved | unresolved |',b'| S3 | yes | no | unresolved | bounded |')
        altered=copy.deepcopy(self.crosswalk);altered['matrix_sha256']=q.sha(changed);altered['organs']=q.matrix_cells(changed)
        with self.assertRaisesRegex(ValueError,'EXACT_SINGLE_CELL_DELTA'):q.verify_matrix_context(self.old,changed,altered)

    def test_unbounded_qualification_and_omission_rejected(self):
        for value in (b'yes',b'unresolved'):
            changed=self.new.replace(b'| S1 | yes | unresolved | bounded |',b'| S1 | yes | unresolved | '+value+b' |')
            altered=copy.deepcopy(self.crosswalk);altered['matrix_sha256']=q.sha(changed);altered['organs']=q.matrix_cells(changed)
            with self.assertRaisesRegex(ValueError,'EXACT_SINGLE_CELL_DELTA'):q.verify_matrix_context(self.old,changed,altered)

    def test_crosswalk_cannot_create_grant_or_another_machine(self):
        for field,value,reason in [('authority_granted_by_crosswalk',True,'QUALIFY_BOUND'),('named_bound','UNBOUNDED','QUALIFY_BOUND')]:
            altered=copy.deepcopy(self.crosswalk);altered[field]=value
            with self.assertRaisesRegex(ValueError,reason):q.verify_matrix_context(self.old,self.new,altered)
        altered=copy.deepcopy(self.crosswalk);altered['selected_machine_dimension_rows'][0]['machine']='M12'
        with self.assertRaisesRegex(ValueError,'UNIT_MACHINE_MEMBERSHIP'):q.verify_matrix_context(self.old,self.new,altered)

    def test_m04_row_and_m03_route_b_cannot_be_spliced(self):
        for machine,field,value,reason in [('M04','declared_owner_cells',{'Qualify':'unresolved'},'M04_BOUND'),('M03','required_dimensions_from_candidate_map',['Qualify'],'M03_ROUTE_B_DIMENSIONS')]:
            altered=copy.deepcopy(self.crosswalk)
            row=next(row for row in altered['selected_machine_dimension_rows']if row['machine']==machine);row[field]=value
            with self.assertRaisesRegex(ValueError,reason):q.verify_matrix_context(self.old,self.new,altered)

    def test_wrong_predecessor_and_matrix_identities_rejected(self):
        for field in ('matrix_sha256','predecessor_matrix_sha256'):
            altered=copy.deepcopy(self.crosswalk);altered[field]='0'*64
            with self.assertRaisesRegex(ValueError,'CROSSWALK_MATRIX_IDENTITY'):q.verify_matrix_context(self.old,self.new,altered)

    def test_duplicate_machine_rows_rejected(self):
        altered=copy.deepcopy(self.crosswalk);altered['selected_machine_dimension_rows'].append(copy.deepcopy(altered['selected_machine_dimension_rows'][0]))
        with self.assertRaisesRegex(ValueError,'UNIQUE_MACHINE_ROWS'):q.verify_matrix_context(self.old,self.new,altered)

    def test_owner_and_owner_cells_cannot_be_detached(self):
        for machine,field,value,reason in [('M03','specification_owner','Cortex','MACHINE_OWNER_BINDING'),('M08','owner_is_matrix_organ',False,'MACHINE_OWNER_BINDING'),('M08','declared_owner_cells',{'Observe':'yes','Propose':'yes'},'MACHINE_OWNER_CELL_BINDING'),('M08','required_dimensions_from_candidate_map',['Authorize'],'MACHINE_OWNER_CELL_BINDING')]:
            altered=copy.deepcopy(self.crosswalk)
            row=next(row for row in altered['selected_machine_dimension_rows']if row['machine']==machine);row[field]=value
            with self.assertRaisesRegex(ValueError,reason):q.verify_matrix_context(self.old,self.new,altered)

class CatalogMembershipTests(unittest.TestCase):
    """Controlled temporary catalogs use real captures; no adoption or corpus execution."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=pathlib.Path(self.temp.name)/'unit';shutil.copytree(ROOT,self.root)
        register=json.loads((self.root/'input-register.json').read_bytes())
        source=json.loads((self.root/register['m03_obligations.json']['path']).read_bytes())
        index=next(i for i,row in enumerate(source['machines'])if row['id']=='M03')
        obligation={'status':'PROPOSED_NOT_ADOPTED','scope':'M03_ROW_ONLY_NO_OTHER_MACHINE_ADOPTION','source_obligations_sha256':register['m03_obligations.json']['sha256'],'source_pointer':'/machines/'+str(index),'selected_obligation':source['machines'][index],'runtime_authority':'UNRESOLVED','runtime_activation':False}
        (self.root/'M03-OBLIGATIONS-SELECTION-DRAFT.json').write_text(json.dumps(obligation),encoding='utf-8')
        names={'M04_contract':'M04-S1-QUALIFICATION-DRAFT.md','authority_delta':'AUTHORITY-DELTA-DRAFT.md','authority_matrix':'AUTHORITY-MATRIX-SUCCESSOR-DRAFT.md','authority_crosswalk':'authority-crosswalk-unit-a.json','M03_selection':'M03-FORWARD-SELECTION-DRAFT.json','M03_machine':'inputs/m03/M03.proposal.json','M03_obligations':'M03-OBLIGATIONS-SELECTION-DRAFT.json','M08_selection':'M08-FORWARD-SELECTION-DRAFT.json','M08_machine':'inputs/m08/successor/machines/M08.proposal.json','M08_denial_routing_table':'inputs/m08/successor/m08-denial-routing-table.json','reference':'ingress_review_reference.py'}
        self.catalog=copy.deepcopy(q.CATALOG_SCOPE)
        self.catalog.update(input_register=self.identity('input-register.json'),selected_artifacts={label:self.identity(path)for label,path in names.items()},supporting_artifacts={})

    def identity(self,path):
        raw=(self.root/path).read_bytes();return {'path':path,'bytes':len(raw),'sha256':q.sha(raw)}

    def verify(self):
        raw=(json.dumps(self.catalog,sort_keys=True)+'\n').encode();(self.root/'unit-a-catalog.json').write_bytes(raw)
        return q.verify_catalog(self.root,q.sha(raw))

    def rewrite_selected(self,label,change):
        path=self.catalog['selected_artifacts'][label]['path'];p=self.root/path;doc=json.loads(p.read_bytes());change(doc);p.write_text(json.dumps(doc),encoding='utf-8');self.catalog['selected_artifacts'][label]=self.identity(path)

    def test_positive_closed_catalog(self):
        self.assertEqual(self.verify()[3],[('S1','Qualify','unresolved','bounded')])

    def test_every_catalog_scope_field_rejected_after_repinning(self):
        original=copy.deepcopy(self.catalog)
        changes={'schema':'OTHER','status':'ADOPTED','adoption_record':{},'atomic_adoption':False,'adoption_unit':'All captured machines individually adopted','runtime_activation':True,'canonical_membership':True,'operative_authority':'SATISFIED','production_ready':True,'input_count':100,'exclusions':[],'authority_delta':dict(q.CATALOG_SCOPE['authority_delta'],principal='S2'),'limits':'No limits'}
        for key,value in changes.items():
            self.catalog=copy.deepcopy(original);self.catalog[key]=value
            with self.subTest(field=key),self.assertRaisesRegex(ValueError,'CATALOG_SCOPE:'+key):self.verify()
        self.catalog=original

    def test_unknown_catalog_field_rejected(self):
        self.catalog['runtime_grant']=True
        with self.assertRaisesRegex(ValueError,'CATALOG_FIELD_MEMBERSHIP'):self.verify()

    def test_duplicate_catalog_and_selected_json_keys_rejected(self):
        raw=(json.dumps(self.catalog,sort_keys=True)+'\n').encode();raw=b'{"production_ready":true,'+raw[1:]
        (self.root/'unit-a-catalog.json').write_bytes(raw)
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY:production_ready'):q.verify_catalog(self.root,q.sha(raw))
        path=self.catalog['selected_artifacts']['M03_selection']['path'];p=self.root/path
        original=p.read_bytes();p.write_bytes(b'{"runtime_activation":true,'+original[1:]);self.catalog['selected_artifacts']['M03_selection']=self.identity(path)
        with self.assertRaisesRegex(ValueError,'DUPLICATE_JSON_KEY:runtime_activation'):self.verify()

    def test_exact_input_label_set_and_historical_anchors(self):
        path=self.root/'input-register.json';original=path.read_bytes();register=json.loads(original)
        register['unexpected_input']=register.pop('m03_bindings');path.write_text(json.dumps(register),encoding='utf-8');self.catalog['input_register']=self.identity('input-register.json')
        with self.assertRaisesRegex(ValueError,'EXACT_INPUT_MEMBERSHIP'):self.verify()
        register=json.loads(original);entry=register['m03_bindings'];source=self.root/entry['path'];source.write_bytes(source.read_bytes()+b'\n');entry.update(self.identity(entry['path']));path.write_text(json.dumps(register),encoding='utf-8');self.catalog['input_register']=self.identity('input-register.json')
        with self.assertRaisesRegex(ValueError,'HISTORICAL_PACKAGE_ANCHOR:m03_bindings'):self.verify()

    def test_extra_normative_member_rejected(self):
        self.catalog['selected_artifacts']['M12_machine']=self.catalog['selected_artifacts']['M03_machine']
        with self.assertRaisesRegex(ValueError,'EXACT_SELECTED_MEMBERSHIP'):self.verify()

    def test_machine_substitution_with_consistent_new_pin_rejected(self):
        for machine in ('M03','M08'):
            original=copy.deepcopy(self.catalog)
            name='substituted-'+machine+'.json';(self.root/name).write_bytes(b'{"machine":"substitute"}')
            self.catalog['selected_artifacts'][machine+'_machine']=self.identity(name)
            with self.assertRaisesRegex(ValueError,'SELECTED_MACHINE_SUBSTITUTION'):self.verify()
            self.catalog=original

    def test_selection_descriptor_drift_rejected(self):
        self.rewrite_selected('M03_selection',lambda doc:doc['selected_artifact'].update(bytes=1))
        with self.assertRaisesRegex(ValueError,'SELECTED_MACHINE_SUBSTITUTION'):self.verify()

    def test_routing_table_substitution_with_new_pin_rejected(self):
        name='substituted-routing.json';(self.root/name).write_bytes(b'{"rows":[]}')
        self.catalog['selected_artifacts']['M08_denial_routing_table']=self.identity(name)
        with self.assertRaisesRegex(ValueError,'M08_ROUTING_TABLE_SUBSTITUTION'):self.verify()

    def test_routing_descriptor_and_scope_cannot_escalate(self):
        label='M08_selection';path=self.catalog['selected_artifacts'][label]['path'];original=(self.root/path).read_bytes()
        for field,value,reason in [('sha256','0'*64,'M08_ROUTING_TABLE_SUBSTITUTION'),('rows',719,'M08_ROUTING_TABLE_CARDINALITY'),('unit_a_scope_input','SATISFIED','M08_ROUTING_TABLE_SCOPE'),('allowed_fixture_finding_is_not_operative_permission',False,'M08_ROUTING_TABLE_SCOPE')]:
            (self.root/path).write_bytes(original)
            self.rewrite_selected(label,lambda doc:doc['selected_denial_routing_table'].update({field:value}))
            with self.assertRaisesRegex(ValueError,reason):self.verify()

    def test_obligation_pointer_row_and_scope_rejected(self):
        label='M03_obligations';path=self.catalog['selected_artifacts'][label]['path'];original=(self.root/path).read_bytes()
        for field,value,reason in [('source_pointer','/machines/1','M03_OBLIGATION_SUBSTITUTION'),('selected_obligation',{'id':'M12'},'M03_OBLIGATION_SUBSTITUTION'),('source_obligations_sha256','0'*64,'M03_OBLIGATION_SUBSTITUTION'),('runtime_activation',True,'M03_OBLIGATION_SCOPE'),('scope','ALL_MACHINES','M03_OBLIGATION_SCOPE')]:
            (self.root/path).write_bytes(original);self.rewrite_selected(label,lambda doc:doc.update({field:value}))
            with self.assertRaisesRegex(ValueError,reason):self.verify()

    def test_detached_procedure_or_baseline_retention_rejected(self):
        register_path=self.root/'input-register.json';original=register_path.read_bytes()
        for label in ('accepted_procedure','procedure_acceptance','baseline_retention'):
            register=json.loads(original);path=register[label]['path'];saved=(self.root/path).read_bytes();(self.root/path).write_bytes(saved+b'\n')
            register[label].update(self.identity(path));register_path.write_text(json.dumps(register),encoding='utf-8');self.catalog['input_register']=self.identity('input-register.json')
            with self.assertRaisesRegex(ValueError,'ADOPTION_PREDECESSOR_DRIFT:'+label):self.verify()
            (self.root/path).write_bytes(saved);register_path.write_bytes(original);self.catalog['input_register']=self.identity('input-register.json')

class RoutingSourceCorrespondenceTests(unittest.TestCase):
    def setUp(self):
        self.raw=(ROOT/'inputs/m08/successor/m08-denial-routing-table.json').read_bytes()
        self.m08=q.captured_module('custody_test_captured_m08',(ROOT/'inputs/code/m08.py').read_bytes(),ROOT/'inputs/code/m08.py')

    def test_all_720_actual_source_cases(self):
        self.assertEqual(q.verify_routing_table(self.raw,self.m08),720)

    def test_duplicate_case_and_false_expected_finding_rejected(self):
        table=json.loads(self.raw);table['rows'][-1]=copy.deepcopy(table['rows'][0])
        with self.assertRaisesRegex(ValueError,'M08_ROUTING_CASE_MEMBERSHIP'):q.verify_routing_table(json.dumps(table).encode(),self.m08)
        table=json.loads(self.raw);table['rows'][0]['expected']['ordinary_access']='CLOSED'
        with self.assertRaisesRegex(ValueError,'M08_ROUTING_SOURCE_MISMATCH'):q.verify_routing_table(json.dumps(table).encode(),self.m08)

    def test_implementation_route_drift_rejected(self):
        original=self.m08.atlas_denial_route
        def drift(*args):
            value=original(*args);value['target_state']='CANONICAL';return value
        self.m08.atlas_denial_route=drift
        with self.assertRaisesRegex(ValueError,'M08_ROUTING_SOURCE_MISMATCH'):q.verify_routing_table(self.raw,self.m08)

if __name__=='__main__':unittest.main()
