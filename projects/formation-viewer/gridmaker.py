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

def add_marker(root: ET.Element, x, y, size=32, fill="#ff0000", stroke_width=12, label: str = None):
	marker_group = ET.SubElement(root, "g", { "id": f"Marker_{x}_{y}" })
	ET.SubElement(marker_group, "line", {
		"x1": str(x - size/2),
		"y1": str(y - size/2),
		"x2": str(x + size/2),
		"y2": str(y + size/2),
		"opacity":"0.7",
		"stroke": fill,
		"stroke-width": str(stroke_width)
	})
	ET.SubElement(marker_group, "line", {
		"x1": str(x + size/2),
		"y1": str(y - size/2),
		"x2": str(x - size/2),
		"y2": str(y + size/2),
		"opacity":"0.7",
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


def main():
	CENTER_X = 20*3/2
	CENTER_Y = 20*3/2

	FORMATION_1_COLOR = "#eeff00"
	FORMATION_2_COLOR = "#0022ff"
	FORMATION_3_COLOR = "#ff0000"
	SW_1_COLOR = "#00ff8c"
	SW_2_COLOR = "#ff006f"
	BOX_DISTANCE = 6
	
	markers_to_draw = [
		# Formation 1 (Box)
		(CENTER_X - BOX_DISTANCE/2 - BOX_DISTANCE, CENTER_Y, FORMATION_1_COLOR),
		(CENTER_X - BOX_DISTANCE/2, CENTER_Y, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2, CENTER_Y, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2 + BOX_DISTANCE, CENTER_Y, FORMATION_1_COLOR),

		(CENTER_X - BOX_DISTANCE/2 - BOX_DISTANCE, CENTER_Y - BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X - BOX_DISTANCE/2, CENTER_Y - BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2, CENTER_Y - BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2 + BOX_DISTANCE, CENTER_Y - BOX_DISTANCE, FORMATION_1_COLOR),

		(CENTER_X - BOX_DISTANCE/2 - BOX_DISTANCE, CENTER_Y + BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X - BOX_DISTANCE/2, CENTER_Y + BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2, CENTER_Y + BOX_DISTANCE, FORMATION_1_COLOR),
		(CENTER_X + BOX_DISTANCE/2 + BOX_DISTANCE, CENTER_Y + BOX_DISTANCE, FORMATION_1_COLOR),

		# Formation 2 (Diamond)
		(CENTER_X - 4, CENTER_Y, FORMATION_2_COLOR),
		(CENTER_X + 4, CENTER_Y, FORMATION_2_COLOR),
		(CENTER_X, CENTER_Y - 4, FORMATION_2_COLOR),
		(CENTER_X, CENTER_Y + 4, FORMATION_2_COLOR),

		(CENTER_X - 12, CENTER_Y, FORMATION_2_COLOR),
		(CENTER_X - 6, CENTER_Y - 6, FORMATION_2_COLOR),
		(CENTER_X, CENTER_Y - 12, FORMATION_2_COLOR),
		(CENTER_X + 6, CENTER_Y - 6, FORMATION_2_COLOR),
		(CENTER_X + 12, CENTER_Y, FORMATION_2_COLOR),
		(CENTER_X + 6, CENTER_Y + 6, FORMATION_2_COLOR),
		(CENTER_X, CENTER_Y + 12, FORMATION_2_COLOR),
		(CENTER_X - 6, CENTER_Y + 6, FORMATION_2_COLOR),

		# Formation 3 (Heart)
		(CENTER_X - 6, CENTER_Y - 3, FORMATION_3_COLOR),
		(CENTER_X - 12, CENTER_Y - 8, FORMATION_3_COLOR),
		(CENTER_X - 18, CENTER_Y - 3, FORMATION_3_COLOR),
		(CENTER_X - 12, CENTER_Y + 2, FORMATION_3_COLOR),
		(CENTER_X - 6, CENTER_Y + 7, FORMATION_3_COLOR),
		(CENTER_X, CENTER_Y + 12, FORMATION_3_COLOR),
		(CENTER_X + 6, CENTER_Y + 7, FORMATION_3_COLOR),
		(CENTER_X + 12, CENTER_Y + 2, FORMATION_3_COLOR),
		(CENTER_X + 18, CENTER_Y - 3, FORMATION_3_COLOR),
		(CENTER_X + 12, CENTER_Y - 8, FORMATION_3_COLOR),
		(CENTER_X + 6, CENTER_Y - 3, FORMATION_3_COLOR),
		
		(CENTER_X, CENTER_Y + 4, FORMATION_3_COLOR),
		
		# Silent Wave 1
		(CENTER_X + 3.5, CENTER_Y + 15, SW_1_COLOR),
		(CENTER_X + 7.0, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X + 10.5, CENTER_Y + 15, SW_1_COLOR),
		(CENTER_X + 14.0, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X + 17.5, CENTER_Y + 15, SW_1_COLOR),
		(CENTER_X + 21, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X - 3.5, CENTER_Y + 15, SW_1_COLOR),
		(CENTER_X - 7.0, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X - 10.5, CENTER_Y + 15, SW_1_COLOR),
		(CENTER_X - 14.0, CENTER_Y + 12, SW_1_COLOR),
		(CENTER_X - 17.5, CENTER_Y + 15, SW_1_COLOR),

		# Center point
		(CENTER_X, CENTER_Y, SW_2_COLOR),

		# Perimeter points (calculated via 2*pi*i/11)
		(CENTER_X + 4.0, CENTER_Y + 0.0, SW_2_COLOR),                  # 0°
		(CENTER_X + 3.37, CENTER_Y + 2.16, SW_2_COLOR),               # 32.7°
		(CENTER_X + 1.66, CENTER_Y + 3.64, SW_2_COLOR),               # 65.4°
		(CENTER_X - 0.57, CENTER_Y + 3.96, SW_2_COLOR),               # 98.2°
		(CENTER_X - 2.62, CENTER_Y + 3.02, SW_2_COLOR),               # 130.9°
		(CENTER_X - 3.84, CENTER_Y + 1.13, SW_2_COLOR),               # 163.6°
		(CENTER_X - 3.84, CENTER_Y - 1.13, SW_2_COLOR),               # 196.4°
		(CENTER_X - 2.62, CENTER_Y - 3.02, SW_2_COLOR),               # 229.1°
		(CENTER_X - 0.57, CENTER_Y - 3.96, SW_2_COLOR),               # 261.8°
		(CENTER_X + 1.66, CENTER_Y - 3.64, SW_2_COLOR),               # 294.5°
		(CENTER_X + 3.37, CENTER_Y - 2.16, SW_2_COLOR),               # 327.3°
	]
	
	generate_svg(markers=markers_to_draw)
	print("grid.svg has been generated!")

if __name__ == "__main__":
	main()