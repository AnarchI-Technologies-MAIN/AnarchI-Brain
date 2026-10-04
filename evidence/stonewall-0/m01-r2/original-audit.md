# AnarchI Brain contract seam audit — 2026-10-01

**Decision: NOT READY to freeze M01 or advance SW0-010.**

The existing suites pass on the current checkout. That result coexists with reproducible candidate defects, a clean-checkout reproducibility failure, contradictory status language, and explicit unfinished authority/lifecycle boundaries.

This audit also reviews Lyra's continuation candidate. Its 4,134 passing assertions do not qualify the complete C03 entry/diagnostic path. Its identity and assertion checks can be removed by Python optimization. The earlier receipt remains a historical record of the narrower normal-mode test run; it must not be promoted into full lifecycle proof.

## Scope, preservation and evidence

- Reviewed all 56 existing files under `C:\AnarchI-Brain`, excluding Git internals, plus the three supplied repair artifacts and four existing continuation/qualification files: **63 source/evidence files**.
- Read governing Markdown and Python, parsed all schemas, fixtures and manifests, checked registry/fixture bindings, and exercised boundary counterexamples.
- Repository HEAD: `79fd607b3b8983fdd2d0254f3af59df9a92257b8`; tree: `2bc508ef199311208cc4b7c68398f61b22d4adf1`.
- All 63 inventoried file byte hashes remained unchanged. Repository HEAD/tree/index snapshots match; tracked/untracked status is clean.
- Audit scripts, reports and evidence were created only in this conversation's workspace. Disposable mutated-runner and checkout fixtures were created outside the repository and removed afterward.
- This is a current-file audit, not an exhaustive audit of every historical chat, remote repository, or unseen candidate. No runtime exploit or production authority resolution is claimed.

Evidence: [probe results and complete inventory](M01-seam-audit-evidence.json), [reproducible probes](audit_m01_seams.py), [fresh R1 baseline](audit-R1-baseline.txt), [fresh continuation baseline](audit-continuation-baseline.txt), [fresh SW0-006 baseline](audit-SW0-006-baseline.txt).

Fresh nominal runs: R1 passed 120,281 assertions and its native PowerShell regression; the continuation passed 4,134 assertions; SW0-006 passed 840 assertions. Counterexamples below identify what those runs do not exercise.

Severity describes importance before freeze or integration. **Reproduced** means executed against the actual supplied functions/files. **Contradiction** means incompatible or ambiguous normative text. **Open seam** means an explicit missing contract or ownership boundary, not a proven production bypass.

## Findings

### A01 — HIGH — Optimization removes qualification safeguards [Reproduced]

Location: `qualify_m01_next.py:52` and `:62`.

The runner identity check and test checks use Python `assert`. Under `-O`, those expressions are removed. A disposable R1 copy with deliberately changed bytes, whose hash did not match PIN, was accepted by the continuation harness. It printed `ASSERTIONS=4134`, `RESULT=PASS`, and exited zero. The count continued increasing even though the corresponding assertion comparisons were removed. `PYTHONOPTIMIZE` provides another way to enable the same behavior.

Repair: use unconditional explicit rejection/check functions for identity, qualification and snapshot comparisons. Include optimized/interpreter-environment runs as negative controls. Do not replace the earlier receipt; create a separately identified corrected candidate and receipt.

### A02 — HIGH — C03 has two incompatible result surfaces and loses entry failures [Reproduced]

Location: `qualify_m01_next.py:21`, `:37`, `:82`; R1 `evaluate_attempt`, line 265.

With a valid admitted empty entry requirement set and all five entry checks satisfied, the new entry function returns True while the carried R1 `AttemptReview.positive_conditions_met` remains False. With `entry.bound_scope=BLOCKED`, entry returns False, but the selection report still returns `NO_DIAGNOSTIC_WITNESS`, with no blocked/unresolved/missing findings. The entry function returns only a Boolean; its assessment findings never enter the carried attempt report.

