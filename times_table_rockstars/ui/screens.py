"""Game screens and UI layouts."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

from ui.widgets import (
    RockButton, QuestionDisplay, AnswerInput, ScoreDisplay,
    TimerDisplay, NumPad, FeedbackLabel, ProfileCard
)


class MenuScreen(Screen):
    """Main menu screen."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'menu'

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.main_layout)

    def on_pre_enter(self):
        """Refresh the screen when entering."""
        self.refresh_screen()

    def refresh_screen(self):
        """Refresh the menu screen with current user info."""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text="🎸 Times Table Rockstars 🎸",
            font_size='36sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='80dp'
        )
        self.main_layout.add_widget(title)

        # Profile card with switch user button
        profile_section = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height='220dp')

        profile_card = ProfileCard(self.game_engine.get_profile())
        profile_section.add_widget(profile_card)

        switch_user_btn = RockButton(text="👥 Switch Player")
        switch_user_btn.height = '50dp'
        switch_user_btn.background_color = get_color_from_hex("#444444")
        switch_user_btn.bind(on_press=self.go_to_user_select)
        profile_section.add_widget(switch_user_btn)

        self.main_layout.add_widget(profile_section)

        # Game mode buttons
        modes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        modes_layout.bind(minimum_height=modes_layout.setter('height'))

        garage_btn = RockButton(text="🏠 Garage Mode\nPractice Tables")
        garage_btn.bind(on_press=self.go_to_garage_select)
        modes_layout.add_widget(garage_btn)

        studio_btn = RockButton(text="🎬 Studio Mode\nSpeed Challenge")
        studio_btn.bind(on_press=self.go_to_studio)
        modes_layout.add_widget(studio_btn)

        jamming_btn = RockButton(text="🎵 Jamming Mode\nRelaxed Practice")
        jamming_btn.bind(on_press=self.go_to_jamming_select)
        modes_layout.add_widget(jamming_btn)

        soundcheck_btn = RockButton(text="🎤 Soundcheck\n25 Question Test")
        soundcheck_btn.bind(on_press=self.go_to_soundcheck)
        modes_layout.add_widget(soundcheck_btn)

        self.main_layout.add_widget(modes_layout)

        # Bottom buttons
        bottom_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='60dp')

        stats_btn = RockButton(text="📊 Stats")
        stats_btn.bind(on_press=self.go_to_stats)
        bottom_layout.add_widget(stats_btn)

        settings_btn = RockButton(text="⚙️ Settings")
        settings_btn.bind(on_press=self.go_to_settings)
        bottom_layout.add_widget(settings_btn)

        self.main_layout.add_widget(bottom_layout)

    def go_to_user_select(self, instance):
        """Go to user selection screen."""
        self.manager.current = 'user_select'

    def go_to_garage_select(self, instance):
        self.manager.current = 'garage_select'

    def go_to_studio(self, instance):
        self.manager.get_screen('gameplay').start_studio_mode()
        self.manager.current = 'gameplay'

    def go_to_jamming_select(self, instance):
        self.manager.current = 'jamming_select'

    def go_to_soundcheck(self, instance):
        self.manager.get_screen('gameplay').start_soundcheck_mode()
        self.manager.current = 'gameplay'

    def go_to_stats(self, instance):
        self.manager.current = 'stats'

    def go_to_settings(self, instance):
        self.manager.current = 'settings'


