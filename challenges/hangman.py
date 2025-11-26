from generators.hangman_generator import get_random_animal
from renderers.hangman_renderer import render_hangman_markdown, render_zombie_stack

DEFAULT_LIVES = 5


def play_hangman():
    """
    Interactive markdown based hangman loop.
    Zombies stack upward, hints revealed on wrong guesses.
    Shows wrong letters under Lives Left for clarity.
    """
    word, all_hints = get_random_animal()
    lives_left = DEFAULT_LIVES

    guessed_letters = set()
    correct_letters = set(word)
    wrong_letters = set()

    hint_items = list(all_hints.items())
    visible_hint_count = 1

    print("# Hangman Challenge\n")
    print("Start guessing the animal.\n")

    while lives_left > 0:
        # Build masked word
        masked = " ".join(
            letter if letter in guessed_letters else "_"
            for letter in word
        )

        # Select visible hints
        visible_hints = dict(hint_items[:visible_hint_count])

        print("\n---\n")

        # ZOMBIE STACK
        print("## Zombie Stack\n")
        print("If you lose all lives, zombies will reach the monkey.\n")

        print("```")
        print(render_zombie_stack(lives_left))
        print("```")

        # Word and lives
        print(f"\n**Word:** `{masked}`")
        print(f"**Lives left:** {lives_left}")

        # Wrong letters section
        if wrong_letters:
            wrong_string = ", ".join(sorted(wrong_letters))
            print(f"**Wrong letters:** {wrong_string}\n")
        else:
            print("**Wrong letters:** None\n")

        # Hints in markdown
        print("### Hints")
        for label, value in visible_hints.items():
            print(f"- **{label}:** {value}")
        print()

        # Player input
        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("\nPlease enter one valid letter.\n")
            continue

        if guess in guessed_letters:
            print("\nYou already guessed that letter.\n")
            continue

        guessed_letters.add(guess)

        if guess in correct_letters:
            print("\nCorrect.\n")
        else:
            lives_left -= 1
            wrong_letters.add(guess)
            print("\nWrong guess.\n")

            # Reveal new hint if available
            if visible_hint_count < len(hint_items):
                visible_hint_count += 1
                print("A new hint has been revealed.\n")

        # Win condition
        if all(letter in guessed_letters for letter in word):
            print("\n## You win")
            print(f"The animal was **{word}**")
            return

    # Lose condition
    print("\n## Game Over")
    print("The zombies reached the monkey.")
    print(f"The animal was **{word}**")

def build_hangman_challenge():
    """
    Creates a non interactive markdown version of the challenge.
    Useful for exporting into the group project.
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
    # Uncomment the one that needs testing 

    # Full game loop
    play_hangman()

    # Markdown only version
    # output = build_hangman_challenge()
    # print(output)