This is a composition defect even though each isolated Boolean test passes. A consumer can disagree about whether entry succeeded and cannot diagnose why the new entry check failed.

Repair: define one typed entry review carrying its own full assessment, governed requirements, source-state witness and eligibility. Diagnostic selection and closure must consume that exact review. Preserve operation and recording assessments separately.

### A03 — HIGH — The alternate route into ACTION_GATED has no corresponding new entry boundary [Reproduced / Open seam]

Location: R1 C9 rows C03/C04; `M01-next-candidate.md:11`; R1 `evaluate_attempt`, line 245.

C03 and C04 both target `CI3_ACTION_GATED`. The new candidate covers only C03. C04 can return positive with P10 SATISFIED and an established empty governed requirement set, without any of the five new entry assessments. This is not proof that C04 is forbidden under the historical candidate; it shows that the proposal has not decided whether entry conditions are C03-specific or invariants of the shared destination state.

Repair: identify shared state-entry obligations and route-specific obligations explicitly, then test both ingress routes. Do not silently copy later execution requirements onto entry.

### A04 — HIGH — DECISION_REQUIRED is advisory and does not gate diagnostic acceptance [Reproduced / Open seam]

Location: `qualify_m01_next.py:37`; R1 `evaluate_diagnostic`, line 307.

For the same mixed blocked/unresolved attempt, selection reports `DECISION_REQUIRED`, but direct R1 calls accept both C09 and C13 when their recording assessments pass. Neither function requires a selection decision or an arbitration witness. The candidate correctly says arbitration is unfinished; therefore the label is informative, not an enforced lifecycle rule.

Repair: specify who selects, what inputs govern selection, what happens while selection remains unresolved, and what binds the selected route. A future transition-facing function must require that result rather than permit optional consultation. Retain both original finding classes.

### A05 — HIGH — Caller-supplied topology can weaken the reference guard [Reproduced]

Location: R1 `evaluate_attempt`, line 254, and `validate_attempt`, line 271.

Both accept an arbitrary topology dictionary. Changing C05 membership from P03–P08 to only P03 produces a positive attempt, and validating that attempt against the same changed dictionary succeeds. The normal main function uses `sources()`, so this is an exposed helper/API weakness rather than an observed bypass of the pinned CLI run.

Repair: pin topology identity at the assessment boundary or encapsulate it in a verified immutable specification object. Recompute against the governing specification, not the caller's replacement. Test removed guards and changed source/target states.

### A06 — MEDIUM — P08 helper trusts cached findings it does not validate [Reproduced]

Location: R1 `p08_reference`, line 278.

Replacing a mixed requirement report's blocked/unresolved/missing summaries with empty tuples changes this helper's result from UNRESOLVED to SATISFIED. It never calls `validate_findings` or checks that the report is bound to the supplied catalog. The helper is currently used for a reference regression, and the normal attempt path performs stronger validation; this is not evidence that C05 authorization was bypassed.

Repair: validate findings and catalog/report context before reading summaries, or make this helper explicitly private to trusted freshly computed reports.

### A07 — MEDIUM — Diagnostic and closure can reuse one evaluation identity [Reproduced / Open seam]

Location: R1 `record_assessment`, line 299, and `evaluate_closure`, line 329.

Recording evaluation must differ from the operation evaluation, but closure may reuse the diagnostic evaluation identity. A C09 diagnostic and C15 closure both labeled `evaluation='record'` were accepted. The complete frames differ by edge, so this is not an identical-frame collision. The seam is that evaluation identity is not defined consistently as global, per edge, or per assessment occurrence.

Repair: define evaluation identity scope and predecessor binding, then enforce the intended uniqueness/replay rule. Avoid treating a distinct string as principal independence.

### A08 — HIGH — Governing assessments remain an unauthenticated admission boundary [Open seam, demonstrated model sensitivity]

Location: R1 `GovernedRequirementSet`, line 216, and `evaluate_attempt`, line 245; supplied repair contract RP-02.

