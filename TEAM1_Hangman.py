import pygame
import random
import time
import requests

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

words_list = ["java", "elephant", "computer", "piano", "algorithm", "python", "monster", "dragon", "ocean", "hangman", "castle", "sky", "building", "engineering", "vehicle", "flag"]

def fetch_hint(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "meanings" in data[0]:
                return data[0]["meanings"][0]["definitions"][0]["definition"]
        else:
            print(f"Error: Unable to fetch hint. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching hint: {e}")
    return "No hint available"

def wrap_text(text, max_width, font_size=24):
    font = pygame.font.Font(None, font_size)
    words = text.split()
    lines = []
    current_line = ""

    [
        lines.append(current_line) or (current_line := word + " ")
        if font.size(current_line + word)[0] > max_width
        else (current_line := current_line + word + " ")
        for word in words
    ]

    if current_line.strip():
        lines.append(current_line.strip())

    return lines

def draw_game(word_display, attempts, wrong_guesses, hint):
    screen.fill(WHITE)
    draw_hangman(attempts)
    draw_text("Hint:", 50, 30, BLACK, 28)
    wrapped_hint = wrap_text(hint, max_width=750, font_size=24)
    y_pos = 60
    for line in wrapped_hint:
        draw_text(f"{line}", 50, y_pos, RED, 24)
        y_pos += 30

    draw_text("Word: " + " ".join(word_display), 400, 150, BLACK)
    draw_text(f"Attempts left: {attempts}", 400, 200, BLACK)
    draw_text("Wrong guesses: " + ", ".join(wrong_guesses), 400, 250, RED)
    pygame.display.update()

def draw_hangman(attempts):
    pygame.draw.line(screen, BLACK, (100, 550), (200, 550), 5)
    pygame.draw.line(screen, BLACK, (150, 550), (150, 150), 5)
    pygame.draw.line(screen, BLACK, (150, 150), (300, 150), 5)
    pygame.draw.line(screen, BLACK, (300, 150), (300, 200), 5)

    if attempts <= 5:
        pygame.draw.circle(screen, BLACK, (300, 230), 30, 5)
    if attempts <= 4:
        pygame.draw.line(screen, BLACK, (300, 260), (300, 370), 5)
    if attempts <= 3:
        pygame.draw.line(screen, BLACK, (300, 280), (250, 330), 5)
    if attempts <= 2:
        pygame.draw.line(screen, BLACK, (300, 280), (350, 330), 5)
    if attempts <= 1:
        pygame.draw.line(screen, BLACK, (300, 370), (250, 450), 5)
    if attempts == 0:
        pygame.draw.line(screen, BLACK, (300, 370), (350, 450), 5)

def draw_dancing_man(arm_position):
    head_pos = (400, 200)
    body_start, body_end = (400, 230), (400, 330)
    left_leg, right_leg = (370, 370), (430, 370)
    arm_start = (400, 250)

    pygame.draw.circle(screen, BLACK, head_pos, 30, 5)
    pygame.draw.line(screen, BLACK, body_start, body_end, 5)
    pygame.draw.line(screen, BLACK, body_end, left_leg, 5)
    pygame.draw.line(screen, BLACK, body_end, right_leg, 5)

    if arm_position == 0:
        left_arm, right_arm = (360, 210), (440, 210)
    elif arm_position == 1:
        left_arm, right_arm = (360, 250), (440, 250)
    else:
        left_arm, right_arm = (360, 290), (440, 290)

    pygame.draw.line(screen, BLACK, arm_start, left_arm, 5)
    pygame.draw.line(screen, BLACK, arm_start, right_arm, 5)

def display_celebration():
    for i in range(10):
        screen.fill(WHITE)
        draw_dancing_man(arm_position=i % 3)
        draw_text("You Win! :)", WIDTH // 2 - 80, 100, GREEN, 50)
        pygame.display.update()
        time.sleep(0.3)

def draw_text(text, x, y, color=BLACK, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def hangman_game():
    word = random.choice(words_list)
    hint = fetch_hint(word)
    word_display = ['_'] * len(word)
    wrong_guesses = []
    attempts = 6
    running = True

    while running:
        draw_game(word_display, attempts, wrong_guesses, hint)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key)
                if guess in wrong_guesses or guess in word_display:
                    continue
                if guess in word:
                    word_display = [guess if letter == guess else word_display[idx] for idx, letter in enumerate(word)]
                else:
                    attempts -= 1
                    wrong_guesses.append(guess)

                if "_" not in word_display:
                    display_celebration()
                    return

                if attempts == 0:
                    draw_game(word_display, attempts, wrong_guesses, hint)
                    pygame.display.update()
                    time.sleep(1)
                    screen.fill(WHITE)
                    draw_text(f"Sorry, you've lost. Better luck next time! The word was: {word}", 100, 150, RED, 28)
                    pygame.display.update()
                    time.sleep(2)
                    return

game_running = True
while game_running:
    hangman_game()

    screen.fill(WHITE)
    draw_text("Play Again? (Y/N)", 300, 250, BLACK, 50)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                elif event.key == pygame.K_n:
                    game_running = False
                    waiting = False

pygame.quit()