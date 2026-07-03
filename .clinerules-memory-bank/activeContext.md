# Active Context

## Current State (2026-07-03)
Project has **expanded from 8 to 16 frameworks** — 8 original analytical frameworks plus 8 new business/strategy frameworks. All 41 tests pass.

## Recent Changes
- **Added 8 new business/strategy frameworks:**
  1. Jobs-to-be-Done (JTBD) — 5 steps (Christensen, Ulwick, Moesta)
  2. Value Proposition Canvas — 5 steps (Osterwalder)
  3. Beachhead Market Strategy — 4 steps (Aulet)
  4. Technology Adoption Life Cycle — 4 steps (Moore)
  5. Blue Ocean Strategy — 5 steps (Kim & Mauborgne)
  6. Ideal Customer Profile — 4 steps (Ross)
  7. STP (Segmentation, Targeting, Positioning) — 4 steps (Kotler, Ries, Trout)
  8. Three Horizons of Growth — 5 steps (McKinsey)
- Updated `src/frameworks/__init__.py` — all 8 imports and exports
- Updated `src/framework_selector.py` — registry grew from 8→16, classification prompt expanded
- Updated `tests/test_frameworks.py` — 41 tests (was 25), all parametrized via `ALL_FRAMEWORKS`
- Updated `README.md` — framework table has 16 rows, project structure updated
- All 41 tests passing in 0.59s

## Immediate Next Steps
### General Next Steps
- [ ] Create `.env` from `.env.example` with sumopod API credentials
- [ ] Run end-to-end test with a real question via CLI or Streamlit
- [ ] Deploy to VPS using Docker
- [ ] Commit and push to GitHub

## Active Decisions
- **LLM Provider**: Sumopod (OpenAI-compatible API)
- **UI**: Streamlit (for web + VPS deployment)
- **Framework Selection**: Auto-detect with manual override — LLM now chooses from 16 frameworks
- **Default Framework**: Fishbone Diagram (unchanged)
- **API Key**: Via `.env` file
- **Architecture Pattern**: All 16 frameworks follow the same `BaseFramework` template method pattern — no special cases

## Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-30 | Use `openai` Python SDK | Sumopod is OpenAI-compatible |
| 2026-06-30 | Streamlit for web UI | Lightweight, Python-native, VPS-friendly |
| 2026-06-30 | `click` + `rich` for CLI | Rich terminal output, easy argument parsing |
| 2026-06-30 | Fishbone as default fallback | Most versatile for general root cause questions |
| 2026-06-30 | Auto-detect via LLM | User wants hands-off framework selection |
| 2026-07-01 | Fixed `Orchestrator(llm=)` → `Orchestrator(llm_adapter=)` | Constructor parameter name mismatch in `app.py` |
| 2026-07-03 | Added 8 business/strategy frameworks | User requested expansion from analytical-only to include marketing, strategy, and growth frameworks |
| 2026-07-03 | Kept `_` separator in framework keys | Consistent with existing convention (e.g., `fault_tree`, `apollo_rca`) |
| 2026-07-03 | Tests parametrized via `ALL_FRAMEWORKS` list | Adding new frameworks automatically generates tests — no per-framework test functions needed |