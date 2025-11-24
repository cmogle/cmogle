"""Game mode implementations."""

import time
from typing import Optional
from game.questions import QuestionGenerator
from game.profile import Profile
from config.settings import (
    GARAGE_COINS_PER_ANSWER,
    STUDIO_COINS_PER_ANSWER,
    SOUNDCHECK_QUESTIONS,
    SOUNDCHECK_TIME_LIMIT,
    STUDIO_TIME_LIMIT
)


class GameMode:
    """Base class for game modes."""

    def __init__(self, profile: Profile):
        self.profile = profile
        self.question_gen = QuestionGenerator()
        self.current_question = None
        self.questions_answered = 0
        self.correct_answers = 0
        self.total_coins = 0
        self.start_time = None
        self.mode_name = "Base"

    def start(self):
        """Start the game mode."""
        self.start_time = time.time()
        self.questions_answered = 0
        self.correct_answers = 0
        self.total_coins = 0

    def get_next_question(self):
        """Get the next question. Override in subclasses."""
        raise NotImplementedError

    def submit_answer(self, answer: int) -> bool:
        """Submit an answer and check if correct."""
        if self.current_question is None:
            return False

        _, _, correct_answer, _ = self.current_question
        is_correct = (answer == correct_answer)

        self.questions_answered += 1
        if is_correct:
            self.correct_answers += 1

        return is_correct

    def get_elapsed_time(self):
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def get_accuracy(self):
        """Get current accuracy percentage."""
        if self.questions_answered == 0:
            return 0
        return (self.correct_answers / self.questions_answered) * 100

    def finish(self):
        """Finish the game and save results."""
        duration = self.get_elapsed_time()
        self.profile.add_coins(self.total_coins)
        self.profile.add_game_session(
            mode=self.mode_name,
            duration=duration,
            questions=self.questions_answered,
            correct=self.correct_answers,
            coins_earned=self.total_coins
        )

        return {
            "mode": self.mode_name,
            "questions": self.questions_answered,
            "correct": self.correct_answers,
            "accuracy": self.get_accuracy(),
            "coins": self.total_coins,
            "duration": duration,
        }


class GarageMode(GameMode):
    """Garage mode - practice specific tables with high rewards."""

    def __init__(self, profile: Profile, table: Optional[int] = None):
        super().__init__(profile)
        self.mode_name = "Garage"
        self.table = table  # Specific table to practice, or None for adaptive
        self.coins_per_answer = GARAGE_COINS_PER_ANSWER

    def start(self):
        """Start garage mode."""
        super().start()

        # If no table specified, choose weakest table
        if self.table is None:
            weak_tables = self.profile.get_weak_tables()
            if weak_tables:
                self.table = weak_tables[0]
            else:
                import random
                self.table = random.randint(2, 12)

    def get_next_question(self):
        """Get next question for the selected table."""
        difficulty = self.profile.data["customization"].get("difficulty", "medium")
        self.current_question = self.question_gen.generate_mixed(
            table=self.table,
            difficulty=difficulty
        )
        return self.current_question

    def submit_answer(self, answer: int) -> bool:
        """Submit answer and award coins if correct."""
        is_correct = super().submit_answer(answer)

        # Record answer for this table
        self.profile.record_answer(self.table, is_correct)

        if is_correct:
            self.total_coins += self.coins_per_answer

        return is_correct


