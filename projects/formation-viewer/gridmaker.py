import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def add_cell(root: ET.Element, x, y, size=32, fill="#000000"):
	cell = ET.SubElement(root, "rect", {
		"x":str(x),
		"y":str(y),
		"width":str(size),
		"height":str(size),
		"transform":"matrix(1, 0, 0, 1, 0, 0)",
		"fill":fill,
		"fill-opacity":"1",
		"stroke":"#000000",
		"stroke-width":"1",
		"stroke-dasharray":"1 2",
		"opacity":"1",
		"id":"Rectangle_{}_{}".format(x, y),
	})
	return cell

def add_marker(root: ET.Element, x, y, size=32, fill="#ff0000", stroke_width=4, label: str = None):
	marker_group = ET.SubElement(root, "g", { "id": f"Marker_{x}_{y}" })
	ET.SubElement(marker_group, "line", {
		"x1": str(x - size/2),
		"y1": str(y - size/2),
		"x2": str(x + size/2),
		"y2": str(y + size/2),
		"stroke": fill,
		"stroke-width": str(stroke_width)
	})
	ET.SubElement(marker_group, "line", {
		"x1": str(x + size/2),
		"y1": str(y - size/2),
		"x2": str(x - size/2),
		"y2": str(y + size/2),
		"stroke": fill,
		"stroke-width": str(stroke_width)
	})
	if label:
		ET.SubElement(marker_group, "text", {
			"x": str(x),
			"y": str(y),
			"fill": "#000000",
			"font-family": "sans-serif",
			"font-size": "10",
			"text-anchor": "middle",
			"dominant-baseline": "middle"
		}).text = label


def generate_svg(markers: list = []):
	tile_size = 32

	num_of_chunk_x = 3
	num_of_chunk_y = 3

	chunk_size = 20
	chunk_color = "#a89ea9"
	chunk_color_alt = "#8e98a5"
	chunk_border_color = "#cececf"
	
	total_width = chunk_size * tile_size * num_of_chunk_x
	total_height = chunk_size * tile_size * num_of_chunk_y

	root = ET.Element("svg", {
		"version": "1.1",
		"viewBox": f"0 0 {total_width} {total_height}",
		"xmlns": "http://www.w3.org/2000/svg"
	})

	grid_group = ET.SubElement(root, "g", { "id": f"Grid" })

	# Draw the grid cells first (so they appear in the background)
	for chunk_x in range(0, num_of_chunk_x):
		for chunk_y in range(0, num_of_chunk_y):
			for local_x in range(0, chunk_size):
				for local_y in range(0, chunk_size):
					x = (chunk_x * chunk_size + local_x) * tile_size
					y = (chunk_y * chunk_size + local_y) * tile_size
					
					is_border = (local_x == 0 or local_x == chunk_size-1) or \
								(local_y == 0 or local_y == chunk_size-1)
					
					if is_border:
						add_cell(grid_group, x, y, tile_size, chunk_border_color)
					else:
						if chunk_x == 2:
							add_cell(grid_group, x, y, tile_size, chunk_color_alt)
						else:
							add_cell(grid_group, x, y, tile_size, chunk_color)

	# Draw all the markers on top of the grid
	for marker_tile_coords in markers:
		tile_x, tile_y, color = marker_tile_coords
		# Convert tile coordinates to pixel coordinates for drawing
		pixel_x = tile_x * tile_size
		pixel_y = tile_y * tile_size
		add_marker(root, pixel_x, pixel_y, size=tile_size*3/4, fill=color)
	
	tree = ET.ElementTree(root)
	# Add the XML declaration for better SVG compatibility
	tree.write(os.path.join(BASE_DIR, "grid.svg"), encoding="utf-8", xml_declaration=True)

def get_marker_silent_wave(
		mid_point: tuple[int, int], 
		gap = 3, 
		total_men = 12, 
		color = "#ff0000"
	) -> list[tuple[int, int, str]]:
	markers: list[tuple[int, int, str]] = []
	for i in range(0, total_men):
		_x = mid_point[0] - (total_men-1)*gap/2 + i*gap
		_y = mid_point[1]
		markers.append(
			(_x, _y, color)
		)
	return markers

