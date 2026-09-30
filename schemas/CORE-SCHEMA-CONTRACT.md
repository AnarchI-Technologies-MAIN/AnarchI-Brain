# Core Schema Contract

Status: FROZEN - SW0-006

## 1. Purpose

This contract defines the initial concrete schema topology for the AnarchI Brain.

SW0-006 translates the frozen constitutional meanings established by SW0-001 through SW0-005 into schema-governed document structures without collapsing representation into constitutional consequence.

This contract defines:

- the initial root schema registry;
- schema identity rules;
- schema-version binding;
- artifact-kind resolution;
- Receipt subtype resolution;
- universal ACS-1 members;
- schema-specific semantic obligations;
- structural validation boundaries;
- extension behavior;
- reference behavior;
- authority-schema boundaries;
- cryptographic-schema boundaries;
- historical schema interpretation;
- requirements for the machine-checkable schema set.

This contract does not implement database storage, state machines, canonical admission, authority resolution, cryptographic key custody, or runtime orchestration.

## 2. Constitutional Precedence

SW0-006 is subordinate to:

- SW0-001 Semantic Language;
- SW0-002 Authority Dimensions;
- SW0-003 Artifact and Receipt Taxonomy;
- SW0-004 ACS-1 Canonical Serialization;
- SW0-005 ACBP-1 Cryptographic Binding.

A schema defined by SW0-006 must not silently redefine any frozen constitutional meaning.

Where a structural representation can be interpreted in multiple ways, the frozen constitutional contracts take precedence over implementation convenience.

## 3. Schema Is Interpretation

A Schema defines permitted structure and interpretation rules for material governed by that schema.

Schema identity is not merely a filename.

Schema identity is not merely a database table.

Schema identity is not merely an application type.

A schema identifier and schema version jointly bind the historical interpretation context of a governed document.

Historical schema meaning is immutable.

## 4. Universal ACS-1 Document Members

Every complete document governed by an SW0-006 root schema must contain exactly the ACS-1 reserved interpretation members required by SW0-004:

- serialization_profile
- schema_id
- schema_version

For all initial SW0-006 schemas:

serialization_profile must be:

ACS-1

schema_id must equal the exact identifier of the applicable registered root schema.

schema_version must be:

1

The value 1 is represented as the exact ACS-1 String:

"1"

## 5. No Additional Universal Artifact Envelope

SW0-006 does not define any additional member as universal across all artifact documents.

The following are therefore not universal merely because they are important elsewhere in the constitution:

- artifact_id
- artifact_kind
- identity
- subject
- provenance
- processing_lineage
- canonicality
- temporal classification
- derivation classification
- evidence status
- authority
- authority root
- authorization
- capability
- cryptographic profile
- digest
- public key
- key identifier
- signature
- revocation state
- lifecycle state
- timestamp

A specific root schema may require one or more such concepts where constitutionally justified.

## 6. Artifact Kind Resolution

For the initial SW0-006 registry, artifact kind is deterministically resolved from:

schema_id + schema_version

An additional universal artifact_kind member is not required.

A document must not use an artifact_kind member to override or contradict the artifact kind resolved by its schema binding.

A future schema may contain a semantic field whose name includes the word kind only where that field has an independently defined meaning.

## 7. Receipt Kind Resolution

Receipt Artifact subtype is deterministically resolved from the specialized Receipt root schema.

The initial registry therefore does not require a separate receipt_kind member.

The following Receipt kinds are represented by distinct root schemas:

- Event Receipt;
- Decision Receipt;
- Attempt Receipt;
- Transition Receipt;
- Effect Receipt.

A Receipt schema identity is sufficient to identify or deterministically resolve its primary Receipt kind.

## 8. Initial Root Schema Registry

SW0-006 defines exactly eighteen initial root schema identities.

All initial root schemas use schema_version:

1

The initial registry is:

1. anarchi.brain.observation
2. anarchi.brain.validation-result
3. anarchi.brain.qualification-result
4. anarchi.brain.attestation
5. anarchi.brain.proposal
6. anarchi.brain.relationship
7. anarchi.brain.authority-grant
8. anarchi.brain.authorization
9. anarchi.brain.capability
10. anarchi.brain.schema
11. anarchi.brain.policy-root
12. anarchi.brain.projection
13. anarchi.brain.integrity-epoch-record
14. anarchi.brain.receipt.event
15. anarchi.brain.receipt.decision
16. anarchi.brain.receipt.attempt
17. anarchi.brain.receipt.transition
18. anarchi.brain.receipt.effect

