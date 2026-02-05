# The Moonstone Packet

Extracting the narrative structure of Wilkie Collins' *The Moonstone* (1868) into graphs and documents.

Collins wrote the novel as multiple witnesses testifying about the same events. We're pulling that structure apart to see what's load-bearing. And seeing what else that structure can be used to plausibly grow, in terms of interesting alternate narratives in this specific set of circumstances. Or boring alternatives. We're trying to understand the alternatives. For fun.

## Quickstart

```bash
poetry install
cd viewer
poetry run python app.py
```

Open http://localhost:5050

## What's Here

**Graphs** (in `graphs/`, viewable in the app):
- Causal chain — what caused what
- Knowledge state — who knows what
- Knowledge asymmetry — who knows things others don't
- Counterfactual DAG — where the story could have gone differently
- Locations — spatial relationships
- Event-perspective matrix — which narrators cover which events

**Hinges** — pivotal moments where the story could have diverged. Browse hinges, add alternative outcomes, note immediate effects and plausibility.

**Stats**: word counts, character co-occurrence, n-grams, the usual.

## Documents

### Foundation

The core extraction — what the packet is built from.

- [ACTIONS.md](ACTIONS.md) — Perspective-neutral timeline of events. What actually happened, when, where. The mechanical backbone.
- [CHARACTERS.md](CHARACTERS.md) — Character inventory. Who exists, what they know and when, what they want, what they hide.
- [PERSPECTIVES.md](PERSPECTIVES.md) — Narrator analysis. How each narrator filters reality, what they perceive, what they miss, what they misinterpret.
- [TONE.md](TONE.md) — Tonal registers and voice fingerprints. Vocabulary markers, rhythm patterns, emotional coloring for each narrator.

### Meta

Documentation about the process.

- [PLAN.md](PLAN.md) — The extraction methodology. Why CHARACTERS and PERSPECTIVES are distinct primitives, order of operations, dependency graph.
- [EXTRACTION_TECHNIQUES.md](EXTRACTION_TECHNIQUES.md) — Load-bearing narrative structures we're extracting. Knowledge state graphs, causal chains, perspective matrices, etc.
- [VIEWER_PLAN.md](VIEWER_PLAN.md) — Plan for the graph viewer application.
- [LOG.md](LOG.md) — Session-by-session work record. What was requested, what was delivered, reasoning behind decisions.
- [CHECKLIST.md](CHECKLIST.md) — Progress tracker for extraction phases.
- [COUNTERFACTUALS_PLAN.md](COUNTERFACTUALS_PLAN.md) — Plan for the alternate outcomes system.
- [CLAUDE.md](CLAUDE.md) — Instructions for Claude Code when working on this project.

## License

Anti-Capitalist Software License. Excludes law enforcement, military, and ICE.
