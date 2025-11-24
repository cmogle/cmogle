"""Audio management for sound effects and music."""

from kivy.core.audio import SoundLoader
from pathlib import Path
import random


class AudioManager:
    """Manages game audio - sound effects and music."""

    def __init__(self, settings):
        self.settings = settings
        self.sounds = {}
        self.music = None
        self.music_volume = 0.3
        self.sfx_volume = 0.7

        # Try to load sounds (will fail gracefully if files don't exist)
        self.load_sounds()

    def load_sounds(self):
        """Load sound effects."""
        sound_files = {
            'correct': 'correct.wav',
            'incorrect': 'incorrect.wav',
            'coin': 'coin.wav',
            'complete': 'complete.wav',
            'click': 'click.wav',
        }

        from config.settings import SOUNDS_DIR

        for name, filename in sound_files.items():
            sound_path = SOUNDS_DIR / filename
            if sound_path.exists():
                try:
                    sound = SoundLoader.load(str(sound_path))
                    if sound:
                        sound.volume = self.sfx_volume
                        self.sounds[name] = sound
                except Exception as e:
                    print(f"Failed to load sound {name}: {e}")

    def play_correct(self):
        """Play correct answer sound."""
        if self.settings.get("sound_enabled", True):
            sound = self.sounds.get('correct')
            if sound:
                sound.play()

    def play_incorrect(self):
        """Play incorrect answer sound."""
        if self.settings.get("sound_enabled", True):
            sound = self.sounds.get('incorrect')
            if sound:
                sound.play()

    def play_coin(self):
        """Play coin collection sound."""
        if self.settings.get("sound_enabled", True):
            sound = self.sounds.get('coin')
            if sound:
                sound.play()

    def play_complete(self):
        """Play game complete sound."""
        if self.settings.get("sound_enabled", True):
            sound = self.sounds.get('complete')
            if sound:
                sound.play()

    def play_click(self):
        """Play button click sound."""
        if self.settings.get("sound_enabled", True):
            sound = self.sounds.get('click')
            if sound:
                sound.play()

    def start_music(self, track=None):
        """Start background music."""
        if not self.settings.get("music_enabled", True):
            return

        from config.settings import MUSIC_DIR

        if track is None:
            # Find a random music file
            music_files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.ogg"))
            if music_files:
                track = random.choice(music_files)
            else:
                return

        try:
            self.music = SoundLoader.load(str(track))
            if self.music:
                self.music.volume = self.music_volume
                self.music.loop = True
                self.music.play()
        except Exception as e:
            print(f"Failed to load music: {e}")

    def stop_music(self):
        """Stop background music."""
        if self.music:
            self.music.stop()

    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music:
            self.music.volume = self.music_volume

    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.volume = self.sfx_volume

    def toggle_sound(self):
        """Toggle sound effects on/off."""
        current = self.settings.get("sound_enabled", True)
        self.settings.set("sound_enabled", not current)

    def toggle_music(self):
        """Toggle music on/off."""
        current = self.settings.get("music_enabled", True)
        self.settings.set("music_enabled", not current)

        if current:  # Was on, now turning off
            self.stop_music()
        else:  # Was off, now turning on
            self.start_music()
