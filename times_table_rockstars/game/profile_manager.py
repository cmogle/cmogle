"""Multi-user profile management system."""

import json
from pathlib import Path
from datetime import datetime
from game.profile import Profile
from config.settings import DATA_DIR


class ProfileManager:
    """Manages multiple user profiles."""

    def __init__(self):
        self.profiles_dir = DATA_DIR / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

        self.profiles_index_file = DATA_DIR / "profiles_index.json"
        self.current_user_file = DATA_DIR / "current_user.json"

        self.profiles_index = self.load_profiles_index()
        self.current_user_id = self.load_current_user()

        # Create default profile if none exist
        if not self.profiles_index:
            self.create_profile("Default Player")

    def load_profiles_index(self):
        """Load the index of all profiles."""
        if self.profiles_index_file.exists():
            with open(self.profiles_index_file, 'r') as f:
                return json.load(f)
        return {}

    def save_profiles_index(self):
        """Save the profiles index."""
        with open(self.profiles_index_file, 'w') as f:
            json.dump(self.profiles_index, f, indent=2)

    def load_current_user(self):
        """Load the current active user ID."""
        if self.current_user_file.exists():
            with open(self.current_user_file, 'r') as f:
                data = json.load(f)
                return data.get("current_user_id")
        return None

    def save_current_user(self, user_id):
        """Save the current active user ID."""
        with open(self.current_user_file, 'w') as f:
            json.dump({"current_user_id": user_id}, f, indent=2)

    def generate_user_id(self):
        """Generate a unique user ID."""
        import uuid
        return str(uuid.uuid4())[:8]

    def create_profile(self, name, rock_name=None):
        """Create a new profile.

        Args:
            name: Display name for the user
            rock_name: Optional custom rock star name

        Returns:
            user_id: The ID of the created profile
        """
        user_id = self.generate_user_id()

        # Create profile data
        profile_data = {
            "user_id": user_id,
            "name": name,
            "rock_name": rock_name or Profile.generate_rock_name(Profile),
            "created_at": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat(),
            "total_coins": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "studio_speeds": [],
            "best_studio_speed": 0,
            "rock_status": "Wannabe",
            "table_performance": {str(i): {"correct": 0, "total": 0} for i in range(2, 13)},
            "achievements": [],
            "customization": {
                "avatar_image": None,
                "theme": "rock",
                "favorite_color": "#8B0000",
            },
            "game_history": [],
        }

        # Save profile
        profile_file = self.profiles_dir / f"{user_id}.json"
        with open(profile_file, 'w') as f:
            json.dump(profile_data, f, indent=2)

        # Update index
        self.profiles_index[user_id] = {
            "name": name,
            "rock_name": profile_data["rock_name"],
            "created_at": profile_data["created_at"],
            "last_played": profile_data["last_played"],
        }
        self.save_profiles_index()

        # Set as current user if it's the first profile
        if len(self.profiles_index) == 1:
            self.set_current_user(user_id)

        return user_id

    def delete_profile(self, user_id):
        """Delete a profile.

        Args:
            user_id: The ID of the profile to delete

        Returns:
            bool: True if deleted, False if not found or if it's the last profile
        """
        # Don't allow deleting the last profile
        if len(self.profiles_index) <= 1:
            return False

        if user_id not in self.profiles_index:
            return False

        # Delete profile file
        profile_file = self.profiles_dir / f"{user_id}.json"
        if profile_file.exists():
            profile_file.unlink()

        # Remove from index
        del self.profiles_index[user_id]
        self.save_profiles_index()

        # If this was the current user, switch to another
        if self.current_user_id == user_id:
            if self.profiles_index:
                next_user = list(self.profiles_index.keys())[0]
                self.set_current_user(next_user)

        return True

    def get_profile(self, user_id):
        """Load a profile by user ID.

        Args:
            user_id: The ID of the profile to load

        Returns:
            Profile object or None if not found
        """
        if user_id not in self.profiles_index:
            return None

        profile_file = self.profiles_dir / f"{user_id}.json"
        if not profile_file.exists():
            return None

        # Create a Profile object and load the data
        profile = Profile()
        with open(profile_file, 'r') as f:
            profile.data = json.load(f)

        # Override the save method to save to the correct file
        original_save = profile.save
        def custom_save():
            with open(profile_file, 'w') as f:
                json.dump(profile.data, f, indent=2)
            # Update last played time in index
            self.profiles_index[user_id]["last_played"] = datetime.now().isoformat()
            self.save_profiles_index()

        profile.save = custom_save
        return profile

    def get_current_profile(self):
        """Get the current active profile.

        Returns:
            Profile object
        """
        if self.current_user_id:
            profile = self.get_profile(self.current_user_id)
            if profile:
                return profile

        # Fallback: return first profile
        if self.profiles_index:
            first_user_id = list(self.profiles_index.keys())[0]
            self.set_current_user(first_user_id)
            return self.get_profile(first_user_id)

        # Should never happen, but create a default profile
        user_id = self.create_profile("Default Player")
        return self.get_profile(user_id)

    def set_current_user(self, user_id):
        """Set the current active user.

        Args:
            user_id: The ID of the user to make active

        Returns:
            bool: True if successful, False if user not found
        """
        if user_id not in self.profiles_index:
            return False

        self.current_user_id = user_id
        self.save_current_user(user_id)

        # Update last played time
        self.profiles_index[user_id]["last_played"] = datetime.now().isoformat()
        self.save_profiles_index()

        return True

    def get_all_profiles(self):
        """Get a list of all profiles with basic info.

        Returns:
            List of dicts with profile info
        """
        profiles = []
        for user_id, info in self.profiles_index.items():
            profiles.append({
                "user_id": user_id,
                "name": info["name"],
                "rock_name": info["rock_name"],
                "created_at": info["created_at"],
                "last_played": info["last_played"],
                "is_current": user_id == self.current_user_id,
            })

        # Sort by last played (most recent first)
        profiles.sort(key=lambda x: x["last_played"], reverse=True)
        return profiles

    def reset_profile_stats(self, user_id):
        """Reset all statistics for a profile, keeping name and customization.

        Args:
            user_id: The ID of the profile to reset

        Returns:
            bool: True if successful, False if user not found
        """
        profile = self.get_profile(user_id)
        if not profile:
            return False

        # Keep name and customization
        name = profile.data.get("name", "Player")
        rock_name = profile.data["rock_name"]
        customization = profile.data.get("customization", {})

        # Reset statistics
        profile.data.update({
            "total_coins": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "studio_speeds": [],
            "best_studio_speed": 0,
            "rock_status": "Wannabe",
            "table_performance": {str(i): {"correct": 0, "total": 0} for i in range(2, 13)},
            "achievements": [],
            "game_history": [],
        })

        # Restore name and customization
        profile.data["name"] = name
        profile.data["rock_name"] = rock_name
        profile.data["customization"] = customization

        profile.save()
        return True

    def rename_profile(self, user_id, new_name):
        """Rename a profile.

        Args:
            user_id: The ID of the profile to rename
            new_name: The new name

        Returns:
            bool: True if successful, False if user not found
        """
        if user_id not in self.profiles_index:
            return False

        # Update index
        self.profiles_index[user_id]["name"] = new_name
        self.save_profiles_index()

        # Update profile data
        profile = self.get_profile(user_id)
        if profile:
            profile.data["name"] = new_name
            profile.save()

        return True

    def get_profile_stats_summary(self, user_id):
        """Get a summary of profile statistics.

        Args:
            user_id: The ID of the profile

        Returns:
            Dict with statistics summary or None if not found
        """
        profile = self.get_profile(user_id)
        if not profile:
            return None

        return {
            "name": profile.data.get("name", "Player"),
            "rock_name": profile.data["rock_name"],
            "rock_status": profile.data["rock_status"],
            "total_coins": profile.data["total_coins"],
            "total_questions": profile.data["total_questions"],
            "correct_answers": profile.data["correct_answers"],
            "overall_accuracy": profile.get_overall_accuracy(),
            "studio_speed": profile.get_current_studio_speed(),
            "best_studio_speed": profile.data["best_studio_speed"],
            "games_played": len(profile.data["game_history"]),
        }
