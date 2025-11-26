from generators.hangman_generator import get_random_animal
from renderers.hangman_renderer import render_hangman_markdown

DEFAULT_LIVES = 5

def build_hangman_challenge():
    """
    Uses the generator and renderer to assemble the full hangman challenge.
    Returns the markdown text that can be embedded into the final escape room.
    """
    word, hints = get_random_animal()
    lives_left = DEFAULT_LIVES

    markdown_output = render_hangman_markdown(
        word=word,
        hints=hints,
        lives_left=lives_left
    )

    return markdown_output


if __name__ == "__main__":
    # Generate a complete preview of the hangman challenge
    output = build_hangman_challenge()
    print(output)