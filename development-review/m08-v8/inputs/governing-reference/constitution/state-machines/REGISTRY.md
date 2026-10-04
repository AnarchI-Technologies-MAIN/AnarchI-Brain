# Core State Machine Registry

Status: OPEN

STONEWALL-0 cannot close until every consequential state machine is formally enumerated.

Required initial registry:

1. Cortex ingress lifecycle
2. S0 validation lifecycle
3. Cartologist qualification lifecycle
4. S1 evidence qualification lifecycle
5. Wavesmith relationship/proposal lifecycle
6. S2 canonicalization lifecycle
7. canonical / noncanonical / quarantine memory lifecycle
8. Librarian processing lifecycle
9. S3 transition lifecycle
10. Prism projection lifecycle
11. S4 egress lifecycle
12. authority grant lifecycle
13. capability lifecycle
14. receipt lifecycle
15. schema/policy-root lifecycle
16. migration lifecycle
17. reconstruction lifecycle
18. integrity epoch lifecycle
19. revocation lifecycle

Each state machine must eventually define:

- states
- legal transitions
- illegal transitions
- proposer
- authorizer
- required evidence
- emitted receipt
- replay behavior
- failure behavior
- idempotency semantics