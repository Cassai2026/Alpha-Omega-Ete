import json
import os
from animus_registry import (
    ANIMUS_REGISTRY,
    get_pillar_registry,
    get_form as get_registry_form,
    get_abilities,
    get_mentor,
    get_all_registry_names,
    get_pillars_by_mentor,
)

# -----------------------------
# Animus Catalogue (player Animus from JSON)
# -----------------------------
CATALOGUE_FILE = os.path.join(os.path.dirname(__file__), "Animus_catalogue.json")


def load_catalogue(filepath=CATALOGUE_FILE):
    """Load the Animus catalogue from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_catalogue(data, filepath=CATALOGUE_FILE):
    """Save the Animus catalogue back to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_all_animus_names(data=None):
    """Return a list of all Animus names in the catalogue."""
    if data is None:
        data = load_catalogue()
    return list(data["animus_entries"].keys())


def get_animus(name, data=None):
    """Return the full entry for a single Animus by name, or None."""
    if data is None:
        data = load_catalogue()
    return data["animus_entries"].get(name)


def add_animus(name, entry, data=None, auto_save=True):
    """Add a new Animus to the catalogue."""
    if data is None:
        data = load_catalogue()

    required_keys = {
        "title", "class", "mentor", "description", "category",
        "pillar_alignment", "strengths", "xp_bonus",
        "xp_bonus_tasks", "shadow_trait_interaction",
        "shadow_risk", "mentor_note"
    }
    missing = required_keys - set(entry.keys())
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    if name in data["animus_entries"]:
        raise ValueError(f"Animus '{name}' already exists. Use update_animus() instead.")

    data["animus_entries"][name] = entry
    if auto_save:
        save_catalogue(data)
    return data


def update_animus(name, updates, data=None, auto_save=True):
    """Update an existing Animus entry with partial field updates."""
    if data is None:
        data = load_catalogue()

    if name not in data["animus_entries"]:
        raise KeyError(f"Animus '{name}' not found in catalogue.")

    data["animus_entries"][name].update(updates)
    if auto_save:
        save_catalogue(data)
    return data


def remove_animus(name, data=None, auto_save=True):
    """Remove an Animus from the catalogue."""
    if data is None:
        data = load_catalogue()

    if name not in data["animus_entries"]:
        raise KeyError(f"Animus '{name}' not found in catalogue.")

    del data["animus_entries"][name]
    if auto_save:
        save_catalogue(data)
    return data


def calculate_xp(base_xp, animus_name, data=None):
    """Apply an Animus's XP bonus to a base XP amount."""
    entry = get_animus(animus_name, data)
    if entry is None:
        return base_xp

    bonus = entry.get("xp_bonus", {})
    bonus_type = bonus.get("type", "flat")
    value = bonus.get("value", 0)

    if bonus_type == "multiplier":
        return int(base_xp * value)
    elif bonus_type == "flat":
        return base_xp + value
    return base_xp


def display_catalogue(data=None):
    """Pretty-print the full Animus catalogue to the console."""
    if data is None:
        data = load_catalogue()

    print(f"\n{'='*60}")
    print(f"  ANIMUS CATALOGUE  (v{data.get('version', '?')})")
    print(f"  System: {data.get('system', 'unknown')}")
    print(f"  Last updated: {data.get('last_updated', 'unknown')}")
    print(f"{'='*60}\n")

    for i, (name, info) in enumerate(data["animus_entries"].items(), start=1):
        pillars = ", ".join(info.get("pillar_alignment", []))
        strengths = ", ".join(info.get("strengths", []))
        risks = ", ".join(info.get("shadow_risk", []))
        tasks = ", ".join(info.get("xp_bonus_tasks", []))
        print(f"  {i:>2}. {name} [{info['class']}]")
        print(f"      Mentor:     {info['mentor']}")
        print(f"      {info['description']}")
        print(f"      Strengths:  {strengths}")
        print(f"      XP Tasks:   {tasks}")
        print(f"      Shadow:     {info['shadow_trait_interaction']} | Risks: {risks}")
        print(f"      Pillars:    {pillars}")
        print()


# -----------------------------
# Animus Registry Access (Eternius pillar forms)
# -----------------------------

def list_animus_pillars():
    """Return a list of all pillar names from the registry."""
    return get_all_registry_names()


def get_animus_forms(pillar_name):
    """
    Return all three forms (omega, ultima, eternium) for a pillar.

    Returns:    
        dict with 'omega', 'ultima', 'eternium' keys, or None.
    """
    pillar = get_pillar_registry(pillar_name)
    if pillar is None:
        return None
    return pillar.get("forms")


def get_animus_form(pillar_name, form_name):
    """
    Return a specific form for a pillar.

    Parameters:
        pillar_name: Name of the pillar (e.g. "Janus")
        form_name:   "omega", "ultima", or "eternium"

    Returns:
        dict with name, description, abilities — or None.
    """
    return get_registry_form(pillar_name, form_name)


def get_animus_abilities(pillar_name, form_name):
    """
    Return the abilities list for a specific pillar and form.

    Returns:
        list of ability strings, or None.
    """
    return get_abilities(pillar_name, form_name)


def get_animus_mentor(pillar_name):
    """Return the mentor name for a pillar, or None."""
    return get_mentor(pillar_name)


def get_animus_pillars_by_mentor(mentor_name):
    """
    Return all pillar names assigned to a given mentor.

    Parameters:
        mentor_name: "KONG", "Hekete", or "ODIN"
    """
    return get_pillars_by_mentor(mentor_name)