class GarageSelectScreen(Screen):
    """Screen to select which times table to practice in Garage mode."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'garage_select'

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(
            text="🏠 Garage Mode\nSelect Times Table",
            font_size='28sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='100dp'
        )
        layout.add_widget(title)

        # Table selection grid
        grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Auto-select weakest tables
        auto_btn = RockButton(text="🎯 Auto\n(Weakest Tables)")
        auto_btn.bind(on_press=lambda x: self.start_garage(None))
        grid.add_widget(auto_btn)

        # Individual table buttons (2-12)
        for i in range(2, 13):
            accuracy = self.game_engine.profile.get_table_accuracy(i)
            btn_text = f"{i} Times\n({accuracy:.0f}%)"

            btn = RockButton(text=btn_text)
            btn.bind(on_press=lambda x, table=i: self.start_garage(table))

            # Color code based on accuracy
            if accuracy >= 90:
                btn.background_color = get_color_from_hex("#2E8B57")  # Green
            elif accuracy >= 70:
                btn.background_color = get_color_from_hex("#FF8C00")  # Orange
            else:
                btn.background_color = get_color_from_hex("#8B0000")  # Red

            grid.add_widget(btn)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # Back button
        back_btn = RockButton(text="← Back to Menu")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def start_garage(self, table):
        self.manager.get_screen('gameplay').start_garage_mode(table)
        self.manager.current = 'gameplay'

    def go_back(self, instance):
        self.manager.current = 'menu'


class JammingSelectScreen(Screen):
    """Screen to configure Jamming mode."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'jamming_select'
        self.selected_tables = list(range(2, 13))
        self.operation = "mixed"

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(
            text="🎵 Jamming Mode\nConfigure Your Practice",
            font_size='28sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='100dp'
        )
        layout.add_widget(title)

        # Operation selection
        op_label = Label(
            text="Choose Operation:",
            font_size='20sp',
            size_hint_y=None,
            height='40dp'
        )
        layout.add_widget(op_label)

        op_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='60dp')

        mult_btn = RockButton(text="× Multiplication")
        mult_btn.bind(on_press=lambda x: self.set_operation("multiplication"))
        op_layout.add_widget(mult_btn)

        div_btn = RockButton(text="÷ Division")
        div_btn.bind(on_press=lambda x: self.set_operation("division"))
        op_layout.add_widget(div_btn)

        mixed_btn = RockButton(text="⚡ Mixed")
        mixed_btn.bind(on_press=lambda x: self.set_operation("mixed"))
        op_layout.add_widget(mixed_btn)

        layout.add_widget(op_layout)

        # Start button
        start_btn = RockButton(text="🚀 Start Jamming!")
        start_btn.bind(on_press=self.start_jamming)
        layout.add_widget(start_btn)

        # Back button
        back_btn = RockButton(text="← Back to Menu")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def set_operation(self, operation):
        self.operation = operation

    def start_jamming(self, instance):
        self.manager.get_screen('gameplay').start_jamming_mode(
            self.selected_tables, self.operation
        )
        self.manager.current = 'gameplay'

    def go_back(self, instance):
        self.manager.current = 'menu'


class GameplayScreen(Screen):
    """Main gameplay screen."""

    def __init__(self, game_engine, audio_manager, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.audio_manager = audio_manager
        self.name = 'gameplay'
        self.current_answer = ""
        self.update_event = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Timer display
        self.timer_display = TimerDisplay()
        layout.add_widget(self.timer_display)

        # Score display
        self.score_display = ScoreDisplay()
        layout.add_widget(self.score_display)

        # Question display
        self.question_display = QuestionDisplay()
        layout.add_widget(self.question_display)

        # Answer input
        answer_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height='100dp')
        answer_container.add_widget(Label(text="Your Answer:", size_hint_y=None, height='20dp'))
        self.answer_display = Label(
            text="",
            font_size='48sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='80dp'
        )
        answer_container.add_widget(self.answer_display)
        layout.add_widget(answer_container)

        # Feedback label
        self.feedback = FeedbackLabel()
        layout.add_widget(self.feedback)

        # Number pad
        self.numpad = NumPad(
            on_number_press=self.on_number_press,
            on_submit=self.on_submit,
            on_clear=self.on_clear
        )
        layout.add_widget(self.numpad)

        # Quit button
        quit_btn = RockButton(text="❌ Quit Game")
        quit_btn.bind(on_press=self.quit_game)
        layout.add_widget(quit_btn)

        self.add_widget(layout)

    def start_garage_mode(self, table):
        """Start a Garage mode game."""
        self.game_engine.start_garage_mode(table)
        self.start_game()

    def start_studio_mode(self):
        """Start a Studio mode game."""
        self.game_engine.start_studio_mode()
        self.start_game()

    def start_jamming_mode(self, tables, operation):
        """Start a Jamming mode game."""
        self.game_engine.start_jamming_mode(tables, operation)
        self.start_game()

    def start_soundcheck_mode(self):
        """Start a Soundcheck mode game."""
        self.game_engine.start_soundcheck_mode()
        self.start_game()

    def start_game(self):
        """Initialize and start the game."""
        self.current_answer = ""
        self.answer_display.text = ""
        self.load_next_question()

        # Start timer updates
        if self.update_event:
            self.update_event.cancel()
        self.update_event = Clock.schedule_interval(self.update_timer, 0.1)

    def load_next_question(self):
        """Load the next question."""
        mode = self.game_engine.get_current_mode()
        if mode is None:
            return

        question = mode.get_next_question()
        if question is None:
            self.end_game()
            return

        _, _, _, question_text = question
        self.question_display.set_question(question_text)
        self.current_answer = ""
        self.answer_display.text = ""
        self.update_score_display()

    def on_number_press(self, number):
        """Handle number button press."""
        self.current_answer += str(number)
        self.answer_display.text = self.current_answer

    def on_clear(self):
        """Clear the current answer."""
        self.current_answer = ""
        self.answer_display.text = ""

    def on_submit(self):
        """Submit the current answer."""
        if not self.current_answer:
            return

        try:
            answer = int(self.current_answer)
            mode = self.game_engine.get_current_mode()

            if mode is None:
                return

            is_correct = mode.submit_answer(answer)

            if is_correct:
                self.feedback.show_correct()
                self.audio_manager.play_correct()
            else:
                _, _, correct_answer, _ = mode.current_question
                self.feedback.show_incorrect(correct_answer)
                self.audio_manager.play_incorrect()

            self.update_score_display()

            # Check if game mode is complete
            if hasattr(mode, 'is_complete') and mode.is_complete():
                Clock.schedule_once(lambda dt: self.end_game(), 1.5)
            else:
                # Load next question after brief delay
                Clock.schedule_once(lambda dt: self.load_next_question(), 1.5)

        except ValueError:
            pass

    def update_timer(self, dt):
        """Update the timer display."""
        mode = self.game_engine.get_current_mode()
        if mode is None:
            return

        # Update based on mode type
        if hasattr(mode, 'is_time_up') and mode.is_time_up():
            self.end_game()
        elif hasattr(mode, 'get_time_remaining_for_question'):
            time_remaining = mode.get_time_remaining_for_question()
            self.timer_display.update_countdown(time_remaining)
            if time_remaining <= 0:
                # Time's up for this question, submit as incorrect
                self.on_submit() if self.current_answer else self.load_next_question()
        else:
            elapsed = mode.get_elapsed_time()
            self.timer_display.update_time(elapsed)

    def update_score_display(self):
        """Update the score display."""
        mode = self.game_engine.get_current_mode()
        if mode is None:
            return

        self.score_display.update(
            mode.total_coins,
            mode.get_accuracy(),
            mode.questions_answered
        )

    def end_game(self):
        """End the game and show results."""
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

        results = self.game_engine.finish_current_mode()
        self.manager.get_screen('results').show_results(results)
        self.manager.current = 'results'

    def quit_game(self, instance):
        """Quit the current game."""
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

        self.game_engine.finish_current_mode()
        self.manager.current = 'menu'