## 9. Registry Mapping

The root schema registry resolves as follows:

anarchi.brain.observation
→ Observation Artifact

anarchi.brain.validation-result
→ Validation Result Artifact

anarchi.brain.qualification-result
→ Qualification Result Artifact

anarchi.brain.attestation
→ Attestation Artifact

anarchi.brain.proposal
→ Proposal Artifact

anarchi.brain.relationship
→ Relationship Artifact

anarchi.brain.authority-grant
→ Authority Grant Artifact

anarchi.brain.authorization
→ Authorization Artifact

anarchi.brain.capability
→ Capability Artifact

anarchi.brain.schema
→ Schema Artifact

anarchi.brain.policy-root
→ Policy Root Artifact

anarchi.brain.projection
→ Projection Artifact

anarchi.brain.integrity-epoch-record
→ Integrity Epoch Record Artifact

anarchi.brain.receipt.event
→ Receipt Artifact / Event Receipt

anarchi.brain.receipt.decision
→ Receipt Artifact / Decision Receipt

anarchi.brain.receipt.attempt
→ Receipt Artifact / Attempt Receipt

anarchi.brain.receipt.transition
→ Receipt Artifact / Transition Receipt

anarchi.brain.receipt.effect
→ Receipt Artifact / Effect Receipt

## 10. Exact Registry Identity

Initial root schema identifiers are exact strings.

An implementation must not:

- case-fold them;
- trim them;
- normalize Unicode into another identifier;
- infer aliases;
- infer plural forms;
- substitute a preferred schema;
- map an unknown identifier to the nearest known identifier;
- silently upgrade a schema version;
- silently downgrade a schema version.

Unknown schema identities are unresolved.

## 11. Initial Version Binding

All initial SW0-006 root schemas have schema_version:

1

SW0-006 does not define a general future schema-version syntax beyond the frozen requirement that schema_version is a non-empty String.

A future schema contract may define successor version identifiers.

A later version must not silently reinterpret material governed by version 1.

## 12. Root Schema Closure

Each root schema defines the complete permitted top-level member set for that schema version.

Unknown top-level members are rejected by default.

A root schema may explicitly declare a governed extension point.

No initial root schema gains an extension point merely because an implementation wishes to preserve arbitrary metadata.

Compatible unknown-field preservation applies only where the governing schema explicitly permits such preservation.

## 13. Reserved Member Protection

The members:

serialization_profile
schema_id
schema_version

are reserved by ACS-1.

A schema-specific semantic member must not redefine their meaning.

A schema-specific member must not duplicate their meaning under another field name in order to evade ACS-1 interpretation rules.

## 14. Null Versus Absence

Null and absent remain distinct.

A schema must explicitly determine whether a member:

- is required;
- is optional;
- may contain Null;
- must contain a non-Null value.

For all initial SW0-006 root schemas, schema-specific members are non-Null unless the applicable root schema explicitly states otherwise.

No initial root schema defined by this contract states otherwise.

Therefore:

- a required member must be present and non-Null;
- an optional member may be absent;
- an optional member, when present, must be non-Null;
- Null must not be used as a substitute for absence.

An implementation must not silently substitute Null for an absent required member.

An implementation must not silently omit a present Null member.

## 15. Schema Validation Boundary

Schema validation determines only whether a semantic value satisfies the applicable schema structure and schema-level constraints.

Schema-valid does not imply:

- truth;
- Evidence;
- Qualification;
- valid issuance;
- authority;
- permission;
- Authorization;
- Capability effectiveness;
- Canonical Membership;
- applicability;
- legal transition;
- successful execution;
- provenance correctness;
- cryptographic validity.

## 16. Artifact Representation Boundary

A document satisfying an artifact schema is an artifact-shaped representation under that schema.

Representation remains distinct from valid issuance.

Schema conformance must not manufacture the constitutional consequence associated with an artifact kind.

A structurally valid Authority Grant Artifact does not itself prove effective authority.

A structurally valid Authorization Artifact does not itself authorize a transition.

A structurally valid Capability Artifact does not itself prove permitted exercise.

## 17. Canonicality Boundary

Schema validity and canonicality are distinct.

Schema-valid != Canonical Membership.

ACS-1 canonical bytes != Canonical Membership.

Canonical Membership is governed by the applicable canonicalization authority path and lifecycle.

No initial root schema contains a universal canonicality member.

A canonicality state associated with a document must not be inferred from schema conformance.

