# M01 R2 independent source review

## Decision

**HOLD FOR REFERENCE REPAIR. Do not freeze M01 or advance SW0-010 on this evidence.**

The submitted archive is internally consistent and the supplied reference suites pass when freshly executed. Independent boundary probes nevertheless reproduce additional defects and identify one source-level coverage hole. The review findings below supplement, rather than overwrite, A01-A20 and the historical receipts.

This review is of the exact uploaded snapshot. It is not a production exploit assessment, a Windows repository qualification, an authentication implementation, or an exhaustive proof of the entire lifecycle.

## 1. Exact review basis and preservation

Archive: `M01-R2-review-20261001T221519Z-0f92b879.zip`

Archive SHA-256:

`20b82017d4fe0bd1da6a957d6dc390e04a9afc4573f664a31267688daa870a42`

R2 repair-manifest SHA-256:

`f66f82eb731b821e2ecab64f3b185b18222ca7f3c772a13a079a691fff3e67ac`

The archive contains 82 candidate/source files, 56 baseline Git blobs, and four review metadata files. All 140 inventory entries matched their recorded byte sizes and SHA-256 values. All 81 manifest-bound candidate files matched; the additional candidate file is the manifest itself, whose identity also matched the collection receipt. All nine preserved-copy entries matched their preservation hashes. The three separately retained frozen-baseline copies matched their corresponding raw baseline files.

Recomputing Git blob and tree identities from the archived modes, names, and raw bytes reproduced the recorded baseline tree:

`2bc508ef199311208cc4b7c68398f61b22d4adf1`

The raw commit object and Git index were not included. Therefore the reported HEAD `79fd607b3b8983fdd2d0254f3af59df9a92257b8` and index digest were not independently reconstructed or checked against a live Windows repository. Tree reproduction must not be promoted into commit/author/history verification.

### Two different preservation comparisons

The candidate has seven tracked-file changes relative to the pre-repair working-tree hashes recorded in preservation.json. The other 49 original working-tree files remain byte-identical. These seven paths match the manifest's authorized_modified_files list.

Against the raw baseline Git blobs, 47 files are byte-identical and nine differ. The extra two differences are pre-existing representation differences, not new R2 edits:

- `constitution/authority/AUTHORITY-DIMENSIONS.md`: the working-tree version has one CRLF terminator; its raw Git blob has none.
- `semantic-language/SEMANTIC-LANGUAGE-v1.md`: the working-tree version has three CRLF terminators; its raw Git blob has none.

Both working-tree hashes already appear in the pre-repair inventory. All other text matches after LF normalization. Their two identities must remain distinct in the evidence index rather than being silently reconciled.

All inventoried captured bytes and all bound execution-copy bytes were checked again after testing and remained unchanged. The original ZIP still has its supplied digest. No Windows repository was accessed. No source commit, source staging, freeze, deployment, protected operation, or historical-recovery installation was performed. Checkout and cache experiments used disposable copies and temporary Git indexes only.

## 2. Freshly executed nominal qualification

Environment: Linux, Python 3.13.5, jsonschema 4.26.0, Git 2.47.3. The user-supplied Windows receipts reported Python 3.14.6; this review does not silently substitute its environment for theirs.

| Execution | Observed result | Scope |
|---|---|---|
| R2 test file, normal Python | 15 test methods passed; exit 0 | Actual archived R2 test source |
| Same R2 test file with `-O` | 15 test methods passed; exit 0 | Optimized execution, not carried-forward counts |
| Preserved SW0-006 runner | 840 reported assertions; zero failures; exit 0 | Actual archived schema corpus |
| Preserved R1 runner with `--model-only` | 120,281 reported assertions; exit 0 | Historical reference model only |
| Deliberately changed historical runner, optimized R2 input check | Exit 1; `HISTORICAL_RUNNER_IDENTITY` | Source-file negative control |
| Six active Python files, AST inspection | Zero `ast.Assert` nodes | Active sources only; history remains history |

