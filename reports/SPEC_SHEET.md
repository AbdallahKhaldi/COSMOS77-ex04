# Token Spec Sheet

Measured per-run metrics from the Gatekeeper ledger (`usage_metadata`), both arms on the SAME buggy code and SAME LLM — honest measurement, no estimates.

| Run | LLM calls | Input | Output | Total | Files read | Iterations |
| --- | --- | --- | --- | --- | --- | --- |
| Naive baseline (raw files) | 1 | 65224 | 3112 | 68336 | 31 | 1 |
| Graph-guided agent | 1 | 38123 | 2703 | 40826 | 2 | 1 |
