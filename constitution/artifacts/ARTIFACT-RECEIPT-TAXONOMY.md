# Artifact and Receipt Taxonomy

Status: FROZEN - SW0-003

## 1. Purpose

This contract defines the constitutional taxonomy for artifacts, artifact kinds, artifact classifications, evidence roles, receipt kinds, and related accountability material within the AnarchI Brain.

It is subordinate to:

- AnarchI Semantic Language v1, frozen by SW0-001
- Authority Dimensions, frozen by SW0-002

This contract defines constitutional distinctions.

It does not define:

- database tables
- storage engines
- wire encodings
- identifier formats
- serialization byte order
- cryptographic profiles
- state-machine implementations
- provider-specific representations

Those concerns belong to later STONEWALL-0 deliverables.

## 2. Artifact

An Artifact is a governed and distinguishable representation of material that may participate in relationships, provenance, processing lineage, lifecycle classification, authority processes, or canonical processes.

Artifact existence does not imply:

- truth
- evidence status
- qualification
- authorization
- permission
- capability
- canonical membership
- semantic validity
- current authority
- successful execution
- storage at any particular location

An Artifact may exist before it becomes canonical.

An Artifact may remain permanently noncanonical.

An Artifact may be quarantined.

An Artifact may be historical or derived.

Artifact identity, storage location, semantic meaning, canonical membership, evidence role, and authority are distinct concerns.

A type label alone does not establish that an artifact validly possesses the semantics claimed by that label.

## 3. Taxonomic Axes

Artifact interpretation is multidimensional.

The following axes must remain distinct:

- artifact kind
- artifact family
- canonicality classification
- evidence role
- temporal classification
- derivation classification
- provenance
- processing lineage
- storage presence
- authority status
- semantic validity

No axis silently determines another.

An Artifact may therefore be, for example:

- an Observation Artifact;
- admitted as Evidence under one evidence contract;
- noncanonical in one canonical domain;
- canonical in another canonical domain;
- derived from another artifact;
- historically retained;
- physically stored in one or more substrates.

Those properties do not collapse into one property merely because they apply to the same Artifact.

## 4. Artifact Families

Artifact families are descriptive groupings.

Artifact family membership does not grant authority.

The initial constitutional families are:

### Epistemic Artifacts

Artifacts representing bounded observations, evaluations, or attributable assertions.

Initial kinds:

- Observation Artifact
- Validation Result Artifact
- Qualification Result Artifact
- Attestation Artifact

### Intent and Structural Artifacts

Artifacts describing proposed change or explicit relationships.

Initial kinds:

- Proposal Artifact
- Relationship Artifact

### Governance Artifacts

Artifacts participating directly in bounded governance, authority, capability, schema, or policy interpretation.

Initial kinds:

- Authority Grant Artifact
- Authorization Artifact
- Capability Artifact
- Schema Artifact
- Policy Root Artifact

### Projection Artifacts

Artifacts representing derived views or presentations.

Initial kind:

- Projection Artifact

### Accountability Artifacts

Artifacts whose primary purpose is durable accountability for governed activity or integrity context.

Initial kinds:

- Receipt Artifact
- Integrity Epoch Record Artifact

## 5. Observation Artifact

An Observation Artifact represents an Observation under the frozen semantic meaning of SW0-001.

An Observation Artifact records what an identified source perceived, measured, received, or reported.

Its existence does not establish:

- truth
- Evidence status
- corroboration
- qualification
- authorization
- canonical membership
- permission to act

An Observation Artifact may later be admitted as Evidence under an applicable evidence contract without changing its artifact kind.

## 6. Validation Result Artifact

A Validation Result Artifact records the bounded result of a validation lifecycle defined by an applicable governing contract.

SW0-003 does not define the complete semantics of validation.

Those semantics belong to the applicable S0 validation state machine and supporting contracts.

A Validation Result Artifact does not automatically imply:

- Evidence status
- Qualification
- Authorization
- Canonicalization
- canonical membership
- truth

Validation Result Artifact is distinct from Qualification Result Artifact unless a later governing contract explicitly defines a bounded relationship.

## 7. Qualification Result Artifact

A Qualification Result Artifact records the result of a Qualification performed under an applicable qualification contract.

It must remain attributable to the governing qualification context.

A Qualification Result Artifact does not automatically:

- authorize a consequential transition
- canonicalize evaluated material
- convert the evaluated material into truth
- grant authority
- become an Attestation
- become Evidence merely because the evaluation occurred

The evaluated material and the Qualification Result Artifact remain distinguishable artifacts or material.

