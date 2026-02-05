"""
Scene Location Graph for The Moonstone

Maps spatial relationships between locations with perception constraints.
Enables validation of what characters could have witnessed from where.

Output formats:
- GraphML, GEXF (standard graph formats)
- JSON (programmatic access)
"""

import json
import networkx as nx
from pathlib import Path

# Locations in the narrative
LOCATIONS = {
    # Verinder Estate - Yorkshire
    "verinder_house": {
        "description": "The Verinder family estate in Yorkshire",
        "type": "building",
        "parent": None,
    },
    "entrance_hall": {
        "description": "Main entrance hall of the Verinder house",
        "type": "room",
        "parent": "verinder_house",
    },
    "drawing_room": {
        "description": "Drawing room where the birthday dinner guests gathered",
        "type": "room",
        "parent": "verinder_house",
    },
    "dining_room": {
        "description": "Dining room where the birthday dinner was held",
        "type": "room",
        "parent": "verinder_house",
    },
    "rachels_sitting_room": {
        "description": "Rachel's private sitting-room with the Indian cabinet (First floor)",
        "type": "room",
        "parent": "verinder_house",
        "floor": 1,
        "key_feature": "Indian cabinet where diamond was kept",
    },
    "rachels_bedroom": {
        "description": "Rachel's bedroom, adjacent to her sitting-room",
        "type": "room",
        "parent": "verinder_house",
        "floor": 1,
    },
    "franklins_room": {
        "description": "Franklin Blake's guest bedroom",
        "type": "room",
        "parent": "verinder_house",
        "floor": 1,
    },
    "godfreys_room": {
        "description": "Godfrey Ablewhite's guest bedroom",
        "type": "room",
        "parent": "verinder_house",
        "floor": 1,
    },
    "servants_hall": {
        "description": "Servants' common area",
        "type": "room",
        "parent": "verinder_house",
        "floor": 0,
    },
    "betteredges_room": {
        "description": "Betteredge's quarters",
        "type": "room",
        "parent": "verinder_house",
    },
    "rosannas_room": {
        "description": "Rosanna Spearman's room in servants' quarters",
        "type": "room",
        "parent": "verinder_house",
    },
    "painted_door": {
        "description": "The freshly painted door to Rachel's sitting-room",
        "type": "feature",
        "parent": "rachels_sitting_room",
        "key_feature": "Paint wet on night of June 21",
    },
    "first_floor_corridor": {
        "description": "Corridor connecting bedrooms on first floor",
        "type": "passage",
        "parent": "verinder_house",
        "floor": 1,
    },

    # Estate grounds
    "verinder_grounds": {
        "description": "Grounds surrounding the Verinder house",
        "type": "outdoor",
        "parent": None,
    },
    "terrace": {
        "description": "Terrace outside the house",
        "type": "outdoor",
        "parent": "verinder_grounds",
    },
    "shrubbery": {
        "description": "The shrubbery walk where Indians appeared",
        "type": "outdoor",
        "parent": "verinder_grounds",
    },

    # Coastal locations
    "shivering_sand": {
        "description": "Tidal quicksand area on the coast",
        "type": "outdoor",
        "parent": None,
        "key_feature": "Where Rosanna hid the nightgown and drowned herself",
        "tidal": True,
    },
    "cobbs_hole": {
        "description": "Fishing village, home of Limping Lucy's family",
        "type": "village",
        "parent": None,
    },
    "yolland_cottage": {
        "description": "The Yolland family cottage",
        "type": "building",
        "parent": "cobbs_hole",
    },

    # Frizinghall
    "frizinghall": {
        "description": "Nearby town",
        "type": "town",
        "parent": None,
    },
    "frizinghall_bank": {
        "description": "Bank where diamond was kept before birthday",
        "type": "building",
        "parent": "frizinghall",
    },
    "dr_candys_house": {
        "description": "Dr. Candy's residence and practice",
        "type": "building",
        "parent": "frizinghall",
    },

    # London locations
    "london": {
        "description": "London",
        "type": "city",
        "parent": None,
    },
    "lukers_bank": {
        "description": "Mr. Luker's bank/money-lending establishment",
        "type": "building",
        "parent": "london",
    },
    "bruffs_office": {
        "description": "Matthew Bruff's law offices",
        "type": "building",
        "parent": "london",
    },
    "wheel_of_fortune": {
        "description": "The inn where Godfrey was murdered",
        "type": "building",
        "parent": "london",
        "key_feature": "Site of Godfrey's death",
    },
    "lady_verinder_london": {
        "description": "Lady Verinder's London residence",
        "type": "building",
        "parent": "london",
    },

    # India
    "india": {
        "description": "India",
        "type": "country",
        "parent": None,
    },
    "seringapatam": {
        "description": "Site of the 1799 siege where diamond was stolen",
        "type": "city",
        "parent": "india",
    },
    "somnauth_shrine": {
        "description": "Hindu shrine where the Moonstone originated and returned",
        "type": "building",
        "parent": "india",
        "key_feature": "The Moon-God idol",
    },
}

