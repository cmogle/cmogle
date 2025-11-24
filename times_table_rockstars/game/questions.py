"""Question generation for times tables."""

import random
from typing import Tuple, List


class QuestionGenerator:
    """Generates times table questions."""

    def __init__(self):
        self.tables = list(range(2, 13))  # 2-12 times tables
        self.difficulty_ranges = {
            "easy": (2, 5),    # 2-5 times tables
            "medium": (2, 10),  # 2-10 times tables
            "hard": (2, 12),    # 2-12 times tables
        }

    def generate_multiplication(self, table=None, difficulty="medium"):
        """Generate a multiplication question.

        Args:
            table: Specific times table (2-12), or None for random
            difficulty: "easy", "medium", or "hard"

        Returns:
            Tuple of (num1, num2, answer, question_text)
        """
        min_table, max_table = self.difficulty_ranges.get(difficulty, (2, 10))

        if table is None:
            num1 = random.randint(min_table, max_table)
        else:
            num1 = table

        num2 = random.randint(2, 12)
        answer = num1 * num2

        # Randomly swap for variety
        if random.random() > 0.5:
            num1, num2 = num2, num1

        question_text = f"{num1} × {num2}"
        return num1, num2, answer, question_text

    def generate_division(self, table=None, difficulty="medium"):
        """Generate a division question.

        Args:
            table: Specific times table (2-12), or None for random
            difficulty: "easy", "medium", or "hard"

        Returns:
            Tuple of (dividend, divisor, answer, question_text)
        """
        min_table, max_table = self.difficulty_ranges.get(difficulty, (2, 10))

        if table is None:
            divisor = random.randint(min_table, max_table)
        else:
            divisor = table

        answer = random.randint(2, 12)
        dividend = divisor * answer

        question_text = f"{dividend} ÷ {divisor}"
        return dividend, divisor, answer, question_text

    def generate_mixed(self, table=None, difficulty="medium"):
        """Generate a random multiplication or division question."""
        if random.random() > 0.5:
            return self.generate_multiplication(table, difficulty)
        else:
            return self.generate_division(table, difficulty)

    def generate_batch(self, count, mode="mixed", table=None, difficulty="medium"):
        """Generate a batch of questions.

        Args:
            count: Number of questions to generate
            mode: "multiplication", "division", or "mixed"
            table: Specific times table or None
            difficulty: "easy", "medium", or "hard"

        Returns:
            List of question tuples
        """
        questions = []
        for _ in range(count):
            if mode == "multiplication":
                questions.append(self.generate_multiplication(table, difficulty))
            elif mode == "division":
                questions.append(self.generate_division(table, difficulty))
            else:
                questions.append(self.generate_mixed(table, difficulty))
        return questions

    def get_adaptive_difficulty(self, recent_scores):
        """Adjust difficulty based on recent performance.

        Args:
            recent_scores: List of recent accuracy percentages

        Returns:
            Adjusted difficulty level
        """
        if not recent_scores:
            return "medium"

        avg_score = sum(recent_scores) / len(recent_scores)

        if avg_score >= 90:
            return "hard"
        elif avg_score >= 70:
            return "medium"
        else:
            return "easy"

    def get_weak_tables(self, performance_data):
        """Identify weak times tables from performance data.

        Args:
            performance_data: Dict mapping table numbers to accuracy percentages

        Returns:
            List of table numbers that need practice
        """
        weak_tables = []
        for table, accuracy in performance_data.items():
            if accuracy < 70:
                weak_tables.append(table)

        # If no weak tables, return random selection
        if not weak_tables:
            return random.sample(self.tables, min(3, len(self.tables)))

        return weak_tables