def get_marker_saturn(
		mid_point: tuple[int, int], 
		saturn_throw_gap = 6, gap = 3, 
		total_men = 12, 
		color = "#4d0000"
	) -> list[tuple[int, int, str]]:
	markers: list[tuple[int, int, str]] = []
	_y_offfset = 0
	for i in range(0, total_men):
		_x = mid_point[0]
		if i % 2 == 0:
			_y_offfset -= gap
			_x -= saturn_throw_gap/2
		else:
			_x += saturn_throw_gap/2
		_y = mid_point[1] + _y_offfset
		markers.append(
			(_x, _y, color)
		)
	return markers

def get_marker_formation(
		mid_point: tuple[int, int], 
		formation_pattern: dict[tuple[int, int], str], 
		gap_multiplier = 1, color = "#000000",
		center_formation: bool = False
	) -> list[tuple[int, int, str]]:
	markers: list[tuple[int, int, str]] = []
	
	if not formation_pattern:
		return []
	
	offset_x, offset_y = 0, 0

	if center_formation:
		all_x = [pos[0] for pos in formation_pattern]
		all_y = [pos[1] for pos in formation_pattern]
		min_x, max_x = min(all_x), max(all_x)
		min_y, max_y = min(all_y), max(all_y)
		
		pattern_center_x = (min_x + max_x) / 2.0
		pattern_center_y = (min_y + max_y) / 2.0
		
		offset_x = -pattern_center_x
		offset_y = -pattern_center_y
	
	for relative_pos in formation_pattern:
		_x = mid_point[0] + (relative_pos[0] + offset_x) * gap_multiplier
		_y = mid_point[1] + (relative_pos[1] + offset_y) * gap_multiplier
		markers.append(
			(_x, _y, color)
		)
	return markers

def create_formation_2(inner_spacing = 1, outer_spacing = 2)->dict[tuple[int, int], str]:
	return {
		(0, -outer_spacing*2): "",
		(outer_spacing, -outer_spacing): "",
		(outer_spacing*2, 0): "",
		(outer_spacing, outer_spacing): "",
		(0, outer_spacing*2): "",
		(-outer_spacing, outer_spacing): "",
		(-outer_spacing*2, 0): "",
		(-outer_spacing, -outer_spacing): "",

		(-inner_spacing, 0): "",
		(inner_spacing, 0): "",
		(0, -inner_spacing): "",
		(0, inner_spacing): "",
	}

def main():
	markers_to_draw = [
	]

	# Generate markers for 1st formation
	markers_to_draw += get_marker_formation(
		mid_point = (30, 35),
		formation_pattern = {
			(0, 0): "IL",
			(1, 0): "SE",
			(2, 0): "JD",
			(3, 0): "EL",
			(0, -1): "RY",
			(1, -1): "DM",
			(2, -1): "ER",
			(3, -1): "JO",
			(0, -2): "AL",
			(1, -2): "CW",
			(2, -2): "JO",
			(3, -2): "LR",
		},
		color="#0000ff",
		gap_multiplier=6,
		center_formation=True
	)

	# Generate markers for 2nd formation
	create_formation_2()
	markers_to_draw += get_marker_formation(
		mid_point = (30, 35),
		formation_pattern = create_formation_2(1,1.5),
		color="#77ff00",
		gap_multiplier=4,
		center_formation=True
	)

	# Generate markers for 3rd formation
	markers_to_draw += get_marker_formation(
		mid_point = (30, 37),
		formation_pattern = {
			(0, 0): "",
			
			(-1, -1): "",
			(1, -1): "",
			
			(-2, -2): "",
			(0, -2): "",
			(2, -2): "",


			(-1, -3): "",
			(1, -3): "",
			(-3, -3): "",
			(3, -3): "",

			(-2, -4): "",
			(2, -4): "",
		},
		color="#ff9500",
		gap_multiplier=6,
		center_formation=True
	)

	# generate markers for silent wave
	markers_to_draw += get_marker_silent_wave(
		mid_point = (30, 40),
		gap = 3,
		total_men = 12
	)

	# Generate markers for saturn toss
	markers_to_draw += get_marker_saturn(
		mid_point = (30, 40),
		saturn_throw_gap = 6,
		gap = 3,
		total_men = 12
	)
	
	generate_svg(markers=markers_to_draw)
	print("grid.svg has been generated!")

if __name__ == "__main__":
	main()