The model rejects an identified blocked required authorization. It accepts all-satisfied predicates when the caller supplies an established empty requirement catalog. That difference is intentional only if catalog completeness, applicability and issuance were independently established. The code checks consistency and identifiers, not the truth or authenticity of that admission.

Repair: specify the governing admission contract, independent issuer/authority path, completeness proof, policy snapshot identity, freshness and scope rules. Treat admitted test fixtures as fixtures. Do not claim that context equality supplies these properties.

### A09 — HIGH — Schema validation and ACS-1 admissibility do not compose over the permitted value space [Reproduced]

Location: all 18 root schemas; `schemas/conformance/run_sw0_006.py:263`; `serialization/CANONICAL-SERIALIZATION.md` sections 5, 8–10.

Every root schema accepted a nested `{"value":0.5}` in a general semantic field; the provided serializer rejected it with `ACS1_NATIVE_FLOAT_FORBIDDEN`. Integral floating values such as 1.0 also pass integer structural checks in relevant fields but fail the serializer. Generic nested objects/arrays are not recursively restricted to ACS-1's value space. Unpaired surrogate strings have the analogous Unicode seam.

The contracts distinguish structural validity from canonical serialization, so an unencodable structural value does not automatically violate the root-schema layer. The defect is the absent explicit composed admissibility boundary and its insufficient fixture coverage.

Repair: specify recursive ACS-1 admissibility and preserve numeric types at parse time. Require a composed validation result before emitting complete canonical documents; test nested values and numeric/Unicode edges.

### A10 — HIGH — Parsing discards duplicate-key evidence before validation [Reproduced]

Location: SW0-006 runner `json.loads` calls at lines 397, 403, 437, 520 and 1034; ACS-1 sections 13 and 35.

A document containing both `schema_id="wrong"` and a later correct `schema_id` was parsed using the runner's parser pattern. The first value disappeared; the resulting object passed the Observation schema. The encoder cannot detect a duplicate after it has been collapsed into a dictionary.

These parsing calls currently ingest controlled manifests/fixtures. No public ingress implementation exists here. The risk is reusing that parse/validate/encode pattern as ingress or canonical-byte validation.

Repair: reject duplicate decoded keys during parsing, including escape-equivalent keys, before building ordinary mappings. Keep original bytes/provenance distinct from any normalized representation.

### A11 — HIGH — Private-key exclusion has no demonstrated enforcement path [Reproduced acceptance / Open seam]

Location: `schemas/CORE-SCHEMA-CONTRACT.md:978`, `:1460`; ACBP-1 section 21; general nested root-schema fields.

All 18 schemas accepted an object containing a `private_key` member with a clearly dummy test string. The serializer encoded it. No real key was used or printed. This proves arbitrary nested content is not screened for the constitutional exclusion; it does not prove that the dummy value is private-key material or that a real secret was leaked.

The existing 90 crypto-uniformity tests exercise forbidden top-level public crypto fields, not private material in permitted nested payloads. A schema cannot generally recognize every secret embedded in arbitrary observations or strings.

Repair: identify the admission/projection/diagnostic boundary responsible for excluding secret material, define permitted opaque content and controlled handling, and add negative fixtures. Narrow the exclusion proof claim to what is actually tested until that boundary exists.

### A12 — HIGH — A clean checkout at the same commit fails 39 persisted digests [Reproduced]

Location: raw-byte digest binding in SW0-006 runner and manifests; repository has no `.gitattributes` file.

The current bound files are LF and match their Git blobs. A disposable clean local clone at the identical HEAD, with `core.autocrlf=true`, failed **39** checks: three corpus bindings, 18 schema digests and 18 fixture digests. Exit code was one. Your global Git setting is currently `core.autocrlf=true`.

Failing closed on changed bytes is correct. The reproducibility defect is that ordinary checkout transformation changes the exact bytes the repository's evidence expects, while Git still reports a clean tree.

Repair: define exact repository byte/line-ending policy for digest-bound artifacts through a separately reviewed change. Preserve the frozen digests and evidence identities; do not casually regenerate them to accommodate a transformed checkout. Qualify fresh-checkout behavior.

