# Narrative Structure Extraction Techniques

An inventory of computational techniques and algorithms for extracting narrative structure from literary texts, with emphasis on graph-based methods and automatable approaches.

---

## 1. CHARACTER NETWORK EXTRACTION (Graph-Based)

**What it does**: Builds a graph where vertices = characters, edges = interactions (co-occurrence, dialogue, relationships).

**Core NLP Pipeline**:
1. **Named Entity Recognition (NER)** — Identify character names
2. **Coreference Resolution** — Link "Tom", "Tom Sawyer", "Mr. Sawyer", pronouns → single entity
3. **Interaction Detection** — Co-occurrence in sentences/paragraphs, dialogue attribution, action-recipient relations

**Tools**:
- [BookNLP](https://github.com/booknlp/booknlp) — Purpose-built for literary texts, includes character clustering, gender inference, quotation speaker ID
- [character-network](https://github.com/hzjken/character-network) — Network graph + sentiment analysis for character relationships
- Stanford NER + spaCy for general NER

**Metrics produced**:
- Centrality measures (degree, betweenness, eigenvector)
- Community detection (character clusters)
- Edge weights (interaction frequency)
- Sentiment polarity on edges

**Automatable?**: Yes, with good accuracy on modern texts. 19th-century texts need tuning.

**References**:
- [Extraction and Analysis of Fictional Character Networks: A Survey](https://hal.science/hal-02173918/document)
- [The Role of NLP Tasks in Automatic Literary Character Network Construction](https://arxiv.org/abs/2412.11560)
- [Evaluating NER Tools for Extracting Social Networks from Novels](https://pmc.ncbi.nlm.nih.gov/articles/PMC7924459/)

---

## 2. EVENT EXTRACTION AND TIMELINE RECONSTRUCTION

**What it does**: Identifies events (actions, state changes) and orders them temporally.

**Core NLP Pipeline**:
1. **Event Detection** — Identify predicates/actions
2. **Temporal Expression Extraction** — "that night", "three days later", absolute dates
3. **Temporal Ordering** — Before/after/simultaneous relationships
4. **Event Linking** — Causal chains, consequence relationships

**Methods**:
- Semantic Role Labeling (SRL) — Who did what to whom
- FrameNet — Semantic frame extraction
- Verb-centric extraction — Subject-Verb-Object triples
- Temporal relation classification (TimeML/TimeBank)

**Output graph**: Events as nodes, temporal/causal relations as directed edges

**Automatable?**: Partially. Event detection is good; temporal ordering is harder (often implicit in narrative).

**References**:
- [Automatic Extraction of Narrative Structure from Long Form Text](https://digitalcommons.fiu.edu/etd/3912/) — PhD dissertation
- [Steps Towards a System to Extract Formal Narratives from Text](https://ceur-ws.org/Vol-2342/paper7.pdf)
- [Extracting Events and Their Relations from Texts](https://www.sciencedirect.com/science/article/pii/S266665102100005X)
- [Event Extraction Survey](https://github.com/BaptisteBlouin/EventExtractionPapers)

---

## 3. EMOTIONAL ARC DETECTION (Sentiment Trajectory)

**What it does**: Plots emotional valence over the course of a narrative to identify story shape.

**The Six Basic Shapes** (Reagan et al., building on Vonnegut):
1. **Rags to riches** (steady rise)
2. **Tragedy** (steady fall)
3. **Man in a hole** (fall → rise)
4. **Icarus** (rise → fall)
5. **Cinderella** (rise → fall → rise)
6. **Oedipus** (fall → rise → fall)

**Method**:
1. Sliding window (e.g., 10,000 words)
2. Sentiment scoring per window (Hedonometer/labMT, VADER, transformer classifiers)
3. Smooth into trajectory curve
4. Classify against archetypal shapes

**Tools**:
- [Hedonometer](http://hedonometer.org/) — Word-level happiness scoring
- VADER — Valence-aware sentiment
- Transformer sentiment classifiers (fine-tuned on literary text)

**Automatable?**: Fully automatable. Interpretation requires domain knowledge.

**References**:
- [The Emotional Arcs of Stories are Dominated by Six Basic Shapes](https://link.springer.com/article/10.1140/epjds/s13688-016-0093-1) — The canonical paper
- [Data Mining Reveals the Six Basic Emotional Arcs](https://www.technologyreview.com/2016/07/06/158961/data-mining-reveals-the-six-basic-emotional-arcs-of-storytelling/)

---

## 4. SCENE AND CHAPTER SEGMENTATION

**What it does**: Automatically detects narrative unit boundaries (scenes, chapters, segments).

**Scene boundary triggers**:
- Temporal shifts ("two hours later")
- Spatial transitions ("back at the house")
- Character constellation changes (new characters enter/exit)

**Methods**:
- Text coherence models (topic shifts)
- Transformer-based classifiers (fine-tuned USE, BERT)
- Coreference chain breaks
- Lexical chain analysis

**Challenges**:
- Scene boundaries often implicit
- Best F1 scores around 24% (still research-grade)
- Chapter boundaries easier than scene boundaries

**Tools**:
- [Chapter Captor](https://aclanthology.org/2020.emnlp-main.672.pdf) — Chapter segmentation using coherence
- Scene segmentation research still emerging

**Automatable?**: Partially. Chapter boundaries: good. Scene boundaries: emerging.

**References**:
- [Chapter Captor: Text Segmentation in Novels](https://arxiv.org/abs/2011.04163)
- [Detecting Scenes in Fiction: A New Segmentation Task](https://aclanthology.org/2021.eacl-main.276.pdf)
- [Rethinking Scene Segmentation](https://aclanthology.org/2025.latechclfl-1.8.pdf)

---

## 5. KNOWLEDGE GRAPH CONSTRUCTION

**What it does**: Builds structured graph of entities, relationships, attributes, and events.

**Graph components**:
- **Nodes**: Characters, locations, objects, events, times
- **Edges**: Relationships (family, employment, romance), actions, causal links
- **Attributes**: Character traits, object properties, temporal metadata

**Methods**:
- Relation extraction (subject-relation-object triples)
- Open Information Extraction (OpenIE)
- LLM-based extraction (GPT-4, Claude for complex relations)
- Schema-guided extraction (predefined relation types)

**Recent work**:
- **HTEKG** (Human-Trait-Enhanced Knowledge Graph) — Adds character traits to event-centered KGs
- **Temporal Knowledge Graphs** — Capture dynamic relationships over narrative time

**Tools**:
- [KGGen](https://arxiv.org/html/2502.09956v1) — LLM-based KG extraction from plain text
- OpenIE (Stanford, AllenNLP)
- Neo4j for storage/querying

**Automatable?**: Yes with LLMs. Quality depends on prompt engineering and post-processing.

**References**:
- [Building Narrative Structures from Knowledge Graphs](https://dl.acm.org/doi/10.1007/978-3-031-11609-4_38)
- [Temporal Knowledge Graph Approach for Narrative Templates](https://link.springer.com/article/10.1007/s13278-025-01429-8)
- [HTEKG: Human-Trait-Enhanced Literary Knowledge Graph](https://www.scitepress.org/Papers/2024/130136/130136.pdf)

---

## 6. HIERARCHICAL NARRATIVE GRAPH MODELS

**What it does**: Represents narrative structure at multiple levels simultaneously.

**Three structural dimensions** (Akimoto model):
1. **Story World** — Background world structure (setting, rules, entities)
2. **Story** — Chronologically organized events (fabula)
3. **Discourse** — Structure used for expression (plot, perspective)

**Graph structure**:
- Hierarchical nodes (story → episodes → scenes → events)
- Cross-level links (character appears in scene, scene contains event)
- Multiple edge types (causal, temporal, thematic)

**Applications**:
- Story generation (top-down)
- Story understanding (bottom-up)
- Plot comparison across works

**Automatable?**: Research-grade. Requires significant manual schema design.

**References**:
- [Computational Modeling of Narrative Structure: A Hierarchical Graph Model](https://www.semanticscholar.org/paper/Computational-Modeling-of-Narrative-Structure-:-A-Akimoto/332621f050564a888f83430b93d72963b21d740d)
- [A Survey on Narrative Extraction from Textual Data](https://link.springer.com/article/10.1007/s10462-022-10338-7)

---

## 7. QUOTATION AND DIALOGUE ATTRIBUTION

**What it does**: Links spoken dialogue to speakers.

**Pipeline**:
1. Quotation boundary detection (quote marks, reporting clauses)
2. Speaker identification (explicit: "said John", implicit: nearby mention)
3. Addressee detection (who's being spoken to)

**Challenges**:
- Nested dialogue
- Interrupted quotations
- Free indirect discourse (character thought without quote marks)

**BookNLP approach**: Uses character clusters + proximity + reporting verbs

**Automatable?**: Yes, reasonable accuracy with BookNLP.

---

## 8. PERSPECTIVE AND FOCALIZATION DETECTION

**What it does**: Identifies whose consciousness filters the narrative at each point.

**Types**:
- **External focalization**: Camera-eye, no interiority
- **Internal focalization**: Through one character's perception
- **Variable focalization**: Shifts between characters

**Signals**:
- Perception verbs ("she saw", "he felt")
- Epistemic markers ("apparently", "seemed")
- Free indirect discourse
- Pronoun patterns

**Current state**: Research-grade. LLMs can help with annotation.

**Relevance to Moonstone**: Critical for multi-narrator structure.

---

## 9. STYLOMETRY AND AUTHOR/NARRATOR VOICE

**What it does**: Quantifies stylistic features that distinguish voices.

**Features**:
- Function word frequencies
- Sentence length distributions
- Vocabulary richness (type-token ratio)
- Part-of-speech patterns
- Punctuation usage

**Applications**:
- Author attribution
- Narrator voice fingerprinting
- Style consistency checking in generation

**Tools**:
- Stylo (R package)
- NLTK for feature extraction
- Custom transformer probes

**Automatable?**: Fully automatable. Interpretation requires expertise.

---

## 10. TOPIC MODELING FOR THEMATIC STRUCTURE

**What it does**: Discovers latent thematic patterns across the text.

**Methods**:
- **LDA** (Latent Dirichlet Allocation) — Classic topic modeling
- **BERTopic** — Neural topic modeling with embeddings
- **Top2Vec** — Document embedding clustering

**Applications for narrative**:
- Theme trajectory over chapters
- Thematic similarity between scenes
- Character-associated topics

**Automatable?**: Fully automatable. Topic labeling needs human review.

---

## TOOLS SUMMARY

| Tool | What it does | URL |
|------|-------------|-----|
| **BookNLP** | Full literary NLP pipeline (characters, events, quotes) | [GitHub](https://github.com/booknlp/booknlp) |
| **LitBank** | Annotated literary dataset for training | [Berkeley](https://people.ischool.berkeley.edu/~dbamman/pubs/pdf/Bamman_DH_Debates_CompHum.pdf) |
| **Hedonometer** | Sentiment/happiness scoring | [hedonometer.org](http://hedonometer.org/) |
| **Neo4j** | Graph database for knowledge graphs | [neo4j.com](https://neo4j.com/) |
| **spaCy** | NER, POS, dependency parsing | [spacy.io](https://spacy.io/) |
| **Hugging Face Transformers** | Pre-trained models for all tasks | [huggingface.co](https://huggingface.co/) |
| **NetworkX** | Python graph analysis | [networkx.org](https://networkx.org/) |
| **Gephi** | Graph visualization | [gephi.org](https://gephi.org/) |

---

## RECOMMENDED EXTRACTION PIPELINE FOR MOONSTONE PACKET

### Phase 1: Automated Extraction (High Confidence)
1. **BookNLP pass** — Characters, quotation attribution, events
2. **Character network** — Build interaction graph
3. **Emotional arc** — Sentiment trajectory per narrator section
4. **Chapter/section boundaries** — Already marked in text, verify

### Phase 2: Semi-Automated (Human-in-Loop)
1. **Knowledge graph** — LLM extraction + human verification
2. **Temporal event ordering** — LLM assist + manual correction
3. **Scene boundaries within chapters** — Model suggestions + human annotation

### Phase 3: Human-Verified Metrics
1. **Perspective shifts** — Manual annotation, guided by pronouns/perception verbs
2. **Causal chain validation** — LLM-generated, human-verified
3. **Thematic structure** — Topic model output + interpretation

---

## METRICS WE COULD AUTOMATE FOR THE MOONSTONE

| Metric | Method | Confidence |
|--------|--------|------------|
| Character mention frequency | BookNLP NER | High |
| Character interaction network | Co-occurrence + sentiment | High |
| Emotional arc per narrator | Sliding window sentiment | High |
| Dialogue distribution | Quotation attribution | Medium-High |
| Event density per chapter | Event extraction | Medium |
| Scene boundaries | Transformer classifier | Medium |
| Temporal ordering of events | SRL + temporal expressions | Medium |
| Perspective shifts | Pronoun/perception analysis | Low-Medium |
| Causal chains | LLM extraction | Medium (needs verification) |
| Knowledge graph | LLM + OpenIE | Medium (needs verification) |

---

## STRUCTURALLY LOAD-BEARING EXTRACTIONS FOR THE PACKET

The following techniques directly enrich the packet architecture. Not metrics for their own sake — structures that enable new capabilities.

### 1. KNOWLEDGE STATE GRAPH (Critical)

**Why it matters**: The packet format depends on perspective asymmetry. Rachel knows Franklin took the diamond but doesn't know about the laudanum. Franklin doesn't know he took it. Godfrey knows both.

**Structure**:
```
Node types: Character, Fact
Edge types: KNOWS(character, fact, since_when), BELIEVES_FALSE(character, fact), SUSPECTS(character, fact)
```

**What it enables**:
- Automatic generation of what a character can/cannot say at any point
- Detection of dramatic irony (reader knows X, character doesn't)
- Validation of perspective coherence ("Betteredge couldn't mention the laudanum in chapter 5 because he didn't learn it until...")

**Extraction method**:
- Semi-automated: LLM pass over each section to extract knowledge state changes
- Human verification of key turning points

### 2. EVENT-PERSPECTIVE COVERAGE MATRIX (Critical)

**Why it matters**: Different narrators cover overlapping and non-overlapping events. The packet needs to know which events are told by whom and how they differ.

**Structure**:
```
Matrix: Events × Narrators
Cell values: {not_covered, narrated_directly, narrated_from_hearsay, mentioned_retrospectively}
```

**What it enables**:
- Identify gaps (events no narrator covers)
- Identify conflicts (same event, different versions)
- Identify redundancy (same event, multiple narrators — compare treatment)

**For The Moonstone specifically**:
- The birthday dinner is covered by Betteredge (present) and referenced by others
- Franklin taking the diamond is covered by Rachel (witnessed), Franklin (reconstructed), nobody else directly
- Godfrey's theft is covered by Cuff's final report only

**Extraction method**:
- Manual extraction from existing ACTIONS.md + PERSPECTIVES.md
- Cross-reference table

### 3. CAUSAL CHAIN GRAPH (Already started)

**Why it matters**: The 12-step causal chain in ACTIONS.md is the backbone. But a graph representation would enable:

**Structure**:
```
Nodes: Events
Edges: CAUSES, ENABLES, PREVENTS
Attributes: necessity (required vs. contingent), timing
```

**What it enables**:
- Perturbation testing: "If Rosanna doesn't hide the nightgown, what breaks?"
- Minimal change identification: What's the smallest intervention that changes the outcome?
- Alternate history generation: Given the same characters, what other plots could occur?

**Extraction method**:
- Already have the chain narratively; convert to formal graph
- Add necessity weights through analysis

### 4. CHARACTER VOICE FINGERPRINT (Supports TONE.md)

**Why it matters**: For generation, we need to distinguish Betteredge's voice from Cuff's computationally.

**Structure**:
```
Features per narrator:
- Sentence length distribution
- Function word profile
- Vocabulary richness
- Digression frequency (parenthetical/aside rate)
- Direct address rate ("you", "the reader")
- Specific lexical markers (Robinson Crusoe mentions, rose references)
```

**What it enables**:
- Automatic style checking during generation
- Voice blending detection (when one narrator reports another's words)
- Quantitative basis for TONE.md claims

**Extraction method**:
- Fully automated with existing NLP tools
- BookNLP + custom feature extraction

### 5. SCENE LOCATION GRAPH (Supports World State)

**Why it matters**: The packet needs spatial grounding. Events happen in places, and places constrain what characters can perceive.

**Structure**:
```
Nodes: Locations (Verinder house, Rachel's sitting room, Shivering Sand, London)
Edges: CONTAINS, ADJACENT_TO, VISIBLE_FROM, AUDIBLE_FROM
Events tagged with location
Characters tagged with location at each time
```

**What it enables**:
- Perception validation: "Could Betteredge hear what happened in Rachel's room?" (No, different floor)
- Spatial coherence in generation
- Map generation

**Extraction method**:
- Semi-automated: NER for locations + manual spatial relationship annotation
- The novel provides good spatial description

---

## PRIORITY ORDER FOR MOONSTONE PACKET

1. **Knowledge State Graph** — Most critical for perspective accuracy
2. **Event-Perspective Coverage Matrix** — Enables systematic comparison
3. **Causal Chain Graph** — Already have data, needs formalization
4. **Character Voice Fingerprint** — Automated, validates TONE.md
5. **Scene Location Graph** — Important for world state, can wait

---

## WHAT'S NOT WORTH DOING

- Generic sentiment analysis (emotional arc of "the novel" — too coarse)
- Character centrality metrics (we already know Franklin/Rachel are central)
- Topic modeling (themes are clear, not latent)
- Full NER extraction (BookNLP will give us character names, but we already have them)

The value is in **relational structures** that encode constraints and enable reasoning, not in counting things.

---

*This inventory serves as a research foundation for building automated extraction tools for the narrative packet format.*
