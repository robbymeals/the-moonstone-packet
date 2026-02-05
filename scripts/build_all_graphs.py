#!/usr/bin/env python3
"""
Master script to build all Moonstone narrative graphs.

Outputs to graphs/ directory:
- knowledge_state.* — Who knows what, when
- knowledge_asymmetry.* — Knowledge differences between characters
- causal_chain.* — Event causation (DAG)
- event_perspective_*.* — Which narrators cover which events
- location_graph.* — Spatial relationships
- voice_fingerprints.json — Narrator style features
- state_transitions.* — Probabilistic state model
"""

from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from build_knowledge_state_graph import export_graphs as export_knowledge
from build_causal_chain_graph import export_graphs as export_causal
from build_event_perspective_matrix import export_matrix as export_perspective
from build_location_graph import export_graphs as export_location
from build_voice_fingerprints import export_fingerprints as export_voice
from build_state_transitions import export_model as export_transitions


def main():
    output_dir = Path(__file__).parent.parent / "graphs"
    source_dir = Path(__file__).parent.parent / "src"

    print("=" * 60)
    print("MOONSTONE NARRATIVE GRAPH BUILDER")
    print("=" * 60)

    print("\n[1/6] Building Knowledge State Graphs...")
    export_knowledge(output_dir)

    print("\n[2/6] Building Causal Chain Graph (DAG + Bayesian Network)...")
    export_causal(output_dir)

    print("\n[3/6] Building Event-Perspective Coverage Matrix...")
    export_perspective(output_dir)

    print("\n[4/6] Building Location Graph...")
    export_location(output_dir)

    print("\n[5/6] Building Voice Fingerprints...")
    export_voice(output_dir, source_dir / "pg155.txt")

    print("\n[6/6] Building Probabilistic State Transition Model...")
    export_transitions(output_dir)

    print("\n" + "=" * 60)
    print("ALL GRAPHS BUILT SUCCESSFULLY")
    print("=" * 60)

    # List output files
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    for f in sorted(output_dir.glob("*")):
        size = f.stat().st_size
        print(f"  {f.name:40} {size:>8} bytes")


if __name__ == "__main__":
    main()
