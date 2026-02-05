"""
Causal Chain Graph for The Moonstone

Represents the causal/enabling relationships between events.
Uses both NetworkX (for general graph operations) and pyAgrum (for Bayesian network analysis).

Output formats:
- GraphML, GEXF (standard graph formats)
- BIF (Bayesian Interchange Format for pyAgrum)
- JSON (programmatic access)
"""

import json
import networkx as nx
import pyagrum as gum
from pathlib import Path

# Events in the causal chain
EVENTS = {
    "E01_herncastle_steals": {
        "description": "Colonel Herncastle steals the Moonstone at Seringapatam (1799)",
        "date": "1799-05-04",
        "agent": "Herncastle",
        "necessity": "required"
    },
    "E02_brahmins_pursue": {
        "description": "Brahmins begin generational pursuit of the diamond",
        "date": "1799",
        "agent": "Brahmins",
        "necessity": "required"
    },
    "E03_herncastle_bequeaths": {
        "description": "Herncastle bequeaths diamond to Rachel in his will",
        "date": "1848-early",
        "agent": "Herncastle",
        "necessity": "required"
    },
    "E04_franklin_brings_diamond": {
        "description": "Franklin Blake brings the diamond to the Verinder house",
        "date": "1848-05-25",
        "agent": "Franklin Blake",
        "necessity": "required"
    },
    "E05_birthday_dinner": {
        "description": "Rachel receives the Moonstone at her birthday dinner",
        "date": "1848-06-21",
        "agent": "Rachel Verinder",
        "necessity": "required"
    },
    "E06_candy_drugs_franklin": {
        "description": "Dr. Candy secretly doses Franklin with laudanum",
        "date": "1848-06-21",
        "agent": "Dr. Candy",
        "necessity": "required"
    },
    "E07_franklin_takes_diamond": {
        "description": "Franklin takes the diamond while in laudanum trance",
        "date": "1848-06-21",
        "agent": "Franklin Blake",
        "necessity": "required"
    },
    "E08_rachel_witnesses": {
        "description": "Rachel witnesses Franklin take the diamond",
        "date": "1848-06-21",
        "agent": "Rachel Verinder",
        "necessity": "required"
    },
    "E09_godfrey_steals": {
        "description": "Godfrey takes the diamond from Franklin's room",
        "date": "1848-06-22",
        "agent": "Godfrey Ablewhite",
        "necessity": "required"
    },
    "E10_rosanna_finds_nightgown": {
        "description": "Rosanna discovers Franklin's paint-stained nightgown",
        "date": "1848-06-22",
        "agent": "Rosanna Spearman",
        "necessity": "contingent"
    },
    "E11_rosanna_hides_evidence": {
        "description": "Rosanna hides the nightgown in the Shivering Sand",
        "date": "1848-06-22",
        "agent": "Rosanna Spearman",
        "necessity": "contingent"
    },
    "E12_godfrey_pledges_diamond": {
        "description": "Godfrey pledges the diamond to Mr. Luker",
        "date": "1848-06-23",
        "agent": "Godfrey Ablewhite",
        "necessity": "required"
    },
    "E13_cuff_investigates": {
        "description": "Sergeant Cuff investigates but fails to solve",
        "date": "1848-06-23",
        "agent": "Sergeant Cuff",
        "necessity": "contingent"
    },
    "E14_rachel_silence": {
        "description": "Rachel maintains silence to protect Franklin",
        "date": "1848-06",
        "agent": "Rachel Verinder",
        "necessity": "required"
    },
    "E15_rosanna_suicide": {
        "description": "Rosanna commits suicide at the Shivering Sand",
        "date": "1848-06-26",
        "agent": "Rosanna Spearman",
        "necessity": "contingent"
    },
    "E16_franklin_departs": {
        "description": "Franklin leaves for Europe, confused by Rachel's coldness",
        "date": "1848-06",
        "agent": "Franklin Blake",
        "necessity": "contingent"
    },
    "E17_jennings_reconstructs": {
        "description": "Ezra Jennings reconstructs Dr. Candy's confession",
        "date": "1849-06",
        "agent": "Ezra Jennings",
        "necessity": "required"
    },
    "E18_opium_experiment": {
        "description": "The opium experiment proves Franklin's unconscious action",
        "date": "1849-06-25",
        "agent": "Ezra Jennings",
        "necessity": "required"
    },
    "E19_reconciliation": {
        "description": "Rachel and Franklin reconcile",
        "date": "1849-06",
        "agent": "Rachel Verinder",
        "necessity": "required"
    },
    "E20_godfrey_reclaims": {
        "description": "Godfrey reclaims the diamond from Luker",
        "date": "1849-06-26",
        "agent": "Godfrey Ablewhite",
        "necessity": "required"
    },
    "E21_brahmins_kill_godfrey": {
        "description": "The Brahmins murder Godfrey and recover the diamond",
        "date": "1849-06-27",
        "agent": "Brahmins",
        "necessity": "required"
    },
    "E22_diamond_returns": {
        "description": "The Moonstone is restored to the idol in India",
        "date": "1850",
        "agent": "Brahmins",
        "necessity": "required"
    },
}

