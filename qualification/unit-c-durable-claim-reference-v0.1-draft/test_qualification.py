"""Custody regressions for the proposed Unit C schema package."""

import shutil
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import qualify_unit_c
import unit_canonical


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[1]


class UnitCPackageQualificationTests(unittest.TestCase):
    def setUp(self):
        self.manifest_pin = os.environ["UNIT_C_MANIFEST_SHA256"]

    def test_pinned_package_passes_only_source_and_schema_scope(self):
        result = qualify_unit_c.verify(PACKAGE, REPO, self.manifest_pin)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["contract_order"], "UNRESOLVED")
        self.assertFalse(result["runtime_authority"])
        self.assertFalse(result["effect_permitted"])
        self.assertFalse(result["durable_consumption"])
        self.assertFalse(result["production_ready"])

    def test_manifest_digest_is_an_external_input(self):
        with self.assertRaisesRegex(qualify_unit_c.QualificationError, "SOURCE_DIGEST_MISMATCH:candidate-manifest.json"):
            qualify_unit_c.verify(PACKAGE, REPO, "0" * 64)

    def test_implementation_work_order_holds_lifecycle_until_order_is_adopted(self):
        work_order = (PACKAGE / "IMPLEMENTATION-WORK-ORDER-DRAFT.md").read_text(encoding="utf-8")
        self.assertIn("HOLD lifecycle composition until the ordering decision", work_order)
        self.assertIn("do not implement a fence/claim/recheck/target transition sequence", work_order)
        self.assertIn("while ordering is unresolved, no lifecycle transition sequence", work_order)
        self.assertNotIn("durable one-shot claim -> fresh post-claim recheck", work_order)

    def test_unmanifested_package_files_and_directories_are_rejected(self):
        for relative in ("unlisted.json", "nested/unlisted.json"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                copy = Path(temporary) / "package"
                shutil.copytree(PACKAGE, copy)
                extra = copy / relative
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_text("{}", encoding="utf-8")
                with self.assertRaisesRegex(
                    qualify_unit_c.QualificationError, "PACKAGE_CONTENT_SET_MISMATCH"
                ):
                    qualify_unit_c.verify(copy, REPO, self.manifest_pin)

    def test_closed_schema_walk_rejects_open_subschemas_in_2020_12_locations(self):
        nested_schemas = {
            keyword: {keyword: {"nested": {"type": "object"}}}
            for keyword in qualify_unit_c.SCHEMA_MAP_KEYWORDS
        }
        nested_schemas.update({
            keyword: {keyword: [{"type": "object"}]}
            for keyword in qualify_unit_c.SCHEMA_ARRAY_KEYWORDS
        })
        nested_schemas.update({
            keyword: {keyword: {"type": "object"}}
            for keyword in qualify_unit_c.SCHEMA_SINGLE_KEYWORDS
        })
        for keyword, nested in nested_schemas.items():
            with self.subTest(keyword=keyword):
                schema = dict(nested)
                with self.assertRaisesRegex(
                    qualify_unit_c.QualificationError, "OPEN_OBJECT_SCHEMA"
                ):
                    qualify_unit_c._check_closed_schema(schema)

    def test_local_ref_to_open_definition_is_rejected(self):
        schema = {
            "type": "object",
            "additionalProperties": False,
            "$defs": {"open": {"type": "object"}},
            "properties": {"value": {"$ref": "#/$defs/open"}},
        }
        with self.assertRaisesRegex(
            qualify_unit_c.QualificationError, r"OPEN_OBJECT_SCHEMA:\$\.\$defs\.open"
        ):
            qualify_unit_c._check_closed_schema(schema)

    def test_type_union_including_object_must_be_closed(self):
        schema = {"type": ["object", "null"]}
        with self.assertRaisesRegex(
            qualify_unit_c.QualificationError, "OPEN_OBJECT_SCHEMA"
        ):
            qualify_unit_c._check_closed_schema(schema)

    def test_digest_schemas_reject_trailing_newline_and_require_exact_length(self):
        def digest_schemas(value):
            if isinstance(value, dict):
                if value.get("pattern") == "^[0-9a-f]{64}$":
                    yield value
                for child in value.values():
                    yield from digest_schemas(child)
            elif isinstance(value, list):
                for child in value:
                    yield from digest_schemas(child)

        checked = 0
        for filename in qualify_unit_c.SCHEMA_FILES:
            schema = qualify_unit_c._read_json(PACKAGE / filename)
            for digest_schema in digest_schemas(schema):
                with self.subTest(filename=filename, schema=digest_schema):
                    self.assertEqual(digest_schema.get("minLength"), 64)
                    self.assertEqual(digest_schema.get("maxLength"), 64)
                    validator = qualify_unit_c.Draft202012Validator(digest_schema)
                    self.assertTrue(validator.is_valid("a" * 64))
                    self.assertFalse(validator.is_valid("a" * 64 + "\n"))
                checked += 1
        self.assertGreater(checked, 0)

    def test_changed_schema_bytes_fail_against_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "package"
            shutil.copytree(PACKAGE, copy)
            schema_path = copy / "target-evidence-draft.schema.json"
            schema_path.write_bytes(schema_path.read_bytes() + b" ")
            with self.assertRaisesRegex(qualify_unit_c.QualificationError, "SOURCE_DIGEST_MISMATCH:target-evidence-draft.schema.json"):
                qualify_unit_c.verify(copy, REPO, self.manifest_pin)


class CanonicalJSONTests(unittest.TestCase):
    def test_canonical_bytes_are_stable_and_utf8(self):
        value = {"é": 1, "a": True}
        self.assertEqual(unit_canonical.canonical_bytes(value), b'{"a":true,"\xc3\xa9":1}')
        self.assertEqual(unit_canonical.parse_bytes(b'{"a":true,"\\u00e9":1}'), value)

    def test_decoder_rejects_ambiguous_or_unsupported_number_encodings(self):
        for raw in (b'{"a":1,"a":2}', b'{"x":1.0}', b'{"x":NaN}', b'"\\ud800"'):
            with self.subTest(raw=raw), self.assertRaises(unit_canonical.CanonicalJSONError):
                unit_canonical.parse_bytes(raw)
        self.assertIs(unit_canonical.parse_bytes(b"true"), True)

    def test_serializer_rejects_unsupported_python_shapes(self):
        for value in ({1: "x"}, {"x": 1.0}, (1, 2), 2**63):
            with self.subTest(value=type(value).__name__), self.assertRaises(unit_canonical.CanonicalJSONError):
                unit_canonical.canonical_bytes(value)
        cyclic = []
        cyclic.append(cyclic)
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "CYCLIC_VALUE"):
            unit_canonical.canonical_bytes(cyclic)

    def test_depth_node_and_raw_size_limits_fail_closed(self):
        deep = None
        for _ in range(unit_canonical.MAX_DEPTH + 1):
            deep = [deep]
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "DEPTH_LIMIT_EXCEEDED"):
            unit_canonical.canonical_bytes(deep)
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "NODE_LIMIT_EXCEEDED"):
            unit_canonical.canonical_bytes([None] * unit_canonical.MAX_NODES)
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "RAW_INPUT_TOO_LARGE"):
            unit_canonical.parse_bytes(b'"' + b"a" * unit_canonical.MAX_RAW_BYTES + b'"')
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "CANONICAL_BYTES_LIMIT_EXCEEDED"):
            unit_canonical.canonical_bytes({"x": "a" * unit_canonical.MAX_RAW_BYTES})

    def test_aggregate_string_size_is_rejected_before_json_encoding(self):
        value = ["a" * (unit_canonical.MAX_RAW_BYTES // 2)] * 2
        with patch.object(
            unit_canonical.json.JSONEncoder,
            "iterencode",
            side_effect=AssertionError("encoder must not materialize oversized strings"),
        ):
            with self.assertRaisesRegex(
                unit_canonical.CanonicalJSONError, "CANONICAL_BYTES_LIMIT_EXCEEDED"
            ):
                unit_canonical.canonical_bytes(value)

    def test_incremental_encoder_stops_at_output_limit(self):
        continued = []

        def chunks(_encoder, _value):
            yield "x" * unit_canonical.MAX_RAW_BYTES
            yield "y"
            continued.append(True)
            yield "z"

        with patch.object(unit_canonical.json.JSONEncoder, "iterencode", chunks):
            with self.assertRaisesRegex(
                unit_canonical.CanonicalJSONError, "CANONICAL_BYTES_LIMIT_EXCEEDED"
            ):
                unit_canonical.canonical_bytes(None)
        self.assertEqual(continued, [])

    def test_digest_domains_are_separated_and_closed(self):
        binding = unit_canonical.digest_object("UNIT-C:BINDING:v1", {"x": 1})
        event = unit_canonical.digest_object("UNIT-C:EVENT:v1", {"x": 1})
        self.assertNotEqual(binding, event)
        with self.assertRaisesRegex(unit_canonical.CanonicalJSONError, "INVALID_DIGEST_DOMAIN"):
            unit_canonical.digest_object("UNIT-C:OTHER:v1", {"x": 1})


if __name__ == "__main__":
    unittest.main()
