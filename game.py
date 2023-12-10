from grid import Grid
from blocks import *
from random import choice
import pygame

class Game:
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.held_block = None
		self.swapped = False
		self.game_over = False
		self.scoring = {
			0: 0,
			1: 40,
			2: 100,
			3: 300,
			4: 1200,
		}
		self.score = 0
		pygame.mixer.music.load("music.mp3")
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)

	def update_score(self, lines_cleared, move_down_points):
		self.score += (self.scoring[lines_cleared] + move_down_points)

	def get_random_block(self):
		# Returns a random block shape and removes from the pool of selections.
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = choice(self.blocks)
		self.blocks.remove(block)
		return block
	
	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False: # Checks for collisions or out of bounds
			self.current_block.move(0, 1)
	
	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False: # Checks for collisions or out of bounds
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False: # Checks for collisions or out of bounds
			self.current_block.move(-1, 0)
			self.lock_block()

	def hard_drop(self):
		# Hard drop all the way to the bottom of the possible play area without delay.
		collided = False
		while collided == False:
			self.current_block.move(1, 0)
			if self.block_inside() == False or self.block_fits() == False: # Checks for collisions or out of bounds
				collided = True
				self.current_block.move(-1, 0)
				self.lock_block()

	def hold(self):
		if self.swapped == False:
			self.swapped = True
		else:
			return
		self.current_block.rotation_state = 0
		if self.held_block == None:
			self.held_block = self.current_block
			self.current_block = self.next_block
			if self.block_inside() == False or self.block_fits() == False: # Checks for collisions or out of bounds
				self.current_block = self.held_block
				self.held_block = None
				return
			self.next_block = self.get_random_block()
		else:
			self.held_block, self.current_block = self.swap(self.held_block, self.current_block)
		if self.current_block.id == 3:
			self.current_block.row_offset = -1
			self.current_block.column_offset = 3
		elif self.current_block.id == 4:
			self.current_block.row_offset = 0
			self.current_block.column_offset = 4
		else:
			self.current_block.row_offset = 0
			self.current_block.column_offset = 3

	def swap(self, first_block, second_block):
		return (second_block, first_block)

	def lock_block(self):
		# Locks the block in place and changes block to a newly drawn block.
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id # Labels the grid with these colours so that the blocks remain drawn even after object is switched.
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		self.swapped = False
		lines_cleared = self.grid.clear_full_rows() # Searches for any completed rows and clears them.
		self.update_score(lines_cleared, 0)
		if self.block_fits() == False: # If a block reaches the bottom and doesn't fit, then the game is over.
			self.game_over = True

	def block_fits(self):
		# Checks for if the block fits into a potential location.
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		# Rotates the block using the 4 total rotations stored in Block().cells
		self.current_block.rotate()
		if self.block_inside() == False:
			self.current_block.un_rotate()

	def block_inside(self):
		# Checks to see if a given block is inside the playing area.
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True
	
	def reset(self):
		# Game reset - resets all parameters for a new game.
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.held_block = None
		self.swapped = False
		self.score = 0
	
	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 0, 0)
		self.next_block.draw(screen, 258, 270)
		if self.held_block != None:
			self.held_block.held_draw(screen, 55, 110)