"""
Event-Perspective Coverage Matrix for The Moonstone

Maps which narrators cover which events and how (direct witness, hearsay, retrospective, etc.)
Enables identification of gaps, conflicts, and redundancies in narrative coverage.

Output formats:
- CSV (spreadsheet compatible)
- JSON (programmatic access)
- GraphML (bipartite graph representation)
"""

import json
import csv
import networkx as nx
import pandas as pd
from pathlib import Path

# Coverage types
COVERAGE_TYPES = {
    "direct": "Narrator witnessed the event firsthand",
    "hearsay": "Narrator learned of event from another character",
    "retrospective": "Narrator mentions event looking back, after learning truth",
    "inferred": "Narrator deduces or speculates about event",
    "not_covered": "Event not mentioned in this narrator's section",
}

# Key events to track (subset of causal chain, focused on narratable events)
EVENTS = [
    "prologue_theft",              # Herncastle steals diamond (1799)
    "indians_appear",              # Indians appear as jugglers
    "birthday_dinner",             # The birthday dinner
    "murthwaite_warning",          # Murthwaite warns about Indians
    "diamond_to_rachel",           # Rachel receives the diamond
    "paint_door_discussion",       # Discussion of where to keep diamond
    "franklin_restless_night",     # Franklin unable to sleep
    "candy_doses_franklin",        # Dr. Candy gives laudanum (secret)
    "franklin_takes_diamond",      # Franklin takes diamond in trance
    "rachel_witnesses_theft",      # Rachel sees Franklin take it
    "godfrey_takes_from_franklin", # Godfrey steals from Franklin
    "discovery_morning",           # Diamond found missing
    "seegrave_investigation",      # Initial investigation
    "cuff_arrives",                # Sergeant Cuff arrives
    "rosanna_suspicious_behavior", # Rosanna acting strangely
    "cuff_paint_analysis",         # Cuff analyzes paint timing
    "rosanna_shivering_sand_trips",# Rosanna's trips to the sand
    "godfrey_to_london",           # Godfrey goes to London (pledges diamond)
    "rachel_refuses_search",       # Rachel refuses to cooperate
    "cuff_theory_rachel",          # Cuff suspects Rachel
    "rosanna_suicide",             # Rosanna drowns herself
    "cuff_withdraws",              # Cuff ends investigation
    "franklin_departs",            # Franklin leaves for Europe
    "indians_attack_godfrey",      # Indians attack Godfrey in London
    "indians_attack_luker",        # Indians attack Luker
    "lady_verinder_death",         # Lady Verinder dies
    "godfrey_proposes_rachel",     # Godfrey proposes to Rachel
    "rachel_breaks_engagement",    # Rachel breaks engagement
    "franklin_returns",            # Franklin returns to England
    "nightgown_discovery",         # Franklin finds his stained nightgown
    "limping_lucy_letter",         # Limping Lucy gives Rosanna's letter
    "franklin_reads_letter",       # Franklin reads Rosanna's posthumous letter
    "jennings_reconstruction",     # Jennings reconstructs Candy's words
    "opium_experiment",            # The experiment
    "rachel_watches_experiment",   # Rachel secretly observes
    "franklin_reenacts",           # Franklin reenacts taking diamond
    "reconciliation",              # Rachel and Franklin reconcile
    "godfrey_reclaims_diamond",    # Godfrey gets diamond from Luker
    "godfrey_murdered",            # Indians kill Godfrey
    "godfrey_exposed",             # Godfrey's double life revealed
    "diamond_returns_india",       # Diamond restored to idol
]

# Narrators
NARRATORS = [
    "prologue_cousin",    # Unnamed Herncastle cousin
    "betteredge",         # Gabriel Betteredge
    "miss_clack",         # Miss Clack
    "bruff",              # Matthew Bruff
    "franklin_blake",     # Franklin Blake
    "ezra_jennings",      # Ezra Jennings (journal)
    "sergeant_cuff",      # Sergeant Cuff (final report)
    "murthwaite",         # Mr. Murthwaite (epilogue)
]

