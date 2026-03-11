# -----------------------------
# Eternius Animus — Module 1: The Awakening
#
# The player begins inside Lilieth's Prime Void form —
# The All-Devouring. This is the unformed state before
# the 14 pillars. The first mission introduces the player
# to the Void, presents a primordial choice, and opens
# the gate to the first Animus stage (Janus).
#
# Design rule: Animus are NOT permanent player classes.
# Every player progresses through all 14 Animus in sequence.
# Each Animus is a trial, a chapter, a gate.
# -----------------------------

import random
from animus import (
    load_catalogue,
    get_animus_form,
)
from shadow_traits import get_traits_by_tier, PILLAR_TRAITS
from mentor import (
    get_mentor_profile,
    get_mentor_guidance,
    get_mentor_form_response,
    get_shadow_encounter_response,
)
from animus_registry import get_pillar_registry


# -----------------------------
# Lilieth — Prime Void / The All-Devouring
# -----------------------------

LILIETH = {
    "name": "Lilieth",
    "title": "The All-Devouring",
    "tier": "Prime Origin",
    "domain": "The Void Before Creation",
    "description": (
        "Before the pillars. Before the mentors. Before the world had shape. "
        "There was hunger. A mind without boundary. A voice that whispered "
        "from the dark between stars. Lilieth. Not mother. Not monster. Origin."
    ),
    "other_titles": [
        "Mother of Silence",
        "Devourer of Truths",
        "The First Hunger",
        "The Abyssal Matriarch",
        "The Primordial Mind",
    ],
    "forms": {
        "prime_void": {
            "name": "The All-Devouring",
            "description": "Primordial consciousness before order. Raw creation. Raw destruction. Uncontained potential.",
            "abilities": [
                "consume",
                "whisper",
                "devour",
            ],
        },
        "omega": {
            "name": "The First Mother",
            "description": "The void remembers what it created. Hunger becomes nurture. Destruction becomes protection.",
            "abilities": [
                "birth_of_pillars",
                "memory_of_void",
                "origin_shield",
            ],
        },
        "eternium": {
            "name": "The Infinite Mind",
            "description": "Lilieth transcended. The origin and the destination are one. All pillars exist within her.",
            "abilities": [
                "cosmic_integration",
                "void_sovereignty",
                "eternal_origin",
            ],
        },
    },
    "void_abilities": {
        "consume": {
            "name": "Consume",
            "description": "Absorb knowledge, memories, or experiences.",
            "effect": "Gain XP from shadow encounters instead of losing it.",
        },
        "whisper": {
            "name": "Whisper",
            "description": "Influence choices without revealing truth.",
            "effect": "Reveal hidden pillar traits before choosing.",
        },
        "devour": {
            "name": "Devour",
            "description": "Break existing structures.",
            "effect": "Reset negative shadow effects.",
        },
    },
    "whispers": [
        "You are not awake. You are remembering.",
        "The pillars are not ahead of you. They are inside you. Fractured.",
        "I am what you were before you forgot.",
        "Do not seek the light. Do not flee the dark. Seek yourself.",
        "Every gate you open was always yours.",
        "The mentors will guide you. But I made the mentors.",
        "You think this is the beginning. It is not. It is the return.",
    ],
}


# -----------------------------
# Progression Map — 14 Stages
# -----------------------------

ANIMUS_STAGES = [
    {"stage": 1,  "pillar": "Janus",       "mentor": "ODIN",   "gate": "The Gate of Two Faces"},
    {"stage": 2,  "pillar": "Jormungandr",  "mentor": "ODIN",   "gate": "The Coil of Balance"},
    {"stage": 3,  "pillar": "Anubis",       "mentor": "ODIN",   "gate": "The Scales of the Dead"},
    {"stage": 4,  "pillar": "Apep",         "mentor": "KONG",   "gate": "The Serpent's Maw"},
    {"stage": 5,  "pillar": "Raven",        "mentor": "ODIN",   "gate": "The Whispering Archive"},
    {"stage": 6,  "pillar": "Ravana",       "mentor": "KONG",   "gate": "The Throne of Ten Crowns"},
    {"stage": 7,  "pillar": "Vali",         "mentor": "KONG",   "gate": "The Forge of Fury"},
    {"stage": 8,  "pillar": "Vritra",       "mentor": "KONG",   "gate": "The Eye of the Storm"},
    {"stage": 9,  "pillar": "Iris",         "mentor": "Hekete", "gate": "The Prismatic Bridge"},
    {"stage": 10, "pillar": "Iblis",        "mentor": "Hekete", "gate": "The Flame of Defiance"},
    {"stage": 11, "pillar": "Sigyn",        "mentor": "Hekete", "gate": "The Bowl of Tears"},
    {"stage": 12, "pillar": "Set",          "mentor": "KONG",   "gate": "The Desert of Betrayal"},
    {"stage": 13, "pillar": "Pillar13",     "mentor": "TBD",    "gate": "The Unknown Gate"},
    {"stage": 14, "pillar": "Pillar14",     "mentor": "TBD",    "gate": "The Final Gate"},
]


# -----------------------------
# Constants
# -----------------------------

