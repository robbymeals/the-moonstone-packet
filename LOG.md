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