## 18. Evidence Boundary

Evidence is a contextual role.

Evidence is not an artifact kind.

No initial root schema contains a universal evidence boolean or evidence status merely because the artifact may later participate as Evidence.

Evidence admission belongs to the applicable evidence lifecycle and contract.

## 19. Provenance Boundary

Provenance is not required by SW0-006 to be represented by one universal member.

A schema may represent provenance through:

- schema-specific fields;
- Relationship Artifacts;
- references;
- Receipt Artifacts;
- later governed structures.

Presence of a provenance-shaped field does not itself prove provenance correctness.

Absence of a universal provenance field does not erase provenance requirements imposed by another governing contract.

## 20. Processing Lineage Boundary

Processing Lineage remains distinguishable from independent corroboration.

Processing Lineage is not a universal root-schema field.

A schema may include processing-lineage material where required.

Repeated derivation through multiple processing steps does not become independent corroboration merely because lineage records exist.

## 21. Identity Boundary

SW0-006 does not define one universal identity format for all subjects, sources, agents, artifacts, devices, organizations, or authorities.

Where a root schema requires an identified source, subject, grantee, or authority source, the applicable member must contain or deterministically resolve the identifier required by its governing contract.

Structural presence of an identifier does not prove correct attribution.

## 22. Reference Semantics

A reference is representational.

A reference does not become the referenced material.

A reference does not inherit the authority of the referenced material.

A reference does not prove that its target exists.

A reference does not prove that its target is canonical, current, valid, authorized, or applicable.

Where exact referenced material is required and cannot be deterministically resolved, the dependent interpretation is unresolved.

## 23. Deterministic Resolution

The phrase deterministically resolve means that the governing contract identifies a bounded resolution process whose inputs are sufficient to produce one interpretation without ambient guessing.

Deterministic resolution must not depend on:

- current database row preference;
- newest timestamp by convention;
- filesystem ordering;
- provider preference;
- model choice;
- undocumented aliases;
- hidden environment state;
- human intuition not represented by governed input.

## 24. Observation Root Schema

Schema:

anarchi.brain.observation
version 1

Artifact kind:

Observation Artifact

The machine-checkable schema must require semantic members sufficient to represent:

- an identified source;
- what that source perceived, measured, received, or reported.

The initial required member names are:

source
observation

source binds or deterministically resolves the identified source.

observation carries the recorded Observation semantic value.

Observation Artifact schema validity does not make the observation true.

Observation Artifact schema validity does not make it Evidence.

## 25. Validation Result Root Schema

Schema:

anarchi.brain.validation-result
version 1

Artifact kind:

Validation Result Artifact

The machine-checkable schema must require:

subject
validation_contract
result

subject binds or deterministically resolves the material evaluated.

validation_contract binds or deterministically resolves the validation contract used.

result records the bounded result produced by the validation lifecycle.

The result vocabulary is not invented by SW0-006 where the applicable validation lifecycle owns that vocabulary.

A Validation Result Artifact does not automatically become a Qualification Result Artifact.

## 26. Qualification Result Root Schema

Schema:

anarchi.brain.qualification-result
version 1

Artifact kind:

Qualification Result Artifact

The machine-checkable schema must require:

subject
qualification_contract
result

subject binds or deterministically resolves the evaluated material.

qualification_contract binds or deterministically resolves the applicable qualification contract, policy, schema, or admissibility rule.

result records the bounded Qualification result.

Qualification result representation does not itself Canonicalize evaluated material.

## 27. Attestation Root Schema

Schema:

anarchi.brain.attestation
version 1

Artifact kind:

Attestation Artifact

The machine-checkable schema must require:

source
assertion

source binds or deterministically resolves the attesting source.

assertion records the assertion for which responsibility is being represented.

Attestation schema validity does not make the assertion true.

Attestation schema validity does not prove Attest authority.

Cryptographic signature material is not required unless an applicable governing schema or contract explicitly requires it.

## 28. Proposal Root Schema

Schema:

anarchi.brain.proposal
version 1

Artifact kind:

Proposal Artifact

The machine-checkable schema must require:

proposal

proposal represents a possible state, relationship, operation, interpretation, or transition.

Proposal representation does not make the proposed change effective.

Canonical Membership of the Proposal Artifact does not make the proposed change effective.

## 29. Relationship Root Schema

Schema:

anarchi.brain.relationship
version 1

Artifact kind:

Relationship Artifact

The machine-checkable schema must require:

subjects
relationship

