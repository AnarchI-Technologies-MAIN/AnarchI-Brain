# SW0-008 Substrate-fin Boundary Contract

Status: FROZEN - SW0-008

## 1. Purpose

This contract defines the constitutional boundary of Substrate-fin within the AnarchI Brain.

Substrate-fin is the persistence-side boundary between physical storage or representation and constitutionally governed meaning, authority, canonical state, migration, reconstruction, and integrity state.

Substrate-fin does not define constitutional meaning merely by storing, indexing, locating, retaining, copying, or otherwise physically representing material.

This contract defines boundary semantics only.

It does not implement a database, persistence service, migration engine, reconstruction engine, integrity engine, or canonical-memory runtime.

## 2. Gate Ownership

SW0-008 owns Substrate-fin boundary semantics.

SW0-008 does not own the final Organ Authority Matrix.

SW0-008 does not own the complete migration lifecycle.

SW0-008 does not own the complete reconstruction lifecycle.

SW0-008 does not own the complete integrity epoch lifecycle.

SW0-009 owns the final Organ Authority Matrix.

SW0-010 owns the complete state-machine specifications, including migration, reconstruction, and integrity epoch lifecycles.

This contract must not silently absorb either later gate.

## 3. Physical Persistence Boundary

Storage Presence means physical or substrate presence.

Physical persistence establishes only that bytes, records, objects, or equivalent representations exist within a substrate.

Physical persistence does not by itself establish:

- constitutional meaning;
- Artifact identity;
- valid issuance;
- authority;
- Authorization;
- Permission;
- Evidence status;
- Canonical Membership;
- schema applicability;
- truth;
- integrity.

The substrate must not manufacture constitutional consequences from physical presence alone.

## 4. Semantic Independence

No database, filesystem, runtime, provider, transport, serialization library, or deployment substrate defines the meaning of a constitutional term merely by representing or processing it.

No implementation-specific database representation may define constitutional semantics.

A storage implementation may represent governed material.

Its representation remains subordinate to the applicable frozen constitutional contracts.

Changing physical representation must not silently redefine semantic meaning.

## 5. Storage Presence and Canonical Membership

Storage Presence is distinct from Canonical Membership.

Physical location is distinct from Canonical Membership.

A database row does not become canonical merely because it exists.

A file does not become canonical merely because it exists.

An indexed object does not become canonical merely because it is retrievable.

Canonical Membership is determined by the governing canonical process, authority path, and lifecycle.

Where known Canonical Membership is required and cannot be resolved, the consequential operation must fail closed.

## 6. Canonical Classification Boundary

Canonical, noncanonical, quarantined, and unresolved are governed classifications.

Substrate-fin must not infer Canonical Membership from storage presence.

Substrate-fin must not infer noncanonical classification merely because Canonical Membership cannot be found.

Unresolved must not silently become canonical.

Unresolved must not silently become noncanonical.

Quarantine must not silently become invalidity, falsehood, or another classification merely because material is physically segregated.

Preservation or relocation must not silently change the governing classification.

## 7. Valid Issuance Boundary

Storage presence does not itself establish valid issuance.

Possession, copying, indexing, retention, backup, restoration, or physical reconstruction of a representation does not establish valid issuance merely because the representation remains available.

A representation shaped like a governed Artifact does not acquire the constitutional consequences of that Artifact kind merely because matching fields are stored.

Issuance remains governed independently from persistence.

## 8. Schema Applicability Boundary

Schema storage does not establish schema applicability.

Storage presence of a Schema Artifact does not make the represented schema applicable.

Canonical Membership of a Schema Artifact does not automatically make that schema applicable to every artifact or domain.

Schema identity is not merely a database table.

A database table name, filesystem path, package name, registry entry, or storage identifier must not silently determine schema interpretation.

## 9. Database Representation Boundary

Database tables and columns must not define constitutional schema semantics.

A database may store or index governed fields.

Database representation remains implementation organization.

Row identity, table identity, column type, index ordering, storage order, database identifiers, and database-specific constraints must not silently redefine constitutional meaning.

