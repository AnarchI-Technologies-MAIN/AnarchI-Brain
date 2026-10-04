# AnarchI Semantic Language v1

Status: FROZEN — SW0-001

## 1. Purpose

This contract defines the constitutional vocabulary used by the AnarchI Brain.

Its purpose is to prevent semantic collapse between concepts that may interact but do not confer one another's meaning, authority, or consequences.

These definitions are implementation-independent.

No database, filesystem, model, provider, runtime, transport, serialization library, or deployment substrate defines the meaning of a constitutional term.

## 2. Interpretation Rule

A constitutional term has only the authority and consequences explicitly assigned to it by the governing contracts.

Possession of one property does not imply another property unless an explicit legal transition establishes that relationship.

Absence of knowledge must not be silently interpreted as falsehood, rejection, permission, authorization, or canonical absence.

Unknown values and compatible unknown fields must remain representable where the governing schema permits them.

## 3. Epistemic Terms

### Observation

An Observation is a recorded claim that some source perceived, measured, received, or reported something.

An Observation records input.

Observation does not imply:

- truth
- evidence qualification
- authorization
- canonical membership
- permission to act

### Evidence

Evidence is material admitted for consideration under an applicable evidence contract.

Evidence may support, contradict, contextualize, or fail to resolve a claim.

Evidence does not become truth merely because it is admitted.

Evidence does not authorize a consequential transition unless a separate governing rule explicitly requires and consumes that evidence as part of an authorization process.

### Qualification

Qualification is the bounded evaluation of material against an explicit contract, policy, schema, or admissibility rule.

Qualification determines whether the evaluated material satisfies that qualification boundary.

Qualification is not canonicalization.

Qualification is not general authorization.

### Corroboration

Corroboration is independent support for a claim or material from a source or lineage that satisfies the applicable independence requirements.

Repeated processing, copying, transformation, storage, or restatement of the same lineage is not independent corroboration.

## 4. Intent and Change Terms

### Proposal

A Proposal is a request or candidate description for a possible state, relationship, operation, interpretation, or transition.

A Proposal expresses possible change.

A Proposal does not authorize itself.

### Authorization

Authorization is an explicit authority-bearing decision permitting a bounded consequential transition under an applicable contract.

Authorization must identify or deterministically bind the operation, scope, subject, authority source, and conditions required by its governing contract.

Authorization is not inferred from observation, proposal, qualification, capability, cognition, storage, or administrative access.

### Permission

Permission is the policy state describing whether an identified operation is allowed for an identified subject within an identified scope and context.

Permission does not prove that the subject possesses the capability to perform the operation.

Permission is not itself proof that an operation occurred.

### Capability

A Capability is a bounded means by which an operation can be exercised.

Capability describes exercisable power, not permission.

Possession of a capability does not independently authorize its exercise.

### Execution

Execution is the performance or attempted performance of an operation.

Execution does not retroactively create authorization.

Successful execution does not prove that the execution was authorized, canonical, truthful, or semantically valid.

## 5. Continuity Terms

### Canonicalization

Canonicalization is the authority-governed transition by which eligible material is admitted to canonical membership under an applicable canonicalization contract.

Canonicalization must be explicit and attributable.

Storage alone cannot canonicalize material.

### Canonical Membership

Canonical Membership is the recognized inclusion of an artifact, state, relationship, or other eligible material within a defined canonical domain.

Canonical membership is determined by the governing canonical process, not by physical location.

Canonical membership does not imply universal truth.

### Memory

Memory is retained state or material available for later continuity, interpretation, retrieval, or processing.

Memory may contain canonical, noncanonical, quarantined, historical, derived, or otherwise classified material.

Memory does not inherently possess action authority.

### Storage Presence

Storage Presence means only that bytes, records, objects, or equivalent representations exist in a storage substrate.

Storage presence does not imply:

- canonical membership
- truth
- qualification
- authorization
- semantic validity

### Reconstruction

Reconstruction is the process of deriving or rebuilding a state or representation from retained artifacts, receipts, evidence, canonical material, or other permitted inputs.

Ability to reconstruct does not confer authority to perform reconstruction.

A reconstructed result does not become canonical merely because reconstruction succeeded.

### Migration

Migration is an explicitly governed transformation or relocation of material between schemas, versions, representations, or substrates.

Migration must preserve the semantic obligations defined by its governing contract.

Physical relocation alone is not semantic migration.

## 6. Accountability Terms

### Receipt

A Receipt is a durable record that a defined event, decision, attempt, transition, or effect was recorded as having occurred.