# Causal relationships: (source, target, relationship_type, necessity)
# relationship_type: CAUSES (direct), ENABLES (makes possible), PREVENTS (blocks)
CAUSAL_EDGES = [
    ("E01_herncastle_steals", "E02_brahmins_pursue", "CAUSES", "required"),
    ("E01_herncastle_steals", "E03_herncastle_bequeaths", "ENABLES", "required"),
    ("E03_herncastle_bequeaths", "E04_franklin_brings_diamond", "CAUSES", "required"),
    ("E04_franklin_brings_diamond", "E05_birthday_dinner", "ENABLES", "required"),
    ("E05_birthday_dinner", "E06_candy_drugs_franklin", "ENABLES", "contingent"),
    ("E06_candy_drugs_franklin", "E07_franklin_takes_diamond", "CAUSES", "required"),
    ("E07_franklin_takes_diamond", "E08_rachel_witnesses", "ENABLES", "contingent"),
    ("E07_franklin_takes_diamond", "E09_godfrey_steals", "ENABLES", "required"),
    ("E07_franklin_takes_diamond", "E10_rosanna_finds_nightgown", "ENABLES", "contingent"),
    ("E08_rachel_witnesses", "E14_rachel_silence", "CAUSES", "required"),
    ("E09_godfrey_steals", "E12_godfrey_pledges_diamond", "CAUSES", "required"),
    ("E10_rosanna_finds_nightgown", "E11_rosanna_hides_evidence", "CAUSES", "contingent"),
    ("E11_rosanna_hides_evidence", "E15_rosanna_suicide", "ENABLES", "contingent"),
    ("E14_rachel_silence", "E13_cuff_investigates", "ENABLES", "contingent"),  # Her silence stymies investigation
    ("E14_rachel_silence", "E16_franklin_departs", "CAUSES", "contingent"),
    ("E06_candy_drugs_franklin", "E17_jennings_reconstructs", "ENABLES", "required"),  # Candy's illness from that night
    ("E17_jennings_reconstructs", "E18_opium_experiment", "CAUSES", "required"),
    ("E18_opium_experiment", "E19_reconciliation", "CAUSES", "required"),
    ("E12_godfrey_pledges_diamond", "E20_godfrey_reclaims", "ENABLES", "required"),
    ("E02_brahmins_pursue", "E21_brahmins_kill_godfrey", "ENABLES", "required"),
    ("E20_godfrey_reclaims", "E21_brahmins_kill_godfrey", "CAUSES", "required"),
    ("E21_brahmins_kill_godfrey", "E22_diamond_returns", "CAUSES", "required"),
]


def build_causal_networkx():
    """Build NetworkX directed graph of causal relationships."""
    G = nx.DiGraph()

    # Add event nodes
    for event_id, event_data in EVENTS.items():
        G.add_node(event_id,
                   description=event_data["description"],
                   date=event_data["date"],
                   agent=event_data["agent"],
                   necessity=event_data["necessity"])

    # Add causal edges
    for source, target, rel_type, necessity in CAUSAL_EDGES:
        G.add_edge(source, target,
                   relationship=rel_type,
                   necessity=necessity,
                   weight=1.0 if necessity == "required" else 0.5)

    return G


