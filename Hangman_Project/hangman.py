from hangman_art import HANGMAN_PICS
import random

def load_words(filename="words.txt"):
    """
    Load words from a text file.

    Filters words between 4 and 12 characters long.

    Args:
        filename (str): Path to the file containing word list.

    Returns:
        list: A list of valid lowercase words.
    """
    try:
        with open(filename, 'r') as file:
            words = [line.strip().lower() for line in file if 4 <= len(line.strip()) <= 12]
            if len(words) < 50:
                print("Warning: Word list should have at least 50 valid words.")
            return words
    except FileNotFoundError:
        print("File not found. Make sure words.txt is in the same folder.")
        return []

def choose_random_word(word_list, difficulty="medium"):
    """
    Choose a random word from the list based on difficulty.

    Args:
        word_list (list): List of available words.
        difficulty (str): Difficulty level - 'easy', 'medium', or 'hard'.

    Returns:
        str: A randomly selected word.
    """
    if difficulty == "easy":
        filtered = [w for w in word_list if 4 <= len(w) <= 6]
    elif difficulty == "hard":
        filtered = [w for w in word_list if 10 <= len(w) <= 12]
    else:
        filtered = [w for w in word_list if 7 <= len(w) <= 9]

    if not filtered:
        return random.choice(word_list)
    
    return random.choice(filtered)

def display_hangman(wrong_count):
    """
    Display the current hangman ASCII art.

    Args:
        wrong_count (int): Number of incorrect guesses so far.
    """
    print(HANGMAN_PICS[wrong_count])

def display_game_state(word, guessed_letters, wrong_letters, wrong_count):
    """
    Show the current game state to the player.

    Args:
        word (str): The secret word.
        guessed_letters (list): Correctly guessed letters.
        wrong_letters (list): Incorrectly guessed letters.
        wrong_count (int): Number of wrong guesses made.
    """
    display_hangman(wrong_count)
    display_word = ' '.join([letter.upper() if letter in guessed_letters else '_' for letter in word])
    print(f"\nWord: {display_word}")
    print(f"Wrong letters: {', '.join(wrong_letters).upper() if wrong_letters else 'None'}")
    remaining = len(HANGMAN_PICS) - 1 - wrong_count
    print(f"Attempts remaining: {remaining}\n")

def get_player_guess(guessed_letters):
    """
    Prompt and validate a player's letter guess.

    Args:
        guessed_letters (list): Already guessed letters.

    Returns:
        str: A valid single-letter guess.
    """
    while True:
        guess = input("Enter a letter: ").strip().lower()
        if len(guess) != 1:
            print("Please enter only one letter.")
        elif not guess.isalpha():
            print("Only alphabet letters are allowed.")
        elif guess in guessed_letters:
            print("You already guessed that letter. Try a new one.")
        else:
            return guess

def check_game_over(word, guessed_letters, wrong_count, max_wrong):
    """
    Check if the game has ended (win/loss).

    Args:
        word (str): The word to guess.
        guessed_letters (list): Correct guesses.
        wrong_count (int): Number of wrong guesses.
        max_wrong (int): Maximum allowed wrong guesses.

    Returns:
        str: "win", "loss", or "continue"
    """
    if all(letter in guessed_letters for letter in word):
        print(f"You guessed the word: {word.upper()}")
        return "win"
    if wrong_count >= max_wrong:
        print(f"Game Over. The correct word was: {word.upper()}")
        return "loss"
    return "continue"

def play_hangman(word_list):
    """
    Start and manage one round of the Hangman game.

    Args:
        word_list (list): List of available words.

    Returns:
        str: "win" or "loss" based on the game result.
    """
    print("Choose mode: 1 - Single Player | 2 - Multiplayer")
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == '2':
        word = input("Player 1, enter a word for Player 2 to guess: ").strip().lower()
        print("\n" * 50)
    else:
        print("Select difficulty: E - Easy | M - Medium | H - Hard")
        level = input("Enter difficulty (E/M/H): ").strip().lower()
        if level == 'e':
            difficulty = "easy"
        elif level == 'h':
            difficulty = "hard"
        else:
            difficulty = "medium"
        word = choose_random_word(word_list, difficulty)

    guessed_letters = []
    wrong_letters = []
    wrong_count = 0
    max_wrong = len(HANGMAN_PICS) - 1

    hint_letter = random.choice(word)
    guessed_letters.append(hint_letter)
    print(f"Hint: The word contains the letter '{hint_letter.upper()}'")

    while True:
        display_game_state(word, guessed_letters, wrong_letters, wrong_count)
        guess = get_player_guess(guessed_letters + wrong_letters)

        if guess in word:
            guessed_letters.append(guess)
            print("Correct guess.\n")
        else:
            wrong_letters.append(guess)
            wrong_count += 1
            print("Incorrect guess.\n")

        result = check_game_over(word, guessed_letters, wrong_count, max_wrong)
        if result in ["win", "loss"]:
            display_game_state(word, guessed_letters, wrong_letters, wrong_count)
            return result

def main():
    """
    Main entry point of the program.

    Loads words, manages custom words, tracks game score, and allows replay.
    """
    words = load_words()
    if not words:
        return

    use_custom = input("Do you want to add your own words? (y/n): ").strip().lower()
    if use_custom == 'y':
        custom_input = input("Enter custom words separated by commas: ")
        custom_words = [w.strip().lower() for w in custom_input.split(",") if 4 <= len(w.strip()) <= 12]
        words.extend(custom_words)

    wins = 0
    losses = 0

    while True:
        result = play_hangman(words)
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1

        print(f"Score: Wins = {wins}, Losses = {losses}")
        choice = input("Do you want to play again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Thanks for playing. Goodbye!")
            break

if __name__ == "__main__":
    main()
