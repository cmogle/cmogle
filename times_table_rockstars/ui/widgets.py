"""Custom UI widgets."""

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.utils import get_color_from_hex


class RockButton(Button):
    """Styled button with rock theme."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex("#8B0000")
        self.color = get_color_from_hex("#FFD700")
        self.bold = True
        self.font_size = '20sp'
        self.size_hint_y = None
        self.height = '60dp'

        # Bind for press animation
        self.bind(on_press=self._on_press_anim)
        self.bind(on_release=self._on_release_anim)

    def _on_press_anim(self, instance):
        """Animate button press."""
        anim = Animation(opacity=0.7, duration=0.1)
        anim.start(self)

    def _on_release_anim(self, instance):
        """Animate button release."""
        anim = Animation(opacity=1.0, duration=0.1)
        anim.start(self)


class QuestionDisplay(Label):
    """Large label for displaying questions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '48sp'
        self.bold = True
        self.color = get_color_from_hex("#FFD700")
        self.halign = 'center'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = '100dp'

    def set_question(self, question_text):
        """Set the question text."""
        self.text = question_text


class AnswerInput(TextInput):
    """Styled text input for answers."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.input_filter = 'int'
        self.font_size = '36sp'
        self.halign = 'center'
        self.size_hint = (0.6, None)
        self.height = '80dp'
        self.background_color = get_color_from_hex("#333333")
        self.foreground_color = get_color_from_hex("#FFFFFF")
        self.cursor_color = get_color_from_hex("#FFD700")
        self.hint_text = "Enter answer"
        self.hint_text_color = get_color_from_hex("#888888")


class ScoreDisplay(BoxLayout):
    """Widget to display score information."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = '50dp'
        self.padding = 10
        self.spacing = 20

        # Coins display
        self.coins_label = Label(
            text="Coins: 0",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#FFD700")
        )

        # Accuracy display
        self.accuracy_label = Label(
            text="Accuracy: 0%",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#FFFFFF")
        )

        # Questions display
        self.questions_label = Label(
            text="Questions: 0",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#FFFFFF")
        )

        self.add_widget(self.coins_label)
        self.add_widget(self.accuracy_label)
        self.add_widget(self.questions_label)

    def update(self, coins, accuracy, questions):
        """Update the score display."""
        self.coins_label.text = f"🪙 {coins}"
        self.accuracy_label.text = f"✓ {accuracy:.1f}%"
        self.questions_label.text = f"Q: {questions}"


class TimerDisplay(Label):
    """Timer display widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '24sp'
        self.bold = True
        self.color = get_color_from_hex("#FFD700")
        self.size_hint_y = None
        self.height = '40dp'

    def update_time(self, seconds):
        """Update the timer display."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        self.text = f"⏱ {minutes:02d}:{secs:02d}"

    def update_countdown(self, seconds):
        """Update as a countdown."""
        self.text = f"⏱ {seconds:.1f}s"

        # Change color based on time remaining
        if seconds < 2:
            self.color = get_color_from_hex("#FF0000")  # Red
        elif seconds < 4:
            self.color = get_color_from_hex("#FF8C00")  # Orange
        else:
            self.color = get_color_from_hex("#FFD700")  # Gold


class NumPad(GridLayout):
    """On-screen number pad for mobile devices."""

    def __init__(self, on_number_press, on_submit, on_clear, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = 5
        self.padding = 10
        self.size_hint = (0.8, None)
        self.height = '300dp'

        self.on_number_press = on_number_press
        self.on_submit = on_submit
        self.on_clear = on_clear

        # Create number buttons (1-9)
        for i in range(1, 10):
            btn = Button(
                text=str(i),
                font_size='28sp',
                bold=True,
                background_color=get_color_from_hex("#444444"),
                color=get_color_from_hex("#FFFFFF")
            )
            btn.bind(on_press=lambda x, num=i: self.on_number_press(num))
            self.add_widget(btn)

        # Clear button
        clear_btn = Button(
            text="Clear",
            font_size='24sp',
            bold=True,
            background_color=get_color_from_hex("#8B0000"),
            color=get_color_from_hex("#FFFFFF")
        )
        clear_btn.bind(on_press=lambda x: self.on_clear())
        self.add_widget(clear_btn)

        # Zero button
        zero_btn = Button(
            text="0",
            font_size='28sp',
            bold=True,
            background_color=get_color_from_hex("#444444"),
            color=get_color_from_hex("#FFFFFF")
        )
        zero_btn.bind(on_press=lambda x: self.on_number_press(0))
        self.add_widget(zero_btn)

        # Submit button
        submit_btn = Button(
            text="Submit",
            font_size='24sp',
            bold=True,
            background_color=get_color_from_hex("#2E8B57"),
            color=get_color_from_hex("#FFFFFF")
        )
        submit_btn.bind(on_press=lambda x: self.on_submit())
        self.add_widget(submit_btn)


class FeedbackLabel(Label):
    """Label for showing feedback (correct/incorrect)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '32sp'
        self.bold = True
        self.size_hint_y = None
        self.height = '60dp'
        self.opacity = 0

    def show_correct(self):
        """Show correct feedback."""
        self.text = "✓ Correct! 🎸"
        self.color = get_color_from_hex("#00FF00")
        self._animate_feedback()

    def show_incorrect(self, correct_answer):
        """Show incorrect feedback."""
        self.text = f"✗ Incorrect! Answer: {correct_answer}"
        self.color = get_color_from_hex("#FF0000")
        self._animate_feedback()

    def _animate_feedback(self):
        """Animate the feedback appearance."""
        self.opacity = 1
        anim = Animation(opacity=0, duration=1.5)
        anim.start(self)


class ProfileCard(BoxLayout):
    """Widget to display profile information."""

    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.size_hint_y = None
        self.height = '200dp'

        stats = profile.get_statistics()

        # Rock name
        self.add_widget(Label(
            text=f"🎸 {stats['rock_name']}",
            font_size='28sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='40dp'
        ))

        # Rock status
        self.add_widget(Label(
            text=f"Status: {stats['rock_status']}",
            font_size='20sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height='30dp'
        ))

        # Coins
        self.add_widget(Label(
            text=f"🪙 Total Coins: {stats['total_coins']}",
            font_size='20sp',
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='30dp'
        ))

        # Overall accuracy
        self.add_widget(Label(
            text=f"Overall Accuracy: {stats['overall_accuracy']:.1f}%",
            font_size='18sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height='30dp'
        ))

        # Studio speed
        if stats['studio_speed'] > 0:
            self.add_widget(Label(
                text=f"Studio Speed: {stats['studio_speed']:.1f} q/min",
                font_size='18sp',
                color=get_color_from_hex("#FFFFFF"),
                size_hint_y=None,
                height='30dp'
            ))
