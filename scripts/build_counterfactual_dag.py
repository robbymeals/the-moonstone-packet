"""
Counterfactual DAG for The Moonstone

A DAG structure where:
1. The spine is what actually happened
2. Hinge points branch to counterfactual possibilities
3. Multiple causes can converge on outcomes
4. We can reason about "what if X didn't happen"

For pyAgrum Bayesian Network inference.
"""

import json
import pyagrum as gum
import networkx as nx
from pathlib import Path

# The narrative DAG
# Each node is a state/event
# Edges represent causal/enabling relationships
# The "actual" path is marked

NODES = {
    # === SETUP CONDITIONS (background) ===
    "herncastle_corrupt": {
        "desc": "Herncastle is morally corrupt",
        "type": "condition",
        "actual": True,
    },
    "diamond_exists": {
        "desc": "The Moonstone exists at Seringapatam",
        "type": "condition",
        "actual": True,
    },
    "siege_happens": {
        "desc": "Siege of Seringapatam occurs",
        "type": "condition",
        "actual": True,
    },

    # === PROLOGUE EVENTS ===
    "herncastle_steals": {
        "desc": "Herncastle steals the diamond",
        "type": "event",
        "actual": True,
        "hinge": False,  # Required for story
    },
    "brahmins_pursue": {
        "desc": "Brahmins begin pursuing the diamond",
        "type": "event",
        "actual": True,
        "hinge": False,
    },

    # === BEQUEST ===
    "herncastle_vindictive": {
        "desc": "Herncastle is bitter/vindictive toward family",
        "type": "condition",
        "actual": True,
    },
    "bequeaths_to_rachel": {
        "desc": "Herncastle leaves diamond to Rachel",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Could have disposed differently
        "alternatives": ["destroyed", "sold", "museum", "buried"],
    },

    # === BIRTHDAY SETUP ===
    "franklin_brings": {
        "desc": "Franklin brings diamond to Verinder house",
        "type": "event",
        "actual": True,
        "hinge": False,
    },
    "birthday_dinner": {
        "desc": "Birthday dinner occurs",
        "type": "event",
        "actual": True,
        "hinge": False,
    },
    "candy_offended": {
        "desc": "Dr. Candy is offended by Franklin's remarks",
        "type": "condition",
        "actual": True,
    },
    "candy_has_laudanum": {
        "desc": "Dr. Candy has access to laudanum",
        "type": "condition",
        "actual": True,
    },

    # === THE KEY HINGE ===
    "candy_doses_franklin": {
        "desc": "Dr. Candy secretly doses Franklin with laudanum",
        "type": "event",
        "actual": True,
        "hinge": True,  # MAJOR HINGE: This is the twist
        "p_actual": 0.15,  # Very unlikely
        "alternatives": ["candy_does_nothing", "candy_confronts_directly"],
    },
    "candy_does_nothing": {
        "desc": "Dr. Candy lets the insult go",
        "type": "counterfactual",
        "actual": False,
    },

    # === NIGHT EVENTS ===
    "franklin_drugged": {
        "desc": "Franklin is under laudanum influence",
        "type": "state",
        "actual": True,
    },
    "franklin_anxious": {
        "desc": "Franklin is anxious about diamond security",
        "type": "condition",
        "actual": True,
    },
    "franklin_takes_diamond": {
        "desc": "Franklin takes diamond in trance",
        "type": "event",
        "actual": True,
        "hinge": False,  # Follows from drugging + anxiety
        "p_actual_given_drugged": 0.7,
    },
    "franklin_sleeps_normally": {
        "desc": "Franklin sleeps through the night normally",
        "type": "counterfactual",
        "actual": False,
    },

    # === WITNESSES ===
    "rachel_awake": {
        "desc": "Rachel is awake and watching",
        "type": "condition",
        "actual": True,
    },
    "rachel_witnesses": {
        "desc": "Rachel sees Franklin take the diamond",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Could have been asleep
        "p_actual": 0.3,  # Unlikely she'd be watching at that moment
    },
    "rachel_asleep": {
        "desc": "Rachel is asleep, doesn't witness",
        "type": "counterfactual",
        "actual": False,
    },

    # === GODFREY'S OPPORTUNITY ===
    "godfrey_awake": {
        "desc": "Godfrey is awake in the night",
        "type": "condition",
        "actual": True,
    },
    "godfrey_desperate": {
        "desc": "Godfrey is financially desperate (embezzlement)",
        "type": "condition",
        "actual": True,
    },
    "godfrey_sees_opportunity": {
        "desc": "Godfrey observes Franklin with diamond",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Requires being in right place
    },
    "godfrey_steals": {
        "desc": "Godfrey takes diamond from unconscious Franklin",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Could have moral qualm
        "p_actual": 0.6,  # Given opportunity + desperation
    },
    "godfrey_doesnt_steal": {
        "desc": "Godfrey doesn't take the opportunity",
        "type": "counterfactual",
        "actual": False,
    },

    # === RACHEL'S CHOICE ===
    "rachel_loves_franklin": {
        "desc": "Rachel loves Franklin",
        "type": "condition",
        "actual": True,
    },
    "rachel_silent": {
        "desc": "Rachel maintains silence to protect Franklin",
        "type": "event",
        "actual": True,
        "hinge": False,  # Character-driven, very likely
        "p_actual": 0.85,
    },
    "rachel_tells": {
        "desc": "Rachel tells someone what she saw",
        "type": "counterfactual",
        "actual": False,
    },

    # === ROSANNA'S PATH ===
    "rosanna_finds_nightgown": {
        "desc": "Rosanna discovers the stained nightgown",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: She had to be doing laundry
    },
    "rosanna_loves_franklin": {
        "desc": "Rosanna is in love with Franklin",
        "type": "condition",
        "actual": True,
    },
    "rosanna_hides_evidence": {
        "desc": "Rosanna hides the nightgown",
        "type": "event",
        "actual": True,
        "hinge": False,  # Character-driven
    },
    "rosanna_reports": {
        "desc": "Rosanna reports what she found",
        "type": "counterfactual",
        "actual": False,
    },
    "rosanna_suicide": {
        "desc": "Rosanna commits suicide",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Tragic but contingent
        "p_actual": 0.4,
    },

    # === INVESTIGATION ===
    "cuff_investigates": {
        "desc": "Sergeant Cuff investigates",
        "type": "event",
        "actual": True,
        "hinge": False,
    },
    "investigation_stalls": {
        "desc": "Investigation stalls due to Rachel's silence",
        "type": "event",
        "actual": True,
        "hinge": False,  # Follows from Rachel's silence
    },

    # === RESOLUTION PATH ===
    "candy_ill": {
        "desc": "Dr. Candy falls ill with brain fever",
        "type": "event",
        "actual": True,
        "hinge": True,  # Required for Jennings discovery
    },
    "jennings_records_ravings": {
        "desc": "Jennings records Candy's fever-ravings",
        "type": "event",
        "actual": True,
        "hinge": True,  # HINGE: Could have dismissed them
    },
    "jennings_reconstructs": {
        "desc": "Jennings reconstructs the truth about laudanum",
        "type": "event",
        "actual": True,
        "hinge": True,  # MAJOR HINGE: The detective work
        "p_actual": 0.25,  # Unlikely chain
    },
    "truth_never_discovered": {
        "desc": "The truth is never discovered",
        "type": "counterfactual",
        "actual": False,
    },
    "opium_experiment": {
        "desc": "The opium experiment proves Franklin's innocence",
        "type": "event",
        "actual": True,
        "hinge": False,  # Follows from Jennings' discovery
    },
    "reconciliation": {
        "desc": "Rachel and Franklin reconcile",
        "type": "event",
        "actual": True,
        "hinge": False,
    },

    # === GODFREY'S FATE ===
    "godfrey_reclaims": {
        "desc": "Godfrey reclaims diamond from Luker",
        "type": "event",
        "actual": True,
        "hinge": False,  # He's trapped
    },
    "brahmins_track": {
        "desc": "Brahmins track the diamond to Godfrey",
        "type": "event",
        "actual": True,
        "hinge": False,  # Their purpose
    },
    "godfrey_murdered": {
        "desc": "Brahmins kill Godfrey, recover diamond",
        "type": "event",
        "actual": True,
        "hinge": False,  # Nearly inevitable
    },
    "diamond_returns": {
        "desc": "Diamond returned to India",
        "type": "event",
        "actual": True,
        "hinge": False,  # Narrative closure
    },
}

