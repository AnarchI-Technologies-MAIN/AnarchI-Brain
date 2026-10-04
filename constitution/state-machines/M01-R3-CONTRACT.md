# M01 Repair R3: six independent-review repairs

Status: CANDIDATE, UNFROZEN. Reference qualification only. No numbered gate advances.

## Basis, preservation, and adoption boundary

This candidate repairs R2-REV-01 through R2-REV-06 from the independent review of
M01-R2-review-20261001T221519Z-0f92b879.zip, SHA-256
20b82017d4fe0bd1da6a957d6dc390e04a9afc4573f664a31267688daa870a42.
R2 remains byte-exact except for the separately identified proposed .gitattributes
replacement. Its original attributes bytes are preserved under m01-r3 evidence.
Its contracts, source, manifests and historical receipts are not rewritten.

The R3 verified-source launcher and R3 namespaces are the candidate APIs for this
qualification only. R2's launcher and its old manifest are historical evidence,
not a qualification entrypoint for the R3 overlay. Adoption into the working
repository still requires a bounded preflight and separate authorization. No
frozen-status amendment is approved merely by inclusion in this candidate.

The R2 contract's lossless attempt findings, shared C03/C04 entry assessment,
actual required-condition satisfaction, independent admission, explicit selected
diagnostic route, and separation of operation from recording remain intact.
The selected diagnostic route may favor unresolved witnesses while retaining
known blocks; semantic findings are not reduced to a dominant truth value.

## Verified execution identity

The supported qualification entrypoint is qualify_m01_r3.py with an externally
pinned manifest digest. It reads each bound file once, checks its SHA-256, and
compiles repository-owned active modules from those exact in-memory buffers.
A restricted import graph prevents fallback to unverified repository modules.
The historical R1 loader separately compiles the same byte buffer it verified.
No .pyc cache loader is used for these repository-owned modules. Disabling
bytecode writing alone is not treated as a code-identity proof.

The launcher itself must be bound by the invoking handoff, which compiles its
verified bytes directly. Child qualification processes do the same, including
optimized Python execution. Ordinary arbitrary import of an R3 .py file is not
the verified qualification interface. Python, its standard library, installed
jsonschema dependencies, Git, OS and approved Python callbacks remain trusted
external dependencies. This mechanism is not a hostile-code sandbox and does
not authenticate governance or prove code correct merely by hashing it.

## Recording target binding

A recording Assessment contains an immutable RecordingTarget: kind,
attempt_digest, and predecessor_digest. Diagnostic kind is DIAGNOSTIC and both
digests identify the exact carried AttemptReview. Closure kind is CLOSURE;
attempt_digest identifies the exact carried attempt and predecessor_digest
identifies the exact admitted diagnostic or occurrence predecessor.

The recording function recomputes this target before admission. An absent or
different target is rejected. The full Assessment, including its target, is
bound into the admitted recording payload. Relabeling the target changes that
payload and does not reuse earlier admission. The record's own Context and
evaluation remain distinct from the operation, entry, diagnostic and occurrence
evaluations where required. Entry assessments have no recording target.

Same-input evaluation remains deterministic reference replay. These pure functions
do not provide a global durable evaluation-ID uniqueness registry or effect
idempotency. A new target needs fresh independently admitted assessment; its
identifier is not proof of principal independence. No reference report creates
recording authority, durable receipt issuance, or permission for protected effects.

## Single-subject representation review

Registry.review captures a bounded independent copy of exact supported JSON value
types before invoking any external verifier. No custom object copy hooks run.
The completed captured value is encoded once as an ACS-1 document and assigned a
SHA-256 reference identity. This does not claim an atomic snapshot of arbitrary
concurrent writes during capture; the completed capture is the reviewed subject.
Unsupported, cyclic, oversized, or unrepresentable inputs are rejected.

All structural, content, and semantic evaluations describe that one capture.
Both R3 verifier methods receive the same immutable ReviewSubject containing the
document digest, schema identity/version/digest, registry digest, and reference
identity-profile label. The returned BoundaryReview carries that subject. It
never invites association with the caller's later mutable dictionary. No raw
payload is retained in the review or rejection reason. Subject hashes are binding
references, not secrecy guarantees, semantic proof, or ACBP cryptographic evidence.

R3 content_verifier.verify_secret_free(subject) and
semantic_verifier.verify_interpretation(subject) replace the narrower R2 signatures
for this candidate. Default admission remains UNRESOLVED. A caller-object change
between callbacks cannot combine approvals for two subject digests into one review.

## Independent result axes

Structural/representation rejection reports STRUCTURALLY_INVALID and leaves
content/semantic stages NOT_CHECKED. Unknown interpretation reports
INTERPRETATION_UNRESOLVED. Recognized forbidden content in an otherwise valid
representation reports STRUCTURALLY_VALID, content_admission=BLOCKED,
content_screening=RECOGNIZED_SHAPE_REJECTED, semantic_resolution=NOT_CHECKED,
and a fixed non-sensitive reason. No real secret is needed to test that boundary.

No recognized shape reports NO_RECOGNIZED_SHAPE, not a proof of secrecy.
Independent content admission remains UNRESOLVED without a verifier. A blocked
content admission does not invoke semantic verification. effective_authority
remains False in every result; passing these axes does not grant use or execution.

## Full manifest checkout bytes

Every bound file, the manifest, and .gitattributes receive exact per-path
-text checkout policy, with filter/ident conversion disabled and other text
conversion attributes reset. Existing source bytes are not normalized. The two
older mixed-newline working-tree representations remain distinct from their raw
Git baseline identities. Frozen corpus hashes and historical receipts are not
regenerated to fit a converted checkout.

Qualification stages only disposable full-candidate copies into disposable Git
indexes, then checks every bound file after checkout with core.autocrlf=false
and core.autocrlf=true. Both the complete manifest and the retained 840-assertion
schema corpus must pass. These experiments do not commit or stage the user repo.
Arbitrary system attributes overrides and hostile concurrent mutation are not
claimed to be eliminated by the candidate's local .gitattributes policy.

## Complete historical coverage

Original absolute paths remain provenance. The current repository root never
selects which originals to check. A pinned relative mapping is reconstructed
against the preserved R2 inventory: exactly 56 original repository paths, of which
49 remain unchanged and seven carry the existing R2 candidate amendments. All
nine separately preserved copies remain byte-identical. Missing, duplicated,
unmapped, outside-root, link/reparse, or altered entries reject qualification.
A relocated root checks the same original identity set rather than zero entries.

## Evidence and limits

Fresh normal/optimized tests must exercise the six independent-review regressions,
including conflicting caches, changed code/manifest, changed recording targets,
re-entrant payload mutation, correct content/structural labeling, full checkout,
and complete relocated historical coverage. New receipts bind new candidate
identities; original results remain historical. An expected test count is never
substituted for executed tests.

M01_FREEZE_READY=False. Admission authentication, contract-specific semantics,
durable recording, atomic execution/freshness/replay enforcement, complete
lifecycle qualification, and historical closure evidence remain separate open
obligations. R3 does not install the prior historical-recovery package, implement
runtime infrastructure, perform protected operations, or approve any freeze.
