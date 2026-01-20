import sys
import pygame

from assets.text import Text
from assets.image import Image
from photos.loader import *
from assets.tilemap import TileMap
from entities.player import Player
from entities.camera import Camera
from utils import *


class Game:
    """
    Main game class.

    Responsibilities:
    - Initialize pygame and all game systems
    - Manage game states (start screen, gameplay, game over)
    - Handle input events
    - Update player, camera, and world
    - Render all objects to the screen
    - Control the main game loop
    """

    def __init__(self):
        # --- Initialize pygame ---
        pygame.init()

        # --- Create main window ---
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Mario (D&D)")
        pygame.display.set_icon(pygame.image.load('photos/icon.png'))

        # --- Clock for FPS control ---
        self.clock = pygame.time.Clock()

        # ---------------- CAMERA ----------------
        # Camera follows the player and offsets world rendering
        self.camera = Camera(config.HEIGHT, config.WIDTH)

        # ---------------- BACKGROUND ----------------
        # Parallax background (moves slower than the world)
        self.background = Image(
            is_parallax=True,
            scale=scale_size(config.BACKGROUND_SIZE),
            image_folder=background_images
        )

        # ---------------- TILEMAP ----------------
        # Load the level from Tiled (.tmx file)
        self.tilemap = TileMap("level/1_level/World.tmx")

        # ---------------- PLAYER ----------------
        # Create player instance and sprite group
        self.player = Player(
            scale_pos(config.PLAYER_POS),
            scale_size(config.PLAYER_SIZE)
        )
        self.sprites = pygame.sprite.Group(self.player)

        # ---------------- SCORE ----------------
        # On-screen score text
        self.score = Text(
            "0",
            int(config.HEIGHT * 0.075),
            scale_pos(config.SCORE_POS),
            config.TEXT_COLOR
        )
        self.score_group = pygame.sprite.Group(self.score)

        # ---------------- START SCREEN ----------------
        # Title and start button
        self.game_name = Text(
            "Mario (D&D)",
            int(config.HEIGHT * 0.25),
            scale_pos(config.GAME_NAME_POS),
            "purple"
        )
        self.start_game_text = Text(
            "Start Game",
            int(config.HEIGHT * 0.125),
            scale_pos(config.BUTTON_POS),
            "lightyellow"
        )
        self.game_start_group = pygame.sprite.Group(
            self.game_name,
            self.start_game_text
        )

        # ---------------- GAME OVER SCREEN ----------------
        # Game over text and retry button
        self.game_over_text = Text(
            "Game Over",
            int(config.HEIGHT * 0.225),
            scale_pos(config.GAME_NAME_POS),
            "darkred"
        )
        self.retry_text = Text(
            "Retry",
            int(config.HEIGHT * 0.125),
            scale_pos(config.BUTTON_POS),
            "darkred"
        )
        self.game_over_group = pygame.sprite.Group(
            self.game_over_text,
            self.retry_text
        )

        # ---------------- GAME STATE ----------------
        self.game_start = True      # Start screen active
        self.running = True         # Main loop flag

    # --------------------------------------------------
    # Handle all pygame events (keyboard, mouse, quit)
    # --------------------------------------------------
    def handle_events(self):
        self.event_list = pygame.event.get()

        for event in self.event_list:
            # Exit game
            if event.type == pygame.QUIT:
                self.running = False

            # Toggle fullscreen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    config.FULLSCREEN = not config.FULLSCREEN
                    if config.FULLSCREEN:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((1280, 720))

    # --------------------------------------------------
    # Draw background and all world tiles with camera offset
    # --------------------------------------------------
    def draw_world(self):
        # Draw parallax background
        self.background.draw(self.screen)

        # Draw decorative (non-collidable) tiles
        for tile in self.tilemap.offgrid_tiles:
            self.screen.blit(tile.image, tile.rect.topleft - self.camera.offset)

        # Draw solid tiles (platforms)
        for tile in self.tilemap.tilemap:
            self.screen.blit(tile.image, tile.rect.topleft - self.camera.offset)

    # --------------------------------------------------
    # Start screen logic
    # --------------------------------------------------
    def start_screen(self):
        # Draw start screen UI
        self.game_start_group.draw(self.screen)

        # Start game on mouse click
        for event in self.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_game_text.rect.collidepoint(event.pos):
                    self.game_start = False
                    config.GAME_ACTIVE = True
                    config.START_TIME = pygame.time.get_ticks()
                    config.LAST_TIME = 0

    # --------------------------------------------------
    # Main gameplay logic
    # --------------------------------------------------
    def game_active(self):
        # Calculate elapsed time
        current_time = pygame.time.get_ticks() - config.START_TIME

        # --- Update score ---
        self.score.update_text(f"Score: {current_time // 1000}")
        self.score_group.draw(self.screen)
        config.LAST_TIME = current_time // 1000

        # --- Update player ---
        self.player.update(self.event_list, current_time, self.tilemap.tilemap)

        # --- Update camera ---
        self.camera.follow(self.player)

        # --- Draw player ---
        self.screen.blit(
            self.player.image,
            self.player.rect.topleft - self.camera.offset
        )

        # --- Player fell out of the world → Game Over ---
        if self.player.rect.top > 3000:
            config.GAME_ACTIVE = False

    # --------------------------------------------------
    # Game over screen logic
    # --------------------------------------------------
    def game_over_screen(self):
        # Draw game over UI
        self.game_over_group.draw(self.screen)

        # Draw final score
        final_score = Text(
            f"Score: {config.LAST_TIME}",
            int(config.HEIGHT * 0.1),
            scale_pos(config.FINAL_SCORE_POS),
            config.TEXT_COLOR
        )
        self.screen.blit(final_score.image, final_score.rect)

        # Retry game on click
        for event in self.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.retry_text.rect.collidepoint(event.pos):
                    self.player.reset(scale_pos(config.PLAYER_POS))
                    config.GAME_ACTIVE = True
                    config.START_TIME = pygame.time.get_ticks()

    # --------------------------------------------------
    # Main game loop
    # --------------------------------------------------
    def run(self):
        while self.running:
            # Limit FPS
            self.clock.tick(60)

            # Handle input
            self.handle_events()

            # Clear screen
            self.screen.fill(config.BG_COLOR)

            # State-based logic
            if self.game_start:
                self.start_screen()

            elif config.GAME_ACTIVE:
                self.draw_world()
                self.game_active()

            else:
                self.game_over_screen()

            # Update display
            pygame.display.flip()

        # Exit safely
        pygame.quit()
        sys.exit()


Game().run()
