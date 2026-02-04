#!/usr/bin/env python3
"""
LinkedIn Carousel PDF Generator
NVIDIA-themed design with dark background and green accents
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import os

# LinkedIn Carousel dimensions (1080x1350 px at 72 DPI = 15x18.75 inches)
# We'll use points (72 points = 1 inch)
WIDTH = 1080
HEIGHT = 1350

# NVIDIA Color Scheme (matching your website)
COLORS = {
    'background': HexColor('#0a0a0a'),      # Near black
    'background_gradient': HexColor('#0d1f0d'),  # Dark green tint
    'primary_green': HexColor('#76B900'),    # NVIDIA Green
    'accent_green': HexColor('#7FFF00'),     # Bright lime (from your site)
    'text_white': HexColor('#FFFFFF'),
    'text_gray': HexColor('#B0B0B0'),
    'text_light_gray': HexColor('#E0E0E0'),
    'card_bg': HexColor('#1a1a1a'),
    'highlight': HexColor('#4ADE80'),        # Success green
}


def draw_gradient_background(c, width, height):
    """Draw a dark gradient background with subtle green tint"""
    # Base dark background
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Add subtle gradient overlay using circles
    for i in range(20):
        alpha = 0.02 - (i * 0.001)
        if alpha > 0:
            c.setFillColor(HexColor('#76B900'))
            c.setFillAlpha(alpha)
            # Bottom right glow
            c.circle(width * 0.8, height * 0.2, 200 + i * 30, fill=1, stroke=0)
            # Top left subtle glow
            c.circle(width * 0.2, height * 0.8, 150 + i * 20, fill=1, stroke=0)
    
    c.setFillAlpha(1)  # Reset alpha


def draw_decorative_elements(c, width, height):
    """Add subtle decorative grid/tech elements"""
    c.setStrokeColor(COLORS['primary_green'])
    c.setStrokeAlpha(0.05)
    c.setLineWidth(0.5)
    
    # Subtle grid lines
    for i in range(0, int(width), 80):
        c.line(i, 0, i, height)
    for i in range(0, int(height), 80):
        c.line(0, i, width, i)
    
    c.setStrokeAlpha(1)


def draw_text_centered(c, text, y, font_size, color=None, font='Helvetica-Bold'):
    """Draw centered text"""
    if color:
        c.setFillColor(color)
    c.setFont(font, font_size)
    text_width = c.stringWidth(text, font, font_size)
    x = (WIDTH - text_width) / 2
    c.drawString(x, y, text)


def draw_text_left(c, text, x, y, font_size, color=None, font='Helvetica'):
    """Draw left-aligned text"""
    if color:
        c.setFillColor(color)
    c.setFont(font, font_size)
    c.drawString(x, y, text)


def draw_bullet_point(c, text, x, y, font_size, color=None):
    """Draw a bullet point with green accent"""
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', font_size)
    c.drawString(x, y, "•")
    
    if color:
        c.setFillColor(color)
    else:
        c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', font_size)
    c.drawString(x + 25, y, text)


def draw_checkmark(c, text, x, y, font_size):
    """Draw a checkmark item with green check"""
    c.setFillColor(COLORS['highlight'])
    c.setFont('Helvetica-Bold', font_size)
    c.drawString(x, y, "✓")
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', font_size)
    c.drawString(x + 30, y, text)


def draw_phase_badge(c, phase_num, y):
    """Draw a phase number badge"""
    badge_width = 180
    badge_height = 50
    x = (WIDTH - badge_width) / 2
    
    # Badge background
    c.setFillColor(COLORS['primary_green'])
    c.roundRect(x, y, badge_width, badge_height, 10, fill=1, stroke=0)
    
    # Badge text
    c.setFillColor(COLORS['background'])
    c.setFont('Helvetica-Bold', 28)
    text = f"PHASE {phase_num}"
    text_width = c.stringWidth(text, 'Helvetica-Bold', 28)
    c.drawString(x + (badge_width - text_width) / 2, y + 15, text)


def create_slide_1_cover(c):
    """Cover slide"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    # Main title
    c.setFillColor(COLORS['text_white'])
    draw_text_centered(c, "FROM IDEA TO PRODUCTION", HEIGHT - 350, 52, COLORS['text_white'])
    
    # Accent line
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "IN 1 YEAR", HEIGHT - 420, 72, COLORS['accent_green'])
    
    # Subtitle
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "The 5-Phase AI Development", HEIGHT - 520, 40, COLORS['text_gray'])
    draw_text_centered(c, "Workflow We Used at NVIDIA", HEIGHT - 570, 40, COLORS['text_gray'])
    
    # Stats box
    box_y = HEIGHT - 780
    box_height = 120
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['card_bg'])
    c.setFillAlpha(0.7)
    c.roundRect(box_x, box_y, box_width, box_height, 15, fill=1, stroke=0)
    c.setFillAlpha(1)
    
    # Stats
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    stats = "200K lines  •  3,248 tests  •  3 engineers"
    stats_width = c.stringWidth(stats, 'Helvetica-Bold', 28)
    c.drawString((WIDTH - stats_width) / 2, box_y + 45, stats)
    
    # Swipe indicator
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Swipe →", HEIGHT - 1200, 32, COLORS['text_gray'])


