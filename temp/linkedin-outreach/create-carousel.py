#!/usr/bin/env python3
"""
LinkedIn Carousel Generator
Creates beautiful carousel slides for the Monitoring vs Observability post.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
import sys

# Slide dimensions (portrait for better LinkedIn visibility)
WIDTH = 1080
HEIGHT = 1350

# Colors - NVIDIA brand theme (Green, Black, White)
COLORS = {
    "bg_top": (10, 10, 10),       # Near black
    "bg_bottom": (20, 25, 20),    # Slight green tint black
    "accent": (118, 185, 0),      # NVIDIA Green #76B900
    "accent_light": (150, 210, 50),  # Lighter NVIDIA green
    "text_primary": (255, 255, 255),  # Pure white
    "text_secondary": (180, 180, 180), # Light gray
    "highlight": (118, 185, 0),   # NVIDIA Green for highlights
    "accent_dark": (80, 130, 0),  # Darker green for depth
}


def create_gradient_background(width: int, height: int) -> Image.Image:
    """Create a smooth vertical gradient background."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(COLORS["bg_top"][0] * (1 - ratio) + COLORS["bg_bottom"][0] * ratio)
        g = int(COLORS["bg_top"][1] * (1 - ratio) + COLORS["bg_bottom"][1] * ratio)
        b = int(COLORS["bg_top"][2] * (1 - ratio) + COLORS["bg_bottom"][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def add_decorative_elements(img: Image.Image, variant: int = 0) -> Image.Image:
    """Add NVIDIA-inspired decorative elements to the background."""
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Glowing green orbs with multiple layers for glow effect
    orb_positions = [
        ((-150, -150), (350, 350)),   # Top left
        ((750, 950), (1250, 1450)),   # Bottom right
        ((850, -100), (1150, 200)),   # Top right
    ]
    
    # Create layered glow effect for orbs
    for i, (pos1, pos2) in enumerate(orb_positions):
        # Outer glow (very faint)
        expand = 80
        draw.ellipse(
            [(pos1[0]-expand, pos1[1]-expand), (pos2[0]+expand, pos2[1]+expand)], 
            fill=(118, 185, 0, 8)
        )
        # Middle glow
        expand = 40
        draw.ellipse(
            [(pos1[0]-expand, pos1[1]-expand), (pos2[0]+expand, pos2[1]+expand)], 
            fill=(118, 185, 0, 15)
        )
        # Inner core
        draw.ellipse([pos1, pos2], fill=(118, 185, 0, 25))
    
    # Add subtle grid lines (tech/matrix feel)
    grid_color = (118, 185, 0, 12)
    
    # Vertical lines
    for x in range(0, WIDTH, 120):
        if variant % 2 == 0:
            draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    
    # Horizontal lines  
    for y in range(0, HEIGHT, 120):
        if variant % 2 == 0:
            draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)
    
    # Add diagonal accent lines (dynamic feel)
    for offset in range(-500, 1500, 300):
        draw.line(
            [(offset, 0), (offset + 400, HEIGHT)], 
            fill=(118, 185, 0, 8), 
            width=2
        )
    
    # Corner accent - geometric shape
    corner_points = [(0, 0), (200, 0), (0, 200)]
    draw.polygon(corner_points, fill=(118, 185, 0, 20))
    
    # Bottom right corner accent
    corner_points_br = [(WIDTH, HEIGHT), (WIDTH-200, HEIGHT), (WIDTH, HEIGHT-200)]
    draw.polygon(corner_points_br, fill=(118, 185, 0, 15))
    
    # Add small floating particles/dots
    import random
    random.seed(42 + variant)  # Consistent but different per slide
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(2, 6)
        alpha = random.randint(20, 60)
        draw.ellipse([(x, y), (x+size, y+size)], fill=(118, 185, 0, alpha))
    
    return img


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get a font, falling back to default if custom fonts unavailable."""
    # Try common system fonts
    font_paths = [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/SF-Pro-Display-Bold.otf" if bold else "/Library/Fonts/SF-Pro-Display-Regular.otf",
        # Fallback
        "/System/Library/Fonts/SFNSDisplay.ttf",
    ]
    
    for path in font_paths:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    # Ultimate fallback
    return ImageFont.load_default()


def draw_text_centered(draw: ImageDraw.Draw, text: str, y: int, font: ImageFont.FreeTypeFont, 
                       color: tuple, width: int = WIDTH) -> int:
    """Draw centered text and return the new y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=color)
    return y + text_height


