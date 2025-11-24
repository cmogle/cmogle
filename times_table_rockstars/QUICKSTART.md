# Quick Start Guide

Get Times Table Rockstars running in 5 minutes!

## For Complete Beginners

### Step 1: Install Python

**macOS**:
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Windows**:
1. Download Python from https://www.python.org/downloads/
2. Run installer, check "Add Python to PATH"
3. Click Install

**Linux**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Download the Project

```bash
# Navigate to where you want the project
cd ~/Documents

# If you have git:
git clone <repository-url>
cd times_table_rockstars

# Or download and extract the ZIP file
```

### Step 3: Run Setup

**macOS/Linux**:
```bash
chmod +x setup.sh
./setup.sh
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
# Activate virtual environment first
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Run the app
python main.py
```

## Testing on Desktop

The app will open in a phone-sized window (400x700 pixels) for testing.

### Controls:
- Click buttons with your mouse
- Type numbers for answers
- Use the on-screen numpad

### Expected behavior:
1. You'll see the main menu with game mode options
2. Your Rock Star name is randomly generated
3. Choose a game mode to start playing
4. Answer times table questions
5. Earn coins and improve your Rock Status!

## Next Steps

### Before Deploying to iPad:

1. **Test all game modes** on desktop
2. **Add assets** (optional but recommended):
   - Sound effects in `assets/sounds/`
   - Music in `assets/music/`
   - Images in `assets/images/`
3. **Customize** for your child (see CUSTOMIZATION.md)
4. **Deploy to iPad** (see DEPLOYMENT.md)

### Quick Customization:

```bash
# Change rock star name
# Run the app, go to Settings → Enter new name → Save

# Change theme
# Run the app, go to Settings → Select a theme

# Change avatar
# Run the app, go to Settings → Customize Avatar → Enter image URL
```

## Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python (see Step 1)

### Issue: "pip not found"
**Solution**:
```bash
python3 -m ensurepip --upgrade
```

### Issue: "Permission denied" on setup.sh
**Solution**:
```bash
chmod +x setup.sh
```

### Issue: Kivy installation fails
**Solution**:
```bash
# Try installing dependencies first
# macOS:
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer

# Linux:
sudo apt install python3-kivy
```

### Issue: App window is too big/small
**Solution**: Edit `main.py`, find this line:
```python
Window.size = (400, 700)  # Change these numbers
```

### Issue: Black screen or crashes
**Solution**:
1. Check terminal for error messages
2. Ensure all requirements installed: `pip install -r requirements.txt`
3. Try: `pip install --upgrade kivy`

## Getting Help

1. Check the error message in the terminal
2. Read DEPLOYMENT.md for platform-specific issues
3. Read CUSTOMIZATION.md for personalization help
4. Google the error message
5. Ask on Kivy forums: https://groups.google.com/g/kivy-users

## Success Checklist

✅ Python installed
✅ Virtual environment created
✅ Requirements installed
✅ App runs on desktop
✅ Can play through a complete game
✅ Settings work (name, theme changes)
✅ Stats are saved between runs

Once all checked, you're ready to deploy to iPad!

## File Structure Overview

```
times_table_rockstars/
├── main.py                  # Start here - run this file
├── requirements.txt         # Python dependencies
├── setup.sh                 # Automated setup script
│
├── game/                    # Game logic
│   ├── core.py             # Main game engine
│   ├── modes.py            # Game modes (Garage, Studio, etc.)
│   ├── questions.py        # Question generation
│   ├── profile.py          # User profile & progress
│   └── audio.py            # Sound effects & music
│
├── ui/                      # User interface
│   ├── screens.py          # All game screens
│   ├── widgets.py          # Custom UI components
│   └── themes.py           # Color themes
│
├── config/                  # Configuration
│   └── settings.py         # Game settings & constants
│
├── assets/                  # Media files
│   ├── images/             # Graphics
│   ├── sounds/             # Sound effects
│   └── music/              # Background music
│
├── data/                    # Saved data (created on first run)
│   ├── profile.json        # User profile
│   └── settings.json       # App settings
│
└── buildozer.spec          # Android build config
```

## Common Questions

**Q: Do I need an Apple Developer account?**
A: A free account works for personal use on your own devices.

**Q: How long does the first build take?**
A: iOS: 10-30 minutes. Android: 30-60 minutes (downloads SDKs).

**Q: Can I use this on multiple iPads?**
A: Yes! Build once, install on any device signed with your account.

**Q: Will it work offline?**
A: Yes! Only needs internet for avatar image URLs.

**Q: Can my child see their progress over time?**
A: Yes! Check Stats screen for detailed progress per times table.

**Q: Is this the official Times Table Rockstars app?**
A: No, this is an educational replica for personal use.

Ready to rock? Let's go! 🎸
