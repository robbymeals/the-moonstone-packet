"""
Moonstone Graph Viewer

Minimal Flask app for viewing narrative structure graphs.
"""

from flask import Flask, render_template, send_from_directory
from markupsafe import Markup
from pathlib import Path
import json
import re

from graphs import (
    render_counterfactual_dag,
    render_causal_chain,
    render_knowledge_state,
    render_knowledge_asymmetry,
    render_location_graph,
    load_perspective_matrix,
    load_hinge_points,
    load_knowledge_asymmetry_data,
)
from stats import get_all_stats

app = Flask(__name__)

GRAPHS_DIR = Path(__file__).parent.parent / "graphs"
DOCS_DIR = Path(__file__).parent.parent

# Document metadata
DOCUMENTS = {
    "ACTIONS": {
        "title": "Actions Timeline",
        "description": "Perspective-neutral sequence of events",
        "question": "What actually happened, in what order?",
        "category": "Foundation",
    },
    "CHARACTERS": {
        "title": "Character Inventory",
        "description": "Who exists, what they know, what they hide",
        "question": "Who are these people and what drives them?",
        "category": "Foundation",
    },
    "PERSPECTIVES": {
        "title": "Narrative Perspectives",
        "description": "How each narrator filters reality",
        "question": "Through whose eyes do we experience the story?",
        "category": "Foundation",
    },
    "TONE": {
        "title": "Tonal Registers",
        "description": "Voice fingerprints for each narrator",
        "question": "How does each narrator sound?",
        "category": "Foundation",
    },
    "PLAN": {
        "title": "Analysis Plan",
        "description": "The extraction methodology",
        "question": "How was this packet constructed?",
        "category": "Meta",
    },
    "EXTRACTION_TECHNIQUES": {
        "title": "Extraction Techniques",
        "description": "Load-bearing narrative structures",
        "question": "What structures are we extracting?",
        "category": "Meta",
    },
    "LOG": {
        "title": "Project Log",
        "description": "Session-by-session work record",
        "question": "What has been done so far?",
        "category": "Meta",
    },
    "CLAUDE": {
        "title": "Claude Instructions",
        "description": "AI guidance for this project",
        "question": "How should Claude work with this?",
        "category": "Meta",
    },
}


