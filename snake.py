import json
import pygame
import event_recognition as er
import initialisation_display as id


def help_instructions():
    """Displays available commands/keypresses to user."""
    help = """
Snake Moves Continously in Direction its Facing.

Available Commands:
  * Up (keypad): Moves Snake Up.
  * Down (keypad): Moves Snake Down.
  * Left (keypad): Moves Snake Left.
  * Right (keypad): Moves Snake Right.
  * Spacebar: Pauses and Unpauses Game.
  * H-key (When Game Paused): Displays these instructions.
  * M-key: Mutes/Unmutes Game Music.
  * exit icon: Closes/Exits Game.\n"""

    return help


def is_game_over(game_values):
    """Determines whether the game is over."""
    game_done = False
    snake_body = game_values["snake"]["snake_body"]
    head_pos = snake_body[0]
    
    if head_pos[0] < 0 or head_pos[0] > (id.window_x - 13):  
        game_done = True
        id.game_over(game_values)
    if head_pos[1] < 0 or head_pos[1] > (id.window_y - 13): 
        game_done = True
        id.game_over(game_values)
    
    # Touching snake body (Self-consumption).
    for body_part in snake_body[1:]:  
        if head_pos == body_part:
            game_done = True
            id.game_over(game_values)
            break

    return game_done


def new_high_score(round_score):
    """Sets new game high score."""
    hscore_data = id.get_high_score()
   
    if round_score > hscore_data[1]:
        print("\nCongratulations you have set a new High Score!")
        
        message = "Provide us your username to store the High Score: "
        username = input(message).strip()

        with open("high_score.json", 'w') as file_obj:  
            hscore_data = {"username": username, "high_score": round_score}           
            json.dump(hscore_data, file_obj)


def cont_playing():
    """Determines whether user would like to play another round."""
    message = "\nWould you Like to Continue Playing? "
    message += "(Y for Yes/ Any Key for No)\nChoice: "
    cont_game = input(message).strip().upper()

    if cont_game == "Y": 
        return True
    else:
        print("Sad to See You Go, Hope to See You Soon!") 
        return False


def run_game(help_display, sound_file):
    """Calls all necessary functions to run snake game."""
    id.setup_pygame()
    game_values = id.initialise_game_values()
    music_playing = id.play_music()
    
    # Game level that determines speed of snake.
    level, point_value = 1, 0

    # Manages direction changes, initially set to initial direction.
    pot_direction = game_values["direction"]

    while True:
        pot_direction, music_playing = er.event_recognition(pot_direction, 
            music_playing, help_display, sound_file)  
        game_values = er.update_direction(pot_direction, game_values)
        game_values = er.continuous_movement(game_values)
        
        game_values, fruit_consumed = er.detect_consumption(game_values)

        if fruit_consumed:
            game_values["fruit_pos"] = id.fruit_positioning(game_values) 

        elif not fruit_consumed:
            # Shorten snake body (Reflect Continuous Movement).
            game_values["snake"]["snake_body"].pop()  

        id.display_game(game_values)
        game_done = is_game_over(game_values)

        if game_done: 
            new_high_score(game_values["score"])
            return

        # Continuosly displaying score.
        id.display_score(1, id.COLOURS["WHITE"], "times new roman", 
            20, game_values["score"])
        
        game_values, level, point_value = er.increase_speed(game_values, 
            level, point_value)

        # Refresh game screen.
        pygame.display.update()
        # Refresh fps.
        id.fps.tick(game_values["snake"]["snake_speed"])


def main():
    """Controls main game loop."""
    # Display welcome message help instructions.
    print("Welcome to Snake!")
    help_display = help_instructions()
    print(help_display)

    sound_file = "sounds/sound_tracker.json"

    # Paused to allow user to read instruction
    while True:
        cont_game = input("Enter any Key to Proceed to Game.\nPaused: ")
        break

    play_game = True

    while play_game:
        run_game(help_display, sound_file)
        play_game = cont_playing()


if __name__ == "__main__":
    main()