subjects identifies the subjects or artifacts participating in the represented relationship.

subjects must contain at least two entries.

relationship represents the declared relationship.

Array ordering of subjects is semantic unless a later schema version explicitly defines unordered relationship semantics.

A Relationship Artifact must not silently create authority between its subjects.

## 30. Authority Grant Root Schema

Schema:

anarchi.brain.authority-grant
version 1

Artifact kind:

Authority Grant Artifact

The machine-checkable schema must require:

grantee
authority_dimension
authority_root

grantee binds or deterministically resolves the identified grantee.

authority_dimension identifies exactly one frozen SW0-002 authority dimension.

The permitted constitutional dimension names are:

- Observe
- Propose
- Qualify
- Authorize
- Canonicalize
- Project
- Execute
- Revoke
- Migrate
- Reconstruct
- Attest
- Administer

authority_root binds or deterministically resolves the applicable authority root.

The schema must permit explicit governed representation of consequential restrictions including, where applicable:

scope
operation
conditions
temporal_bounds
delegation
revocation

A complete effective grant must explicitly bind, or have its governing authority root explicitly define, every consequential restriction required for interpretation.

Structural schema validity alone cannot prove that this completeness condition has been satisfied.

## 31. Authority Grant Non-Transitivity

An Authority Grant Artifact must not gain additional dimensions through schema interpretation.

One authority dimension does not imply another.

A grant must not silently delegate itself.

A grant must not silently permit subdelegation.

A grant must not exceed its authority root.

Two grant records belonging to one effective authority principal do not become independent merely because two documents exist.

## 32. Authorization Root Schema

Schema:

anarchi.brain.authorization
version 1

Artifact kind:

Authorization Artifact

The machine-checkable schema must require:

operation
scope
subject
authority_source
conditions

These members must bind or deterministically resolve the operation, scope, subject, authority source, and conditions required by the governing contract.

An Authorization Artifact does not authorize merely because the required fields are structurally present.

Authorization validity requires the applicable authority-resolution and lifecycle semantics.

An Authorization Artifact is distinct from an Authority Grant Artifact.

An Authorization Artifact is distinct from a Capability Artifact.

An Authorization Artifact is distinct from the Receipt recording its issuance or use.

## 33. Capability Root Schema

Schema:

anarchi.brain.capability
version 1

Artifact kind:

Capability Artifact

The machine-checkable schema must require:

operation
means

operation identifies or deterministically resolves the bounded operation that may technically be exercised.

means represents the bounded means through which that operation can be exercised.

A schema may additionally define:

scope
conditions
temporal_bounds

where required by the capability contract.

Capability representation does not imply Permission.

Capability representation does not imply Authorization.

Possession of a Capability Artifact does not prove permitted exercise.

## 34. Schema Artifact Root Schema

Schema:

anarchi.brain.schema
version 1

Artifact kind:

Schema Artifact

The machine-checkable schema must require:

governed_schema_id
governed_schema_version
schema_definition

governed_schema_id identifies the schema represented by the artifact.

governed_schema_version identifies the represented interpretation version.

schema_definition contains or deterministically resolves the governed schema definition and interpretation rules.

The member names governed_schema_id and governed_schema_version are intentionally distinct from the ACS-1 reserved members schema_id and schema_version.

The reserved members identify the schema governing the Schema Artifact itself.

The governed members identify the schema represented by that artifact.

Storage presence does not make the represented schema applicable.

Canonical Membership does not make the represented schema universally applicable.

## 35. Policy Root Root Schema

Schema:

anarchi.brain.policy-root
version 1

Artifact kind:

Policy Root Artifact

The machine-checkable schema must require:

policy_root
policy

policy_root identifies or deterministically resolves the represented policy root.

policy contains or deterministically resolves the governed policy-root definition.

Policy Root Artifact schema validity does not create constitutional authority.

Policy applicability is governed separately.

## 36. Projection Root Schema

Schema:

anarchi.brain.projection
version 1

Artifact kind:

Projection Artifact

The machine-checkable schema must require:

source
projection

source binds or deterministically resolves the permitted underlying material.

projection records the derived projection.

A Projection Artifact does not mutate its source.

A Projection Artifact does not automatically inherit Canonical Membership, authority, Evidence role, or provenance validity from its source.

## 37. Integrity Epoch Record Root Schema

Schema:

anarchi.brain.integrity-epoch-record
version 1

Artifact kind:

Integrity Epoch Record Artifact

The machine-checkable schema must require:

