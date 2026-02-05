"""
Moonstone Graph Viewer

Minimal Flask app for viewing narrative structure graphs.
"""

from flask import Flask, render_template, send_from_directory
from pathlib import Path
import json

from graphs import (
    render_counterfactual_dag,
    render_causal_chain,
    render_knowledge_state,
    render_knowledge_asymmetry,
    render_location_graph,
    load_perspective_matrix,
    load_hinge_points,
)

app = Flask(__name__)

GRAPHS_DIR = Path(__file__).parent.parent / "graphs"


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
                          description="Actual narrative path (green) vs counterfactual branches (gray). Yellow = hinge points.",
                          graph_html=html_content)


@app.route("/causal")
def causal():
    """Causal chain of events."""
    html_content = render_causal_chain(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Causal Chain",
                          description="Event causation. Darker = required, lighter = contingent.",
                          graph_html=html_content)


@app.route("/knowledge")
def knowledge():
    """Knowledge state graph."""
    html_content = render_knowledge_state(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Knowledge State",
                          description="Who knows what. Characters (left) → Facts (right).",
                          graph_html=html_content)


@app.route("/asymmetry")
def asymmetry():
    """Knowledge asymmetry between characters."""
    html_content = render_knowledge_asymmetry(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Knowledge Asymmetry",
                          description="Who knows more than whom. Thicker edge = more exclusive knowledge.",
                          graph_html=html_content)


@app.route("/locations")
def locations():
    """Location graph."""
    html_content = render_location_graph(GRAPHS_DIR)
    return render_template("graph.html",
                          title="Locations",
                          description="Spatial relationships. Contains, adjacent, visible/audible from.",
                          graph_html=html_content)


@app.route("/perspectives")
def perspectives():
    """Event-perspective coverage matrix."""
    matrix, narrators, events = load_perspective_matrix(GRAPHS_DIR)
    return render_template("matrix.html",
                          title="Event-Perspective Matrix",
                          description="Which narrators cover which events, and how.",
                          matrix=matrix,
                          narrators=narrators,
                          events=events)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
