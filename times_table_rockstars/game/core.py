"""Core game engine."""

from game.profile import Profile
from game.profile_manager import ProfileManager
from game.modes import GarageMode, StudioMode, JammingMode, SoundcheckMode
from config.settings import Settings


class GameEngine:
    """Main game engine that coordinates all game systems."""

    def __init__(self):
        self.profile_manager = ProfileManager()
        self.profile = self.profile_manager.get_current_profile()
        self.settings = Settings()
        self.current_mode = None
        self.audio_manager = None  # Will be set by UI

    def get_profile(self):
        """Get the current profile."""
        return self.profile

    def get_profile_manager(self):
        """Get the profile manager."""
        return self.profile_manager

    def switch_user(self, user_id):
        """Switch to a different user.

        Args:
            user_id: The ID of the user to switch to

        Returns:
            bool: True if successful, False otherwise
        """
        if self.profile_manager.set_current_user(user_id):
            self.profile = self.profile_manager.get_current_profile()
            return True
        return False

    def get_settings(self):
        """Get game settings."""
        return self.settings

    def start_garage_mode(self, table=None):
        """Start Garage mode.

        Args:
            table: Specific times table to practice (2-12), or None for adaptive
        """
        self.current_mode = GarageMode(self.profile, table)
        self.current_mode.start()
        return self.current_mode

    def start_studio_mode(self):
        """Start Studio mode."""
        self.current_mode = StudioMode(self.profile)
        self.current_mode.start()
        return self.current_mode

    def start_jamming_mode(self, tables=None, operation="mixed"):
        """Start Jamming mode.

        Args:
            tables: List of tables to practice, or None for all
            operation: "multiplication", "division", or "mixed"
        """
        self.current_mode = JammingMode(self.profile, tables, operation)
        self.current_mode.start()
        return self.current_mode

    def start_soundcheck_mode(self):
        """Start Soundcheck mode."""
        self.current_mode = SoundcheckMode(self.profile)
        self.current_mode.start()
        return self.current_mode

    def get_current_mode(self):
        """Get the currently active game mode."""
        return self.current_mode

    def finish_current_mode(self):
        """Finish the current game mode and get results."""
        if self.current_mode is None:
            return None

        results = self.current_mode.finish()
        self.current_mode = None
        return results

    def update_profile_name(self, name):
        """Update the profile's rock star name."""
        self.profile.set_rock_name(name)

    def update_avatar(self, image_path):
        """Update the profile's avatar image."""
        self.profile.set_avatar_image(image_path)

    def update_theme(self, theme_name):
        """Update the color theme."""
        self.profile.set_theme(theme_name)
        self.settings.set("theme", theme_name)

    def get_statistics(self):
        """Get formatted player statistics."""
        return self.profile.get_statistics()

    def get_table_performance(self):
        """Get performance data for all times tables."""
        performance = {}
        for table in range(2, 13):
            accuracy = self.profile.get_table_accuracy(table)
            performance[table] = accuracy
        return performance

    def get_recent_games(self, count=10):
        """Get recent game sessions."""
        history = self.profile.data.get("game_history", [])
        return history[-count:] if len(history) > count else history

    def reset_profile(self):
        """Reset the current profile statistics."""
        user_id = self.profile_manager.current_user_id
        if user_id:
            self.profile_manager.reset_profile_stats(user_id)
            self.profile = self.profile_manager.get_current_profile()
