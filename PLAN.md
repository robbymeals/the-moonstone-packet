# Plan: Moonstone Packet Foundation Files

## Hypothesis: Why CHARACTERS and PERSPECTIVES Are Distinct Primitives

**CHARACTERS** = ontological entities (who exists in the world)
**PERSPECTIVES** = epistemological frames (through whose consciousness we experience the world)

In *The Moonstone*, Gabriel Betteredge exists as a **character** (elderly house-steward, loyal, superstitious, loves Robinson Crusoe) AND as a **perspective** (First Period narrator whose warm, digressive, class-conscious lens filters everything we see).

The same material events filtered through different perspectives yield different narratives:
- Franklin Blake as seen by Betteredge (beloved young master, slightly foreign)
- Franklin Blake as seen by Miss Clack (godless, dangerously attractive)
- Franklin Blake narrating himself (confused, guilty, seeking truth)

This separation is essential for the packet format because:
1. **ACTIONS** are perspective-neutral (what materially occurred)
2. **CHARACTERS** persist across all perspectives as consistent entities
3. **PERSPECTIVES** are the transformation functions that convert actions into experienced narrative
4. **TONE** emerges from the intersection of perspective-holder and content

---

## Deterministic Analysis (Already Gathered)

**Basic Statistics:**
- 21,377 lines / 197,940 words / 1,135,571 characters

**Structure:**
- PROLOGUE (line 118) — "Extracted from a Family Paper" (Herncastle cousin)
- FIRST PERIOD (line 355) — "The Loss of the Diamond" — Gabriel Betteredge (23 chapters)
- SECOND PERIOD (line 8489) — "The Discovery of the Truth":
  - First Narrative — Miss Clack (8 chapters)
  - Second Narrative — Matthew Bruff, Solicitor (3 chapters)
  - Third Narrative — Franklin Blake (10 chapters)
  - Fourth Narrative — Ezra Jennings' Journal
  - Fifth Narrative — Franklin Blake (conclusion)
  - Sixth Narrative — Sergeant Cuff (report)
- EPILOGUE (line 20771) — "The Finding of the Diamond":
  - Statement of Sergeant Cuff's Man
  - Statement of the Captain
  - Statement of Mr. Murthwaite

**Character Name Frequency (top 15):**
| Character | Mentions |
|-----------|----------|
| Franklin (Blake) | 537 |
| Rachel (Verinder) | 483 |
| Betteredge | 350 |
| Diamond | 335 |
| Verinder | 296 |
| Cuff | 258 |
| Rosanna (Spearman) | 249 |
| Godfrey (Ablewhite) | 247 |
| Bruff | 230 |
| Moonstone | 176 |
| Penelope | 147 |
| Luker | 128 |
| Spearman | 115 |
| Jennings | 100 |
| Clack | 66 |

**Key Motifs:**
- Shivering Sand: 33 mentions
- Nightgown: 70 mentions
- Paint/smear: 84 mentions
- Robinson Crusoe: 42 mentions
- Indians: 217 mentions

---

## Order of Operations

**Dependency graph:**
```
ACTIONS (foundation - what happened)
   ↓
CHARACTERS (who did it, their arcs)
   ↓
PERSPECTIVES (how it's filtered through consciousness)
   ↓
TONE (the felt quality of each perspective's voice)
```

ACTIONS must come first because you cannot describe character arcs without knowing what happened. CHARACTERS must precede PERSPECTIVES because perspectives are held by characters. TONE is last because it emerges from the intersection of perspective-holder and content.

---

## Execution Plan (Parallelizable Steps Marked)

### Phase A: Create Tracking Checklist
Create `CHECKLIST.md` to track progress through all files.

### Phase B: ACTIONS.md
Extract the purely mechanical sequence of events, perspective-neutral. This requires reading through the text and distilling what materially occurred, when, and where.

**Sections:**
1. Prologue events (1799 — Siege of Seringapatam, theft of diamond)
2. Birthday dinner night (June 1848 — timeline hour by hour)
3. Post-theft investigation (June-July 1848)
4. London events (1848-1849)
5. Opium experiment (June 1849)
6. Resolution and recovery of diamond

### Phase C: CHARACTERS.md
**Can begin in parallel with Phase B** — character inventory doesn't require complete action timeline.

For each character:
- Role/position
- What they know and when
- What they want
- What they hide
- Key actions they take

**Major characters:** Betteredge, Franklin Blake, Rachel Verinder, Rosanna Spearman, Sergeant Cuff, Godfrey Ablewhite, Ezra Jennings, Miss Clack, Matthew Bruff
**Minor characters:** Penelope, Lady Verinder, Mr. Murthwaite, Mr. Luker, the three Indians, Limping Lucy, Dr. Candy

### Phase D: PERSPECTIVES.md
**Must wait for ACTIONS.md and CHARACTERS.md**

Document each narrative voice:
- Who narrates (character identity)
- What portion of the text
- What they can perceive vs. what they miss
- What they misinterpret
- Their relationship to other characters (bias sources)
- How they compare to other narrators

**Narrators:** Prologue narrator (Herncastle cousin), Betteredge, Miss Clack, Bruff, Franklin Blake, Ezra Jennings, Sergeant Cuff, Murthwaite

### Phase E: TONE.md
**Must wait for PERSPECTIVES.md**

Inventory the distinct tonal registers:
- Betteredge's warm/digressive/class-conscious/superstitious
- Clack's pious/self-righteous/repressed
- Bruff's legal/dry/factual
- Franklin Blake's anxious/searching/self-doubting
- Jennings' melancholic/scientific/compassionate
- Cuff's analytical/detached/professional

Document how tone shifts within narrators and what triggers shifts.

---

## Parallel Execution Opportunities

```
Phase A (CHECKLIST.md)
        ↓
   ┌────┴────┐
   ↓         ↓
Phase B   Phase C
(ACTIONS) (CHARACTERS)
   └────┬────┘
        ↓
    Phase D
  (PERSPECTIVES)
        ↓
    Phase E
     (TONE)
```

Phases B and C can run in parallel. Phases D and E are sequential dependencies.

---

## Files to Create

1. `CHECKLIST.md` — Progress tracker
2. `ACTIONS.md` — Mechanical events
3. `CHARACTERS.md` — Character inventory
4. `PERSPECTIVES.md` — Narrative voice analysis
5. `TONE.md` — Tonal register inventory

---

## Verification

After completion:
- Cross-check that every action in ACTIONS.md has an agent in CHARACTERS.md
- Verify every narrator in PERSPECTIVES.md has a corresponding character entry
- Confirm tonal descriptors in TONE.md align with perspective analysis
- Update LOG.md with session summary
