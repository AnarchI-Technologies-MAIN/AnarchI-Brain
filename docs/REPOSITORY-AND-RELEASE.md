# Repository structure and release boundaries

- `constitution/`, `contracts/`, `schemas/`, `semantic-language/`, `serialization/`, `hashing/`, `validation/`, `qualification/`, `resolution/`: governed reference contracts and qualification implementation. Existing freeze headers require their actual adoption evidence; headers alone do not establish authority.
- `tests/`: executable conformance and adversarial reference tests.
- `evidence/`: historical, versioned evidence with its original identities and scope.
- `development-review/`: explicitly UNADOPTED machine drafts, authority decision packet and proposed adversarial cases. These are not executable runtime services or issued authority.
- `ci/` and `.github/`: publication qualification, review ownership and automation. The preserved historical ignore preimage is solely for disposable byte-faithful qualification.

## Branches

`main` is the reviewed baseline; `development` is the integration candidate. Both require pull requests, current passing Linux/Windows checks, one approving review, code-owner review, dismissal of stale approvals and resolved conversations. Force pushes and branch deletion are prohibited, including for administrators. Git HEAD is a commit pointer, and origin is a remote alias; neither is a separately protectable server branch.

## Deployment

There is no automatic deployment or production secret in this repository. Passing CI is reference qualification, not production authority. A future staging workflow must identify the exact approved commit, target and rollback, isolate Mainframe from existing Stewardence services, use narrowly scoped staging credentials and retain attack/restore evidence. Production requires separate human approval, governing closure and deployment qualification. A staging success cannot close those gates automatically.

Corpus databases and archives use governed external intake; they are excluded from Git. Secrets and machine-local configuration must never be committed. Historical receipts remain historical even when their files are published here.
