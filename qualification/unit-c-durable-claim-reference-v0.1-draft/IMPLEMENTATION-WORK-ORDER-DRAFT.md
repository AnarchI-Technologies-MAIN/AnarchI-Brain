# Unit C bounded implementation work order

PROPOSED SOURCE WORK / NO DOCUMENT ADOPTION, ENROLLMENT OR LIVE EFFECT.

1. Capture exact adopted Unit B contract/source/schema/catalog and acceptance/retention references; keep actual root/input prerequisites unresolved. Define the SQLite/fixture serialization version and externally pinned dependency set. Do not use directory labels as adoption evidence.
2. Implement immutable binding and event validators using the closed schemas; reject omitted/extra coordinates, bool integers, malformed digests and unsupported state/version. Typed evaluation references remain distinct. Unknown operational authority always stays held.
3. Implement a disposable SQLite backend with explicit verified settings, transactions, unique identity, committed hash-chain rows and replay from rows. Separate read-only state reconstruction from mutation. Bound inputs and total events.
4. Implement a separately persisted zero-effect target ledger in another task-owned path. Bind target evidence independently to operation/subject/context. Never derive success solely from the authority journal or a submitted boolean.
5. Compose only the proposed order: validation/evaluation -> durable fence -> durable one-shot claim -> fresh post-claim recheck -> simulated target -> completion. Keep no-effect/uncertain states distinct and operational flags false.
6. Test deterministic fresh success and denial paths, exact replay, changed-subject/context conflicts, duplicate concurrent claims, stale/revoked post-claim recheck, cache deletion/drift, corruption/hash/order failures and every crash cut. Explicitly test effect-without-receipt and receipt-without-effect; both must remain unresolved.
7. Qualify normal and optimized Python on observed Windows and isolated Ubuntu fixtures. Exercise resource/disk/locking errors in task-owned paths. Use subprocess kill/reopen tests for actual process-crash evidence; static state fixtures alone are insufficient. Preserve failures and exact commands/results.
8. Consult independent review on exact source, schemas, custody bindings and observed evidence. Do not adopt the unit, mutate gates, connect real consumers or deploy from passing tests.

Reviewable invariants: claim != effect success; no completion without independent exact target evidence; no protected effect before post-claim freshness check; no blind retry after uncertainty; operation identity covers all three authority layers and actual request/context; caches never authoritative; missing evidence remains unresolved; history is append-preserved; every runtime flag remains false.

Unresolved operational dependencies are exact actual root selection, principal/key/control admission, authenticated grant and positive Authorization issuance, current generation/revocation/time evidence, access/disclosure scope, actual executor/target contract, production effect fence/durable storage and recovery. They block operational claims, not this isolated reference work.
