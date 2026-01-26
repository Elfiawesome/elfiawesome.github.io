"""
Static Site Builder
Usage:
	python build.py [--data DATA_FILE] [--output OUTPUT_FILE]

Options:
	--data	  Path to the JSON data file (default: data.json)
	--output	Path to the output HTML file (default: index.html)
"""

import json
import argparse
from pathlib import Path
from typing import Any


class SiteBuilder:
	"""Main site builder class that generates HTML from JSON data."""

	def __init__(self, data: dict[str, Any]):
		self.data = data
		self.colors = data.get("branding", {}).get("colors", {})

	def build(self) -> str:
		"""Build the complete HTML document."""
		return f"""<!DOCTYPE html>
<html lang="en">
<head>
{self._build_head()}
</head>
<body>
	<!-- Gradient line -->
	<div class="gradient-line"></div>

	<!-- Grid background -->
	<div class="grid-bg"></div>

	<!-- Floating shapes -->
	<div class="shape shape-1"></div>
	<div class="shape shape-2"></div>
	<div class="shape shape-3"></div>

	<!-- Navigation -->
{self._build_navigation()}

	<!-- Mobile Menu -->
{self._build_mobile_menu()}

	<div class="content">
		<!-- Hero -->
{self._build_hero()}

		<!-- About -->
{self._build_about()}

		<!-- Projects -->
{self._build_projects()}

		<!-- Contact -->
{self._build_contact()}
	</div>

	<!-- Footer -->
{self._build_footer()}

{self._build_scripts()}
</body>
</html>"""

	def _build_head(self) -> str:
		"""Build the <head> section."""
		meta = self.data.get("meta", {})
		return f"""	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{meta.get("title", "Portfolio")}</title>
	<meta name="description" content="{meta.get("description", "")}">
	<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
	<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
	<style>
{self._build_styles()}
	</style>"""

	def _build_styles(self) -> str:
		"""Build the CSS styles."""
		primary = self.colors.get("primary", "#6366f1")
		secondary = self.colors.get("secondary", "#ec4899")
		success = self.colors.get("success", "#10b981")
		
		return f"""		* {{
			margin: 0;
			padding: 0;
			box-sizing: border-box;
		}}

		html {{
			scroll-behavior: smooth;
		}}

		body {{
			font-family: 'Inter', sans-serif;
			background: #0a0a0a;
			color: #a3a3a3;
			line-height: 1.6;
			overflow-x: hidden;
		}}

		::selection {{
			background: {primary};
			color: #fff;
		}}

		::-webkit-scrollbar {{
			width: 6px;
		}}
		::-webkit-scrollbar-track {{
			background: #0a0a0a;
		}}
		::-webkit-scrollbar-thumb {{
			background: #262626;
		}}

		.gradient-line {{
			position: fixed;
			top: 0;
			left: 0;
			right: 0;
			height: 2px;
			background: linear-gradient(90deg, {primary}, {secondary}, {primary});
			background-size: 200% 100%;
			animation: gradientMove 3s linear infinite;
			z-index: 200;
		}}

		@keyframes gradientMove {{
			0% {{ background-position: 0% 0%; }}
			100% {{ background-position: 200% 0%; }}
		}}

		.grid-bg {{
			position: fixed;
			inset: 0;
			background-image: 
				linear-gradient(rgba(99, 102, 241, 0.03) 1px, transparent 1px),
				linear-gradient(90deg, rgba(99, 102, 241, 0.03) 1px, transparent 1px);
			background-size: 60px 60px;
			pointer-events: none;
			z-index: 0;
		}}

		.shape {{
			position: fixed;
			pointer-events: none;
			z-index: 1;
			opacity: 0.5;
		}}

		.shape-1 {{
			top: 15%;
			right: 10%;
			width: 300px;
			height: 300px;
			border: 1px solid rgba(99, 102, 241, 0.2);
			transform: rotate(45deg);
			animation: float 20s ease-in-out infinite;
		}}

		.shape-2 {{
			bottom: 20%;
			left: 5%;
			width: 200px;
			height: 200px;
			border: 1px solid rgba(236, 72, 153, 0.15);
			animation: float 15s ease-in-out infinite reverse;
		}}

		.shape-3 {{
			top: 60%;
			right: 15%;
			width: 100px;
			height: 100px;
			background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), transparent);
			animation: float 25s ease-in-out infinite;
		}}

		@keyframes float {{
			0%, 100% {{ transform: rotate(45deg) translate(0, 0); }}
			25% {{ transform: rotate(45deg) translate(20px, -20px); }}
			50% {{ transform: rotate(45deg) translate(0, -30px); }}
			75% {{ transform: rotate(45deg) translate(-20px, -10px); }}
		}}

		.nav {{
			position: fixed;
			top: 2px;
			left: 0;
			right: 0;
			z-index: 100;
			padding: 20px 32px;
			transition: all 0.3s ease;
		}}

		.nav.scrolled {{
			background: rgba(10, 10, 10, 0.9);
			backdrop-filter: blur(20px);
			border-bottom: 1px solid #1a1a1a;
		}}

		.nav-container {{
			max-width: 1400px;
			margin: 0 auto;
			display: flex;
			justify-content: space-between;
			align-items: center;
		}}

		.logo {{
			font-family: 'Space Mono', monospace;
			font-size: 18px;
			font-weight: 700;
			color: #fafafa;
			text-decoration: none;
			letter-spacing: -0.5px;
		}}

		.logo span {{
			color: {primary};
		}}

		.nav-links {{
			display: flex;
			gap: 40px;
		}}

		.nav-link {{
			color: #525252;
			text-decoration: none;
			font-size: 13px;
			font-weight: 500;
			text-transform: uppercase;
			letter-spacing: 1px;
			transition: color 0.3s;
			position: relative;
		}}

		.nav-link::after {{
			content: '';
			position: absolute;
			bottom: -4px;
			left: 0;
			width: 0;
			height: 1px;
			background: {primary};
			transition: width 0.3s;
		}}

		.nav-link:hover {{
			color: #fafafa;
		}}

		.nav-link:hover::after {{
			width: 100%;
		}}

		.menu-btn {{
			display: none;
			background: none;
			border: none;
			color: #fafafa;
			font-size: 24px;
			cursor: pointer;
		}}

		.mobile-menu {{
			display: none;
			position: fixed;
			inset: 0;
			background: #0a0a0a;
			z-index: 150;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			gap: 32px;
		}}

		.mobile-menu.active {{
			display: flex;
		}}

		.mobile-menu a {{
			font-size: 32px;
			color: #525252;
			text-decoration: none;
			font-weight: 600;
			transition: all 0.3s;
		}}

		.mobile-menu a:hover {{
			color: #fafafa;
			transform: translateX(10px);
		}}

		.close-btn {{
			position: absolute;
			top: 24px;
			right: 32px;
			background: none;
			border: none;
			color: #fafafa;
			font-size: 28px;
			cursor: pointer;
		}}

		.content {{
			position: relative;
			z-index: 10;
		}}

		.section {{
			max-width: 1400px;
			margin: 0 auto;
			padding: 140px 32px;
		}}

		.hero {{
			min-height: 100vh;
			display: flex;
			align-items: center;
			padding-top: 80px;
		}}

		.hero-content {{
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 80px;
			align-items: center;
			width: 100%;
		}}

		.hero-left {{
			position: relative;
		}}

		.hero-label {{
			font-family: 'Space Mono', monospace;
			font-size: 12px;
			color: {primary};
			text-transform: uppercase;
			letter-spacing: 3px;
			margin-bottom: 24px;
			display: flex;
			align-items: center;
			gap: 12px;
		}}

		.hero-label::before {{
			content: '';
			width: 40px;
			height: 1px;
			background: {primary};
		}}

		.hero h1 {{
			font-size: clamp(48px, 7vw, 80px);
			font-weight: 700;
			color: #fafafa;
			line-height: 1;
			margin-bottom: 32px;
			letter-spacing: -3px;
		}}

		.hero h1 .gradient {{
			background: linear-gradient(135deg, {primary}, {secondary});
			-webkit-background-clip: text;
			-webkit-text-fill-color: transparent;
			background-clip: text;
		}}

		.hero-text {{
			font-size: 18px;
			color: #525252;
			max-width: 450px;
			line-height: 1.8;
			margin-bottom: 48px;
		}}

		.hero-buttons {{
			display: flex;
			gap: 16px;
		}}

		.btn {{
			display: inline-flex;
			align-items: center;
			gap: 10px;
			padding: 16px 32px;
			font-size: 13px;
			font-weight: 600;
			text-decoration: none;
			text-transform: uppercase;
			letter-spacing: 1px;
			transition: all 0.3s;
			cursor: pointer;
			border: none;
		}}

		.btn-primary {{
			background: #fafafa;
			color: #0a0a0a;
			position: relative;
			overflow: hidden;
		}}

		.btn-primary::before {{
			content: '';
			position: absolute;
			inset: 0;
			background: linear-gradient(135deg, {primary}, {secondary});
			opacity: 0;
			transition: opacity 0.3s;
		}}

		.btn-primary:hover {{
			color: #fafafa;
		}}

		.btn-primary:hover::before {{
			opacity: 1;
		}}

		.btn-primary span {{
			position: relative;
			z-index: 1;
		}}

		.btn-primary .iconify {{
			position: relative;
			z-index: 1;
		}}

		.btn-secondary {{
			background: transparent;
			color: #fafafa;
			border: 1px solid #262626;
		}}

		.btn-secondary:hover {{
			background: #fafafa;
			color: #0a0a0a;
			border-color: #fafafa;
		}}

		.hero-visual {{
			position: relative;
			height: 500px;
			display: flex;
			align-items: center;
			justify-content: center;
		}}

		.visual-box {{
			position: absolute;
			border: 1px solid #1a1a1a;
			transition: all 0.5s;
		}}

		.visual-box-1 {{
			width: 300px;
			height: 300px;
			animation: rotateBox 30s linear infinite;
		}}

		.visual-box-2 {{
			width: 200px;
			height: 200px;
			border-color: {primary};
			opacity: 0.3;
			animation: rotateBox 20s linear infinite reverse;
		}}

		.visual-box-3 {{
			width: 100px;
			height: 100px;
			background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
			animation: rotateBox 15s linear infinite;
		}}

		@keyframes rotateBox {{
			from {{ transform: rotate(0deg); }}
			to {{ transform: rotate(360deg); }}
		}}

		.visual-text {{
			font-family: 'Space Mono', monospace;
			font-size: 14px;
			color: #262626;
			position: relative;
			z-index: 2;
		}}

		.section-header {{
			margin-bottom: 64px;
			display: flex;
			align-items: flex-end;
			justify-content: space-between;
			gap: 40px;
		}}

		.section-label {{
			font-family: 'Space Mono', monospace;
			font-size: 12px;
			color: {primary};
			text-transform: uppercase;
			letter-spacing: 3px;
			margin-bottom: 16px;
			display: flex;
			align-items: center;
			gap: 12px;
		}}

		.section-label::before {{
			content: '';
			width: 40px;
			height: 1px;
			background: {primary};
		}}

		.section-title {{
			font-size: clamp(36px, 5vw, 56px);
			font-weight: 700;
			color: #fafafa;
			letter-spacing: -2px;
			line-height: 1.1;
		}}

		.section-count {{
			font-family: 'Space Mono', monospace;
			font-size: 72px;
			font-weight: 700;
			color: #1a1a1a;
			line-height: 1;
		}}

		.about-grid {{
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 100px;
		}}

		.about-text {{
			font-size: 17px;
			line-height: 1.9;
			color: #737373;
		}}

		.about-text p {{
			margin-bottom: 24px;
		}}

		.about-text strong {{
			color: #fafafa;
			font-weight: 500;
		}}

		.about-visual {{
			position: relative;
		}}

		.stats-grid {{
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 2px;
			background: #1a1a1a;
		}}

		.stat-card {{
			background: #0a0a0a;
			padding: 40px;
			transition: all 0.3s;
			position: relative;
			overflow: hidden;
		}}

		.stat-card::before {{
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 0;
			height: 2px;
			background: linear-gradient(90deg, {primary}, {secondary});
			transition: width 0.3s;
		}}

		.stat-card:hover::before {{
			width: 100%;
		}}

		.stat-card:hover {{
			background: #111;
		}}

		.stat-number {{
			font-size: 48px;
			font-weight: 700;
			color: #fafafa;
			margin-bottom: 8px;
			letter-spacing: -2px;
		}}

		.stat-label {{
			font-size: 13px;
			color: #525252;
			text-transform: uppercase;
			letter-spacing: 1px;
		}}

		.projects-grid {{
			display: grid;
			gap: 2px;
			background: #1a1a1a;
		}}

		.project-card {{
			display: grid;
			grid-template-columns: 80px 1fr auto;
			align-items: center;
			gap: 40px;
			padding: 40px;
			background: #0a0a0a;
			text-decoration: none;
			transition: all 0.3s;
			position: relative;
			overflow: hidden;
		}}

		.project-card::before {{
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 3px;
			height: 0;
			background: linear-gradient(180deg, {primary}, {secondary});
			transition: height 0.3s;
		}}

		.project-card:hover::before {{
			height: 100%;
		}}

		.project-card:hover {{
			background: #111;
		}}

		.project-card:hover .project-arrow {{
			transform: translateX(8px);
			color: {primary};
		}}

		.project-card:hover .project-number {{
			color: {primary};
		}}

		.project-number {{
			font-family: 'Space Mono', monospace;
			font-size: 14px;
			color: #262626;
			transition: color 0.3s;
		}}

		.project-content {{
			display: grid;
			grid-template-columns: 1fr auto;
			align-items: center;
			gap: 40px;
		}}

		.project-title {{
			font-size: 22px;
			font-weight: 600;
			color: #fafafa;
			margin-bottom: 8px;
			letter-spacing: -0.5px;
		}}

		.project-desc {{
			font-size: 14px;
			color: #525252;
		}}

		.project-tags {{
			display: flex;
			gap: 8px;
		}}

		.project-tag {{
			font-family: 'Space Mono', monospace;
			font-size: 11px;
			padding: 8px 16px;
			background: #1a1a1a;
			color: #525252;
			text-transform: uppercase;
			letter-spacing: 1px;
		}}

		.project-tag.wiki {{
			color: {primary};
			background: rgba(99, 102, 241, 0.1);
		}}

		.project-tag.game {{
			color: {secondary};
			background: rgba(236, 72, 153, 0.1);
		}}

		.project-tag.tool {{
			color: {success};
			background: rgba(16, 185, 129, 0.1);
		}}

		.project-arrow {{
			font-size: 24px;
			color: #262626;
			transition: all 0.3s;
		}}

		.contact-grid {{
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 100px;
		}}

		.contact-text {{
			font-size: 17px;
			color: #525252;
			margin-top: 24px;
			line-height: 1.8;
		}}

		.contact-email {{
			font-size: clamp(24px, 3vw, 36px);
			color: #fafafa;
			font-weight: 600;
			margin-top: 40px;
			text-decoration: none;
			display: inline-block;
			position: relative;
			letter-spacing: -1px;
		}}

		.contact-email::after {{
			content: '';
			position: absolute;
			bottom: -4px;
			left: 0;
			width: 100%;
			height: 2px;
			background: linear-gradient(90deg, {primary}, {secondary});
		}}

		.social-grid {{
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 2px;
			background: #1a1a1a;
		}}

		.social-link {{
			display: flex;
			align-items: center;
			gap: 16px;
			padding: 32px;
			background: #0a0a0a;
			text-decoration: none;
			color: #525252;
			font-size: 14px;
			font-weight: 500;
			transition: all 0.3s;
			position: relative;
			overflow: hidden;
		}}

		.social-link::before {{
			content: '';
			position: absolute;
			bottom: 0;
			left: 0;
			width: 0;
			height: 2px;
			background: linear-gradient(90deg, {primary}, {secondary});
			transition: width 0.3s;
		}}

		.social-link:hover {{
			background: #111;
			color: #fafafa;
		}}

		.social-link:hover::before {{
			width: 100%;
		}}

		.social-link:hover .iconify {{
			color: {primary};
		}}

		.social-link .iconify {{
			font-size: 24px;
			transition: color 0.3s;
		}}

		.footer {{
			max-width: 1400px;
			margin: 0 auto;
			padding: 60px 32px;
			border-top: 1px solid #1a1a1a;
			display: flex;
			justify-content: space-between;
			align-items: center;
			flex-wrap: wrap;
			gap: 20px;
		}}

		.footer-text {{
			font-size: 13px;
			color: #525252;
		}}

		.footer-links {{
			display: flex;
			gap: 24px;
		}}

		.footer-link {{
			color: #525252;
			font-size: 20px;
			transition: all 0.3s;
		}}

		.footer-link:hover {{
			color: {primary};
		}}

		.reveal {{
			opacity: 0;
			transform: translateY(40px);
			transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
		}}

		.reveal.visible {{
			opacity: 1;
			transform: translateY(0);
		}}

		.reveal-delay-1 {{ transition-delay: 0.1s; }}
		.reveal-delay-2 {{ transition-delay: 0.2s; }}
		.reveal-delay-3 {{ transition-delay: 0.3s; }}
		.reveal-delay-4 {{ transition-delay: 0.4s; }}
		.reveal-delay-5 {{ transition-delay: 0.5s; }}

		@media (max-width: 1024px) {{
			.hero-content {{
				grid-template-columns: 1fr;
				gap: 60px;
			}}

			.hero-visual {{
				height: 300px;
			}}

			.about-grid,
			.contact-grid {{
				grid-template-columns: 1fr;
				gap: 60px;
			}}
		}}

		@media (max-width: 768px) {{
			.nav-links {{
				display: none;
			}}

			.menu-btn {{
				display: block;
			}}

			.section {{
				padding: 100px 24px;
			}}

			.hero {{
				padding-top: 120px;
			}}

			.section-header {{
				flex-direction: column;
				align-items: flex-start;
			}}

			.section-count {{
				display: none;
			}}

			.project-card {{
				grid-template-columns: 1fr;
				gap: 20px;
			}}

			.project-content {{
				grid-template-columns: 1fr;
				gap: 16px;
			}}

			.project-number {{
				display: none;
			}}

			.stats-grid {{
				grid-template-columns: 1fr 1fr;
			}}

			.stat-card {{
				padding: 24px;
			}}

			.stat-number {{
				font-size: 36px;
			}}

			.social-grid {{
				grid-template-columns: 1fr;
			}}

			.hero-buttons {{
				flex-direction: column;
			}}

			.btn {{
				justify-content: center;
			}}

			.hero-visual {{
				display: none;
			}}
		}}"""

	def _build_navigation(self) -> str:
		"""Build the navigation section."""
		logo = self.data.get("branding", {}).get("logo", {})
		nav_items = self.data.get("navigation", [])
		
		nav_links = "\n				".join([
			f'<a href="{item["href"]}" class="nav-link">{item["label"]}</a>'
			for item in nav_items
		])
		
		return f"""	<nav class="nav" id="nav">
		<div class="nav-container">
			<a href="#" class="logo">{logo.get("text", "")}<span>{logo.get("accent", "")}</span>{logo.get("suffix", "")}</a>
			<div class="nav-links">
				{nav_links}
			</div>
			<button class="menu-btn" id="menuBtn">
				<span class="iconify" data-icon="mdi:menu"></span>
			</button>
		</div>
	</nav>"""

	def _build_mobile_menu(self) -> str:
		"""Build the mobile menu."""
		nav_items = self.data.get("navigation", [])
		
		menu_links = "\n		".join([
			f'<a href="{item["href"]}">{item["label"]}</a>'
			for item in nav_items
		])
		
		return f"""	<div class="mobile-menu" id="mobileMenu">
		<button class="close-btn" id="closeBtn">
			<span class="iconify" data-icon="mdi:close"></span>
		</button>
		{menu_links}
	</div>"""

	def _build_hero(self) -> str:
		"""Build the hero section."""
		hero = self.data.get("hero", {})
		title = hero.get("title", {})
		
		buttons_html = ""
		for btn in hero.get("buttons", []):
			target = ' target="_blank"' if btn.get("external") else ""
			btn_class = "btn-primary" if btn.get("type") == "primary" else "btn-secondary"
			icon_html = f'<span class="iconify" data-icon="{btn["icon"]}"></span>' if btn.get("icon") else ""
			
			if btn.get("type") == "primary":
				buttons_html += f"""
						<a href="{btn["href"]}"{target} class="btn {btn_class}">
							<span>{btn["text"]}</span>
							{icon_html}
						</a>"""
			else:
				buttons_html += f"""
						<a href="{btn["href"]}"{target} class="btn {btn_class}">
							{icon_html}
							{btn["text"]}
						</a>"""
		
		return f"""		<section class="section hero">
			<div class="hero-content">
				<div class="hero-left">
					<div class="hero-label reveal">{hero.get("label", "")}</div>
					<h1 class="reveal reveal-delay-1">
						{title.get("prefix", "")}<span class="gradient">{title.get("highlight", "")}</span>
					</h1>
					<p class="hero-text reveal reveal-delay-2">
						{hero.get("description", "")}
					</p>
					<div class="hero-buttons reveal reveal-delay-3">{buttons_html}
					</div>
				</div>
				<div class="hero-visual reveal reveal-delay-4">
					<div class="visual-box visual-box-1"></div>
					<div class="visual-box visual-box-2"></div>
					<div class="visual-box visual-box-3"></div>
					<div class="visual-text">&lt;/&gt;</div>
				</div>
			</div>
		</section>"""

	def _build_about(self) -> str:
		"""Build the about section."""
		about = self.data.get("about", {})
		
		paragraphs_html = "\n					".join([
			f"<p>{p}</p>" for p in about.get("paragraphs", [])
		])
		
		stats_html = "\n						".join([
			f"""<div class="stat-card">
							<div class="stat-number">{stat["value"]}</div>
							<div class="stat-label">{stat["label"]}</div>
						</div>"""
			for stat in about.get("stats", [])
		])
		
		return f"""		<section class="section" id="about">
			<div class="section-header reveal">
				<div>
					<div class="section-label">{about.get("label", "About")}</div>
					<h2 class="section-title">{about.get("title", "")}</h2>
				</div>
				<div class="section-count">{about.get("section_number", "01")}</div>
			</div>

			<div class="about-grid">
				<div class="about-text reveal">
					{paragraphs_html}
				</div>
				<div class="about-visual reveal reveal-delay-2">
					<div class="stats-grid">
						{stats_html}
					</div>
				</div>
			</div>
		</section>"""

	def _build_projects(self) -> str:
		"""Build the projects section."""
		projects = self.data.get("projects", {})
		
		projects_html = ""
		for i, project in enumerate(projects.get("items", [])):
			delay_class = f" reveal-delay-{i}" if i > 0 else ""
			
			tags_html = " ".join([
				f'<span class="project-tag {tag}">{tag.upper()}</span>'
				for tag in project.get("tags", [])
			])
			
			projects_html += f"""
				<a href="{project["url"]}" class="project-card reveal{delay_class}">
					<div class="project-number">{project["id"]}</div>
					<div class="project-content">
						<div>
							<div class="project-title">{project["title"]}</div>
							<div class="project-desc">{project["description"]}</div>
						</div>
						<div class="project-tags">
							{tags_html}
						</div>
					</div>
					<span class="iconify project-arrow" data-icon="mdi:arrow-right"></span>
				</a>"""
		
		return f"""		<section class="section" id="projects">
			<div class="section-header reveal">
				<div>
					<div class="section-label">{projects.get("label", "Projects")}</div>
					<h2 class="section-title">{projects.get("title", "")}</h2>
				</div>
				<div class="section-count">{projects.get("section_number", "02")}</div>
			</div>

			<div class="projects-grid">{projects_html}
			</div>
		</section>"""

	def _build_contact(self) -> str:
		"""Build the contact section."""
		contact = self.data.get("contact", {})
		
		socials_html = "\n					".join([
			f"""<a href="{social["url"]}" target="_blank" class="social-link">
						<span class="iconify" data-icon="{social["icon"]}"></span>
						{social["platform"]}
					</a>"""
			for social in contact.get("socials", [])
		])
		
		return f"""		<section class="section" id="contact">
			<div class="contact-grid">
				<div class="reveal">
					<div class="section-label">{contact.get("label", "Contact")}</div>
					<h2 class="section-title">{contact.get("title", "")}</h2>
					<p class="contact-text">
						{contact.get("description", "")}
					</p>
					<a href="mailto:{contact.get("email", "")}" class="contact-email">{contact.get("email", "")}</a>
				</div>
				<div class="social-grid reveal reveal-delay-2">
					{socials_html}
				</div>
			</div>
		</section>"""

	def _build_footer(self) -> str:
		"""Build the footer section."""
		footer = self.data.get("footer", {})
		
		socials_html = "\n			".join([
			f"""<a href="{social["url"]}" target="_blank" class="footer-link">
				<span class="iconify" data-icon="{social["icon"]}"></span>
			</a>"""
			for social in footer.get("socials", [])
		])
		
		return f"""	<footer class="footer">
		<p class="footer-text">&copy; {footer.get("copyright", "")}</p>
		<div class="footer-links">
			{socials_html}
		</div>
	</footer>"""

	def _build_scripts(self) -> str:
		"""Build the JavaScript section."""
		return """	<script>
		// Nav scroll effect
		const nav = document.getElementById('nav');
		window.addEventListener('scroll', () => {
			nav.classList.toggle('scrolled', window.scrollY > 50);
		});

		// Mobile menu
		const menuBtn = document.getElementById('menuBtn');
		const closeBtn = document.getElementById('closeBtn');
		const mobileMenu = document.getElementById('mobileMenu');

		menuBtn.addEventListener('click', () => {
			mobileMenu.classList.add('active');
			document.body.style.overflow = 'hidden';
		});

		closeBtn.addEventListener('click', () => {
			mobileMenu.classList.remove('active');
			document.body.style.overflow = '';
		});

		mobileMenu.querySelectorAll('a').forEach(link => {
			link.addEventListener('click', () => {
				mobileMenu.classList.remove('active');
				document.body.style.overflow = '';
			});
		});

		// Reveal on scroll
		const reveals = document.querySelectorAll('.reveal');
		const revealObserver = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					entry.target.classList.add('visible');
				}
			});
		}, { threshold: 0.1, rootMargin: '-50px' });

		reveals.forEach(el => revealObserver.observe(el));

		// Smooth scroll
		document.querySelectorAll('a[href^="#"]').forEach(anchor => {
			anchor.addEventListener('click', function(e) {
				e.preventDefault();
				const target = document.querySelector(this.getAttribute('href'));
				if (target) {
					target.scrollIntoView({ behavior: 'smooth', block: 'start' });
				}
			});
		});

		// Parallax effect on shapes
		document.addEventListener('mousemove', (e) => {
			const shapes = document.querySelectorAll('.shape');
			const x = e.clientX / window.innerWidth;
			const y = e.clientY / window.innerHeight;
			
			shapes.forEach((shape, i) => {
				const speed = (i + 1) * 20;
				shape.style.transform = `rotate(45deg) translate(${x * speed}px, ${y * speed}px)`;
			});
		});
	</script>"""