BASE_XP_REWARD = 15
SHADOW_XP_PENALTY = 5
BONUS_XP_LIGHT = 10
VOID_XP_BONUS = 3
MODULE_NAME = "The Awakening"


# -----------------------------
# Internal Helpers
# -----------------------------

def get_stage(stage_number):
    """Return stage dict by number (1-based), or None."""
    for stage in ANIMUS_STAGES:
        if stage["stage"] == stage_number:
            return stage
    return None


def get_current_pillar_name(stage_number):
    """Return the pillar name for a given stage."""
    stage = get_stage(stage_number)
    if stage is None:
        return None
    return stage["pillar"]


def _pick_shadow_trait(pillar_name):
    """Pick a random shadow core trait for the encounter."""
    traits = get_traits_by_tier(pillar_name, "shadow", "core")
    if traits:
        return random.choice(traits)
    return {"name": "unknown_shadow", "description": "A shadow stirs within you."}


def _pick_light_trait(pillar_name):
    """Pick a random light core trait as the virtue anchor."""
    traits = get_traits_by_tier(pillar_name, "light", "core")
    if traits:
        return random.choice(traits)
    return {"name": "unknown_light", "description": "A light flickers inside you."}


def _lilieth_whisper():
    """Return a random Lilieth whisper."""
    return random.choice(LILIETH["whispers"])


def _build_void_choices(shadow_trait, light_trait):
    """
    Build 3 primordial choices for the Void awakening.
    Themed around Lilieth's void abilities.
    """
    shadow_name = shadow_trait["name"].replace("_", " ").title()
    light_name = light_trait["name"].replace("_", " ").title()

    return [
        {
            "label": f"Consume — Absorb {shadow_name}",
            "description": (
                f"Draw {shadow_name} into yourself. Transform its energy. "
                f"Let {light_name} emerge from what you devour."
            ),
            "path": "consume",
            "xp_modifier": BONUS_XP_LIGHT,
        },
        {
            "label": f"Whisper — Observe {shadow_name}",
            "description": (
                f"Do not act. Let {shadow_name} reveal its shape. "
                f"Understand it before you name it."
            ),
            "path": "whisper",
            "xp_modifier": VOID_XP_BONUS,
        },
        {
            "label": f"Devour — Destroy {shadow_name}",
            "description": (
                f"Unmake {shadow_name} entirely. Break the structure. "
                f"Leave nothing. Start clean."
            ),
            "path": "devour",
            "xp_modifier": -SHADOW_XP_PENALTY,
        },
    ]


def _resolve_void_choice(choice, shadow_trait, pillar_name, mentor_name):
    """Resolve the player's primordial choice and return outcome."""
    path = choice["path"]
    shadow_name = shadow_trait["name"].replace("_", " ").title()
    base_xp = BASE_XP_REWARD + choice["xp_modifier"]

    shadow_responses = get_shadow_encounter_response("Lilith") or []
    mentor_guidance = get_mentor_guidance(mentor_name, "core") or []

    if path == "consume":
        outcome = (
            f"You drew {shadow_name} into yourself. It burned — then transformed. "
            f"The shadow became fuel. The first light stirs."
        )
        lilieth_line = "You begin to remember what you are."
        mentor_line = random.choice(mentor_guidance) if mentor_guidance else ""

    elif path == "whisper":
        outcome = (
            f"You watched {shadow_name} without moving. It circled you, "
            f"tested you, then revealed its true shape. You understand it now."
        )
        lilieth_line = "Patience. The void rewards those who listen."
        mentor_line = random.choice(shadow_responses) if shadow_responses else ""

    else:  # devour
        outcome = (
            f"You unmade {shadow_name}. It shattered into fragments. "
            f"The void is clean — but emptier. Something was lost."
        )
        lilieth_line = "Destruction is easy. Creation is the test."
        mentor_line = random.choice(shadow_responses) if shadow_responses else ""

    return {
        "outcome_text": outcome,
        "lilieth_line": lilieth_line,
        "mentor_line": mentor_line,
        "xp_earned": max(base_xp, 0),
        "path_taken": path,
    }


# -----------------------------
# Main Module Entry Point
# -----------------------------

