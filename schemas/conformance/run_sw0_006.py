import argparse
import copy
import hashlib
import json
import pathlib
import sys

from collections import defaultdict
from jsonschema import Draft202012Validator

REPO = pathlib.Path(__file__).resolve().parents[2]
RUNNER = pathlib.Path(__file__).resolve()

CONTRACT = REPO / "schemas" / "CORE-SCHEMA-CONTRACT.md"
REGISTRY_PATH = REPO / "schemas" / "registry.v1.json"
CASES_PATH = REPO / "schemas" / "conformance" / "cases.v1.json"
POSITIVE_DIR = REPO / "schemas" / "conformance" / "positive"

DIALECT = "https://json-schema.org/draft/2020-12/schema"

EXPECTED_ASSERTION_PLAN = {
    "acs1_document_boundary": 18,
    "acs1_key_order": 18,
    "acs1_no_bom": 18,
    "acs1_parse_reserialize": 18,
    "acs1_repeat": 18,
    "authority_dimension_invalid": 1,
    "authority_dimension_valid": 12,
    "authorization_omission": 5,
    "closed_root": 18,
    "contradictory_identity": 2,
    "corpus_contract_digest": 1,
    "corpus_registry_digest": 1,
    "corpus_runner_digest": 1,
    "cross_schema": 306,
    "crypto_uniformity": 90,
    "dialect": 18,
    "fixture_digest": 18,
    "fixture_inventory": 1,
    "meta_schema": 18,
    "missing_reserved": 54,
    "optional_null": 9,
    "positive": 18,
    "receipt_confusion": 20,
    "receipt_inventory": 1,
    "registry": 3,
    "registry_digest": 18,
    "relationship": 2,
    "required_null": 37,
    "resolver_positive": 18,
    "resolver_unresolved": 4,
    "schema_artifact": 2,
    "unknown_field": 18,
    "wrong_profile": 18,
    "wrong_schema_id": 18,
    "wrong_schema_version": 18,
}

EXPECTED_ASSERTIONS = 840

FIXTURE_NAMES = {
    "anarchi.brain.observation":
        "observation.v1.fixture.json",
    "anarchi.brain.validation-result":
        "validation-result.v1.fixture.json",
    "anarchi.brain.qualification-result":
        "qualification-result.v1.fixture.json",
    "anarchi.brain.attestation":
        "attestation.v1.fixture.json",
    "anarchi.brain.proposal":
        "proposal.v1.fixture.json",
    "anarchi.brain.relationship":
        "relationship.v1.fixture.json",
    "anarchi.brain.authority-grant":
        "authority-grant.v1.fixture.json",
    "anarchi.brain.authorization":
        "authorization.v1.fixture.json",
    "anarchi.brain.capability":
        "capability.v1.fixture.json",
    "anarchi.brain.schema":
        "schema.v1.fixture.json",
    "anarchi.brain.policy-root":
        "policy-root.v1.fixture.json",
    "anarchi.brain.projection":
        "projection.v1.fixture.json",
    "anarchi.brain.integrity-epoch-record":
        "integrity-epoch-record.v1.fixture.json",
    "anarchi.brain.receipt.event":
        "receipt.event.v1.fixture.json",
    "anarchi.brain.receipt.decision":
        "receipt.decision.v1.fixture.json",
    "anarchi.brain.receipt.attempt":
        "receipt.attempt.v1.fixture.json",
    "anarchi.brain.receipt.transition":
        "receipt.transition.v1.fixture.json",
    "anarchi.brain.receipt.effect":
        "receipt.effect.v1.fixture.json",
}

