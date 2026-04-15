# -----------------------------
# CassWorld — Module 1: The Threshold
#
# The first playable mission.
# The player selects their Animus, navigates a 7x7 grid,
# encounters shadow traits drawn from their pillar alignment,
# receives dynamic mentor guidance, and unlocks the Omega form.
# -----------------------------

import random

from animus import (
    load_catalogue,
    get_animus,
    get_all_animus_names,
    calculate_xp,
    get_animus_form,
    get_animus_mentor,
    get_animus_pillars_by_mentor,
)
from shadow_traits import get_traits_by_tier
from mentor import (
    get_mentor_guidance,
    get_mentor_form_response,
    get_shadow_encounter_response,
)
from utils import (
    print_header,
    print_subheader,
    print_dialogue,
    print_blank,
    print_stat,
    print_divider,
    render_grid,
    get_choice,
    get_yes_no,
    format_trait_name,
    format_list,
)

# -----------------------------
# Mission constants
# -----------------------------
GRID_SIZE = 7
XP_TOKEN_COUNT = 5
SHADOW_TOKEN_COUNT = 3
OMEGA_UNLOCK_THRESHOLD = 25   # XP needed to unlock Omega form
MISSION_NAME = "The Threshold"


# -----------------------------
# Shadow encounter helpers
# -----------------------------

def _pick_shadow_trait(pillar_names, tier="core"):
    """
    Pick a random shadow trait from one of the player's aligned pillars.

    Parameters:
        pillar_names: list of pillar name strings from the player's Animus.
        tier:         "core", "developed", or "ascended"

    Returns:
        (pillar_name, trait_dict) tuple, or (None, None) if unavailable.
    """
    candidates = []
    for pillar in pillar_names:
        traits = get_traits_by_tier(pillar, "shadow", tier)
        if traits:
            for trait in traits:
                candidates.append((pillar, trait))
    if not candidates:
        return None, None
    return random.choice(candidates)


def _pick_light_trait(pillar_names, tier="core"):
    """
    Pick a random light trait from one of the player's aligned pillars.

    Returns:
        (pillar_name, trait_dict) tuple, or (None, None) if unavailable.
    """
    candidates = []
    for pillar in pillar_names:
        traits = get_traits_by_tier(pillar, "light", tier)
        if traits:
            for trait in traits:
                candidates.append((pillar, trait))
    if not candidates:
        return None, None
    return random.choice(candidates)


def _resolve_shadow_encounter(animus_entry, pillar_names, mentor_name, xp_total, tier="core"):
    """
    Handle a shadow trait encounter.

    Returns:
        xp_penalty (int) -- XP deducted from the encounter.
    """
    interaction = animus_entry.get("shadow_trait_interaction", "default")
    shadow_risks = animus_entry.get("shadow_risk", [])

    pillar, trait = _pick_shadow_trait(pillar_names, tier)

    print_subheader("SHADOW ENCOUNTER")

    if pillar and trait:
        trait_display = format_trait_name(trait["name"])
        print(f"  A shadow stirs within [{pillar}]: {trait_display}")
        print(f"  \"{trait['description']}\"")
        print_blank()
        if shadow_risks:
            risk = random.choice(shadow_risks)
            print(f"  Your shadow risk surfaces: {format_trait_name(risk)}")
    else:
        print("  A shadow stirs -- formless, but present.")
    print_blank()

    # Dynamic mentor guidance for this encounter
    encounter_prompts = get_shadow_encounter_response(mentor_name)
    if encounter_prompts:
        print_dialogue(mentor_name, random.choice(encounter_prompts))
    print_blank()

    # Resolve based on Animus interaction type
    if interaction == "bypass_once":
        print(f"  Your Animus bypasses this shadow entirely -- this time.")
        penalty = 0
    elif interaction == "reduce_half":
        print(f"  Your resilience halves the impact of this shadow.")
        penalty = 2
    elif interaction == "detect_nearby":
        print(f"  You sensed this shadow early and were prepared.")
        penalty = 1
    else:
        print(f"  Face it directly. Reflect before you continue.")
        penalty = 3

    if penalty > 0:
        print(f"  XP penalty: -{penalty}")
    else:
        print(f"  No XP lost.")

    print_divider()
    return penalty