# Causal/enabling edges (source, target, type)
EDGES = [
    # Prologue
    ("herncastle_corrupt", "herncastle_steals", "enables"),
    ("diamond_exists", "herncastle_steals", "enables"),
    ("siege_happens", "herncastle_steals", "enables"),
    ("herncastle_steals", "brahmins_pursue", "causes"),

    # Bequest
    ("herncastle_steals", "bequeaths_to_rachel", "enables"),
    ("herncastle_vindictive", "bequeaths_to_rachel", "enables"),
    ("bequeaths_to_rachel", "franklin_brings", "causes"),

    # Birthday
    ("franklin_brings", "birthday_dinner", "enables"),
    ("birthday_dinner", "candy_offended", "causes"),

    # The Key Hinge
    ("candy_offended", "candy_doses_franklin", "enables"),
    ("candy_has_laudanum", "candy_doses_franklin", "enables"),
    ("candy_offended", "candy_does_nothing", "enables"),  # Counterfactual branch

    # Night events
    ("candy_doses_franklin", "franklin_drugged", "causes"),
    ("franklin_drugged", "franklin_takes_diamond", "enables"),
    ("franklin_anxious", "franklin_takes_diamond", "enables"),
    ("candy_does_nothing", "franklin_sleeps_normally", "causes"),  # Counterfactual

    # Witnesses
    ("franklin_takes_diamond", "rachel_witnesses", "enables"),
    ("rachel_awake", "rachel_witnesses", "enables"),
    ("franklin_takes_diamond", "rachel_asleep", "enables"),  # Counterfactual

    # Godfrey
    ("franklin_takes_diamond", "godfrey_sees_opportunity", "enables"),
    ("godfrey_awake", "godfrey_sees_opportunity", "enables"),
    ("godfrey_sees_opportunity", "godfrey_steals", "enables"),
    ("godfrey_desperate", "godfrey_steals", "enables"),
    ("godfrey_sees_opportunity", "godfrey_doesnt_steal", "enables"),  # Counterfactual

    # Rachel's choice
    ("rachel_witnesses", "rachel_silent", "enables"),
    ("rachel_loves_franklin", "rachel_silent", "enables"),
    ("rachel_witnesses", "rachel_tells", "enables"),  # Counterfactual

    # Rosanna
    ("franklin_takes_diamond", "rosanna_finds_nightgown", "enables"),
    ("rosanna_finds_nightgown", "rosanna_hides_evidence", "enables"),
    ("rosanna_loves_franklin", "rosanna_hides_evidence", "enables"),
    ("rosanna_finds_nightgown", "rosanna_reports", "enables"),  # Counterfactual
    ("rosanna_hides_evidence", "rosanna_suicide", "enables"),

    # Investigation
    ("godfrey_steals", "cuff_investigates", "enables"),
    ("rachel_silent", "investigation_stalls", "causes"),
    ("rosanna_hides_evidence", "investigation_stalls", "enables"),

    # Resolution
    ("candy_doses_franklin", "candy_ill", "enables"),  # Got sick riding home
    ("candy_ill", "jennings_records_ravings", "enables"),
    ("jennings_records_ravings", "jennings_reconstructs", "enables"),
    ("investigation_stalls", "jennings_reconstructs", "enables"),  # Need for truth
    ("investigation_stalls", "truth_never_discovered", "enables"),  # Counterfactual
    ("jennings_reconstructs", "opium_experiment", "causes"),
    ("opium_experiment", "reconciliation", "causes"),

    # Godfrey's fate
    ("godfrey_steals", "godfrey_reclaims", "enables"),
    ("brahmins_pursue", "brahmins_track", "enables"),
    ("godfrey_reclaims", "brahmins_track", "enables"),
    ("brahmins_track", "godfrey_murdered", "causes"),
    ("godfrey_murdered", "diamond_returns", "causes"),
]