def build_causal_bayesnet():
    """Build pyAgrum Bayesian Network for causal inference."""
    bn = gum.BayesNet("MoonstoneCausalModel")

    # Add binary variables for each event (happened / didn't happen)
    event_vars = {}
    for event_id in EVENTS.keys():
        var = gum.LabelizedVariable(event_id, event_id, 2)
        var.changeLabel(0, "no")
        var.changeLabel(1, "yes")
        event_vars[event_id] = bn.add(var)

    # Add arcs based on causal edges
    for source, target, rel_type, necessity in CAUSAL_EDGES:
        if rel_type in ["CAUSES", "ENABLES"]:
            bn.addArc(event_vars[source], event_vars[target])

    # Set up CPTs (Conditional Probability Tables)
    # For root nodes (no parents): assume they happened
    root_nodes = [n for n in bn.names() if bn.parents(n) == set()]
    for node in root_nodes:
        bn.cpt(node).fillWith([0.01, 0.99])  # 99% probability event happened

    # For nodes with parents: use simple probability model
    for node in bn.names():
        if node in root_nodes:
            continue

        parents = list(bn.parents(node))
        if not parents:
            continue

        # Simple model: if story continues, this event likely happens
        # P(event | all parents happened) = 0.95
        # P(event | any parent didn't happen) = 0.05
        cpt = bn.cpt(node)
        cpt.fillWith(0.05)  # Default: low probability
        # Set high probability when all parents are "yes" (value 1)
        # This is the last entry in the CPT
        cpt.fillWith([0.05, 0.95])  # Simplified: uniform conditioning

    return bn


def analyze_causal_structure(G):
    """Analyze the causal graph structure."""
    analysis = {
        "total_events": G.number_of_nodes(),
        "total_causal_links": G.number_of_edges(),
        "root_events": [n for n, d in G.in_degree() if d == 0],
        "terminal_events": [n for n, d in G.out_degree() if d == 0],
        "critical_path_length": nx.dag_longest_path_length(G) if nx.is_directed_acyclic_graph(G) else None,
        "critical_path": nx.dag_longest_path(G) if nx.is_directed_acyclic_graph(G) else None,
        "bottleneck_events": [],  # Events that all paths pass through
        "contingent_events": [n for n, d in G.nodes(data=True) if d.get("necessity") == "contingent"],
        "required_events": [n for n, d in G.nodes(data=True) if d.get("necessity") == "required"],
    }

    # Find bottleneck events (high betweenness centrality)
    centrality = nx.betweenness_centrality(G)
    bottlenecks = sorted(
        [(n, c) for n, c in centrality.items() if c > 0.1],
        key=lambda x: x[1],
        reverse=True
    )
    analysis["bottleneck_events"] = [{"event": n, "centrality": c} for n, c in bottlenecks]

    return analysis


def export_graphs(output_dir: Path):
    """Export all causal chain representations."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build NetworkX graph
    causal_graph = build_causal_networkx()

    # Export NetworkX formats
    nx.write_graphml(causal_graph, output_dir / "causal_chain.graphml")
    nx.write_gexf(causal_graph, output_dir / "causal_chain.gexf")

    # Export JSON
    causal_json = nx.node_link_data(causal_graph)
    with open(output_dir / "causal_chain.json", "w") as f:
        json.dump(causal_json, f, indent=2)

    # Build and export Bayesian Network
    try:
        bn = build_causal_bayesnet()
        gum.saveBN(bn, str(output_dir / "causal_chain.bif"))
        gum.saveBN(bn, str(output_dir / "causal_chain.bifxml"))
        print(f"Bayesian Network: {bn.size()} nodes, {bn.sizeArcs()} arcs")
    except Exception as e:
        print(f"Warning: Could not build Bayesian Network: {e}")

    # Export raw data
    with open(output_dir / "causal_data.json", "w") as f:
        json.dump({
            "events": EVENTS,
            "causal_edges": CAUSAL_EDGES
        }, f, indent=2)

    # Analyze and export analysis
    analysis = analyze_causal_structure(causal_graph)
    with open(output_dir / "causal_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2, default=str)

    print(f"Causal Chain Graph: {causal_graph.number_of_nodes()} nodes, {causal_graph.number_of_edges()} edges")
    print(f"Critical path length: {analysis['critical_path_length']}")
    print(f"Bottleneck events: {[e['event'] for e in analysis['bottleneck_events'][:3]]}")

    return causal_graph


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_graphs(output_dir)
    print(f"\nCausal chain graphs exported to {output_dir}")