# Coverage matrix: narrator -> event -> coverage_type
COVERAGE_MATRIX = {
    "prologue_cousin": {
        "prologue_theft": "direct",
        "indians_appear": "not_covered",
        "birthday_dinner": "not_covered",
        "murthwaite_warning": "not_covered",
        "diamond_to_rachel": "not_covered",
        "paint_door_discussion": "not_covered",
        "franklin_restless_night": "not_covered",
        "candy_doses_franklin": "not_covered",
        "franklin_takes_diamond": "not_covered",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "not_covered",
        "seegrave_investigation": "not_covered",
        "cuff_arrives": "not_covered",
        "rosanna_suspicious_behavior": "not_covered",
        "cuff_paint_analysis": "not_covered",
        "rosanna_shivering_sand_trips": "not_covered",
        "godfrey_to_london": "not_covered",
        "rachel_refuses_search": "not_covered",
        "cuff_theory_rachel": "not_covered",
        "rosanna_suicide": "not_covered",
        "cuff_withdraws": "not_covered",
        "franklin_departs": "not_covered",
        "indians_attack_godfrey": "not_covered",
        "indians_attack_luker": "not_covered",
        "lady_verinder_death": "not_covered",
        "godfrey_proposes_rachel": "not_covered",
        "rachel_breaks_engagement": "not_covered",
        "franklin_returns": "not_covered",
        "nightgown_discovery": "not_covered",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "not_covered",
        "opium_experiment": "not_covered",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "not_covered",
        "reconciliation": "not_covered",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "not_covered",
        "godfrey_exposed": "not_covered",
        "diamond_returns_india": "not_covered",
    },
    "betteredge": {
        "prologue_theft": "hearsay",
        "indians_appear": "direct",
        "birthday_dinner": "direct",
        "murthwaite_warning": "direct",
        "diamond_to_rachel": "direct",
        "paint_door_discussion": "direct",
        "franklin_restless_night": "inferred",
        "candy_doses_franklin": "not_covered",
        "franklin_takes_diamond": "not_covered",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "direct",
        "seegrave_investigation": "direct",
        "cuff_arrives": "direct",
        "rosanna_suspicious_behavior": "direct",
        "cuff_paint_analysis": "direct",
        "rosanna_shivering_sand_trips": "direct",
        "godfrey_to_london": "hearsay",
        "rachel_refuses_search": "direct",
        "cuff_theory_rachel": "hearsay",
        "rosanna_suicide": "direct",
        "cuff_withdraws": "direct",
        "franklin_departs": "direct",
        "indians_attack_godfrey": "not_covered",
        "indians_attack_luker": "not_covered",
        "lady_verinder_death": "not_covered",
        "godfrey_proposes_rachel": "not_covered",
        "rachel_breaks_engagement": "not_covered",
        "franklin_returns": "not_covered",
        "nightgown_discovery": "not_covered",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "not_covered",
        "opium_experiment": "not_covered",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "not_covered",
        "reconciliation": "not_covered",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "not_covered",
        "godfrey_exposed": "not_covered",
        "diamond_returns_india": "not_covered",
    },
    "miss_clack": {
        "prologue_theft": "not_covered",
        "indians_appear": "not_covered",
        "birthday_dinner": "not_covered",
        "murthwaite_warning": "not_covered",
        "diamond_to_rachel": "not_covered",
        "paint_door_discussion": "not_covered",
        "franklin_restless_night": "not_covered",
        "candy_doses_franklin": "not_covered",
        "franklin_takes_diamond": "not_covered",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "not_covered",
        "seegrave_investigation": "not_covered",
        "cuff_arrives": "not_covered",
        "rosanna_suspicious_behavior": "not_covered",
        "cuff_paint_analysis": "not_covered",
        "rosanna_shivering_sand_trips": "not_covered",
        "godfrey_to_london": "not_covered",
        "rachel_refuses_search": "not_covered",
        "cuff_theory_rachel": "not_covered",
        "rosanna_suicide": "not_covered",
        "cuff_withdraws": "not_covered",
        "franklin_departs": "not_covered",
        "indians_attack_godfrey": "hearsay",
        "indians_attack_luker": "hearsay",
        "lady_verinder_death": "direct",
        "godfrey_proposes_rachel": "direct",
        "rachel_breaks_engagement": "direct",
        "franklin_returns": "not_covered",
        "nightgown_discovery": "not_covered",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "not_covered",
        "opium_experiment": "not_covered",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "not_covered",
        "reconciliation": "not_covered",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "not_covered",
        "godfrey_exposed": "not_covered",
        "diamond_returns_india": "not_covered",
    },
    "bruff": {
        "prologue_theft": "not_covered",
        "indians_appear": "not_covered",
        "birthday_dinner": "not_covered",
        "murthwaite_warning": "not_covered",
        "diamond_to_rachel": "not_covered",
        "paint_door_discussion": "not_covered",
        "franklin_restless_night": "not_covered",
        "candy_doses_franklin": "not_covered",
        "franklin_takes_diamond": "not_covered",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "not_covered",
        "seegrave_investigation": "not_covered",
        "cuff_arrives": "not_covered",
        "rosanna_suspicious_behavior": "not_covered",
        "cuff_paint_analysis": "not_covered",
        "rosanna_shivering_sand_trips": "not_covered",
        "godfrey_to_london": "retrospective",
        "rachel_refuses_search": "not_covered",
        "cuff_theory_rachel": "not_covered",
        "rosanna_suicide": "not_covered",
        "cuff_withdraws": "not_covered",
        "franklin_departs": "not_covered",
        "indians_attack_godfrey": "hearsay",
        "indians_attack_luker": "hearsay",
        "lady_verinder_death": "hearsay",
        "godfrey_proposes_rachel": "hearsay",
        "rachel_breaks_engagement": "hearsay",
        "franklin_returns": "direct",
        "nightgown_discovery": "not_covered",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "not_covered",
        "opium_experiment": "not_covered",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "not_covered",
        "reconciliation": "not_covered",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "not_covered",
        "godfrey_exposed": "retrospective",
        "diamond_returns_india": "not_covered",
    },
    "franklin_blake": {
        "prologue_theft": "hearsay",
        "indians_appear": "retrospective",
        "birthday_dinner": "retrospective",
        "murthwaite_warning": "retrospective",
        "diamond_to_rachel": "retrospective",
        "paint_door_discussion": "retrospective",
        "franklin_restless_night": "retrospective",
        "candy_doses_franklin": "retrospective",  # Learns later
        "franklin_takes_diamond": "retrospective",  # Learns he did it
        "rachel_witnesses_theft": "retrospective",
        "godfrey_takes_from_franklin": "retrospective",
        "discovery_morning": "retrospective",
        "seegrave_investigation": "retrospective",
        "cuff_arrives": "retrospective",
        "rosanna_suspicious_behavior": "retrospective",
        "cuff_paint_analysis": "retrospective",
        "rosanna_shivering_sand_trips": "retrospective",
        "godfrey_to_london": "not_covered",
        "rachel_refuses_search": "retrospective",
        "cuff_theory_rachel": "retrospective",
        "rosanna_suicide": "retrospective",
        "cuff_withdraws": "retrospective",
        "franklin_departs": "retrospective",
        "indians_attack_godfrey": "hearsay",
        "indians_attack_luker": "hearsay",
        "lady_verinder_death": "hearsay",
        "godfrey_proposes_rachel": "hearsay",
        "rachel_breaks_engagement": "hearsay",
        "franklin_returns": "direct",
        "nightgown_discovery": "direct",
        "limping_lucy_letter": "direct",
        "franklin_reads_letter": "direct",
        "jennings_reconstruction": "direct",
        "opium_experiment": "direct",
        "rachel_watches_experiment": "retrospective",
        "franklin_reenacts": "direct",
        "reconciliation": "direct",
        "godfrey_reclaims_diamond": "hearsay",
        "godfrey_murdered": "hearsay",
        "godfrey_exposed": "hearsay",
        "diamond_returns_india": "not_covered",
    },
    "ezra_jennings": {
        "prologue_theft": "not_covered",
        "indians_appear": "not_covered",
        "birthday_dinner": "hearsay",
        "murthwaite_warning": "not_covered",
        "diamond_to_rachel": "not_covered",
        "paint_door_discussion": "not_covered",
        "franklin_restless_night": "inferred",
        "candy_doses_franklin": "inferred",  # He reconstructs this
        "franklin_takes_diamond": "inferred",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "not_covered",
        "seegrave_investigation": "not_covered",
        "cuff_arrives": "not_covered",
        "rosanna_suspicious_behavior": "not_covered",
        "cuff_paint_analysis": "not_covered",
        "rosanna_shivering_sand_trips": "not_covered",
        "godfrey_to_london": "not_covered",
        "rachel_refuses_search": "not_covered",
        "cuff_theory_rachel": "not_covered",
        "rosanna_suicide": "not_covered",
        "cuff_withdraws": "not_covered",
        "franklin_departs": "not_covered",
        "indians_attack_godfrey": "not_covered",
        "indians_attack_luker": "not_covered",
        "lady_verinder_death": "not_covered",
        "godfrey_proposes_rachel": "not_covered",
        "rachel_breaks_engagement": "not_covered",
        "franklin_returns": "direct",
        "nightgown_discovery": "hearsay",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "direct",
        "opium_experiment": "direct",
        "rachel_watches_experiment": "direct",
        "franklin_reenacts": "direct",
        "reconciliation": "direct",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "not_covered",
        "godfrey_exposed": "not_covered",
        "diamond_returns_india": "not_covered",
    },
    "sergeant_cuff": {
        "prologue_theft": "hearsay",
        "indians_appear": "hearsay",
        "birthday_dinner": "hearsay",
        "murthwaite_warning": "hearsay",
        "diamond_to_rachel": "hearsay",
        "paint_door_discussion": "hearsay",
        "franklin_restless_night": "not_covered",
        "candy_doses_franklin": "retrospective",
        "franklin_takes_diamond": "retrospective",
        "rachel_witnesses_theft": "retrospective",
        "godfrey_takes_from_franklin": "retrospective",
        "discovery_morning": "hearsay",
        "seegrave_investigation": "hearsay",
        "cuff_arrives": "direct",
        "rosanna_suspicious_behavior": "direct",
        "cuff_paint_analysis": "direct",
        "rosanna_shivering_sand_trips": "direct",
        "godfrey_to_london": "retrospective",
        "rachel_refuses_search": "direct",
        "cuff_theory_rachel": "direct",
        "rosanna_suicide": "direct",
        "cuff_withdraws": "direct",
        "franklin_departs": "direct",
        "indians_attack_godfrey": "retrospective",
        "indians_attack_luker": "retrospective",
        "lady_verinder_death": "hearsay",
        "godfrey_proposes_rachel": "hearsay",
        "rachel_breaks_engagement": "hearsay",
        "franklin_returns": "hearsay",
        "nightgown_discovery": "hearsay",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "hearsay",
        "opium_experiment": "hearsay",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "hearsay",
        "reconciliation": "hearsay",
        "godfrey_reclaims_diamond": "direct",
        "godfrey_murdered": "direct",
        "godfrey_exposed": "direct",
        "diamond_returns_india": "not_covered",
    },
    "murthwaite": {
        "prologue_theft": "hearsay",
        "indians_appear": "direct",
        "birthday_dinner": "direct",
        "murthwaite_warning": "direct",
        "diamond_to_rachel": "direct",
        "paint_door_discussion": "not_covered",
        "franklin_restless_night": "not_covered",
        "candy_doses_franklin": "not_covered",
        "franklin_takes_diamond": "not_covered",
        "rachel_witnesses_theft": "not_covered",
        "godfrey_takes_from_franklin": "not_covered",
        "discovery_morning": "not_covered",
        "seegrave_investigation": "not_covered",
        "cuff_arrives": "not_covered",
        "rosanna_suspicious_behavior": "not_covered",
        "cuff_paint_analysis": "not_covered",
        "rosanna_shivering_sand_trips": "not_covered",
        "godfrey_to_london": "not_covered",
        "rachel_refuses_search": "not_covered",
        "cuff_theory_rachel": "not_covered",
        "rosanna_suicide": "not_covered",
        "cuff_withdraws": "not_covered",
        "franklin_departs": "not_covered",
        "indians_attack_godfrey": "not_covered",
        "indians_attack_luker": "not_covered",
        "lady_verinder_death": "not_covered",
        "godfrey_proposes_rachel": "not_covered",
        "rachel_breaks_engagement": "not_covered",
        "franklin_returns": "not_covered",
        "nightgown_discovery": "not_covered",
        "limping_lucy_letter": "not_covered",
        "franklin_reads_letter": "not_covered",
        "jennings_reconstruction": "not_covered",
        "opium_experiment": "not_covered",
        "rachel_watches_experiment": "not_covered",
        "franklin_reenacts": "not_covered",
        "reconciliation": "not_covered",
        "godfrey_reclaims_diamond": "not_covered",
        "godfrey_murdered": "hearsay",
        "godfrey_exposed": "hearsay",
        "diamond_returns_india": "direct",
    },
}