The R2 suite's 8,192 entry vectors run inside each of the two 15-method executions. They were not counted as 8,192 separately named unit tests.

The full Git/index-bound `qualification/m01_r2/qualify.py` and `rescan.py` commands were not run as if the archive were the original repository. Their baseline HEAD/index preconditions cannot be honestly satisfied by this export. Native PowerShell is unavailable here; its regression remains supported by the supplied local receipt, not a newly performed native run.

The independent lifecycle/representation probes were repeated with optimized Python and returned identical observations. The cache probe and checkout probes were separate experiments, with their own explicit scope.

## 3. Findings

Source references below are relative to the archive's `repo/` directory, with physical line numbers from the exact captured files. Severity describes importance before extending or qualifying these boundaries. It is not a claim of production exploitability.

### R2-REV-01 | HIGH | A source hash does not bind the code actually loaded from a bytecode cache

**Locations:** `qualification/m01_r2/model.py:15-29,40-42`; import/child boundaries in `qualification/m01_r2/qualify.py:78-81`.

The loader hashes `history/repair_r1.py`, then independently asks an import loader to execute that file. Those are not necessarily the same byte representation. In a disposable copy, a timestamp-matching cached `.pyc` containing a harmless topology-test alteration was supplied while the `.py` source remained byte-identical.

Observed under `python -B` and `sys.dont_write_bytecode=True`:

```
source_pin_matches: true
historical_source_sha256: cb8a492c4667ffaaf0ef1ac1b62f2c9883c9e90d09873d470aeb47175a100a6c
actual_C05_predicate_ids: [P03]
expected_C05_predicate_ids: [P03, P04, P05, P06, P07, P08]
```

A separate control compiled the checked source bytes directly and recovered all six predicates despite the conflicting cache. This demonstrates the distinction experimentally; merely disabling new bytecode writes did not prevent this cache from being read.

**Scope qualification:** This was a direct loader/reference-API counterexample. It did not demonstrate passage through the full Windows Git-bound qualification command. The current bundle preflight can reject unexpected untracked cache files when Git exposes them; that additional check does not make the loader's source-hash check itself an execution binding. No poisoned cache is alleged to exist on the user's machine or in the uploaded archive. The supplied `.gitignore` is not claimed to exclude Python caches.

**Repair:** Compile/execute the exact in-memory bytes that were hashed for the historical loader. Apply an equally explicit verified-source/staging policy to active imports and qualification children, rather than assuming source-file hashes bind arbitrary cached execution. Preserve normal dependency trust boundaries; this does not require a runtime authority service.

**Required regression:** With source bytes intact and conflicting cache content present in an isolated fixture, either reject before use or load the verified source and retain the exact six-member C05 topology. Test normal and optimized cache variants. A changed-source rejection alone is insufficient.

Evidence: `results/bytecode-loader-counterexample.json`; reproducer: `tools/probe_verified_loader.py`.

### R2-REV-02 | HIGH | Recording admission is not bound to the attempt or predecessor it records

**Locations:** `qualification/m01_r2/model.py:89-94,249-271,281-319`; contract `constitution/state-machines/M01-R2-CONTRACT.md:18,22,44-48,58`.

An `Assessment` carries its own context, basis, rows, and permitted effects, but no assessed-attempt or predecessor identity. `recording()` checks shared lifecycle/operation/policy/version/epoch and passes only the assessment to admission. The final ControlReview adds an attempt/predecessor digest after that admission. It does not bind the admitted assessment to that target.

An exact-payload fixture verifier was used. Two distinct failed attempts, `attempt.A` and `attempt.B`, shared the declared operation scope. A single recording assessment/evaluation `record.shared` was admitted once. Diagnostic review returned `conditions_met=True` for both attempts. Crucially, the recording verifier received identical `(context, role, payload digest)` inputs in both cases, even though the carried attempt digests differed.

