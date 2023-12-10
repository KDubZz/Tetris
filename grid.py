import pygame
from colours import Colours

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

class Grid:
	def __init__(self):
		self.num_rows = 20
		self.num_cols = 10
		self.cell_size = 30
		self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
		self.colours = Colours.get_cell_colours()
		self.margin = 4
		self.draw_offset = 10
		self.x_offset = 190
	
	def print_grid(self):
		# For debugging and initial play mainly.
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				print(self.grid[row][column], end = ' ')
			print()

	def is_inside(self, row, column):
		# Check to see if an inputted row and column are within the bounds of the nested list (grid).
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

	def is_empty(self, row, column):
		# Check to see if a cell is vacant.
		if self.grid[row][column] == 0:
			return True
		return False
	
	def is_row_full(self, row):
		# Check to see if a row has been completed.
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True
	
	def clear_row(self, row):
		# Clears a given row.
		for column in range(self.num_cols):
			self.grid[row][column] = 0
	
	def move_row_down(self, row, num_rows):
		# Moves a given row down by a specified number of rows.
		for column in range(self.num_cols):
			self.grid[row+num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	def clear_full_rows(self):
		# Reads up the rows and clears any full rows present, then moves all of the remaining rows down by the number of completed rows.
		completed = 0
		for row in range(self.num_rows - 1, 0, -1):
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed

	def get_offsets(self):
		# Returns margin and drawing offset for use in block.py
		return self.margin, self.draw_offset, self.x_offset
	
	def reset(self):
		# Fully resets the grid back to empty.
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0
	
	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(
					column * self.cell_size + self.margin + self.draw_offset + self.x_offset,
					row*self.cell_size+self.margin + self.draw_offset,
					self.cell_size-self.margin,
					self.cell_size-self.margin)
				pygame.draw.rect(screen, self.colours[cell_value], cell_rect)