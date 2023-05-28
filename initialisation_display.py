# Module handles initialisation of pygame window, pygame-related variables 
# and displaying of game.

import json
import time
import random
import pygame


def setup_pygame():
    """
    Sets up pygame and initialised pygame-related variables used in game.
    """
    global window_x, window_y, GAME_WINDOW
    global COLOURS, fruit, fps

    # window dimensions.
    window_x, window_y = 936, 624    

    # Defining & Storing pygame colours (RGB).
    COLOURS = {
        "BLACK": pygame.Color(0, 0, 0), "WHITE": pygame.Color(255, 255, 255), 
        "GREEN": pygame.Color(0, 255, 0), "BLUE": pygame.Color(0, 0, 255)
        }
    
    # pygame and game window initialisation.
    pygame.init()
    pygame.display.set_caption("Snake Game")
    GAME_WINDOW = pygame.display.set_mode((window_x, window_y))

    # Loading and scaling fruit image.
    fruit = pygame.image.load("pictures/fruit.png").convert_alpha()
    fruit = pygame.transform.scale(fruit, (13,13))

    # Setting up game music.
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/Angry Birds Theme Song.wav")
    
    # Music played indefinitely, paused initially.
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()

    # Frames-Per-Second (FPS) controller.
    fps = pygame.time.Clock()


def initialise_game_values():
    """
    Sets up and initialises values to be used in game - 
    (snake_body, fruit_pos, direction values, draw fruit flag),
    stores them in a dictionary and returns the dictionary. 
    """
    game_values = {}

    game_values["snake"] = {"snake_speed": 15}

    # Snake default position (head, body).
    snake_head = [104, 65]  

    snake_body = [
        snake_head, [snake_head[0] - (1 * 13), snake_head[1]], 
        [snake_head[0] - (2 * 13), snake_head[1]], 
        [snake_head[0] - (3 * 13), snake_head[1]]
        ]
    
    game_values["snake"]["snake_body"] = snake_body
    
    # Fruit position.
    fruit_pos = fruit_positioning(game_values)
    
    game_values["fruit_pos"] = fruit_pos

    # Setting default direction and opening score.
    game_values["direction"] = "RIGHT"
    game_values["score"] = 0

    return game_values


def fruit_positioning(game_values):
    """
    Sets new position for fruit and ensures that
    fruit isn't randomly paced in same position as snake_body.
    """
    while True:
        fruit_pos = [
            random.randrange(1, (window_x // 13) - 1) * 13,
                    random.randrange(1, (window_y // 13) -1) * 13
                    ]
        
        if fruit_pos not in game_values["snake"]["snake_body"][1:]:
            return fruit_pos


def display_score(choice, colour, font, size, score):
    """Displays users score on pygame window."""
    # Creating font object.
    score_font = pygame.font.SysFont(font, size)
    high_score_font = pygame.font.SysFont(font, size)
    
    # Creating surface to display score.
    score_surface = score_font.render("Score: " + str(score), True, colour)

    username, high_score = get_high_score()
    display_txt = f"High Score: {username} ({high_score})"

    high_score_surface = score_font.render(display_txt, True, colour)
    
    # Rect objects for scores surface objects.
    score_rect = score_surface.get_rect()
    high_score_rect = high_score_surface.get_rect(topright=(window_x, 0))

    # Displaying score.
    GAME_WINDOW.blit(score_surface, score_rect)  
    GAME_WINDOW.blit(high_score_surface, high_score_rect)


def get_high_score():
    """Returns game high score."""
    with open("high_score.json", 'r') as file_obj:
        hscore_data = json.load(file_obj)

    hscore_info = [
        hscore_data.setdefault("username", "Nobody"), 
        hscore_data.setdefault("high_score", 0)
    ]
    
    return hscore_info


def game_over(game_values):
    """
    Displays game over text and exits game when game over conditions are met.
    """
    score = game_values["score"]    
    
    # Creating font object.
    over_font = pygame.font.SysFont("times new roman", 50)

    # Creating surface to display game over text.
    game_over_surface = over_font.render("Round Score: " + str(score), 
        True, COLOURS.get("WHITE"))

    # Rect object for game over text surface object.
    game_over_rect = game_over_surface.get_rect()

    # Setting position of game over text.
    game_over_rect.midtop = (window_x / 2, window_y / 4)  

    # Displaying game over text.
    GAME_WINDOW.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Program paused to see text displayed.
    time.sleep(3)  

    # pygame library deactivated.
    pygame.quit()


def display_game(game_values):
    """Displays the snake and fruit in pygame window."""
    GAME_WINDOW.fill(COLOURS["BLACK"])

    snake_body = game_values["snake"]["snake_body"]
    
    # Drawing the snake (head and body).
    for pos in snake_body:
        if pos == snake_body[0]:  
            pygame.draw.rect(GAME_WINDOW, COLOURS["BLUE"], 
                pygame.Rect(pos[0], pos[1], 13, 13))
        else:
            pygame.draw.rect(GAME_WINDOW, COLOURS["GREEN"], 
                pygame.Rect(pos[0], pos[1], 13, 13))

    # Drawing fruit.
    GAME_WINDOW.blit(fruit, game_values["fruit_pos"])


def play_music():
    """Determines whether game music should be played initially.
    Dependent on recent game play music control (paused/unpaused)."""
    music_playing = False
    with open("sounds/sound_tracker.json", 'r') as file_obj:
        music_data = json.load(file_obj)

    # Played in recent round, thus continue playing.
    if music_data["play_sound"]:
        music_playing = True
        pygame.mixer.music.unpause()

    return music_playing