def create_slide_2_design(c):
    """Phase 1: Design"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    draw_phase_badge(c, 1, HEIGHT - 200)
    
    # Title
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "DESIGN", HEIGHT - 320, 64, COLORS['accent_green'])
    
    # Time
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Time: ~1 week", HEIGHT - 380, 28, COLORS['text_gray'])
    
    # Bullet points
    y_start = HEIGHT - 500
    line_height = 70
    items = [
        "Brainstorm with AI (Cursor + Gemini)",
        "Create design documents",
        "Technology comparison research",
        "Architecture definition",
        "API specifications"
    ]
    
    for i, item in enumerate(items):
        draw_bullet_point(c, item, 150, y_start - (i * line_height), 32)
    
    # Key insight box
    box_y = HEIGHT - 1050
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['primary_green'])
    c.setFillAlpha(0.15)
    c.roundRect(box_x, box_y, box_width, 150, 15, fill=1, stroke=0)
    c.setFillAlpha(1)
    
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    c.drawString(box_x + 30, box_y + 100, "Key:")
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', 28)
    c.drawString(box_x + 100, box_y + 100, "Use AI for THINKING,")
    c.drawString(box_x + 100, box_y + 55, "not just coding.")


def create_slide_3_standards(c):
    """Phase 2: Standards"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    draw_phase_badge(c, 2, HEIGHT - 200)
    
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "STANDARDS", HEIGHT - 320, 64, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Time: ~1 week", HEIGHT - 380, 28, COLORS['text_gray'])
    
    # Intro text
    c.setFillColor(COLORS['text_white'])
    draw_text_centered(c, "Ask AI to document:", HEIGHT - 470, 32, COLORS['text_white'])
    
    y_start = HEIGHT - 570
    line_height = 70
    items = [
        "Coding guidelines",
        "Testing standards (we set 85%+)",
        "Documentation conventions",
        "CI/CD workflow",
        "Code structure expectations"
    ]
    
    for i, item in enumerate(items):
        draw_bullet_point(c, item, 150, y_start - (i * line_height), 32)
    
    # Key insight box
    box_y = HEIGHT - 1050
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['primary_green'])
    c.setFillAlpha(0.15)
    c.roundRect(box_x, box_y, box_width, 150, 15, fill=1, stroke=0)
    c.setFillAlpha(1)
    
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    c.drawString(box_x + 30, box_y + 100, "Key:")
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', 28)
    c.drawString(box_x + 100, box_y + 100, "AI follows YOUR rules—")
    c.drawString(box_x + 100, box_y + 55, "if you give it rules.")


