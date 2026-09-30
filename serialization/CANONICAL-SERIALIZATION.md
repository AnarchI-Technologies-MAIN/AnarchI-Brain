# Canonical Serialization Contract

Status: FROZEN - SW0-004

## 1. Purpose

This contract defines the deterministic serialization profile used to produce stable semantic bytes for governed material within the AnarchI Brain.

The initial profile is:

AnarchI Canonical Serialization profile 1

Profile identifier:

ACS-1

This contract is subordinate to:

- AnarchI Semantic Language v1, frozen by SW0-001
- Authority Dimensions, frozen by SW0-002
- Artifact and Receipt Taxonomy, frozen by SW0-003

ACS-1 defines representation.

ACS-1 does not define truth, authority, Evidence status, valid issuance, canonical membership, or constitutional meaning.

## 2. Constitutional Separation

Canonical serialization is not Canonicalization.

Within this contract, the phrase canonical bytes means only the unique byte representation produced by ACS-1 for a valid semantic value under an identified schema and schema version.

Canonical bytes do not imply Canonical Membership.

Canonical bytes do not imply truth.

Canonical bytes do not imply Evidence status.

Canonical bytes do not imply authorization.

Canonical bytes do not imply authority.

Canonical bytes do not imply valid issuance.

Canonical bytes do not imply successful execution.

Canonical bytes do not imply semantic validity outside the schema and contracts under which they were produced.

A byte sequence may be serialization-canonical while the artifact it represents remains noncanonical, quarantined, unresolved, invalidly issued, unauthorized, or otherwise ineligible for a consequential transition.

## 3. Representation Independence

Constitutional meaning does not derive from:

- a filesystem
- a database
- a database column type
- a programming language
- a serializer library
- a JSON library
- a runtime
- a model provider
- a transport
- Git
- line-ending policy
- operating-system locale
- machine architecture
- hash-map iteration order
- provider-specific metadata

A conforming ACS-1 implementation must produce the same canonical bytes for the same governed semantic value, schema identifier, schema version, and serialization profile regardless of implementation environment.

## 4. Serialization Profile Binding

Every complete ACS-1 document must be a top-level object.

Every complete ACS-1 document must contain the following reserved members:

- serialization_profile
- schema_id
- schema_version

serialization_profile must be the exact string:

ACS-1

schema_id must be a non-empty string.

schema_version must be a non-empty string.

These members are part of the canonical bytes.

A serializer must not infer a missing serialization profile.

A serializer must not infer a missing schema identifier.

A serializer must not infer a missing schema version.

A serializer must not silently substitute a current or preferred schema version for the version supplied by governed material.

The exact format and registry of schema identifiers belong to later schema contracts.

## 5. ACS-1 Semantic Data Model

ACS-1 directly supports exactly these semantic value classes:

- Null
- Boolean
- Integer
- String
- Array
- Object

No other native scalar class exists in ACS-1.

A schema requiring a value not natively represented by ACS-1 must define an explicit representation using the supported value classes.

Examples include:

- decimal values
- binary values
- timestamps
- durations
- identifiers with specialized structure
- geographic values
- domain-specific numeric quantities

The serializer must not invent or infer such representations.

## 6. Null

Null is encoded as the exact ASCII byte sequence:

null

Null and absence are distinct.

A present member whose value is Null must not be silently omitted.

An absent member must not be silently materialized as Null.

A serializer must not insert or remove Null values based on language-specific default behavior.

## 7. Boolean

Boolean true is encoded as:

true

Boolean false is encoded as:

false

No other spelling or numeric substitution is valid.

The following are not Boolean encodings:

- 0
- 1
- TRUE
- FALSE
- True
- False
- yes
- no

A serializer must not coerce another scalar type into Boolean.

## 8. Integer

ACS-1 Integer values are signed arbitrary-precision mathematical integers.

Their canonical encoding is base-10 ASCII.

Valid integer grammar is:

- 0
- a positive integer beginning with digits 1 through 9
- a negative integer beginning with a minus sign followed by digits 1 through 9

Leading zeros are forbidden.

A leading plus sign is forbidden.

Negative zero is forbidden.

Decimal points are forbidden.

Exponent notation is forbidden.

Examples of canonical integers include:

- 0
- 1
- 42
- -1
- -987654321

Examples of forbidden numeric encodings include:

- +1
- 01
- -0
- 1.0
- 1e3
- 1E3

