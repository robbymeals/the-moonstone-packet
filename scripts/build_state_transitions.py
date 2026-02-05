"""
Probabilistic State Transition Model for The Moonstone

Models narrative as a sequence of state transitions with subjective probabilities.
For each transition: P(what actually happened) vs P(anything else)

This quantifies how "inevitable" vs "surprising" each narrative turn was.

Uses pyAgrum for Bayesian network inference.
"""

import json
import pyagrum as gum
import networkx as nx
from pathlib import Path

# Narrative states and transitions
# Format: each state has prior conditions and the transition that occurred
# We assign P(actual outcome | prior state) subjectively

STATE_TRANSITIONS = [
    {
        "id": "T01",
        "prior_state": "Herncastle at Seringapatam, diamond guarded by priests",
        "transition": "Herncastle steals the diamond",
        "actual_outcome": "steals_diamond",
        "prior_factors": [
            "Herncastle is morally corrupt",
            "Siege provides cover",
            "Diamond is unprotected moment",
            "Herncastle has motive (greed/obsession)",
        ],
        "p_actual": 0.6,  # Given his character, somewhat likely but not inevitable
        "p_other": 0.4,   # Could have been stopped, killed, or chosen not to
        "counterfactuals": [
            "Herncastle killed in siege",
            "Priests successfully defend",
            "Herncastle has attack of conscience",
            "Another soldier gets there first",
        ],
        "inevitability": "moderate",  # Story needs this, but it's a choice
    },
    {
        "id": "T02",
        "prior_state": "Herncastle has diamond, family ostracizes him, he's dying",
        "transition": "Herncastle bequeaths diamond to Rachel",
        "actual_outcome": "bequeaths_to_rachel",
        "prior_factors": [
            "Herncastle is vindictive/bitter",
            "Rachel is innocent/vulnerable",
            "Herncastle wants to spread the curse/trouble",
            "Or: genuine affection for niece",
        ],
        "p_actual": 0.5,  # Could have destroyed it, sold it, kept it hidden
        "p_other": 0.5,
        "counterfactuals": [
            "Diamond destroyed",
            "Sold to collector",
            "Left to museum",
            "Buried with him",
        ],
        "inevitability": "contingent",  # This is the inciting incident - it's a choice
    },
    {
        "id": "T03",
        "prior_state": "Diamond at Verinder house, birthday dinner, Franklin protective",
        "transition": "Dr. Candy doses Franklin with laudanum",
        "actual_outcome": "candy_doses_franklin",
        "prior_factors": [
            "Candy offended by Franklin's dinner remarks",
            "Candy has professional pride wounded",
            "Candy has access to laudanum",
            "Victorian culture of casual drugging",
        ],
        "p_actual": 0.15,  # This is VERY unlikely - it's the twist
        "p_other": 0.85,
        "counterfactuals": [
            "Candy lets insult go",
            "Candy confronts Franklin directly",
            "Someone notices the drugging",
            "Candy lacks opportunity",
        ],
        "inevitability": "surprising",  # Key twist - low probability
    },
    {
        "id": "T04",
        "prior_state": "Franklin drugged, anxious about diamond, paint wet on door",
        "transition": "Franklin takes diamond while unconscious",
        "actual_outcome": "franklin_takes_diamond",
        "prior_factors": [
            "Laudanum effects on memory and volition",
            "Franklin's anxiety about diamond security",
            "Somnambulism is documented effect",
            "No obstacles between rooms",
        ],
        "p_actual": 0.7,  # Given the drugging, his acting on anxiety is likely
        "p_other": 0.3,
        "counterfactuals": [
            "Franklin sleeps through the night",
            "Franklin wakes up normally",
            "Someone intercepts him",
        ],
        "inevitability": "likely_given_prior",  # Follows from the drugging
    },
    {
        "id": "T05",
        "prior_state": "Franklin has taken diamond to his room unconsciously",
        "transition": "Godfrey steals diamond from Franklin",
        "actual_outcome": "godfrey_steals",
        "prior_factors": [
            "Godfrey is awake (why?)",
            "Godfrey has financial desperation",
            "Godfrey sees opportunity",
            "Franklin is unconscious/vulnerable",
        ],
        "p_actual": 0.4,  # Requires Godfrey to be in right place + right state
        "p_other": 0.6,
        "counterfactuals": [
            "Godfrey asleep",
            "Godfrey doesn't see Franklin",
            "Franklin wakes",
            "Godfrey has moral qualm",
        ],
        "inevitability": "moderate",  # Opportunistic - needs circumstances
    },
    {
        "id": "T06",
        "prior_state": "Rachel saw Franklin take diamond, believes he stole it",
        "transition": "Rachel maintains silence to protect Franklin",
        "actual_outcome": "rachel_silent",
        "prior_factors": [
            "Rachel loves Franklin",
            "Rachel has fierce pride/principles",
            "Rachel would rather suffer than betray",
            "Victorian women expected to be passive",
        ],
        "p_actual": 0.8,  # Given her character, this is very likely
        "p_other": 0.2,
        "counterfactuals": [
            "Rachel tells her mother",
            "Rachel confronts Franklin",
            "Rachel tells Cuff",
        ],
        "inevitability": "highly_likely",  # Character-driven
    },
    {
        "id": "T07",
        "prior_state": "Rosanna finds stained nightgown, loves Franklin",
        "transition": "Rosanna hides the evidence",
        "actual_outcome": "rosanna_hides_evidence",
        "prior_factors": [
            "Rosanna's love for Franklin",
            "Rosanna's outsider status (former thief)",
            "Rosanna's desperation",
            "Rosanna can access Shivering Sand",
        ],
        "p_actual": 0.75,  # Given her love, very likely
        "p_other": 0.25,
        "counterfactuals": [
            "Rosanna reports to Betteredge",
            "Rosanna confronts Franklin",
            "Rosanna uses evidence as leverage",
        ],
        "inevitability": "highly_likely",  # Character-driven
    },
    {
        "id": "T08",
        "prior_state": "Rosanna has hidden evidence, Franklin oblivious, she despairs",
        "transition": "Rosanna commits suicide",
        "actual_outcome": "rosanna_suicide",
        "prior_factors": [
            "Rosanna's hopeless love",
            "Rosanna's isolation",
            "Victorian limited options for women of her class",
            "The Shivering Sand nearby",
        ],
        "p_actual": 0.4,  # Tragic but not inevitable
        "p_other": 0.6,
        "counterfactuals": [
            "Rosanna lives with secret",
            "Rosanna leaves service",
            "Someone notices her distress",
            "Franklin shows her kindness",
        ],
        "inevitability": "moderate",  # Tragic convergence of factors
    },
    {
        "id": "T09",
        "prior_state": "Diamond at Luker's for a year, Godfrey desperate, pledge expires",
        "transition": "Godfrey reclaims diamond to flee",
        "actual_outcome": "godfrey_reclaims",
        "prior_factors": [
            "Pledge term expiring",
            "Godfrey's embezzlement about to be discovered",
            "Diamond is his only escape",
        ],
        "p_actual": 0.9,  # Almost inevitable given his situation
        "p_other": 0.1,
        "counterfactuals": [
            "Godfrey confesses",
            "Godfrey found dead before",
            "Trust discovery happens first",
        ],
        "inevitability": "nearly_inevitable",  # Trapped
    },
    {
        "id": "T10",
        "prior_state": "Godfrey has diamond, Indians have tracked it for 50 years",
        "transition": "Indians kill Godfrey, recover diamond",
        "actual_outcome": "indians_kill_godfrey",
        "prior_factors": [
            "Indians' 50-year sacred mission",
            "They've been patient and determined",
            "Godfrey is alone and vulnerable",
            "No witnesses at the inn",
        ],
        "p_actual": 0.85,  # Their whole purpose
        "p_other": 0.15,
        "counterfactuals": [
            "Godfrey escapes",
            "Police intervene",
            "Indians captured before",
        ],
        "inevitability": "highly_likely",  # Narrative destiny
    },
    {
        "id": "T11",
        "prior_state": "Franklin confused, Rachel hostile, evidence hidden",
        "transition": "Ezra Jennings discovers the truth",
        "actual_outcome": "jennings_discovers",
        "prior_factors": [
            "Jennings has Candy's fever-notes",
            "Jennings is brilliant and desperate for meaning",
            "Jennings understands opium",
            "Franklin seeks help",
        ],
        "p_actual": 0.3,  # Unlikely concatenation
        "p_other": 0.7,
        "counterfactuals": [
            "Candy dies without raving",
            "Jennings doesn't record ravings",
            "Jennings doesn't meet Franklin",
            "Pattern never emerges",
        ],
        "inevitability": "surprising",  # The detective-story resolution
    },
]


