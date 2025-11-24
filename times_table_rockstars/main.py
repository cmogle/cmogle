"""
Times Table Rockstars - Main Application
A Python replica of the Times Table Rockstars game for mobile devices.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform

from game.core import GameEngine
from game.audio import AudioManager
from ui.screens import (
    MenuScreen, GarageSelectScreen, JammingSelectScreen,
    GameplayScreen, ResultsScreen, StatsScreen, SettingsScreen,
    AvatarCustomizationScreen
)
from ui.themes import ThemeManager


class TimesTableRockstarsApp(App):
    """Main application class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = None
        self.audio_manager = None
        self.theme_manager = None

    def build(self):
        """Build the application UI."""
        # Set window properties for desktop testing
        if platform not in ('android', 'ios'):
            Window.size = (400, 700)  # Phone-like dimensions

        # Initialize game engine
        self.game_engine = GameEngine()

        # Initialize audio manager
        self.audio_manager = AudioManager(self.game_engine.get_settings())

        # Initialize theme manager
        self.theme_manager = ThemeManager(self.game_engine.get_settings())

        # Set window background color
        theme_colors = self.theme_manager.get_color('background')
        Window.clearcolor = theme_colors

        # Create screen manager
        screen_manager = ScreenManager(transition=FadeTransition())

        # Add all screens
        screen_manager.add_widget(MenuScreen(self.game_engine, name='menu'))
        screen_manager.add_widget(GarageSelectScreen(self.game_engine, name='garage_select'))
        screen_manager.add_widget(JammingSelectScreen(self.game_engine, name='jamming_select'))
        screen_manager.add_widget(GameplayScreen(
            self.game_engine,
            self.audio_manager,
            name='gameplay'
        ))
        screen_manager.add_widget(ResultsScreen(self.game_engine, name='results'))
        screen_manager.add_widget(StatsScreen(self.game_engine, name='stats'))
        screen_manager.add_widget(SettingsScreen(self.game_engine, name='settings'))
        screen_manager.add_widget(AvatarCustomizationScreen(
            self.game_engine,
            name='avatar_custom'
        ))

        # Start with menu screen
        screen_manager.current = 'menu'

        # Start background music
        # self.audio_manager.start_music()  # Uncomment when music files are added

        return screen_manager

    def on_start(self):
        """Called when the application starts."""
        print("Times Table Rockstars - Starting!")
        print(f"Profile: {self.game_engine.profile.data['rock_name']}")

    def on_pause(self):
        """Called when app goes to background (mobile)."""
        # Save game state
        self.game_engine.profile.save()
        return True

    def on_resume(self):
        """Called when app returns from background (mobile)."""
        pass

    def on_stop(self):
        """Called when application is closing."""
        # Save profile and settings
        self.game_engine.profile.save()
        self.game_engine.settings.save()
        self.audio_manager.stop_music()


def main():
    """Entry point for the application."""
    TimesTableRockstarsApp().run()


if __name__ == '__main__':
    main()