The analogous closure probe reused one admitted closure assessment for two different diagnostic predecessors. Both closures returned True; their predecessor digests differed while their assessment and closure evaluation were identical.

This is not ordinary deterministic replay: the target being recorded changed. Global evaluation-identity uniqueness is not enforced by these pure functions, and the admission interface cannot distinguish the target relationship using the arguments it currently receives. Merely asking a future authenticator to enforce the missing relation does not supply it.

**Scope qualification:** No recording effect occurred and no protected authority was granted. The observation concerns reference assessment correlation and the contract's identity/replay claim, not forged production signatures or unauthorized external execution.

**Repair:** Include an immutable target binding in the admitted recording request. Diagnostic admission should identify the exact attempted review; closure admission should identify the exact predecessor and carried attempt. Keep recording's own evaluation/context separate. Either explicitly model permitted reusable scope or reject cross-target reuse; do not leave reuse implicit.

**Required regression:** Admission for attempt A or predecessor A must not authorize an otherwise context-identical recording for B. Same-input replay must remain deterministic. Changed-target reuse must fail before a positive ControlReview is produced. Continue preserving blocked and unresolved findings separately.

Evidence: `results/independent-counterexamples.json`, keys `recording_assessment_retarget` and `closure_assessment_retarget`; same observations in the optimized probe.

### R2-REV-03 | HIGH for reproducibility | The full manifest remains checkout-sensitive

**Locations:** `.gitattributes:1-7`; `qualification/m01_r2/qualify.py:44-59,92-99`; `evidence/stonewall-0/m01-r2/repair-manifest.json`.

The proposed attributes protect schema/corpus bytes, historical R1 bytes, and evidence files. They do not specify byte-preserving checkout for every other file bound by the new R2 manifest.

Disposable index-stage/checkout-index experiments used the complete captured candidate and its actual attributes. No source repository commit was made.

| Checkout setting | Full R2 bound-file digest mismatches | SW0-006 result |
|---|---:|---|
| `core.autocrlf=false` | 0 of 81 | 840, PASS |
| `core.autocrlf=true` | 19 of 81 | 840, PASS |

All 19 mismatches were newline transformations. Affected files include `.gitattributes` itself, the M01-R2 contract, sequence, governing Markdown, status reconciliation, and supplemental contracts.

The earlier report's narrower schema-corpus checkout claim is supported. It must not become a claim of full R2 manifest portability. Correct byte checks would reject the changed files; this is a reproducibility defect, not a demonstrated fail-open hash check.

**Repair:** Define checkout treatment for every digest-bound file, including the attributes file. Preserve historical raw/working-tree representations explicitly. Qualify the complete new candidate manifest under the required checkout settings. Do not regenerate frozen digests merely to accommodate unintended conversions. A revised attributes file and manifest require new candidate identities.

**Required regression:** Zero unexplained bound-file mismatches after checkout with conversion enabled and disabled, plus the retained 840-assertion corpus. Do not use a pass of that corpus alone as the oracle for the 81-file candidate.

Evidence: `results/checkout-counterexamples.json`; reproducer: `tools/probe_checkout.py`.

### R2-REV-04 | MEDIUM | One BoundaryReview can combine results for different mutable payload snapshots

**Locations:** `schemas/conformance/boundary_r2.py:137-142,182-210`.

`Registry.review()` validates the caller's mutable object, invokes external verifiers, and recomputes document bytes later from that same object. It does not take a stable snapshot and its returned BoundaryReview contains no subject digest.

Two re-entrant fixture probes show the gap:

1. A content verifier confirms the original document's exact digest, then an alias removes a required `source` member. The returned review still says `STRUCTURALLY_VALID` and content `SATISFIED`, while the now-referenced object fails its schema.
2. Content admission correctly matches snapshot A, the caller-owned object changes, and semantic admission correctly matches snapshot B. The returned review reports both admissions SATISFIED even though their subject digests differ.

