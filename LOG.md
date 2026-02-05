# Project Log

This file tracks what was requested, what was delivered, and the reasoning behind decisions.

---

## 2026-02-04 — Session 1: Project Initialization

### Requested
1. Create a `CLAUDE.md` file for future Claude Code instances
2. Create a log file to track work across sessions

### Context Provided
User shared the complete Aristoi Institute project plan for the narrative packet format proof of concept using *The Moonstone*.

### Delivered

**CLAUDE.md** — Guidance file for future Claude Code instances containing:
- Project overview (what a narrative packet is, why *The Moonstone*)
- Source material location (`src/pg155.txt`)
- Three-layer packet architecture with word count targets
- Character models to extract (7 key characters)
- Causal chain mapping requirement
- Seams/handles notation need
- Playtesting protocols

**LOG.md** — This file.

### Decisions & Reasoning
- Focused CLAUDE.md on actionable technical architecture rather than project management (phases, timelines, success criteria) since those are for the human, not the AI
- Kept extraction targets specific (Verinder house geography, Shivering Sand tides, birthday dinner timeline, paint on door) rather than abstract
- Included the experimental Moonstone-as-narrator perspective since it tests format limits
- Omitted philosophical framing about compression/decompression — the architecture implies the philosophy

### Current State
- Phase 0: Source text acquired, project plan established, tooling initialized
- Next likely work: Phase 1 extraction (world state, character models, causal chains)

---

## 2026-02-04 — Session 2: ACTIONS Timeline Extraction

### Requested
Extract a perspective-neutral, mechanical ACTIONS timeline from *The Moonstone* source text. Structure in six sections:
1. Prologue Events (1799)
2. Birthday Dinner Night (June 21, 1848) — hour-by-hour
3. Post-Theft Investigation (June–July 1848)
4. London Events (1848–1849)
5. Opium Experiment (June 1849)
6. Resolution

### Delivered

