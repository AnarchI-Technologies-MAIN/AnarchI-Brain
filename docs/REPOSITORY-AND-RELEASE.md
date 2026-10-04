# Repository structure and release boundaries

- `constitution/`, `contracts/`, `schemas/`, `semantic-language/`, `serialization/`, `hashing/`, `validation/`, `qualification/`, `resolution/`: governed reference contracts and qualification implementation. Existing freeze headers require their actual adoption evidence; headers alone do not establish authority.
- `tests/`: executable conformance and adversarial reference tests.
- `evidence/`: historical, versioned evidence with its original identities and scope.
- `development-review/`: explicitly UNADOPTED machine drafts, authority decision packet and proposed adversarial cases. These are not executable runtime services or issued authority.
- `ci/` and `.github/`: publication qualification, review ownership and automation. The preserved historical README and ignore preimages are solely for disposable byte-faithful qualification.

## Branches

`main` is the reviewed baseline; `development` is the integration candidate. As inspected on 2026-10-04, both require pull requests, current passing Linux/Windows qualification checks, linear history and resolved conversations, including for administrators. Approving-review count is zero; code-owner review, last-push approval and required commit signatures are disabled. Stale-review dismissal remains enabled. Force pushes and branch deletion are prohibited. This supports a solo maintainer without requiring another human's approval. GitHub settings are the operational source of truth; this document does not configure them. Git HEAD is a commit pointer, and origin is a remote alias; neither is a separately protectable server branch.

## Push qualification and Kiln boundary

The Brain qualification workflow tests branch pushes and pull requests targeting `main` or `development`, with Ubuntu 24.04 and Windows 2025 jobs. Each job checks the CI boundary in normal and optimized Python, then qualifies the preserved R3 candidate after both Git autocrlf checkout modes. Ref-scoped concurrency cancels superseded runs; permissions remain `contents: read`, checkout credentials are not persisted, and jobs have a 15-minute limit. Official checkout/setup-python actions are SHA-pinned to v7 releases. The required qualification check names remain `qualify (ubuntu-latest)` and `qualify (windows-latest)` for compatibility with existing protections; the runner generations are fixed independently of those names.

Kiln's own repository has `Kiln Push Turn`, which runs native tests and then calls its pinned reusable proof workflow for bounded destructive self-specimen trials and evidence capture. That trigger does not subscribe to Brain pushes. Brain is public and Kiln is private as inspected on 2026-10-04; Kiln's `docs/KILN-ORG-WIDE-REUSABLE-WORKFLOW-001.md` explicitly requires a distribution decision before public callers can use its private workflow. Brain therefore has no automated Kiln call. A separately approved public, pinned runtime/workflow distribution or a narrowly scoped private-side intake would be needed; neither is configured here. Local worker campaigns are separate from GitHub push integration. Qualification and Kiln survivors cannot authorize promotion or deployment.

## Deployment

There is no automatic deployment or production secret in this repository. Passing CI is reference qualification, not production authority. A future staging workflow must identify the exact approved commit, target and rollback, isolate Mainframe from existing Stewardence services, use narrowly scoped staging credentials and retain attack/restore evidence. Production requires separate human approval, governing closure and deployment qualification. A staging success cannot close those gates automatically.

Corpus databases and archives use governed external intake; they are excluded from Git. Secrets and machine-local configuration must never be committed. Historical receipts remain historical even when their files are published here.