POSITIVE = {
    "anarchi.brain.observation": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.observation",
        "schema_version": "1",
        "source": "source:test",
        "observation": {"value": "observed"},
    },
    "anarchi.brain.validation-result": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.validation-result",
        "schema_version": "1",
        "subject": "artifact:test",
        "validation_contract": "validation:test",
        "result": "PASS",
    },
    "anarchi.brain.qualification-result": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.qualification-result",
        "schema_version": "1",
        "subject": "artifact:test",
        "qualification_contract": "qualification:test",
        "result": "PASS",
    },
    "anarchi.brain.attestation": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.attestation",
        "schema_version": "1",
        "source": "source:test",
        "assertion": "bounded assertion",
    },
    "anarchi.brain.proposal": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.proposal",
        "schema_version": "1",
        "proposal": {"operation": "test"},
    },
    "anarchi.brain.relationship": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.relationship",
        "schema_version": "1",
        "subjects": ["subject:a", "subject:b"],
        "relationship": "related-to",
    },
    "anarchi.brain.authority-grant": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.authority-grant",
        "schema_version": "1",
        "grantee": "principal:test",
        "authority_dimension": "Observe",
        "authority_root": "authority-root:test",
    },
    "anarchi.brain.authorization": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.authorization",
        "schema_version": "1",
        "operation": "operation:test",
        "scope": "scope:test",
        "subject": "subject:test",
        "authority_source": "authority:test",
        "conditions": {"mode": "bounded"},
    },
    "anarchi.brain.capability": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.capability",
        "schema_version": "1",
        "operation": "operation:test",
        "means": "means:test",
    },
    "anarchi.brain.schema": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.schema",
        "schema_version": "1",
        "governed_schema_id": "example.schema",
        "governed_schema_version": "1",
        "schema_definition": {"rule": "test"},
    },
    "anarchi.brain.policy-root": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.policy-root",
        "schema_version": "1",
        "policy_root": "policy-root:test",
        "policy": {"rule": "bounded"},
    },
    "anarchi.brain.projection": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.projection",
        "schema_version": "1",
        "source": "artifact:test",
        "projection": {"view": "test"},
    },
    "anarchi.brain.integrity-epoch-record": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.integrity-epoch-record",
        "schema_version": "1",
        "epoch": "epoch:test",
        "record": {"event": "test"},
    },
    "anarchi.brain.receipt.event": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.receipt.event",
        "schema_version": "1",
        "event": {"event": "test"},
    },
    "anarchi.brain.receipt.decision": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.receipt.decision",
        "schema_version": "1",
        "decision": {"decision": "test"},
    },
    "anarchi.brain.receipt.attempt": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.receipt.attempt",
        "schema_version": "1",
        "attempt": {"attempt": "test"},
    },
    "anarchi.brain.receipt.transition": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.receipt.transition",
        "schema_version": "1",
        "transition": {"transition": "test"},
    },
    "anarchi.brain.receipt.effect": {
        "serialization_profile": "ACS-1",
        "schema_id": "anarchi.brain.receipt.effect",
        "schema_version": "1",
        "effect": {"effect": "test"},
    },
}


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    text = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"

    path.write_text(
        text,
        encoding="utf-8",
        newline="\n",
    )


def acs1_string(value):
    for char in value:
        code = ord(char)
        if 0xD800 <= code <= 0xDFFF:
            raise ValueError("ACS1_UNPAIRED_SURROGATE")

    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def acs1_encode(value):
    if value is None:
        return b"null"

    if type(value) is bool:
        return b"true" if value else b"false"

    if type(value) is int:
        return str(value).encode("ascii")

    if type(value) is float:
        raise ValueError("ACS1_NATIVE_FLOAT_FORBIDDEN")

    if isinstance(value, str):
        return acs1_string(value)

    if isinstance(value, list):
        return (
            b"["
            + b",".join(acs1_encode(item) for item in value)
            + b"]"
        )

    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise ValueError("ACS1_NON_STRING_KEY")

        items = sorted(
            value.items(),
            key=lambda item: item[0].encode("utf-8"),
        )

        encoded = []

        for key, item in items:
            encoded.append(
                acs1_string(key)
                + b":"
                + acs1_encode(item)
            )

        return b"{" + b",".join(encoded) + b"}"

    raise ValueError(
        "ACS1_UNSUPPORTED_VALUE:"
        + type(value).__name__
    )


