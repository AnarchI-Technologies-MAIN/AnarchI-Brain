# M14 occurrence-recording dependency interface draft

PROPOSED / NOT ADOPTED / INTERFACE ONLY / NO DURABLE OCCURRENCE CLAIM.

Unit B diagnostics are finite reference artifacts, not signed authority, M14 committed receipts or proof of actual consumption. This interface names the dependency needed before future consequential authorization consumption can succeed; it does not select the M14 lifecycle or implement a storage system.

A future occurrence record must bind exact subject and authorization/grant references, operation and purpose/scope, governing contract/policy/root pins, predecessor/expected state, generation/epoch, idempotency identity, all findings, actual terminal effect/state and durable commit identity. An acknowledgement may claim only the durability and custody actually established; it cannot retroactively authorize an effect.

The binding includes all three distinct layers: grant identity/version/digest, Authorization identity/version/canonical digest, and requested effect identity/digest. Retain separate GrantEvaluation, AuthorizationEvaluation and ConsumptionEvaluation identities/findings, consumer, effect actor and target, current generation/epoch and independent grant/Authorization revocation context. A record binding only a parent grant cannot establish that a particular Authorization was issued or consumed. Replay must recheck all layers and current disclosure authority, with no grandfathering or cross-generation reuse.

Recording must be coordinated with the effect fence and recoverable protocol. Missing or failed record, partial commit, uncertain actual effect or unavailable replay evidence cannot produce a success receipt or blind re-execution. Recovery must reconstruct actual state from authoritative records and re-evaluate current disclosure/authority; caches are not authority. Off-host custody or recoverability requires separately demonstrated evidence, not a same-host backup label.

Unit B creates no durable registry, transactional journal, publication acknowledgement, signature, canonical receipt, external-store mutation or production recovery proof. All such operational prerequisites remain held. A diagnostic digest can identify reference bytes but cannot replace an occurrence record.

## Required future call/state interface — not implemented

Every future call binds exact authorization/grant and requested-effect digests, subject identity/version, full scope/purpose, governing contract/policy/root, predecessor, generation/epoch, evaluation digest and operation/idempotency identity. The following are dependency signatures, not callable Unit B methods:

- prepare_effect(binding) -> PREPARED_CANDIDATE or HELD. No protected effect or consumption yet.
- record_authority_evaluation(binding, findings) -> EVALUATION_DURABLE or RECORD_FAILED. Never acknowledge unestablished durability.
- acquire_effect_fence(binding, expected_state) -> FENCE_DURABLE or HELD. Requires recoverable exclusion and current external generation; a local lock alone is insufficient.
- record_consumption(binding, fence_identity, fresh_evaluation) -> CONSUMPTION_CLAIM_DURABLE or RECORD_FAILED. This pre-effect operation is a one-shot durable claim/reservation against reuse, not evidence of actual effect or successful completed consumption. Fresh evaluation occurs after the durable fence and before effect; unknown authority holds.
- commit_effect(binding, fence_identity, consumption_identity, actual_effect) -> EFFECT_AND_COMPLETION_DURABLE or EFFECT_OUTCOME_UNRESOLVED. Success requires actual effect evidence plus durable completion, not merely a receipt.
- abort_effect(binding, fence_identity, observed_state) -> ABORTED_NO_EFFECT or EFFECT_OUTCOME_UNRESOLVED. An abort cannot erase a possibly occurred effect.
- recover_incomplete_effect(binding, authoritative_records, actual_state_evidence) -> RECONCILED_TERMINAL or EFFECT_OUTCOME_UNRESOLVED. No blind retry or cache-only reconstruction.

Required future order: evaluation -> prepared candidate -> durable evaluation/fence -> fresh authority recheck -> durable consumption binding -> effect -> durable completion. Any failed recording or crash at/after fencing holds EFFECT_OUTCOME_UNRESOLVED until authoritative reconciliation; do not invent terminal success, release uncertain exclusion or retry the effect. Unit B's modeled NOT_CONSUMED/PREPARED/CONSUMED/UNKNOWN inputs and effect_observation values test those holds only. Even a fixture marked CONSUMED does not establish durable consumption or implement this interface.

The pre-effect consumption binding is only the durable one-shot claim/reservation. Actual effect success and terminal consumption completion require separately verified effect evidence plus durable completion. This entire future interface remains unimplemented in Unit B.
