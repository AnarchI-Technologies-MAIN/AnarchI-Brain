"""Repinned-catalog attacks against atomic scope and schema consistency."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from qualify_unit_b import qualify_catalog, verify_reference_inventory

ROOT = Path(__file__).resolve().parent


class CatalogAttacks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.unit = Path(self.temporary.name) / 'unit'
        shutil.copytree(ROOT, self.unit, ignore=shutil.ignore_patterns('__pycache__'))
        self.catalog = json.loads((self.unit / 'unit-b-catalog.json').read_bytes())

    def repin(self):
        raw = (json.dumps(self.catalog, sort_keys=True, indent=2) + '\n').encode()
        (self.unit / 'unit-b-catalog.json').write_bytes(raw)
        return hashlib.sha256(raw).hexdigest()

    def mutate_schema(self, action):
        descriptor = self.catalog['selected_artifacts']['grant_schema']
        path = self.unit / descriptor['path']
        schema = json.loads(path.read_bytes())
        action(schema)
        raw = json.dumps(schema, sort_keys=True).encode()
        path.write_bytes(raw)
        descriptor.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        catalog, buffers = qualify_catalog(self.unit, self.repin())
        with self.assertRaisesRegex(ValueError, 'SCHEMA_CLOSED_COORDINATES'):
            verify_reference_inventory(buffers)

    def test_actual_candidate_consistency(self):
        catalog, buffers = qualify_catalog(self.unit, self.repin())
        result = verify_reference_inventory(buffers)
        self.assertTrue(result['embedded_reference_inventory_identical'])

    def test_repin_cannot_enable_runtime_authority(self):
        self.catalog['runtime_authority'] = True
        with self.assertRaisesRegex(ValueError, 'OPERATIVE_FLAG'):
            qualify_catalog(self.unit, self.repin())

    def test_repin_cannot_adopt_subset(self):
        del self.catalog['selected_artifacts']['M09_contract']
        with self.assertRaisesRegex(ValueError, 'ATOMIC_MEMBER_SET'):
            qualify_catalog(self.unit, self.repin())

    def test_repin_cannot_add_descriptor_extension(self):
        self.catalog['selected_artifacts']['reference']['override'] = True
        with self.assertRaisesRegex(ValueError, 'DESCRIPTOR_SCHEMA'):
            qualify_catalog(self.unit, self.repin())

    def test_repin_schema_cannot_widen_operation_enum(self):
        def mutate(schema):
            schema['$defs']['grant']['properties']['operation']['enum'].append('EXECUTE_ANYTHING')
        self.mutate_schema(mutate)

    def test_repin_schema_cannot_change_subject_version_type(self):
        def mutate(schema):
            schema['$defs']['grant']['properties']['subject_version'] = {'type': 'string'}
        self.mutate_schema(mutate)

    def test_repin_schema_cannot_remove_integer_bound(self):
        def mutate(schema):
            del schema['$defs']['grant']['properties']['generation']['maximum']
        self.mutate_schema(mutate)

    def test_repin_schema_cannot_make_scope_optional(self):
        def mutate(schema):
            schema['$defs']['grant']['required'].remove('tenant')
        self.mutate_schema(mutate)


if __name__ == '__main__':
    unittest.main()