def create_slide_4_bootstrap(c):
    """Phase 3: Bootstrap"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    draw_phase_badge(c, 3, HEIGHT - 200)
    
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "BOOTSTRAP", HEIGHT - 320, 64, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Time: ~1 day", HEIGHT - 380, 28, COLORS['text_gray'])
    
    # Main instruction
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica-Bold', 36)
    draw_text_centered(c, "Feed ALL documents to Cursor.", HEIGHT - 500, 36, COLORS['text_white'])
    
    # Quote box
    box_y = HEIGHT - 680
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['card_bg'])
    c.roundRect(box_x, box_y, box_width, 100, 10, fill=1, stroke=0)
    
    c.setFillColor(COLORS['text_gray'])
    c.setFont('Helvetica-Oblique', 28)
    draw_text_centered(c, '"Create a project following', box_y + 60, 28, COLORS['text_gray'], 'Helvetica-Oblique')
    draw_text_centered(c, 'these standards."', box_y + 20, 28, COLORS['text_gray'], 'Helvetica-Oblique')
    
    # Results
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica-Bold', 32)
    draw_text_centered(c, "Result:", HEIGHT - 820, 32, COLORS['text_white'])
    
    y_start = HEIGHT - 900
    items = [
        "Day 1 code quality",
        "Consistent structure",
        "No cleanup needed later"
    ]
    
    for i, item in enumerate(items):
        draw_checkmark(c, item, 280, y_start - (i * 60), 32)


def create_slide_5_roadmap(c):
    """Phase 4: Roadmap"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    draw_phase_badge(c, 4, HEIGHT - 200)
    
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "ROADMAP", HEIGHT - 320, 64, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Time: ~3 days", HEIGHT - 380, 28, COLORS['text_gray'])
    
    y_start = HEIGHT - 520
    line_height = 70
    items = [
        "Break into milestones",
        "Create implementation plans",
        "Define actionable items per feature",
        "Set measurable targets"
    ]
    
    for i, item in enumerate(items):
        draw_bullet_point(c, item, 150, y_start - (i * line_height), 32)
    
    # Key insight box
    box_y = HEIGHT - 950
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['primary_green'])
    c.setFillAlpha(0.15)
    c.roundRect(box_x, box_y, box_width, 150, 15, fill=1, stroke=0)
    c.setFillAlpha(1)
    
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    c.drawString(box_x + 30, box_y + 100, "Key:")
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', 28)
    c.drawString(box_x + 100, box_y + 100, "Plan THOROUGHLY before")
    c.drawString(box_x + 100, box_y + 55, "asking AI to build.")


