# SW0-007 Cortex Contract Boundary

Status: FROZEN - SW0-007

## 1. Purpose

This contract defines the constitutional boundary of Cortex within the AnarchI Brain.

Cortex is a governed ingress and boundary participant.

This contract defines what Cortex may accept, resolve, preserve, request, propose, and participate in without collapsing identity, authority, capability, permission, authorization, canonicalization, receipts, transport, or execution into one another.

This contract does not implement Cortex.

## 2. Gate Ownership

SW0-007 owns Cortex boundary semantics.

SW0-007 does not own the final Organ Authority Matrix.

SW0-007 does not own the complete Cortex ingress lifecycle state machine.

SW0-009 owns the final Organ Authority Matrix.

SW0-010 owns the complete Cortex ingress lifecycle specification.

This contract must not silently absorb either later gate.

## 3. Cortex Ingress Boundary

Cortex ingress is the constitutional boundary through which material may enter Cortex-governed processing.

Arrival at Cortex does not by itself establish:

- identity;
- authority;
- permission;
- effective capability;
- valid Authorization;
- Evidence status;
- Canonical Membership;
- truth;
- valid issuance;
- authorization to execute.

Ingress is not admission to canonical state.

Ingress is not proof that the represented material is effective.

## 4. Transport Boundary

Transport success does not establish semantic validity.

Transport success does not establish valid issuance.

Transport success does not establish authority.

Transport success does not establish Canonical Membership.

A representation may reach Cortex while remaining unresolved, invalid, unauthorized, noncanonical, quarantined, or otherwise constitutionally ineffective.

Transport and constitutional effect remain separate concerns.

## 5. Identity Boundary

Identity and authority are distinct.

Resolving an identity does not resolve that identity's authority.

An identity associated with ingress material must not acquire authority merely because Cortex can identify, authenticate, address, store, retrieve, or route it.

Identity resolution must not silently become permission.

Identity resolution must not silently become capability effectiveness.

## 6. Authority Resolution Boundary

Required authority must resolve through the applicable authority path.

Cortex must not manufacture missing authority.

Cortex must not infer authority from:

- identity;
- role;
- capability;
- permission;
- administrative control;
- storage location;
- transport success;
- execution ability;
- possession of an artifact.

If authority required for a consequential operation cannot be deterministically resolved, that operation must fail closed.

## 7. Capability Boundary

Capability and authority are distinct.

Capability and permission are distinct.

Capability and Authorization are distinct.

Possession of a Capability Artifact does not establish that exercising the represented capability is permitted.

A capability that is revoked, expired, invalid, unresolved, or otherwise ineffective must not become effective merely because Cortex possesses or receives its representation.

## 8. Permission Boundary

Permission must not be inferred from capability possession.

Permission must not be inferred from successful execution.

Permission must not be inferred from Cortex visibility or administrative access.

Where permission is required, it must resolve through the applicable governing contract.

Unknown permission state must not silently become permission.

## 9. Observe Boundary

The current provisional Cortex authority surface permits observation.

Observation remains bounded by the applicable scope and governing contracts.

Observation does not itself create:

- Evidence;
- truth;
- authority;
- Authorization;
- Canonical Membership;
- permission to disclose;
- permission to execute.

Cortex observation must remain distinguishable from constitutional effect.

## 10. Propose Boundary

The current provisional Cortex authority surface permits bounded proposal behavior.

A Cortex proposal describes or submits possible action within its applicable scope.

A proposal does not authorize itself.

A proposal does not become canonical merely because Cortex produced it.

A proposal does not create the authority required to approve, canonicalize, or execute it.

## 11. Authorization Prohibition

Cortex has no inherent Authorize authority under the SW0-007 boundary.

Cortex must not issue constitutional Authorization merely because it:

- receives an Authorization-shaped representation;
- validates an Authorization-shaped representation;
- stores an Authorization Artifact;
- transports an Authorization Artifact;
- possesses execution capability;
- controls infrastructure;
- observes a requested operation.

Cortex may receive, preserve, resolve, or route an Authorization Artifact where permitted.

Such handling does not make Cortex the authorizing authority.

## 12. Canonicalization Prohibition

Cortex has no inherent Canonicalize authority under the SW0-007 boundary.

Cortex ingress does not create Canonical Membership.

Cortex storage does not create Canonical Membership.

Cortex validation does not create Canonical Membership.

Cortex transport does not create Canonical Membership.

Cortex execution does not create Canonical Membership.

Admission to canonical state remains governed by the applicable canonicalization authority path and lifecycle.

## 13. Project Request Boundary

The current provisional Cortex authority surface permits project-request behavior.

A Cortex request for projection is not itself Project authority.

A request for projection does not alter canonical state.

A request for projection does not authorize disclosure.

Any resulting Projection remains governed by its own applicable authority and visibility rules.

## 14. Execute Boundary

The current provisional Cortex authority surface permits only bounded execution.

Execute authority does not supply any independently required:

- Authorization;
- permission;
- capability effectiveness;
- Qualification;
- Canonicalization;
- authority in another dimension.

Successful execution does not retroactively authorize an operation.

Successful execution does not enlarge Cortex authority.

Execution ability is not execution authority.

## 15. Authorization Artifact Boundary

An Authorization Artifact represents an Authorization for a bounded consequential transition.

Authorization-shaped fields do not authorize anything merely by existing.

A structurally valid Authorization Artifact does not itself prove effective Authorization.

Cortex must preserve the distinction between:

- Authorization representation;
- valid issuance;
- effective authority;
- applicable scope;
- current authorization state;
- Receipt recording issuance or use.