## 8. Attestation Artifact

An Attestation Artifact represents an Attestation under the frozen semantic meaning of SW0-001.

It records an attributable assertion regarding a defined subject and scope.

An Attestation Artifact does not become true merely because:

- it exists
- it is signed
- it is stored
- it is canonical
- its producer possesses authority in another dimension

Attestation authority must be independently valid for the attestation to possess constitutional attesting authority.

## 9. Proposal Artifact

A Proposal Artifact represents a Proposal for a possible state, relationship, operation, interpretation, or transition.

A Proposal Artifact expresses possible change.

It does not authorize itself.

Canonical membership of a Proposal Artifact does not make the proposed change effective.

Storage of a Proposal Artifact does not make the proposed change effective.

Repeated copying or processing of a Proposal Artifact does not create independent authority for the proposal.

## 10. Relationship Artifact

A Relationship Artifact represents a declared relationship between identified subjects or artifacts.

A Relationship Artifact may describe:

- association
- derivation
- dependency
- reference
- qualification target
- proposal target
- authority relationship
- projection source
- other explicitly governed relationship semantics

The existence of a Relationship Artifact does not prove that the represented relationship is true, authoritative, canonical, or currently effective.

A Relationship Artifact may itself require qualification, authorization, or canonicalization according to its governing contract.

A Relationship Artifact must not silently create authority between its subjects.

## 11. Authority Grant Artifact

An Authority Grant Artifact represents an explicitly bounded authority grant governed by SW0-002.

Its artifact representation must not be confused with effective authority.

Mere possession, storage, copying, reconstruction, or presentation of something shaped like an Authority Grant Artifact does not establish that the grant is valid.

Effective authority requires a valid authority path to an applicable authority root.

An Authority Grant Artifact must not silently:

- enlarge itself
- reinterpret itself
- renew itself
- replace its authority root
- grant additional dimensions
- grant authority outside its scope

A historical Authority Grant Artifact does not establish current effective authority.

## 12. Authorization Artifact

An Authorization Artifact represents an Authorization for a bounded consequential transition.

Its validity depends upon the applicable authority contract and effective authorize authority.

A representation claiming to be an Authorization Artifact does not authorize anything merely because it contains authorization-shaped fields.

An Authorization Artifact must bind or deterministically resolve the operation, scope, subject, authority source, and conditions required by its governing contract.

Authorization Artifact is distinct from:

- Proposal Artifact
- Qualification Result Artifact
- Authority Grant Artifact
- Capability Artifact
- Receipt Artifact

A Receipt recording issuance of an Authorization does not replace the Authorization Artifact itself unless a later governing contract explicitly defines a combined representation without collapsing their meanings.

## 13. Capability Artifact

A Capability Artifact represents a bounded means through which an operation can be exercised.

Capability Artifact does not imply:

- permission
- authorization
- authority
- successful execution
- canonical membership
- unrestricted operation

Possession of a Capability Artifact must not be treated as sufficient proof that its exercise is permitted.

A revoked, expired, invalid, or otherwise ineffective capability must not regain effectiveness merely because an older Capability Artifact remains stored.

## 14. Schema Artifact

A Schema Artifact represents a governed schema and its interpretation rules.

Schema Artifact semantics remain subject to the frozen historical-meaning rules of SW0-001.

A Schema Artifact must not silently redefine the historical meaning of material governed by an earlier schema version.

Storage presence of a Schema Artifact does not make that schema applicable.

Canonical membership of a Schema Artifact does not automatically make it applicable to every artifact or domain.

Applicability must be resolved through the governing contracts.

## 15. Policy Root Artifact

A Policy Root Artifact represents a policy root or policy-root definition used by an applicable governance regime.

Its existence does not automatically establish applicability or supremacy.

A Policy Root Artifact does not acquire constitutional authority merely because:

- it is stored
- it is named as a root
- an administrator created it
- a model generated it
- it appears in configuration
- it is referenced by an unrelated artifact

Applicability and authority must resolve through the governing authority path.

The complete lifecycle of schema and policy roots belongs to the schema/policy-root state machine.

## 16. Projection Artifact

A Projection Artifact represents a Projection under the frozen semantic meaning of SW0-001.

A Projection Artifact is derived from permitted underlying material.

It may omit, transform, organize, summarize, or render that material according to its governing contract.

Projection does not mutate its source merely because a Projection Artifact exists.

A Projection Artifact does not inherit from its source:

- canonical membership
- Evidence status
- authority
- permission
- capability
- attestation authority
- truth

Any inherited property must be explicitly defined by the governing contract.

