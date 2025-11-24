"""User management screens."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex

from ui.widgets import RockButton


class UserSelectionScreen(Screen):
    """Screen to select or create users."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'user_select'

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.main_layout)

    def on_pre_enter(self):
        """Update the user list when entering the screen."""
        self.refresh_user_list()

    def refresh_user_list(self):
        """Refresh the list of users."""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text="👥 Select Player",
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='80dp'
        )
        self.main_layout.add_widget(title)

        # User list
        users_scroll = ScrollView(size_hint=(1, 1))
        users_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        users_layout.bind(minimum_height=users_layout.setter('height'))

        profiles = self.game_engine.get_profile_manager().get_all_profiles()

        for profile_info in profiles:
            user_btn = self.create_user_button(profile_info)
            users_layout.add_widget(user_btn)

        users_scroll.add_widget(users_layout)
        self.main_layout.add_widget(users_scroll)

        # Action buttons
        actions_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height='60dp'
        )

        new_user_btn = RockButton(text="➕ New Player")
        new_user_btn.bind(on_press=self.show_create_user_dialog)
        actions_layout.add_widget(new_user_btn)

        manage_btn = RockButton(text="⚙️ Manage")
        manage_btn.bind(on_press=self.go_to_manage)
        actions_layout.add_widget(manage_btn)

        self.main_layout.add_widget(actions_layout)

    def create_user_button(self, profile_info):
        """Create a button for a user profile."""
        user_id = profile_info['user_id']
        name = profile_info['name']
        rock_name = profile_info['rock_name']
        is_current = profile_info['is_current']

        # Get stats for this user
        pm = self.game_engine.get_profile_manager()
        stats = pm.get_profile_stats_summary(user_id)

        button_text = f"{'★ ' if is_current else ''}{name}\n"
        button_text += f"🎸 {rock_name}\n"
        button_text += f"Status: {stats['rock_status']} | Coins: {stats['total_coins']}"

        btn = RockButton(text=button_text)
        btn.height = '100dp'

        if is_current:
            btn.background_color = get_color_from_hex("#2E8B57")  # Green for current

        btn.bind(on_press=lambda x: self.select_user(user_id))
        return btn

    def select_user(self, user_id):
        """Select a user and go to main menu."""
        if self.game_engine.switch_user(user_id):
            self.manager.current = 'menu'

    def show_create_user_dialog(self, instance):
        """Show dialog to create a new user."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        content.add_widget(Label(
            text="Enter player name:",
            size_hint_y=None,
            height='30dp'
        ))

        name_input = TextInput(
            hint_text="Player Name",
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(name_input)

        buttons = BoxLayout(spacing=10, size_hint_y=None, height='50dp')

        def create_user(instance):
            name = name_input.text.strip()
            if name:
                pm = self.game_engine.get_profile_manager()
                user_id = pm.create_profile(name)
                self.game_engine.switch_user(user_id)
                popup.dismiss()
                self.refresh_user_list()

        create_btn = RockButton(text="Create")
        create_btn.bind(on_press=create_user)
        buttons.add_widget(create_btn)

        cancel_btn = RockButton(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        buttons.add_widget(cancel_btn)

        content.add_widget(buttons)

        popup = Popup(
            title='Create New Player',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def go_to_manage(self, instance):
        """Go to profile management screen."""
        self.manager.current = 'profile_manage'


class ProfileManageScreen(Screen):
    """Screen to manage user profiles."""

    def __init__(self, game_engine, **kwargs):
        super().__init__(**kwargs)
        self.game_engine = game_engine
        self.name = 'profile_manage'

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.main_layout)

    def on_pre_enter(self):
        """Update the profile list when entering the screen."""
        self.refresh_profile_list()

    def refresh_profile_list(self):
        """Refresh the list of profiles."""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text="⚙️ Manage Players",
            font_size='32sp',
            bold=True,
            color=get_color_from_hex("#FFD700"),
            size_hint_y=None,
            height='60dp'
        )
        self.main_layout.add_widget(title)

        # Profile list
        profiles_scroll = ScrollView(size_hint=(1, 1))
        profiles_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        profiles_layout.bind(minimum_height=profiles_layout.setter('height'))

        profiles = self.game_engine.get_profile_manager().get_all_profiles()

        for profile_info in profiles:
            profile_card = self.create_profile_card(profile_info)
            profiles_layout.add_widget(profile_card)

        profiles_scroll.add_widget(profiles_layout)
        self.main_layout.add_widget(profiles_scroll)

        # Back button
        back_btn = RockButton(text="← Back")
        back_btn.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_btn)

    def create_profile_card(self, profile_info):
        """Create a card showing profile info and management options."""
        user_id = profile_info['user_id']
        name = profile_info['name']
        rock_name = profile_info['rock_name']
        is_current = profile_info['is_current']

        pm = self.game_engine.get_profile_manager()
        stats = pm.get_profile_stats_summary(user_id)

        card = BoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint_y=None,
            height='180dp',
            padding=10
        )

        # Info
        info_text = f"{'★ ' if is_current else ''}{name}\n"
        info_text += f"🎸 {rock_name}\n"
        info_text += f"Status: {stats['rock_status']}\n"
        info_text += f"Coins: {stats['total_coins']} | "
        info_text += f"Games: {stats['games_played']} | "
        info_text += f"Accuracy: {stats['overall_accuracy']:.1f}%"

        info_label = Label(
            text=info_text,
            font_size='16sp',
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height='80dp'
        )
        card.add_widget(info_label)

        # Action buttons
        actions = BoxLayout(spacing=5, size_hint_y=None, height='50dp')

        rename_btn = RockButton(text="✏️ Rename")
        rename_btn.bind(on_press=lambda x: self.show_rename_dialog(user_id, name))
        actions.add_widget(rename_btn)

        reset_btn = RockButton(text="🔄 Reset Stats")
        reset_btn.bind(on_press=lambda x: self.show_reset_confirm(user_id, name))
        actions.add_widget(reset_btn)

        # Only show delete if not the last profile
        if len(pm.get_all_profiles()) > 1:
            delete_btn = RockButton(text="🗑️ Delete")
            delete_btn.background_color = get_color_from_hex("#8B0000")
            delete_btn.bind(on_press=lambda x: self.show_delete_confirm(user_id, name))
            actions.add_widget(delete_btn)

        card.add_widget(actions)

        return card

    def show_rename_dialog(self, user_id, current_name):
        """Show dialog to rename a profile."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        content.add_widget(Label(
            text=f"Rename '{current_name}':",
            size_hint_y=None,
            height='30dp'
        ))

        name_input = TextInput(
            text=current_name,
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(name_input)

        buttons = BoxLayout(spacing=10, size_hint_y=None, height='50dp')

        def rename(instance):
            new_name = name_input.text.strip()
            if new_name:
                pm = self.game_engine.get_profile_manager()
                pm.rename_profile(user_id, new_name)
                popup.dismiss()
                self.refresh_profile_list()

        rename_btn = RockButton(text="Rename")
        rename_btn.bind(on_press=rename)
        buttons.add_widget(rename_btn)

        cancel_btn = RockButton(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        buttons.add_widget(cancel_btn)

        content.add_widget(buttons)

        popup = Popup(
            title='Rename Player',
            content=content,
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def show_reset_confirm(self, user_id, name):
        """Show confirmation dialog for resetting statistics."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        content.add_widget(Label(
            text=f"Reset all statistics for '{name}'?\n\n"
                 "This will clear:\n"
                 "• All coins\n"
                 "• Game history\n"
                 "• Times table progress\n"
                 "• Rock status\n\n"
                 "Name and customization will be kept.",
            size_hint_y=None,
            height='200dp'
        ))

        buttons = BoxLayout(spacing=10, size_hint_y=None, height='50dp')

        def reset(instance):
            pm = self.game_engine.get_profile_manager()
            pm.reset_profile_stats(user_id)
            # Reload profile if it's the current user
            if pm.current_user_id == user_id:
                self.game_engine.profile = pm.get_current_profile()
            popup.dismiss()
            self.refresh_profile_list()

        reset_btn = RockButton(text="Reset Statistics")
        reset_btn.background_color = get_color_from_hex("#FF8C00")
        reset_btn.bind(on_press=reset)
        buttons.add_widget(reset_btn)

        cancel_btn = RockButton(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        buttons.add_widget(cancel_btn)

        content.add_widget(buttons)

        popup = Popup(
            title='Confirm Reset',
            content=content,
            size_hint=(0.8, 0.5)
        )
        popup.open()

    def show_delete_confirm(self, user_id, name):
        """Show confirmation dialog for deleting a profile."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        content.add_widget(Label(
            text=f"Delete player '{name}'?\n\n"
                 "This cannot be undone!\n"
                 "All data will be permanently lost.",
            size_hint_y=None,
            height='150dp'
        ))

        buttons = BoxLayout(spacing=10, size_hint_y=None, height='50dp')

        def delete(instance):
            pm = self.game_engine.get_profile_manager()
            pm.delete_profile(user_id)
            # If we deleted the current user, switch to the new current user
            self.game_engine.profile = pm.get_current_profile()
            popup.dismiss()
            self.refresh_profile_list()

        delete_btn = RockButton(text="Delete Player")
        delete_btn.background_color = get_color_from_hex("#8B0000")
        delete_btn.bind(on_press=delete)
        buttons.add_widget(delete_btn)

        cancel_btn = RockButton(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        buttons.add_widget(cancel_btn)

        content.add_widget(buttons)

        popup = Popup(
            title='Confirm Delete',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def go_back(self, instance):
        """Go back to user selection."""
        self.manager.current = 'user_select'