def draw_text_left(draw: ImageDraw.Draw, text: str, x: int, y: int, 
                   font: ImageFont.FreeTypeFont, color: tuple) -> int:
    """Draw left-aligned text and return the new y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_height = bbox[3] - bbox[1]
    draw.text((x, y), text, font=font, fill=color)
    return y + text_height


def create_slide_1() -> Image.Image:
    """Cover slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=1)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(72, bold=True)
    font_medium = get_font(42, bold=True)
    font_small = get_font(36)
    
    y = 350
    
    # Main title - NVIDIA green emphasis
    draw_text_centered(draw, "MONITORING", y, font_large, COLORS["text_primary"])
    y += 90
    draw_text_centered(draw, "vs", y, font_medium, COLORS["accent"])
    y += 70
    draw_text_centered(draw, "OBSERVABILITY", y, font_large, COLORS["accent"])
    
    y += 150
    
    # Subtitle
    draw_text_centered(draw, "What's the difference?", y, font_medium, COLORS["text_primary"])
    y += 70
    draw_text_centered(draw, "(And why it matters at 3 AM)", y, font_small, COLORS["text_secondary"])
    
    # Swipe indicator
    y = HEIGHT - 150
    draw_text_centered(draw, "Swipe →", y, font_medium, COLORS["accent"])
    
    return img


def create_slide_2() -> Image.Image:
    """Monitoring answers slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=2)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(56, bold=True)
    font_text = get_font(40)
    font_footer = get_font(36, bold=True)
    
    y = 200
    draw_text_centered(draw, "MONITORING answers:", y, font_title, COLORS["text_primary"])
    
    y = 400
    x = 100
    questions = [
        '"Is CPU above 80%?"',
        '"Did the health check pass?"',
        '"Is the service up?"',
    ]
    
    for q in questions:
        draw_text_left(draw, f"→  {q}", x, y, font_text, COLORS["text_secondary"])
        y += 100
    
    y = HEIGHT - 350
    draw_text_centered(draw, "Known questions.", y, font_footer, COLORS["accent"])
    y += 80
    draw_text_centered(draw, "Known answers.", y, font_footer, COLORS["accent"])
    
    return img


def create_slide_3() -> Image.Image:
    """Observability answers slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=3)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(56, bold=True)
    font_text = get_font(40)
    font_footer = get_font(36, bold=True)
    
    y = 200
    draw_text_centered(draw, "OBSERVABILITY answers:", y, font_title, COLORS["accent"])
    
    y = 400
    x = 100
    questions = [
        '"Why is checkout slow?"',
        '"Which service caused the failure?"',
        '"What\'s different about failing requests?"',
    ]
    
    for q in questions:
        draw_text_left(draw, f"→  {q}", x, y, font_text, COLORS["text_primary"])
        y += 100
    
    y = HEIGHT - 350
    draw_text_centered(draw, "Unknown questions.", y, font_footer, COLORS["accent"])
    y += 80
    draw_text_centered(draw, "Discovered answers.", y, font_footer, COLORS["accent"])
    
    return img


def create_slide_4() -> Image.Image:
    """Monitoring car dashboard analogy."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=4)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(48, bold=True)
    font_text = get_font(42)
    font_emphasis = get_font(38, bold=True)
    
    y = 200
    draw_text_centered(draw, "MONITORING is like", y, font_title, COLORS["text_secondary"])
    y += 80
    draw_text_centered(draw, "a car dashboard:", y, font_title, COLORS["text_primary"])
    
    y = 450
    x = 150
    items = ["Speed", "Fuel level", "Engine temperature"]
    
    for item in items:
        draw_text_left(draw, f"✓  {item}", x, y, font_text, COLORS["accent"])
        y += 90
    
    y = HEIGHT - 350
    draw_text_centered(draw, "You know SOMETHING is wrong.", y, font_emphasis, COLORS["text_secondary"])
    y += 80
    draw_text_centered(draw, "You don't know WHAT.", y, font_emphasis, COLORS["accent"])
    
    return img


def create_slide_5() -> Image.Image:
    """Observability diagnostic analogy."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=5)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(48, bold=True)
    font_text = get_font(42)
    font_emphasis = get_font(38, bold=True)
    
    y = 200
    draw_text_centered(draw, "OBSERVABILITY is like", y, font_title, COLORS["text_secondary"])
    y += 80
    draw_text_centered(draw, "a full diagnostic:", y, font_title, COLORS["accent"])
    
    y = 450
    x = 150
    items = ["Every component checked", "Error codes explained", "Root cause identified"]
    
    for item in items:
        draw_text_left(draw, f"✓  {item}", x, y, font_text, COLORS["accent"])
        y += 90
    
    y = HEIGHT - 300
    draw_text_centered(draw, "You know EXACTLY what's wrong.", y, font_emphasis, COLORS["accent"])
    
    return img


