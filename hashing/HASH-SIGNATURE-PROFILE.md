# Hash and Signature Profile

Status: FROZEN - SW0-005

## 1. Purpose

This contract defines the initial cryptographic binding profile for the AnarchI Brain.

The initial profile is:

AnarchI Cryptographic Binding Profile 1

Profile identifier:

ACBP-1

ACBP-1 defines:

- cryptographic hash algorithm
- digital signature algorithm
- cryptographic domain separation
- deterministic preimage framing
- digest representation
- public-key representation
- signature representation
- deterministic public-key identifiers
- cryptographic verification semantics
- historical verification boundaries
- cryptographic non-collapse laws

This contract is subordinate to:

- AnarchI Semantic Language v1, frozen by SW0-001
- Authority Dimensions, frozen by SW0-002
- Artifact and Receipt Taxonomy, frozen by SW0-003
- ACS-1 Canonical Serialization, frozen by SW0-004 and corrected by SW0-004-ERRATUM-001

## 2. Constitutional Separation

Cryptography provides bounded mathematical properties.

Cryptography does not independently define constitutional authority.

Within ACBP-1:

- digest != truth
- digest != Evidence
- digest != Canonical Membership
- digest != valid issuance
- signature != Authorization
- signature validity != authority
- signature validity != identity ownership
- signature validity != permission
- signature validity != valid issuance
- public-key possession != identity
- private-key possession != permission
- key identifier != authority
- cryptographic verification != constitutional acceptance
- historical signature validity != current effective authority
- revocation != deletion of cryptographic history

A cryptographic result may be consumed by a governing contract.

The governing contract determines what constitutional consequence, if any, follows.

## 3. Profile Identity

The exact profile identifier is:

ACBP-1

A cryptographic operation governed by this profile must explicitly bind or deterministically resolve ACBP-1.

A missing cryptographic profile must not be inferred.

An unknown cryptographic profile must not be interpreted as ACBP-1.

A future incompatible cryptographic profile requires a new profile identifier.

Historical ACBP-1 operations remain interpreted under ACBP-1.

## 4. Hash Algorithm

ACBP-1 uses SHA-256 as its cryptographic hash algorithm.

The algorithm identifier is:

sha256

SHA-256 produces exactly 32 digest bytes.

ACBP-1 does not truncate SHA-256 digests.

ACBP-1 does not extend SHA-256 digests.

ACBP-1 does not silently substitute another hash algorithm.

A future replacement or additional algorithm requires an explicitly identified profile or governing extension compatible with the constitutional versioning rules.

## 5. Signature Algorithm

ACBP-1 uses pure Ed25519 as its digital signature algorithm.

The algorithm identifier is:

ed25519

The signing message is the exact ACBP-1 domain-separated signing frame.

ACBP-1 does not use:

- Ed25519ph
- Ed25519ctx
- an implementation-defined prehash
- an implementation-defined context
- an implementation-defined message transformation

An Ed25519 public key is exactly 32 raw bytes.

An Ed25519 signature is exactly 64 raw bytes.

ACBP-1 does not silently substitute another signature algorithm.

## 6. Cryptographic Operations

ACBP-1 defines three cryptographic framing operations:

- hash
- sign
- key-id

Each operation has an independent domain.

Material framed for one operation must not be interpreted as material framed for another operation.

Hash framing is not signing framing.

Signing framing is not key-identifier framing.

Key-identifier framing is not semantic hashing.

## 7. Cryptographic Purpose

Every hash or signature operation must bind an explicit purpose.

Purpose identifies the governed semantic use of the cryptographic operation.

Purpose must be defined by an applicable governing contract.

Purpose must not be invented from:

- artifact kind
- filename
- database table
- network route
- component name
- provider name
- model output
- caller implementation type

There is no default purpose.

An absent purpose is an error.

An unresolved purpose is an error.

## 8. Purpose Grammar

An ACBP-1 purpose is an ASCII string.

Its encoded length must be from 1 through 128 bytes inclusive.

Permitted characters are:

- lowercase letters a through z
- digits 0 through 9
- period
- underscore
- hyphen
- solidus