### A13 — HIGH — Frozen status and candidate-status clauses conflict [Contradiction]

Location: `contracts/organs/AUTHORITY-MATRIX.md:3`, `:19`, `:50`, `:110`; `contracts/cortex/CORTEX-CONTRACT.md:3`, `:411`; `contracts/substrate-fin/SUBSTRATE-FIN-CONTRACT.md:3`, `:477`; `STONEWALL-SEQUENCE.md` Current Position.

The sequence and headers say SW0-007/008/009 are frozen. Matrix vocabulary still defines yes/bounded/no as candidate assignments and warns that appearing in this candidate does not freeze them. Cortex/Substrate-fin endings say the gates remain candidates until their closure conditions are proven, without a local proof link. Some language can be read as historical derivation, but the active semantics never clearly reconcile those readings.

Repair: add an explicit, provenance-bound status reconciliation that distinguishes historical origins from current normative assignments. Preserve unresolved cells. Use the applicable governance amendment workflow for frozen text.

### A14 — MEDIUM — Resolution and validation claim overlapping evaluation responsibility [Contradiction]

Location: `resolution/RESOLUTION-CONTRACT.md:25`, `:42`; `validation/VALIDATION-CONTRACT.md:19`, `:33`.

Resolution VALID requires an available interpretation and the ability to evaluate. Resolution INVALID requires evaluated content to violate the contract. Validation separately owns evaluation after interpretation resolution. A known schema with invalid instance content can therefore be resolution-VALID under one paragraph and resolution-INVALID under another.

Repair: decide whether resolution owns only context selection or also a named structural evaluation, and use typed result boundaries. Define unavailable context and mixed failed/unresolved checks explicitly. Do not reuse bare VALID/INVALID labels without their owning contract.

### A15 — MEDIUM — Structural member presence does not establish usable identity or result semantics [Open seam]

Location: root schemas for Observation, Authority Grant, Authorization, Validation Result and Qualification Result; core schema sections 21–23; supplemental Validation section 3.

Broad semantic fields allow empty strings, Booleans, integers, objects and arrays. They do not prove a resolvable subject, source, operation or governing contract. The validation fixture uses PASS while the supplemental validation vocabulary is VALID/INVALID/UNRESOLVED. The fixture references a separate dummy contract, so PASS is not by itself a contradiction; there is simply no tested adapter to the actual supplemental contract.

Repair: define contract-specific identifier/result resolution and reject missing/ambiguous interpretation there. Keep generic representation and effective interpretation distinct. Do not impose one universal identity envelope or qualification vocabulary.

### A16 — HIGH — Historical closure assertions lack an in-repository evidence map [Open seam / preservation gap]

Location: closure endings of frozen documents; `constitution/state-machines/REGISTRY.md`; `evidence`, `tests`, `spec` directories; R1 C9/C13 headers.

Current evidence/tests/spec directories contain no files. The only tracked executable corpus is SW0-006. `git log --all -- evidence tests` returned no entries. The frozen law documents assert their conditions were proven, but this repository has no indexed receipts binding those proofs to reviewed bytes and outcomes. R1 reconstructs C9/C13 from embedded text and hashes, while C6/C7/C8/C11/C12 are represented only by upstream hash references in those headers.

This audit does not conclude that historical proofs never existed elsewhere. It concludes that a reviewer cannot reproduce or verify their complete chain from the files currently present.

Repair: locate and preserve original artifacts/receipts, build an exact-byte provenance index, and mark unavailable evidence explicitly. Do not fabricate new historical receipts or label a new run as the original closure.

### A17 — HIGH — Required consequential lifecycles have no explicit ownership map [Open seam]

Location: state-machine registry lines 9–27; authority contract sections 8, 11; ACBP-1 sections 43, 48, 49.

