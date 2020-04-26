import SETTINGS

class Map():

	def __init__(self):
		self.text_map = SETTINGS.text_map
		self.map_of_tiles, self.map, self.flat_map = self.create_map()

	def create_map(self):
		set_of_coords_tiles = set()
		map = {}
		for y,row in enumerate(self.text_map):
			for x,char in enumerate(row):
				if char != ' ':
					set_of_coords_tiles.add((x * SETTINGS.scale_map, y * SETTINGS.scale_map,
									 SETTINGS.scale_map, SETTINGS.scale_map))
					map[(x, y)] = char
		return set_of_coords_tiles, map, set(map.keys())
