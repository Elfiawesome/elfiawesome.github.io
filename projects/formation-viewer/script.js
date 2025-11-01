document.addEventListener('DOMContentLoaded', () => {
	// --- Constants from Python Script ---
	const TILE_SIZE = 32;
	const NUM_OF_CHUNK_X = 3;
	const NUM_OF_CHUNK_Y = 3;
	const CHUNK_SIZE = 20;
	const CHUNK_COLOR = "#a89ea9";
	const CHUNK_COLOR_ALT = "#8e98a5";
	const CHUNK_BORDER_COLOR = "#cececf";

	const SVG_NS = "http://www.w3.org/2000/svg";

	// --- DOM Element References ---
	const controls = document.querySelectorAll('#controls input, #controls select');
	const svgOutputContainer = document.getElementById('svg-output');
	const downloadBtn = document.getElementById('download-btn');

	// --- NEW: Mobile control references ---
	const body = document.body;
	const toggleBtn = document.getElementById('toggle-controls-btn');
	const closeBtn = document.getElementById('close-controls-btn');
	const overlay = document.getElementById('overlay');

	// --- Helper functions to create SVG elements ---
	const createElement = (tag, attributes) => {
		const el = document.createElementNS(SVG_NS, tag);
		for (const key in attributes) {
			el.setAttribute(key, attributes[key]);
		}
		return el;
	};

	const addCell = (root, x, y, size, fill) => {
		const cell = createElement("rect", {
			x: x, y: y, width: size, height: size,
			transform: "matrix(1, 0, 0, 1, 0, 0)",
			fill: fill, "fill-opacity": "1",
			stroke: "#000000", "stroke-width": "1",
			"stroke-dasharray": "1 2", opacity: "1",
			id: `Rectangle_${x}_${y}`
		});
		root.appendChild(cell);
	};

	const addMarker = (root, x, y, size, fill, strokeWidth = 4, label = null) => {
		const markerGroup = createElement("g", { id: `Marker_${x}_${y}` });
		markerGroup.appendChild(createElement("line", {
			x1: x - size / 2, y1: y - size / 2,
			x2: x + size / 2, y2: y + size / 2,
			stroke: fill, "stroke-width": strokeWidth
		}));
		markerGroup.appendChild(createElement("line", {
			x1: x + size / 2, y1: y - size / 2,
			x2: x - size / 2, y2: y + size / 2,
			stroke: fill, "stroke-width": strokeWidth
		}));
		if (label) {
			const text = createElement("text", {
				x: x, y: y, fill: "#000000",
				"font-family": "sans-serif", "font-size": "10",
				"text-anchor": "middle", "dominant-baseline": "middle"
			});
			text.textContent = label;
			markerGroup.appendChild(text);
		}
		root.appendChild(markerGroup);
	};

	// --- Formation Logic (Translated from Python) ---
	const getMarkerSilentWave = ({ midPoint, gap, totalMen, color }) => {
		const markers = [];
		for (let i = 0; i < totalMen; i++) {
			const _x = midPoint.x - (totalMen - 1) * gap / 2 + i * gap;
			const _y = midPoint.y;
			markers.push({ x: _x, y: _y, color });
		}
		return markers;
	};

	const getMarkerSaturn = ({ midPoint, saturnThrowGap, gap, totalMen, color }) => {
		const markers = [];
		let _y_offset = 0;
		for (let i = 0; i < totalMen; i++) {
			let _x = midPoint.x;
			if (i % 2 === 0) {
				_y_offset -= gap;
				_x -= saturnThrowGap / 2;
			} else {
				_x += saturnThrowGap / 2;
			}
			const _y = midPoint.y + _y_offset;
			markers.push({ x: _x, y: _y, color });
		}
		return markers;
	};

	const getMarkerFormation = ({ midPoint, formationPattern, gapMultiplier, color, centerFormation }) => {
		if (!formationPattern || formationPattern.length === 0) return [];

		const markers = [];
		let offsetX = 0, offsetY = 0;

		if (centerFormation) {
			const allX = formationPattern.map(p => p.x);
			const allY = formationPattern.map(p => p.y);
			const minX = Math.min(...allX);
			const maxX = Math.max(...allX);
			const minY = Math.min(...allY);
			const maxY = Math.max(...allY);

			const patternCenterX = (minX + maxX) / 2.0;
			const patternCenterY = (minY + maxY) / 2.0;

			offsetX = -patternCenterX;
			offsetY = -patternCenterY;
		}

		formationPattern.forEach(relativePos => {
			const _x = midPoint.x + (relativePos.x + offsetX) * gapMultiplier;
			const _y = midPoint.y + (relativePos.y + offsetY) * gapMultiplier;
			markers.push({ x: _x, y: _y, color });
		});

		return markers;
	};

	// --- Pre-defined Patterns ---
	const formationPattern1 = [
		{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 2, y: 0 }, { x: 3, y: 0 },
		{ x: 0, y: -1 }, { x: 1, y: -1 }, { x: 2, y: -1 }, { x: 3, y: -1 },
		{ x: 0, y: -2 }, { x: 1, y: -2 }, { x: 2, y: -2 }, { x: 3, y: -2 }
	];

	const createFormationPattern2 = (innerSpacing = 1, outerSpacing = 2) => [
		{ x: 0, y: -outerSpacing * 2 }, { x: outerSpacing, y: -outerSpacing },
		{ x: outerSpacing * 2, y: 0 }, { x: outerSpacing, y: outerSpacing },
		{ x: 0, y: outerSpacing * 2 }, { x: -outerSpacing, y: outerSpacing },
		{ x: -outerSpacing * 2, y: 0 }, { x: -outerSpacing, y: -outerSpacing },
		{ x: -innerSpacing, y: 0 }, { x: innerSpacing, y: 0 },
		{ x: 0, y: -innerSpacing }, { x: 0, y: innerSpacing }
	];

	const formationPattern3 = [
		{ x: 0, y: 0 },
		{ x: -1, y: -1 }, { x: 1, y: -1 },
		{ x: -2, y: -2 }, { x: 0, y: -2 }, { x: 2, y: -2 },
		{ x: -1, y: -3 }, { x: 1, y: -3 }, { x: -3, y: -3 }, { x: 3, y: -3 },
		{ x: -2, y: -4 }, { x: 2, y: -4 }
	];


	// --- Main SVG Generation Function ---
	const generateSVG = (markers = []) => {
		const totalWidth = CHUNK_SIZE * TILE_SIZE * NUM_OF_CHUNK_X;
		const totalHeight = CHUNK_SIZE * TILE_SIZE * NUM_OF_CHUNK_Y;

		const root = createElement("svg", {
			version: "1.1",
			viewBox: `0 0 ${totalWidth} ${totalHeight}`,
			xmlns: SVG_NS
		});

		const gridGroup = createElement("g", { id: "Grid" });

		for (let chunkX = 0; chunkX < NUM_OF_CHUNK_X; chunkX++) {
			for (let chunkY = 0; chunkY < NUM_OF_CHUNK_Y; chunkY++) {
				for (let localX = 0; localX < CHUNK_SIZE; localX++) {
					for (let localY = 0; localY < CHUNK_SIZE; localY++) {
						const x = (chunkX * CHUNK_SIZE + localX) * TILE_SIZE;
						const y = (chunkY * CHUNK_SIZE + localY) * TILE_SIZE;

						const isBorder = (localX === 0 || localX === CHUNK_SIZE - 1) ||
							(localY === 0 || localY === CHUNK_SIZE - 1);

						if (isBorder) {
							addCell(gridGroup, x, y, TILE_SIZE, CHUNK_BORDER_COLOR);
						} else {
							addCell(gridGroup, x, y, TILE_SIZE, chunkX === 2 ? CHUNK_COLOR_ALT : CHUNK_COLOR);
						}
					}
				}
			}
		}
		root.appendChild(gridGroup);

		markers.forEach(marker => {
			const pixelX = marker.x * TILE_SIZE;
			const pixelY = marker.y * TILE_SIZE;
			addMarker(root, pixelX, pixelY, TILE_SIZE * 3 / 4, marker.color);
		});

		return root;
	};

	// --- Update Function and Event Handlers ---
	const updateSVG = () => {
		let markersToDraw = [];

		// Collect markers from all active formations
		if (document.getElementById('f1-visible').checked) {
			markersToDraw.push(...getMarkerFormation({
				midPoint: { x: +document.getElementById('f1-midX').value, y: +document.getElementById('f1-midY').value },
				formationPattern: formationPattern1,
				gapMultiplier: +document.getElementById('f1-gap').value,
				color: document.getElementById('f1-color').value,
				centerFormation: document.getElementById('f1-center').checked
			}));
		}

		if (document.getElementById('f2-visible').checked) {
			markersToDraw.push(...getMarkerFormation({
				midPoint: { x: +document.getElementById('f2-midX').value, y: +document.getElementById('f2-midY').value },
				formationPattern: createFormationPattern2(
					+document.getElementById('f2-inner-gap').value,
					+document.getElementById('f2-outer-gap').value
				),
				gapMultiplier: +document.getElementById('f2-gap-mult').value,
				color: document.getElementById('f2-color').value,
				centerFormation: document.getElementById('f2-center').checked
			}));
		}

		if (document.getElementById('f3-visible').checked) {
			markersToDraw.push(...getMarkerFormation({
				midPoint: { x: +document.getElementById('f3-midX').value, y: +document.getElementById('f3-midY').value },
				formationPattern: formationPattern3,
				gapMultiplier: +document.getElementById('f3-gap').value,
				color: document.getElementById('f3-color').value,
				centerFormation: document.getElementById('f3-center').checked
			}));
		}

		if (document.getElementById('sw-visible').checked) {
			markersToDraw.push(...getMarkerSilentWave({
				midPoint: { x: +document.getElementById('sw-midX').value, y: +document.getElementById('sw-midY').value },
				gap: +document.getElementById('sw-gap').value,
				totalMen: +document.getElementById('sw-totalMen').value,
				color: document.getElementById('sw-color').value
			}));
		}

		if (document.getElementById('sat-visible').checked) {
			markersToDraw.push(...getMarkerSaturn({
				midPoint: { x: +document.getElementById('sat-midX').value, y: +document.getElementById('sat-midY').value },
				saturnThrowGap: +document.getElementById('sat-throw-gap').value,
				gap: +document.getElementById('sat-gap').value,
				totalMen: +document.getElementById('sat-totalMen').value,
				color: document.getElementById('sat-color').value
			}));
		}

		const svgElement = generateSVG(markersToDraw);
		svgOutputContainer.innerHTML = '';
		svgOutputContainer.appendChild(svgElement);
	};

	// Attach event listeners to all controls
	controls.forEach(control => {
		control.addEventListener('input', updateSVG);
	});

	// Download button functionality
	downloadBtn.addEventListener('click', () => {
		const svgData = new XMLSerializer().serializeToString(svgOutputContainer.querySelector('svg'));
		const blob = new Blob([`<?xml version="1.0" standalone="no"?>\r\n` + svgData], { type: 'image/svg+xml;charset=utf-8' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = 'formation.svg';
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	});

	// --- NEW: Mobile controls logic ---
	const showControls = () => body.classList.add('controls-visible');
	const hideControls = () => body.classList.remove('controls-visible');

	toggleBtn.addEventListener('click', showControls);
	closeBtn.addEventListener('click', hideControls);
	overlay.addEventListener('click', hideControls);

	// Initial render
	updateSVG();
});