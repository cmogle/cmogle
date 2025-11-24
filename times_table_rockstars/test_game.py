"""
Test script for Times Table Rockstars
Run this to verify game logic without the GUI
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from game.core import GameEngine
from game.questions import QuestionGenerator


def test_question_generation():
    """Test question generation."""
    print("🎸 Testing Question Generation...")
    qgen = QuestionGenerator()

    # Test multiplication
    num1, num2, answer, question = qgen.generate_multiplication(table=7)
    print(f"  Multiplication: {question} = {answer}")
    assert answer == num1 * num2, "Multiplication calculation error"

    # Test division
    dividend, divisor, answer, question = qgen.generate_division(table=6)
    print(f"  Division: {question} = {answer}")
    assert dividend == divisor * answer, "Division calculation error"

    # Test batch generation
    questions = qgen.generate_batch(5, mode="mixed", difficulty="medium")
    print(f"  Generated batch of {len(questions)} questions")
    assert len(questions) == 5, "Batch generation error"

    print("  ✓ Question generation working!\n")


def test_profile():
    """Test profile management."""
    print("🎸 Testing Profile System...")
    engine = GameEngine()
    profile = engine.get_profile()

    print(f"  Rock Name: {profile.data['rock_name']}")
    print(f"  Total Coins: {profile.data['total_coins']}")

    # Test adding coins
    initial_coins = profile.data['total_coins']
    profile.add_coins(50)
    assert profile.data['total_coins'] == initial_coins + 50, "Coin addition error"
    print(f"  Added 50 coins, now have: {profile.data['total_coins']}")

    # Test recording answers
    profile.record_answer(7, True)
    profile.record_answer(7, False)
    profile.record_answer(7, True)

    accuracy = profile.get_table_accuracy(7)
    print(f"  7 times table accuracy: {accuracy:.1f}%")
    # Check accuracy is approximately 66.67% (2 out of 3 correct)
    assert 66.0 <= accuracy <= 67.0, "Accuracy calculation error"

    print("  ✓ Profile system working!\n")


def test_game_modes():
    """Test game modes."""
    print("🎸 Testing Game Modes...")
    engine = GameEngine()

    # Test Garage Mode
    print("  Testing Garage Mode...")
    garage = engine.start_garage_mode(table=5)
    question = garage.get_next_question()
    _, _, correct_answer, question_text = question
    print(f"    Question: {question_text} = {correct_answer}")

    is_correct = garage.submit_answer(correct_answer)
    assert is_correct, "Garage mode answer check failed"
    print(f"    Correct! Coins earned: {garage.total_coins}")

    # Test Studio Mode
    print("  Testing Studio Mode...")
    studio = engine.start_studio_mode()
    question = studio.get_next_question()
    _, _, correct_answer, question_text = question
    print(f"    Question: {question_text} = {correct_answer}")

    is_correct = studio.submit_answer(correct_answer)
    assert is_correct, "Studio mode answer check failed"
    print(f"    Correct! Coins earned: {studio.total_coins}")

    # Test Jamming Mode
    print("  Testing Jamming Mode...")
    jamming = engine.start_jamming_mode(tables=[3, 4, 5], operation="multiplication")
    question = jamming.get_next_question()
    _, _, correct_answer, question_text = question
    print(f"    Question: {question_text} = {correct_answer}")

    is_correct = jamming.submit_answer(correct_answer)
    assert is_correct, "Jamming mode answer check failed"
    print(f"    Correct!")

    # Test Soundcheck Mode
    print("  Testing Soundcheck Mode...")
    soundcheck = engine.start_soundcheck_mode()
    question = soundcheck.get_next_question()
    _, _, correct_answer, question_text = question
    print(f"    Question: {question_text} = {correct_answer}")

    is_correct = soundcheck.submit_answer(correct_answer)
    print(f"    Answer submitted: {is_correct}")

    print("  ✓ All game modes working!\n")


def test_statistics():
    """Test statistics tracking."""
    print("🎸 Testing Statistics...")
    engine = GameEngine()

    stats = engine.get_statistics()
    print(f"  Rock Name: {stats['rock_name']}")
    print(f"  Rock Status: {stats['rock_status']}")
    print(f"  Total Coins: {stats['total_coins']}")
    print(f"  Total Questions: {stats['total_questions']}")
    print(f"  Overall Accuracy: {stats['overall_accuracy']:.1f}%")

    performance = engine.get_table_performance()
    print("  Times table performance:")
    for table in range(2, 13):
        accuracy = performance[table]
        print(f"    {table} times: {accuracy:.1f}%")

    print("  ✓ Statistics working!\n")


def test_customization():
    """Test customization features."""
    print("🎸 Testing Customization...")
    engine = GameEngine()

    # Test name change
    original_name = engine.profile.data['rock_name']
    engine.update_profile_name("Test Rocker")
    assert engine.profile.data['rock_name'] == "Test Rocker", "Name update failed"
    print(f"  Changed name from '{original_name}' to 'Test Rocker'")

    # Change back
    engine.update_profile_name(original_name)

    # Test theme change
    engine.update_theme("ocean")
    assert engine.settings.get("theme") == "ocean", "Theme update failed"
    print(f"  Changed theme to 'ocean'")

    # Test avatar
    test_url = "https://example.com/avatar.jpg"
    engine.update_avatar(test_url)
    assert engine.profile.data['customization']['avatar_image'] == test_url, "Avatar update failed"
    print(f"  Set avatar URL")

    print("  ✓ Customization working!\n")


def simulate_game_session():
    """Simulate a complete game session."""
    print("🎸 Simulating Complete Game Session...")
    engine = GameEngine()

    # Start a garage mode session
    mode = engine.start_garage_mode(table=8)
    print(f"  Playing Garage Mode (8 times table)")

    # Answer 10 questions
    for i in range(10):
        question = mode.get_next_question()
        _, _, correct_answer, question_text = question

        # Simulate 80% accuracy
        import random
        user_answer = correct_answer if random.random() < 0.8 else (correct_answer + 1)

        is_correct = mode.submit_answer(user_answer)
        print(f"    Q{i+1}: {question_text} = {user_answer} {'✓' if is_correct else '✗ (correct: ' + str(correct_answer) + ')'}")

    # Finish the game
    results = mode.finish()
    print(f"\n  Game Complete!")
    print(f"    Questions: {results['questions']}")
    print(f"    Correct: {results['correct']}")
    print(f"    Accuracy: {results['accuracy']:.1f}%")
    print(f"    Coins Earned: {results['coins']}")
    print(f"    Duration: {results['duration']:.1f}s")

    print("  ✓ Game session simulation complete!\n")


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("   TIMES TABLE ROCKSTARS - TEST SUITE")
    print("="*50 + "\n")

    try:
        test_question_generation()
        test_profile()
        test_game_modes()
        test_statistics()
        test_customization()
        simulate_game_session()

        print("="*50)
        print("   ✅ ALL TESTS PASSED!")
        print("="*50)
        print("\nThe game logic is working correctly!")
        print("Run 'python main.py' to start the GUI version.\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
