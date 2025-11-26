from generators.hangman_generator import get_random_animal
from renderers.hangman_renderer import render_hangman_markdown

DEFAULT_LIVES = 5


def play_hangman():
    """
    Console based hangman game loop for testing the challenge.
    Uses the random animal generator and updates lives with each guess.
    Reveals a new hint each time the player guesses wrong.
    """
    word, all_hints = get_random_animal()
    lives_left = DEFAULT_LIVES

    guessed_letters = set()
    correct_letters = set(word)

    # Start by showing only the first hint, then reveal more on wrong guesses
    hint_items = list(all_hints.items())
    visible_hint_count = 1

    print("Starting Hangman Game")
    print("The animal word has", len(word), "letters.")

    while lives_left > 0:
        # Build the subset of hints to show this round
        visible_hints = dict(hint_items[:visible_hint_count])

        # Show the game status using the renderer
        current_state = render_hangman_markdown(
            word=word,
            hints=visible_hints,
            lives_left=lives_left
        )
        print(current_state)

        # Build the masked word for display
        masked = " ".join(
            letter if letter in guessed_letters else "_"
            for letter in word
        )
        print("Word:", masked)

        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please guess one letter at a time.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in correct_letters:
            print("Correct guess.")
        else:
            lives_left -= 1
            print("Wrong guess. Lives left:", lives_left)

            # Reveal one more hint on each wrong guess, up to the total number
            if visible_hint_count < len(hint_items):
                visible_hint_count += 1
                print("Revealing an extra hint.")

        # Check win condition
        if all(letter in guessed_letters for letter in word):
            print("\nYou win. The animal was:", word)
            return

    # Lose condition
    print("\nYou lost. The zombies reached the monkey.")
    print("The animal was:", word)


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