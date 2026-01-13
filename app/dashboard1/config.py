"""
Configuration file for centralized constants and theme settings.
This file contains all color schemes, font settings, and reusable configurations
to maintain consistency across the dashboard and follow DRY principles.
"""

# Theme colors - Barclays corporate identity and dark theme
COLORS = {
    "primary": "#00AEEF",  # Barclays Cyan
    "primary_dark": "#0078B4",  # Darker cyan variant
    "navy": "#00395D",  # Barclays Navy
    "slate": "#475569",  # Neutral slate
    "background": "rgba(0,0,0,0)",  # Transparent background
    "text_primary": "#E0E7FF",  # Light text for dark backgrounds
    "text_secondary": "#94A3B8",  # Muted text
    "grid": "rgba(255,255,255,0.08)",  # Subtle grid lines
    "card_bg": "#0B1120",  # Card background
    "success": "#4ADE80",  # Green for positive metrics
    "warning": "#FACC15",  # Yellow for warnings
}

# Color scales for different chart types
COLOR_SCALES = {
    # Gradient from cyan to navy to slate (used in donut charts)
    "blue_gradient": ["#00AEEF", "#0078B4", "#005A8C", "#00395D", "#475569"],
    # Monochrome blue scale (used in treemaps)
    "blue_monochrome": [
        [0.00, "#0A2844"],  # Dark blue
        [0.50, "#0B5E8C"],  # Barclays Cyan
        [1.00, "#4BA3C3"],  # Light blue
    ],
    # Heatmap scale (used in geographic maps)
    "heatmap_blue": [
        [0.00, "#0B1220"],
        [0.15, "#0B2A3F"],
        [0.35, "#0B4A6A"],
        [0.55, "#0EA5E9"],
        [0.75, "#38BDF8"],
        [1.00, "#E0F2FE"],
    ],
    # Performance gradient (red to yellow to green to blue)
    "performance_gradient": ["#DC2626", "#F59E0B", "#10B981", "#00AEEF"],
}

# Font configuration for consistency
FONT_CONFIG = {
    "family": "Inter, Roboto, Arial",
    "color": "#E0E7FF",
    "size": 12,
}

# Chart dimensions and spacing
CHART_DIMENSIONS = {
    "default_height": 400,
    "default_margin": {"t": 20, "l": 20, "r": 20, "b": 20},
}
