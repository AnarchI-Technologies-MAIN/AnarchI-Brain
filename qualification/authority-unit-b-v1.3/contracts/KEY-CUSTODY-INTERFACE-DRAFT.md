# Key identity and custody interface draft

PROPOSED / NOT ADOPTED / NO LIVE KEYS OR SIGNATURE VERIFICATION.

A fixture key identifier or fingerprint binds only an expected reference coordinate. It is not a private key, authenticated signer, proof of possession, authorization or canonical authority. Principal-to-key association must be separately identified rather than inferred from matching labels. Unknown, mismatched, expired, revoked or conflicting fixture associations cannot satisfy the relevant finding.

Explicit key-binding records include stable principal ID, key ID/fingerprint, generation, activation, predecessor and admitting issuer/verifier. The current observation identifies expected principal and key generations independently of submitted records. Old binding replay, unknown generation, rollback or a conflicting predecessor does not become current merely because a fingerprint matches.

Unit B reads no private keys, accesses no server, signs nothing, enrolls nothing and provides no secret custody implementation. Private keys, tokens and signing secrets must never be embedded in proposals, grants, receipts or fixture packages. The eventual operational interface must resolve actual enrollment evidence, allowed algorithm/profile, key fingerprint, accountable custody, signing jurisdiction, rotation/revocation and recovery without exposing secret material to artifact payloads.

Cryptographic correctness would prove a signature under a key, not the key's constitutional authority or current scope. Fixture-key equality similarly proves only reference equality. Signing, live key enrollment, rotation and root replacement remain excluded and held.