# Spatial relationships
SPATIAL_EDGES = [
    # Containment
    ("verinder_house", "entrance_hall", "CONTAINS"),
    ("verinder_house", "drawing_room", "CONTAINS"),
    ("verinder_house", "dining_room", "CONTAINS"),
    ("verinder_house", "rachels_sitting_room", "CONTAINS"),
    ("verinder_house", "rachels_bedroom", "CONTAINS"),
    ("verinder_house", "franklins_room", "CONTAINS"),
    ("verinder_house", "godfreys_room", "CONTAINS"),
    ("verinder_house", "servants_hall", "CONTAINS"),
    ("verinder_house", "betteredges_room", "CONTAINS"),
    ("verinder_house", "rosannas_room", "CONTAINS"),
    ("verinder_house", "first_floor_corridor", "CONTAINS"),
    ("rachels_sitting_room", "painted_door", "CONTAINS"),
    ("verinder_grounds", "terrace", "CONTAINS"),
    ("verinder_grounds", "shrubbery", "CONTAINS"),
    ("cobbs_hole", "yolland_cottage", "CONTAINS"),
    ("frizinghall", "frizinghall_bank", "CONTAINS"),
    ("frizinghall", "dr_candys_house", "CONTAINS"),
    ("london", "lukers_bank", "CONTAINS"),
    ("london", "bruffs_office", "CONTAINS"),
    ("london", "wheel_of_fortune", "CONTAINS"),
    ("london", "lady_verinder_london", "CONTAINS"),
    ("india", "seringapatam", "CONTAINS"),
    ("india", "somnauth_shrine", "CONTAINS"),

    # Adjacency (same floor, can move between)
    ("entrance_hall", "drawing_room", "ADJACENT_TO"),
    ("drawing_room", "dining_room", "ADJACENT_TO"),
    ("rachels_sitting_room", "rachels_bedroom", "ADJACENT_TO"),
    ("rachels_sitting_room", "first_floor_corridor", "ADJACENT_TO"),
    ("franklins_room", "first_floor_corridor", "ADJACENT_TO"),
    ("godfreys_room", "first_floor_corridor", "ADJACENT_TO"),
    ("rachels_bedroom", "first_floor_corridor", "ADJACENT_TO"),
    ("verinder_house", "terrace", "ADJACENT_TO"),
    ("terrace", "shrubbery", "ADJACENT_TO"),
    ("verinder_grounds", "shivering_sand", "ADJACENT_TO"),
    ("cobbs_hole", "shivering_sand", "ADJACENT_TO"),
    ("verinder_house", "verinder_grounds", "ADJACENT_TO"),

    # Perception - what can be seen/heard from where
    ("rachels_sitting_room", "painted_door", "VISIBLE_FROM"),
    ("first_floor_corridor", "painted_door", "VISIBLE_FROM"),
    ("rachels_bedroom", "rachels_sitting_room", "AUDIBLE_FROM"),
    ("terrace", "shrubbery", "VISIBLE_FROM"),
    ("drawing_room", "terrace", "VISIBLE_FROM"),
]

# Key events mapped to locations
EVENT_LOCATIONS = {
    "prologue_theft": "seringapatam",
    "birthday_dinner": "dining_room",
    "indians_appear": "shrubbery",
    "diamond_given": "dining_room",
    "diamond_placed": "rachels_sitting_room",
    "candy_doses_franklin": "verinder_house",  # Exact room unclear
    "franklin_takes_diamond": "rachels_sitting_room",
    "rachel_witnesses": "rachels_bedroom",  # She watched from concealment
    "godfrey_steals": "franklins_room",
    "discovery_morning": "rachels_sitting_room",
    "cuff_investigates": "verinder_house",
    "rosanna_hides_nightgown": "shivering_sand",
    "rosanna_suicide": "shivering_sand",
    "godfrey_pledges": "lukers_bank",
    "lady_verinder_death": "lady_verinder_london",
    "nightgown_discovery": "shivering_sand",
    "jennings_reconstruction": "dr_candys_house",
    "opium_experiment": "rachels_sitting_room",  # Recreated
    "godfrey_murdered": "wheel_of_fortune",
    "diamond_restored": "somnauth_shrine",
}