**ACTIONS.md** — Complete perspective-neutral timeline (~2,500 words) containing:
- Prologue: Siege of Seringapatam, Herncastle's murder of three priests, diamond theft, 50-year gap
- Birthday night: Hour-by-hour reconstruction including the hidden truth (Dr. Candy's laudanum dose, Franklin's unconscious taking of diamond, Godfrey's opportunistic theft)
- Investigation: Sergeant Cuff's arrival, paint smear discovery, Rosanna's suicide, Godfrey's London trip to Luker
- London events: Godfrey's pledge, Indian attacks, Lady Verinder's death, Rachel's broken engagement
- Opium experiment: Ezra Jennings's discovery from Candy's fever-ramblings, the recreation, proof of Franklin's innocence
- Resolution: Godfrey's death at "The Wheel of Fortune," Indians recover diamond
- Epilogue: Diamond returned to Somnauth idol (1850)
- Causal chain summary: 12-step causation sequence

### Decisions & Reasoning
- Marked uncertain timings with [time uncertain] where the novel leaves gaps
- Included the causal chain summary at the end as a backbone reference for perspective shifts
- Kept Godfrey's theft mechanism slightly ambiguous (matching source — exact moment of observation/theft unclear)
- Documented that Rachel witnessed Franklin but chose silence — this is key hidden logic
- Structured for use as Layer 1 foundation: perspective-neutral facts that downstream perspective layers can interpret differently

### Current State
- ACTIONS.md complete — the factual backbone for the narrative packet
- Next likely work: Layer 2 perspective entry points (Betteredge, Cuff, Rosanna, Rachel, Moonstone) or Layer 1 world state (geography, physical descriptions)

---

## 2026-02-04 — Session 3: CHARACTERS Inventory Extraction

### Requested
Extract a comprehensive CHARACTERS inventory from the source text with:
- **Major characters (full treatment)**: Gabriel Betteredge, Franklin Blake, Rachel Verinder, Rosanna Spearman, Sergeant Cuff, Godfrey Ablewhite, Ezra Jennings, Miss Clack, Matthew Bruff
- **Minor characters (brief treatment)**: Penelope Betteredge, Lady Julia Verinder, Mr. Murthwaite, Mr. Luker, The Three Indians, Limping Lucy Yolland, Dr. Candy, Colonel John Herncastle
- For each character: Role/Position, What They Know and When, What They Want, What They Hide, Key Actions
- Special attention to: Rosanna's knowledge about Franklin, Rachel's observations on theft night, Godfrey's true activities, Dr. Candy's illness mystery

### Delivered

**CHARACTERS.md** — Comprehensive character reference (~3,200 words) containing:

**9 Major Characters (full treatment)**:
- Gabriel Betteredge: Steward, narrator of First Period, warm/digressive perspective, believes in Franklin's innocence throughout
- Franklin Blake: The unwitting thief, drugged with laudanum, no memory of taking the Diamond, later vindicated
- Rachel Verinder: Witnessed Franklin take the Diamond, protected him through silence, eventually marries him
- Rosanna Spearman: Former thief, fell in love with Franklin, hid his paint-stained nightgown, committed suicide at Shivering Sand
- Sergeant Cuff: Detective investigator, correctly identified Rosanna's involvement but misread its nature, delivers final report
- Godfrey Ablewhite: Secret embezzler, saw opportunity and took Diamond from drugged Franklin, pledged to Luker, murdered by Indians
- Ezra Jennings: Dr. Candy's assistant, dying, reconstructed the laudanum revelation from Candy's fever-speech, designed the proof experiment
- Miss Clack: Evangelical narrator, comic/satirical perspective, unwittingly documents Godfrey's false virtue
- Matthew Bruff: Family lawyer, investigates Godfrey's trust fraud, voice of legal propriety

**8 Minor Characters (brief treatment)**:
- Penelope Betteredge, Lady Julia Verinder, Mr. Murthwaite, Mr. Luker, The Three Indians (Brahmins), Limping Lucy Yolland, Dr. Candy, Colonel John Herncastle

**Additional reference materials**:
- Character Knowledge Timeline table (who knows what, when)
- Character Relationships Map (love/devotion, service/loyalty, antagonism, deception)

### Decisions & Reasoning
- Structured "What They Know and When" to track knowledge progression across the novel's timeline — essential for perspective accuracy
- Separated "What They Hide" to support Layer 3 (Hidden Narrative Logic) development
- Included the knowledge timeline table as quick reference for scene-level accuracy
- Documented the key hidden truths: Rosanna's love, Rachel's witness, Godfrey's theft, Dr. Candy's prank
- Added relationship map to support character interaction modeling
- Kept minor character entries brief but complete enough for accurate scene generation

### Current State
- CHARACTERS.md complete — character reference for the narrative packet
- ACTIONS.md complete — timeline backbone
- Next likely work: Layer 1 world state (geography, Verinder house layout, Shivering Sand description) or Layer 2 perspective entry points

---

## 2026-02-04 — Session 4: Foundation Files Complete

### Requested
Implement the full plan for Moonstone Packet Foundation Files:
- Create CHECKLIST.md progress tracker
- Create ACTIONS.md (perspective-neutral events)
- Create CHARACTERS.md (character inventory)
- Create PERSPECTIVES.md (narrative voice analysis)
- Create TONE.md (tonal register inventory)
- Save full plan to PLAN.md

### Delivered

**PLAN.md** — Full plan document including:
- Hypothesis on CHARACTERS vs PERSPECTIVES distinction
- Deterministic analysis (statistics, structure, character frequencies, motifs)
- Order of operations with dependency graph
- Execution plan with parallelization notes

**CHECKLIST.md** — Progress tracker for all phases

**ACTIONS.md** — Complete (from previous session, verified)

**CHARACTERS.md** — Complete (from previous session, verified)

**PERSPECTIVES.md** — New file (~2,800 words) containing:
- Multi-narrator architecture analysis
- 8 narrator analyses: Prologue cousin, Betteredge, Miss Clack, Bruff, Franklin Blake, Ezra Jennings, Sergeant Cuff, Epilogue voices
- Each narrator: text coverage, what they perceive, what they miss, misinterpretations, character relationships, narrative function, tonal markers
- Perspective comparison matrix
- Packet design implications

**TONE.md** — New file (~2,200 words) containing:
- 6 narrator tonal registers with vocabulary markers, rhythm/syntax patterns, emotional coloring, sample markers
- Tonal shift triggers for each narrator
- Tonal contrast table
- Tone as generation parameter (vocabulary, rhythm, metaphor sourcing, etc.)
- Tone mixing/contamination notes

### Verification Completed
- All actions in ACTIONS.md have agents in CHARACTERS.md
- All narrators in PERSPECTIVES.md have character entries
- Tonal descriptors in TONE.md align with perspective analysis

### Architecture Summary
```
ACTIONS (what happened) → CHARACTERS (who did it)
                              ↓
                       PERSPECTIVES (how it's filtered)
                              ↓
                          TONE (how it sounds)
```

### Current State
- Foundation layer complete: ACTIONS, CHARACTERS, PERSPECTIVES, TONE
- Ready for Layer 1 world state extraction (geography, settings)
- Ready for Layer 3 hidden narrative logic development
- Ready for playtesting protocols

---

## 2026-02-04 — Session 5: Graph Structures and Probabilistic Models

### Requested
Build computational graph representations for narrative structure extraction:
1. All five "load-bearing" extraction structures from EXTRACTION_TECHNIQUES.md
2. Persist in formats viewable with standard tools (Gephi, yEd)
3. Test with pyAgrum for Bayesian network analysis
4. Model state transitions probabilistically (P(actual) vs P(anything else))
5. Build as a Poetry project
6. Create DAG structure for counterfactual reasoning

### Delivered

**Poetry Project Setup** (`pyproject.toml`):
- Dependencies: pyagrum, networkx, matplotlib, pandas
- Python 3.11 compatible

**Graph Build Scripts** (`scripts/`):

1. `build_knowledge_state_graph.py` — Who knows what, when
   - Bipartite graph: Characters ↔ Facts
   - Knowledge asymmetry graph between characters
   - 21 nodes, 62 edges

2. `build_causal_chain_graph.py` — Event causation DAG
   - 22 events with CAUSES/ENABLES relationships
   - Bottleneck analysis (Candy dosing Franklin is key hinge)
   - 22 nodes, 22 edges

3. `build_event_perspective_matrix.py` — Narrator coverage
   - 41 events × 8 narrators matrix
   - Coverage types: direct, hearsay, retrospective, inferred
   - Bipartite graph: 49 nodes, 127 edges

4. `build_location_graph.py` — Spatial relationships
   - 30 locations with CONTAINS, ADJACENT_TO, VISIBLE_FROM edges
   - Perception constraints for witness validation
   - 30 nodes, 52 edges

5. `build_voice_fingerprints.py` — Narrator style features
   - Lexical markers, punctuation profiles, discourse patterns
   - Quantitative basis for TONE.md

6. `build_state_transitions.py` — Probabilistic state model
   - 11 key transitions with P(actual) assignments
   - Chain probability: 0.000694 (the story is very unlikely!)
   - Most surprising: Candy doses Franklin (P=0.15)

7. `build_counterfactual_dag.py` — Hinge points and alternatives
   - 45 nodes including 7 counterfactual branches
   - 10 identified hinge points
   - DAG structure for "what if" reasoning

**Output Files** (`graphs/`):
- `.graphml` — For yEd, Gephi, NetworkX
- `.gexf` — Gephi native format
- `.json` — Programmatic access
- Analysis files with metrics

**Test Script** (`scripts/test_graphs.py`):
- Loads and validates all graphs
- Reports on hinge points
- Shows knowledge asymmetries

### Key Findings

**Most Contingent Hinge Points** (lowest P, most surprising):
1. Dr. Candy doses Franklin (P=0.15) — The twist
2. Jennings reconstructs truth (P=0.25) — The detection
3. Rachel witnesses theft (P=0.30) — The dramatic irony

**Chain Probability**: 0.000694
- The actual narrative path is very unlikely (~1 in 1400)
- Most branches would have led elsewhere

**Knowledge Asymmetries** (who knows what others don't):
- Dr. Candy knows only one fact (he drugged Franklin) that's crucial
- Godfrey knows he stole the diamond — no one else does until the end
- Rachel knows Franklin entered her room — her silence drives the plot

### Decisions & Reasoning
- Used NetworkX for graphs (well-supported, many export formats)
- pyAgrum BIF export had CPT sizing issues — graphs work, BN inference needs refinement
- Focused on "load-bearing" structures, not trivial metrics
- Simplified probabilistic model: P(actual) vs P(other) binary
- DAG structure allows counterfactual reasoning about alternative outcomes

### Current State
- Computational graph infrastructure complete
- All foundation documents (ACTIONS, CHARACTERS, PERSPECTIVES, TONE) verified against graphs
- Ready for: Generation testing, perturbation experiments, alternative narrative generation

---

## 2026-02-05 — Session 6: Graph Viewer

### Requested
Build a minimal, parsimonious viewer for the narrative graphs. Not minimal in functionality—minimal in the sense of a clean foundation that can be iterated rapidly.

### Delivered

**Viewer** (`viewer/`):
- Flask + PyVis web app
- Six views: Counterfactual DAG, Causal Chain, Knowledge State, Knowledge Asymmetry, Locations, Event-Perspective Matrix
- Clean CSS optimized for screenshots
- Interactive graphs with hover info

**Dependencies added**: flask, pyvis

**Run with**: `poetry run python viewer/app.py` → http://localhost:5050

### Architecture Notes

The viewer is part of the larger system for growing the story into a meta-story. The plan (per user):
- Parameterize the story
- Fill in probability distributions from what's in the text and what's implied by worldbuilding
- The graphs are the skeleton; the viewer is the interface; the packet is the artifact

### Current State
- Viewer running and functional
- Ready for iteration via screenshots and discussion
- Next: refine visualizations, add interactivity, connect to generation

---

## 2026-02-04 — Session 7: Stats View and Graph Annotations

### Requested
1. Add NLP statistics view with word counts, character co-occurrence matrix, and classic metrics
2. Add helper text/questions to each graph view as "a way in"
3. Add color legends explaining what node/edge colors mean
4. Add hover tooltips with narrative detail
5. Explain what transitions edges represent
6. Fix knowledge asymmetry graph interpretability — add alternative view

### Delivered

**Stats View** (`viewer/stats.py`, `viewer/templates/stats.html`):
- Basic corpus statistics: 197,940 words, 21,377 lines, type-token ratio, hapax legomena
- Words per narrator section with bar charts
- Character mention frequencies
- Character co-occurrence matrix (within 50-word window) with heat coloring
- Top bigrams and trigrams
- Top 50 words visualization

**Graph Annotations**:
- Each graph now has a **question** as entry point (e.g., "What if things had gone differently?")
- Each graph now has a **color legend** explaining node and edge colors
- All nodes and edges now have **rich hover tooltips** with narrative context:
  - Counterfactual DAG: Shows probability, hinge point status, counterfactual branches
  - Causal Chain: Shows required vs. contingent events, CAUSES vs. ENABLES relationships
  - Knowledge State: Shows character/fact type, KNOWS vs. SUSPECTS relationships
  - Knowledge Asymmetry: Shows who holds secrets over whom, with fact lists
  - Locations: Shows location type, spatial relationships (CONTAINS, ADJACENT, VISIBLE/AUDIBLE)

**Secrets View** (`viewer/templates/secrets.html`, new route `/secrets`):
- Alternative to Knowledge Asymmetry graph
- Readable list format showing: who → who, count of secrets, list of facts
- Sorted by number of secrets (most powerful asymmetries first)

**Files Changed**:
- `viewer/app.py` — Added stats route, secrets route, questions and legends for all graph routes
- `viewer/graphs.py` — Added `load_knowledge_asymmetry_data()`, improved all render functions with rich tooltips
- `viewer/static/style.css` — Added styles for stats page, graph legends, secrets page
- `viewer/templates/graph.html` — Added question, description, and legend display
- `viewer/templates/matrix.html` — Added question
- `viewer/templates/stats.html` — Created
- `viewer/templates/secrets.html` — Created
- `viewer/templates/base.html` — Added Stats and Secrets nav links

**Documents View** (`viewer/templates/docs_index.html`, `viewer/templates/docs_view.html`, new routes `/docs`, `/docs/<name>`):
- Index page listing all documents grouped by category (Foundation vs. Meta)
- Individual document view with rendered markdown
- Cross-references between documents (document names become links)
- Character name highlighting
- Related documents sidebar (shows documents referenced within current document)
- Quick navigation between all documents

**Documents Included**:
- Foundation: ACTIONS, CHARACTERS, PERSPECTIVES, TONE
- Meta: PLAN, EXTRACTION_TECHNIQUES, LOG, CLAUDE

### Current State
- All graph views now have: questions, descriptions, color legends, rich hover tooltips
- Stats view provides classic NLP metrics
- Secrets view provides interpretable alternative to knowledge asymmetry graph
- Documents view provides access to all foundation and meta documents with cross-references
- Ready for: further iteration, generation testing, connecting graphs to narrative output

---

## 2026-02-04 — Session 8: Counterfactuals System

### Requested
Build a system for cooperatively filling in alternate paths at hinge points. Need to:
- Browse an inventory of plausible immediate alternative outcomes
- Assess plausibility of alternatives
- Start minimal (no probability), layer probability later

### Delivered

**Plan Document** (`COUNTERFACTUALS_PLAN.md`):
- Data model for hinges and alternatives
- JSON schema with outcome, immediate_effects, plausibility_notes, blocks fields
- View specifications for index, detail, and edit pages
- Implementation order
- Future probability layer design

**Data File** (`graphs/counterfactuals.json`):
- 10 hinge points seeded from existing hinge_points.json
- Each with description and actual_outcome
- Empty alternatives arrays ready to be filled

**Backend** (`viewer/counterfactuals.py`):
- load_counterfactuals / save_counterfactuals
- get_hinge, add_alternative, update_alternative, delete_alternative
- get_all_hinge_ids (for blocks dropdown)

**Routes** (in `viewer/app.py`):
- `/hinges` — Index of all hinge points
- `/hinges/<id>` — Detail view with alternatives
- `/hinges/<id>/add` — Form to add alternative (GET/POST)
- `/hinges/<id>/<alt_id>/edit` — Edit existing alternative
- `/hinges/<id>/<alt_id>/delete` — Delete alternative

**Templates**:
- `hinges_index.html` — Card list of hinges with alternative counts
- `hinge_detail.html` — Shows actual outcome + all alternatives with effects, plausibility, blocks
- `hinge_edit.html` — Form for adding/editing alternatives

**Styling**: Full CSS for hinges pages including cards, forms, checkbox grids, action buttons

**Nav**: Added "Hinges" link to navigation

### Data Model (v1 — no probability)

```json
{
  "id": "rachel_witnesses",
  "description": "Rachel sees Franklin take the diamond",
  "actual_outcome": "Rachel stays silent, assumes Franklin is a thief, breaks off engagement",
  "alternatives": [
    {
      "id": "rachel_witnesses_alt_1",
      "outcome": "Rachel confronts Franklin immediately",
      "immediate_effects": [
        "Franklin reveals he has no memory of it",
        "Rachel's anger turns to confusion"
      ],
      "plausibility_notes": "In character — Rachel is direct. But wounded pride might override.",
      "blocks": ["rosanna_hides_nightgown", "investigation_splits"]
    }
  ]
}
```

### Files Changed
- `COUNTERFACTUALS_PLAN.md` — Created
- `graphs/counterfactuals.json` — Created (10 hinges seeded)
- `viewer/counterfactuals.py` — Created
- `viewer/app.py` — Added hinges routes
- `viewer/templates/hinges_index.html` — Created
- `viewer/templates/hinge_detail.html` — Created
- `viewer/templates/hinge_edit.html` — Created
- `viewer/templates/base.html` — Added Hinges nav link
- `viewer/static/style.css` — Added hinges styling
- `README.md` — Added Hinges section, COUNTERFACTUALS_PLAN.md link
- `LOG.md` — This entry

### What's NOT in v1
- Probability scores
- Cascading effects (alternative A affects hinge B)
- AI-assisted generation
- Versioning or history

### Current State
- Hinges system functional at http://localhost:5050/hinges
- Can browse hinges, add alternatives, edit/delete them
- Data persists to counterfactuals.json
- Ready for: manual population of alternatives, then probability layer
