"""Game configuration and settings."""

import json
import os
from pathlib import Path

# Game constants
GAME_TITLE = "Times Table Rockstars"
GARAGE_COINS_PER_ANSWER = 10
STUDIO_COINS_PER_ANSWER = 5
SOUNDCHECK_QUESTIONS = 25
SOUNDCHECK_TIME_LIMIT = 6  # seconds per question
STUDIO_TIME_LIMIT = 60  # seconds

# File paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MUSIC_DIR = ASSETS_DIR / "music"
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Profile settings
PROFILE_FILE = DATA_DIR / "profile.json"

# Rock status levels (based on Studio speed - questions per minute)
ROCK_STATUS = {
    0: "Wannabe",
    10: "Gigging",
    20: "Unsigned Act",
    30: "Breakthrough Artist",
    40: "Support Act",
    50: "Headliner",
    60: "Rock Star",
    70: "Rock Legend",
    80: "Rock Hero",
}

# Color themes
THEMES = {
    "rock": {
        "primary": "#8B0000",  # Dark red
        "secondary": "#FFD700",  # Gold
        "background": "#1a1a1a",  # Dark gray
        "text": "#FFFFFF",  # White
        "accent": "#FF4500",  # Orange red
    },
    "ocean": {
        "primary": "#006994",
        "secondary": "#00C9FF",
        "background": "#001F3F",
        "text": "#FFFFFF",
        "accent": "#39CCCC",
    },
    "forest": {
        "primary": "#2D5016",
        "secondary": "#8BC34A",
        "background": "#1B3409",
        "text": "#FFFFFF",
        "accent": "#CDDC39",
    },
    "sunset": {
        "primary": "#FF6B35",
        "secondary": "#F7931E",
        "background": "#4A1A2C",
        "text": "#FFFFFF",
        "accent": "#FBB040",
    },
}

# Default settings
DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "music_enabled": True,
    "theme": "rock",
    "show_timer": True,
    "difficulty": "medium",
}


class Settings:
    """Manages game settings."""

    def __init__(self):
        self.settings_file = DATA_DIR / "settings.json"
        self.settings = self.load()

    def load(self):
        """Load settings from file."""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return DEFAULT_SETTINGS.copy()

    def save(self):
        """Save settings to file."""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set a setting value."""
        self.settings[key] = value
        self.save()

    def get_theme(self):
        """Get current theme colors."""
        theme_name = self.settings.get("theme", "rock")
        return THEMES.get(theme_name, THEMES["rock"])
