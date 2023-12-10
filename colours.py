class Colours:
	# Initialise all colours to be used, here for easy editing.
	dark_gray = (42, 42, 42)
	green = (17, 205, 89)
	red = (239, 62, 54)
	orange = (226, 116, 17)
	yellow = (250, 223, 29)
	purple = (160, 18, 160)
	cyan = (65, 226, 186)
	blue = (21, 96, 185)
	black = (28, 28, 28)
	white = (255, 255, 255)
	light_gray = (170, 170, 170)

	@classmethod
	def get_cell_colours(cls):
		return [cls.dark_gray, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]