def load_data(file_path: str) -> dict[str, Any]:
	"""Load JSON data from file."""
	path = Path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"Data file not found: {file_path}")
	
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def save_html(content: str, file_path: str) -> None:
	"""Save HTML content to file."""
	path = Path(file_path)
	path.parent.mkdir(parents=True, exist_ok=True)
	
	with open(path, "w", encoding="utf-8") as f:
		f.write(content)


def main():
	"""Main entry point."""
	parser = argparse.ArgumentParser(
		description="Build a static website from JSON data",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
	python build.py
	python build.py --data my-data.json
	python build.py --data data.json --output dist/index.html
		"""
	)
	parser.add_argument(
		"--data",
		default="data.json",
		help="Path to the JSON data file (default: data.json)"
	)
	parser.add_argument(
		"--output",
		default="index.html",
		help="Path to the output HTML file (default: index.html)"
	)
	
	args = parser.parse_args()
	
	try:
		print(f"Loading data from: {args.data}")
		data = load_data(args.data)
		
		print("Building site...")
		builder = SiteBuilder(data)
		html = builder.build()
		
		print(f"Saving to: {args.output}")
		save_html(html, args.output)
		
		print("Build complete!")
		
	except FileNotFoundError as e:
		print(f"Error: {e}")
		return 1
	except json.JSONDecodeError as e:
		print(f"Error parsing JSON: {e}")
		return 1
	except Exception as e:
		print(f"Unexpected error: {e}")
		return 1
	
	return 0


if __name__ == "__main__":
	exit(main())
