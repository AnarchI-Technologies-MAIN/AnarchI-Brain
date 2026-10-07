# Unit C disposable durable-claim reference contract

PROPOSED / NOT ADOPTED / ISOLATED SQLITE FIXTURES / ZERO LIVE EFFECTS.

This contract proposes a local standard-library SQLite journal reference and separately observable zero-effect fixture target. It enrolls no root, verifies no actual principal, exercises no grant, deploys nothing and changes no canonical memory. Unit B documentary acceptance does not materialize actual authority inputs. SQLite persistence in a disposable test directory can provide measured local process-crash/reopen evidence, not host-loss recovery, production durability or authenticated authority.

## Exact identity and isolation

Each operation binds operation_id, consumer/actor/target, subject identity/version/digest, request/context digest, generation/epoch, policy/schema/contract/root pins, exact grant and Authorization identities/versions/digests, and separate GrantEvaluation/AuthorizationEvaluation/ConsumptionEvaluation digests. Capture and verify those independently supplied fixture references before execution. No submitted success flag substitutes for evaluation or target evidence. Use the exact selected Unit B semantics; fixture ALLOW remains non-operative.

The SQLite file and separate target-evidence file/directory live only in a fresh task-owned temporary workspace. Never open a supplied adjacent database, server or production path. The fixture target records simulated effect identities only; it performs no external operation. Its evidence identity is bound separately from the authority journal. Any caller trying to expand those paths or substitute evidence is refused.

Replay identity includes all bound coordinates, not operation_id alone. Same ID with changed bytes, subject, request, consumer/actor/target, generation or authority context conflicts. Exact replay can inspect the recorded state; it cannot automatically re-run an uncertain effect or grant disclosure. No generation rollover or old-authority grandfathering occurs.

## Exact serialization and digest domains

UNIT-C-CANONICAL-JSON-1 is UTF-8 JSON produced with sorted string keys, compact separators (comma and colon without spaces), ensure_ascii=False and allow_nan=False. Reject duplicate keys during decoding, floats/nonfinite numbers, non-string keys, lone surrogate code points and unsupported values before canonicalization. Integers are exact signed values within the selected schema ranges; boolean values cannot satisfy integer coordinates. Enforce raw 1 MiB input, depth 64 and 100000-node bounds before invoking canonical serialization; malformed/overflow/recursion errors hold rather than fall back to another codec.

Binding digest is SHA-256 over UTF-8 bytes of the literal prefix UNIT-C:BINDING:v1 followed by a single NUL byte and the canonical binding bytes. Event digest uses prefix UNIT-C:EVENT:v1 plus NUL and canonical record bytes with only event_digest excluded. Target evidence digest uses prefix UNIT-C:TARGET:v1 plus NUL and canonical evidence bytes with only evidence_digest excluded. Recheck evidence digest uses prefix UNIT-C:RECHECK:v1 plus NUL and canonical recheck bytes. No object-class digest is substituted for another. Raw fixture bundle hashes retain Unit B's own exact byte hashing profile, not these Unit C domain prefixes.

## Initial evaluation and fresh recheck separation

The initial binding/context and its three evaluation digests are immutable. A post-claim observation may legitimately have different time/revocation bytes and context digest; preserve it as separate recheck evidence rather than overwrite or relabel the initial binding. The closed recheck object binds initial_binding_digest, raw_fresh_bundle_digest, fresh_context_digest, fresh GrantEvaluation/AuthorizationEvaluation/ConsumptionEvaluation digests, observed time window and all required immutable subject/policy/root/generation coordinates. A journal event's recheck_evidence_digest identifies that separate object; earlier events use explicit NONE.

Integrate the exact pinned adopted Unit B reference API: validate independently captured raw initial bundle against its external SHA-256, evaluate the validated fixture, and prepare_consumption against the recomputed exact decision. Extract the immutable operation binding from actual returned/captured identities; do not accept a caller's ALLOW assertion. For fresh recheck, independently pin the new raw bundle, validate and evaluate through the same pinned Unit B code/schema/contract dependency set, and recompute preparation/compatibility with the immutable operation. Compare required subject/version, grant/Authorization/request/consumer/actor, policy/root and generation/epoch coordinates directly. New observation bytes do not permit a new jurisdiction or changed requested effect. Unknown, denied, conflicting, changed-generation or different-jurisdiction recheck keeps the original claim spent/held.

The recheck record's findings must be derived from those actual finite API outputs and exact coordinate comparisons. Its schema fields describe evidence custody, not permission. A fixture recheck ALLOW still permits only the zero-effect simulation under this reference profile; operational flags remain false. Use the actual selected Unit B return object/member names during implementation and independently verify the adapter instead of manufacturing absent fields or flattening its three evaluation layers.

## Proposed states and order

