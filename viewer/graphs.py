"""
Graph loading and rendering for the viewer.
"""

import json
import networkx as nx
from pyvis.network import Network
from pathlib import Path


def load_hinge_points(graphs_dir: Path) -> list:
    """Load hinge points data."""
    with open(graphs_dir / "hinge_points.json") as f:
        return json.load(f)


def load_perspective_matrix(graphs_dir: Path):
    """Load the event-perspective matrix."""
    with open(graphs_dir / "event_perspective_matrix.json") as f:
        data = json.load(f)
    return data["matrix"], data["narrators"], data["events"]


def render_counterfactual_dag(graphs_dir: Path) -> str:
    """Render the counterfactual DAG with PyVis."""
    G = nx.read_graphml(graphs_dir / "counterfactual_dag.graphml")

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#000000",
    )
    net.barnes_hut(gravity=-3000, spring_length=150)

    # Add nodes with styling based on attributes
    for node_id, data in G.nodes(data=True):
        node_type = data.get("node_type", "event")
        actual = data.get("actual", "True") == "True"
        hinge = data.get("hinge", "False") == "True"
        p_actual = float(data.get("p_actual", 0.5))

        # Color based on type and status
        if node_type == "counterfactual":
            color = "#cccccc"  # Gray for counterfactuals
        elif hinge:
            color = "#ffd700"  # Gold for hinge points
        elif actual:
            color = "#4CAF50"  # Green for actual path
        else:
            color = "#9e9e9e"  # Gray

        # Size based on probability (lower = bigger = more surprising)
        if node_type != "condition":
            size = 15 + (1 - p_actual) * 25
        else:
            size = 12

        # Label
        desc = data.get("description", node_id)
        label = desc[:30] + "..." if len(desc) > 30 else desc

        net.add_node(
            node_id,
            label=label,
            title=f"{desc}\nP(actual)={p_actual:.2f}" if p_actual else desc,
            color=color,
            size=size,
            shape="dot" if node_type == "condition" else "box",
        )

    # Add edges
    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")
        color = "#4CAF50" if rel == "causes" else "#999999"
        net.add_edge(source, target, color=color, arrows="to")

    # Generate HTML
    html = net.generate_html()
    # Extract just the body content
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html


def render_causal_chain(graphs_dir: Path) -> str:
    """Render the causal chain graph."""
    G = nx.read_graphml(graphs_dir / "causal_chain.graphml")

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#000000",
    )
    net.barnes_hut(gravity=-2000, spring_length=200)

    for node_id, data in G.nodes(data=True):
        desc = data.get("description", node_id)
        necessity = data.get("necessity", "required")

        color = "#2196F3" if necessity == "required" else "#90CAF9"
        label = desc[:25] + "..." if len(desc) > 25 else desc

        net.add_node(
            node_id,
            label=label,
            title=desc,
            color=color,
            size=20,
            shape="box",
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")
        style = "solid" if rel == "CAUSES" else "dashed"
        net.add_edge(source, target, arrows="to", dashes=(style == "dashed"))

    html = net.generate_html()
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html


def render_knowledge_state(graphs_dir: Path) -> str:
    """Render the knowledge state bipartite graph."""
    G = nx.read_graphml(graphs_dir / "knowledge_state.graphml")

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#000000",
    )
    net.barnes_hut(gravity=-1500, spring_length=250)

    for node_id, data in G.nodes(data=True):
        node_type = data.get("node_type", "")
        label = data.get("label", node_id)

        if node_type == "character":
            color = "#E91E63"  # Pink for characters
            size = 25
            shape = "dot"
            # Clean up label
            label = label.replace("_", " ").title()
        else:
            color = "#3F51B5"  # Blue for facts
            size = 18
            shape = "box"
            # Clean up fact labels
            label = label.replace("_", " ").replace("fact:", "")

        net.add_node(
            node_id,
            label=label,
            title=data.get("description", label),
            color=color,
            size=size,
            shape=shape,
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "KNOWS")
        color = "#4CAF50" if rel == "KNOWS" else "#FFC107"
        dashes = rel == "SUSPECTS"
        net.add_edge(source, target, color=color, arrows="to", dashes=dashes)

    html = net.generate_html()
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html


def render_knowledge_asymmetry(graphs_dir: Path) -> str:
    """Render the knowledge asymmetry graph."""
    G = nx.read_graphml(graphs_dir / "knowledge_asymmetry.graphml")

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#000000",
    )
    net.barnes_hut(gravity=-2000, spring_length=200)

    for node_id, data in G.nodes(data=True):
        label = data.get("label", node_id).replace("_", " ").title()
        net.add_node(
            node_id,
            label=label,
            color="#E91E63",
            size=30,
            shape="dot",
        )

    for source, target, data in G.edges(data=True):
        count = int(data.get("count", 1))
        facts = data.get("exclusive_facts", "")

        # Width based on count
        width = 1 + count * 0.5

        net.add_edge(
            source, target,
            width=width,
            title=f"{count} exclusive facts: {facts}",
            arrows="to",
            color="#666666",
        )

    html = net.generate_html()
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html


def render_location_graph(graphs_dir: Path) -> str:
    """Render the location graph."""
    G = nx.read_graphml(graphs_dir / "location_graph.graphml")

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#000000",
    )
    net.barnes_hut(gravity=-1500, spring_length=150)

    # Color by location type
    type_colors = {
        "building": "#795548",
        "room": "#FF9800",
        "outdoor": "#4CAF50",
        "town": "#9C27B0",
        "city": "#9C27B0",
        "country": "#673AB7",
        "village": "#8BC34A",
        "feature": "#FFC107",
        "passage": "#FFEB3B",
    }

    for node_id, data in G.nodes(data=True):
        loc_type = data.get("location_type", "room")
        desc = data.get("description", node_id)

        color = type_colors.get(loc_type, "#999999")
        label = node_id.replace("_", " ").title()

        net.add_node(
            node_id,
            label=label,
            title=desc,
            color=color,
            size=20,
            shape="box",
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")

        if rel == "CONTAINS":
            color = "#333333"
            dashes = False
        elif rel == "ADJACENT_TO":
            color = "#666666"
            dashes = False
        elif rel in ["VISIBLE_FROM", "AUDIBLE_FROM"]:
            color = "#2196F3"
            dashes = True
        else:
            color = "#999999"
            dashes = False

        net.add_edge(source, target, color=color, dashes=dashes, arrows="to")

    html = net.generate_html()
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html
