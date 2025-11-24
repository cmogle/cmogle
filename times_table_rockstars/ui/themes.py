"""UI theming and styling."""

from kivy.utils import get_color_from_hex
from config.settings import THEMES


class ThemeManager:
    """Manages UI themes and colors."""

    def __init__(self, settings):
        self.settings = settings
        self.current_theme = self.settings.get("theme", "rock")

    def get_theme_name(self):
        """Get current theme name."""
        return self.current_theme

    def set_theme(self, theme_name):
        """Set a new theme."""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.settings.set("theme", theme_name)

    def get_color(self, color_name):
        """Get a color from the current theme.

        Args:
            color_name: One of "primary", "secondary", "background", "text", "accent"

        Returns:
            Kivy color tuple (r, g, b, a)
        """
        theme = THEMES.get(self.current_theme, THEMES["rock"])
        hex_color = theme.get(color_name, "#FFFFFF")
        return get_color_from_hex(hex_color)

    def get_all_themes(self):
        """Get list of all available themes."""
        return list(THEMES.keys())

    def get_theme_preview(self, theme_name):
        """Get color preview for a theme."""
        theme = THEMES.get(theme_name, THEMES["rock"])
        return {
            key: get_color_from_hex(value)
            for key, value in theme.items()
        }


def apply_shadow(widget, offset=(0, -2), blur_radius=5):
    """Apply a shadow effect to a widget (helper function)."""
    # This is a placeholder - full shadow implementation would use
    # custom graphics instructions
    pass


def create_gradient_background(colors):
    """Create a gradient background (helper function)."""
    # Placeholder for gradient creation
    # Would use Canvas instructions in actual implementation
    pass
