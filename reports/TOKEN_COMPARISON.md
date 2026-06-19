# Token Comparison — Naive Raw-Files vs Graph-Guided (C8)

All numbers are MEASURED from `usage_metadata` via the Gatekeeper ledger, for both arms on the SAME buggy code and SAME LLM.

| Metric | Baseline | Guided | Delta | % |
| --- | --- | --- | --- | --- |
| Total tokens | 68336 | 40826 | -27510 | 40.3% |
| Input tokens | 65224 | 38123 | -27101 | 41.6% |
| Output tokens | 3112 | 2703 | -409 | 13.1% |
| Files read | 31 | 2 | -29 | 93.5% |

## Honest verdict

Guided retrieval cut total tokens by 40.26% (27510 fewer). By consulting `index.md` as the navigation hub and reading only the top suspect files, the agent kept a high signal-to-noise context and avoided the Lost in the Middle and Context Rot failure modes of the raw-file baseline.

See the chart `artifacts/token_comparison.pdf` for the grouped bars.
