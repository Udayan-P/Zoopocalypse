def render_zombie_stack(lives_left, max_lives=5):
    """
    Creates a simple visual of zombies stacking when lives go down.
    Each life lost adds one zombie to the stack.
    """
    zombies = max_lives - lives_left
    art = []

    for _ in range(zombies):
        art.append("  (Z)")        # zombie head
        art.append("  /|\\")       # body with arms
        art.append("  / \\")       # legs

    if zombies == 0:
        art.append("No zombies yet. You are safe.")

    return "\n".join(art)


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
    # BUG HERE: lives_remaining does not exist
    md += render_zombie_stack(lives_remaining)
    md += "\n```\n"

    return md


if __name__ == "__main__":
    # Example preview for testing the renderer
    sample_word = "lion"
    sample_hints = {"Classification": "Mammal", "Diet": "Carnivore"}
    markdown_output = render_hangman_markdown(sample_word, sample_hints, lives_left=3)
    print(markdown_output)