An implementation must not route an ACS-1 Integer through a floating-point representation if doing so can alter its exact value.

An implementation that cannot preserve an Integer exactly must fail closed.

## 9. Floating-Point and Decimal Values

ACS-1 does not define a native floating-point scalar.

ACS-1 does not define a native decimal scalar.

The following tokens are forbidden as ACS-1 numeric values:

- NaN
- Infinity
- -Infinity
- +Infinity

Binary floating-point values must not be silently converted into ACS-1 Integers.

Decimal values must not be silently converted into binary floating-point values.

A schema that requires decimal or floating-point semantics must define an explicit deterministic representation using ACS-1 supported primitives.

That representation must define its own precision, scale, range, rounding, and exceptional-value semantics where applicable.

## 10. String Model

An ACS-1 String is an exact sequence of Unicode scalar values.

Strings must be encoded as UTF-8.

UTF-8 must be valid.

A UTF-8 byte-order mark is forbidden.

Unpaired UTF-16 surrogate code points are forbidden.

Invalid Unicode scalar sequences are forbidden.

ACS-1 performs no Unicode normalization.

ACS-1 performs no:

- NFC normalization
- NFD normalization
- NFKC normalization
- NFKD normalization
- case folding
- case conversion
- whitespace trimming
- newline normalization
- locale-sensitive transformation

Two visually similar strings represented by different Unicode scalar sequences remain distinct ACS-1 String values unless a governing schema explicitly performs a semantic normalization before serialization.

## 11. String Escaping

An ACS-1 String uses JSON-compatible quotation with deterministic escaping.

The quotation mark must be escaped as:

\"

The reverse solidus must be escaped as:

\\

The following control characters use these short escapes:

- U+0008 as \b
- U+0009 as \t
- U+000A as \n
- U+000C as \f
- U+000D as \r

All other code points from U+0000 through U+001F must be encoded using a six-character lowercase hexadecimal escape of the form:

\u00xx

The solidus character must not be escaped.

Printable ASCII characters other than quotation mark and reverse solidus must not be escaped.

Valid non-ASCII Unicode scalar values must be emitted directly as UTF-8 rather than converted to \u escapes.

A serializer must not choose among multiple equivalent escape representations.

ACS-1 therefore defines one string representation for one exact Unicode scalar sequence.

## 12. Newlines Inside Strings

A carriage return contained in a String is a semantic character.

A line feed contained in a String is a semantic character.

They must be represented using the required ACS-1 escapes.

A serializer must not convert:

- CR to LF
- LF to CRLF
- CRLF to LF
- platform-native line endings to another line ending

Git line-ending normalization and filesystem line-ending behavior do not define ACS-1 String semantics.

## 13. Object Model

An ACS-1 Object is a finite mapping from unique String keys to ACS-1 values.

Object keys must be Strings.

Duplicate decoded keys are forbidden.

Duplicate detection occurs after escape decoding.

For example, two input keys that decode to the same Unicode scalar sequence are duplicates even if their source escape spellings differ.

A parser or serializer must reject an Object containing duplicate keys.

An implementation must not silently keep:

- the first duplicate
- the last duplicate
- an arbitrary duplicate

Object-member ordering is not semantic.

ACS-1 imposes a deterministic encoding order.

## 14. Object Member Ordering

Object members are serialized in ascending lexicographic order of the UTF-8 byte sequence of each decoded key.

Ordering is applied to the decoded String value of the key.

Ordering is not applied to the escaped source spelling of a key.

No locale-sensitive comparison is permitted.

No case-insensitive comparison is permitted.

No Unicode normalization is performed before comparison.

If one key's UTF-8 byte sequence is an exact prefix of another, the shorter key sorts first.

The same Object must therefore serialize with the same member order on every conforming implementation.

## 15. Array Model

An ACS-1 Array is an ordered finite sequence of ACS-1 values.

Array order is semantic unless the governing schema explicitly declares different collection semantics.

A serializer must preserve Array order.

A serializer must not sort an Array merely to obtain deterministic output.

A serializer must not remove duplicate Array elements unless an applicable schema explicitly defines set semantics.

## 16. Unordered Collections

ACS-1 has no native Set type.

Where a governing schema defines a collection as unordered, that schema must define how the collection is represented using ACS-1 values.

The default constitutional rule for an explicitly unordered collection represented as an Array is:

1. serialize each element using the ACS-1 recursive value encoding;
2. sort elements lexicographically by those encoded element bytes;
3. emit the resulting ordered Array.

