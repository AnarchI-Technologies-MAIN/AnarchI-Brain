# AnarchI Foundational Brain / Mainframe

This repository is the independent deterministic continuity substrate for the AnarchI ecosystem.

Current gate:

STONEWALL-0 — AnarchI Constitutional Freeze

## Constitutional invariant

AnarchI exists and functions before cognition is attached.

## Current scope

Only constitutional semantics, authority boundaries, canonical serialization, hashing/signature profiles, Cortex contracts, Substrate-fin contracts, organ authority matrices, schemas, and conformance/invariant tests may be developed during STONEWALL-0.

## Forbidden during STONEWALL-0

- database implementation
- Prism implementation
- model integration
- AnarchI Engine wiring
- companion integration
- distributed appendages

The existing AnarchI Engine may be used only as an external execution/proof workshop. It is not part of this repository and does not own brain truth.

## Current unfrozen M01 qualification candidate

The active reference qualification candidate is R3, described in `constitution/state-machines/M01-R3-CONTRACT.md`. R2 and earlier evidence remain historical; their launchers are not qualification entrypoints for the R3 overlay.

From a committed checkout with Python 3.12, Git and `jsonschema==4.26.0` installed, run `python -I -B ci/qualify.py`. This qualifies committed HEAD, so commit candidate changes first. It preserves the historical manifest pin, restores the manifest-bound README and ignore preimages only in a disposable candidate, checks the full manifest after real Git checkouts with both `core.autocrlf=false` and `true`, and verifies and compiles the launcher's exact bytes before execution in normal and optimized Python. The current README and ignore file are publication overlays, not revised historical evidence. Directly executing the historical R3 launcher is not the supported invoking handoff.

Run `python -I -B -m unittest discover -s ci -p "test_*.py"` for the CI boundary regressions. These tests cover launcher tampering, checkout conversion, full-manifest rejection and preserved preimages. Qualification does not implement an authority resolver or execute protected effects. Missing admission dependencies remain fail-closed. The candidate and supplemental contracts remain unfrozen; SW0-010 is not advanced and `M01_FREEZE_READY=False`.

`evidence/stonewall-0/m01-r2/evidence-index.json` records available source identities and explicitly missing historical closure receipts. Declared frozen status does not replace independent proof.