The first character must be a lowercase letter or digit.

Purpose comparison is byte-exact.

Purpose comparison is case-sensitive.

No Unicode normalization applies.

No case folding applies.

No whitespace trimming applies.

Examples of syntactically valid purposes include:

- artifact
- receipt
- authority-grant
- integrity-epoch
- anarchi.receipt.v1
- cortex/transition

Syntactic validity does not itself establish that a purpose is constitutionally defined or applicable.

## 9. Frame Primitive

Every ACBP-1 cryptographic frame has this byte structure:

MAGIC ||
0x00 ||
U16BE(operation_length) ||
operation ||
U16BE(purpose_length) ||
purpose ||
U64BE(payload_length) ||
payload

MAGIC is the exact ASCII byte sequence:

ANARCHI-ACBP-1

U16BE is an unsigned 16-bit integer encoded in big-endian byte order.

U64BE is an unsigned 64-bit integer encoded in big-endian byte order.

Lengths are measured in bytes.

No terminator is included in a length.

No implicit padding is permitted.

No platform-native integer representation is permitted.

## 10. Operation Encoding

The exact operation byte strings are:

hash

sign

key-id

Operation strings are ASCII.

Operation strings are encoded exactly as listed.

No operation alias is permitted.

No case variant is permitted.

No unknown operation may be interpreted as a known operation.

## 11. Payload Binding

For hash and sign operations over governed semantic material, payload is the exact ACS-1 canonical byte sequence.

The payload must already contain the serialization profile, schema identifier, and schema version required by ACS-1.

ACBP-1 must not:

- rewrite ACS-1 bytes
- normalize ACS-1 bytes
- reserialize ACS-1 bytes
- add whitespace
- remove whitespace
- alter Unicode
- alter field ordering
- change schema binding
- infer missing semantic content

ACS-1 determines canonical semantic bytes.

ACBP-1 binds those bytes cryptographically.

## 12. Semantic Digest

An ACBP-1 semantic digest is calculated as:

SHA-256(
    FRAME(
        operation = hash,
        purpose = governing purpose,
        payload = ACS-1 canonical bytes
    )
)

The resulting digest is 32 bytes.

Changing any of the following changes the framed hash input:

- ACBP profile
- operation
- purpose
- payload length
- payload bytes

Digest calculation does not perform Canonicalization.

Digest calculation does not validate constitutional authority.

Digest calculation does not establish artifact validity.

## 13. Digest Text Representation

The canonical textual representation of an ACBP-1 SHA-256 digest is:

sha256:<64 lowercase hexadecimal characters>

Example shape:

sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

Uppercase hexadecimal is not canonical ACBP-1 digest text.

Whitespace is forbidden.

A prefix other than:

sha256:

is not an ACBP-1 SHA-256 digest representation.

Textual digest parsing must recover exactly 32 digest bytes.

## 14. Digest Equality

Digest equality means that two computed digest byte sequences are equal.

Digest equality does not prove byte-for-byte equality of the hashed payloads because distinct inputs may theoretically collide.

Digest equality does not independently establish:

- truth
- Evidence status
- artifact identity
- provenance identity
- Canonical Membership
- authorization
- authority
- valid issuance
- semantic equivalence
- independent corroboration

Under the same ACBP-1 framing inputs and SHA-256 algorithm, differing digest values establish that the framed byte inputs were not identical.

## 15. Signature Message

An ACBP-1 signature is calculated over:

FRAME(
    operation = sign,
    purpose = governing purpose,
    payload = ACS-1 canonical bytes
)

The signature operation does not sign the ACBP-1 semantic digest unless a future governing profile explicitly defines such behavior.

Hash and signature framing are intentionally separate cryptographic domains.

A signature over one purpose must not verify as a signature over another purpose.

A signature over one payload must not verify as a signature over another payload.

## 16. Public-Key Text Representation

The canonical textual representation of an Ed25519 public key is:

ed25519-pub:<64 lowercase hexadecimal characters>

The hexadecimal content represents exactly 32 raw public-key bytes.

