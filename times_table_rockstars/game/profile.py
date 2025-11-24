"""User profile and progress management."""

import json
import random
from datetime import datetime
from pathlib import Path
from config.settings import PROFILE_FILE, ROCK_STATUS


class Profile:
    """Manages user profile and game progress."""

    # Rock star name components
    ADJECTIVES = [
        "Lightning", "Thunder", "Blazing", "Sonic", "Electric", "Cosmic",
        "Mega", "Super", "Turbo", "Radical", "Epic", "Legendary"
    ]

    NOUNS = [
        "Storm", "Bolt", "Flash", "Blaze", "Thunder", "Star",
        "Rocket", "Phoenix", "Dragon", "Tiger", "Wolf", "Eagle"
    ]

    def __init__(self):
        self.data = self.load()

    def load(self):
        """Load profile from file."""
        if PROFILE_FILE.exists():
            with open(PROFILE_FILE, 'r') as f:
                return json.load(f)
        return self._create_default_profile()

    def save(self):
        """Save profile to file."""
        PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def _create_default_profile(self):
        """Create a new default profile."""
        return {
            "rock_name": self.generate_rock_name(),
            "created_at": datetime.now().isoformat(),
            "total_coins": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "studio_speeds": [],  # List of recent studio speeds (questions/min)
            "best_studio_speed": 0,
            "rock_status": "Wannabe",
            "table_performance": {str(i): {"correct": 0, "total": 0} for i in range(2, 13)},
            "achievements": [],
            "customization": {
                "avatar_image": None,
                "theme": "rock",
                "favorite_color": "#8B0000",
            },
            "game_history": [],  # Recent game sessions
        }

    def generate_rock_name(self):
        """Generate a random rock star name."""
        adj = random.choice(self.ADJECTIVES)
        noun = random.choice(self.NOUNS)
        return f"{adj} {noun}"

    def set_rock_name(self, name):
        """Set custom rock star name."""
        self.data["rock_name"] = name
        self.save()

    def add_coins(self, amount):
        """Add coins to profile."""
        self.data["total_coins"] += amount
        self.save()

    def record_answer(self, table, correct):
        """Record an answer for a specific times table.

        Args:
            table: The times table number (2-12)
            correct: Whether the answer was correct
        """
        table_key = str(table)
        if table_key not in self.data["table_performance"]:
            self.data["table_performance"][table_key] = {"correct": 0, "total": 0}

        self.data["total_questions"] += 1
        self.data["table_performance"][table_key]["total"] += 1

        if correct:
            self.data["correct_answers"] += 1
            self.data["table_performance"][table_key]["correct"] += 1

        self.save()

    def get_table_accuracy(self, table):
        """Get accuracy percentage for a specific table."""
        table_key = str(table)
        perf = self.data["table_performance"].get(table_key, {"correct": 0, "total": 0})

        if perf["total"] == 0:
            return 0

        return (perf["correct"] / perf["total"]) * 100

    def get_overall_accuracy(self):
        """Get overall accuracy percentage."""
        if self.data["total_questions"] == 0:
            return 0

        return (self.data["correct_answers"] / self.data["total_questions"]) * 100

    def update_studio_speed(self, questions_per_minute):
        """Update studio speed and recalculate rock status.

        Args:
            questions_per_minute: Speed achieved in studio mode
        """
        # Keep last 10 studio speeds
        self.data["studio_speeds"].append(questions_per_minute)
        if len(self.data["studio_speeds"]) > 10:
            self.data["studio_speeds"] = self.data["studio_speeds"][-10:]

        # Update best speed
        if questions_per_minute > self.data["best_studio_speed"]:
            self.data["best_studio_speed"] = questions_per_minute

        # Update rock status based on average of last 10 games
        avg_speed = sum(self.data["studio_speeds"]) / len(self.data["studio_speeds"])
        self.data["rock_status"] = self._calculate_rock_status(avg_speed)

        self.save()

    def _calculate_rock_status(self, speed):
        """Calculate rock status based on speed."""
        status = "Wannabe"
        for threshold, status_name in sorted(ROCK_STATUS.items()):
            if speed >= threshold:
                status = status_name
            else:
                break
        return status

    def get_current_studio_speed(self):
        """Get current average studio speed."""
        if not self.data["studio_speeds"]:
            return 0
        return sum(self.data["studio_speeds"]) / len(self.data["studio_speeds"])

    def add_game_session(self, mode, duration, questions, correct, coins_earned):
        """Add a game session to history.

        Args:
            mode: Game mode played
            duration: Time in seconds
            questions: Number of questions
            correct: Number of correct answers
            coins_earned: Coins earned
        """
        session = {
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "questions": questions,
            "correct": correct,
            "accuracy": (correct / questions * 100) if questions > 0 else 0,
            "coins_earned": coins_earned,
        }

        self.data["game_history"].append(session)

        # Keep only last 50 sessions
        if len(self.data["game_history"]) > 50:
            self.data["game_history"] = self.data["game_history"][-50:]

        self.save()

    def get_weak_tables(self):
        """Get list of times tables that need practice."""
        weak_tables = []
        for table in range(2, 13):
            accuracy = self.get_table_accuracy(table)
            if accuracy < 70:
                weak_tables.append((table, accuracy))

        # Sort by accuracy (lowest first)
        weak_tables.sort(key=lambda x: x[1])
        return [table for table, _ in weak_tables]

    def set_avatar_image(self, image_path):
        """Set custom avatar image."""
        self.data["customization"]["avatar_image"] = image_path
        self.save()

    def set_theme(self, theme_name):
        """Set color theme."""
        self.data["customization"]["theme"] = theme_name
        self.save()

    def get_statistics(self):
        """Get formatted statistics."""
        return {
            "rock_name": self.data["rock_name"],
            "rock_status": self.data["rock_status"],
            "total_coins": self.data["total_coins"],
            "total_questions": self.data["total_questions"],
            "overall_accuracy": self.get_overall_accuracy(),
            "studio_speed": self.get_current_studio_speed(),
            "best_studio_speed": self.data["best_studio_speed"],
        }