States: PREPARED, EVALUATION_RECORDED, FENCED, CLAIMED, RECHECK_ALLOWED, TARGET_OBSERVED, COMPLETED, ABORTED_NO_EFFECT, EFFECT_OUTCOME_UNRESOLVED. They are reference journal states, not Brain machine or canonical states.

Required order: validate all identities and initial three-layer evaluation -> PREPARED -> durable EVALUATION_RECORDED -> durable FENCED -> durable one-shot CLAIMED -> fresh three-layer/context/revocation recheck immediately before target simulation -> RECHECK_ALLOWED -> separately observed target simulation -> TARGET_OBSERVED -> durable COMPLETED.

CLAIMED is a spent/held reservation against reuse, not completed consumption or effect success. All states retain runtime_authority=false, operative_grant=false, effect_permitted=false, durable_consumption=false and production_ready=false; local fixture reservation persistence must be labeled separately from an operative consumption claim.

Post-claim stale/revoked/conflicted/unresolved recheck prevents simulation and preserves the spent/held claim. ABORTED_NO_EFFECT requires independently bound target evidence proving no occurrence for this exact operation. A failure return alone is not proof of no effect. A crash at/after fencing conservatively becomes EFFECT_OUTCOME_UNRESOLVED unless reconstruction from authoritative journal and exact target evidence resolves it. Do not release exclusion or create a replacement operation merely to bypass uncertainty.

No completion before both exact positive target occurrence evidence and the matching durable terminal journal record. Effect with missing completion, completion with missing or negative target evidence, partial target effect, corrupt target evidence or contradictory references yields EFFECT_OUTCOME_UNRESOLVED. Completion and abort cannot erase prior evidence.

## SQLite journal and commit protocol

Use stdlib sqlite3 with explicitly configured foreign_keys=ON, synchronous=FULL and rollback journal DELETE for the initial reference. Verify returned configuration values; unsupported or failed configuration holds qualification. Use explicit BEGIN IMMEDIATE transactions for each state-changing event, with one-shot unique operation identity and monotonic sequence enforced in the database. Commit transaction before acknowledging that reference event as recorded. A local SQLite transaction does not provide cross-file atomicity with the fixture target.

Persist immutable event payload bytes, sequence, predecessor hash and event digest. Event digest is SHA-256 over the exact canonical record bytes excluding event_digest. predecessor_hash binds the preceding event digest; genesis uses an explicit NONE tag. Require exact equality between indexed columns and decoded payload coordinates. The chain establishes reference byte/order integrity only, not an authenticated issuer or hostile-administrator-proof append-only storage.

Journal replay reconstructs state exclusively from validated committed event rows, never from a cache or caller-reported state. A derived cache may be deleted and rebuilt; mismatch cannot overwrite authoritative records. Reject corrupt hashes, sequence gaps/reordering, conflicting duplicates, impossible transitions, inconsistent indexed fields, unknown versions and unsupported records. Unknown tail/failed read/ambiguous commit holds rather than treating a prefix as complete history. Application-level incomplete record bytes are rejected; SQLite corruption or missing WAL/journal components cannot be labeled harmless truncation.

Initial bounds: 1 MiB per serialized record, 64 nested levels, 100000 parsed nodes, 4096 events per qualification journal, 512-character identity coordinates; integers exact, booleans rejected as sequence/generation/version. Fix a deterministic serialization profile before implementation. No unbounded dependency loading, decompression, traversal or target evidence scans. File-system byte corruption tests operate on isolated copies only.

Process kill/reopen tests establish only measured results on the observed OS/filesystem/SQLite/configuration. Commit acknowledgement cannot guarantee power-loss durability on an unqualified storage stack. No same-host backup, hash chain or successful reopening proves off-host restore or permanent immutability.

## Recovery and independently bound target evidence

Recovery takes journal snapshot identity plus independently captured target evidence bytes/hash and expected operation/subject/context bindings. It must not synthesize target evidence from journal success fields. Validate the chain and state transitions first; reconcile only the exact fixture target for the exact operation.

If the claim exists and no simulation occurred, keep claim held; mark ABORTED_NO_EFFECT only after complete negative target evidence is proved. If exact occurrence evidence exists but terminal recording failed, report EFFECT_OUTCOME_UNRESOLVED and a proposed reconciliation record; do not silently manufacture prior completion or retry the target. A future reviewed reconciliation policy could record newly observed terminal facts with their actual observation provenance; it cannot backdate them. Contradictory completion/target evidence remains unresolved.

Recovery must test crash after fence, after claim, before/after fresh recheck, during target simulation, after target occurrence, during target evidence persistence and before/after completion commit. Maintain separate status for state reconstructed, target evidence verified, and terminal outcome resolved. Healthy process or successful SQL integrity_check alone does not resolve the outcome.