Uppercase hexadecimal is not canonical.

Whitespace is forbidden.

Public-key text is representation.

Public-key representation does not establish:

- identity
- authority
- permission
- valid issuance
- ownership
- custody
- current effectiveness

## 17. Signature Text Representation

The canonical textual representation of an Ed25519 signature is:

ed25519-sig:<128 lowercase hexadecimal characters>

The hexadecimal content represents exactly 64 raw signature bytes.

Uppercase hexadecimal is not canonical.

Whitespace is forbidden.

A signature-shaped byte sequence does not establish that verification succeeded.

## 18. Public-Key Identifier

ACBP-1 defines a deterministic identifier for an Ed25519 public key.

The key-identifier payload is the exact 32 raw public-key bytes.

The key-identifier frame uses:

operation:

key-id

purpose:

ed25519-public-key

The key identifier digest is:

SHA-256(
    FRAME(
        operation = key-id,
        purpose = ed25519-public-key,
        payload = raw Ed25519 public-key bytes
    )
)

## 19. Key-Identifier Text Representation

The canonical textual representation of an ACBP-1 Ed25519 key identifier is:

ed25519-kid:<64 lowercase hexadecimal characters>

The hexadecimal content represents the 32-byte key-identifier digest.

A key identifier identifies public-key material under ACBP-1.

A key identifier does not independently identify:

- a human
- an organization
- an agent
- a role
- an authority root
- an authority grant
- a device
- a current key custodian

Binding a key identifier to any such identity or role requires a separate governed relationship.

## 20. Key Identifier Versus Public Key

A key identifier is derived from a public key.

A key identifier is not the public key itself.

Possession of a key identifier does not enable signature verification unless the applicable public key is also available or deterministically resolvable.

A key identifier does not prove that the referenced public key is:

- trusted
- current
- authorized
- unrevoked
- correctly attributed
- constitutionally applicable

## 21. Private-Key Boundary

ACBP-1 does not define a canonical textual private-key representation.

ACBP-1 does not define private-key storage format.

ACBP-1 does not define private-key backup format.

ACBP-1 does not define private-key transport format.

Private-key generation, custody, storage, hardware binding, recovery, rotation, destruction, and access control belong to dedicated key-management contracts and substrates.

Private-key material must not be placed in:

- canonical artifacts
- Receipt Artifacts
- provenance records
- processing-lineage records
- logs
- diagnostics
- error messages
- telemetry
- public projections
- signature records

A conforming signing boundary exposes only the minimum information required by its governing contract.

## 22. Private-Key Possession

Possession or control of private-key material means only that the cryptographic signing operation may be technically exercisable.

Private-key possession does not independently establish:

- identity
- permission
- authority
- valid issuance
- Canonical Membership
- legitimacy
- current key status
- applicable signing purpose

Cryptographic capability is not constitutional authorization.

## 23. Cryptographic Verification

Cryptographic Verification is the bounded mathematical evaluation of a signature against:

- ACBP profile
- signature algorithm
- purpose
- exact payload
- public key
- signature bytes

ACBP-1 defines three verification outcomes:

VALID

INVALID

UNRESOLVED

## 24. VALID Verification

VALID means that pure Ed25519 verification succeeded for the supplied signature over the exact ACBP-1 signing frame using the supplied public key.

VALID establishes only successful cryptographic verification under ACBP-1.

VALID does not independently establish:

- who controlled the private key
- when the signature was created
- why the signature was created
- authority
- permission
- key applicability
- key trust
- current key status
- valid artifact issuance
- Canonical Membership
- truth
- Evidence status
- legal transition

## 25. INVALID Verification

INVALID means that cryptographic verification was attempted with deterministically resolved required inputs and the signature did not verify.

INVALID must not be silently converted to VALID.

INVALID does not necessarily prove malicious behavior.

INVALID may result from:

- wrong payload
- wrong purpose
- wrong public key
- altered signature
- altered bytes
- malformed cryptographic material
- other verification failure

The applicable contract determines further consequences.

## 26. UNRESOLVED Verification

