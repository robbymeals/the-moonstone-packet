"""
Knowledge State Graph for The Moonstone

Tracks who knows what, when they learn it, and knowledge asymmetries
that drive the narrative.

Output formats:
- GraphML (standard interchange)
- GEXF (Gephi native)
- JSON (programmatic access)
"""

import json
import networkx as nx
from pathlib import Path

# Define the key facts that drive the narrative
FACTS = {
    "diamond_curse": "The Moonstone carries a curse and is pursued by Brahmin guardians",
    "indians_are_brahmins": "The three Indians are high-caste Brahmins, not common jugglers",
    "paint_wet": "The sitting-room door paint was wet on the night of June 21",
    "franklin_entered_room": "Franklin Blake entered Rachel's sitting-room and took the diamond",
    "franklin_drugged": "Dr. Candy secretly administered laudanum to Franklin",
    "franklin_unconscious": "Franklin was in a laudanum trance and has no memory",
    "nightgown_stained": "Franklin's nightgown has a paint smear proving he touched the door",
    "rosanna_hid_nightgown": "Rosanna hid the stained nightgown in the Shivering Sand",
    "rosanna_loves_franklin": "Rosanna is in love with Franklin Blake",
    "godfrey_took_diamond": "Godfrey Ablewhite took the diamond from Franklin's room",
    "godfrey_embezzled": "Godfrey embezzled from a trust fund he managed",
    "diamond_at_luker": "The diamond was pledged to Mr. Luker's bank",
    "rachel_witnessed": "Rachel saw Franklin take the diamond from her room",
}

# Characters and their knowledge states over time
# Format: character -> fact -> (knows: bool, since_when: str, belief: str)
# belief can be: "true", "false", "suspects", "unknown"