def materialize():
    POSITIVE_DIR.mkdir(
        parents=True,
        exist_ok=False,
    )

    fixture_entries = []

    for schema_id in sorted(POSITIVE):
        name = FIXTURE_NAMES[schema_id]
        path = POSITIVE_DIR / name

        write_json(
            path,
            POSITIVE[schema_id],
        )

        fixture_entries.append({
            "schema_id": schema_id,
            "fixture_path":
                path.relative_to(REPO).as_posix(),
            "fixture_sha256":
                sha256_file(path),
        })

    cases = {
        "contract": "SW0-006",
        "corpus_version": "1",
        "schema_count": 18,
        "positive_fixture_count": 18,
        "expected_assertions": EXPECTED_ASSERTIONS,
        "crypto_enabled_root_schemas": [],
        "contract_sha256":
            sha256_file(CONTRACT),
        "registry_sha256":
            sha256_file(REGISTRY_PATH),
        "runner_sha256":
            sha256_file(RUNNER),
        "runner_path":
            RUNNER.relative_to(REPO).as_posix(),
        "assertion_plan":
            EXPECTED_ASSERTION_PLAN,
        "negative_fixture_strategy":
            "deterministic mutations of persisted positive fixtures",
        "acs1_fixture_rule":
            "persisted fixture files are transport representations; "
            "ACS-1 canonical bytes are produced from parsed semantic "
            "values in memory by the conformance runner",
        "fixtures":
            fixture_entries,
    }

    write_json(
        CASES_PATH,
        cases,
    )

    print("=== SW0-006 CORPUS MATERIALIZATION ===")
    print("POSITIVE_FIXTURES=18")
    print("CASE_MANIFESTS=1")
    print("RUNNERS=1")
    print("TOTAL_CORPUS_FILES=20")
    print("EXPECTED_ASSERTIONS=840")
    print("CRYPTO_ENABLED_ROOT_SCHEMAS=0")
    print("RESULT=PASS")


