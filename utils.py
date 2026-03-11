# -----------------------------
# Eternius Animus — Shared Utilities
#
# Common helpers used across modules:
#   - Display formatting
#   - Input validation
#   - Grid rendering
#   - Text formatting
# -----------------------------


# -----------------------------
# Display Helpers
# -----------------------------

def print_header(title, width=60):
    """Print a formatted section header."""
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")


def print_subheader(title):
    """Print a formatted sub-section header."""
    print(f"\n  --- {title} ---")


def print_dialogue(speaker, text):
    """Print a formatted dialogue line."""
    print(f"  [{speaker}]: \"{text}\"")


def print_blank():
    """Print a blank line with consistent spacing."""
    print()


def print_stat(label, value, indent=2):
    """Print a label: value pair with consistent formatting."""
    padding = " " * indent
    print(f"{padding}{label}:  {value}")


def print_divider(char="-", width=60):
    """Print a horizontal divider."""
    print(f"  {char * (width - 4)}")


# -----------------------------
# Input Helpers
# -----------------------------

def get_choice(prompt, min_val, max_val):
    """
    Get a validated integer choice from the player.

    Parameters:
        prompt:  Text to display before input.
        min_val: Minimum valid choice (inclusive).
        max_val: Maximum valid choice (inclusive).

    Returns:
        int — the validated choice.
    """
    while True:
        try:
            raw = input(prompt).strip()
            choice = int(raw)
            if min_val <= choice <= max_val:
                return choice
            print(f"  Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print(f"  Enter a number between {min_val} and {max_val}.")


def get_yes_no(prompt):
    """
    Get a yes/no response from the player.

    Returns:
        True for yes, False for no.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Enter Y or N.")


def get_text_input(prompt, allow_empty=False):
    """
    Get a non-empty text input from the player.

    Parameters:
        prompt:      Text to display before input.
        allow_empty: If True, accepts empty string.

    Returns:
        str — the player's input.
    """
    while True:
        raw = input(prompt).strip()
        if raw or allow_empty:
            return raw
        print("  Input cannot be empty.")


# -----------------------------
# Grid Helpers
# -----------------------------

def render_grid(grid_size, player_pos, xp_positions=None, shadow_positions=None):
    """
    Render a 2D grid to the console.

    Symbols:
        @  = player
        $  = XP token
        !  = shadow trait
        .  = empty cell

    Parameters:
        grid_size:        int — width and height of the grid.
        player_pos:       [row, col] — current player position.
        xp_positions:     list of [row, col] — XP token locations.
        shadow_positions: list of [row, col] — shadow trait locations.
    """
    if xp_positions is None:
        xp_positions = []
    if shadow_positions is None:
        shadow_positions = []

    print()
    for row in range(grid_size):
        cells = []
        for col in range(grid_size):
            pos = [row, col]
            if pos == player_pos:
                cells.append(" @ ")
            elif pos in xp_positions:
                cells.append(" $ ")
            elif pos in shadow_positions:
                cells.append(" ! ")
            else:
                cells.append(" . ")
        print(f"  {''.join(cells)}")
    print()


# -----------------------------
# Text Formatting
# -----------------------------

def format_trait_name(trait_name):
    """Convert a snake_case trait name to Title Case display."""
    return trait_name.replace("_", " ").title()


def format_list(items, separator=", "):
    """Join a list of strings with a separator."""
    if not items:
        return "None"
    return separator.join(str(item) for item in items)


def truncate(text, max_length=80, suffix="..."):
    """Truncate text to a maximum length with a suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix