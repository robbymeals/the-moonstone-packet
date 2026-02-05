# The Moonstone Packet

A proof-of-concept for **narrative packets**: dense, structured artifacts that readers decompress collaboratively with an AI, exploring stories from any angle, at any depth, through any consciousness.

## What This Is

Wilkie Collins' *The Moonstone* (1868) is the test case. Collins structured the novel as multiple witnesses testifying about the same events—a theft, an investigation, a slowly revealed truth. That multi-perspectival architecture makes it ideal for extraction into computable form.

This project extracts the novel's latent narrative structure into:

- **Foundation documents** — perspective-neutral timelines, character inventories, tonal registers
- **Graph structures** — causal chains, knowledge states, counterfactual branches, spatial relationships
- **Probabilistic models** — hinge points where the story could have gone differently, with assigned probabilities

The graphs are the skeleton. The viewer is the interface. The packet is the artifact.

## Why This Matters

Traditional novels are static. Readers experience them linearly, through a fixed sequence of perspectives.

A narrative packet is different. It encodes:
- What happened (perspective-neutral facts)
- Who knows what and when (knowledge asymmetries)
- How each consciousness filters reality (perspective transforms)
- Where the story could have diverged (counterfactual branches)

With this structure, a reader can:
- Experience the same events through different characters' eyes
- Explore "what if" branches where key decisions went otherwise
- Adjust their depth of engagement (surface summary to full immersion)
- Discover hidden logic that the original text only implies

## Quickstart

```bash
# Clone and enter
git clone <repo-url>
cd the-moonstone-packet

# Install dependencies
poetry install

# Start the viewer
cd viewer
poetry run python app.py
```

Open http://localhost:5050

## The Viewer

The web interface provides access to:

| View | Question It Answers |
|------|---------------------|
| **Counterfactual DAG** | What if things had gone differently? |
| **Causal Chain** | What caused what? What was inevitable vs. contingent? |
| **Knowledge State** | Who knows what? Whose knowledge is power? |
| **Knowledge Asymmetry** | Who holds secrets? Whose silence shapes the plot? |
| **Secrets** | (Alternative view) Readable list of who knows what others don't |
| **Locations** | Where could characters be seen or overheard? |
| **Perspectives** | What does each narrator know firsthand vs. secondhand? |
| **Stats** | Classic NLP metrics (word counts, co-occurrence, n-grams) |
| **Docs** | Foundation documents with cross-references |

## Project Structure

```
the-moonstone-packet/
├── src/
│   └── pg155.txt           # Source text (Project Gutenberg)
├── graphs/
│   ├── *.graphml           # Graph exports (yEd, Gephi compatible)
│   ├── *.gexf              # Gephi native format
│   └── *.json              # Programmatic access
├── scripts/
│   └── build_*.py          # Graph generation scripts
├── viewer/
│   ├── app.py              # Flask application
│   ├── graphs.py           # Graph rendering (PyVis)
│   ├── stats.py            # NLP statistics
│   ├── static/style.css    # Styling
│   └── templates/          # Jinja2 templates
├── ACTIONS.md              # Perspective-neutral timeline
├── CHARACTERS.md           # Character inventory
├── PERSPECTIVES.md         # Narrator analysis
├── TONE.md                 # Tonal registers
├── LOG.md                  # Session-by-session work record
└── CLAUDE.md               # AI guidance for this project
```

## Key Findings So Far

**Most Contingent Hinge Points** (events that could easily have gone otherwise):
1. Dr. Candy doses Franklin with laudanum (P=0.15) — the hidden twist
2. Ezra Jennings reconstructs the truth from fever-ramblings (P=0.25)
3. Rachel witnesses Franklin take the diamond but stays silent (P=0.30)

**Chain Probability**: ~0.07%
The actual narrative path is very unlikely (~1 in 1400). Most branches would have led elsewhere.

**Knowledge Asymmetries**:
- Rachel knows Franklin entered her room — her silence drives the entire plot
- Godfrey knows he stole the diamond — no one else does until the end
- Dr. Candy knows he drugged Franklin — the one fact that explains everything

## Foundation Documents

- **ACTIONS.md** — What actually happened, when, where (perspective-neutral)
- **CHARACTERS.md** — Who exists, what they know, what they hide, what they want
- **PERSPECTIVES.md** — How each narrator filters reality, what they miss, what they misinterpret
- **TONE.md** — Voice fingerprints: vocabulary, rhythm, emotional coloring

## License

Anti-Capitalist Software License. See LICENSE for terms.

Specifically excludes: law enforcement, military, immigration enforcement (including ICE), and for-profit use without permission.
