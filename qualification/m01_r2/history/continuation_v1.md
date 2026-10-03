# SW0-010 M01 continuation candidate

Status: PROPOSED, UNFROZEN. Repository application and gate closure are not performed.

## Verified starting point

Repair R1 runner SHA-256 is cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c. Its local qualification passed against HEAD 79fd607b3b8983fdd2d0254f3af59df9a92257b8. The repository remains the source for governing contracts; the runner reconstructs historical C9/C13 candidate text, not tracked M01 specifications.

## Proposed C03 entry assessment

C03 remains CI1_OBSERVED > CI3_ACTION_GATED. C9's empty predicate membership remains empty. A separate entry assessment is proposed; it is not an invented historical predicate binding.

Entry requires a distinct evaluation for the same lifecycle, operation, policy snapshot and C03 edge, with an explicit governing-basis reference. All five entry conditions must be reported SATISFIED:

- entry.source_observed: the source is established as CI1_OBSERVED;
- entry.bound_scope: entry is inside the applicable Cortex scope;
- entry.applicable_gate: the governing gate for this operation is identified;
- entry.no_semantic_promotion: entering assessment does not assign Evidence, truth, Authorization, Canonical Membership, or authority;
- entry.no_protected_effect: entry performs no protected operation.

These are new candidate assessment conditions. A scoped, established requirement set and satisfaction of its identified requirements remain necessary. Empty historical predicate membership alone never suffices. Requirements for later C05 execution are not universally imposed on C03; applicable entry requirements come from its own governing context.

A missing, blocked or unresolved condition prevents positive entry. Passing this reference check does not execute a transition, authenticate a source state, establish governance freshness, or grant execution permission. The external admitted assessment boundary is explicit and remains unimplemented. Context matching and an identifier are insufficient authentication.

## Proposed diagnostic selection boundary

Recompute attempt findings before inspecting witnesses. Known blocks and unresolved/missing findings remain separate and preserved.

- no witness: NO_DIAGNOSTIC_WITNESS;
- only known blocks: BLOCKED_WITNESS_ONLY;
- only unresolved/missing findings: UNRESOLVED_WITNESS_ONLY;
- both: DECISION_REQUIRED.

These are selection reports, not control outcomes or transitions. For a single witness class, the corresponding diagnostic action still requires Repair R1's independent recording assessment. For mixed witnesses, no route is selected automatically. No precedence is inferred, neither class is erased, and no new lifecycle state is introduced.

DECISION_REQUIRED makes the unresolved arbitration explicit; it does not complete arbitration. Final selection policy must be specified and separately qualified before M01 freezes. Closure through either historically proposed diagnostic route continues to preserve all original findings.

## Evidence and remaining gates

The companion harness tests the new reference entry condition and selection report against the pinned R1 model. It does not implement an authority resolver, runtime, database, provenance verifier or protected executor. Its test claims apply only to these candidate functions.

Remaining: choose and qualify mixed-witness arbitration; admit/authenticate governing, source-state, authority, occurrence and provenance assessments; complete retry/replay, receipt and carrier semantics; independently qualify the full lifecycle; discover and review repository application targets. M01_FREEZE_READY remains False.