class StudioMode(GameMode):
    """Studio mode - timed challenge to set speed records."""

    def __init__(self, profile: Profile):
        super().__init__(profile)
        self.mode_name = "Studio"
        self.time_limit = STUDIO_TIME_LIMIT
        self.coins_per_answer = STUDIO_COINS_PER_ANSWER

    def get_next_question(self):
        """Get next random question."""
        difficulty = self.profile.data["customization"].get("difficulty", "medium")
        self.current_question = self.question_gen.generate_mixed(
            table=None,
            difficulty=difficulty
        )
        return self.current_question

    def submit_answer(self, answer: int) -> bool:
        """Submit answer and award coins if correct."""
        is_correct = super().submit_answer(answer)

        # Extract table from question
        num1, num2, _, _ = self.current_question
        # Record for the smaller number (the table being practiced)
        table = min(num1, num2) if min(num1, num2) <= 12 else max(num1, num2)
        self.profile.record_answer(table, is_correct)

        if is_correct:
            self.total_coins += self.coins_per_answer

        return is_correct

    def is_time_up(self):
        """Check if time limit has been reached."""
        return self.get_elapsed_time() >= self.time_limit

    def finish(self):
        """Finish studio mode and update speed."""
        result = super().finish()

        # Calculate questions per minute
        if result["duration"] > 0:
            questions_per_minute = (self.correct_answers / result["duration"]) * 60
            self.profile.update_studio_speed(questions_per_minute)
            result["speed"] = questions_per_minute

        return result


class JammingMode(GameMode):
    """Jamming mode - relaxed practice without timer."""

    def __init__(self, profile: Profile, tables: Optional[list] = None,
                 operation: str = "mixed"):
        super().__init__(profile)
        self.mode_name = "Jamming"
        self.tables = tables or list(range(2, 13))
        self.operation = operation  # "multiplication", "division", or "mixed"
        self.coins_per_answer = STUDIO_COINS_PER_ANSWER

    def get_next_question(self):
        """Get next question based on selected tables and operation."""
        import random
        table = random.choice(self.tables)
        difficulty = self.profile.data["customization"].get("difficulty", "medium")

        if self.operation == "multiplication":
            self.current_question = self.question_gen.generate_multiplication(
                table=table, difficulty=difficulty
            )
        elif self.operation == "division":
            self.current_question = self.question_gen.generate_division(
                table=table, difficulty=difficulty
            )
        else:
            self.current_question = self.question_gen.generate_mixed(
                table=table, difficulty=difficulty
            )

        return self.current_question

    def submit_answer(self, answer: int) -> bool:
        """Submit answer and award coins if correct."""
        is_correct = super().submit_answer(answer)

        # Extract table from question
        num1, num2, _, _ = self.current_question
        table = min(num1, num2) if min(num1, num2) <= 12 else max(num1, num2)
        self.profile.record_answer(table, is_correct)

        if is_correct:
            self.total_coins += self.coins_per_answer

        return is_correct


class SoundcheckMode(GameMode):
    """Soundcheck mode - 25 questions with 6-second time limits."""

    def __init__(self, profile: Profile):
        super().__init__(profile)
        self.mode_name = "Soundcheck"
        self.total_questions = SOUNDCHECK_QUESTIONS
        self.time_per_question = SOUNDCHECK_TIME_LIMIT
        self.question_start_time = None
        self.coins_per_answer = STUDIO_COINS_PER_ANSWER

    def get_next_question(self):
        """Get next question."""
        if self.questions_answered >= self.total_questions:
            return None

        difficulty = self.profile.data["customization"].get("difficulty", "medium")
        self.current_question = self.question_gen.generate_multiplication(
            table=None,
            difficulty=difficulty
        )
        self.question_start_time = time.time()
        return self.current_question

    def submit_answer(self, answer: int) -> bool:
        """Submit answer and award coins if correct and within time."""
        is_correct = super().submit_answer(answer)

        # Check if answer was within time limit
        time_taken = time.time() - self.question_start_time
        within_time = time_taken <= self.time_per_question

        # Extract table from question
        num1, num2, _, _ = self.current_question
        table = min(num1, num2) if min(num1, num2) <= 12 else max(num1, num2)
        self.profile.record_answer(table, is_correct and within_time)

        if is_correct and within_time:
            self.total_coins += self.coins_per_answer

        return is_correct and within_time

    def get_time_remaining_for_question(self):
        """Get time remaining for current question."""
        if self.question_start_time is None:
            return self.time_per_question

        elapsed = time.time() - self.question_start_time
        return max(0, self.time_per_question - elapsed)

    def is_complete(self):
        """Check if all questions have been answered."""
        return self.questions_answered >= self.total_questions