Database representation is subordinate to frozen semantic, schema, serialization, authority, and lifecycle contracts.

## 10. Registry and Index Boundary

A database registry, filesystem registry, package registry, API registry, index, or lookup structure may assist retrieval or resolution where permitted.

Registry presence does not establish applicability.

Index presence does not establish Canonical Membership.

Lookup preference does not establish authority.

Current database row preference must not silently replace governed resolution semantics.

Filesystem ordering must not silently replace governed resolution semantics.

Operational convenience does not become constitutional precedence.

## 11. Serialization and Stored Representation

Storage of ACS-1 canonical bytes does not perform Canonicalization.

Reconstructing identical ACS-1 canonical bytes does not perform Canonicalization.

Canonical bytes do not imply Canonical Membership.

Filesystem newline translation, database text encoding, storage encoding, or implementation representation must not redefine ACS-1 semantics.

A persistence layer must not treat an implementation-specific representation as the constitutional source of semantic meaning.

## 12. Time Boundary

Filesystem time is not trusted semantic time.

Database time is not trusted semantic time.

Transport time is not trusted semantic time.

Model-generated time is not trusted semantic time.

Filesystem timestamps are not trusted signature time.

Database timestamps are not trusted signature time.

Storage recency must not silently become semantic precedence, schema applicability, authority, or truth.

Trusted time, where required, must come from the applicable governing contract.

## 13. Substrate Authority Boundary

A storage substrate possesses no constitutional authority merely because it exists, observes state, controls infrastructure, performs computation, stores material, or is technically capable of an operation.

Administrative control of a substrate does not redefine the constitutional meaning of material stored or processed by that substrate.

Infrastructure ownership does not establish semantic authority.

Database administration does not establish Canonicalize authority.

Filesystem administration does not establish Migrate authority.

Operational capability does not establish constitutional authority.

Required authority must resolve through the applicable authority path.

If required authority cannot be resolved, the consequential transition must fail closed.

## 14. Consequential Transition Boundary

A physical storage operation is not automatically a constitutional transition.

Where an operation can change canonical state, authority, permissions, capabilities, externally observable effects, integrity state, or other constitutionally protected state, the operation is subject to the applicable consequential-transition governance.

The substrate's technical ability to perform an operation does not authorize that operation.

Successful persistence does not retroactively authorize a consequential transition.

Successful retrieval does not establish that the retrieved material may be constitutionally acted upon.

## 15. Migration Boundary

Migration is an explicitly governed transformation or relocation of material between identified schemas, versions, representations, or substrates.

Migration is not inferred merely from movement of bytes.

Physical relocation alone is not semantic Migration.

A database migration does not automatically constitute a constitutional schema Migration.

Copying material from one substrate to another does not automatically constitute a semantic Migration.

Migration must preserve the semantic obligations defined by its governing contract.

Migration success does not perform Canonicalization.

## 16. Migrate Authority Boundary

Migrate authority governs the migration operation.

Migrate authority does not imply ownership of migrated material.

Migrate authority does not inherently imply Canonicalize authority.

Migrate authority does not permit changing semantic meaning outside the governing migration contract.

Migrate authority does not permit reconstruction of missing authority.

Migrate authority does not permit invention of missing authority history.

Possession of migration capability is not equivalent to Migrate authority.

Where required Migrate authority cannot be resolved, the migration must fail closed.

## 17. Historical Meaning Across Migration

Migration must not silently rewrite the historical meaning of original material.

Migration between serialization profiles does not rewrite the historical meaning of the original material.

A newly migrated representation must not retroactively redefine the semantic meaning under which its source representation previously existed.

Historical provenance and current representation remain distinguishable.

A later storage format must not silently reinterpret earlier governed state.

## 18. Reconstruction Boundary

Reconstruction is a governed operation.

Reconstruction may derive or rebuild state or representation only from permitted inputs under its governing contract.

Ability to reconstruct does not confer authority to perform reconstruction.

Successful reconstruction does not by itself establish:

- Canonical Membership;
- authority;
- Authorization;
- Permission;
- Evidence status;
- valid issuance;
- truth;
- validity.

Reconstruction success does not perform Canonicalization.

## 19. Reconstruct Authority Boundary

Reconstruct authority is distinct from technical reconstruction capability.

Reconstruct authority does not inherently imply Migrate authority.

Reconstruct authority does not inherently imply Canonicalize authority.

Reconstruct authority does not permit creation of missing authority history.

A successfully reconstructed result remains subject to whatever qualification, authorization, canonicalization, attestation, and other requirements its governing contract requires.

Where required Reconstruct authority cannot be resolved, reconstruction must fail closed.

## 20. Reconstruction and Corroboration

Reconstructing an artifact creates no independent corroboration by itself.

A reconstructed copy derived from existing material does not become an independent source merely because it was regenerated.

Repeated reconstruction does not increase evidentiary independence.

Physical redundancy is distinct from independent corroboration.

Recovery availability must not be mistaken for epistemic independence.

## 21. Integrity Epoch Boundary

An Integrity Epoch Record Artifact records a bounded integrity epoch, integrity context, or integrity-boundary event under its applicable lifecycle.

Existence of an Integrity Epoch Record Artifact does not prove system integrity.

Storage of an Integrity Epoch Record Artifact does not prove system integrity.

Cryptographic validity of governed material does not by itself prove complete system integrity.

Any integrity claim remains subject to its governing contract, provenance, authority, required evidence, and lifecycle.

The complete integrity epoch lifecycle belongs to SW0-010.

## 22. Cryptographic Integrity Compatibility

The frozen cryptographic profile reserves the ACBP-1 purpose:

integrity-epoch

Where later lifecycle work uses that purpose, cryptographic binding must remain distinct from the constitutional validity of the represented integrity claim.

Hashing does not perform Canonicalization.

Signing does not perform Canonicalization.

Verification does not perform Canonicalization.

Storing a digest does not create Canonical Membership.

Storing a signature does not create Canonical Membership.

## 23. Unknown Material Preservation

Unknown schema material may be preserved only where the applicable governing transport or storage contract permits preservation.

Preserving unknown material does not assign invented semantic meaning.

Preserving unknown material does not make an unknown schema applicable.

Preserving unknown material does not establish valid issuance.

Preserving unknown material does not create Canonical Membership.

Preserving unknown material does not resolve unresolved authority.

Substrate-fin must remain capable of preserving constitutional uncertainty without silently converting uncertainty into a known conclusion.

## 24. Quarantine and Unresolved Preservation

Physical segregation may support a governed quarantine classification, but physical segregation does not itself define that classification.

Quarantined material remains governed material.

Unresolved material remains unresolved until the applicable process resolves it.

Historical retention does not restore expired authority, Permission, or capability effectiveness.

Retention must not silently reactivate revoked, expired, invalid, or otherwise ineffective constitutional state.

Storage availability is not current effectiveness.

## 25. Cortex Continuity Boundary

Cortex storage does not create Canonical Membership.

Material transferred from Cortex into Substrate-fin does not gain constitutional authority, valid issuance, Canonical Membership, schema applicability, or integrity merely because the handoff succeeds.

Material retrieved from Substrate-fin into Cortex does not regain constitutional effectiveness merely because it becomes operationally available again.

Cortex and Substrate-fin remain jointly subordinate to the applicable authority, canonicalization, schema, migration, reconstruction, and state-machine contracts.

Transport between constitutional components must not upgrade semantic status.

## 26. Key Custody Exclusion

Private-key generation, custody, storage, hardware binding, recovery, rotation, destruction, and access control belong to dedicated key-management contracts and substrates.

SW0-008 does not define a private-key storage format.

SW0-008 does not define key custody authority.

Generic persistence capability must not silently become cryptographic key-custody authority.

## 27. Implementation Wall

SW0-008 defines Substrate-fin boundary semantics only.

SW0-008 does not authorize or implement:

- database schema design;
- PostgreSQL schema implementation;
- persistence-service implementation;
- canonical-memory implementation;
- migration-engine implementation;
- reconstruction-engine implementation;
- integrity-epoch implementation;
- runtime orchestration;
- database deployment;
- persistence infrastructure deployment.

Implementation remains downstream of the applicable STONEWALL gates.

## 28. Substrate-fin Non-Collapse Laws

The following distinctions are mandatory:

- storage presence != constitutional meaning;
- storage presence != Canonical Membership;
- physical location != Canonical Membership;
- storage presence != valid issuance;
- database representation != constitutional meaning;
- database table != constitutional schema identity;
- schema storage != schema applicability;
- registry presence != semantic applicability;
- database time != trusted semantic time;
- filesystem time != trusted semantic time;
- substrate control != semantic authority;
- administrative control != unrestricted constitutional authority;
- database migration != constitutional Migration;
- physical relocation != semantic Migration;
- migration success != Canonicalization;
- Migrate authority != ownership;
- Migrate authority != unrestricted semantic reinterpretation;
- migration != rewriting historical meaning;
- reconstruction ability != Reconstruct authority;
- reconstruction success != Canonicalization;
- reconstruction success != inherited authority;
- reconstruction != independent corroboration;
- Integrity Epoch Record != proved system integrity;
- preservation of unknown material != interpretation;
- persistence availability != constitutional effectiveness.

## 29. SW0-008 Closure Conditions

SW0-008 may close only when machine-checkable evidence demonstrates that:

1. Storage Presence remains a physical or substrate-presence fact only.
2. database, filesystem, runtime, transport, or deployment representation does not define constitutional semantics.
3. Storage Presence remains distinct from Canonical Membership.
4. physical location remains distinct from Canonical Membership.
5. Storage Presence does not establish valid issuance.
6. database tables and columns do not define constitutional schema semantics.
7. a database may store or index governed fields without becoming their semantic authority.
8. stored Schema material does not become applicable merely because it is stored.
9. registries, indexes, and lookup structures do not silently redefine schema interpretation or semantic precedence.
10. filesystem and database time do not silently become trusted semantic time.
11. filesystem and database timestamps do not silently become trusted signature time.
12. a storage substrate does not acquire constitutional authority merely through existence, infrastructure control, computation, or operational capability.
13. administrative control of a substrate remains distinct from semantic authority.
14. canonical, noncanonical, quarantined, and unresolved remain governed classifications distinct from physical persistence.
15. unresolved canonicality does not silently become canonical.
16. unresolved canonicality does not silently become noncanonical.
17. Migration remains an explicitly governed transformation or relocation.
18. physical relocation alone does not become semantic Migration.
19. database migration does not automatically become constitutional schema Migration.
20. Migration preserves the semantic obligations of its governing contract.
21. successful Migration does not perform Canonicalization.
22. Migrate authority governs the operation rather than ownership of migrated material.
23. Migrate authority does not permit semantic reinterpretation outside the governing migration contract.
24. Migration does not rewrite the historical meaning of original material.
25. Reconstruction remains a governed operation.
26. reconstruction capability remains distinct from Reconstruct authority.
27. successful Reconstruction does not automatically confer canonicality, authority, Evidence status, valid issuance, or validity.
28. Reconstruction does not create independent corroboration merely because material was regenerated.
29. migration or reconstruction authority does not permit creation of missing authority history.
30. existence or storage of an Integrity Epoch Record Artifact does not prove system integrity.
31. preservation of unknown material does not invent interpretation, schema applicability, valid issuance, Canonical Membership, or authority.
32. SW0-009 ownership of the final Organ Authority Matrix remains preserved.
33. SW0-010 ownership of the migration, reconstruction, and integrity epoch lifecycle specifications remains preserved.
34. SW0-008 does not implement database, PostgreSQL, persistence-service, migration, reconstruction, integrity-epoch, or canonical-memory runtime machinery.
35. the Substrate-fin non-collapse laws remain explicit and machine-testable.

Until these closure conditions are proven, SW0-008 remains a candidate.