def run():
    failures = []
    counts = defaultdict(int)

    def check(category, name, condition):
        counts[category] += 1

        if not condition:
            failures.append(
                f"{category}:{name}"
            )

    def invalid(schema, document):
        return not Draft202012Validator(
            schema
        ).is_valid(document)

    cases = json.loads(
        CASES_PATH.read_text(
            encoding="utf-8"
        )
    )

    registry = json.loads(
        REGISTRY_PATH.read_text(
            encoding="utf-8"
        )
    )

    check(
        "corpus_contract_digest",
        "contract",
        sha256_file(CONTRACT)
        == cases["contract_sha256"],
    )

    check(
        "corpus_registry_digest",
        "registry",
        sha256_file(REGISTRY_PATH)
        == cases["registry_sha256"],
    )

    check(
        "corpus_runner_digest",
        "runner",
        sha256_file(RUNNER)
        == cases["runner_sha256"],
    )

    entries = registry["schemas"]
    schemas = {}
    entries_by_key = {}

    for entry in entries:
        path = REPO / entry["schema_path"]

        schema = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        key = (
            entry["schema_id"],
            entry["schema_version"],
        )

        entries_by_key[key] = entry
        schemas[entry["schema_id"]] = schema

        actual_digest = sha256_file(path)

        check(
            "registry_digest",
            entry["schema_id"],
            actual_digest
            == entry["schema_sha256"],
        )

        check(
            "dialect",
            entry["schema_id"],
            schema.get("$schema")
            == DIALECT,
        )

        check(
            "closed_root",
            entry["schema_id"],
            schema.get(
                "additionalProperties"
            ) is False,
        )

        try:
            Draft202012Validator.check_schema(
                schema
            )
            meta_ok = True
        except Exception:
            meta_ok = False

        check(
            "meta_schema",
            entry["schema_id"],
            meta_ok,
        )

    check(
        "registry",
        "schema_count",
        registry.get("schema_count") == 18,
    )

    check(
        "registry",
        "entry_count",
        len(entries) == 18,
    )

    check(
        "registry",
        "unique_schema_keys",
        len(entries_by_key) == 18,
    )

    positive = {}

    for fixture in cases["fixtures"]:
        path = REPO / fixture["fixture_path"]

        check(
            "fixture_digest",
            fixture["schema_id"],
            sha256_file(path)
            == fixture["fixture_sha256"],
        )

        positive[fixture["schema_id"]] = (
            json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        )

    check(
        "fixture_inventory",
        "positive_count",
        len(positive) == 18,
    )

    for schema_id, document in positive.items():
        validator = Draft202012Validator(
            schemas[schema_id]
        )

        check(
            "positive",
            schema_id,
            validator.is_valid(document),
        )

        for field in (
            "serialization_profile",
            "schema_id",
            "schema_version",
        ):
            candidate = copy.deepcopy(
                document
            )

            del candidate[field]

            check(
                "missing_reserved",
                f"{schema_id}:{field}",
                invalid(
                    schemas[schema_id],
                    candidate,
                ),
            )

        candidate = copy.deepcopy(document)
        candidate["serialization_profile"] = (
            "ACS-2"
        )

        check(
            "wrong_profile",
            schema_id,
            invalid(
                schemas[schema_id],
                candidate,
            ),
        )

        candidate = copy.deepcopy(document)
        candidate["schema_id"] = (
            "anarchi.brain.not-this-schema"
        )

        check(
            "wrong_schema_id",
            schema_id,
            invalid(
                schemas[schema_id],
                candidate,
            ),
        )

        candidate = copy.deepcopy(document)
        candidate["schema_version"] = "2"

        check(
            "wrong_schema_version",
            schema_id,
            invalid(
                schemas[schema_id],
                candidate,
            ),
        )

        candidate = copy.deepcopy(document)
        candidate["ambient_metadata"] = (
            "forbidden"
        )

        check(
            "unknown_field",
            schema_id,
            invalid(
                schemas[schema_id],
                candidate,
            ),
        )

        required_semantic = [
            name
            for name
            in schemas[schema_id]["required"]
            if name not in {
                "serialization_profile",
                "schema_id",
                "schema_version",
            }
        ]

        for field in required_semantic:
            candidate = copy.deepcopy(
                document
            )

            candidate[field] = None

            check(
                "required_null",
                f"{schema_id}:{field}",
                invalid(
                    schemas[schema_id],
                    candidate,
                ),
            )

        optional_semantic = (
            set(
                schemas[
                    schema_id
                ]["properties"]
            )
            - set(
                schemas[
                    schema_id
                ]["required"]
            )
        )

        for field in sorted(
            optional_semantic
        ):
            candidate = copy.deepcopy(
                document
            )

            candidate[field] = None

            check(
                "optional_null",
                f"{schema_id}:{field}",
                invalid(
                    schemas[schema_id],
                    candidate,
                ),
            )

    schema_ids = sorted(positive)

    for source_id in schema_ids:
        for target_id in schema_ids:
            if source_id == target_id:
                continue

            check(
                "cross_schema",
                f"{source_id}->{target_id}",
                invalid(
                    schemas[target_id],
                    positive[source_id],
                ),
            )

    receipt_ids = sorted(
        schema_id
        for schema_id in schema_ids
        if schema_id.startswith(
            "anarchi.brain.receipt."
        )
    )

    check(
        "receipt_inventory",
        "receipt_count",
        len(receipt_ids) == 5,
    )

    for source_id in receipt_ids:
        for target_id in receipt_ids:
            if source_id == target_id:
                continue

            check(
                "receipt_confusion",
                f"{source_id}->{target_id}",
                invalid(
                    schemas[target_id],
                    positive[source_id],
                ),
            )

    dimensions = [
        "Observe",
        "Propose",
        "Qualify",
        "Authorize",
        "Canonicalize",
        "Project",
        "Execute",
        "Revoke",
        "Migrate",
        "Reconstruct",
        "Attest",
        "Administer",
    ]

    grant_schema = schemas[
        "anarchi.brain.authority-grant"
    ]

    for dimension in dimensions:
        candidate = copy.deepcopy(
            positive[
                "anarchi.brain.authority-grant"
            ]
        )

        candidate[
            "authority_dimension"
        ] = dimension

        check(
            "authority_dimension_valid",
            dimension,
            Draft202012Validator(
                grant_schema
            ).is_valid(candidate),
        )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.authority-grant"
        ]
    )

    candidate["authority_dimension"] = (
        "Omnipotent"
    )

    check(
        "authority_dimension_invalid",
        "invented_dimension",
        invalid(
            grant_schema,
            candidate,
        ),
    )

    auth_schema = schemas[
        "anarchi.brain.authorization"
    ]

    for field in (
        "operation",
        "scope",
        "subject",
        "authority_source",
        "conditions",
    ):
        candidate = copy.deepcopy(
            positive[
                "anarchi.brain.authorization"
            ]
        )

        del candidate[field]

        check(
            "authorization_omission",
            field,
            invalid(
                auth_schema,
                candidate,
            ),
        )

    relationship_schema = schemas[
        "anarchi.brain.relationship"
    ]

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.relationship"
        ]
    )

    candidate["subjects"] = [
        "subject:a"
    ]

    check(
        "relationship",
        "one_subject_rejected",
        invalid(
            relationship_schema,
            candidate,
        ),
    )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.relationship"
        ]
    )

    candidate["subjects"] = [
        "subject:a",
        None,
    ]

    check(
        "relationship",
        "null_subject_rejected",
        invalid(
            relationship_schema,
            candidate,
        ),
    )

    schema_artifact_schema = schemas[
        "anarchi.brain.schema"
    ]

    for field in (
        "governed_schema_id",
        "governed_schema_version",
    ):
        candidate = copy.deepcopy(
            positive[
                "anarchi.brain.schema"
            ]
        )

        candidate[field] = ""

        check(
            "schema_artifact",
            f"empty_{field}",
            invalid(
                schema_artifact_schema,
                candidate,
            ),
        )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.authorization"
        ]
    )

    candidate["artifact_kind"] = (
        "Authority Grant Artifact"
    )

    check(
        "contradictory_identity",
        "artifact_kind_rejected",
        invalid(
            auth_schema,
            candidate,
        ),
    )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.receipt.event"
        ]
    )

    candidate["receipt_kind"] = (
        "Decision Receipt"
    )

    check(
        "contradictory_identity",
        "receipt_kind_rejected",
        invalid(
            schemas[
                "anarchi.brain.receipt.event"
            ],
            candidate,
        ),
    )

    def resolve(document):
        schema_id = document.get(
            "schema_id"
        )

        schema_version = document.get(
            "schema_version"
        )

        if not isinstance(
            schema_id,
            str,
        ):
            return "UNRESOLVED"

        if not isinstance(
            schema_version,
            str,
        ):
            return "UNRESOLVED"

        entry = entries_by_key.get(
            (
                schema_id,
                schema_version,
            )
        )

        if entry is None:
            return "UNRESOLVED"

        schema = schemas[schema_id]

        if Draft202012Validator(
            schema
        ).is_valid(document):
            return "STRUCTURALLY_VALID"

        return "STRUCTURALLY_INVALID"

    for schema_id, document in positive.items():
        check(
            "resolver_positive",
            schema_id,
            resolve(document)
            == "STRUCTURALLY_VALID",
        )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.observation"
        ]
    )
    candidate["schema_id"] = (
        "anarchi.brain.future"
    )

    check(
        "resolver_unresolved",
        "unknown_schema_id",
        resolve(candidate)
        == "UNRESOLVED",
    )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.observation"
        ]
    )
    candidate["schema_version"] = "2"

    check(
        "resolver_unresolved",
        "unknown_schema_version",
        resolve(candidate)
        == "UNRESOLVED",
    )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.observation"
        ]
    )
    del candidate["schema_id"]

    check(
        "resolver_unresolved",
        "missing_schema_id",
        resolve(candidate)
        == "UNRESOLVED",
    )

    candidate = copy.deepcopy(
        positive[
            "anarchi.brain.observation"
        ]
    )
    del candidate["schema_version"]

    check(
        "resolver_unresolved",
        "missing_schema_version",
        resolve(candidate)
        == "UNRESOLVED",
    )

    for schema_id, document in positive.items():
        encoded_one = acs1_encode(
            document
        )

        encoded_two = acs1_encode(
            document
        )

        check(
            "acs1_repeat",
            schema_id,
            encoded_one == encoded_two,
        )

        parsed = json.loads(
            encoded_one.decode("utf-8")
        )

        check(
            "acs1_parse_reserialize",
            schema_id,
            acs1_encode(parsed)
            == encoded_one,
        )

        check(
            "acs1_no_bom",
            schema_id,
            not encoded_one.startswith(
                b"\xef\xbb\xbf"
            ),
        )

        check(
            "acs1_document_boundary",
            schema_id,
            encoded_one[:1] == b"{"
            and encoded_one[-1:] == b"}"
            and encoded_one
                == encoded_one.strip(),
        )

        reversed_document = dict(
            reversed(
                list(
                    document.items()
                )
            )
        )

        check(
            "acs1_key_order",
            schema_id,
            acs1_encode(
                reversed_document
            )
            == encoded_one,
        )

    crypto_fields = (
        "cryptographic_profile",
        "digest",
        "public_key",
        "key_identifier",
        "signature",
    )

    for schema_id, document in positive.items():
        for field in crypto_fields:
            candidate = copy.deepcopy(
                document
            )

            candidate[field] = (
                "not-permitted-by-this-root"
            )

            check(
                "crypto_uniformity",
                f"{schema_id}:{field}",
                invalid(
                    schemas[schema_id],
                    candidate,
                ),
            )

    total = sum(counts.values())

    if (
        dict(counts)
        != cases["assertion_plan"]
    ):
        failures.append(
            "ASSERTION_PLAN_MISMATCH"
        )

    if total != cases[
        "expected_assertions"
    ]:
        failures.append(
            "ASSERTION_TOTAL_MISMATCH:"
            + str(total)
        )

    print(
        "=== SW0-006 PERSISTED "
        "CONFORMANCE CORPUS ==="
    )
    print(
        f"PYTHON={sys.version.split()[0]}"
    )
    print(
        f"ROOT_SCHEMAS={len(schemas)}"
    )
    print(
        f"POSITIVE_FIXTURES={len(positive)}"
    )
    print(
        f"REGISTRY_ENTRIES={len(entries)}"
    )

    print(
        "=== TEST CATEGORY COUNTS ==="
    )

    for category in sorted(counts):
        print(
            f"{category.upper()}="
            f"{counts[category]}"
        )

    print("=== COMPOSITION PROOFS ===")
    print("ACS1_COMPOSITION_ASSERTIONS=90")
    print("CRYPTO_UNIFORMITY_ATTACKS=90")
    print("CRYPTO_ENABLED_ROOT_SCHEMAS=0")
    print("PERSISTED_FIXTURE_DIGESTS=18")
    print("CORPUS_BINDING_ASSERTIONS=3")
    print(
        "UNKNOWN_SCHEMA_RESOLUTION="
        "UNRESOLVED"
    )
    print(
        "UNKNOWN_VERSION_RESOLUTION="
        "UNRESOLVED"
    )

    print("=== RESULT ===")
    print(
        f"EXPECTED_ASSERTIONS="
        f"{cases['expected_assertions']}"
    )
    print(
        f"TOTAL_ASSERTIONS={total}"
    )
    print(
        f"FAILURE_COUNT={len(failures)}"
    )

    if failures:
        print("RESULT=FAIL")

        for failure in failures:
            print(
                f"FAILURE={failure}"
            )

        return 1

    print("RESULT=PASS")
    print(
        "SW0_006_PERSISTED_CORPUS_PROVEN=True"
    )
    print(
        "SW0_006_ACS1_COMPOSITION_PROVEN=True"
    )
    print(
        "SW0_006_NO_CRYPTO_BY_UNIFORMITY_PROVEN=True"
    )
    print(
        "SW0_006_CONFORMANCE_RUNNER_COMPLETE=True"
    )

    return 0


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--materialize",
        action="store_true",
    )

    args = parser.parse_args()

    if args.materialize:
        materialize()
        return 0

    return run()


if __name__ == "__main__":
    raise SystemExit(main())