def create_slide_6_build(c):
    """Phase 5: Build"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    draw_phase_badge(c, 5, HEIGHT - 200)
    
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "BUILD", HEIGHT - 320, 64, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_gray'])
    draw_text_centered(c, "Time: ~6-7 weeks", HEIGHT - 380, 28, COLORS['text_gray'])
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica-Bold', 32)
    draw_text_centered(c, "Feature by feature:", HEIGHT - 480, 32, COLORS['text_white'])
    
    y_start = HEIGHT - 580
    line_height = 70
    items = [
        "Reference the roadmap",
        "Implement with AI",
        "Maintain progress log",
        "Handle crashes gracefully"
    ]
    
    for i, item in enumerate(items):
        draw_bullet_point(c, item, 150, y_start - (i * line_height), 32)
    
    # Key insight box
    box_y = HEIGHT - 1000
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['primary_green'])
    c.setFillAlpha(0.15)
    c.roundRect(box_x, box_y, box_width, 150, 15, fill=1, stroke=0)
    c.setFillAlpha(1)
    
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    c.drawString(box_x + 30, box_y + 100, "Key:")
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica', 28)
    c.drawString(box_x + 100, box_y + 100, 'The progress log is your')
    c.drawString(box_x + 100, box_y + 55, '"save game" for AI development.')


def create_slide_7_secret(c):
    """The Secret Sauce: Progress Log"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    # Title
    c.setFillColor(COLORS['text_white'])
    draw_text_centered(c, "THE SECRET SAUCE:", HEIGHT - 250, 48, COLORS['text_white'])
    
    c.setFillColor(COLORS['accent_green'])
    draw_text_centered(c, "THE PROGRESS LOG", HEIGHT - 330, 56, COLORS['accent_green'])
    
    # Every session box
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica-Bold', 32)
    draw_text_centered(c, "Every session:", HEIGHT - 450, 32, COLORS['text_white'])
    
    y_start = HEIGHT - 550
    items = [
        "What's done",
        "Current status",
        "What's next",
        "Decisions made"
    ]
    
    for i, item in enumerate(items):
        draw_checkmark(c, item, 320, y_start - (i * 60), 32)
    
    # Bottom highlights
    box_y = HEIGHT - 950
    box_width = 800
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['card_bg'])
    c.roundRect(box_x, box_y, box_width, 150, 15, fill=1, stroke=0)
    
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 28)
    draw_text_centered(c, "Agent crashes? Resume instantly.", box_y + 100, 28, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_white'])
    c.setFont('Helvetica-Bold', 28)
    draw_text_centered(c, "Context lost? Never.", box_y + 50, 28, COLORS['text_white'])


def create_slide_8_results(c):
    """The Results"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    # Title
    c.setFillColor(COLORS['text_white'])
    draw_text_centered(c, "THE RESULT:", HEIGHT - 250, 56, COLORS['text_white'])
    
    # Results with checkmarks
    y_start = HEIGHT - 420
    line_height = 80
    items = [
        "200,000 lines of code",
        "3,248 tests (2:1 ratio)",
        "2 applications (Java + Go)",
        "1 year total (3-4x faster)",
        "3 engineers"
    ]
    
    for i, item in enumerate(items):
        draw_checkmark(c, item, 200, y_start - (i * line_height), 36)
    
    # Comparison box
    box_y = HEIGHT - 1000
    box_width = 700
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['card_bg'])
    c.roundRect(box_x, box_y, box_width, 100, 15, fill=1, stroke=0)
    
    c.setFillColor(COLORS['text_gray'])
    c.setFont('Helvetica', 28)
    draw_text_centered(c, "Traditional timeline: 3-4 years", box_y + 35, 28, COLORS['text_gray'])


def create_slide_9_cta(c):
    """Call to Action"""
    draw_gradient_background(c, WIDTH, HEIGHT)
    draw_decorative_elements(c, WIDTH, HEIGHT)
    
    # Title
    c.setFillColor(COLORS['text_white'])
    draw_text_centered(c, "Want the detailed", HEIGHT - 350, 48, COLORS['text_white'])
    draw_text_centered(c, "workflow?", HEIGHT - 420, 48, COLORS['text_white'])
    
    # CTA Box
    box_y = HEIGHT - 650
    box_width = 700
    box_height = 150
    box_x = (WIDTH - box_width) / 2
    
    c.setFillColor(COLORS['primary_green'])
    c.roundRect(box_x, box_y, box_width, box_height, 15, fill=1, stroke=0)
    
    c.setFillColor(COLORS['background'])
    c.setFont('Helvetica-Bold', 32)
    draw_text_centered(c, 'Comment "WORKFLOW"', box_y + 95, 32, COLORS['background'])
    c.setFont('Helvetica', 28)
    draw_text_centered(c, "and I'll share our internal playbook.", box_y + 45, 28, COLORS['background'])
    
    # Follow CTA
    c.setFillColor(COLORS['text_gray'])
    c.setFont('Helvetica', 32)
    draw_text_centered(c, "Follow for more AI dev content.", HEIGHT - 850, 32, COLORS['text_gray'])
    
    # Handle/Name
    c.setFillColor(COLORS['accent_green'])
    c.setFont('Helvetica-Bold', 36)
    draw_text_centered(c, "Shivam Mishra", HEIGHT - 1000, 36, COLORS['accent_green'])
    
    c.setFillColor(COLORS['text_gray'])
    c.setFont('Helvetica', 28)
    draw_text_centered(c, "Senior Software Engineer @ NVIDIA", HEIGHT - 1050, 28, COLORS['text_gray'])


def create_carousel_pdf(output_path):
    """Generate the complete carousel PDF"""
    c = canvas.Canvas(output_path, pagesize=(WIDTH, HEIGHT))
    
    # Slide 1: Cover
    create_slide_1_cover(c)
    c.showPage()
    
    # Slide 2: Phase 1 - Design
    create_slide_2_design(c)
    c.showPage()
    
    # Slide 3: Phase 2 - Standards
    create_slide_3_standards(c)
    c.showPage()
    
    # Slide 4: Phase 3 - Bootstrap
    create_slide_4_bootstrap(c)
    c.showPage()
    
    # Slide 5: Phase 4 - Roadmap
    create_slide_5_roadmap(c)
    c.showPage()
    
    # Slide 6: Phase 5 - Build
    create_slide_6_build(c)
    c.showPage()
    
    # Slide 7: Secret Sauce
    create_slide_7_secret(c)
    c.showPage()
    
    # Slide 8: Results
    create_slide_8_results(c)
    c.showPage()
    
    # Slide 9: CTA
    create_slide_9_cta(c)
    
    c.save()
    print(f"✅ Carousel PDF created: {output_path}")


if __name__ == "__main__":
    # Output path
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "carousel-5-phase-workflow.pdf")
    
    create_carousel_pdf(output_path)
    print(f"\n📊 PDF Details:")
    print(f"   - Dimensions: {WIDTH}x{HEIGHT} pixels")
    print(f"   - Slides: 9")
    print(f"   - Theme: NVIDIA (dark + green)")
    print(f"\n📤 Upload this PDF directly to LinkedIn as a document post.")