def build_transition_network():
    """Build NetworkX graph of state transitions."""
    G = nx.DiGraph()

    for i, t in enumerate(STATE_TRANSITIONS):
        # Add state node
        state_id = f"S{i:02d}"
        G.add_node(state_id,
                   description=t["prior_state"],
                   node_type="state")

        # Add outcome node
        outcome_id = t["id"]
        G.add_node(outcome_id,
                   description=t["transition"],
                   actual_outcome=t["actual_outcome"],
                   p_actual=t["p_actual"],
                   p_other=t["p_other"],
                   inevitability=t["inevitability"],
                   node_type="transition")

        # Add edge from state to transition
        G.add_edge(state_id, outcome_id,
                   factors="; ".join(t["prior_factors"]))

        # Add edge to next state (if not last)
        if i < len(STATE_TRANSITIONS) - 1:
            next_state_id = f"S{i+1:02d}"
            G.add_edge(outcome_id, next_state_id)

    return G


def build_bayesian_model():
    """Build pyAgrum Bayesian Network for probabilistic inference."""
    bn = gum.BayesNet("MoonstoneStateTransitions")

    # Create variables for each transition
    transition_vars = {}
    for t in STATE_TRANSITIONS:
        var = gum.LabelizedVariable(t["id"], t["transition"][:30], 2)
        var.changeLabel(0, "other")
        var.changeLabel(1, "actual")
        transition_vars[t["id"]] = bn.add(var)

    # Add arcs for sequential dependencies
    for i in range(len(STATE_TRANSITIONS) - 1):
        current_id = STATE_TRANSITIONS[i]["id"]
        next_id = STATE_TRANSITIONS[i + 1]["id"]
        bn.addArc(transition_vars[current_id], transition_vars[next_id])

    # Set CPTs
    for i, t in enumerate(STATE_TRANSITIONS):
        tid = t["id"]
        p_actual = t["p_actual"]
        p_other = 1 - p_actual

        if i == 0:
            # Root node - simple probability
            bn.cpt(tid).fillWith([p_other, p_actual])
        else:
            # Conditional on previous transition happening
            # If previous happened (actual), this probability applies
            # If previous didn't happen (other), story doesn't continue as written
            cpt = bn.cpt(tid)

            # When parent is "other" (story diverged), very low probability
            # When parent is "actual" (story continues), normal probability
            cpt[{"other": 0}] = [0.99, 0.01]  # If story diverged, almost nothing continues
            cpt[{"other": 1}] = [p_other, p_actual]  # If story continues, normal probs

    return bn