## 17. Receipt Artifact

A Receipt Artifact represents a Receipt under the frozen semantic meaning of SW0-001.

Its purpose is durable accountability for a defined occurrence recorded as having occurred.

Receipt Artifact is not automatically:

- Evidence
- truth
- Authorization
- Authority Grant
- Attestation
- canonical membership
- proof of correctness
- proof of successful execution
- proof of effective authority

A Receipt Artifact records an occurrence claim.

The existence of the Receipt Artifact and the validity of the occurrence it records remain distinguishable questions.

## 18. Integrity Epoch Record Artifact

An Integrity Epoch Record Artifact records a bounded integrity epoch, integrity context, or integrity-boundary event defined by the future integrity epoch lifecycle.

SW0-003 reserves this artifact kind because the core state-machine registry requires an integrity epoch lifecycle.

SW0-003 does not define the complete integrity epoch state machine.

An Integrity Epoch Record Artifact does not prove system integrity merely because the record exists.

Any integrity claim carried by such an artifact remains subject to its governing contract, provenance, authority, and required evidence.

## 19. Semantic Concepts That Are Not Artifact Kinds

The following constitutional concepts are not defined as first-class artifact kinds by SW0-003:

### Evidence

Evidence is a contextual role of material admitted under an applicable evidence contract.

Evidence is not a permanent intrinsic artifact kind.

An Observation Artifact, Receipt Artifact, Attestation Artifact, or other permitted material may become Evidence only through the applicable evidence process.

Evidence status under one evidence contract does not automatically create Evidence status under another.

### Permission

Permission is policy state.

Permission is not defined by SW0-003 as a universal artifact kind.

A future schema may represent permission state, but the representation and the effective policy state must remain distinguishable.

### Canonicalization

Canonicalization is a consequential transition.

It is not an artifact kind.

The transition may consume and emit governed artifacts and receipts.

### Canonical Membership

Canonical Membership is a governed classification within a defined canonical domain.

It is not an artifact kind.

### Memory

Memory is retained state or material.

It is not an artifact kind.

### Storage Presence

Storage Presence is physical or substrate presence.

It is not an artifact kind.

### Migration

Migration is a governed operation or transition.

It is not itself an artifact kind.

Migration may produce:

- migrated artifacts
- provenance relationships
- processing lineage
- receipts

The migrated result does not become canonical merely because migration succeeded.

### Reconstruction

Reconstruction is a governed operation.

It is not itself an artifact kind.

Reconstruction may produce an artifact of an existing kind.

The reconstructed artifact does not inherit canonicality, authority, Evidence status, or validity merely from successful reconstruction.

### Execution

Execution is an operation or attempted operation.

It is not an artifact kind.

Execution may emit receipts or other governed results.

### Revocation

Revocation is a governed authority-state transition.

It is not itself an artifact kind.

A revocation process may consume governance artifacts and emit receipts.

A receipt recording revocation does not itself possess revoke authority.

### Provenance

Provenance is attributable history.

It is not required by SW0-003 to be a standalone artifact kind.

Provenance may be represented by governed relationships, fields, references, or later schemas without changing its semantic meaning.

### Processing Lineage

Processing Lineage is derivation history through processing steps, agents, systems, or representations.

It is not required by SW0-003 to be a standalone artifact kind.

Processing lineage does not create independent corroboration.

### Corroboration

Corroboration is an independence-qualified relationship between supporting material.

It is not an artifact kind.

Repeated descendants of one lineage do not become independent corroboration by receiving different artifact identities.

## 20. Canonicality Classification

Canonicality classification is independent from artifact kind.

Canonicality is evaluated relative to a defined canonical domain.

An artifact may therefore have different canonicality classifications in different domains.

The initial canonicality classifications are:

### Canonical

The artifact or eligible material has been explicitly admitted to canonical membership in the identified canonical domain by the applicable canonical process.

Canonical does not imply universal truth.

### Noncanonical

The artifact or eligible material has been explicitly classified as not belonging to the identified canonical domain.

Noncanonical must not be inferred merely because canonical membership cannot be found.

### Quarantined

The artifact or eligible material is explicitly held in a quarantine classification under an applicable governing rule.

Quarantine does not inherently mean:

- false
- malicious
- corrupt
- permanently rejected
- noncanonical in every domain

The reason for quarantine must be governed independently.

### Unresolved

The effective canonicality classification cannot currently be deterministically resolved.

Unresolved must not silently become canonical.

Unresolved must not silently become noncanonical.

Where an operation requires known canonical membership, unresolved classification must fail closed.

