# AnarchI Brain
# Supplemental Resolution Contract

Status: CANDIDATE - SUPPLEMENTAL
Role: Supporting semantic contract for SW0-010 state-machine specifications.


## 1. Purpose

This contract defines deterministic resolution of governed interpretation context.

Resolution identifies the applicable schema interpretation boundary.
Resolution does not create authority, authorization, evidence, canonical membership, or truth.

## 2. Resolution Result States

A resolver MUST return exactly one resolution state:

- VALID
- INVALID
- UNRESOLVED

## 3. VALID Resolution

VALID requires:

- schema identity is known
- schema version is known
- governing schema contract is available
- instance evaluation can proceed against the resolved contract

VALID does not imply:

- valid issuance
- authority
- authorization
- canonical membership
- evidence admission

## 4. INVALID Resolution

INVALID means:

- governing interpretation was successfully resolved
- evaluated content violates the governing contract

INVALID does not imply:

- malicious intent
- nonexistence
- revocation
- loss of historical meaning

## 5. UNRESOLVED Resolution

UNRESOLVED is required when:

- schema identity is unknown
- schema version is unknown
- governing interpretation cannot be deterministically selected
- required interpretation context is unavailable

UNRESOLVED MUST NOT silently become VALID or INVALID.

## 6. Resolver Boundaries

Resolution is not:

- Authorization
- Canonicalization
- Evidence determination
- Authority determination
- Truth determination

A resolver MUST NOT manufacture missing authority.

## 7. Historical Interpretation

Historical schema meaning is immutable.

A newer schema version does not reinterpret prior schema meaning.

## 8. Registry Binding

Resolution MUST use explicit registry identity.

Unknown registry entries fail closed.

## 9. Cognition Boundary

Cognition producing a resolution result does not gain authority over the resolved artifact.

## 10. Closure Requirements

The resolver MUST preserve:

- explicit schema identity
- explicit version identity
- fail-closed unknown handling
- deterministic interpretation
- separation from authority systems
