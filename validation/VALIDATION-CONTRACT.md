# Supplemental Validation Contract

Status: CANDIDATE - SUPPLEMENTAL
Role: Supporting semantic contract for SW0-010 state-machine specifications.


## 1. Purpose

Validation determines whether an interpreted artifact satisfies declared validation conditions.

Validation is an evaluation boundary.

Validation does not create authority, authorization, evidence status, or Canonical Membership.

## 2. Relationship To Resolution

Resolution determines interpretation context.

Validation operates only after interpretation context is available.

Resolution and validation are separate boundaries.

A validation result does not replace resolution.

## 3. Validation States

Validation has three possible outcomes:

- VALID
- INVALID
- UNRESOLVED

VALID means all declared validation conditions were satisfied.

INVALID means the required interpretation/input context was available, every required condition was evaluated, and one or more conditions failed.

UNRESOLVED means required interpretation or validation context was unavailable.

A report preserves satisfied, failed, unresolved and missing conditions separately. If a known failure coexists with unavailable required context, the primary result remains UNRESOLVED while the known failure remains in the report. A result label does not erase findings. No result may be interpreted without its owning validation-contract identity and version. Structural results from the schema boundary remain distinct from this lifecycle's result vocabulary.

## 4. Closed State Semantics

UNRESOLVED must not silently become VALID.

UNRESOLVED must not silently become INVALID.

A transition from UNRESOLVED requires additional valid context.

## 5. Authority Separation

A validation result does not:

- grant authority
- create authorization
- create permission
- establish identity
- establish Evidence status
- establish Canonical Membership
- issue an artifact

## 6. Evidence Separation

Validation evaluates supplied inputs and conditions.

Validation does not manufacture evidence merely by producing a result.

## 7. Canonical Separation

Validation does not perform Canonicalization.

A valid validation result does not imply Canonical Membership.

## 8. Failure Semantics

Validation failures must identify the failed condition.

Failures are records of evaluation outcome.

Failures do not erase historical artifacts.

## 9. Determinism Boundary

Validation output must be derived only from declared inputs and declared validation rules.

Ambient mutable environment state must not determine validation outcome.

## 10. Cognition Boundary

A cognition system producing a validation result does not gain authority from producing that result.

The validator remains subordinate to governing contracts.

---

Supplemental candidate artifact for SW0-010 state-machine specification work.