def build_coverage_dataframe():
    """Build pandas DataFrame of the coverage matrix."""
    data = []
    for narrator in NARRATORS:
        row = {"narrator": narrator}
        for event in EVENTS:
            row[event] = COVERAGE_MATRIX.get(narrator, {}).get(event, "not_covered")
        data.append(row)
    return pd.DataFrame(data)


def build_bipartite_graph():
    """Build bipartite graph: Narrators <-> Events with coverage type as edge attribute."""
    G = nx.Graph()

    # Add narrator nodes
    for narrator in NARRATORS:
        G.add_node(f"narrator:{narrator}", node_type="narrator", label=narrator)

    # Add event nodes
    for event in EVENTS:
        G.add_node(f"event:{event}", node_type="event", label=event)

    # Add edges for non-trivial coverage
    for narrator in NARRATORS:
        for event in EVENTS:
            coverage = COVERAGE_MATRIX.get(narrator, {}).get(event, "not_covered")
            if coverage != "not_covered":
                weight = {
                    "direct": 1.0,
                    "hearsay": 0.7,
                    "retrospective": 0.5,
                    "inferred": 0.3
                }.get(coverage, 0.0)

                G.add_edge(f"narrator:{narrator}", f"event:{event}",
                          coverage_type=coverage,
                          weight=weight)

    return G


