# Web-compatible entry point for Pygbag
# This file is the main entry point for web deployment

import asyncio
import pygame
import random
import json

# Game constants
WINDOW_X, WINDOW_Y = 936, 624
CELL_SIZE = 13

# Colors (RGB)
COLOURS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "RED": (255, 0, 0),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (40, 40, 40),
}

# Game states
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_ENTER_NAME = "enter_name"


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.fruit = pygame.image.load("pictures/fruit.png").convert_alpha()
        self.fruit = pygame.transform.scale(self.fruit, (CELL_SIZE, CELL_SIZE))
        
        # Try to load music (may fail on some browsers)
        self.music_loaded = False
        try:
            pygame.mixer.init()
            # Try ogg first, fall back to wav
            try:
                pygame.mixer.music.load("sounds/theme_music.ogg")
            except:
                pygame.mixer.music.load("sounds/Angry Birds Theme Song.wav")
            self.music_loaded = True
        except Exception as e:
            print(f"Could not load music: {e}")
        
        self.music_playing = False
        self.state = STATE_START
        self.username_input = ""
        self.reset_game()
        
    def reset_game(self):
        """Initialize/reset game values."""
        self.snake_speed = 15
        snake_head = [104, 65]
        self.snake_body = [
            snake_head,
            [snake_head[0] - CELL_SIZE, snake_head[1]],
            [snake_head[0] - 2 * CELL_SIZE, snake_head[1]],
            [snake_head[0] - 3 * CELL_SIZE, snake_head[1]],
        ]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.point_value = 0
        self.fruit_pos = self.new_fruit_position()
        
    def new_fruit_position(self):
        """Generate new fruit position not on snake."""
        while True:
            pos = [
                random.randrange(1, (WINDOW_X // CELL_SIZE) - 1) * CELL_SIZE,
                random.randrange(1, (WINDOW_Y // CELL_SIZE) - 1) * CELL_SIZE,
            ]
            if pos not in self.snake_body:
                return pos
    
    def get_high_score(self):
        """Get high score from storage (localStorage in browser, file on desktop)."""
        try:
            # Try browser localStorage first (Pygbag/web environment)
            import platform
            if hasattr(platform, 'window') and hasattr(platform.window, 'localStorage'):
                stored = platform.window.localStorage.getItem("snake_high_score")
                if stored:
                    data = json.loads(stored)
                    return data.get("username", "Nobody"), data.get("high_score", 0)
                return "Nobody", 0
        except:
            pass
        
        # Fall back to file-based storage (desktop)
        try:
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("username", "Nobody"), data.get("high_score", 0)
        except:
            return "Nobody", 0
    
    def save_high_score(self, username, score):
        """Save high score to storage (localStorage in browser, file on desktop)."""
        data = {"username": username, "high_score": score}
        
        try:
            # Try browser localStorage first (Pygbag/web environment)
            import platform
            if hasattr(platform, 'window') and hasattr(platform.window, 'localStorage'):
                platform.window.localStorage.setItem("snake_high_score", json.dumps(data))
                print(f"High score saved to localStorage: {username} - {score}")
                return
        except Exception as e:
            print(f"localStorage save failed: {e}")
        
        # Fall back to file-based storage (desktop)
        try:
            with open("high_score.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Could not save high score: {e}")
    
    def toggle_music(self):
        """Toggle music on/off."""
        if not self.music_loaded:
            return
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.unpause()
            self.music_playing = True
    
    def draw_text(self, text, size, color, center_x, center_y, font_name="Arial"):
        """Draw centered text on screen."""
        font = pygame.font.SysFont(font_name, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(center_x, center_y))
        self.screen.blit(surface, rect)
        
    def draw_text_left(self, text, size, color, x, y, font_name="Arial"):
        """Draw left-aligned text on screen."""
        font = pygame.font.SysFont(font_name, size)
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
        
    def draw_start_screen(self):
        """Draw the start/title screen."""
        self.screen.fill(COLOURS["BLACK"])
        
        # Title
        self.draw_text("🐍 SNAKE GAME 🐍", 60, COLOURS["GREEN"], WINDOW_X // 2, 150)
        
        # Instructions
        instructions = [
            "Use ARROW KEYS to move the snake",
            "Eat fruit to grow and score points",
            "Don't hit the walls or yourself!",
            "",
            "SPACE - Pause/Unpause",
            "M - Toggle Music",
            "H - Show Help (when paused)",
        ]
        
        y = 250
        for line in instructions:
            self.draw_text(line, 24, COLOURS["WHITE"], WINDOW_X // 2, y)
            y += 35
            
        # High score
        username, high_score = self.get_high_score()
        self.draw_text(f"High Score: {username} ({high_score})", 28, COLOURS["GREEN"], WINDOW_X // 2, 500)
        
        # Start prompt
        self.draw_text("Press SPACE to Start!", 36, COLOURS["WHITE"], WINDOW_X // 2, 570)
        
    def draw_game(self):
        """Draw the game state."""
        self.screen.fill(COLOURS["BLACK"])
        
        # Draw snake
        for i, pos in enumerate(self.snake_body):
            color = COLOURS["BLUE"] if i == 0 else COLOURS["GREEN"]
            pygame.draw.rect(self.screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        
        # Draw fruit
        self.screen.blit(self.fruit, self.fruit_pos)
        
        # Draw score
        self.draw_text_left(f"Score: {self.score}", 20, COLOURS["WHITE"], 10, 5)
        
        # Draw high score
        username, high_score = self.get_high_score()
        font = pygame.font.SysFont("Arial", 20)
        hs_text = f"High Score: {username} ({high_score})"
        hs_surface = font.render(hs_text, True, COLOURS["WHITE"])
        hs_rect = hs_surface.get_rect(topright=(WINDOW_X - 10, 5))
        self.screen.blit(hs_surface, hs_rect)
        
    def draw_pause_overlay(self):
        """Draw pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_X, WINDOW_Y))
        overlay.fill(COLOURS["BLACK"])
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("PAUSED", 60, COLOURS["WHITE"], WINDOW_X // 2, WINDOW_Y // 2 - 50)
        self.draw_text("Press SPACE to Resume", 30, COLOURS["GRAY"], WINDOW_X // 2, WINDOW_Y // 2 + 20)
        self.draw_text("Press H for Help", 24, COLOURS["GRAY"], WINDOW_X // 2, WINDOW_Y // 2 + 60)
        
    def draw_help_overlay(self):
        """Draw help screen."""
        overlay = pygame.Surface((WINDOW_X, WINDOW_Y))
        overlay.fill(COLOURS["DARK_GRAY"])
        overlay.set_alpha(240)
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("CONTROLS", 48, COLOURS["GREEN"], WINDOW_X // 2, 80)
        
        help_lines = [
            "↑ ↓ ← → - Move Snake",
            "SPACE - Pause/Unpause",
            "M - Toggle Music",
            "R - Restart (after Game Over)",
            "",
            "Collect fruit to score points!",
            "Speed increases every 120 points.",
            "Don't hit walls or yourself!",
        ]
        
        y = 160
        for line in help_lines:
            self.draw_text(line, 28, COLOURS["WHITE"], WINDOW_X // 2, y)
            y += 45
            
        self.draw_text("Press any key to continue", 24, COLOURS["GRAY"], WINDOW_X // 2, 550)
        
    def draw_game_over(self):
        """Draw game over screen."""
        self.screen.fill(COLOURS["BLACK"])
        
        self.draw_text("GAME OVER", 70, COLOURS["RED"], WINDOW_X // 2, 150)
        self.draw_text(f"Your Score: {self.score}", 40, COLOURS["WHITE"], WINDOW_X // 2, 250)
        
        # Check if new high score
        _, high_score = self.get_high_score()
        if self.score > high_score:
            self.draw_text("🎉 NEW HIGH SCORE! 🎉", 36, COLOURS["GREEN"], WINDOW_X // 2, 320)
            self.draw_text("Press ENTER to save your name", 28, COLOURS["WHITE"], WINDOW_X // 2, 380)
        
        self.draw_text("Press R to Restart", 30, COLOURS["GRAY"], WINDOW_X // 2, 480)
        self.draw_text("Press SPACE for Menu", 24, COLOURS["GRAY"], WINDOW_X // 2, 530)
        
    def draw_name_input(self):
        """Draw name input screen."""
        self.screen.fill(COLOURS["BLACK"])
        
        self.draw_text("🎉 NEW HIGH SCORE! 🎉", 50, COLOURS["GREEN"], WINDOW_X // 2, 150)
        self.draw_text(f"Score: {self.score}", 36, COLOURS["WHITE"], WINDOW_X // 2, 220)
        
        self.draw_text("Enter your name:", 30, COLOURS["WHITE"], WINDOW_X // 2, 320)
        
        # Draw input box
        input_box = pygame.Rect(WINDOW_X // 2 - 150, 360, 300, 50)
        pygame.draw.rect(self.screen, COLOURS["WHITE"], input_box, 2)
        
        # Draw current input
        self.draw_text(self.username_input + "_", 32, COLOURS["GREEN"], WINDOW_X // 2, 385)
        
        self.draw_text("Press ENTER to confirm", 24, COLOURS["GRAY"], WINDOW_X // 2, 450)
        self.draw_text("(Max 15 characters)", 20, COLOURS["GRAY"], WINDOW_X // 2, 490)
        
    async def handle_events(self):
        """Handle pygame events based on current state."""
        show_help = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_START:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                        self.reset_game()
                        
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    elif event.key == pygame.K_SPACE:
                        self.state = STATE_PAUSED
                    elif event.key == pygame.K_m:
                        self.toggle_music()
                        
                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_h:
                        show_help = True
                    elif event.key == pygame.K_m:
                        self.toggle_music()
                        
                elif self.state == STATE_GAME_OVER:
                    _, high_score = self.get_high_score()
                    if event.key == pygame.K_RETURN and self.score > high_score:
                        self.username_input = ""
                        self.state = STATE_ENTER_NAME
                    elif event.key == pygame.K_r:
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_SPACE:
                        self.state = STATE_START
                        
                elif self.state == STATE_ENTER_NAME:
                    if event.key == pygame.K_RETURN:
                        if self.username_input.strip():
                            self.save_high_score(self.username_input.strip(), self.score)
                        self.state = STATE_START
                    elif event.key == pygame.K_BACKSPACE:
                        self.username_input = self.username_input[:-1]
                    elif len(self.username_input) < 15:
                        # Add character if printable
                        if event.unicode.isprintable() and event.unicode:
                            self.username_input += event.unicode
                            
        # Handle help display (blocks until key press)
        if show_help:
            self.draw_help_overlay()
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                await asyncio.sleep(0)
                        
        return True
    
    def update_game(self):
        """Update game logic."""
        if self.state != STATE_PLAYING:
            return
            
        # Move snake
        head = self.snake_body[0].copy()
        if self.direction == "UP":
            head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            head[1] += CELL_SIZE
        elif self.direction == "LEFT":
            head[0] -= CELL_SIZE
        elif self.direction == "RIGHT":
            head[0] += CELL_SIZE
            
        self.snake_body.insert(0, head)
        
        # Check fruit consumption
        if head == self.fruit_pos:
            self.score += 10
            self.fruit_pos = self.new_fruit_position()
            
            # Speed increase every 120 points
            if self.level <= 6 and self.score >= self.point_value + 120:
                self.snake_speed += 5
                self.level += 1
                self.point_value += 120
        else:
            self.snake_body.pop()
            
        # Check collisions
        # Wall collision
        if (head[0] < 0 or head[0] > WINDOW_X - CELL_SIZE or
            head[1] < 0 or head[1] > WINDOW_Y - CELL_SIZE):
            self.state = STATE_GAME_OVER
            return
            
        # Self collision
        if head in self.snake_body[1:]:
            self.state = STATE_GAME_OVER
            return
    
    def draw(self):
        """Draw current state."""
        if self.state == STATE_START:
            self.draw_start_screen()
        elif self.state == STATE_PLAYING:
            self.draw_game()
        elif self.state == STATE_PAUSED:
            self.draw_game()
            self.draw_pause_overlay()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        elif self.state == STATE_ENTER_NAME:
            self.draw_name_input()
            
        pygame.display.update()


async def main():
    """Main async game loop for Pygbag compatibility."""
    game = SnakeGame()
    running = True
    
    while running:
        running = await game.handle_events()
        game.update_game()
        game.draw()
        
        # Control frame rate
        game.clock.tick(game.snake_speed if game.state == STATE_PLAYING else 30)
        
        # Yield control to browser - REQUIRED for Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()


# Entry point for both desktop and web
if __name__ == "__main__":
    asyncio.run(main())
