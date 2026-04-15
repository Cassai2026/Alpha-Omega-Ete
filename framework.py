import json
import os

# -----------------------------
# Animus Framework (Celestial Triad + 12 Pillars)
# -----------------------------
FRAMEWORK_FILE = os.path.join(os.path.dirname(__file__), "Animus_framework.json")


def load_framework(filepath=FRAMEWORK_FILE):
    """Load the Animus Framework from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_framework(data, filepath=FRAMEWORK_FILE):
    """Save the Animus Framework back to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ----- Celestial Triad -----

def get_triad(data=None):
    """Return the full Celestial Triad dict."""
    if data is None:
        data = load_framework()
    return data["celestial_triad"]


def get_triad_member(name, data=None):
    """Return a single Celestial Triad member by name, or None."""
    if data is None:
        data = load_framework()
    return data["celestial_triad"].get(name)


def get_mentor_forms(name, data=None):
    """Return the forms (prime/lumen/umbra) for a Celestial Triad member."""
    member = get_triad_member(name, data)
    if member is None:
        return None
    return member.get("forms", {})


# ----- 12 Pillars -----

def get_all_pillars(data=None):
    """Return the full pillars dict."""
    if data is None:
        data = load_framework()
    return data["pillars"]


def get_pillar(name, data=None):
    """Return a single pillar entry by name, or None."""
    if data is None:
        data = load_framework()
    return data["pillars"].get(name)


def get_pillar_by_virtue(virtue, data=None):
    """Find a pillar by its virtue. Returns (name, entry) or None."""
    if data is None:
        data = load_framework()
    for name, entry in data["pillars"].items():
        if entry["virtue"].lower() == virtue.lower():
            return (name, entry)
    return None


def get_pillar_by_sin(sin, data=None):
    """Find a pillar by its sin. Returns (name, entry) or None."""
    if data is None:
        data = load_framework()
    for name, entry in data["pillars"].items():
        if entry["sin"].lower() == sin.lower():
            return (name, entry)
    return None


def get_form(pillar_name, form_type, data=None):
    """
    Get a specific form for a pillar.

    Parameters:
        pillar_name: Name of the pillar (e.g. "Janus")
        form_type:   "lumen" or "umbra"

    Returns:
        Form string or None.
    """
    pillar = get_pillar(pillar_name, data)
    if pillar is None:
        return None
    return pillar.get("forms", {}).get(form_type)


# ----- Display -----

def display_framework(data=None):
    """Pretty-print the full Animus Framework to the console."""
    if data is None:
        data = load_framework()

    print(f"\n{'='*60}")
    print(f"  {data.get('system', 'Animus Framework')}  (v{data.get('version', '?')})")
    print(f"  Total entities: {data.get('total_entities', '?')}")
    print(f"{'='*60}")

    # Celestial Triad
    print(f"\n  --- CELESTIAL TRIAD ---\n")
    for name, info in data["celestial_triad"].items():
        forms = info.get("forms", {})
        print(f"  ? {name}  [{info['tier']}]")
        print(f"    Domain: {info['domain']}")
        print(f"    Role:   {info['role']}")
        print(f"    Forms:  Prime: {forms.get('prime', '—')}")
        print(f"            Lumen: {forms.get('lumen', '—')}")
        print(f"            Umbra: {forms.get('umbra', '—')}")
        print()

    # 12 Pillars
    print(f"  --- 12 PILLARS ---\n")
    for i, (name, info) in enumerate(data["pillars"].items(), start=1):
        forms = info.get("forms", {})
        print(f"  {i:>2}. {name}")
        print(f"      Virtue: {info['virtue']}  |  Sin: {info['sin']}")
        print(f"      Lumen:  {forms.get('lumen', '—')}")
        print(f"      Umbra:  {forms.get('umbra', '—')}")
        print()