A Receipt provides accountability for the event it describes.

A Receipt is not automatically Evidence.

A Receipt is not automatically proof that the recorded event was authorized, correct, truthful, or canonical.

### Attestation

An Attestation is an attributable assertion by an identified attesting authority or source regarding a defined subject.

Attestation records who asserts what under which applicable scope.

Attestation does not become truth solely because it is signed, stored, or authoritative in another dimension.

### Provenance

Provenance is the attributable history of origin, derivation, transformation, custody, or relevant processing relationships for material.

Provenance explains lineage.

Provenance does not independently establish truth or authorization.

### Processing Lineage

Processing Lineage records derivation through processing steps, transformations, agents, systems, or representations.

Multiple descendants of one lineage do not become independent corroboration merely because they were processed separately.

## 7. Interpretation Terms

### Schema

A Schema defines the permitted structure and interpretation rules for material governed by that schema.

A schema identifier and applicable version must be sufficient to resolve the intended historical interpretation under the governing contracts.

Historical schema meaning is immutable.

A later schema may supersede an earlier schema for new material but must not silently redefine the historical meaning of already-governed material.

### Semantic Version

A Semantic Version identifies a defined interpretation of a governed semantic contract or schema.

Version changes must not silently alter the meaning of historical material.

### Projection

A Projection is a derived presentation or bounded view of underlying material.

A Projection may omit, transform, organize, or render information according to its governing contract.

Projection does not alter canonical state merely by presenting it differently.

### Cognition

Cognition is reasoning, inference, generation, interpretation, planning, or similar model- or agent-produced processing.

Cognition may observe permitted context and produce bounded outputs such as assessments or proposals.

Cognition does not own canonical truth.

Cognition does not receive authority merely because it produced a useful, correct, confident, or persuasive result.

## 8. Governance Terms

### Authority

Authority is an explicitly granted and bounded right to perform or govern a defined class of consequential operations.

Authority is multidimensional.

Authority in one dimension does not imply authority in another.

Authority must be attributable to an applicable constitutional, policy, or delegated authority root.

### Authority Boundary

An Authority Boundary is an explicit separation at which authority must be independently established, checked, transferred, delegated, or denied before a governed operation may continue.

An authority boundary must not be satisfied merely by the component requesting or proposing the consequential transition unless the governing contract explicitly defines an independent authority mechanism.

### Administrator

An Administrator is an identity possessing explicitly granted administrative capabilities or permissions.

Administrative visibility, substrate control, or operational access does not inherently confer semantic authority, canonicalization authority, or truth ownership.

### Consequential Transition

A Consequential Transition is a governed operation capable of changing canonical state, authority, permissions, capabilities, externally observable effects, integrity state, or other constitutionally protected state.

Every consequential transition must eventually be bound to an explicitly enumerated state machine and authority path before STONEWALL-0 may close.

## 9. Constitutional Non-Collapse Laws

The following distinctions are mandatory:

- evidence != truth
- receipt != evidence
- capability != permission
- observation != authorization
- proposal != authorization
- qualification != canonicalization
- processing lineage != independent corroboration
- memory != action authority
- projection != canonical state
- cognition != truth ownership
- administrator visibility != semantic authority
- storage presence != canonical membership
- reconstruction ability != authority to reconstruct
- execution != authorization
- successful execution != semantic validity
- canonical membership != universal truth
- physical location != canonical membership
- repeated derivation != independent corroboration
- administrative control != semantic authority

No governing contract may silently collapse these distinctions.

If a later contract creates a relationship between two distinct concepts, that relationship must be explicit, bounded, and attributable.

## 10. Compatibility and Historical Meaning

Unknown future fields must survive compatible round-trip processing when the governing schema permits extension preservation.

Unknown fields must not silently acquire semantic meaning merely because they are preserved.

Historical schema meaning must remain immutable.

A future implementation may change representation without changing historical interpretation.

No implementation-specific database representation may define constitutional semantics.

## 11. SW0-001 Closure Conditions

SW0-001 may close only when machine-checkable evidence demonstrates that:

1. every mandatory non-collapse law is represented;
2. every defined constitutional term has an explicit bounded meaning;
3. no defined term silently grants authority belonging to another term;
4. unknown compatible fields are required to survive round-trip processing;
5. historical semantic meaning is immutable;
6. implementation-specific storage cannot define constitutional meaning;
7. consequential transition is explicitly connected to later state-machine enumeration.

These closure conditions have been proven for SW0-001. This semantic contract is frozen.


