# AnarchI Brain: SW0-010 M01 Repair R1

**Status: proposed repair contract with an executed reference model. Not frozen or applied to the repository.**

This is a new, self-contained repair candidate. It is not represented as an in-place patch of the previous C17 downloadable file, whose bytes were not available in the current runtime. C9 and C13 are reconstructed from the supplied candidate text and checked against their recorded digests. The earlier candidates and receipts remain historical records.

## Scope

Repair the identified result-aggregation, prerequisite-satisfaction, diagnostic/closure, and qualification-harness defects. Do not implement authority resolution, cryptographic provenance verification, effect execution, databases, model integration, receipt issuance, or runtime deployment.

Repository precondition for local qualification:

- HEAD: `79fd607b3b8983fdd2d0254f3af59df9a92257b8`
- Tree: `2bc508ef199311208cc4b7c68398f61b22d4adf1`
- Clean tracked and untracked status and an unchanged index before/after the read-only qualification.

Source identities reproduced by the runner:

- C9: `29f5caf40e6c94c01030ab444ab06420498ca8e1b28ec1b2fdb59e917d8afa60`
- C13: `d1f1009d11eb0a18fce6ec66372f2d5a4340b9dc48e0eb9c9d13445d8388a54b`

## Source-derived constraints and new repair clauses

The supplied archaeology material identifies these existing constraints:

- `constitution/authority/AUTHORITY-DIMENSIONS.md:155`: Execute authority does not itself supply separately required authorization, permission, capability, qualification, or canonicalization.
- `contracts/cortex/CORTEX-CONTRACT.md:78-94`: required authority must resolve through its applicable path; Cortex cannot manufacture missing authority; unresolved required authority fails closed.
- `contracts/cortex/CORTEX-CONTRACT.md:116-118`: where permission is required, it must resolve through the governing contract; unknown permission cannot become permission.
- `contracts/cortex/CORTEX-CONTRACT.md:209`: successful execution does not retroactively authorize the operation.
- The source matrix separates a candidate assignment from frozen authority and reserves complete state-machine specifications to SW0-010.

The concrete aggregation and acceptance rules below are **new repair proposals implementing those distinctions**. They are not presented as already frozen clauses or as a completed runtime authority path.

## RP-01: lossless result collection

Keep per-predicate `SATISFIED`, `BLOCKED`, and `UNRESOLVED` unchanged. Collect separate sets of satisfied, blocked, unresolved, and missing IDs. Missing means no report was supplied; it is not a fabricated predicate result. A mixed result preserves both blocked and unresolved findings.

The aggregation model makes no dominant-result choice. Empty membership is `EMPTY`, not vacuous success. An aggregate can describe all expected members as satisfied without claiming that every governing prerequisite has been discovered or satisfied.

Validate context identity, expected membership, result labels, duplicate rows, and derived summary consistency. Recompute summaries from underlying rows before consuming them. A caller cannot upgrade a review by changing a cached `positive_conditions_met` flag or inserting a made-up blocking summary.

## RP-02: C05 actual requirement satisfaction

Keep P08 as a resolvability predicate. A known-absent authorization can remain a determinate value and therefore does not have to make P08 UNRESOLVED.

C05 positive acceptance additionally requires:

1. An applicable governed requirement-set assessment for the same operation, evaluation and policy snapshot, established as resolved and accompanied by a governing-basis reference.
2. Complete reports for the currently expected predicates, all SATISFIED.
3. Outcomes for every requirement identified by the governed set, with every required condition SATISFIED.

Required IDs come from the separately supplied governed expectation, not from whatever result rows happened to arrive. Omitting a required outcome is detected. An unresolved requirement set cannot become an established empty set. A determinately failed requirement prevents positive acceptance even when P03-P08 all report SATISFIED.

A governed, explicitly established set with no additional requirements is different from an absent or unresolved set. No universal Authorization Artifact, Capability Artifact, qualification, or canonicalization requirement is introduced by this rule.

**Trust boundary:** `GovernedRequirementSet` models an already-admitted assessment. The reference code validates identity/consistency but does not authenticate its issuer or implement the mechanism that establishes it. Feeding a forged assessment across that boundary remains an integration threat, not a solved cryptographic problem.

## RP-03: failure recording has its own assessment

Diagnostic edges C06-C13 use the assessed operation's findings as witnesses:

- A determinate blocking finding can justify a proposed BLOCKED control outcome.
- An unresolved finding or missing required report can justify a proposed UNRESOLVED control outcome.

They do not require the failed operation's predicates to become SATISFIED. Recording a failure does not make the original operation acceptable.

The proposed recording action has a separate evaluation identity and separately assessed conditions for bounded recording scope, usable provenance, no semantic promotion, and no protected effect. These are abstract candidate conditions; they do not prescribe a receipt, artifact kind, carrier, storage mechanism, or new authority grant.

The recording assessment must remain bound to the same lifecycle, operation and policy snapshot as its referenced attempt. It carries the original result report unchanged. Negative or missing conditions on the recording action itself prevent that recording action from passing the reference check.

When both blocking and unresolved findings exist, both diagnostic routes can have a witness. This repair does not secretly choose between them. Arbitration must be explicitly specified before M01 is frozen.

## RP-04: closure preserves the prior outcome