## 16. Capability Artifact Boundary

A Capability Artifact represents a bounded means through which an operation may be exercised.

Capability representation does not imply Permission.

Capability representation does not imply Authorization.

Capability possession does not establish permitted exercise.

Cortex must not silently convert stored or transported capability representation into constitutional effectiveness.

## 17. Receipt Boundary

A Receipt Artifact records an occurrence claim under its applicable Receipt semantics.

Receipt existence does not establish the validity of the represented occurrence.

A Receipt does not automatically become:

- Authorization;
- Authority Grant;
- Capability;
- Evidence;
- Canonical Membership;
- semantic validity.

Cortex must not substitute a Receipt for the distinct artifact, authority, authorization, or occurrence it references.

## 18. Canonical Membership Boundary

Canonical Membership is governed state.

Physical presence inside Cortex is not Canonical Membership.

Storage presence is not Canonical Membership.

Serialization-canonical bytes are not Canonical Membership.

Cryptographic validity is not Canonical Membership.

Where an operation requires known Canonical Membership and that classification cannot be resolved, the operation must fail closed.

## 19. Cryptographic Transition Binding

Where an ACBP-1 cryptographic operation binds a Cortex transition under the existing cryptographic profile, the applicable purpose is:

cortex/transition

A valid cryptographic binding does not by itself establish:

- authority;
- Authorization;
- permission;
- Canonical Membership;
- Evidence status;
- truth;
- legality of the transition.

Cryptographic validity and constitutional validity remain distinct.

## 20. Administrative Boundary

Administrative control over Cortex does not establish semantic authority.

Infrastructure control does not establish constitutional authority.

Ability to configure, restart, inspect, route, store, or operate Cortex infrastructure does not silently confer:

- Authorize authority;
- Canonicalize authority;
- Qualify authority;
- Project authority;
- unrestricted Execute authority;
- authority over another constitutional organ.

## 21. Implementation Wall

SW0-007 defines constitutional boundary semantics only.

SW0-007 does not authorize:

- database implementation;
- model integration;
- Engine wiring;
- complete Cortex runtime implementation;
- complete Cortex ingress state-machine implementation.

Implementation must remain downstream of the applicable STONEWALL gates.

## 22. State-Machine Deferral

The Cortex ingress lifecycle is a declared core state machine.

Its complete:

- states;
- transitions;
- guards;
- required evidence;
- authority requirements;
- emitted receipts;
- failure behavior;
- recovery behavior

belong to SW0-010.

This contract constrains that future state machine but does not replace it.

No Cortex state machine may manufacture authority absent from the applicable authority root and constitutional contracts.

## 23. Organ Authority Matrix Deferral

The existing Organ Authority Matrix is provisional.

SW0-007 must not silently freeze the entire provisional matrix as the final Organ Authority Matrix.

For Cortex, this contract establishes constitutional boundaries that the later matrix must respect unless explicitly amended through constitutional governance.

The final cross-organ authority enumeration belongs to SW0-009.

## 24. Cortex Non-Collapse Laws

The following distinctions are mandatory:

- ingress != canonical admission;
- transport != semantic validity;
- identity != authority;
- identity != permission;
- capability != authority;
- capability != permission;
- capability != Authorization;
- administrative control != semantic authority;
- proposal != Authorization;
- observation != Evidence;
- Authorization representation != effective Authorization;
- Receipt != underlying occurrence;
- Receipt != Authorization;
- storage presence != Canonical Membership;
- execution ability != Execute authority;
- successful execution != Authorization;
- cryptographic validity != constitutional validity;
- Cortex possession != constitutional effectiveness.

## 25. SW0-007 Closure Conditions

SW0-007 may close only when machine-checkable evidence demonstrates that:

1. Cortex ingress is distinct from canonical admission.
2. transport success does not establish semantic validity.
3. identity remains distinct from authority.
4. identity remains distinct from permission.
5. capability remains distinct from authority.
6. capability remains distinct from permission.
7. capability remains distinct from Authorization.
8. unresolved required authority fails closed.
9. Cortex cannot manufacture missing authority.
10. observation does not create constitutional effect.
11. bounded proposal does not self-authorize.
12. Cortex possesses no inherent Authorize authority.
13. handling an Authorization Artifact does not make Cortex the authorizing authority.
14. Cortex possesses no inherent Canonicalize authority.
15. Cortex ingress, storage, validation, transport, or execution does not create Canonical Membership.
16. project-request behavior remains distinct from Project authority.
17. bounded execution does not supply missing Authorization, permission, capability effectiveness, Qualification, or Canonicalization.
18. successful execution does not retroactively authorize an operation.
19. Authorization representation remains distinct from effective Authorization.
20. Capability representation remains distinct from permitted exercise.
21. Receipt remains distinct from the occurrence or artifact it records.
22. unresolved required Canonical Membership fails closed.
23. cortex/transition cryptographic binding remains distinct from constitutional validity.
24. administrative control remains distinct from semantic authority.
25. SW0-007 does not implement Cortex.
26. SW0-007 does not freeze the final Organ Authority Matrix.
27. SW0-007 does not define the complete Cortex ingress state machine.
28. SW0-009 ownership of the Organ Authority Matrix remains preserved.
29. SW0-010 ownership of the Cortex ingress lifecycle remains preserved.
30. the Cortex non-collapse laws remain explicit and testable.

SW0-007 is declared FROZEN by this document and STONEWALL-SEQUENCE.md. The former candidate-ending sentence is superseded by this editorial reconciliation; no authority boundary or closure condition is changed. Historical closure evidence must be independently verified through the evidence index; this status declaration is not a new closure receipt.