def build_dag():
    """Build the counterfactual DAG."""
    G = nx.DiGraph()

    # Add nodes
    for node_id, data in NODES.items():
        G.add_node(node_id,
                   description=data["desc"],
                   node_type=data["type"],
                   actual=str(data["actual"]),
                   hinge=str(data.get("hinge", False)),
                   p_actual=data.get("p_actual", 0.5))

    # Add edges
    for source, target, edge_type in EDGES:
        G.add_edge(source, target, relationship=edge_type)

    return G


def build_bayesian_network():
    """Build pyAgrum Bayesian Network from the DAG."""
    bn = gum.BayesNet("MoonstoneCounterfactual")

    # Only add actual nodes (not counterfactuals) for the main model
    actual_nodes = {k: v for k, v in NODES.items() if v["actual"]}

    # Add variables
    var_ids = {}
    for node_id, data in actual_nodes.items():
        var = gum.LabelizedVariable(node_id, data["desc"][:40], 2)
        var.changeLabel(0, "false")
        var.changeLabel(1, "true")
        var_ids[node_id] = bn.add(var)

    # Add arcs (only between actual nodes)
    for source, target, _ in EDGES:
        if source in var_ids and target in var_ids:
            try:
                bn.addArc(var_ids[source], var_ids[target])
            except gum.InvalidDirectedCycle:
                pass  # Skip if would create cycle

    # Set CPTs
    for node_id, data in actual_nodes.items():
        node = var_ids[node_id]
        parents = bn.parents(node)

        if not parents:
            # Root node - conditions are typically true for the story
            if data["type"] == "condition":
                bn.cpt(node_id).fillWith([0.1, 0.9])  # Conditions usually true
            else:
                p = data.get("p_actual", 0.5)
                bn.cpt(node_id).fillWith([1-p, p])
        else:
            # Node with parents - simplified model
            # High probability if all parents true, low otherwise
            cpt = bn.cpt(node_id)
            p = data.get("p_actual", 0.8)
            # Fill with low probability, override for "all parents true" case
            cpt.fillWith([1-p*0.1, p*0.1])

    return bn


