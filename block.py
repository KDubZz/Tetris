import pygame
from colours import Colours
from position import Position
from grid import Grid

class Block:
	def __init__(self, id):
		self.id = id
		self.grid = Grid()
		self.cells = {}
		self.cell_size = 30
		self.row_offset = 0
		self.column_offset = 0
		self.rotation_state = 0
		self.colours = Colours.get_cell_colours()
		self.margin, self.draw_offset, self.x_offset = self.grid.get_offsets()

	def move(self, rows, columns):
		# Adds inputted data to move the block by a specified amount by the origin.
		self.row_offset += rows
		self.column_offset += columns

	def get_cell_positions(self):
		# Updates all of the cell locations within the block by the offsets provided.
		tiles = self.cells.get(self.rotation_state, self.cells[1])
		moved_tiles = []
		for position in tiles:
			new_position = Position(position.row + self.row_offset, position.column + self.column_offset)
			moved_tiles.append(new_position)
		return moved_tiles
	
	def rotate(self):
		# Adjusts the rotation_state which is then used in get_cell_positions.
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0
	
	def un_rotate(self):
		# Undo a rotate by decrementing rotation_state.
		self.rotation_state -= 1
		if self.rotation_state == 0:
			self.rotation_state = len(self.cells) - 1

	def draw(self, screen, offset_x, offset_y):
		# Draws the block onto the screen.
		tiles = self.get_cell_positions()
		for tile in tiles:
			tile_rect = pygame.Rect(
				tile.column * self.cell_size + self.margin + self.draw_offset + self.x_offset + offset_x,
				tile.row * self.cell_size + self.margin + self.draw_offset + offset_y,
				self.cell_size - self.margin,
				self.cell_size - self.margin)
			pygame.draw.rect(screen, self.colours[self.id], tile_rect)