def create_slide_6() -> Image.Image:
    """Three pillars slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=6)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(56, bold=True)
    font_pillar = get_font(48, bold=True)
    font_desc = get_font(36)
    
    y = 200
    draw_text_centered(draw, "THE THREE PILLARS", y, font_title, COLORS["accent"])
    
    pillars = [
        ("📈  METRICS", "What's the pattern?", COLORS["text_primary"]),
        ("🔍  TRACES", "What's the journey?", COLORS["text_primary"]),
        ("📝  LOGS", "What's the detail?", COLORS["text_primary"]),
    ]
    
    y = 420
    for emoji_title, desc, color in pillars:
        draw_text_centered(draw, emoji_title, y, font_pillar, color)
        y += 70
        draw_text_centered(draw, desc, y, font_desc, COLORS["accent"])
        y += 130
    
    return img


def create_slide_7() -> Image.Image:
    """When you need observability slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=7)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(48, bold=True)
    font_text = get_font(38)
    
    y = 200
    draw_text_centered(draw, "WHEN YOU NEED", y, font_title, COLORS["text_secondary"])
    y += 80
    draw_text_centered(draw, "OBSERVABILITY:", y, font_title, COLORS["accent"])
    
    y = 450
    x = 100
    items = [
        "Requests cross service boundaries",
        "Failures are intermittent",
        "Scale makes direct inspection impossible",
        "Context gets lost between services",
    ]
    
    for item in items:
        draw_text_left(draw, f"→  {item}", x, y, font_text, COLORS["text_primary"])
        y += 110
    
    return img


def create_slide_8() -> Image.Image:
    """CTA slide."""
    img = create_gradient_background(WIDTH, HEIGHT)
    img = add_decorative_elements(img, variant=8)
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(52, bold=True)
    font_text = get_font(40)
    font_cta = get_font(44, bold=True)
    font_url = get_font(36)
    
    y = 300
    draw_text_centered(draw, "Want the complete guide?", y, font_title, COLORS["text_primary"])
    
    y = 500
    draw_text_centered(draw, 'Comment "GUIDE"', y, font_cta, COLORS["accent"])
    y += 80
    draw_text_centered(draw, "and I'll send you my free", y, font_text, COLORS["text_secondary"])
    y += 70
    draw_text_centered(draw, "observability documentation.", y, font_text, COLORS["text_secondary"])
    
    y = 900
    draw_text_centered(draw, "Follow for more DevOps content", y, font_text, COLORS["text_primary"])
    
    y = HEIGHT - 200
    draw_text_centered(draw, "blog.shivamm.info", y, font_url, COLORS["accent"])
    
    return img


def main():
    """Generate all carousel slides."""
    output_dir = Path(__file__).parent / "carousel-slides"
    output_dir.mkdir(exist_ok=True)
    
    slides = [
        ("01-cover.png", create_slide_1),
        ("02-monitoring-answers.png", create_slide_2),
        ("03-observability-answers.png", create_slide_3),
        ("04-monitoring-dashboard.png", create_slide_4),
        ("05-observability-diagnostic.png", create_slide_5),
        ("06-three-pillars.png", create_slide_6),
        ("07-when-you-need.png", create_slide_7),
        ("08-cta.png", create_slide_8),
    ]
    
    print("🎨 Creating carousel slides...")
    print(f"📁 Output directory: {output_dir}\n")
    
    images = []
    for filename, create_func in slides:
        img = create_func()
        filepath = output_dir / filename
        img.save(filepath, "PNG", quality=95)
        images.append(img)
        print(f"  ✓ Created {filename}")
    
    # Create PDF for LinkedIn upload
    pdf_path = output_dir / "carousel.pdf"
    images[0].save(
        pdf_path,
        "PDF",
        save_all=True,
        append_images=images[1:],
        resolution=100.0
    )
    print(f"\n📄 Created carousel.pdf")
    
    print(f"\n✅ Done! Upload '{pdf_path}' to LinkedIn as a document post.")
    print("\n💡 Tip: On LinkedIn, click 'Create a post' → 'Document' → Select the PDF")


if __name__ == "__main__":
    main()