class ResultsScreen(Screen):
    """Results screen shown after completing a game."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'results'

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.layout)

    def show_results(self, results):
        """Display game results."""
        self.layout.clear_widgets()

        # Title
        title = Label(
            text="🎉 Game Complete! 🎉",
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='80dp'
        )
        self.layout.add_widget(title)

        # Results
        results_text = f"""
Mode: {results['mode']}
Questions: {results['questions']}
Correct: {results['correct']}
Accuracy: {results['accuracy']:.1f}%
Coins Earned: {results['coins']}
Duration: {int(results['duration'])}s
"""

        if 'speed' in results:
            results_text += f"\nSpeed: {results['speed']:.1f} questions/min"

        results_label = Label(
            text=results_text,
            font_size='20sp',
            color=get_color_from_hex("#FFFFFF")
        )
        self.layout.add_widget(results_label)

        # Updated profile stats
        stats = self.game_engine.get_statistics()
        stats_text = f"""
Rock Status: {stats['rock_status']}
Total Coins: {stats['total_coins']}
Overall Accuracy: {stats['overall_accuracy']:.1f}%
"""
        stats_label = Label(
            text=stats_text,
            font_size='18sp',
            color=get_color_from_hex("#FFD700")
        )
        self.layout.add_widget(stats_label)

        # Buttons
        play_again_btn = RockButton(text="🔄 Play Again")
        play_again_btn.bind(on_press=self.play_again)
        self.layout.add_widget(play_again_btn)

        menu_btn = RockButton(text="🏠 Main Menu")
        menu_btn.bind(on_press=self.go_to_menu)
        self.layout.add_widget(menu_btn)

    def play_again(self, instance):
        self.manager.current = 'menu'

    def go_to_menu(self, instance):
        self.manager.current = 'menu'


class StatsScreen(Screen):
    """Statistics screen."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'stats'

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(
            text="📊 Your Statistics",
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='60dp'
        )
        layout.add_widget(title)

        # Stats content (will be updated on enter)
        self.stats_content = BoxLayout(orientation='vertical', spacing=10)
        scroll = ScrollView()
        scroll.add_widget(self.stats_content)
        layout.add_widget(scroll)

        # Back button
        back_btn = RockButton(text="← Back to Menu")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        """Update stats when screen is entered."""
        self.stats_content.clear_widgets()

        stats = self.game_engine.get_statistics()

        # Overall stats
        overall_text = f"""
Rock Name: {stats['rock_name']}
Rock Status: {stats['rock_status']}

Total Coins: {stats['total_coins']}
Total Questions: {stats['total_questions']}
Overall Accuracy: {stats['overall_accuracy']:.1f}%

Studio Speed: {stats['studio_speed']:.1f} q/min
Best Studio Speed: {stats['best_studio_speed']:.1f} q/min
"""

        overall_label = Label(
            text=overall_text,
            font_size='18sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height='250dp'
        )
        self.stats_content.add_widget(overall_label)

        # Times table performance
        table_title = Label(
            text="Times Table Performance:",
            font_size='20sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='40dp'
        )
        self.stats_content.add_widget(table_title)

        performance = self.game_engine.get_table_performance()
        for table in range(2, 13):
            accuracy = performance.get(table, 0)
            table_label = Label(
                text=f"{table} times table: {accuracy:.1f}%",
                font_size='16sp',
                color=get_color_from_hex("#FFFFFF"),
                size_hint_y=None,
                height='30dp'
            )
            self.stats_content.add_widget(table_label)

    def go_back(self, instance):
        self.manager.current = 'menu'


