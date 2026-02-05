"""
Counterfactuals data management.

Load, save, and manipulate the counterfactuals inventory.
"""

import json
from pathlib import Path


def load_counterfactuals(graphs_dir: Path) -> dict:
    """Load counterfactuals data."""
    path = graphs_dir / "counterfactuals.json"
    with open(path) as f:
        return json.load(f)


def save_counterfactuals(graphs_dir: Path, data: dict):
    """Save counterfactuals data."""
    path = graphs_dir / "counterfactuals.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_hinge(data: dict, hinge_id: str) -> dict | None:
    """Get a specific hinge by ID."""
    for hinge in data["hinges"]:
        if hinge["id"] == hinge_id:
            return hinge
    return None


def add_alternative(data: dict, hinge_id: str, alternative: dict) -> bool:
    """Add an alternative to a hinge. Returns True if successful."""
    hinge = get_hinge(data, hinge_id)
    if hinge is None:
        return False

    # Generate ID if not provided
    if "id" not in alternative:
        existing_ids = [a["id"] for a in hinge["alternatives"]]
        base_id = f"{hinge_id}_alt"
        counter = len(existing_ids) + 1
        while f"{base_id}_{counter}" in existing_ids:
            counter += 1
        alternative["id"] = f"{base_id}_{counter}"

    hinge["alternatives"].append(alternative)
    return True


def update_alternative(data: dict, hinge_id: str, alt_id: str, updates: dict) -> bool:
    """Update an existing alternative. Returns True if successful."""
    hinge = get_hinge(data, hinge_id)
    if hinge is None:
        return False

    for alt in hinge["alternatives"]:
        if alt["id"] == alt_id:
            alt.update(updates)
            return True
    return False


def delete_alternative(data: dict, hinge_id: str, alt_id: str) -> bool:
    """Delete an alternative. Returns True if successful."""
    hinge = get_hinge(data, hinge_id)
    if hinge is None:
        return False

    original_len = len(hinge["alternatives"])
    hinge["alternatives"] = [a for a in hinge["alternatives"] if a["id"] != alt_id]
    return len(hinge["alternatives"]) < original_len


def get_all_hinge_ids(data: dict) -> list[str]:
    """Get list of all hinge IDs (for blocks dropdown)."""
    return [h["id"] for h in data["hinges"]]