def analyze_coverage(df):
    """Analyze the coverage matrix for gaps and redundancies."""
    analysis = {
        "events_by_coverage_count": {},
        "narrators_by_coverage_count": {},
        "uncovered_events": [],
        "single_source_events": [],
        "multi_perspective_events": [],
        "coverage_type_distribution": {},
    }

    # Count coverage per event
    for event in EVENTS:
        coverage_count = sum(1 for narrator in NARRATORS
                            if COVERAGE_MATRIX.get(narrator, {}).get(event, "not_covered") != "not_covered")
        analysis["events_by_coverage_count"][event] = coverage_count

        if coverage_count == 0:
            analysis["uncovered_events"].append(event)
        elif coverage_count == 1:
            analysis["single_source_events"].append(event)
        elif coverage_count >= 3:
            analysis["multi_perspective_events"].append(event)

    # Count coverage per narrator
    for narrator in NARRATORS:
        coverage_count = sum(1 for event in EVENTS
                            if COVERAGE_MATRIX.get(narrator, {}).get(event, "not_covered") != "not_covered")
        analysis["narrators_by_coverage_count"][narrator] = coverage_count

    # Coverage type distribution
    for coverage_type in COVERAGE_TYPES.keys():
        count = sum(1 for narrator in NARRATORS for event in EVENTS
                   if COVERAGE_MATRIX.get(narrator, {}).get(event) == coverage_type)
        analysis["coverage_type_distribution"][coverage_type] = count

    return analysis


