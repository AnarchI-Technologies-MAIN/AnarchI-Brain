# Unit C ordering conflict review

**Status: unresolved design issue; no lifecycle implementation authorized by this note.**

The proposed Unit C lifecycle has two incompatible placements for the fresh authority recheck:

- The accepted Unit B v1.3 M14 interface draft defines `record_consumption(binding, fence_identity, fresh_evaluation)`. Its required order places the fresh authority recheck after the durable fence and before the durable one-shot consumption claim. See `../authority-unit-b-v1.3/contracts/M14-RECORDING-INTERFACE-DRAFT.md`, “Required future call/state interface” and “Required future order”.
- The isolated Unit C reference contract places durable `CLAIMED` before a fresh post-claim recheck, and requires that recheck immediately before target simulation. See `REFERENCE-CONTRACT-DRAFT.md`, “Initial evaluation and fresh recheck separation” and “Proposed states and order”.

One evaluation cannot satisfy both temporal requirements. This is a contract-order conflict, not a naming issue. It determines whether a failed freshness evaluation consumes the one-shot reservation and whether a second evaluation is required.

## Candidate reconciliation for adjudication

Preserve the M14 pre-claim requirement and retain Unit C's stronger point-of-effect check as a second, separately captured evaluation:

1. Validate and evaluate the initial fixture; durably record the reference evaluation and acquire the fixture fence.
2. Re-evaluate the independently supplied current grant, Authorization, request, policy, root, generation, revocation, and time evidence after fencing. Denied, stale, conflicting, or unknown results do not create the one-shot claim and cannot reach the fixture target.
3. Durably record the one-shot reference claim bound to that exact fresh evaluation.
4. Capture and evaluate a second fresh observation after the claim and immediately before the zero-effect target simulation. Any non-ALLOW result leaves the claim spent/held and prevents simulation.
5. Bind both observations independently to the immutable initial operation. Never overwrite initial evidence or reuse one observation to represent both times.

This candidate preserves the M14 call contract while making the post-claim check explicit. It adds a second evidence object and has not been accepted. It confers no real authority, consumption, effect permission, or production readiness; all implementation and runtime flags remain false.

## Decision required before lifecycle code

Lyra/human review must choose among:

- adopt the two-recheck reconciliation above;
- amend Unit C to follow M14's single pre-claim recheck and remove the post-claim requirement; or
- amend M14 before implementation to select a different single order.

Until then, lifecycle transition code, execution claims, and any proposed runtime wiring remain held. Pure serialization, schema, and journal-format review can proceed independently.