class SettingsScreen(Screen):
    """Settings and customization screen."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'settings'

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(
            text="⚙️ Settings",
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='60dp'
        )
        layout.add_widget(title)

        # Settings content
        settings_scroll = ScrollView()
        settings_content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        settings_content.bind(minimum_height=settings_content.setter('height'))

        # Profile name
        from kivy.uix.textinput import TextInput
        name_label = Label(text="Rock Star Name:", size_hint_y=None, height='30dp')
        settings_content.add_widget(name_label)

        self.name_input = TextInput(
            text=self.game_engine.profile.data["rock_name"],
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        settings_content.add_widget(self.name_input)

        save_name_btn = RockButton(text="Save Name")
        save_name_btn.bind(on_press=self.save_name)
        settings_content.add_widget(save_name_btn)

        # Theme selection
        theme_label = Label(
            text="Color Theme:",
            size_hint_y=None,
            height='40dp',
            font_size='20sp'
        )
        settings_content.add_widget(theme_label)

        themes = ["rock", "ocean", "forest", "sunset"]
        for theme in themes:
            theme_btn = RockButton(text=f"{theme.capitalize()} Theme")
            theme_btn.bind(on_press=lambda x, t=theme: self.set_theme(t))
            settings_content.add_widget(theme_btn)

        # Avatar customization button
        avatar_btn = RockButton(text="🖼️ Customize Avatar")
        avatar_btn.bind(on_press=self.customize_avatar)
        settings_content.add_widget(avatar_btn)

        settings_scroll.add_widget(settings_content)
        layout.add_widget(settings_scroll)

        # Back button
        back_btn = RockButton(text="← Back to Menu")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def save_name(self, instance):
        """Save the updated rock star name."""
        new_name = self.name_input.text.strip()
        if new_name:
            self.game_engine.update_profile_name(new_name)

    def set_theme(self, theme):
        """Set a new color theme."""
        self.game_engine.update_theme(theme)

    def customize_avatar(self, instance):
        """Go to avatar customization."""
        self.manager.current = 'avatar_custom'

    def go_back(self, instance):
        self.manager.current = 'menu'


class AvatarCustomizationScreen(Screen):
    """Screen for customizing avatar with online images."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'avatar_custom'

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title = Label(
            text="🖼️ Customize Your Avatar",
            font_size='28sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='60dp'
        )
        layout.add_widget(title)

        # Instructions
        instructions = Label(
            text="Enter an image URL to use as your avatar:",
            font_size='16sp',
            size_hint_y=None,
            height='40dp'
        )
        layout.add_widget(instructions)

        # URL input
        from kivy.uix.textinput import TextInput
        self.url_input = TextInput(
            hint_text="https://example.com/image.jpg",
            multiline=False,
            size_hint_y=None,
            height='50dp'
        )
        layout.add_widget(self.url_input)

        # Load button
        load_btn = RockButton(text="📥 Load Image")
        load_btn.bind(on_press=self.load_image)
        layout.add_widget(load_btn)

        # Preview
        self.preview = Image(size_hint=(1, 0.5))
        layout.add_widget(self.preview)

        # Save button
        save_btn = RockButton(text="💾 Save Avatar")
        save_btn.bind(on_press=self.save_avatar)
        layout.add_widget(save_btn)

        # Back button
        back_btn = RockButton(text="← Back to Settings")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def load_image(self, instance):
        """Load image from URL."""
        url = self.url_input.text.strip()
        if url:
            try:
                self.preview.source = url
                self.preview.reload()
            except Exception as e:
                print(f"Error loading image: {e}")

    def save_avatar(self, instance):
        """Save the avatar image."""
        url = self.url_input.text.strip()
        if url:
            self.game_engine.update_avatar(url)

    def go_back(self, instance):
        self.manager.current = 'settings'
