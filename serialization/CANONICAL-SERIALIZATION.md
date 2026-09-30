# Canonical Serialization Contract

Status: OPEN

STONEWALL-0 must define a deterministic serialization profile before any journal or canonical-memory implementation exists.

Required properties:

- deterministic field ordering
- deterministic scalar encoding
- deterministic collection ordering where semantics permit
- explicit version binding
- explicit schema identifier
- extension preservation
- rejection of ambiguous encodings
- byte-stable semantic hashing
- no provider-specific hidden fields
- historical interpretation remains stable

No implementation-specific database representation may define canonical semantics.