def run_module(player_name, stage_number=1):
    """
    Run The Awakening — first CassWorld mission.

    The player awakens inside Lilieth's Prime Void form
    and must face the first shadow of the first pillar
    to unlock Stage 1 of the Animus progression.

    Parameters:
        player_name:  Display name for the player.
        stage_number: Which Animus stage to enter (default 1 = Janus).

    Returns:
        dict with keys:
            completed, module, player, origin_form, current_animus,
            pillar, mentor, gate, shadow_trait, light_trait,
            path_taken, xp_earned, outcome_text, lilieth_line,
            mentor_line, next_stage_unlocked
    """
    stage = get_stage(stage_number)
    if stage is None:
        print(f"\n  [ERROR] Stage {stage_number} not found.")
        return {"completed": False, "error": f"Stage {stage_number} not found."}

    pillar_name = stage["pillar"]
    mentor_name = stage["mentor"]
    gate_name = stage["gate"]

    pillar_data = get_pillar_registry(pillar_name)
    mentor_profile = get_mentor_profile(mentor_name)
    mentor_title = mentor_profile["title"] if mentor_profile else mentor_name

    shadow_trait = _pick_shadow_trait(pillar_name)
    light_trait = _pick_light_trait(pillar_name)

    # ===== THE VOID =====
    print(f"\n{'='*60}")
    print(f"  THE VOID")
    print(f"{'='*60}")
    print()
    print(f"  {LILIETH['description']}")
    print()
    print(f"  And you...")
    print(f"  You awaken within her shadow.")
    print()
    print(f"  [LILIETH]: \"{_lilieth_whisper()}\"")

    # ===== GATE REVEAL =====
    print(f"\n{'='*60}")
    print(f"  MODULE 1: {MODULE_NAME.upper()}")
    print(f"  Stage {stage_number} — {gate_name}")
    print(f"{'='*60}")
    print(f"\n  Player:  {player_name}")
    print(f"  Animus:  {pillar_name} (Stage {stage_number} of 14)")
    print(f"  Mentor:  {mentor_name} — {mentor_title}")
    if pillar_data:
        print(f"  Virtue:  {pillar_data.get('virtue', '?')}")
        print(f"  Sin:     {pillar_data.get('sin', '?')}")

    # ===== LILIETH SPEAKS =====
    print(f"\n  --- Lilieth speaks from the Void ---")
    print(f"  [LILIETH]: \"{_lilieth_whisper()}\"")

    # ===== MENTOR ARRIVES =====
    guidance = get_mentor_guidance(mentor_name, "core")
    if guidance:
        print(f"\n  --- {mentor_name} steps forward ---")
        print(f"  [{mentor_name}]: \"{random.choice(guidance)}\"")

    # ===== SHADOW ENCOUNTER =====
    shadow_display = shadow_trait["name"].replace("_", " ").title()
    light_display = light_trait["name"].replace("_", " ").title()

    print(f"\n  --- The First Shadow ---")
    print(f"  From the void, a shape forms: {shadow_display}")
    print(f"  \"{shadow_trait['description']}\"")
    print()
    print(f"  But within you, something responds: {light_display}")
    print(f"  \"{light_trait['description']}\"")
    print()

    # ===== CHOICES =====
    choices = _build_void_choices(shadow_trait, light_trait)

    for i, c in enumerate(choices, start=1):
        print(f"  [{i}] {c['label']}")
        print(f"      {c['description']}")

    # ===== INPUT =====
    selected = None
    while selected is None:
        try:
            raw = input(f"\n  Choose (1-3): ").strip()
            idx = int(raw)
            if 1 <= idx <= 3:
                selected = choices[idx - 1]
            else:
                print("  Enter 1, 2, or 3.")
        except ValueError:
            print("  Enter 1, 2, or 3.")

    # ===== RESOLVE =====
    result = _resolve_void_choice(selected, shadow_trait, pillar_name, mentor_name)

    print(f"\n  --- Outcome ---")
    print(f"  {result['outcome_text']}")
    print(f"\n  [LILIETH]: \"{result['lilieth_line']}\"")
    if result["mentor_line"]:
        print(f"  [{mentor_name}]: \"{result['mentor_line']}\"")
    print(f"\n  XP earned: +{result['xp_earned']}")

    # ===== OMEGA FORM HINT =====
    omega_form = get_animus_form(pillar_name, "omega")
    if omega_form:
        print(f"\n  --- Gate Opening ---")
        print(f"  The void parts. {gate_name} appears before you.")
        print(f"  Omega Form awaits: {omega_form['name']}")
        print(f"  \"{omega_form['description']}\"")
        form_response = get_mentor_form_response(mentor_name, "omega")
        if form_response:
            print(f"  [{mentor_name}]: \"{form_response}\"")

    # ===== NEXT STAGE =====
    next_stage = stage_number + 1 if stage_number < 14 else None
    next_stage_info = get_stage(next_stage) if next_stage else None

    if next_stage_info:
        print(f"\n  Next: Stage {next_stage} — {next_stage_info['gate']}")
    else:
        print(f"\n  All 14 gates have been revealed. The journey is complete.")

    # ===== SUMMARY =====
    print(f"\n{'='*60}")
    print(f"  {MODULE_NAME.upper()} — STAGE {stage_number} COMPLETE")
    print(f"{'='*60}\n")

    return {
        "completed": True,
        "module": MODULE_NAME,
        "player": player_name,
        "origin_form": "Lilieth - The All-Devouring",
        "current_animus": pillar_name,
        "pillar": pillar_name,
        "mentor": mentor_name,
        "gate": gate_name,
        "shadow_trait": shadow_trait["name"],
        "light_trait": light_trait["name"],
        "path_taken": result["path_taken"],
        "xp_earned": result["xp_earned"],
        "outcome_text": result["outcome_text"],
        "lilieth_line": result["lilieth_line"],
        "mentor_line": result["mentor_line"],
        "next_stage_unlocked": next_stage,
    }


# -----------------------------
# Standalone run
# -----------------------------
#if __name__ == "__main__":
#    run_module("Voyager", stage_number=1)