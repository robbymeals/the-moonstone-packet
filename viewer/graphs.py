"""
Graph loading and rendering for the viewer.
"""

import json
import networkx as nx
from pyvis.network import Network
from pathlib import Path


def load_knowledge_asymmetry_data(graphs_dir: Path) -> dict:
    """Load knowledge asymmetry as structured data for table view."""
    G = nx.read_graphml(graphs_dir / "knowledge_asymmetry.graphml")

    # Build character list and their secrets
    characters = []
    for node_id, data in G.nodes(data=True):
        label = data.get("label", node_id).replace("_", " ").title()
        characters.append({"id": node_id, "name": label})

    # Build secrets list
    secrets = []
    for source, target, data in G.edges(data=True):
        count = int(data.get("count", 1))
        facts = data.get("exclusive_facts", "")
        fact_list = [f.strip() for f in facts.split(",") if f.strip()]

        source_name = source.replace("_", " ").title()
        target_name = target.replace("_", " ").title()

        secrets.append({
            "holder": source_name,
            "ignorant": target_name,
            "count": count,
            "facts": fact_list,
        })

    # Sort by count descending
    secrets.sort(key=lambda x: x["count"], reverse=True)

    return {"characters": characters, "secrets": secrets}


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

        # Rich tooltip
        tooltip_lines = [f"<b>{desc}</b>"]
        if node_type == "counterfactual":
            tooltip_lines.append("<i>Counterfactual branch — this didn't happen</i>")
        elif hinge:
            tooltip_lines.append("<i>Hinge point — the story pivots here</i>")
            tooltip_lines.append(f"Probability: {p_actual:.0%} (lower = more surprising)")
        elif p_actual and p_actual < 1.0:
            tooltip_lines.append(f"Probability: {p_actual:.0%}")
        tooltip = "<br>".join(tooltip_lines)

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color=color,
            size=size,
            shape="dot" if node_type == "condition" else "box",
        )

    # Add edges
    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")
        color = "#4CAF50" if rel == "causes" else "#999999"
        edge_label = "directly causes" if rel == "causes" else "could have led to"
        net.add_edge(source, target, color=color, arrows="to", title=edge_label)

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

        # Rich tooltip
        tooltip = f"<b>{desc}</b><br>"
        if necessity == "required":
            tooltip += "<i>Required event — structurally essential to the plot</i>"
        else:
            tooltip += "<i>Contingent event — could have gone otherwise</i>"

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color=color,
            size=20,
            shape="box",
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")
        style = "solid" if rel == "CAUSES" else "dashed"
        edge_tooltip = "CAUSES — necessary consequence" if rel == "CAUSES" else "ENABLES — makes possible but not inevitable"
        net.add_edge(source, target, arrows="to", dashes=(style == "dashed"), title=edge_tooltip)

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
        desc = data.get("description", "")

        if node_type == "character":
            color = "#E91E63"  # Pink for characters
            size = 25
            shape = "dot"
            clean_label = label.replace("_", " ").title()
            tooltip = f"<b>{clean_label}</b><br><i>Character node</i>"
        else:
            color = "#3F51B5"  # Blue for facts
            size = 18
            shape = "box"
            clean_label = label.replace("_", " ").replace("fact:", "")
            tooltip = f"<b>{clean_label}</b><br>{desc}" if desc else f"<b>{clean_label}</b><br><i>A piece of knowledge in the story</i>"

        net.add_node(
            node_id,
            label=clean_label,
            title=tooltip,
            color=color,
            size=size,
            shape=shape,
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "KNOWS")
        color = "#4CAF50" if rel == "KNOWS" else "#FFC107"
        dashes = rel == "SUSPECTS"
        edge_tooltip = "KNOWS — confirmed knowledge" if rel == "KNOWS" else "SUSPECTS — uncertain belief"
        net.add_edge(source, target, color=color, arrows="to", dashes=dashes, title=edge_tooltip)

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
    net.barnes_hut(gravity=-3000, spring_length=250)

    # Calculate in/out degree to size nodes by knowledge power
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    for node_id, data in G.nodes(data=True):
        label = data.get("label", node_id).replace("_", " ").title()
        # Larger nodes have more secrets (higher out-degree)
        secrets_held = out_degree.get(node_id, 0)
        size = 25 + secrets_held * 3

        tooltip = f"<b>{label}</b><br>"
        tooltip += f"Holds secrets over {secrets_held} others<br>"
        tooltip += f"Others hold secrets over them: {in_degree.get(node_id, 0)}"

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color="#E91E63",
            size=size,
            shape="dot",
        )

    for source, target, data in G.edges(data=True):
        count = int(data.get("count", 1))
        facts = data.get("exclusive_facts", "")

        # Width based on count
        width = 1 + count * 1.5

        # Parse facts for better display
        fact_list = [f.strip() for f in facts.split(",") if f.strip()]
        fact_display = "<br>• ".join(fact_list) if fact_list else "unknown"

        source_name = source.replace("_", " ").title()
        target_name = target.replace("_", " ").title()

        tooltip = f"<b>{source_name}</b> knows {count} thing(s)<br>"
        tooltip += f"that <b>{target_name}</b> doesn't:<br>• {fact_display}"

        net.add_edge(
            source, target,
            width=width,
            title=tooltip,
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

        tooltip = f"<b>{label}</b><br>"
        tooltip += f"<i>Type: {loc_type}</i><br>"
        if desc and desc != node_id:
            tooltip += desc

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color=color,
            size=20,
            shape="box",
        )

    for source, target, data in G.edges(data=True):
        rel = data.get("relationship", "")

        if rel == "CONTAINS":
            color = "#333333"
            dashes = False
            edge_tooltip = f"CONTAINS — {source.replace('_', ' ')} contains {target.replace('_', ' ')}"
        elif rel == "ADJACENT_TO":
            color = "#666666"
            dashes = False
            edge_tooltip = f"ADJACENT — physically next to each other"
        elif rel == "VISIBLE_FROM":
            color = "#2196F3"
            dashes = True
            edge_tooltip = f"VISIBLE FROM — can see into from here"
        elif rel == "AUDIBLE_FROM":
            color = "#2196F3"
            dashes = True
            edge_tooltip = f"AUDIBLE FROM — can hear from here"
        else:
            color = "#999999"
            dashes = False
            edge_tooltip = rel

        net.add_edge(source, target, color=color, dashes=dashes, arrows="to", title=edge_tooltip)

    html = net.generate_html()
    start = html.find('<div id="mynetwork"')
    end = html.find('</body>')
    return html[start:end] if start > 0 else html