def build_location_graph():
    """Build the location graph with spatial relationships."""
    G = nx.DiGraph()

    # Add location nodes
    for loc_id, loc_data in LOCATIONS.items():
        # Filter out None values and convert booleans for GraphML compatibility
        attrs = {
            "description": loc_data["description"],
            "location_type": loc_data["type"],
        }
        if loc_data.get("parent"):
            attrs["parent"] = loc_data["parent"]
        for k, v in loc_data.items():
            if k not in ["description", "type", "parent"] and v is not None:
                # Convert booleans to strings for GraphML
                attrs[k] = str(v) if isinstance(v, bool) else v
        G.add_node(loc_id, **attrs)

    # Add spatial edges
    for source, target, rel_type in SPATIAL_EDGES:
        G.add_edge(source, target,
                   relationship=rel_type,
                   weight=1.0 if rel_type == "CONTAINS" else 0.5)

        # Make adjacency and perception bidirectional
        if rel_type in ["ADJACENT_TO", "VISIBLE_FROM", "AUDIBLE_FROM"]:
            G.add_edge(target, source,
                       relationship=rel_type,
                       weight=0.5)

    return G


def build_perception_matrix():
    """Build a matrix of what can be perceived from each location."""
    locations = list(LOCATIONS.keys())

    # For each location, calculate what other locations are perceptible
    perception = {}

    for loc in locations:
        perception[loc] = {
            "visible": [],
            "audible": [],
            "accessible": [],
        }

    for source, target, rel_type in SPATIAL_EDGES:
        if rel_type == "VISIBLE_FROM":
            perception[source]["visible"].append(target)
            perception[target]["visible"].append(source)
        elif rel_type == "AUDIBLE_FROM":
            perception[source]["audible"].append(target)
            perception[target]["audible"].append(source)
        elif rel_type == "ADJACENT_TO":
            perception[source]["accessible"].append(target)
            perception[target]["accessible"].append(source)
        elif rel_type == "CONTAINS":
            # Child locations are accessible from parent
            perception[source]["accessible"].append(target)

    return perception


def analyze_location_graph(G):
    """Analyze the location graph for narrative implications."""
    analysis = {
        "total_locations": G.number_of_nodes(),
        "total_relationships": G.number_of_edges(),
        "location_types": {},
        "key_narrative_locations": [],
        "perception_constraints": [],
    }

    # Count by type
    for node, data in G.nodes(data=True):
        loc_type = data.get("location_type", "unknown")
        analysis["location_types"][loc_type] = analysis["location_types"].get(loc_type, 0) + 1

    # Identify key narrative locations (those with key_feature)
    for node, data in G.nodes(data=True):
        if data.get("key_feature"):
            analysis["key_narrative_locations"].append({
                "location": node,
                "feature": data["key_feature"]
            })

    # Document key perception constraints
    analysis["perception_constraints"] = [
        {
            "constraint": "Rachel could see into her sitting-room from her bedroom",
            "locations": ["rachels_bedroom", "rachels_sitting_room"],
            "implication": "She could witness Franklin without being seen"
        },
        {
            "constraint": "The first-floor corridor connects all guest bedrooms",
            "locations": ["first_floor_corridor", "franklins_room", "godfreys_room", "rachels_sitting_room"],
            "implication": "Godfrey could observe/follow Franklin from the corridor"
        },
        {
            "constraint": "Servants' quarters separate from family rooms",
            "locations": ["servants_hall", "rosannas_room", "betteredges_room"],
            "implication": "Betteredge unaware of night events on upper floor"
        },
        {
            "constraint": "Shivering Sand accessible from both estate and Cobb's Hole",
            "locations": ["shivering_sand", "verinder_grounds", "cobbs_hole"],
            "implication": "Rosanna could reach it secretly; Limping Lucy could observe"
        },
    ]

    return analysis


def export_graphs(output_dir: Path):
    """Export location graph in multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build graph
    G = build_location_graph()

    # Export graph formats
    nx.write_graphml(G, output_dir / "location_graph.graphml")
    nx.write_gexf(G, output_dir / "location_graph.gexf")

    # Export JSON
    location_json = nx.node_link_data(G)
    with open(output_dir / "location_graph.json", "w") as f:
        json.dump(location_json, f, indent=2)

    # Export raw data
    with open(output_dir / "location_data.json", "w") as f:
        json.dump({
            "locations": LOCATIONS,
            "spatial_edges": SPATIAL_EDGES,
            "event_locations": EVENT_LOCATIONS
        }, f, indent=2)

    # Build and export perception matrix
    perception = build_perception_matrix()
    with open(output_dir / "perception_matrix.json", "w") as f:
        json.dump(perception, f, indent=2)

    # Analyze and export
    analysis = analyze_location_graph(G)
    with open(output_dir / "location_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"Location Graph: {G.number_of_nodes()} locations, {G.number_of_edges()} relationships")
    print(f"Key narrative locations: {len(analysis['key_narrative_locations'])}")

    return G


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_graphs(output_dir)
    print(f"\nLocation graph exported to {output_dir}")