Canonical, noncanonical, quarantined, and unresolved are classifications.

They are not artifact kinds.

## 21. Temporal Classification

Historical is a temporal classification.

Historical is not a canonicality classification.

An artifact may be both historical and canonical.

An artifact may be historical and noncanonical.

An artifact may be historical and quarantined.

Historical retention does not restore expired authority, permission, or capability.

A historical artifact retains the historical meaning applicable to its governing semantic version.

## 22. Derivation Classification

Derived describes a lineage relationship or derivation condition.

Derived is not a canonicality classification.

A derived artifact does not automatically inherit from its source:

- canonical membership
- Evidence status
- authority
- authorization
- permission
- capability
- attestation validity
- corroboration independence

Any inheritance must be explicitly defined by the applicable governing contract.

Multiple derived artifacts from one source lineage do not become independent corroboration merely because they have distinct artifact identities.

## 23. Evidence Role

Evidence status is contextual and contract-bound.

An artifact may be admitted as Evidence under one contract while remaining unadmitted under another.

Evidence admission does not change the underlying artifact kind.

Evidence admission does not automatically change canonicality classification.

Canonicalization does not automatically create Evidence status.

A Receipt Artifact may become Evidence only through an explicit evidence process.

An Observation Artifact may become Evidence only through an explicit evidence process.

An Attestation Artifact may become Evidence only through an explicit evidence process.

Evidence role must preserve provenance and applicable independence requirements.

## 24. Receipt Taxonomy

Every Receipt Artifact must identify or deterministically resolve a primary receipt kind.

The initial receipt kinds are:

### Event Receipt

Records that a defined event was recorded as having occurred.

An Event Receipt does not independently prove the event was truthful, valid, authorized, or canonical.

### Decision Receipt

Records that a defined decision was recorded as having been made.

A Decision Receipt does not replace the decision artifact when a distinct decision artifact is required.

A Decision Receipt does not prove that the decision-maker possessed valid authority.

### Attempt Receipt

Records that a defined operation or action was attempted.

Attempt does not imply success.

Attempt does not imply authorization.

Attempt does not imply an external effect occurred.

### Transition Receipt

Records that a defined transition was recorded as having occurred or been applied.

A Transition Receipt does not independently establish that the transition was legal, authorized, canonical, or valid.

The applicable state machine determines transition validity.

### Effect Receipt

Records that a defined effect was recorded as having occurred or been observed.

An Effect Receipt does not automatically prove causal attribution.

An Effect Receipt does not automatically prove that the operation producing the effect was authorized.

## 25. Receipt Boundaries

A Receipt Artifact records accountability information.

It must not silently become the universal container for every semantic object.

The following distinctions are mandatory:

- receipt != occurrence
- receipt != Evidence
- receipt != Authorization
- receipt != Authority Grant
- receipt != Capability
- receipt != Proposal
- receipt != Attestation
- receipt != canonical membership
- receipt != semantic validity

A Receipt Artifact may reference another artifact without becoming that artifact.

A Receipt Artifact may record creation, issuance, evaluation, transition, execution, failure, or effect involving another artifact without replacing that artifact's semantic kind.

A receipt of an unauthorized action does not make the action authorized.

A receipt of an invalid transition does not make the transition valid.

A receipt of storage does not make stored material canonical.

## 26. Provenance and Processing Lineage

Every artifact kind may participate in provenance and processing lineage.

Provenance records attributable origin, derivation, transformation, custody, or relevant processing history.

Processing Lineage records derivation through processing operations, agents, systems, or representations.

Provenance and Processing Lineage remain distinct from:

- truth
- Evidence status
- corroboration
- authority
- canonical membership
- semantic validity

Copying an artifact creates no independent corroboration by itself.

Transforming an artifact creates no independent corroboration by itself.

Reconstructing an artifact creates no independent corroboration by itself.

Migrating an artifact creates no independent corroboration by itself.

Projection creates no independent corroboration by itself.

## 27. Representation and Valid Issuance

Artifact representation is distinct from valid issuance.

A byte sequence, object, record, file, message, or database row that resembles an artifact kind does not acquire that artifact kind's constitutional consequences merely because it has matching fields.

Where an artifact kind carries authority-bearing or governance consequences, valid issuance must resolve through the applicable governing contract and authority path.

This rule applies especially to:

- Authority Grant Artifact
- Authorization Artifact
- Capability Artifact
- Attestation Artifact
- Policy Root Artifact

Serialization correctness does not itself establish valid issuance.

Signature validity does not itself establish authority.