epoch
record

epoch identifies or deterministically resolves the bounded integrity epoch or integrity context.

record contains the integrity-boundary event or record defined by the applicable integrity lifecycle.

Existence of the record does not prove system integrity.

The integrity epoch lifecycle belongs to later state-machine work.

## 38. Event Receipt Root Schema

Schema:

anarchi.brain.receipt.event
version 1

Artifact kind:

Receipt Artifact

Primary Receipt kind:

Event Receipt

The machine-checkable schema must require:

event

event records the occurrence claim represented by the Event Receipt.

An Event Receipt does not independently prove that the event was truthful, valid, authorized, or canonical.

## 39. Decision Receipt Root Schema

Schema:

anarchi.brain.receipt.decision
version 1

Artifact kind:

Receipt Artifact

Primary Receipt kind:

Decision Receipt

The machine-checkable schema must require:

decision

decision records the decision occurrence claim represented by the Receipt.

A Decision Receipt does not replace a distinct decision artifact where one is required.

A Decision Receipt does not prove that the decision-maker possessed valid authority.

## 40. Attempt Receipt Root Schema

Schema:

anarchi.brain.receipt.attempt
version 1

Artifact kind:

Receipt Artifact

Primary Receipt kind:

Attempt Receipt

The machine-checkable schema must require:

attempt

attempt records the attempt occurrence claim represented by the Receipt.

Recording an attempt does not prove successful execution.

Recording an attempt does not prove that the attempted operation was authorized.

## 41. Transition Receipt Root Schema

Schema:

anarchi.brain.receipt.transition
version 1

Artifact kind:

Receipt Artifact

Primary Receipt kind:

Transition Receipt

The machine-checkable schema must require:

transition

transition records the transition occurrence claim represented by the Receipt.

A Transition Receipt does not independently establish that the transition was legal, authorized, canonical, or valid.

## 42. Effect Receipt Root Schema

Schema:

anarchi.brain.receipt.effect
version 1

Artifact kind:

Receipt Artifact

Primary Receipt kind:

Effect Receipt

The machine-checkable schema must require:

effect

effect records the effect occurrence claim represented by the Receipt.

An Effect Receipt does not automatically prove causal attribution.

An Effect Receipt does not automatically prove that the operation producing the effect was authorized.

## 43. Receipt Artifact Boundaries

All five Receipt root schemas remain Receipt Artifacts.

Receipt subtype does not change the constitutional artifact family.

A Receipt may reference another artifact without becoming that artifact.

A Receipt may record creation, issuance, evaluation, transition, execution, failure, or effect involving another artifact without replacing that artifact's semantic kind.

Receipt existence and validity of the represented occurrence remain distinguishable questions.

## 44. Cryptographic Material

No cryptographic member is universal.

A root schema may include cryptographic material only where its governing semantics require that material.

Where a governed record claims an ACBP-1 cryptographic result, it must bind or deterministically resolve the information required by SW0-005.

Depending on the result, that may include:

- cryptographic profile;
- algorithm identifier;
- purpose;
- digest;
- public key or resolvable key identifier;
- signature;
- payload or deterministic payload reference.

Cryptographic presence does not create authority.

Cryptographic verification does not create Canonical Membership.

## 45. Private-Key Exclusion

No SW0-006 root schema may define production private-key material as artifact content.

Private-key material must not be represented in:

- canonical artifacts;
- Receipt Artifacts;
- provenance records;
- processing-lineage records;
- projections;
- diagnostics;
- telemetry;
- cryptographic result records.

Key custody belongs to dedicated key-management contracts and substrates.

## 46. Detached Signature Boundary

A schema permitting detached signatures must not equate:

payload reference

with:

payload

A payload digest is not the payload.

Where exact signed payload bytes cannot be deterministically recovered, cryptographic verification remains unresolved.

## 47. Temporal Material

No universal created_at, updated_at, signed_at, or recorded_at field is defined by SW0-006.

A root schema may require temporal semantic material where its governing contract requires it.

Filesystem time, database time, transport time, and model-generated time must not silently become trusted semantic time.

## 48. Authority Coordinates

Authority-bearing schemas may structurally represent:

- grantee;
- authority dimension;
- authority root;
- subject;
- scope;
- operation;
- conditions;
- temporal bounds;
- delegation;
- revocation.

Presence of these coordinates does not itself prove effective authority.

Missing or unresolved authority required by a consequential transition must fail closed under the applicable state machine.

## 49. Authority Source Versus Authority Grant