For set semantics, duplicate canonical element byte sequences are forbidden.

For multiset semantics, duplicates may be retained only when the governing schema explicitly permits them.

A serializer must not infer unordered semantics from application-language collection types.

## 17. Object and Array Punctuation

ACS-1 uses these structural bytes:

- left brace and right brace for Objects
- left bracket and right bracket for Arrays
- colon between Object key and value
- comma between members or elements

No whitespace is emitted around structural punctuation.

Trailing commas are forbidden.

Comments are forbidden.

## 18. Whitespace and Document Boundaries

No whitespace is permitted outside Strings in ACS-1 canonical bytes.

A complete ACS-1 document contains:

- no leading whitespace
- no trailing whitespace
- no indentation
- no line wrapping
- no trailing newline
- no byte-order mark

The final byte of an ACS-1 document is the final byte of the top-level Object encoding.

Platform line-ending policy must not modify ACS-1 canonical bytes.

## 19. Null Versus Absent Members

Null and absent remain distinct.

The serializer must encode the semantic Object it receives.

The serializer must not:

- add missing members
- remove present members
- replace absent members with Null
- replace Null with absence
- materialize implementation defaults
- omit values because a host language considers them empty
- omit zero
- omit false
- omit empty String
- omit empty Array
- omit empty Object

Any schema-defined default materialization must occur as an explicit semantic operation before ACS-1 serialization.

## 20. Unknown Extension Fields

Unknown compatible fields must remain representable when the governing schema permits extension preservation.

An unknown field must preserve:

- its exact decoded key
- its ACS-1 value class
- its complete nested semantic value
- its relationship to the containing Object

An unknown field must not be silently:

- dropped
- renamed
- retyped
- defaulted
- interpreted
- promoted into authority
- treated as a known field

Unknown fields are serialized using the same ACS-1 ordering and encoding rules as known fields.

If an implementation cannot preserve an unknown compatible field without semantic loss, it must fail closed.

Preserving an unknown field does not assign meaning to that field.

## 21. Schema Binding

Canonical serialization is schema-bound.

The schema_id and schema_version contained in the document identify the interpretation context required by the governing schema contracts.

Serialization does not itself prove that the claimed schema exists.

Serialization does not itself prove that the claimed schema is applicable.

Serialization does not itself prove that the document satisfies the claimed schema.

Schema qualification and applicability remain separate governed concerns.

A later schema version must not silently reinterpret historical bytes governed by an earlier schema version.

## 22. Special Semantic Types

ACS-1 does not intrinsically interpret a String as:

- a timestamp
- a date
- a duration
- a URL
- a UUID
- a hash
- a signature
- a decimal
- binary data
- an authority identifier
- an artifact identifier

Such interpretation belongs to the applicable schema.

A serializer must not inspect String contents and rewrite them according to guessed semantic type.

A timestamp-like String remains a String unless the governing schema explicitly defines timestamp semantics.

## 23. Parseability Versus Canonicality

Parseable input is not necessarily ACS-1 canonical input.

A byte sequence may describe a value that can be parsed while failing ACS-1 canonical representation requirements.

Examples include:

- additional whitespace
- alternate key order
- alternate String escapes
- a byte-order mark
- trailing newline
- noncanonical Integer spelling
- duplicate keys
- unsupported number syntax

A canonical-byte validator must reject any byte sequence that is not byte-for-byte identical to the ACS-1 serialization of the semantic value it claims to represent.

An ingress process may parse a permitted noncanonical external representation and later produce ACS-1 bytes, but that ingress operation is distinct from validating the original bytes as ACS-1 canonical.

Original provenance must not be erased by normalization.

## 24. Serialization Procedure

A conforming ACS-1 serializer performs the following logical procedure:

1. receive a governed semantic value;
2. resolve the serialization profile;
3. require an explicit schema identifier;
4. require an explicit schema version;
5. reject unsupported or ambiguous value classes;
6. reject invalid Unicode;
7. reject duplicate Object keys;
8. preserve Null versus absence;
9. preserve Array order unless explicit schema-defined unordered semantics apply;
10. order Object members according to ACS-1 key ordering;
11. encode every scalar according to ACS-1;
12. emit UTF-8 bytes with no byte-order mark and no surrounding whitespace;
13. emit no hidden or environment-derived fields.

The serializer must not consult ambient mutable state to determine output bytes.

## 25. Forbidden Ambient Inputs

ACS-1 output must not vary because of:

- current time
- current timezone
- current locale
- current language
- process identifier
- machine hostname
- random values
- memory address
- object insertion history
- hash-map iteration order
- filesystem path
- database row order
- provider metadata
- model metadata
- operating system
- CPU architecture
- Git configuration
- environment variables

If such information is semantically required, it must already exist as explicit governed input before serialization.

## 26. Hidden Fields

A serializer must not inject provider-specific hidden fields.

A serializer must not inject library-specific hidden fields.

A serializer must not inject framework metadata.

A serializer must not inject tracing metadata unless the governing schema explicitly includes that material as semantic content.

A serializer must not omit schema-defined material merely because a provider or library does not recognize it.

## 27. Deterministic Equality Property

For a fixed:

- ACS-1 profile
- schema identifier
- schema version
- semantic value

every conforming serializer must produce exactly the same canonical byte sequence.

A repeated serialization of the same semantic value under the same bindings must be byte-identical.

Serialization must be independent of execution order and implementation language.

## 28. Non-Collision of Distinct Semantic Values

Within ACS-1, two distinct supported typed semantic values must not intentionally serialize to the same canonical byte sequence.

Type distinctions must remain visible in representation.

For example:

- String "1" is distinct from Integer 1
- String "true" is distinct from Boolean true
- Null is distinct from absent
- empty String is distinct from Null
- empty Array is distinct from empty Object

If a schema defines semantic equivalence beyond ACS-1's typed value model, that equivalence belongs to the schema and must occur before serialization.

## 29. Serialization-Canonical Bytes and Canonical Membership

Serialization-canonical bytes are representation.

Canonical Membership is governed state.

Producing ACS-1 canonical bytes does not perform Canonicalization.

Hashing ACS-1 canonical bytes does not perform Canonicalization.

Signing ACS-1 canonical bytes does not perform Canonicalization.

Storing ACS-1 canonical bytes does not perform Canonicalization.

Replicating ACS-1 canonical bytes does not perform Canonicalization.

Reconstructing identical ACS-1 canonical bytes does not perform Canonicalization.

Canonical Membership requires the applicable canonical authority path and state-machine transition.

## 30. Semantic Hash Boundary

ACS-1 defines the deterministic semantic byte sequence suitable for use as hash input.

SW0-004 does not select the cryptographic hash algorithm.

Hash-algorithm selection, domain separation, digest representation, and signature profiles belong to SW0-005.

A semantic hash must ultimately bind the exact serialization profile and schema interpretation required by its applicable hashing profile.

Hash equality proves only equality of the hashed byte input under the applicable hash profile.

Hash equality does not prove:

- truth
- Evidence status
- authority
- authorization
- valid issuance
- Canonical Membership
- legal transition
- independent corroboration

## 31. Signature Boundary

ACS-1 does not define digital signature algorithms.

SW0-005 defines signature profiles.

A valid cryptographic signature over ACS-1 bytes may establish that a defined signing operation verified under the applicable cryptographic profile.

Signature validity does not independently establish:

- authority
- truth
- Evidence status
- valid issuance
- Canonical Membership
- permission
- legal applicability

The constitutional authority of a signer remains governed by SW0-002 and applicable authority contracts.

## 32. Historical Stability

ACS-1 meaning is immutable once frozen.

A future serialization profile must not silently alter ACS-1 rules.

Any change that would alter the canonical bytes of a valid ACS-1 semantic value requires a new serialization profile identifier.

Historical ACS-1 material must continue to be interpreted and verified under ACS-1.

A newer serialization profile may coexist with ACS-1.

A newer profile must not silently reinterpret historical ACS-1 bytes.

Migration between serialization profiles is a governed Migration operation.

Migration does not rewrite the historical meaning of the original material.

## 33. Working-Tree and Transport Transformations

Working-tree transformations are not ACS-1 transformations.

The following do not define ACS-1 semantics:

- Git autocrlf
- .gitattributes
- filesystem newline translation
- text-editor newline conversion
- archive format
- transport framing
- HTTP content encoding
- database text encoding

An ACS-1 implementation must operate on the semantic value and canonical byte profile, not on assumptions derived from a working-tree representation.

If an ACS-1 byte sequence is transported through a medium that mutates its bytes, the transported representation is no longer byte-identical ACS-1 canonical content until the original bytes are deterministically recovered.

## 34. Failure Behavior

ACS-1 fails closed.

Canonical bytes must not be emitted when required interpretation cannot be deterministically resolved.