UNRESOLVED means that cryptographic verification cannot currently be deterministically completed.

Reasons may include:

- missing public key
- unresolved key identifier
- missing payload
- missing purpose
- unknown profile
- unsupported algorithm
- unavailable required historical material
- ambiguous required input

UNRESOLVED must not silently become VALID.

UNRESOLVED must not silently become INVALID.

Where VALID verification is required for a consequential transition, UNRESOLVED must fail closed.

## 27. Verification Versus Acceptance

Cryptographic Verification and constitutional acceptance are distinct.

A VALID signature may still be constitutionally unacceptable because:

- the key was not applicable
- the key lacked required authority
- the signing purpose was unauthorized
- valid issuance requirements were not satisfied
- required independence was absent
- applicable evidence was missing
- the key was revoked under the relevant policy
- the signature was outside applicable temporal bounds
- another governing condition failed

An INVALID signature cannot be elevated to VALID by policy.

An UNRESOLVED signature cannot be treated as VALID merely because acceptance would be convenient.

## 28. Identity Binding

ACBP-1 does not infer identity from cryptographic material.

A public key may be associated with an identity only through an explicit governed relationship.

A valid signature proves mathematical correspondence to a public key under the verification inputs.

It does not prove that a named human, organization, agent, role, or system actually controlled that key at signing time.

Identity attribution requires applicable governance and provenance.

## 29. Authority Binding

Authority is governed by SW0-002.

A public key does not possess constitutional authority merely because it exists.

A private key does not possess constitutional authority merely because it can sign.

A valid signature does not manufacture authority.

A valid signature cannot enlarge an Authority Grant.

A valid signature cannot repair an invalid Authorization.

A valid signature cannot satisfy proposer-authorizer independence when the governing authority path does not.

A signature may be consumed as cryptographic evidence within an authority-resolution process only where a governing contract explicitly requires it.

## 30. Attestation Boundary

A cryptographic signature is not automatically an Attestation.

An Attestation Artifact may use a cryptographic signature where its governing schema and contract require one.

Cryptographic signature validity does not establish attestation truth.

Cryptographic signature validity does not establish attest authority.

Attest authority must resolve independently under SW0-002.

## 31. Evidence Boundary

A digest is not automatically Evidence.

A signature is not automatically Evidence.

A public key is not automatically Evidence.

A verification result is not automatically Evidence.

Any such material becomes Evidence only through an applicable evidence process.

Cryptographic consistency does not create independent corroboration.

Multiple signatures produced by the same effective source do not automatically become independent corroboration.

## 32. Canonical Membership Boundary

Hashing material does not Canonicalize it.

Signing material does not Canonicalize it.

Verifying a signature does not Canonicalize it.

Assigning a key identifier does not Canonicalize it.

Storing a digest does not create Canonical Membership.

Storing a signature does not create Canonical Membership.

Canonical Membership requires the applicable canonical authority path and state-machine transition.

## 33. Historical Verification

Cryptographic history and current governance state are distinct.

A signature that was mathematically valid remains historically verifiable when its required historical inputs remain available.

Later revocation does not retroactively alter the mathematical result of an earlier signature verification.

Later expiry does not alter the mathematical signature bytes.

Later authority changes do not alter the historical cryptographic bytes.

Historical verification does not establish current authorization.

Historical verification does not establish current effective authority.

## 34. Revocation Boundary

Key revocation is a governed state transition outside the mathematical Ed25519 verification function.

Revocation may alter whether a key or signature is constitutionally accepted for an operation.

Revocation does not:

- change the public-key bytes
- change historical signature bytes
- change historical payload bytes
- erase required receipts
- erase required provenance
- cause a mathematically invalid signature to become valid
- cause a mathematically valid historical signature to have never verified

The complete key-revocation lifecycle belongs to later governance and state-machine contracts.

## 35. Temporal Semantics

ACBP-1 signatures contain no inherent trusted creation time.

Filesystem timestamps are not trusted signature time.

Database timestamps are not trusted signature time.

Network receipt time is not trusted signature creation time.

Model-generated time is not trusted signature time.