KNOWLEDGE_STATES = {
    "Gabriel Betteredge": {
        "diamond_curse": ("knows", "before_birthday", "true"),
        "indians_are_brahmins": ("knows", "birthday_dinner", "true"),  # Murthwaite tells household
        "paint_wet": ("knows", "june_22_morning", "true"),
        "franklin_entered_room": ("unknown", None, None),
        "franklin_drugged": ("unknown", None, None),  # Never learns directly in his narrative
        "franklin_unconscious": ("knows", "opium_experiment", "true"),
        "nightgown_stained": ("knows", "june_1849", "true"),  # When Franklin shows him
        "rosanna_hid_nightgown": ("knows", "june_1849", "true"),
        "rosanna_loves_franklin": ("suspects", "june_1848", "true"),  # Sees signs, doesn't fully grasp
        "godfrey_took_diamond": ("knows", "resolution", "true"),
        "godfrey_embezzled": ("knows", "resolution", "true"),
        "diamond_at_luker": ("knows", "resolution", "true"),
        "rachel_witnessed": ("knows", "opium_experiment", "true"),
    },
    "Franklin Blake": {
        "diamond_curse": ("knows", "before_birthday", "true"),
        "indians_are_brahmins": ("knows", "birthday_dinner", "true"),
        "paint_wet": ("knows", "june_22_morning", "true"),
        "franklin_entered_room": ("unknown", None, None),  # Until Rachel tells him
        "franklin_drugged": ("knows", "june_1849_jennings", "true"),
        "franklin_unconscious": ("knows", "june_1849_jennings", "true"),
        "nightgown_stained": ("knows", "june_1849_shivering_sand", "true"),
        "rosanna_hid_nightgown": ("knows", "june_1849_letter", "true"),
        "rosanna_loves_franklin": ("knows", "june_1849_letter", "true"),  # Posthumous letter
        "godfrey_took_diamond": ("knows", "resolution", "true"),
        "godfrey_embezzled": ("knows", "resolution", "true"),
        "diamond_at_luker": ("knows", "investigation_1849", "true"),
        "rachel_witnessed": ("knows", "confrontation_1849", "true"),
    },
    "Rachel Verinder": {
        "diamond_curse": ("knows", "birthday_dinner", "true"),
        "indians_are_brahmins": ("knows", "birthday_dinner", "true"),
        "paint_wet": ("unknown", None, None),  # Not mentioned that she knew
        "franklin_entered_room": ("knows", "june_21_night", "true"),  # SHE WITNESSED IT
        "franklin_drugged": ("unknown", None, None),  # Until experiment
        "franklin_unconscious": ("knows", "opium_experiment", "true"),
        "nightgown_stained": ("unknown", None, None),
        "rosanna_hid_nightgown": ("unknown", None, None),
        "rosanna_loves_franklin": ("unknown", None, None),
        "godfrey_took_diamond": ("knows", "resolution", "true"),
        "godfrey_embezzled": ("knows", "resolution", "true"),
        "diamond_at_luker": ("unknown", None, None),
        "rachel_witnessed": ("knows", "june_21_night", "true"),  # Tautology - she is the witness
    },
    "Rosanna Spearman": {
        "diamond_curse": ("unknown", None, None),
        "indians_are_brahmins": ("unknown", None, None),
        "paint_wet": ("knows", "june_22_morning", "true"),
        "franklin_entered_room": ("suspects", "june_22", "true"),  # Infers from nightgown
        "franklin_drugged": ("unknown", None, None),
        "franklin_unconscious": ("unknown", None, None),
        "nightgown_stained": ("knows", "june_22", "true"),  # SHE FOUND IT
        "rosanna_hid_nightgown": ("knows", "june_22", "true"),  # SHE DID IT
        "rosanna_loves_franklin": ("knows", "always", "true"),
        "godfrey_took_diamond": ("unknown", None, None),
        "godfrey_embezzled": ("unknown", None, None),
        "diamond_at_luker": ("unknown", None, None),
        "rachel_witnessed": ("unknown", None, None),
    },
    "Sergeant Cuff": {
        "diamond_curse": ("knows", "investigation_start", "true"),
        "indians_are_brahmins": ("knows", "investigation", "true"),
        "paint_wet": ("knows", "june_23", "true"),  # Key to his investigation
        "franklin_entered_room": ("unknown", None, None),  # Never learns during main investigation
        "franklin_drugged": ("unknown", None, None),
        "franklin_unconscious": ("knows", "final_report", "true"),
        "nightgown_stained": ("suspects", "june_1848", "true"),  # Knows there's a stained garment
        "rosanna_hid_nightgown": ("suspects", "june_1848", "true"),
        "rosanna_loves_franklin": ("knows", "june_1848", "true"),  # He sees it clearly
        "godfrey_took_diamond": ("knows", "investigation_1849", "true"),
        "godfrey_embezzled": ("knows", "investigation_1849", "true"),
        "diamond_at_luker": ("knows", "investigation_1849", "true"),
        "rachel_witnessed": ("knows", "final_report", "true"),
    },
    "Godfrey Ablewhite": {
        "diamond_curse": ("knows", "birthday_dinner", "true"),
        "indians_are_brahmins": ("knows", "birthday_dinner", "true"),
        "paint_wet": ("unknown", None, None),
        "franklin_entered_room": ("knows", "june_21_night", "true"),  # HE SAW/FOLLOWED
        "franklin_drugged": ("unknown", None, None),  # Doesn't know why Franklin was dazed
        "franklin_unconscious": ("knows", "june_21_night", "true"),  # Saw Franklin's state
        "nightgown_stained": ("unknown", None, None),
        "rosanna_hid_nightgown": ("unknown", None, None),
        "rosanna_loves_franklin": ("unknown", None, None),
        "godfrey_took_diamond": ("knows", "june_21_night", "true"),  # HE DID IT
        "godfrey_embezzled": ("knows", "always", "true"),  # HIS SECRET
        "diamond_at_luker": ("knows", "june_23", "true"),  # HE PLEDGED IT
        "rachel_witnessed": ("unknown", None, None),
    },
    "Ezra Jennings": {
        "diamond_curse": ("knows", "1849", "true"),
        "indians_are_brahmins": ("unknown", None, None),
        "paint_wet": ("knows", "1849", "true"),
        "franklin_entered_room": ("knows", "reconstruction", "true"),
        "franklin_drugged": ("knows", "reconstruction", "true"),  # HE DISCOVERED THIS
        "franklin_unconscious": ("knows", "reconstruction", "true"),
        "nightgown_stained": ("knows", "1849", "true"),
        "rosanna_hid_nightgown": ("knows", "1849", "true"),
        "rosanna_loves_franklin": ("unknown", None, None),
        "godfrey_took_diamond": ("unknown", None, None),  # Dies before resolution
        "godfrey_embezzled": ("unknown", None, None),
        "diamond_at_luker": ("unknown", None, None),
        "rachel_witnessed": ("knows", "experiment", "true"),
    },
    "Dr. Candy": {
        "diamond_curse": ("unknown", None, None),
        "indians_are_brahmins": ("unknown", None, None),
        "paint_wet": ("unknown", None, None),
        "franklin_entered_room": ("unknown", None, None),
        "franklin_drugged": ("knows", "june_21_night", "true"),  # HE DID IT
        "franklin_unconscious": ("unknown", None, None),  # Doesn't know the consequence
        "nightgown_stained": ("unknown", None, None),
        "rosanna_hid_nightgown": ("unknown", None, None),
        "rosanna_loves_franklin": ("unknown", None, None),
        "godfrey_took_diamond": ("unknown", None, None),
        "godfrey_embezzled": ("unknown", None, None),
        "diamond_at_luker": ("unknown", None, None),
        "rachel_witnessed": ("unknown", None, None),
    },
}

# Timeline of key moments for knowledge state changes
TIMELINE = [
    "before_birthday",
    "birthday_dinner",
    "june_21_night",
    "june_22_morning",
    "june_22",
    "june_23",
    "june_1848",
    "investigation_start",
    "investigation",
    "resolution_1848",
    "1849",
    "investigation_1849",
    "june_1849",
    "june_1849_shivering_sand",
    "june_1849_letter",
    "june_1849_jennings",
    "reconstruction",
    "confrontation_1849",
    "experiment",
    "opium_experiment",
    "final_report",
    "resolution",
    "always",  # Things known throughout
]