An authority_source binding may reference or resolve material involved in authority determination.

The presence of authority_source does not mean the referenced source is valid.

An Authority Grant Artifact is representational.

Effective authority requires resolution under SW0-002.

## 50. Applicability

A schema may be known without being applicable.

A Schema Artifact may be valid without being applicable.

A schema may be canonical without being applicable to every domain.

Schema applicability requires the applicable governed selection or registry process.

SW0-006 does not infer applicability from storage presence or recency.

## 51. Structural Validation Outcomes

The machine-checkable schema layer must be able to distinguish:

- structurally valid;
- structurally invalid;
- interpretation unresolved.

Interpretation unresolved applies where the claimed schema identity or version cannot be deterministically resolved.

These structural outcomes must not be confused with Validation Result Artifact or Qualification Result Artifact semantics.

## 52. Unknown Schema

An unknown schema_id must not be interpreted as a known root schema.

An unknown schema_version must not be interpreted as version 1.

Unknown schema material may be preserved where a governing transport or storage contract permits preservation.

Preservation does not assign semantic meaning.

## 53. Future Artifact Kinds

Unknown future artifact kinds must not be coerced into the nearest known root schema.

A future artifact kind requires an explicitly governed schema identity and semantic definition.

An implementation must not infer a future kind from field resemblance.

## 54. Schema Evolution

A new schema version may:

- add new governed structure;
- change constraints for new material;
- add explicit extension semantics;
- supersede a previous version for new material.

A new schema version must not silently redefine the historical interpretation of version 1 material.

Migration must create an explicitly governed transition where representation or semantic version changes require one.

## 55. Field Renaming

Renaming a member changes schema structure.

An implementation must not silently map unknown member names to known members merely because they appear semantically similar.

Compatibility aliases require explicit schema rules.

## 56. Default Materialization

No initial root schema relies on ambient default materialization.

A required member must be explicitly present.

An optional absent member remains absent.

A semantic default, where ever later permitted, must be materialized as an explicit governed semantic operation before ACS-1 serialization.

## 57. Hidden Metadata

Schema validation and serialization must not inject:

- provider metadata;
- database identifiers;
- trace identifiers;
- host identifiers;
- runtime versions;
- model identifiers;
- cloud-provider metadata;
- filesystem paths;
- timestamps;
- request identifiers;

unless the applicable schema explicitly defines that information as semantic content.

## 58. Collection Semantics

Array ordering remains semantic by default.

A machine-checkable root schema must explicitly identify any collection whose semantics are unordered.

No implementation may sort a semantically ordered collection for convenience.

Duplicate handling must be governed by the applicable schema.

## 59. Relationship Subjects

The initial Relationship schema treats subjects as an ordered Array because no frozen contract establishes unordered relationship-subject semantics.

A future schema may define unordered relationship semantics explicitly.

Changing that interpretation requires a new schema version.

## 60. Authority Dimension Enumeration

The initial Authority Grant schema must reject an authority_dimension value outside the twelve frozen SW0-002 dimensions.

No implementation may invent a thirteenth authority dimension through schema extension.

A future constitutional change to authority dimensions is outside ordinary schema evolution.

## 61. Schema Artifact Self-Description

A Schema Artifact may represent the same schema family that governs the Schema Artifact itself.

Such self-description does not make the represented schema self-authorizing.

A Schema Artifact must not infer applicability from recursive self-reference.

## 62. Schema Registry Boundary

The initial root registry is defined constitutionally by SW0-006.

Runtime lookup infrastructure may mirror this registry.

The runtime registry does not own its constitutional meaning.

A database registry, filesystem registry, package registry, or API registry must not silently change root-schema interpretation.

## 63. File Naming

Machine-checkable schema filenames are transport and repository organization.

Filename does not define schema identity.

The schema_id contained in the governed document and resolved through the applicable registry defines schema interpretation.

## 64. Database Representation

Database tables and columns must not define constitutional schema semantics.

A database may store or index governed fields.

A database migration does not automatically constitute a constitutional schema migration.

## 65. API Representation

An API route or endpoint does not define artifact kind.

An API may transport an artifact representation.

Transport success does not establish schema validity, valid issuance, authority, or Canonical Membership.

## 66. Cognition Boundary

Cognition may propose schema-shaped material.

Cognition does not gain schema authority merely by generating structurally valid material.

A model may generate an Authority Grant-shaped document without creating authority.

A model may generate an Authorization-shaped document without authorizing anything.

A model may generate a Schema Artifact-shaped document without making that schema applicable.

## 67. Administrator Boundary

Administrator visibility or write access does not redefine schema semantics.

Administrator control over schema files does not itself grant authority to alter frozen constitutional meaning.

Governed schema evolution must follow the applicable authority and lifecycle contracts.

## 68. Schema-Valid Non-Collapse Laws

The following are mandatory:

- schema-valid != true
- schema-valid != Evidence
- schema-valid != Qualified
- schema-valid != valid issuance
- schema-valid != authorized
- schema-valid != permitted
- schema-valid != effective authority
- schema-valid != effective Capability
- schema-valid != Canonical Membership
- schema-valid != applicable
- schema-valid != cryptographically valid
- schema-valid != successfully executed
- schema identity != artifact validity
- schema storage != schema applicability
- schema recency != schema applicability
- schema resemblance != schema identity
- artifact representation != constitutional consequence
- Receipt != underlying occurrence
- Authority Grant representation != effective authority
- Authorization representation != valid Authorization
- Capability representation != Permission
- cryptographic field presence != authority
- provenance field presence != provenance correctness
- canonical bytes != Canonical Membership
- administrator control != schema authority
- cognition != schema authority

## 69. Machine-Checkable Root Schema Set

SW0-006 closure requires machine-checkable schema definitions for exactly the eighteen initial root schemas.

The machine-checkable schema dialect for SW0-006 is JSON Schema Draft 2020-12.

Each machine-checkable root schema must declare the exact dialect identifier:

https://json-schema.org/draft/2020-12/schema

JSON Schema Draft 2020-12 defines the structural validation language used to encode SW0-006 constraints.

The JSON Schema dialect does not define constitutional meaning.

JSON Schema validation does not establish:

- valid issuance;
- authority;
- Authorization;
- Permission;
- Canonical Membership;
- Evidence;
- schema applicability;
- cryptographic validity.

An implementation must not silently interpret an unsupported or different JSON Schema dialect as Draft 2020-12.

Each machine-checkable schema must:

- require ACS-1 serialization_profile;
- require the exact applicable schema_id;
- require schema_version "1";
- require the semantic members defined by this contract;
- reject incorrect root schema identity;
- reject missing reserved ACS-1 members;
- reject unknown top-level members unless explicitly permitted;
- encode applicable collection constraints;
- encode applicable enumerations;
- remain free of hidden ambient defaults.

## 70. Schema Registry Manifest

SW0-006 closure requires one machine-checkable registry manifest binding:

- schema_id;
- schema_version;
- artifact kind;
- Receipt subtype where applicable;
- machine-checkable schema location;
- frozen schema digest once finalized.

The registry manifest is representational.

Registry presence does not establish schema applicability outside its governing domain.

## 71. Positive Fixtures

SW0-006 closure requires at least one structurally valid fixture for every root schema.

A positive fixture proves only that the fixture satisfies the tested structural contract.

A positive fixture does not prove valid issuance, authority, truth, Evidence, or Canonical Membership.

## 72. Negative Fixtures

SW0-006 closure requires adversarial negative fixtures including:

- missing serialization_profile;
- incorrect serialization_profile;
- missing schema_id;
- wrong schema_id;
- missing schema_version;
- wrong schema_version;
- missing required semantic member;
- unknown top-level member;
- incorrect authority dimension;
- contradictory schema identity;
- Receipt subtype confusion;
- Authorization missing operation;
- Authorization missing scope;
- Authorization missing subject;
- Authorization missing authority_source;
- Authorization missing conditions.

## 73. Cross-Schema Confusion Tests

A fixture valid under one root schema must not silently validate under a different root schema merely because field shapes overlap.

In particular:

- Validation Result must not become Qualification Result;
- Authority Grant must not become Authorization;
- Authorization must not become Capability;
- Proposal must not become Authorization;
- Receipt must not become the artifact it records;
- Projection must not become its source;
- Schema Artifact must not become the represented schema.

## 74. Receipt Subtype Confusion Tests

Each specialized Receipt fixture must resolve exactly one primary Receipt subtype.

An Event Receipt fixture must not silently validate as Decision Receipt.

A Decision Receipt fixture must not silently validate as Transition Receipt.

An Attempt Receipt fixture must not silently validate as Effect Receipt.

Receipt subtype resolution must follow schema identity rather than heuristic field inspection.

## 75. Authority Schema Tests

SW0-006 closure requires machine-checkable evidence that:

