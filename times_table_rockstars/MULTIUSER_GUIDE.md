# Multi-User Guide

Times Table Rockstars now supports multiple players! Perfect for families with multiple children.

## 🎮 Features

### Multiple Players
- Create unlimited player profiles
- Each player has independent progress and statistics
- Switch between players anytime
- Persistent storage for all users

### Profile Management
- ➕ **Create** new players
- ✏️ **Rename** players
- 🔄 **Reset statistics** (keeps name and customization)
- 🗑️ **Delete** players (cannot delete the last one)
- 👥 **Switch** between players

## 📖 How to Use

### First Time Setup
When you first launch the app:
1. A default player profile is automatically created
2. You'll see the main menu with your rock star name

### Adding New Players

**From Main Menu:**
1. Tap "👥 Switch Player"
2. Tap "➕ New Player"
3. Enter the player's name
4. Tap "Create"

**From User Selection:**
1. Launch the app (if multiple users exist)
2. Tap "➕ New Player"
3. Enter name and tap "Create"

### Switching Players

**From Main Menu:**
1. Tap "👥 Switch Player"
2. Tap on the player you want to use
3. You'll return to the main menu as that player

**At Startup:**
- If you have multiple players, the user selection screen shows automatically
- Select your player to continue

### Managing Players

**From User Selection Screen:**
1. Tap "⚙️ Manage"
2. You'll see all players with their stats

**Available Actions:**

#### ✏️ Rename Player
- Change a player's display name
- Rock star name stays the same (can change in Settings)

#### 🔄 Reset Statistics
- Clears all game progress and statistics
- Keeps the player's name and customization
- Use this to start fresh
- **What gets reset:**
  - All coins
  - Game history
  - Times table progress
  - Rock status (back to "Wannabe")
- **What's preserved:**
  - Player name
  - Rock star name
  - Avatar image
  - Color theme preferences

#### 🗑️ Delete Player
- Permanently removes a player profile
- **Cannot be undone!**
- Cannot delete if it's the only player
- If you delete the current player, automatically switches to another

## 💾 Data Storage

### Profile Files
Each player's data is stored separately:
```
data/
├── profiles/
│   ├── abc123def.json    # Player 1 data
│   ├── xyz789ghi.json    # Player 2 data
│   └── ...
├── profiles_index.json   # List of all players
└── current_user.json     # Currently selected player
```

### What's Stored Per Player
- Display name and rock star name
- Total coins earned
- Complete game history
- Times table performance (2-12)
- Studio speeds and rock status
- Avatar and theme preferences
- Last played timestamp

## 🎯 Use Cases

### Family with Multiple Children
```
1. Create a profile for each child
2. Each child selects their name when playing
3. All progress tracked separately
4. View each child's statistics independently
```

### Classroom Setting
```
1. Teacher creates profiles for students
2. Students select their profile
3. Teacher monitors individual progress
4. Reset stats at end of term if needed
```

### Personal Practice Tracking
```
1. Create profiles for different skill levels
2. "Easy Mode" profile for learning
3. "Challenge Mode" profile for speed
4. Compare your own progress over time
```

## 🔒 Safety Features

### Protected Actions
- **Delete confirmation** - Prevents accidental deletion
- **Reset confirmation** - Clear warning about data loss
- **Last profile protection** - Cannot delete the only remaining player
- **No data loss** - Names and customization preserved on reset

### Automatic Handling
- **Default profile creation** - Always have at least one profile
- **Auto user switching** - If current user deleted, switches to another
- **Data persistence** - All saves happen automatically
- **Backup on background** - Mobile app saves when backgrounded

## ⚙️ Technical Details

### Profile IDs
- Each profile has a unique 8-character ID
- Used internally for file management
- Users see friendly names, not IDs

### Current User
- The app tracks which user is active
- Stored in `data/current_user.json`
- Used to load correct profile on startup

### Profile Index
- Master list of all profiles
- Stores names and last played time
- Used for user selection screen
- Sorted by most recently played

## 🐛 Troubleshooting

### User selection screen not showing
- Only shows if you have 2+ players
- With 1 player, goes straight to menu
- To add players: Main Menu → Switch Player → New Player

### Lost a player profile
- Check `data/profiles/` directory
- Profile files are named with unique IDs
- Manual recovery possible if file exists

### Want to start completely fresh
Delete the data directory:
```bash
rm -rf data/
```
Next launch will create a new default profile.

### Statistics not saving
- Profiles save automatically after each game
- Check file permissions on `data/` directory
- Profile manager handles all saves

## 📱 Mobile Considerations

### iPad/iPhone (iOS)
- User selection at app launch
- Touch-optimized profile buttons
- Swipe between management screens
- Auto-save when app backgrounds

### Android
- Same features as iOS
- Back button returns to previous screen
- Profile data stored in app data directory

### Performance
- Handles 100+ profiles efficiently
- Instant user switching
- No lag when loading profiles
- Minimal storage per user (~10KB)

## 🎨 Customization Per User

Each user can have their own:
- **Rock star name** - Unique identity
- **Avatar image** - Custom picture URL
- **Color theme** - Rock, Ocean, Forest, or Sunset
- **Progress tracking** - Independent statistics

Changes made in Settings apply only to the current user.

## 🚀 Tips & Best Practices

### For Parents
1. Create profiles for each child
2. Use descriptive names (first name works great)
3. Let each child customize their profile
4. Check stats periodically to track progress
5. Use reset sparingly - progress is motivation!

### For Teachers
1. Create profiles at start of term
2. Use student names or ID numbers
3. Monitor progress in Manage screen
4. Reset at end of term for fresh start
5. Consider separate profiles for practice vs. tests

### For Developers
1. Profile data is in JSON format
2. Easy to backup/restore
3. Profile manager handles all CRUD
4. Extend with additional fields as needed
5. Safe multi-user implementation

## 🎉 Benefits

### Educational
- Track individual learning progress
- Compare performance across tables
- Motivate through personal achievement
- Safe, private progress tracking

### Convenience
- No need for multiple devices
- Quick user switching
- Persistent data per user
- Works offline

### Family-Friendly
- Fair gameplay for siblings
- No conflict over progress
- Personalized experience
- Parental oversight available

---

## Quick Reference

| Action | From Where | Button |
|--------|------------|--------|
| Add player | Main menu or User select | ➕ New Player |
| Switch player | Main menu | 👥 Switch Player |
| Rename player | Manage screen | ✏️ Rename |
| Reset stats | Manage screen | 🔄 Reset Stats |
| Delete player | Manage screen | 🗑️ Delete |
| View all players | User select | (automatic) |
| Manage players | User select | ⚙️ Manage |

Happy playing! 🎸
