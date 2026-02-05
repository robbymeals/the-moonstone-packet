# Counterfactuals System Plan

Minimal version: an inventory of plausible immediate alternative outcomes at each hinge point. No probability yet — just "what else could have happened here?"

## Data Model

### `counterfactuals.json`

```json
{
  "hinges": [
    {
      "id": "rachel_witnesses_theft",
      "description": "Rachel sees Franklin take the diamond",
      "actual_outcome": "She stays silent, assumes the worst about Franklin",
      "alternatives": [
        {
          "id": "rachel_confronts_immediately",
          "outcome": "Rachel confronts Franklin that night",
          "immediate_effects": [
            "Franklin reveals he has no memory of it",
            "Rachel's anger turns to confusion",
            "They investigate together instead of apart"
          ],
          "plausibility_notes": "In character — Rachel is direct and principled. But her pride and hurt might override this.",
          "blocks": ["investigation_splits", "rosanna_hides_nightgown"]
        },
        {
          "id": "rachel_tells_mother",
          "outcome": "Rachel tells Lady Verinder what she saw",
          "immediate_effects": [
            "Lady Verinder confronts Franklin privately",
            "Family closes ranks — no police involvement",
            "Sergeant Cuff never arrives"
          ],
          "plausibility_notes": "Less in character — Rachel is secretive about emotional matters. But plausible if she's scared enough.",
          "blocks": ["cuff_investigation"]
        }
      ]
    }
  ]
}
```

### Fields

- **id**: Machine-readable identifier
- **description**: What the hinge point is
- **actual_outcome**: What actually happened
- **alternatives[]**: Array of alternative outcomes
  - **id**: Identifier for this alternative
  - **outcome**: One-sentence description of what happens instead
  - **immediate_effects**: Array of direct consequences (not cascading yet)
  - **plausibility_notes**: Freeform reasoning about whether this is in-character, physically possible, etc.
  - **blocks**: Which downstream events this would prevent (links to other hinge IDs or event IDs)

## Views

### 1. Hinges Index (`/hinges`)

List all hinge points with:
- Description of the hinge
- What actually happened
- Count of alternatives generated
- Link to detail view

### 2. Hinge Detail (`/hinges/<id>`)

Shows:
- The hinge description
- What actually happened (highlighted)
- All alternatives in cards:
  - Outcome description
  - Immediate effects (bulleted)
  - Plausibility notes (collapsible or muted)
  - What this would block

### 3. Alternative Editor (`/hinges/<id>/add` or modal)

Form to add a new alternative:
- Outcome (text)
- Immediate effects (multi-line, one per line)
- Plausibility notes (textarea)
- Blocks (checkboxes of other hinges/events)

## File Structure

```
viewer/
├── app.py              # Add routes
├── counterfactuals.py  # Load/save/validate counterfactuals.json
├── templates/
│   ├── hinges_index.html
│   ├── hinge_detail.html
│   └── hinge_edit.html (or modal in detail)
graphs/
└── counterfactuals.json  # The data
```

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/hinges` | GET | List all hinge points |
| `/hinges/<id>` | GET | View hinge and its alternatives |
| `/hinges/<id>/add` | GET | Form to add alternative |
| `/hinges/<id>/add` | POST | Save new alternative |
| `/hinges/<id>/<alt_id>/edit` | GET | Edit existing alternative |
| `/hinges/<id>/<alt_id>/edit` | POST | Save edits |

## Workflow

1. **Seed the data**: Start with the existing hinge points from `hinge_points.json`, convert to new format with empty alternatives
2. **Browse**: User views hinges index, picks one to explore
3. **Generate**: User (with AI help or manually) adds alternative outcomes
4. **Review**: Alternatives accumulate, can be browsed and compared
5. **Later**: Layer probability assessments over the alternatives

## Implementation Order

1. Create `counterfactuals.json` with seed data (hinges from existing file, no alternatives yet)
2. Create `counterfactuals.py` with load/save functions
3. Create `/hinges` index route and template
4. Create `/hinges/<id>` detail route and template
5. Create add/edit routes and forms
6. Add "Hinges" to nav

## What's NOT in v1

- Probability scores
- Cascading effects (alternative A affects what's possible at hinge B)
- AI-assisted generation (just manual entry for now)
- Versioning or history
- Multi-user collaboration

## Later: Probability Layer

Once we have an inventory of alternatives, we add:

```json
{
  "id": "rachel_confronts_immediately",
  "outcome": "...",
  "probability": {
    "score": 0.25,
    "factors": {
      "character_consistency": 0.6,
      "knowledge_constraints": 1.0,
      "physical_possibility": 1.0,
      "motivation_alignment": 0.4
    },
    "reasoning": "Rachel is direct but her pride is wounded. She might confront, but silence is more likely given her emotional state."
  }
}
```

But that's v2.
