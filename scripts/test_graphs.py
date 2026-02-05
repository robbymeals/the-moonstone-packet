#!/usr/bin/env python3
"""
Test script to load and inspect the Moonstone narrative graphs.

Usage:
    poetry run python scripts/test_graphs.py
"""

import json
import networkx as nx
from pathlib import Path

try:
    import pyagrum as gum
    PYAGRUM_AVAILABLE = True
except ImportError:
    PYAGRUM_AVAILABLE = False


def test_networkx_graphs(graphs_dir: Path):
    """Test loading NetworkX graphs."""
    print("=" * 60)
    print("NETWORKX GRAPH TESTS")
    print("=" * 60)

    graph_files = [
        "knowledge_state.graphml",
        "knowledge_asymmetry.graphml",
        "causal_chain.graphml",
        "event_perspective_bipartite.graphml",
        "location_graph.graphml",
        "state_transitions.graphml",
        "counterfactual_dag.graphml",
    ]

    for gf in graph_files:
        path = graphs_dir / gf
        if path.exists():
            G = nx.read_graphml(path)
            print(f"\n{gf}:")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            print(f"  Is DAG: {nx.is_directed_acyclic_graph(G) if isinstance(G, nx.DiGraph) else 'N/A'}")

            # Sample nodes
            nodes = list(G.nodes(data=True))[:3]
            print(f"  Sample nodes: {[n[0] for n in nodes]}")
        else:
            print(f"\n{gf}: NOT FOUND")


def test_json_data(graphs_dir: Path):
    """Test loading JSON data files."""
    print("\n" + "=" * 60)
    print("JSON DATA TESTS")
    print("=" * 60)

    json_files = [
        "knowledge_data.json",
        "causal_data.json",
        "event_perspective_matrix.json",
        "hinge_points.json",
        "counterfactual_metrics.json",
        "voice_fingerprints.json",
    ]

    for jf in json_files:
        path = graphs_dir / jf
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            print(f"\n{jf}:")
            if isinstance(data, dict):
                print(f"  Keys: {list(data.keys())[:5]}")
            elif isinstance(data, list):
                print(f"  Items: {len(data)}")
        else:
            print(f"\n{jf}: NOT FOUND")


def test_pyagrum_networks(graphs_dir: Path):
    """Test loading pyAgrum Bayesian Networks."""
    print("\n" + "=" * 60)
    print("PYAGRUM BAYESIAN NETWORK TESTS")
    print("=" * 60)

    if not PYAGRUM_AVAILABLE:
        print("pyAgrum not available")
        return

    bif_files = [
        "causal_chain.bif",
        "state_transitions.bif",
        "counterfactual.bif",
    ]

    for bf in bif_files:
        path = graphs_dir / bf
        if path.exists():
            try:
                bn = gum.loadBN(str(path))
                print(f"\n{bf}:")
                print(f"  Nodes: {bn.size()}")
                print(f"  Arcs: {bn.sizeArcs()}")
                print(f"  Variables: {list(bn.names())[:5]}...")
            except Exception as e:
                print(f"\n{bf}: Error loading - {e}")
        else:
            print(f"\n{bf}: NOT FOUND")


def analyze_hinge_points(graphs_dir: Path):
    """Analyze the hinge points for narrative structure."""
    print("\n" + "=" * 60)
    print("HINGE POINT ANALYSIS")
    print("=" * 60)

    path = graphs_dir / "hinge_points.json"
    if not path.exists():
        print("hinge_points.json not found")
        return

    with open(path) as f:
        hinges = json.load(f)

    print(f"\nTotal hinge points: {len(hinges)}")
    print("\nOrdered by contingency (most surprising first):")
    for i, h in enumerate(hinges, 1):
        print(f"\n{i}. {h['description']}")
        print(f"   P(actual) = {h['p_actual']}")
        if h.get('alternatives'):
            print(f"   Alternatives: {h['alternatives']}")


def analyze_knowledge_asymmetry(graphs_dir: Path):
    """Analyze knowledge asymmetries between characters."""
    print("\n" + "=" * 60)
    print("KNOWLEDGE ASYMMETRY ANALYSIS")
    print("=" * 60)

    path = graphs_dir / "knowledge_asymmetry.graphml"
    if not path.exists():
        print("knowledge_asymmetry.graphml not found")
        return

    G = nx.read_graphml(path)

    print("\nWho knows more than whom:")
    for source, target, data in G.edges(data=True):
        count = data.get("count", 0)
        if int(count) > 2:
            facts = data.get("exclusive_facts", "")
            print(f"\n  {source} knows {count} facts that {target} doesn't:")
            for fact in facts.split(",")[:3]:
                print(f"    - {fact}")


def main():
    graphs_dir = Path(__file__).parent.parent / "graphs"

    if not graphs_dir.exists():
        print(f"Graphs directory not found: {graphs_dir}")
        print("Run build_all_graphs.py first")
        return

    test_networkx_graphs(graphs_dir)
    test_json_data(graphs_dir)
    test_pyagrum_networks(graphs_dir)
    analyze_hinge_points(graphs_dir)
    analyze_knowledge_asymmetry(graphs_dir)

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
    print(f"\nGraphs available in: {graphs_dir}")
    print("\nTo view in Gephi: Open .gexf files")
    print("To view in yEd: Open .graphml files")
    print("To use in Python: nx.read_graphml() or json.load()")


if __name__ == "__main__":
    main()