No schema, verifier function, or result cache was monkey-patched. The deliberate alias mutation occurred during the verifier callback. This models a re-entrant/concurrent-input consistency boundary; it is not evidence that a remote caller controls trusted Python code. The model still returns `effective_authority=False`.

**Repair:** Construct and validate one independent snapshot; compute one identity for it; bind every verifier and the returned review to that identity and interpretation context. A mutation of the original caller object must not silently change what the review means. Prefer returning an immutable subject reference rather than leaving consumers to associate a verdict with any mutable dictionary.

**Required regression:** Mutation during/between callbacks must either be rejected or leave the result bound only to the original immutable snapshot. Mixed-snapshot approvals must never be combined into one subject review.

Evidence: `results/independent-counterexamples.json`, keys `mutable_review_during_verification` and `split_snapshot_review`; repeated identically under optimization.

### R2-REV-05 | MEDIUM | Secret-shape rejection is mislabeled as structural invalidity

**Locations:** `schemas/conformance/boundary_r2.py:111-128,187-195`; `tests/conformance/test_m01_r2.py:209-220`; contract `constitution/state-machines/M01-R2-CONTRACT.md:28,62,66`.

The R2 contract assigns secret-shape screening to artifact admission and separates it from structural admissibility. The implementation catches `reject_secret_shapes()` in the same block as structural/ACS failures, returning:

```
structural: STRUCTURALLY_INVALID
content_admission: NOT_CHECKED
```

For an Observation fixture containing a nested `private_key` member with the explicit dummy value `DUMMY_NOT_A_SECRET`, independent root-schema validation returned True and canonical encoding succeeded, but the review returned that structural rejection. This is appropriate conservative rejection of a recognized shape, but not an accurate account of which layer rejected it. No real secret was used and no universal secret-detection claim is made.

The supplied test currently expects the collapsed outcome, so its PASS does not catch this distinction.

**Repair:** Retain separately named structural/representation and content-admission outcomes. Recognized forbidden content should produce a bounded content rejection with a non-sensitive reason; absence of independent content admission remains unresolved where appropriate. Do not label an unevaluated admission `NOT_CHECKED` when its local screening rule caused the rejection.

**Required regression:** A structurally valid forbidden-content shape and a structurally invalid document must remain distinguishable, while neither becomes accepted for use. Preserve payload-free error reporting.

Evidence: `results/independent-counterexamples.json`, key `secret_shape_layer`.

### R2-REV-06 | MEDIUM | The rescan can select zero historical files after repository relocation

**Locations:** `qualification/m01_r2/rescan.py:16-24,39-44`; absolute original-source keys in `evidence/stonewall-0/m01-r2/preservation.json`.

Historical file verification is conditional on each original absolute path being relative to the current repository path. The code never requires that the expected historical coverage was actually selected.

Evaluating the exact selection rule using Windows path semantics gives:

```
C:\AnarchI-Brain       -> 49 selected historical checks
D:\AnarchI-Brain       ->  0 selected historical checks
C:\AnarchI-Brain-copy  ->  0 selected historical checks
```

**Scope qualification:** This is an executed path-selection counterexample and a source-level coverage defect. The full relocated Git/index-bound rescan CLI was not run here. Other preflight conditions could fail first. The claim is that this historical-check loop has no coverage floor and will skip all originals when the roots differ, not that every relocated command necessarily prints PASS.

**Repair:** Preserve the original absolute location as provenance, but verify current files by an independently validated repository-relative mapping. Require the expected identity set/count, not simply zero observed mismatches. A deliberate relocation should verify the same 49 files or report a specific inability to do so.

**Required regression:** Root changes must not reduce historical coverage to zero unnoticed. Include missing, duplicated, unmapped, and outside-root cases, and fail on incomplete expected coverage.

