# HangmanGame
This repository contains two implementations of the classic Hangman game:

hangmancmd.py: A command-line version that fetches random words from an API and provides hints.
TEAM1_Hangman.py: A graphical version built with Pygame, displaying a visual hangman and hint system.

Features
Command-Line Version (hangmancmd.py)
1. Fetches random words using an API
2. Provides hints from a dictionary API
3. ASCII-based Hangman graphics
4. Celebration animation on winning

GUI Version (TEAM1_Hangman.py)
✅ Pygame-based graphical interface
✅ Displays the Hangman drawing as the game progresses
✅ Uses a predefined word list with hint fetching
✅ Animated winning celebration

## How to Run
### Running the Command-Line Version
Install dependencies:
pip install requests
Run the script:
python hangmancmd.py

### Running the Pygame GUI Version
Install dependencies:
pip install pygame requests
Run the script:
python TEAM1_Hangman.py

## Requirements
Python 3.x
requests module for API calls
pygame module for GUI version

## Future Improvements
Adding a difficulty level option
Enhancing the word selection process
Improving UI elements in the Pygame version