Failure conditions include:

- missing serialization_profile
- unknown serialization profile
- missing schema_id
- missing schema_version
- invalid UTF-8
- invalid Unicode scalar sequence
- unpaired surrogate
- duplicate Object key
- unsupported scalar type
- native floating-point value
- native decimal value without schema-defined representation
- non-exact Integer handling
- ambiguous unordered-collection semantics
- inability to preserve an unknown compatible field
- hidden field injection
- environment-dependent output
- non-deterministic ordering

A serialization failure does not authorize fallback to a weaker encoding.

## 35. Canonical Byte Validation

A conforming ACS-1 canonical-byte validator must:

1. decode valid UTF-8 without a byte-order mark;
2. parse without duplicate-key collapse;
3. preserve exact supported scalar types;
4. resolve the claimed serialization profile;
5. resolve the claimed schema binding as required by the validation contract;
6. reserialize according to ACS-1;
7. compare the resulting bytes to the supplied bytes.

Canonical-byte validation passes only when the bytes are identical.

Semantic or schema validation remains a separate concern unless the governing validation contract explicitly composes those checks.

## 36. Constitutional Serialization Laws

The following laws are mandatory:

- canonical serialization != Canonicalization
- canonical bytes != Canonical Membership
- canonical bytes != truth
- canonical bytes != Evidence
- canonical bytes != Authorization
- canonical bytes != authority
- canonical bytes != valid issuance
- parseable != canonical
- canonical != schema-valid
- schema-valid != authorized
- hash equality != truth
- signature validity != authority
- storage representation != constitutional meaning
- database representation != constitutional meaning
- working-tree representation != canonical semantic bytes
- Null != absent
- String "1" != Integer 1
- String "true" != Boolean true
- array order is preserved unless schema explicitly defines unordered semantics
- object member order is deterministic and non-semantic
- duplicate Object keys are invalid
- Unicode normalization is not implicit
- newline normalization is not implicit
- floating-point representation is not implicit
- unknown compatible fields must survive where extension preservation is required
- unknown fields do not gain meaning through preservation
- serialization must not inject hidden provider fields
- environment state must not influence canonical bytes
- historical serialization meaning is immutable
- serialization profile changes require explicit version identity
- migration between serialization profiles does not rewrite historical meaning
- cognition does not gain authority by producing canonical bytes

## 37. Relationship to Later Contracts

SW0-004 defines deterministic representation.

It does not define:

- hash algorithms
- signature algorithms
- key management
- schema registries
- schema applicability
- artifact lifecycle
- authority lifecycle
- canonicalization lifecycle
- database implementation
- journal implementation
- canonical-memory implementation

SW0-005 will define hashing and signature profiles.

Later schema work will define concrete governed document structures.

Later state-machine contracts will define the consequential transitions that consume or emit governed material.

Those contracts must not silently redefine ACS-1 historical representation rules.

## 38. SW0-004 Closure Conditions

SW0-004 may close only when machine-checkable evidence demonstrates that:

1. ACS-1 has one explicit profile identifier.
2. every complete document explicitly binds serialization profile, schema identifier, and schema version.
3. the supported semantic value classes are explicitly bounded.
4. Null and absence remain distinct.
5. Boolean encoding is unique.
6. Integer encoding is unique and arbitrary-precision.
7. native floating-point and decimal ambiguity are excluded.
8. UTF-8 and Unicode behavior are explicit.
9. Unicode normalization is not implicit.
10. String escaping is deterministic.
11. newline transformation is not implicit.
12. duplicate Object keys are rejected.
13. Object member ordering is deterministic.
14. Array order remains semantic unless a schema explicitly defines unordered semantics.
15. unordered collection ordering is deterministic when permitted by schema.
16. no whitespace, byte-order mark, or trailing newline appears outside String content.
17. unknown compatible fields remain preservable without acquiring invented meaning.
18. parseability is separated from canonical-byte validity.
19. serialization is independent of ambient runtime and provider state.
20. serialization-canonical bytes are separated from Canonical Membership.
21. hash equality is separated from truth and authority.
22. signature validity is separated from constitutional authority.
23. historical ACS-1 interpretation is immutable.
24. profile changes require explicit new profile identity.
25. failure behavior is fail-closed.
26. this contract remains subordinate to SW0-001, SW0-002, and SW0-003.

These closure conditions have been proven for SW0-004. The ACS-1 canonical serialization contract is frozen.