def export_matrix(output_dir: Path):
    """Export the coverage matrix in multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build DataFrame
    df = build_coverage_dataframe()

    # Export CSV
    df.to_csv(output_dir / "event_perspective_matrix.csv", index=False)

    # Export transposed CSV (events as rows)
    df_t = df.set_index("narrator").T
    df_t.index.name = "event"
    df_t.to_csv(output_dir / "event_perspective_matrix_transposed.csv")

    # Export JSON
    matrix_json = {
        "narrators": NARRATORS,
        "events": EVENTS,
        "coverage_types": COVERAGE_TYPES,
        "matrix": COVERAGE_MATRIX
    }
    with open(output_dir / "event_perspective_matrix.json", "w") as f:
        json.dump(matrix_json, f, indent=2)

    # Build and export bipartite graph
    G = build_bipartite_graph()
    nx.write_graphml(G, output_dir / "event_perspective_bipartite.graphml")
    nx.write_gexf(G, output_dir / "event_perspective_bipartite.gexf")

    # Analyze and export analysis
    analysis = analyze_coverage(df)
    with open(output_dir / "event_perspective_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"Event-Perspective Matrix: {len(EVENTS)} events x {len(NARRATORS)} narrators")
    print(f"Multi-perspective events: {len(analysis['multi_perspective_events'])}")
    print(f"Single-source events: {len(analysis['single_source_events'])}")
    print(f"Uncovered events: {len(analysis['uncovered_events'])}")

    return df, G


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_matrix(output_dir)
    print(f"\nEvent-perspective matrix exported to {output_dir}")