A governing schema may include explicit temporal material inside the signed ACS-1 payload.

Trust in that temporal assertion remains a separate governed question.

## 36. Replay Boundary

A valid signature may be replayed as bytes.

Replay resistance is not automatically provided by Ed25519.

Where replay protection is required, the governing payload and state machine must bind the required replay-control material.

Examples may include:

- unique operation identity
- nonce
- sequence
- epoch
- subject version
- transition identity

ACBP-1 does not silently invent replay semantics.

## 37. Algorithm Confusion

Algorithm identifiers are mandatory where a governing representation requires cryptographic interpretation.

A verifier must not:

- guess the hash algorithm
- guess the signature algorithm
- infer an algorithm from byte length alone
- substitute a preferred algorithm
- downgrade to another algorithm
- treat unknown algorithms as known

Algorithm confusion must fail closed.

## 38. Domain Confusion

A verifier must bind the exact operation and purpose.

The same payload under:

hash

and:

sign

belongs to different cryptographic domains.

The same payload under two different purposes belongs to different cryptographic domains.

A valid signature under one purpose must not satisfy verification under another purpose.

A digest under one purpose must not be silently reused as the digest for another purpose.

## 39. Length Framing

All variable-length frame components are length-bound.

Length framing prevents ambiguity caused by simple byte concatenation.

A parser must reject:

- truncated lengths
- truncated payloads
- extra bytes outside the declared frame
- impossible lengths
- lengths that exceed implementation safety limits
- malformed operation lengths
- malformed purpose lengths

Implementation safety limits may be stricter than the U64BE payload capacity but must not alter interpretation of accepted frames.

## 40. Hexadecimal Representation

All ACBP-1 canonical hexadecimal text uses lowercase ASCII characters:

0 through 9

and:

a through f

Uppercase hexadecimal is noncanonical.

Whitespace is noncanonical.

Separators inside hexadecimal payloads are forbidden.

A parser must reject an incorrect encoded byte length.

## 41. Cryptographic Record Requirements

A governed record that claims an ACBP-1 cryptographic result must bind or deterministically resolve all information required to interpret that result.

Depending on the result, this includes:

- cryptographic profile
- algorithm identifier
- purpose
- digest
- public key or resolvable key identifier
- signature
- payload or deterministic payload reference

No field may silently derive constitutional authority from its cryptographic presence.

Concrete record schemas belong to later schema contracts.

## 42. Detached Signatures

ACBP-1 permits detached signature representation.

A detached signature does not contain the signed payload by definition.

Verification therefore requires deterministic recovery of the exact signed ACS-1 canonical bytes.

A payload reference is not the payload.

A payload digest is not the payload.

Digest equality alone is not byte-identity proof.

Where the exact payload cannot be deterministically recovered, verification is UNRESOLVED.

## 43. Key Rotation

Key rotation does not alter historical key identifiers.

A new public key receives a new deterministic key identifier.

A rotated key must not silently inherit:

- identity binding
- authority
- permission
- applicability
- revocation state
- temporal status

Any continuity relationship between old and new keys requires a separately governed transition.

## 44. Cryptographic Agility

ACBP-1 is immutable once frozen.

If cryptographic policy later requires different:

- hash algorithms
- signature algorithms
- framing
- key identifiers
- textual representation
- verification semantics

the change requires an explicitly identified successor profile or compatible governed extension.

A successor profile must not silently reinterpret ACBP-1 historical material.

Algorithm deprecation may prevent new cryptographic operations while preserving historical verification under applicable policy.

## 45. Provider Independence

ACBP-1 output and verification semantics must not vary because of:

- operating system
- CPU architecture
- cryptographic provider
- programming language
- locale
- timezone
- database
- filesystem
- model provider
- cloud provider
- key-storage provider

A provider may implement the primitive.

The provider does not define the constitutional meaning of the primitive.

## 46. Failure Behavior

ACBP-1 fails closed.

Cryptographic operation must not proceed when required interpretation is unresolved.

Failure conditions include:

- missing ACBP profile
- unknown profile
- missing operation
- unknown operation
- missing purpose
- invalid purpose
- missing payload
- malformed frame
- unsupported algorithm
- malformed digest
- malformed public key
- malformed signature
- malformed key identifier
- unresolved public key
- unavailable required payload
- ambiguous cryptographic interpretation

Failure must not authorize fallback to an unspecified algorithm or weaker profile.

## 47. Constitutional Cryptographic Laws

The following laws are mandatory:

- cryptographic profile must be explicit
- hash algorithm must be explicit
- signature algorithm must be explicit
- cryptographic purpose must be explicit
- cryptographic operation must be domain-separated
- purpose must be domain-separated
- digest != truth
- digest != Evidence
- digest != Canonical Membership
- digest != valid issuance
- digest equality != byte-identity proof
- signature != Authorization
- signature validity != authority
- signature validity != permission
- signature validity != identity
- signature validity != valid issuance
- signature validity != Canonical Membership
- public key != identity
- public key != authority
- private-key possession != permission
- private-key possession != authority
- key identifier != authority
- verification VALID != constitutional acceptance
- verification UNRESOLVED != VALID
- historical signature validity != current effective authority
- revocation != erasure of cryptographic history
- cryptographic consistency != independent corroboration
- hashing != Canonicalization
- signing != Canonicalization
- verification != Canonicalization
- cryptographic provider != constitutional authority
- cognition does not gain authority by producing or verifying cryptographic material

## 48. Relationship to Later Contracts

SW0-005 defines cryptographic binding semantics.

It does not define:

- key-generation procedures
- private-key storage
- hardware security modules
- key escrow
- key recovery
- key lifecycle state machines
- identity enrollment
- authority-grant lifecycle
- schema registry
- certificate authority
- public-key infrastructure topology
- network transport security
- TLS policy
- canonical-memory implementation
- database implementation

Later contracts must define those concerns without silently redefining ACBP-1.

## 49. Relationship to State Machines

Later state machines may consume:

- digests
- key identifiers
- public keys
- signatures
- verification results

A state machine requiring cryptographic verification must explicitly define:

- required ACBP profile
- required purpose
- acceptable verification outcome
- key applicability rules
- temporal rules
- revocation rules
- replay rules where required
- authority requirements
- emitted receipts

Cryptographic verification alone must not manufacture a legal state transition.

## 50. SW0-005 Closure Conditions

SW0-005 may close only when machine-checkable evidence demonstrates that:

1. ACBP-1 has one explicit profile identifier.
2. SHA-256 is uniquely bound as the ACBP-1 hash algorithm.
3. pure Ed25519 is uniquely bound as the ACBP-1 signature algorithm.
4. hash, sign, and key-id operations occupy distinct cryptographic domains.
5. cryptographic purpose is explicit and has no default.
6. frame construction is deterministic and unambiguous.
7. all variable-length frame components are length-bound.
8. semantic digests bind exact ACS-1 canonical bytes.
9. digest text representation is deterministic.
10. digest equality is not treated as proof of byte equality.
11. signatures bind exact ACS-1 canonical bytes under the sign domain.
12. public-key representation is deterministic.
13. signature representation is deterministic.
14. public-key identifiers are deterministic and domain-separated.
15. private-key representation is excluded from constitutional artifacts.
16. private-key possession is separated from permission and authority.
17. cryptographic verification has explicit VALID, INVALID, and UNRESOLVED outcomes.
18. VALID verification is separated from constitutional acceptance.
19. public-key material is separated from identity and authority.
20. signature validity is separated from authority, valid issuance, truth, Evidence, and Canonical Membership.
21. historical verification is separated from current effective authority.
22. revocation does not erase historical cryptographic material.
23. replay semantics are not silently inferred.
24. algorithm confusion fails closed.
25. domain confusion fails closed.
26. provider implementation does not define constitutional meaning.
27. profile evolution does not silently reinterpret historical ACBP-1 material.
28. this contract remains subordinate to SW0-001 through SW0-004.

These closure conditions have been proven for SW0-005. The ACBP-1 cryptographic binding profile is frozen.