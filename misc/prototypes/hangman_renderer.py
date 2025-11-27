def render_zombie_stack(lives_left, max_lives=5):
    """
    Shows the monkey at the top, a fixed vertical space, zombies stacking
    upward from the ground, and ground at the bottom.
    Zombies fill the gap as lives go down.
    When zombies fill the gap completely, they reach the monkey.
    """
    zombies = max_lives - lives_left

    art_lines = []

    # Monkey at the top
    art_lines.append("     (M)")
    art_lines.append("     /|\\")
    art_lines.append("     / \\")

    # Fixed vertical gap
    GAP_HEIGHT = 5
    gap_lines = ["     |"] * GAP_HEIGHT

    # Zombie block
    zombie_block = ["  (Z)", "  /|\\", "  / \\"]

    # Build a list of zombie blocks
    zombie_lines = []
    for _ in range(zombies):
        zombie_lines.extend(zombie_block)

    # Total zombie height in lines
    zombie_height = len(zombie_lines)

    # Space that remains above zombies
    remaining_gap = GAP_HEIGHT * 1 - (zombies if zombies <= GAP_HEIGHT else GAP_HEIGHT)

    # Add remaining gap lines
    for _ in range(remaining_gap):
        art_lines.append("     |")

    # Add zombies (bottom up)
    art_lines.extend(zombie_lines)

    # Ground
    art_lines.append("==== ground ====")

    # If zombies reached the monkey
    if zombies >= GAP_HEIGHT:
        art_lines.append("The zombies reached the monkey.")

    return "\n".join(art_lines)


def render_hangman_markdown(word, hints, lives_left):
    """
    Creates a markdown formatted output that describes the hangman challenge.
    Includes the masked word, hint list, and zombie stack.
    """
    masked = " ".join("_" for _ in word)

    md = f"# Challenge 1: Hangman\n\n"

    md += "Guess the animal before the zombies reach the monkey.\n\n"

    md += f"**Word:** `{masked}`\n"
    md += f"**Lives left:** {lives_left}\n\n"

    md += "## Hints\n"
    for key, value in hints.items():
        md += f"- **{key}:** {value}\n"

    md += "\n## Zombie Stack\n"
    md += "If you lose all five lives, the zombies stack tall enough to reach the monkey.\n\n"
    md += "```\n"
    # Fixed lives_left instead of undefined lives_remaining
    md += render_zombie_stack(lives_left)
    md += "\n```\n"

    return md


if __name__ == "__main__":
    # Example preview for testing the renderer
    sample_word = "lion"
    sample_hints = {"Classification": "Mammal", "Diet": "Carnivore"}
    markdown_output = render_hangman_markdown(sample_word, sample_hints, lives_left=3)
    print(markdown_output)