- exactly twelve authority_dimension values are accepted;
- unknown authority dimensions are rejected;
- required Authority Grant core members are present;
- required Authorization bindings are present;
- schema conformance alone is not reported as effective authority.

## 76. Extension Tests

If any initial root schema defines an extension point, SW0-006 closure requires tests proving:

- permitted unknown extension values survive round trip;
- extension preservation does not assign invented meaning;
- forbidden unknown top-level fields fail closed;
- extensions cannot replace required known members;
- extensions cannot override reserved ACS-1 members.

If no initial root schema defines an extension point, closure evidence must explicitly prove that unknown top-level fields are rejected.

## 77. Historical Stability Tests

SW0-006 closure requires evidence that:

- schema_id is byte-exact;
- schema_version is byte-exact;
- version 1 is not silently upgraded;
- unknown versions are unresolved;
- unknown schema identifiers are unresolved;
- historical version 1 fixtures retain their version 1 interpretation.

## 78. ACS-1 Composition Tests

SW0-006 closure requires fixtures demonstrating composition with ACS-1.

For each tested valid root document:

- required ACS members are present;
- semantic value satisfies the root schema;
- ACS-1 canonical serialization is deterministic;
- canonical byte production does not create Canonical Membership.

## 79. ACBP-1 Composition Tests

Where a root-schema fixture contains an ACBP-1 cryptographic record, SW0-006 closure requires tests demonstrating:

- profile binding remains explicit;
- cryptographic purpose remains explicit;
- signature or digest representation remains deterministic;
- cryptographic validity remains separate from schema validity;
- cryptographic validity remains separate from authority and Canonical Membership.

Schemas without cryptographic semantics must not gain cryptographic fields merely for uniformity.

## 80. SW0-006 Closure Conditions

SW0-006 may close only when machine-checkable evidence demonstrates that:

1. exactly eighteen initial root schema identities are defined;
2. all initial root schemas use schema_version "1";
3. all root documents require the three ACS-1 reserved interpretation members;
4. no additional universal artifact envelope is introduced;
5. schema identity deterministically resolves artifact kind;
6. specialized Receipt schema identity deterministically resolves primary Receipt kind;
7. no universal artifact_kind field is required;
8. no universal Receipt-kind discriminator is required;
9. unknown root schema identities fail closed;
10. unknown root schema versions fail closed;
11. historical schema meaning remains immutable;
12. unknown top-level fields are rejected unless explicitly permitted;
13. Null and absent remain distinguishable;
14. schema-valid remains distinct from valid issuance;
15. schema-valid remains distinct from authority;
16. schema-valid remains distinct from Canonical Membership;
17. schema-valid remains distinct from Evidence;
18. schema-valid remains distinct from cryptographic validity;
19. provenance is not collapsed into one universal representation;
20. processing lineage remains distinct from independent corroboration;
21. Observation binds an identified source and observation value;
22. Validation Result binds evaluated subject, validation contract, and result;
23. Qualification Result binds evaluated subject, qualification contract, and result;
24. Attestation binds source and assertion;
25. Proposal carries proposed semantic material without effecting the proposal;
26. Relationship binds subjects and represented relationship without creating authority;
27. Authority Grant binds grantee, authority dimension, and authority root;
28. the Authority Grant schema admits the twelve and only the twelve frozen authority dimensions;
29. Authorization requires operation, scope, subject, authority source, and conditions;
30. Capability remains distinct from Permission and Authorization;
31. Schema Artifact distinguishes its own schema binding from the governed schema it represents;
32. Policy Root representation does not manufacture authority;
33. Projection remains distinct from source;
34. Integrity Epoch Record existence does not prove integrity;
35. all five Receipt subtypes remain Receipt Artifacts;
36. Receipt representation remains distinct from the occurrence claim it records;
37. cryptographic members are not universal;
38. private-key material is excluded from production artifact schemas;
39. no ambient timestamps or metadata are silently injected;
40. machine-checkable positive fixtures exist for all eighteen root schemas;
41. machine-checkable negative fixtures exercise required structural failures;
42. cross-schema confusion is rejected;
43. Receipt subtype confusion is rejected;
44. schema fixtures compose deterministically with ACS-1;
45. cryptographic schema fixtures preserve the ACBP-1 constitutional boundary where applicable;
46. a machine-checkable schema registry manifest binds every initial root schema;
47. schema implementation remains subordinate to SW0-001 through SW0-005.

All SW0-006 closure conditions have been proven. This contract is frozen as SW0-006.