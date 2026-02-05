# Plan: Moonstone Graph Viewer

## Goal

Minimal, purpose-built web viewer for the narrative graphs. Optimized for:
- Viewing specific graph structures we've built
- Taking screenshots for discussion
- Rapid iteration on presentation via code changes

## Tech Stack

**PyVis + Flask** (simplest path)
- PyVis generates interactive HTML from NetworkX graphs
- Flask serves the pages and handles graph switching
- No frontend build step, just Python + HTML templates
- Already have NetworkX graphs, PyVis is one line to visualize

## Views Needed

### 1. Counterfactual DAG (Primary)
- The 45-node DAG with hinge points
- Color coding: actual path (green), counterfactual branches (red/gray), hinge points (yellow)
- Node size by probability (lower P = larger, more "surprising")
- Hierarchical top-to-bottom layout

### 2. Knowledge State Graph
- Bipartite: Characters on left, Facts on right
- Edge color by relationship type (KNOWS = solid, SUSPECTS = dashed)
- Filter by character or by fact

### 3. Knowledge Asymmetry
- Character-to-character graph
- Edge thickness = number of exclusive facts
- Click edge to see what facts differ

### 4. Causal Chain
- Linear-ish DAG of 22 events
- Color by necessity (required = bold, contingent = light)
- Highlight critical path

### 5. Event-Perspective Matrix
- Heatmap/table view (not a graph)
- Rows = events, Columns = narrators
- Color = coverage type (direct/hearsay/retrospective/inferred/none)

### 6. Location Graph
- Spatial layout mimicking actual geography
- Nested containment visible
- Perception edges (VISIBLE_FROM, AUDIBLE_FROM) highlighted

## File Structure

```
viewer/
├── app.py              # Flask app, routes
├── graphs.py           # Load and prepare graphs for visualization
├── templates/
│   ├── base.html       # Common layout, nav
│   ├── graph.html      # PyVis graph embed
│   └── matrix.html     # Table/heatmap for event-perspective
├── static/
│   └── style.css       # Minimal styling for screenshots
└── requirements.txt    # flask, pyvis, pandas
```

## Routes

```
/                       → Landing, links to all views
/counterfactual         → Counterfactual DAG
/knowledge              → Knowledge state graph
/asymmetry              → Knowledge asymmetry
/causal                 → Causal chain
/perspectives           → Event-perspective matrix (table)
/locations              → Location graph
```

## Iteration Workflow

1. Run `flask run` (or `poetry run flask run`)
2. Open in browser
3. Screenshot and share
4. Discuss changes
5. I modify Python/HTML/CSS
6. Refresh browser
7. Repeat

## Visual Design Principles

- White/light background (screenshots)
- High contrast node colors
- Readable labels (no tiny text)
- Minimal chrome (no unnecessary UI)
- Fixed viewport size option for consistent screenshots

## Implementation Order

1. **Scaffold**: Flask app, base template, nav
2. **Counterfactual DAG**: Most important view, get this right first
3. **Causal chain**: Similar to counterfactual, simpler
4. **Knowledge graphs**: Two related views
5. **Perspectives matrix**: Different (table not graph)
6. **Locations**: Nice to have, less critical

## Dependencies

```
flask
pyvis
pandas
networkx  # already have
```

## Quick Start (after implementation)

```bash
cd viewer
poetry run flask run
# Open http://localhost:5000
```

## Screenshot-Friendly Features

- Export button to save current view as PNG (PyVis has this)
- Toggle labels on/off
- Zoom presets (fit all, 100%, 150%)
- Dark/light mode toggle
- Hide UI option (graph only, for clean screenshots)

---

## Questions Before Implementation

1. Any specific color scheme preference?
2. Any graphs more important than others (prioritize)?
3. Preferred browser for viewing?
