import pygame, sys
from game import Game
from colours import Colours

# Set constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
TIME = 500

pygame.init() # Initialise pygame

title_font = pygame.font.SysFont("verdana", 30) # Create a pygame font from a system font.

score_surface = title_font.render("Score", True, Colours.white)
score_rect = pygame.Rect(515, 75, 170, 60)

next_surface = title_font.render("Next", True, Colours.white)
next_rect = pygame.Rect(515, 215, 170, 180)

held_surface = title_font.render("Held", True, Colours.white)
held_rect = pygame.Rect(15, 75, 170, 180)

game_over_surface = title_font.render("Game Over!", True, Colours.white)

screen = pygame.display.set_mode((SCREEN_WIDTH+400, SCREEN_HEIGHT+20)) # Draw in the pygame screen

pygame.display.set_caption("TETRIS") # Window title

clock = pygame.time.Clock() # Refresh rate clock

game = Game() # Create a game class from game.py for processing

# Create a clock for moving the block down (game speed).
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, TIME)

while True:
	# Event Handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == GAME_UPDATE and game.game_over == False: # Automatic block moving down
			game.move_down()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_LCTRL and game.game_over == False:
				game.rotate()
			if event.key == pygame.K_SPACE and game.game_over == False:
				game.hard_drop()
				game.update_score(0, 2)
	keys = pygame.key.get_pressed()
	if game.game_over == True:
		if keys[pygame.K_RETURN]:
			game.reset()
			game.game_over = False
	if keys[pygame.K_LEFT] and game.game_over == False:
		game.move_left()
	if keys[pygame.K_RIGHT] and game.game_over == False:
		game.move_right()
	if keys[pygame.K_DOWN] and game.game_over == False:
		game.move_down()
		game.update_score(0, 1)
	if keys[pygame.K_LSHIFT] and game.game_over == False:
		game.hold()
	
	

	# Drawing
	score_value_surface = title_font.render(str(game.score), True, Colours.white)
	screen.fill(Colours.black)
	if game.game_over == True:
		screen.blit(game_over_surface, (510, 450, 50, 50))
	pygame.draw.rect(screen, Colours.dark_gray, score_rect, 0, 8)
	pygame.draw.rect(screen, Colours.dark_gray, next_rect, 0, 8)
	pygame.draw.rect(screen, Colours.dark_gray, held_rect, 0, 8)
	screen.blit(score_surface, (560, 20, 50, 50))
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
	screen.blit(next_surface, (565, 165, 50, 50))
	screen.blit(held_surface, (65, 20, 50, 50))
	game.draw(screen)

	pygame.display.update()
	clock.tick(20)