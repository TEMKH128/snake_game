# Module looks for and handles keypress events and increasing of game speed.

import json
import pygame


def event_recognition(pot_direction, music_playing, help_display, sound_file):
    """
    Identifies valid keypresses and returns pot_direction 
    dependent on pygame event recognition.
    """
    # Key events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()

        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_UP: pot_direction = "UP"
            elif event.key == pygame.K_DOWN: pot_direction = "DOWN"
            elif event.key == pygame.K_LEFT: pot_direction = "LEFT"
            elif event.key == pygame.K_RIGHT: pot_direction = "RIGHT"

            elif event.key == pygame.K_m:
                if music_playing:  
                    music_playing = pause_music(music_playing, sound_file)
                elif not music_playing:
                    music_playing = unpause_music(music_playing, sound_file)
                
            elif event.key == pygame.K_SPACE:  
                pause_game(music_playing, help_display)

    return pot_direction, music_playing
                

def pause_game(music_playing, help_display):
    """Pauses and unpauses game when spacebar pressed."""
    paused = True

    # Temporarily pause music if playing.
    if music_playing: pygame.mixer.music.pause()

    while paused:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: 
                    paused = False

                    # Unpause music if it was temporarily paused.
                    if music_playing: pygame.mixer.music.unpause()
                
                elif event.key == pygame.K_h: print(help_display)


def update_direction(pot_direction, game_values):
    """
    Compares pot_direction (where snake want to go) to direction.
    Updates direction if valid and returns game_values dictionary 
    reflecting updates.
    """
    if pot_direction == "UP" and game_values["direction"] != "DOWN":
        game_values["direction"] = "UP"  

    elif pot_direction == "DOWN" and game_values["direction"] != "UP":
        game_values["direction"] = "DOWN"

    elif pot_direction == "LEFT" and game_values["direction"] != "RIGHT":
        game_values["direction"] = "LEFT"
    
    elif pot_direction == "RIGHT" and game_values["direction"] != "LEFT":
        game_values["direction"] = "RIGHT"

    return game_values


def continuous_movement(game_values):
    """
    Updates snakes' body coords to reflect movement.
    Adds to body, seperate function removes from body."""
    head_pos = game_values["snake"]["snake_body"][0].copy()

    if game_values["direction"] == "UP":
        head_pos[1] -= 13 
    elif game_values["direction"] == "DOWN":
        head_pos[1] += 13
    elif game_values["direction"] == "LEFT":
        head_pos[0] -= 13
    elif game_values["direction"] == "RIGHT":
        head_pos[0] += 13

    # Lengthening snake (new head pos appended to snake body).
    game_values["snake"]["snake_body"].insert(0, head_pos) 
    
    return game_values


def detect_consumption(game_values):
    """
    Determines whether snake has consumed fruit and 
    updates fruit_pos if consumed.
    """
    fruit_consumed = False
    head_pos = game_values["snake"]["snake_body"][0]
    fruit_pos = game_values["fruit_pos"]

    # fruit consumed (head_pos meets fruit_pos)
    if head_pos == fruit_pos: 
            fruit_consumed = True
            game_values["score"] += 10
            
    return game_values, fruit_consumed


def pause_music(music_playing, file_path):
    """Pauses music and updates sound tracker."""
    with open(file_path, 'r') as file_obj:
        music_data = json.load(file_obj)        

    if music_data["play_sound"]:
        music_playing = False
        pygame.mixer.music.pause()
        with open(file_path, 'w') as file_obj:
            json.dump({"play_sound": False}, file_obj) 

    return music_playing


def unpause_music(music_playing, file_path):
    """Unpauses music and updates sound tracker."""
    with open(file_path, 'r') as file_obj:
        music_data = json.load(file_obj)        

    if not music_data["play_sound"]:
        music_playing = True
        pygame.mixer.music.unpause()

        with open(file_path, 'w') as file_obj:
            json.dump({"play_sound": True}, file_obj)  

    return music_playing


def increase_speed(game_values, level, point_value):
    """
    Mocks game levels by increasing speed of snake once 
    certain point levels are reached. Done until level 7 is reached.
    Increases every 120 points.
    return game_values dictionary.
    """
    if level <= 6:
        if game_values["score"] >= point_value + 120:
            game_values["snake"]["snake_speed"] += 5
            level += 1
            point_value += 120
    
    return game_values, level, point_value 