def identify_hinge_points():
    """Identify the key hinge points in the narrative."""
    hinges = []
    for node_id, data in NODES.items():
        if data.get("hinge"):
            hinges.append({
                "node": node_id,
                "description": data["desc"],
                "p_actual": data.get("p_actual", 0.5),
                "alternatives": data.get("alternatives", []),
                "counterfactual_branch": [k for k, v in NODES.items()
                                          if v["type"] == "counterfactual"
                                          and node_id in k]
            })
    return sorted(hinges, key=lambda x: x.get("p_actual", 0.5))


def compute_narrative_metrics(G):
    """Compute metrics about the narrative structure."""
    actual_path = [n for n, d in G.nodes(data=True) if d.get("actual") == "True"]
    counterfactual_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "counterfactual"]
    hinge_nodes = [n for n, d in G.nodes(data=True) if d.get("hinge") == "True"]

    # Chain probability of actual path
    p_chain = 1.0
    for node in actual_path:
        data = G.nodes[node]
        if "p_actual" in data:
            p_chain *= data["p_actual"]

    return {
        "total_nodes": G.number_of_nodes(),
        "actual_path_nodes": len(actual_path),
        "counterfactual_nodes": len(counterfactual_nodes),
        "hinge_points": len(hinge_nodes),
        "total_edges": G.number_of_edges(),
        "chain_probability": p_chain,
        "hinge_point_list": hinge_nodes,
    }


def export_model(output_dir: Path):
    """Export the counterfactual DAG model."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build DAG
    G = build_dag()

    # Export graph formats
    nx.write_graphml(G, output_dir / "counterfactual_dag.graphml")
    nx.write_gexf(G, output_dir / "counterfactual_dag.gexf")

    # Export JSON
    graph_json = nx.node_link_data(G)
    with open(output_dir / "counterfactual_dag.json", "w") as f:
        json.dump(graph_json, f, indent=2)

    # Export raw data
    with open(output_dir / "counterfactual_data.json", "w") as f:
        json.dump({
            "nodes": NODES,
            "edges": EDGES,
        }, f, indent=2)

    # Build and export Bayesian Network
    try:
        bn = build_bayesian_network()
        gum.saveBN(bn, str(output_dir / "counterfactual.bif"))
        print(f"Bayesian Network: {bn.size()} nodes, {bn.sizeArcs()} arcs")
    except Exception as e:
        print(f"Warning: Bayesian Network issue: {e}")

    # Identify hinge points
    hinges = identify_hinge_points()
    with open(output_dir / "hinge_points.json", "w") as f:
        json.dump(hinges, f, indent=2)

    # Compute metrics
    metrics = compute_narrative_metrics(G)
    with open(output_dir / "counterfactual_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nCounterfactual DAG: {metrics['total_nodes']} nodes, {metrics['total_edges']} edges")
    print(f"Hinge points: {metrics['hinge_points']}")
    print(f"Counterfactual branches: {metrics['counterfactual_nodes']}")
    print(f"\nMost contingent hinges (lowest P):")
    for h in hinges[:3]:
        print(f"  - {h['description']} (P={h['p_actual']})")

    return G, hinges


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_model(output_dir)
    print(f"\nCounterfactual DAG exported to {output_dir}")