The registry lists 19 lifecycle names but does not assign Authorization issuance/use/expiry, identity/key enrollment, key rotation/custody, trusted time, or governance-root replacement to concrete owning machines/contracts. Authority Grant, Capability, Revocation and Schema/Policy Root are plausible owners for parts of this work, but naming them does not resolve the ownership. Substrate-fin is also absent from the organ matrix; whether it is a substrate boundary, a delegated participant, or an authority-bearing organ needs explicit ownership when it performs consequential work.

Repair: map each consequential operation to an existing declared lifecycle and applicable authority/root, or use an explicit sequence/registry amendment when necessary. Avoid silently adding a twentieth machine or assigning missing authority.

### A18 — HIGH — Recording/closure scope is not connected to actual recording effects [Open seam]

Location: R1 `RECORD_CHECKS`, line 285; semantic language Consequential Transition definition; registry receipt requirements.

The model asks for `record.no_protected_effect`, but the future recording action may change durable receipts, integrity state, or externally observable state and thus itself need consequential-transition governance. Four abstract labels do not identify which effects are permitted, the required authority/prerequisites, receipt issuance, or what happens if recording fails. There is no runtime recorder here, so this is a design boundary still requiring a contract.

Repair: define the bounded recording operation, its governed effects and separate authority/requirements. Do not require the failed operation to succeed first. Preserve the original failure even if recording or closure is itself blocked/unresolved.

### A19 — MEDIUM — Occurrence, predecessor and in-flight freshness are not fully bound [Open seam]

Location: R1 `OccurrenceAssessment` and `evaluate_closure`, lines 322–348; authority contract section 8; ACBP-1 replay boundary.

C14 occurrence assessment matches lifecycle, operation, policy and C05 edge but has no explicit assessed-attempt reference, subject/version, effective-authority interval, revocation epoch or replay token. A distinct occurrence evaluation is intentionally allowed, but its relationship to a particular attempt is not represented. The complete treatment of revocation/expiry between checking and execution, retry, conflicting occurrences and repeated closure remains unspecified.

Repair: specify exact assessment/predecessor identities and freshness requirements as governed input, plus in-flight revocation, idempotency and replay behavior. Do not infer trusted time from the host or interpret guard success as execution occurrence.

### A20 — MEDIUM — Qualification coverage is much narrower than a whole-contract proof [Reproduced coverage weakness]

Location: SW0-006 runner lines 618–637, 1034–1077, 1079–1104; R1 faulty variants at lines 614–636; continuation tests.

Required-semantic tests mostly substitute Null rather than remove each member. Removing `source` from an in-memory Observation schema's required list permits an omitted source while the old Null test still rejects Null. Frozen digest checks would detect an unapproved on-disk schema edit; this counterexample concerns test sufficiency, not bypassing those digests.

ACS composition repeats one serializer over simple fixtures, not an independent implementation or the full ACS value space. The 12 R1 faulty variants are targeted report/formula comparisons, as its contract honestly notes; they are not an exhaustive mutation campaign. `False` flags for no authority/no protected effects are declarations of scope, not measurements of a production resolver/executor. The continuation's isolated formulas missed A02–A04.

Repair: add integrated lifecycle/contact-point counterexamples, omitted-member controls, topology removal, malformed parser input, optimized interpreter runs, fresh-checkout reproduction and exact scope labels. Preserve the useful existing tests; expand evidence where a consequential claim actually needs it.

## Repair order

1. Correct continuation qualification safeguards and unify C03 entry/diagnostic review (A01–A02). Keep its current bytes/receipt as historical evidence.
2. Specify shared gate-entry obligations and enforced mixed-route selection, with pinned topology and validated helper inputs (A03–A07).
3. Define admitted governance, recording/closure effects, predecessor identity and replay/freshness requirements (A08, A18–A19).
4. Qualify representation boundaries: ACS admissibility, duplicate-safe parsing, secret handling and fresh-checkout bytes (A09–A12).
5. Reconcile frozen-status language, resolution/validation boundaries and owning lifecycles using governed candidate amendments (A13–A17).
6. Recover original evidence and expand conformance coverage before any freeze claim (A16, A20).

No fixes were applied by this audit. No commit, push, deployment, constitutional status change, or gate advancement occurred.
