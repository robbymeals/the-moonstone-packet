# The Moonstone Packet

Extracting the narrative structure of Wilkie Collins' *The Moonstone* (1868) into graphs and documents.

Collins wrote the novel as multiple witnesses testifying about the same events. We're pulling that structure apart to see what's load-bearing.

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

**Documents** (in root, also viewable in the app):
- `ACTIONS.md` — timeline of events
- `CHARACTERS.md` — character inventory
- `PERSPECTIVES.md` — narrator analysis
- `TONE.md` — voice fingerprints

**Stats**: word counts, character co-occurrence, n-grams, the usual.

## License

Anti-Capitalist Software License. Excludes law enforcement, military, and ICE.
