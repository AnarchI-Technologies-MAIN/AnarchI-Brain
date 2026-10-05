"""Pinned documentary Unit B qualification; confers no operative authority."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath

SELECTED_PATHS = {
    'bootstrap_contract': 'contracts/BOOTSTRAP-DRAFT.md',
    'principal_contract': 'contracts/PRINCIPAL-INDEPENDENCE-DRAFT.md',
    'key_binding_contract': 'contracts/KEY-CUSTODY-INTERFACE-DRAFT.md',
    'evaluation_contract': 'contracts/GRANT-EVALUATION-DRAFT.md',
    'M09_contract': 'contracts/M09-CONSUMPTION-DRAFT.md',
    'M09_reconciliation': 'contracts/M09-RECONCILIATION-DRAFT.json',
    'M12_selection': 'contracts/M12-SELECTION-DRAFT.json',
    'M14_interface': 'contracts/M14-RECORDING-INTERFACE-DRAFT.md',
    'authority_matrix': 'inputs/unit_a_matrix.md',
    'unchanged_matrix_proof': 'contracts/UNCHANGED-MATRIX-PROOF-DRAFT.json',
    'authority_crosswalk': 'contracts/AUTHORITY-CROSSWALK-UNIT-B-DRAFT.json',
    'grant_schema': 'schemas/AUTHORITY-GRANT-v2.schema.json',
    'authorization_schema': 'schemas/AUTHORIZATION-v1.schema.json',
    'fixture_schema': 'schemas/AUTHORITY-FIXTURE-v1.schema.json',
    'interface_inventory': 'reference/API-INVENTORY.json',
    'reference': 'reference/authority_reference.py',
}
FALSE_FLAGS = ('runtime_authority', 'operative_grant', 'effect_permitted',
               'durable_consumption', 'canonical_membership', 'production_ready')
PREDECESSORS = {
    'baseline_catalog_sha256': '421b5d5bab28a32afe557e17970a14beb75a99eddc9f536a75bb1bcda9d26eb3',
    'mapping_contract_sha256': '61411344381e31149a1b652a34e75f65438a4e18c98970115454ab3ad785d9a4',
    'unit_a_catalog_sha256': '7db495b0a1034c9211c3d08c90569c3b0bccc3209a31f9f9e1885889b99b75c3',
    'unit_a_acceptance_sha256': '79d46e4c1a41c48bcca88a04c42cc2b08068134c971df456a7a59f0aff0d8d1c',
    'unit_a_retention_sha256': 'fc95e1f43f40dc576ab7295435bad3effd8ad99e6fc8be4f9263e8d55154a155',
    'unit_a_effective_not_before_utc': '2026-10-04T22:28:23Z',
}
EXCLUSIONS = ['actual bootstrap root selection', 'runtime enrollment',
              'grant issuance', 'root replacement', 'delegation',
              'actual cryptographic authentication', 'M14 implementation',
              'durable effect execution', 'S2 canonical adjudication',
              'canonical commit', 'staging', 'deployment']
ADOPTION_UNIT = ('All sixteen selected artifacts atomically or none. Documentary '
                 'authority interpretation and non-effecting external-authorization '
                 'consumption fixture foundation only.')
MAX_SOURCE_BYTES = 2 * 1024 * 1024


def bounded_read(path):
    if not path.is_file() or not 0 < path.stat().st_size <= MAX_SOURCE_BYTES:
        raise ValueError('SOURCE_RESOURCE_BOUND')
    with path.open('rb') as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise ValueError('SOURCE_RESOURCE_BOUND')
    return raw


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('DUPLICATE_JSON_FIELD:' + key)
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError('NONFINITE_JSON:' + value)

    if type(raw) is not bytes or len(raw) > 2 * 1024 * 1024:
        raise ValueError('JSON_BYTE_LIMIT')
    return json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=pairs,
                      parse_constant=nonfinite)


def read_descriptor(unit, descriptor, expected_path):
    if type(descriptor) is not dict or set(descriptor) != {'path', 'bytes', 'sha256'}:
        raise ValueError('DESCRIPTOR_SCHEMA')
    if descriptor['path'] != expected_path:
        raise ValueError('DESCRIPTOR_PATH')
    path = PurePosixPath(expected_path)
    if path.is_absolute() or '..' in path.parts or '\\' in expected_path:
        raise ValueError('UNSAFE_PATH')
    local = unit / expected_path
    if not local.resolve().is_relative_to(unit.resolve()):
        raise ValueError('PATH_ESCAPE')
    if type(descriptor['bytes']) is not int or descriptor['bytes'] < 0:
        raise ValueError('DESCRIPTOR_LENGTH')
    raw = bounded_read(local)
    if len(raw) != descriptor['bytes'] or hashlib.sha256(raw).hexdigest() != descriptor['sha256']:
        raise ValueError('BOUND_BYTES_DRIFT:' + expected_path)
    return raw


def qualify_catalog(unit, expected_sha256):
    raw = bounded_read(unit / 'unit-b-catalog.json')
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('CATALOG_DIGEST_MISMATCH')
    catalog = strict_json(raw)
    expected_fields = {'schema', 'status', 'adoption_record', 'atomic_adoption',
                       'adoption_unit', 'selected_artifacts', 'input_registers',
                       'predecessors', 'matrix_cell_changes', 'S3_Authorize',
                       'supporting_artifacts',
                       'profile', 'exclusions', *FALSE_FLAGS}
    if type(catalog) is not dict or set(catalog) != expected_fields:
        raise ValueError('CATALOG_FIELDSET')
    for key in FALSE_FLAGS:
        if catalog[key] is not False:
            raise ValueError('OPERATIVE_FLAG:' + key)
    if (catalog['schema'] != 'PROPOSED-AUTHORITY-INTERPRETATION-CONSUMPTION-UNIT-B-1'
            or catalog['status'] != 'PROPOSED_NOT_ADOPTED'
            or catalog['adoption_record'] is not None
            or catalog['atomic_adoption'] is not True
            or catalog['profile'] != 'OFFLINE_FIXTURE_ONLY'
            or catalog['matrix_cell_changes'] != []
            or catalog['S3_Authorize'] != 'UNRESOLVED'
            or catalog['predecessors'] != PREDECESSORS
            or catalog['exclusions'] != EXCLUSIONS
            or catalog['adoption_unit'] != ADOPTION_UNIT):
        raise ValueError('CATALOG_SCOPE')
    members = catalog['selected_artifacts']
    if type(members) is not dict or set(members) != set(SELECTED_PATHS):
        raise ValueError('ATOMIC_MEMBER_SET')
    buffers = {label: read_descriptor(unit, members[label], path)
               for label, path in SELECTED_PATHS.items()}
    register_paths = {'input-register.json', 'chain-supplement-register.json',
                      'custody/matrix-support-register.json'}
    if set(catalog['input_registers']) != register_paths:
        raise ValueError('INPUT_REGISTER_SET')
    for path in sorted(register_paths):
        read_descriptor(unit, catalog['input_registers'][path], path)
    support_paths = {'custody/qualify_custody.py',
                     'custody/expected-capture-identities.json',
                     'custody/test_custody.py', 'qualify_unit_b.py', 'test_catalog.py',
                     'reference/fixture_factory.py', 'reference/test_authority_reference.py',
                     'inputs/lyra_authorization_repair.txt', 'DIRECTION-APPROVAL.json',
                     'SUCCESSOR-CUSTODY-NOTE.json', 'TEST-STRENGTHENING-SUCCESSOR-NOTE.json',
                     'REVIEW-EXCERPT-PROVENANCE.json'}
    if set(catalog['supporting_artifacts']) != support_paths:
        raise ValueError('SUPPORT_MEMBER_SET')
    for path in sorted(support_paths):
        read_descriptor(unit, catalog['supporting_artifacts'][path], path)
    return catalog, buffers


def verify_reference_inventory(buffers):
    inventory = strict_json(buffers['interface_inventory'])
    limits = inventory['limits']
    text = {'type': 'string', 'minLength': 1, 'maxLength': limits['text_chars']}
    digest = {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}
    integer = {'type': 'integer', 'minimum': 0, 'maximum': limits['integer_max']}
    properties = {
        'text': text, 'digest': digest, 'bool': {'type': 'boolean'},
        'description': {'type': 'string', 'minLength': 1,
                        'maxLength': limits['description_chars']},
        'nonnegative_int': integer, 'positive_int': dict(integer, minimum=1),
        'nullable_int': {'anyOf': [integer, {'type': 'null'}]},
        'nullable_text': {'anyOf': [text, {'type': 'null'}]},
        'nullable_digest': {'anyOf': [digest, {'type': 'null'}]},
        'digest_or_none_tag': {'anyOf': [digest, {'const': 'NONE'}]},
        'texts': {'type': 'array', 'items': text, 'maxItems': limits['list_items'],
                  'uniqueItems': True},
        'lineage': {'type': 'array', 'minItems': 1,
                    'maxItems': limits['lineage_items'],
                    'items': {'$ref': '#/$defs/lineage_entry'}},
        'denials': {'type': 'array', 'maxItems': limits['list_items'],
                    'items': {'$ref': '#/$defs/denial'}},
    }
    properties.update({name: {'type': 'string', 'enum': values}
                       for name, values in inventory['enums'].items()})
    properties.update({name: {'$ref': '#/$defs/' + name}
                       for name in inventory['objects']})
    tree = ast.parse(buffers['reference'].decode('utf-8'))
    matches = [node for node in tree.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == 'SPEC'
                       for target in node.targets)]
    if len(matches) != 1:
        raise ValueError('REFERENCE_SPEC_IDENTITY')
    expression = matches[0].value
    if (not isinstance(expression, ast.Call) or len(expression.args) != 1
            or expression.keywords or not isinstance(expression.func, ast.Attribute)
            or not isinstance(expression.func.value, ast.Name)
            or expression.func.value.id != 'json' or expression.func.attr != 'loads'):
        raise ValueError('REFERENCE_SPEC_EXPRESSION')
    literal = ast.literal_eval(expression.args[0])
    if type(literal) is not str or strict_json(literal.encode('utf-8')) != inventory:
        raise ValueError('REFERENCE_INVENTORY_DRIFT')
    for label, model in [('grant_schema', 'grant'),
                         ('authorization_schema', 'authorization'),
                         ('fixture_schema', 'bundle')]:
        schema = strict_json(buffers[label])
        if (schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema'
                or schema.get('$ref') != '#/$defs/' + model
                or set(schema['$defs']) != set(inventory['objects'])):
            raise ValueError('SCHEMA_MODEL_IDENTITY:' + label)
        for name, fields in inventory['objects'].items():
            definition = schema['$defs'][name]
            if (set(definition) != {'type', 'additionalProperties', 'required', 'properties'}
                    or definition['type'] != 'object'
                    or definition['additionalProperties'] is not False
                    or definition['required'] != sorted(fields)
                    or definition['properties'] != {
                        field: properties[kind] for field, kind in fields.items()}):
                raise ValueError('SCHEMA_CLOSED_COORDINATES:' + name)
    return {'grant_coordinates': len(inventory['objects']['grant']),
            'request_coordinates': len(inventory['objects']['requested_effect']),
            'embedded_reference_inventory_identical': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--catalog-sha256', required=True)
    arguments = parser.parse_args()
    catalog, buffers = qualify_catalog(arguments.unit, arguments.catalog_sha256)
    inventory_result = verify_reference_inventory(buffers)
    source_path = 'custody/qualify_custody.py'
    source = read_descriptor(arguments.unit,
                             catalog['supporting_artifacts'][source_path], source_path)
    namespace = {'__name__': 'unit_b_pinned_custody',
                 '__file__': str(arguments.unit / source_path)}
    # Trusted first-party code is compiled only after independent catalog pin and
    # exact support-byte verification. This is not hostile-code containment.
    exec(compile(source, str(arguments.unit / source_path), 'exec'), namespace)
    custody = namespace['qualify_predecessors'](arguments.unit)
    by_path = {SELECTED_PATHS[label]: raw for label, raw in buffers.items()}
    for path, checked in custody['checked_draft_documents'].items():
        raw = by_path[path]
        if checked != {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}:
            raise ValueError('CUSTODY_READ_BUFFER_DRIFT:' + path)
    result = {'result': 'PINNED_DOCUMENTARY_CUSTODY_VERIFIED',
              'catalog_sha256': arguments.catalog_sha256,
              'selected_artifacts': len(buffers), 'runtime_authority': False,
              'operative_grant': False, 'effect_permitted': False,
              'durable_consumption': False, 'production_ready': False,
              'prerequisite_chain_qualified': True,
              'custody': custody,
              'reference_inventory': inventory_result,
              'execution_qualified': False,
              'notice': 'Documentary source/custody qualification only. Reference '
                        'execution qualification is separately required; no '
                        'operative authority or actual bootstrap enrollment.'}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
