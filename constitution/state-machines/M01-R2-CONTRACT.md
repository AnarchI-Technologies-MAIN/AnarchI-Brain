# SW0-010 M01 R2 repair contract
Status: CANDIDATE — UNFROZEN. Reference qualification only.

## Governing scope and preserved history

R2 supersedes the R1 and continuation-v1 reference APIs for new qualification work. Their original bytes and receipts remain historical evidence. R2 does not rewrite C9's historical 16 rows/25 predicate bindings or its empty C03 membership. It supplies explicitly new assessment/selection clauses and a new unified review surface. It creates no database, runtime resolver, durable recorder, effect executor, authority grant, commit, or gate closure.

Frozen laws remain constraints. Changes to the Cortex/Substrate-fin status endings and matrix historical terminology are recorded as editorial reconciliation, not changes to cells, bounds, authority dimensions, or proof of freeze. Current policy pointers and evidence are indexed separately.

## One attempt review, including both gate-entry routes

Every assessed progress attempt binds lifecycle, evaluation identity, operation identity, policy snapshot, subject version, epoch, applicable requirement catalog, declared predicate results and a source-state witness. Expected predicates come only from the pinned historical topology.

C03 and C04 both enter CI3_ACTION_GATED. Both require a distinct independent entry assessment with five candidate conditions: source state, bound scope, applicable gate, no semantic promotion, no protected execution on entry. The source witness identifies CI1_OBSERVED for C03 and CI2_PROPOSAL_AVAILABLE for C04. C04 retains P10. C03's historical predicate membership remains empty.

A unified AttemptReview carries predicate, requirement and entry findings plus admission findings. Empty historical C03 membership is insufficient without its complete entry assessment. Entry failures, missing reports and unknown findings remain available to diagnostic selection/closure; no disconnected Boolean is consumed.

Distinct evaluation identity separates assessment occurrences. It does not establish principal independence. Evaluation identity is unique within a lifecycle; the upstream admitted context must bind any proposer/authorizer independence required by frozen law.

## Admission dependencies and fail-closed defaults

Every catalog, predicate/requirement report, source witness, entry assessment, recording assessment and occurrence requires an independently admitted context bound to the exact report identity, scope and role. Absence of an admission verifier produces UNRESOLVED, never positive acceptance. Changing an admitted catalog to an empty requirement set invalidates the prior report binding.

The AdmissionVerifier interface is a dependency, not an implemented authenticator. It must independently establish issuer identity/jurisdiction, applicable root, completeness, effective authority where required, semantic interpretation, principal independence, policy snapshot, subject version, trusted epoch/freshness and revocation status. It must preserve determinate failures and unresolved input separately.

Tests use an explicit exact-payload fixture allowlist. That allowlist proves reference consistency only. It is not an issuer verifier, signature proof, completeness proof or production authority resolver. No catalog becomes trusted through a caller flag or a field named basis.

For opaque artifact content, Registry.review separately reports structural admissibility, secret-free content admission and contract-specific semantic resolution. Missing verifiers leave the latter two unresolved; generic representation cannot become a usable identity or effective authority.

## Deterministic diagnostic selection

Candidate policy: UNRESOLVED_PRESERVING_BLOCKS-v1.

- Known blocks with no unknown/missing finding select the matching CI5_BLOCKED diagnostic edge.
- Unknown or missing findings select the matching CI6_UNRESOLVED diagnostic edge, including when known blocks also exist.
- No findings select no diagnostic edge.
- Every route decision binds the complete attempt review and policy identity.
- Diagnostic acceptance requires that exact recomputed decision; an unselected route cannot be called successfully.

This policy makes an explicit control-route choice. It does not collapse the semantic findings into one dominant result. Both blocked and unknown/missing sets remain carried throughout recording and closure. A failed operation need not become successful to record or close its failure.

## Recording, effects and closure

The independently assessed recording action binds scope, provenance, no semantic promotion, recording authority, actual required conditions and effect scope. In this reference candidate, the only modeled permitted effect is reference_report. No function performs a durable record write or lifecycle transition.

Future durable receipt issuance, storage changes, integrity changes, disclosure or external effects are separate consequential operations owned by their declared lifecycles. This reference report does not authorize those effects, issue a receipt, or claim their occurrence.

Closure binds its exact predecessor report identity. Its evaluation cannot equal the operation, entry assessment, diagnostic predecessor or occurrence evaluation. C15/C16 require a qualified selected diagnostic predecessor and preserve the entire failed attempt. C14 requires an independently admitted occurrence, with an explicit assessed-attempt reference, policy snapshot, subject version and epoch matching the attempt.

Occurrence.fence_result assesses the freshness/context binding of the occurrence claim; it is not a claim that execution was authorized. A factual occurrence can be unauthorized. Recording or closing its record never retroactively legitimizes it.

## Freshness, retry, replay and in-flight revocation

No host time, transport time or ambient epoch is trusted. Epoch and subject version are explicit admitted context. Missing or differing epoch/version cannot pass. Actual atomic check-at-effect enforcement is downstream runtime work and remains unimplemented.

The owning lifecycle must re-establish effective authority, capability, permission and separately required authorization at its governed execution boundary. A revoked/expired prerequisite before effect prevents execution; revocation after a historical occurrence does not rewrite that occurrence. Compensation/reversal requires a new separately authorized operation.

Repeated evaluation of identical declared input is a pure deterministic replay of the same reference report, not another effect. A retry after changed input, policy, epoch or subject version requires a new evaluation identity and fresh admission. A predecessor's old positive flag cannot be reused. Duplicate effect suppression and durable idempotency are obligations of the owning lifecycle; no in-memory reference evaluation claims to implement them.

## Representation boundary

boundary_r2.py separates: duplicate-safe transport parsing; recursive ACS admissibility; complete-document binding; byte-exact canonical validation; immutable-registry binding; structural validation; content admission; contract-specific semantic resolution.

Arrays retain order, false/zero/empty/null are preserved, Unicode is not normalized, keys sort by UTF-8 bytes, and duplicates are rejected after escape decoding. Native floats/nonfinite numbers and unpaired surrogates are rejected before schema validation. Resource limits fail closed and do not change accepted canonical bytes.

Serialization does not guess identity, authority or secret meaning. Secret-shape screening belongs to artifact admission and rejects recognized nested secret keys/private-key markers. It is a conservative safeguard, not universal secret detection. Opaque strings require independent secret-free admission. No payload contents appear in rejection messages.

## Evidence and qualification limits

Persisted schema-corpus files retain exact bytes via .gitattributes; frozen schema/corpus digests are not regenerated. A fresh snapshot checkout under core.autocrlf=true must pass the old corpus.

Every required root member is tested by actual omission, alongside nested type, Unicode, duplicate parser, secret shape, context, topology, forged-summary and optimized-interpreter controls. Whole-lifecycle contact points are tested rather than only isolated Boolean formulas.

The evidence index records present sources and missing original closure receipts without fabricating historical proof. The 19-machine registry is retained; the supplemental obligation map assigns work to existing lifecycle owners and flags cross-lifecycle key custody/time/root-governance dependencies.

M01_FREEZE_READY remains False. Passing reference tests does not implement any admitted dependency, establish an independent review, prove production execution, or close any numbered gate.