def compute_chain_probability():
    """Compute probability of the entire chain of events as written."""
    p_chain = 1.0
    for t in STATE_TRANSITIONS:
        p_chain *= t["p_actual"]

    return p_chain


def compute_surprise_scores():
    """Compute information-theoretic surprise for each transition."""
    import math

    scores = []
    for t in STATE_TRANSITIONS:
        p = t["p_actual"]
        # Surprise = -log2(p) = information content in bits
        surprise = -math.log2(p) if p > 0 else float('inf')
        scores.append({
            "id": t["id"],
            "transition": t["transition"],
            "p_actual": p,
            "surprise_bits": surprise,
            "inevitability": t["inevitability"],
        })

    return sorted(scores, key=lambda x: x["surprise_bits"], reverse=True)


def export_model(output_dir: Path):
    """Export all probabilistic model artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build and export NetworkX graph
    G = build_transition_network()
    nx.write_graphml(G, output_dir / "state_transitions.graphml")
    nx.write_gexf(G, output_dir / "state_transitions.gexf")

    # Export JSON
    graph_json = nx.node_link_data(G)
    with open(output_dir / "state_transitions.json", "w") as f:
        json.dump(graph_json, f, indent=2)

    # Build and export Bayesian Network
    try:
        bn = build_bayesian_model()
        gum.saveBN(bn, str(output_dir / "state_transitions.bif"))
        gum.saveBN(bn, str(output_dir / "state_transitions.bifxml"))
        print(f"Bayesian Network: {bn.size()} nodes, {bn.sizeArcs()} arcs")
    except Exception as e:
        print(f"Warning: Could not build Bayesian Network: {e}")

    # Compute and export analysis
    chain_prob = compute_chain_probability()
    surprise_scores = compute_surprise_scores()

    analysis = {
        "chain_probability": chain_prob,
        "chain_probability_log10": -1 * (1 - chain_prob) if chain_prob > 0 else None,
        "total_transitions": len(STATE_TRANSITIONS),
        "most_surprising": surprise_scores[:3],
        "most_inevitable": surprise_scores[-3:],
        "average_p_actual": sum(t["p_actual"] for t in STATE_TRANSITIONS) / len(STATE_TRANSITIONS),
    }

    with open(output_dir / "state_transition_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    # Export raw transition data
    with open(output_dir / "state_transition_data.json", "w") as f:
        json.dump(STATE_TRANSITIONS, f, indent=2)

    print(f"\nState Transitions: {len(STATE_TRANSITIONS)} transitions modeled")
    print(f"Chain probability (all events as written): {chain_prob:.6f}")
    print(f"Most surprising transition: {surprise_scores[0]['transition']} (P={surprise_scores[0]['p_actual']:.2f})")

    return G


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    export_model(output_dir)
    print(f"\nState transition model exported to {output_dir}")