C15 and C16 can close a properly witnessed diagnostic state while preserving all original blocking, unresolved and missing findings. Closure does not make the original attempt eligible and does not create execution authority.

C14 needs an independently supplied execution-occurrence assessment bound to the same operation and policy context. A successful guard check is not evidence that execution occurred. The reference validates the occurrence assessment's context and required attribution field; it does not authenticate the occurrence claim.

A prior diagnostic result is recomputed before closure. Editing a summary's status flag cannot manufacture a valid predecessor state.

These rules specify reference conditions for candidate control transitions. They do not issue receipts, perform transitions, or authorize protected effects.

## RP-05: derive C9 bindings; do not restate the expected answer

The runner derives all 25 predicate bindings from C9's exact 16 rows. It handles `PREDICATES=NONE` as no members and validates predicate-field layout and IDs.

In local `--repo` mode it also launches a short noninteractive PowerShell regression. That regression reproduces the scalar `[0]` behavior and verifies the corrected `@(...)` extraction against the independently derived binding list. Native PowerShell is not emulated or marked passed when unavailable.

## RP-06: fresh C14 replay and honest test labels

All 74 C14 textual checks are recomputed against the exact C13 candidate. A61, A71 and A72 use corrected checks. No previous pass count is imported or incremented.

Four negative controls remove a negation or promote an unresolved statement. The appropriate checks must fail on those mutated statements.

This replay remains labeled **text qualification**. It is not evidence of live authority checking, provenance authentication, or successful resistance to forged runtime inputs. Historical C14/C14-R1 receipts are not overwritten or retroactively turned into new runs.

## Executed reference qualification

The bundled runner was executed with `--model-only` in the assistant's container:

| Test class | Observed result |
|---|---:|
| Aggregate reported-result/missing combinations over C9 memberships | 4,213 executed |
| C05 predicate/required-authorization/requirement-set combinations | 49,152 executed |
| All orderings of a mixed six-result report | 720 executed |
| Diagnostic edge families | All 8 checked |
| Invalid/context-mismatched/forged-summary inputs | 28 of 28 rejected |
| C14 text checks | 74 of 74 freshly passed |
| Prior C14 passes carried into this run | 0 |
| Text negative controls | 4 executed |
| Deliberately faulty reference variants | 12 of 12 detected |
| Total reference assertions | 120,281 passed |

The deliberately faulty variants include both lossy dominance rules, empty-set success, dropped missing rows, all-predicate-SAT as an execution guard, resolvability as satisfaction, unresolved empty catalog acceptance, requiring operation success to record or close failure, bypassing the recording action's own guard, treating guard success as execution occurrence, and erasing unknown findings at closure.

These are targeted reference-model regressions and report/formula mutations, not a complete mutation campaign against production code. The generic aggregate-vector test includes common result-label combinations that need not be reachable for every individual predicate. The reachable known-absence/P08 case is tested separately.

The repository snapshot checker was additionally tested on a disposable local Git fixture for clean state, untracked changes, unstaged changes, staged changes, and a wrong HEAD. That fixture is not Alexander's repository.

## Observed critical counterexample after repair

```text
LEGACY_ALL_PREDICATES_SATISFIED=true
P08_KNOWN_ABSENT_AUTHORIZATION="SATISFIED"
REPAIRED_C05_CONDITIONS_MET=false
REQUIRED_AUTHORIZATION_OUTCOME=["authorization"]
```

The aggregate and predicates need not be rewritten to hide the failure. The additional requirement-satisfaction condition rejects it directly.

## Local use

Save `sw0_010_m01_repair_r1.py` outside the repository. Python 3.10 or newer, Git, and PowerShell 7 are used; no external Python packages are required. The chat launcher validates the file hash and copies the complete receipt to the clipboard.

`--repo C:\AnarchI-Brain` checks the pinned repository before and after tests and requires the native PowerShell regression to pass. It runs read-only Git commands with optional locking and fsmonitor disabled. It compares the observed HEAD, tree, index hash and clean status. It does not claim that every ignored file or external process was immutable throughout the interval.

`--model-only` explicitly omits both local repository and native PowerShell qualification. Its PASS is not a local deployment or freeze approval.

## Remaining work, separate from these repairs

- C03's positive gate-entry acceptance remains uncompleted; empty membership does not open it.
- Arbitration between simultaneous BLOCKED and UNRESOLVED diagnostic-route witnesses remains unspecified.
- Admitted governance, authority, occurrence and provenance assessments still require their genuine source/resolution contracts and eventual implementation. Context equality alone does not authenticate or prove freshness.
- Full lifecycle closure, retry/replay, concrete carriers, and downstream integration are not supplied by this repair.

Consequently `M01_FREEZE_READY=False` remains intentional. Applying this candidate to repository specification files still requires target discovery, review, a bounded mutation preflight, and the existing commit/provenance workflow.

## Artifact identities

Runner SHA-256:
`cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c`

Executed qualification-transcript SHA-256:
`40485e85fe32210ce0d988d7b2d228d419e26601b95ecd389b501d1cea04e810`

A runner digest identifies implementation bytes. A transcript digest identifies a particular recorded execution of the reference checks. Neither by itself supplies authority or validates the facts assumed at an external governing boundary.
