# Organ Authority Matrix

Status: FROZEN - SW0-009

## 1. Purpose and Status

SW0-009 owns the final cross-organ authority enumeration.

This candidate separates constitutional authority from lifecycle behavior, technical capability, operational prerequisites, state possession, requests, validation, qualification behavior, and implementation mechanics.

Except where a frozen anchor is identified below, non-unresolved cells are SW0-009 candidate assignments derived from the existing provisional matrix. They are not represented as pre-existing frozen constitutional facts.

## 2. Authority Dimensions

The matrix uses exactly twelve authority dimensions: Observe, Propose, Qualify, Authorize, Canonicalize, Project, Execute, Revoke, Migrate, Reconstruct, Attest, and Administer.

## 3. Cell Vocabulary

- `yes`: candidate assignment of the named authority dimension, subject to governing contracts.
- `bounded`: candidate assignment only inside explicitly stated constitutional bounds.
- `no`: candidate assignment that the organ possesses no inherent authority in that dimension.
- `unresolved`: SW0-009 does not establish the assignment in this candidate; required use must fail closed.

Missing authority must not be interpreted as `no`, `yes`, permission, capability, or unrestricted authority.

## 4. Candidate Authority Matrix

| Organ | Observe | Propose | Qualify | Authorize | Canonicalize | Project | Execute | Revoke | Migrate | Reconstruct | Attest | Administer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cortex | yes | bounded | unresolved | no | no | unresolved | bounded | unresolved | unresolved | unresolved | unresolved | unresolved |
| S0 | yes | no | unresolved | unresolved | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| Cartologist | yes | yes | unresolved | no | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| S1 | yes | unresolved | unresolved | unresolved | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| Wavesmith | yes | yes | unresolved | no | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| S2 | yes | no | unresolved | unresolved | yes | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| Canonical Memory | unresolved | no | unresolved | no | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| Librarian | yes | bounded | unresolved | no | no | no | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| S3 | yes | no | unresolved | unresolved | no | bounded | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| Prism | bounded | unresolved | unresolved | no | no | yes | no | unresolved | unresolved | unresolved | unresolved | unresolved |
| S4 | yes | no | unresolved | unresolved | no | no | bounded | unresolved | unresolved | unresolved | unresolved | unresolved |

## 5. Evidence Classification

- `FROZEN_EXPLICIT`: an earlier frozen contract explicitly establishes the authority boundary.
- `PROVISIONAL_CARRY`: the candidate preserves an intelligible primitive value from the prior OPEN matrix.
- `NORMALIZED_PROVISIONAL`: overloaded provisional wording is converted only where the authority meaning is unambiguous.
- `UNRESOLVED_OVERLOAD`: overloaded wording is not converted into authority.
- `UNRESOLVED_MISSING_DIMENSION`: the prior matrix supplied no assignment for that dimension.

A lifecycle name does not itself grant authority. A provisional cell does not become frozen merely by appearing in this candidate.

## 6. Legacy Normalization Register

- `derived proposals` -> Propose `bounded` for Librarian as NORMALIZED_PROVISIONAL.
- `bounded egress` -> Execute `bounded` for S4 as NORMALIZED_PROVISIONAL.
- S3 Project = `bounded` is a PROVISIONAL_CARRY from the prior OPEN matrix; its bound is limited to S3 transition-lifecycle participation and does not imply broader Project, Propose, Authorize, Canonicalize, or Execute authority.
- Prism Observe = `bounded` is a PROVISIONAL_CARRY from the prior OPEN matrix; its bound is limited to Prism projection-lifecycle observation and does not imply broader Observe, Propose, Authorize, Canonicalize, or Execute authority.
- Cortex `request` -> Project `unresolved`; requesting projection is not Project authority.
- S0 `validate` -> Authorize `unresolved`; validation behavior is not Authorize authority.
- S1 `qualify` -> Propose `unresolved`; qualification behavior is not Propose authority.
- S1 `bounded qualification` -> Authorize `unresolved`; qualification scope is not Authorize authority.
- S2 `policy/authority gated` -> Authorize `unresolved`; a prerequisite is not an authority assignment.
- Canonical Memory `state` -> Observe `unresolved`; state possession is not Observe authority.
- S3 `validate` -> Authorize `unresolved`; validation behavior is not Authorize authority.
- Prism `projection only` -> Propose `unresolved`; projection role is not Propose authority.
- S4 `capability gated` -> Authorize `unresolved`; capability gating is not Authorize authority.

## 7. Frozen Cortex Anchor

The frozen Cortex contract provides the strongest pre-existing organ-specific authority anchor.

- Cortex Observe = `yes`.
- Cortex Propose = `bounded`.
- Cortex Authorize = `no`.
- Cortex Canonicalize = `no`.
- Cortex Execute = `bounded`.
- Cortex Project remains `unresolved` because project-request behavior is explicitly distinct from Project authority.

## 8. Missing-Dimension Policy

Qualify, Revoke, Migrate, Reconstruct, Attest, and Administer were absent from the prior matrix.

This candidate therefore preserves all sixty-six corresponding organ/dimension cells as `unresolved` rather than silently manufacturing authority or prohibition.

An unresolved cell is a fail-closed constitutional state, not permission and not a conclusion that the authority can never be assigned.

## 9. Non-Collapse Rules

- lifecycle responsibility != authority;
- validation behavior != Authorize authority;
- qualification behavior != Authorize authority;
- projection request != Project authority;
- execution capability != Execute authority;
- capability prerequisite != Authorize authority;
- state possession != Observe authority;
- infrastructure administration != constitutional Administer authority;
- unresolved != permission;
- missing != unrestricted;
- candidate assignment != frozen authority;
- authority in one dimension != authority in another dimension.

## 10. Gate Ownership and Implementation Wall

SW0-009 owns the final Organ Authority Matrix semantics.

SW0-010 retains ownership of complete state-machine specifications and lifecycles.

This contract does not implement an authority resolver, authority-grant lifecycle, capability lifecycle, database authority tables, runtime enforcement, migration engine, reconstruction engine, Prism implementation, or state-machine implementation.

Freezing this candidate requires a separate adversarial review and a separate closure audit over the exact candidate bytes; neither this requirement nor the closure list may self-certify satisfaction.

## 11. Candidate Closure Conditions

1. exactly eleven organs are enumerated;
2. exactly twelve frozen authority dimensions are represented;
3. exactly 132 authority cells exist;
4. every cell is `yes`, `bounded`, `no`, or `unresolved`;
5. overloaded legacy behavior is absent from authority cells;
6. bounded cells require explicit scope or normalization evidence;
7. unresolved cells do not grant permission or authority;
8. missing dimensions do not silently default to `no`;
9. lifecycle names do not independently grant authority;
10. validation behavior remains distinct from Authorize authority;
11. qualification behavior remains distinct from Authorize authority;
12. projection requests remain distinct from Project authority;
13. capability gating remains distinct from Authorize authority;
14. state possession remains distinct from Observe authority;
15. Cortex frozen authority anchors remain preserved;
16. SW0-009 does not absorb SW0-010 lifecycle ownership;
17. no runtime or database authority implementation is introduced;
18. freezing this candidate requires a separate adversarial and closure proof.
