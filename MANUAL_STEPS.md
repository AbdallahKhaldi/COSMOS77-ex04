# MANUAL_STEPS — capturing the Obsidian Graph View screenshot

Four of the five README images are **generated** by the pipeline
(`artifacts/block_diagram.png`, `artifacts/oop_schema.png`,
`artifacts/knowledge_graph.png`, `artifacts/token_comparison.png`).

The fifth — `artifacts/obsidian_graph_view.png` — is a **manual screenshot** the authors add via
**Obsidian Desktop**, because it visualises the live vault as a navigable knowledge space (something
only the Obsidian app renders). It is included to *show* the `index.md` navigation hub and its
resolved `[[wikilinks]]`; it is not produced by `cosmos77-rev`.

## How to reproduce the screenshot

1. Run the pipeline so the vault exists:
   ```bash
   uv run cosmos77-rev run
   ```
   This writes `obsidian/` (`index.md`, `hot.md`, `suspects.md`, `investigation.md`,
   `fix-process.md`, and `pages/`).
2. Install **Obsidian Desktop** (free): https://obsidian.md
3. **Open folder as vault** → select the repository's `obsidian/` directory.
4. Open **Graph View** (left ribbon graph icon, or `Ctrl/Cmd+G`).
5. Optional: in Graph View settings, raise link force / node size so the `tqdm` God Node hub and the
   community pages are clearly separated and the navigation structure is legible.
6. Take a screenshot of the Graph View and save it as:
   ```
   artifacts/obsidian_graph_view.png
   ```

Once saved, the README image embed `![Obsidian graph view of the vault](artifacts/obsidian_graph_view.png)`
resolves and renders the vault map.