Storage presence does not itself establish valid issuance.

Canonical membership does not retroactively repair invalid issuance unless an explicit constitutional process defines such repair.

## 28. Artifact Kind and Canonical Membership

Artifact kind and canonical membership are independent.

Canonicalizing an Artifact does not change its artifact kind unless an explicit governed migration creates a new artifact under a different schema or semantic version.

A Proposal Artifact remains a Proposal Artifact after canonicalization.

An Observation Artifact remains an Observation Artifact after Evidence admission.

A Receipt Artifact remains a Receipt Artifact if later admitted as Evidence.

A Projection Artifact remains a Projection Artifact if separately admitted to a canonical domain.

No canonical process may silently rewrite an artifact's historical semantic kind.

## 29. Unknown and Future Artifact Kinds

Future artifact kinds may be introduced only by an explicit governing contract and compatible semantic versioning process.

Unknown artifact kinds must not be interpreted as known artifact kinds.

Unknown artifact kinds must not silently receive:

- canonical membership
- Evidence status
- authority
- authorization
- permission
- capability
- semantic validity

Where compatible preservation is required, unknown artifact kinds and unknown compatible fields must remain representable without acquiring invented meaning.

Historical artifact-kind meaning is immutable.

## 30. Constitutional Artifact Laws

The following laws are mandatory:

- artifact != truth
- artifact kind != canonicality
- artifact kind != Evidence status
- artifact identity != storage location
- storage presence != canonical membership
- Evidence is a contextual role, not an intrinsic artifact kind
- canonical is a classification, not an artifact kind
- noncanonical is a classification, not an artifact kind
- quarantine is a classification, not an artifact kind
- unresolved canonicality must not become canonical by default
- unresolved canonicality must not become noncanonical by default
- historical is not canonicality
- derived is not canonicality
- derived artifacts do not automatically inherit source authority
- derived artifacts do not automatically inherit source canonicality
- derived artifacts do not automatically inherit source Evidence status
- receipt != occurrence
- receipt != Evidence
- receipt != Authorization
- receipt != Authority Grant
- receipt != canonical membership
- receipt != semantic validity
- receipt of execution != authorization
- receipt of storage != canonicalization
- proposal canonicality != proposal effectiveness
- relationship existence != relationship truth
- authority-grant representation != effective authority
- authorization representation != valid authorization
- capability possession != permission
- projection != source mutation
- provenance != corroboration
- processing lineage != independent corroboration
- migration success != canonicalization
- reconstruction success != canonicalization
- artifact type labels do not self-establish constitutional validity
- cognition does not create artifact authority merely by generating an artifact

## 31. Relationship to Later State Machines

SW0-003 defines taxonomy.

It does not define full lifecycle behavior.

Later state-machine contracts remain responsible for:

- ingress behavior
- validation behavior
- qualification behavior
- evidence admission
- proposal handling
- relationship handling
- canonicalization
- memory classification
- processing
- transitions
- projection
- egress
- authority grants
- capabilities
- receipts
- schema and policy roots
- migration
- reconstruction
- integrity epochs
- revocation

Those state machines may consume and emit artifacts defined here.

They must not silently redefine the artifact meanings frozen by this taxonomy.

## 32. SW0-003 Closure Conditions

SW0-003 may close only when machine-checkable evidence demonstrates that:

1. Artifact has an explicit implementation-independent meaning.
2. artifact kind is separated from canonicality, Evidence role, provenance, lineage, storage presence, authority, and semantic validity.
3. initial first-class artifact kinds are uniquely defined.
4. Evidence is treated as a contextual role rather than an intrinsic artifact kind.
5. canonical, noncanonical, quarantined, and unresolved are classifications rather than artifact kinds.
6. historical and derived remain orthogonal to canonicality.
7. Receipt Artifact has explicit non-collapse boundaries.
8. all five initial receipt kinds are uniquely defined.
9. Receipt does not automatically become Evidence, Authorization, canonical membership, or semantic validity.
10. derived artifacts do not automatically inherit source authority, canonicality, Evidence status, or corroboration independence.
11. representation is separated from valid issuance.
12. unknown future artifact kinds cannot silently acquire known meaning or authority.
13. migration, reconstruction, execution, canonicalization, and revocation remain operations or transitions rather than artifact kinds.
14. taxonomy remains compatible with the currently enumerated STONEWALL-0 state-machine registry.
15. this contract remains subordinate to the frozen meanings of SW0-001 and SW0-002.

These closure conditions have been proven for SW0-003. This artifact and receipt taxonomy is frozen.