def simple_markdown_to_html(text):
    """Convert markdown to HTML with cross-references."""
    # Escape HTML
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Headers
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Code blocks
    text = re.sub(r'```(\w*)\n(.*?)\n```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Lists
    lines = text.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^- ', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line[2:]}</li>')
        elif re.match(r'^\d+\. ', line):
            if not in_list:
                result.append('<ol>')
                in_list = True
            cleaned = re.sub(r"^\d+\. ", "", line)
            result.append(f'<li>{cleaned}</li>')
        else:
            if in_list:
                result.append('</ul>' if result[-2].startswith('<li>') else '</ol>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    text = '\n'.join(result)

    # Cross-references to other documents
    for doc_name in DOCUMENTS.keys():
        pattern = rf'\b({doc_name}(?:\.md)?)\b'
        replacement = rf'<a href="/docs/{doc_name}" class="doc-link">\1</a>'
        text = re.sub(pattern, replacement, text)

    # Character cross-references
    characters = ["Franklin Blake", "Rachel Verinder", "Betteredge", "Sergeant Cuff",
                  "Rosanna Spearman", "Godfrey Ablewhite", "Ezra Jennings", "Miss Clack",
                  "Matthew Bruff", "Lady Verinder", "Penelope", "Dr. Candy"]
    for char in characters:
        text = re.sub(rf'\b({char})\b', rf'<span class="char-ref">\1</span>', text)

    # Paragraphs
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = f'<p>{text}</p>'
    text = text.replace('<p></p>', '')
    text = text.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
    text = text.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
    text = text.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    text = text.replace('<p><ol>', '<ol>').replace('</ol></p>', '</ol>')
    text = text.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')

    return text


@app.route("/")
def index():
    """Landing page with links to all views."""
    hinge_points = load_hinge_points(GRAPHS_DIR)
    return render_template("index.html", hinge_points=hinge_points[:3])


@app.route("/counterfactual")
def counterfactual():
    """Counterfactual DAG with hinge points."""
    html_content = render_counterfactual_dag(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Counterfactual DAG",
                          question="What if things had gone differently?",
                          description="Shows the actual narrative path alongside branching points where the story could have diverged. Larger nodes are more surprising (lower probability).",
                          legend={
                              "nodes": [
                                  {"color": "#4CAF50", "label": "Actual events"},
                                  {"color": "#ffd700", "label": "Hinge points (pivotal)"},
                                  {"color": "#cccccc", "label": "Counterfactual branches"},
                              ],
                              "edges": [
                                  {"color": "#4CAF50", "label": "Causes", "dashed": False},
                                  {"color": "#999999", "label": "Could have led to", "dashed": False},
                              ]
                          },
                          graph_html=html_content)


@app.route("/causal")
def causal():
    """Causal chain of events."""
    html_content = render_causal_chain(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Causal Chain",
                          question="What caused what? What was inevitable vs. contingent?",
                          description="The backbone of narrative causation — what events necessarily led to others. Required events are structurally essential; contingent events could have gone otherwise.",
                          legend={
                              "nodes": [
                                  {"color": "#2196F3", "label": "Required (structurally essential)"},
                                  {"color": "#90CAF9", "label": "Contingent (could have gone otherwise)"},
                              ],
                              "edges": [
                                  {"color": "#333", "label": "CAUSES (necessary)", "dashed": False},
                                  {"color": "#999", "label": "ENABLES (contingent)", "dashed": True},
                              ]
                          },
                          graph_html=html_content)


@app.route("/knowledge")
def knowledge():
    """Knowledge state graph."""
    html_content = render_knowledge_state(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Knowledge State",
                          question="Who knows what? Whose knowledge is power?",
                          description="A bipartite graph connecting characters to the facts they possess. Drives dramatic irony — readers see the full picture while characters see fragments.",
                          legend={
                              "nodes": [
                                  {"color": "#E91E63", "label": "Characters"},
                                  {"color": "#3F51B5", "label": "Facts / Knowledge"},
                              ],
                              "edges": [
                                  {"color": "#4CAF50", "label": "KNOWS (confirmed)", "dashed": False},
                                  {"color": "#FFC107", "label": "SUSPECTS (uncertain)", "dashed": True},
                              ]
                          },
                          graph_html=html_content)


@app.route("/asymmetry")
def asymmetry():
    """Knowledge asymmetry between characters."""
    html_content = render_knowledge_asymmetry(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Knowledge Asymmetry",
                          question="Who holds secrets? Whose silence shapes the plot?",
                          description="Shows directed power relationships — an edge from A to B means A knows things B doesn't. Thicker edges indicate larger knowledge gaps. Hover to see the exclusive facts.",
                          legend={
                              "nodes": [
                                  {"color": "#E91E63", "label": "Characters"},
                              ],
                              "edges": [
                                  {"color": "#666666", "label": "\"Knows more than\" (thicker = more secrets)", "dashed": False},
                              ]
                          },
                          graph_html=html_content)


@app.route("/locations")
def locations():
    """Location graph."""
    html_content = render_location_graph(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Locations",
                          question="Where could characters be seen or overheard?",
                          description="Spatial constraints that enable or prevent witnesses. The Verinder house geography shapes what's possible — who could have seen what, from where.",
                          legend={
                              "nodes": [
                                  {"color": "#795548", "label": "Building"},
                                  {"color": "#FF9800", "label": "Room"},
                                  {"color": "#4CAF50", "label": "Outdoor"},
                                  {"color": "#9C27B0", "label": "Town/City"},
                                  {"color": "#FFC107", "label": "Feature"},
                              ],
                              "edges": [
                                  {"color": "#333333", "label": "CONTAINS", "dashed": False},
                                  {"color": "#666666", "label": "ADJACENT_TO", "dashed": False},
                                  {"color": "#2196F3", "label": "VISIBLE_FROM / AUDIBLE_FROM", "dashed": True},
                              ]
                          },
                          graph_html=html_content)


@app.route("/secrets")
def secrets():
    """Knowledge asymmetry as a readable list."""
    data = load_knowledge_asymmetry_data(GRAPHS_DIR)
    return render_template("secrets.html",
                          title="Who Knows What Others Don't",
                          question="Whose silence drives the plot?",
                          description="A readable breakdown of knowledge asymmetries. Each row shows what one character knows that another doesn't — the fuel for dramatic irony.",
                          secrets=data["secrets"])


@app.route("/perspectives")
def perspectives():
    """Event-perspective coverage matrix."""
    matrix, narrators, events = load_perspective_matrix(GRAPHS_DIR)
    return render_template("matrix.html",
                          title="Event-Perspective Matrix",
                          question="What does each narrator know firsthand vs. secondhand?",
                          description="Coverage types reveal narrative reliability. Direct witnesses saw it; hearsay is filtered through others; retrospective knowledge came later; inferred knowledge is deduction.",
                          matrix=matrix,
                          narrators=narrators,
                          events=events)


@app.route("/stats")
def stats():
    """Classic NLP statistics."""
    src_dir = Path(__file__).parent.parent / "src"
    all_stats = get_all_stats(src_dir)
    return render_template("stats.html",
                          title="Corpus Statistics",
                          description="Classic NLP metrics. The stuff that wowed em at NeurIPS 2012.",
                          stats=all_stats)


@app.route("/docs")
def docs_index():
    """Document index page."""
    # Group by category
    foundation = {k: v for k, v in DOCUMENTS.items() if v["category"] == "Foundation"}
    meta = {k: v for k, v in DOCUMENTS.items() if v["category"] == "Meta"}
    return render_template("docs_index.html",
                          title="Documents",
                          question="What structures underpin this narrative packet?",
                          description="The foundation documents extracted from The Moonstone, plus meta-documentation about the extraction process.",
                          foundation=foundation,
                          meta=meta)


@app.route("/docs/<doc_name>")
def docs_view(doc_name):
    """View a specific document."""
    if doc_name not in DOCUMENTS:
        return "Document not found", 404

    doc_path = DOCS_DIR / f"{doc_name}.md"
    if not doc_path.exists():
        return "Document file not found", 404

    with open(doc_path) as f:
        content = f.read()

    html_content = simple_markdown_to_html(content)
    doc_info = DOCUMENTS[doc_name]

    # Find related documents based on content
    related = []
    for other_name, other_info in DOCUMENTS.items():
        if other_name != doc_name and other_name in content:
            related.append({"name": other_name, **other_info})

    return render_template("docs_view.html",
                          title=doc_info["title"],
                          question=doc_info["question"],
                          description=doc_info["description"],
                          doc_name=doc_name,
                          content=Markup(html_content),
                          related=related,
                          all_docs=DOCUMENTS)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