def build_knowledge_graph():
    """Build a bipartite graph: Characters <-> Facts with knowledge relationships."""
    G = nx.DiGraph()

    # Add fact nodes
    for fact_id, fact_desc in FACTS.items():
        G.add_node(f"fact:{fact_id}",
                   node_type="fact",
                   label=fact_id,
                   description=fact_desc)

    # Add character nodes and their knowledge edges
    for character, knowledge in KNOWLEDGE_STATES.items():
        char_id = character.replace(" ", "_").lower()
        G.add_node(f"char:{char_id}",
                   node_type="character",
                   label=character)

        for fact_id, (status, since_when, belief) in knowledge.items():
            if status == "knows":
                G.add_edge(f"char:{char_id}", f"fact:{fact_id}",
                          relationship="KNOWS",
                          since=since_when,
                          belief=belief,
                          weight=1.0)
            elif status == "suspects":
                G.add_edge(f"char:{char_id}", f"fact:{fact_id}",
                          relationship="SUSPECTS",
                          since=since_when,
                          belief=belief,
                          weight=0.5)
            elif status == "believes_false":
                G.add_edge(f"char:{char_id}", f"fact:{fact_id}",
                          relationship="BELIEVES_FALSE",
                          since=since_when,
                          belief="false",
                          weight=-1.0)

    return G


def build_knowledge_asymmetry_graph():
    """Build a graph showing knowledge asymmetries between characters."""
    G = nx.DiGraph()

    characters = list(KNOWLEDGE_STATES.keys())

    # Add character nodes
    for char in characters:
        char_id = char.replace(" ", "_").lower()
        G.add_node(char_id, label=char)

    # For each pair, calculate knowledge asymmetry
    for i, char1 in enumerate(characters):
        for char2 in characters[i+1:]:
            char1_id = char1.replace(" ", "_").lower()
            char2_id = char2.replace(" ", "_").lower()

            # What does char1 know that char2 doesn't?
            char1_exclusive = []
            char2_exclusive = []

            for fact_id in FACTS.keys():
                k1 = KNOWLEDGE_STATES[char1].get(fact_id, ("unknown", None, None))
                k2 = KNOWLEDGE_STATES[char2].get(fact_id, ("unknown", None, None))

                if k1[0] == "knows" and k2[0] != "knows":
                    char1_exclusive.append(fact_id)
                if k2[0] == "knows" and k1[0] != "knows":
                    char2_exclusive.append(fact_id)

            if char1_exclusive:
                G.add_edge(char1_id, char2_id,
                          relationship="KNOWS_MORE",
                          exclusive_facts=",".join(char1_exclusive),
                          count=len(char1_exclusive))

            if char2_exclusive:
                G.add_edge(char2_id, char1_id,
                          relationship="KNOWS_MORE",
                          exclusive_facts=",".join(char2_exclusive),
                          count=len(char2_exclusive))

    return G


def export_graphs(output_dir: Path):
    """Export all graphs to multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build graphs
    knowledge_graph = build_knowledge_graph()
    asymmetry_graph = build_knowledge_asymmetry_graph()

    # Export knowledge graph
    nx.write_graphml(knowledge_graph, output_dir / "knowledge_state.graphml")
    nx.write_gexf(knowledge_graph, output_dir / "knowledge_state.gexf")

    # Export as JSON for programmatic access
    knowledge_json = nx.node_link_data(knowledge_graph)
    with open(output_dir / "knowledge_state.json", "w") as f:
        json.dump(knowledge_json, f, indent=2)

    # Export asymmetry graph
    nx.write_graphml(asymmetry_graph, output_dir / "knowledge_asymmetry.graphml")
    nx.write_gexf(asymmetry_graph, output_dir / "knowledge_asymmetry.gexf")

    asymmetry_json = nx.node_link_data(asymmetry_graph)
    with open(output_dir / "knowledge_asymmetry.json", "w") as f:
        json.dump(asymmetry_json, f, indent=2)

    # Export raw data as JSON for reference
    with open(output_dir / "knowledge_data.json", "w") as f:
        json.dump({
            "facts": FACTS,
            "knowledge_states": KNOWLEDGE_STATES,
            "timeline": TIMELINE
        }, f, indent=2, default=str)

    print(f"Knowledge State Graph: {knowledge_graph.number_of_nodes()} nodes, {knowledge_graph.number_of_edges()} edges")
    print(f"Knowledge Asymmetry Graph: {asymmetry_graph.number_of_nodes()} nodes, {asymmetry_graph.number_of_edges()} edges")

    return knowledge_graph, asymmetry_graph


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_graphs(output_dir)
    print(f"\nGraphs exported to {output_dir}")