Evidence: `results/rescan-portability.json`; reproducer: `tools/check_rescan_portability.py`.

## 4. What R2 genuinely improves

The actual source and freshly passing tests support the following bounded improvements: shared C03/C04 entry checks feed one review; catalog removal invalidates exact-payload fixture admission; no verifier defaults to unresolved; the selected diagnostic route is enforced; findings remain lossless through diagnostic closure; caller-supplied topology arguments are removed from the active API; forged P08 summary fields are rejected; direct predecessor/evaluation collisions and epoch/version mismatches are checked; duplicate decoded JSON keys and recursive unsupported values are rejected; registry callers receive defensive copies; and required root members are tested by actual omission.

These changes should be retained. The new findings show that correlation, loaded-code identity, stable input identity and qualification coverage need further work around them. They do not justify reverting to the old isolated Boolean continuation or repeating the C1-C16 textual PASS sequence.

## 5. Proposed amendments and unfinished dependencies

The seven intentional tracked modifications are README, three frozen-status/authority documents, and three supplemental contracts. The authority matrix's complete table rows match the baseline exactly, including all twelve dimensions, eleven organs and unresolved cells. The three frozen-baseline copies remain byte-exact. That supports preservation of the table, not authority to amend any frozen normative wording.

Treat the status reconciliation as a candidate amendment with explicit before/after identities and adjudication. Its text correctly distinguishes declared freeze from unavailable original closure evidence, but its own assertion that it is editorial is not independent approval. An append-only status/adoption record or separately approved amendment can make that relationship unambiguous.

Resolution's proposed context/instance separation and Validation's lossless failed/unresolved reporting are explicit candidate changes. They are not silently treated as historical frozen behavior in this review.

The original open admission, semantic interpretation, durable-recording and atomic-effect dependencies remain open. A future authenticated resolver, recorder or executor must not be presumed to exist because the fixture interface now names it. Conversely, runtime implementation should not be smuggled into STONEWALL-0 merely to make a reference-stage report look complete. Track specification, reference qualification and runtime enforcement separately under their actual owning gates.

The supplied archive still labels the five previously discussed upstream ledger texts unavailable. The separate historical-recovery package from the earlier conversation was not installed or used to manufacture original execution evidence. A16 must be updated only through a separately reviewed additive evidence-index change.

## 6. Bounded repair order and exit conditions

First, bind executed code to the checked source bytes and establish a full-manifest byte policy. This protects the meaning and reproducibility of the subsequent qualification evidence.

Second, bind diagnostic/closure assessment admission to the exact target it records, and bind every representation review to one immutable payload snapshot. These repairs address concrete interface relationships without inventing a runtime authority resolver.

Third, separate content-screening outcomes from structural outcomes and replace absolute-path skip logic with complete relative-path historical verification.

Then run the existing normal/optimized R2 suites and retained schema corpus, plus the six review regressions and their negative controls. Preserve R2 and its receipts as history; give any new candidate and manifest new identities. A successful repair qualification must distinguish passed nominal tests, rejected counterexamples, deliberately unimplemented dependencies and remaining freeze obligations.

No new chronological C-step or canonical gate status is assigned by this review. **M01_FREEZE_READY remains False.**

## 7. Evidence and reproducibility

The companion evidence JSON contains archive/manifest/tree checks, environment, fresh suite results, counterexamples, and final byte-preservation observations. The review bundle contains all test output and the probe source. Each counterexample uses explicit dummy fixtures or disposable copied sources; none performs a protected operation or reads user credentials.

The probe tools accept `--repo` pointing to the extracted archive's `repo` directory. `probe_verified_loader.py` and `probe_checkout.py` create and remove disposable test copies. They are not commands to modify the working AnarchI repository. The full original Git-bound qualifier requires its original repository context and is intentionally not simulated as a successful local run.

The source may contain other defects not exposed by these tests. This is a concrete, bounded independent review, not a formal whole-system proof.
