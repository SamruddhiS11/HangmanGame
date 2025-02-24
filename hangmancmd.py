import random
import time
import requests  # Import requests for API calls

# Hangman images/text representations
hangman_images = [
    """
       ------
       |    |
            |
            |
            |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
     =========
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
     =========
    """
]

# Function to fetch a random word and ensure it has a valid hint
def fetch_valid_word():
    for _ in range(5):  # Try 5 times to get a valid word with a definition
        word = fetch_random_word()
        hint = fetch_hint(word)
        if hint != "No hint available":
            return word, hint  # Return only if a valid hint is found
    return "python", "A popular programming language"  # Fallback word and hint

# Function to fetch a random word from API
def fetch_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        if response.status_code == 200:
            word = response.json()[0].lower()
            return word
    except Exception as e:
        print(f"Error fetching word: {e}")
    return "python"  # Default word if API fails

# Function to fetch a hint using Dictionary API
def fetch_hint(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "meanings" in data[0]:  # Ensure correct response format
                definition = data[0]["meanings"][0]["definitions"][0]["definition"]
                return definition
    except Exception as e:
        print(f"Error fetching hint: {e}")
    return "No hint available"

# Function to display a sad face
def display_sad_face():
    sad_face = """
          _______
        .'       '.
       /           \\
      |  (o)   (o)  |
      |   ! .-. !   |
       \\    ___    /
        '.       .'
          '-...-'
    """
    print(sad_face)

# Function to display celebration animation
def display_celebration():
    celebration_frames = [
        """
         \o/
          |
         / \\
        """,
        """
          o/
         /|
         / \\
        """,
        """
         \o
          |\\         
         / \\
        """
    ]
    for _ in range(5):  # Repeat animation 5 times
        for frame in celebration_frames:
            print(frame)
            time.sleep(0.3)
            print("\033c", end="")  # Clear terminal

# Function to play Hangman game
def hangman_game():
    while True:
        word, hint = fetch_valid_word()  # Ensure valid word and hint
        word_display = ['_'] * len(word)
        wrong_guesses = []
        attempts = 6

        print("\nWelcome to Hangman!")
        print(f"Hint: {hint}")
        print("Let's start guessing the word...")

        while attempts > 0 and "_" in word_display:
            print(f"\nWord: {' '.join(word_display)}")
            print(f"Attempts left: {attempts}")
            print(f"Wrong guesses: {', '.join(wrong_guesses) if wrong_guesses else 'None'}")
            print(hangman_images[6 - attempts])  # Display Hangman state

            guess = input("Enter a letter: ").lower()

            if guess in wrong_guesses or guess in word_display:
                print("You've already guessed that letter. Try again.")
                continue

            if guess in word:
                for idx, letter in enumerate(word):
                    if letter == guess:
                        word_display[idx] = guess
                print(f"Good guess! {guess} is in the word.")
            else:
                attempts -= 1
                wrong_guesses.append(guess)
                print(f"Oops! {guess} is not in the word.")

            if "_" not in word_display:
                print(f"\nCongratulations! You've guessed the word: {word}")
                display_celebration()  # Show celebration animation
                break

        if attempts == 0:
            print(f"\nSorry, you've lost. The word was: {word}")
            display_sad_face()  # Show sad face if the player loses

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye!")
            break  # Exit the game loop

# Start the game
hangman_game()