def _show_omega_unlock(animus_name, animus_entry, pillar_names, mentor_name):
    """Display the Omega form unlock sequence."""
    print_header("OMEGA FORM UNLOCKED", width=60)
    print(f"  Your Animus has awakened its first true form.")
    print_blank()

    for pillar in pillar_names:
        form = get_animus_form(pillar, "omega")
        if form:
            print(f"  [ {pillar} ] {form['name']}")
            print(f"    {form['description']}")
            abilities_display = format_list(
                [format_trait_name(a) for a in form.get("abilities", [])]
            )
            print(f"    Abilities: {abilities_display}")
            print_blank()

    # Mentor response to form unlock
    response = get_mentor_form_response(mentor_name, "omega")
    if response:
        print_dialogue(mentor_name, response)
    print_divider()


# -----------------------------
# Main mission function
# -----------------------------

def run_module1():
    """Run the full Module 1: The Threshold mission."""

    # ---- Intro ----
    print_header(f"CASSWORLD -- MODULE 1: {MISSION_NAME}", width=60)
    print("  You stand at the threshold between who you are")
    print("  and who you are becoming.")
    print_blank()
    print("  Collect XP tokens ($) to build your strength.")
    print("  Face shadow encounters (!) to grow through resistance.")
    print("  Unlock your Omega form and complete the mission.")
    print_divider()

    # ---- Animus Selection ----
    catalogue = load_catalogue()
    animus_names = get_all_animus_names(catalogue)

    print_subheader("SELECT YOUR ANIMUS")
    for i, name in enumerate(animus_names, start=1):
        entry = get_animus(name, catalogue)
        print(f"  {i:>2}. {name} [{entry['class']}] -- Mentor: {entry['mentor']}")
        print(f"        {entry['description']}")
    print_blank()

    choice = get_choice("  Enter the number of your Animus: ", 1, len(animus_names))
    animus_name = animus_names[choice - 1]
    animus_entry = get_animus(animus_name, catalogue)

    print_blank()
    print_header(f"ANIMUS SELECTED: {animus_name}", width=60)
    print_stat("Class", animus_entry["class"])
    print_stat("Mentor", animus_entry["mentor"])
    print_stat("Pillar Alignment", format_list(animus_entry.get("pillar_alignment", [])))
    print_stat("Strengths", format_list(animus_entry.get("strengths", [])))
    print_stat("Shadow Risk", format_list(animus_entry.get("shadow_risk", [])))
    print_blank()

    mentor_name = animus_entry["mentor"]
    pillar_names = animus_entry.get("pillar_alignment", [])

    # Opening mentor guidance (core tier)
    opening_guidance = get_mentor_guidance(mentor_name, "core")
    if opening_guidance:
        print_dialogue(mentor_name, random.choice(opening_guidance))
    print_divider()

    input("  Press Enter to begin The Threshold...\n")

    # ---- Grid Setup ----
    player_pos = [0, 0]
    xp_total = 0
    omega_unlocked = False
    shadows_encountered = 0

    def random_pos():
        """Generate a random grid position away from the starting corner."""
        while True:
            pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            if pos != [0, 0]:
                return pos

    xp_tokens = [random_pos() for _ in range(XP_TOKEN_COUNT)]
    shadow_positions = []
    for _ in range(SHADOW_TOKEN_COUNT):
        while True:
            pos = random_pos()
            if pos not in xp_tokens and pos not in shadow_positions:
                shadow_positions.append(pos)
                break

    # ---- Game Loop ----
    while True:
        print_blank()
        print_stat("Position", f"Row {player_pos[0]}, Col {player_pos[1]}")
        print_stat("XP", xp_total)
        print_stat("XP tokens remaining", len(xp_tokens))
        print_stat(
            "Omega",
            "UNLOCKED" if omega_unlocked else f"Locked (need {OMEGA_UNLOCK_THRESHOLD} XP)"
        )
        print_blank()
        render_grid(GRID_SIZE, player_pos, xp_tokens, shadow_positions)

        move = input("  Move (W/A/S/D) or Q to quit: ").strip().upper()

        if move == "Q":
            print_blank()
            print("  You step back from the threshold. The journey pauses.")
            break

        new_pos = player_pos[:]
        if move == "W" and player_pos[0] > 0:
            new_pos[0] -= 1
        elif move == "S" and player_pos[0] < GRID_SIZE - 1:
            new_pos[0] += 1
        elif move == "A" and player_pos[1] > 0:
            new_pos[1] -= 1
        elif move == "D" and player_pos[1] < GRID_SIZE - 1:
            new_pos[1] += 1
        else:
            if move in ("W", "A", "S", "D"):
                print("  The boundary holds. You cannot move further in that direction.")
            else:
                print("  Use W (up), A (left), S (down), D (right).")
            continue

        player_pos = new_pos

        # --- XP Token collected ---
        if player_pos in xp_tokens:
            base_xp = random.randint(8, 15)
            gained = calculate_xp(base_xp, animus_name, catalogue)
            xp_total += gained
            xp_tokens.remove(player_pos[:])

            print_subheader("XP COLLECTED")
            print(f"  +{gained} XP (base {base_xp}, Animus bonus applied).")

            # Reinforce with a light trait from the player's pillar alignment
            _, light_trait = _pick_light_trait(pillar_names)
            if light_trait:
                print(f"  Your strength surfaces: {format_trait_name(light_trait['name'])}")
                print(f"  \"{light_trait['description']}\"")

            # Mentor shifts to developed guidance at the halfway point
            if len(xp_tokens) <= XP_TOKEN_COUNT // 2:
                guidance = get_mentor_guidance(mentor_name, "developed")
                if guidance:
                    print_blank()
                    print_dialogue(mentor_name, random.choice(guidance))

            print_divider()

            # Check Omega unlock threshold
            if not omega_unlocked and xp_total >= OMEGA_UNLOCK_THRESHOLD:
                omega_unlocked = True
                _show_omega_unlock(animus_name, animus_entry, pillar_names, mentor_name)

        # --- Shadow encounter ---
        if player_pos in shadow_positions:
            shadow_positions.remove(player_pos[:])
            shadows_encountered += 1

            # Escalate shadow tier with each encounter
            if shadows_encountered == 1:
                tier = "core"
            elif shadows_encountered == 2:
                tier = "developed"
            else:
                tier = "ascended"

            penalty = _resolve_shadow_encounter(
                animus_entry, pillar_names, mentor_name, xp_total, tier
            )
            xp_total = max(0, xp_total - penalty)

        # --- Win condition: all XP collected ---
        if not xp_tokens:
            print_blank()
            print_header("THE THRESHOLD -- CLEARED", width=60)
            print(f"  All XP tokens collected.")
            print_stat("Final XP", xp_total)
            print_stat("Shadow encounters", shadows_encountered)
            print_stat("Omega form", "UNLOCKED" if omega_unlocked else "Not yet unlocked")
            print_blank()

            # Closing mentor guidance scales to performance
            if omega_unlocked:
                guidance_tier = "ascended"
            elif xp_total >= 15:
                guidance_tier = "developed"
            else:
                guidance_tier = "core"

            final_guidance = get_mentor_guidance(mentor_name, guidance_tier)
            if final_guidance:
                print_dialogue(mentor_name, random.choice(final_guidance))

            print_blank()
            print("  You have crossed the threshold.")
            print("  The next stage awaits.")
            print_divider()
            break

    return xp_total


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run_module1()
