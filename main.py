import random
from animus import load_catalogue, get_animus, get_all_animus_names, calculate_xp, display_catalogue

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
            print(f"\nYou selected {animus_name}! Ability: {animus_entry['description']}\n")
            break
        else:
            print("Invalid choice. Try again.")
    except ValueError:
        print("Enter a number corresponding to your Animus.")

# -----------------------------
# Game Setup
# -----------------------------
grid_size = 5
player_pos = [0, 0]
xp_total = 0

xp_tokens = [[random.randint(0, grid_size-1), random.randint(0, grid_size-1)] for _ in range(3)]
shadow_traits = [[random.randint(0, grid_size-1), random.randint(0, grid_size-1)] for _ in range(2)]

# -----------------------------
# Game Loop
# -----------------------------
while True:
    print(f"\nPlayer position: {player_pos}, XP: {xp_total}")
    move = input("Move (W/A/S/D): ").upper()

    # Movement logic
    if move == "W" and player_pos[0] > 0:
        player_pos[0] -= 1
    elif move == "S" and player_pos[0] < grid_size-1:
        player_pos[0] += 1
    elif move == "A" and player_pos[1] > 0:
        player_pos[1] -= 1
    elif move == "D" and player_pos[1] < grid_size-1:
        player_pos[1] += 1
    else:
        print("Invalid move!")

    # Check XP collection
    if player_pos in xp_tokens:
        gained_xp = calculate_xp(10, animus_name, catalogue)
        print(f"Collected XP! +{gained_xp} life-value points")
        xp_total += gained_xp
        xp_tokens.remove(player_pos.copy())
        print(f"Mentor AI says: '{animus_entry['mentor_note']}'")

    # Check Shadow Traits
    if player_pos in shadow_traits:
        shadow_interaction = animus_entry["shadow_trait_interaction"]
        print("Encountered Shadow Trait! Reflect and choose wisely...")
        if shadow_interaction == "reduce_half":
            print(f"Your {animus_name} resilience reduces the challenge!")
        elif shadow_interaction == "bypass_once":
            print(f"You bypass this shadow trait thanks to {animus_name} ingenuity!")
        elif shadow_interaction == "detect_nearby":
            print(f"{animus_name} detected this shadow trait early — you were prepared!")
        else:
            print(f"Mentor AI says: '{animus_entry['mentor_note']}'")
        shadow_traits.remove(player_pos.copy())

    # Win condition
    if not xp_tokens:
        print(f"\nAll XP collected! Total life-value XP: {xp_total}")
        print("Congratulations! Your CassWorld journey begins...")
        break