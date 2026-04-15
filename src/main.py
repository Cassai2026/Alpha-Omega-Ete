import random
from animus import load_catalogue, get_animus, get_all_animus_names, calculate_xp, display_catalogue
from shadow_traits import get_traits_by_tier, PILLAR_TRAITS
from mentor import get_mentor_guidance, get_shadow_encounter_response

# -----------------------------
# Animus Setup (from catalogue)
# -----------------------------
catalogue = load_catalogue()
animus_names = get_all_animus_names(catalogue)

print("Welcome to CassWorld 2D!\nChoose your Animus:\n")
display_catalogue(catalogue)

while True:
    try:
        choice = int(input("Enter the number of your Animus: "))
        if 1 <= choice <= len(animus_names):
            animus_name = animus_names[choice - 1]
            animus_entry = get_animus(animus_name, catalogue)
            print(f"\nYou selected {animus_name}! {animus_entry['description']}\n")
            break
        else:
            print("Invalid choice. Try again.")
    except ValueError:
        print("Enter a number corresponding to your Animus.")

mentor_name = animus_entry["mentor"]
pillar_names = animus_entry.get("pillar_alignment", [])

# Opening mentor guidance
opening = get_mentor_guidance(mentor_name, "core")
if opening:
    print(f"[{mentor_name}]: \"{random.choice(opening)}\"\n")

# -----------------------------
# Game Setup
# -----------------------------
grid_size = 5
player_pos = [0, 0]
xp_total = 0

xp_tokens = [[random.randint(0, grid_size-1), random.randint(0, grid_size-1)] for _ in range(3)]
shadow_positions = [[random.randint(0, grid_size-1), random.randint(0, grid_size-1)] for _ in range(2)]


def _get_shadow_trait(pillar_names):
    """Return a random shadow trait (name, description) from the player's pillar alignment."""
    candidates = []
    for pillar in pillar_names:
        traits = get_traits_by_tier(pillar, "shadow", "core")
        if traits:
            for t in traits:
                candidates.append((pillar, t))
    if candidates:
        pillar, trait = random.choice(candidates)
        pillar_entry = PILLAR_TRAITS.get(pillar, {})
        return (
            pillar,
            pillar_entry.get("sin", "Unknown"),
            trait["name"].replace("_", " ").title(),
            trait["description"],
        )
    return None, None, None, None


# -----------------------------
# Game Loop
# -----------------------------
while True:
    print(f"\nPosition: {player_pos}  |  XP: {xp_total}")
    move = input("Move (W/A/S/D): ").upper()

    # Movement logic
    if move == "W" and player_pos[0] > 0:
        player_pos[0] -= 1
    elif move == "S" and player_pos[0] < grid_size - 1:
        player_pos[0] += 1
    elif move == "A" and player_pos[1] > 0:
        player_pos[1] -= 1
    elif move == "D" and player_pos[1] < grid_size - 1:
        player_pos[1] += 1
    else:
        print("Invalid move or boundary reached.")

    # Check XP collection
    if player_pos in xp_tokens:
        gained_xp = calculate_xp(10, animus_name, catalogue)
        print(f"Collected XP! +{gained_xp}")
        xp_total += gained_xp
        xp_tokens.remove(player_pos.copy())
        # Mid-game mentor guidance
        guidance = get_mentor_guidance(mentor_name, "developed")
        if guidance:
            print(f"[{mentor_name}]: \"{random.choice(guidance)}\"")

    # Check Shadow Trait encounter
    if player_pos in shadow_positions:
        shadow_interaction = animus_entry["shadow_trait_interaction"]
        pillar, sin, trait_name, trait_desc = _get_shadow_trait(pillar_names)

        print("\nShadow Trait Encountered! Reflect and choose wisely...")
        if pillar:
            print(f"  Pillar: {pillar} | Sin: {sin}")
            print(f"  Trait:  {trait_name}")
            print(f"  \"{trait_desc}\"")

        # Dynamic mentor response
        encounter_prompts = get_shadow_encounter_response(mentor_name)
        if encounter_prompts:
            print(f"[{mentor_name}]: \"{random.choice(encounter_prompts)}\"")

        if shadow_interaction == "reduce_half":
            print(f"Your resilience reduces the shadow's impact.")
        elif shadow_interaction == "bypass_once":
            print(f"You bypass this shadow thanks to your ingenuity.")
        elif shadow_interaction == "detect_nearby":
            print(f"You detected this shadow early and were prepared.")
        else:
            print(f"Face it directly. Growth lives on the other side.")

        shadow_positions.remove(player_pos.copy())

    # Win condition
    if not xp_tokens:
        print(f"\nAll XP collected! Total: {xp_total}")
        # Closing ascended mentor guidance
        closing = get_mentor_guidance(mentor_name, "ascended")
        if closing:
            print(f"[{mentor_name}]: \"{random.choice(closing)}\"")
        print("Congratulations! Your CassWorld journey begins...")
        break
