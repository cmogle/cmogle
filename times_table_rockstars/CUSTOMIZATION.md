# Customization Guide

This guide helps you personalize Times Table Rockstars for your child.

## 🎨 Visual Customization

### Themes

The app includes 4 built-in color themes:

1. **Rock** (default) - Dark red and gold, classic rock theme
2. **Ocean** - Blues and teals, calming water theme
3. **Forest** - Greens, nature theme
4. **Sunset** - Oranges and warm colors

**How to change**: Settings → Select theme

### Custom Avatar

Users can set a custom avatar image:

1. Go to Settings → Customize Avatar
2. Enter an image URL from the internet
3. Click "Load Image" to preview
4. Click "Save Avatar"

**Image URL Sources**:
- Search Google Images (use "Copy image address")
- Use imgur.com to upload and host images
- Free image sites: unsplash.com, pixabay.com

**Tips**:
- Use square images (they look best)
- Pick fun, colorful images
- Rock stars, instruments, or favorite characters work great!

### Rock Star Name

Personalize the profile name:

1. Go to Settings
2. Enter a new Rock Star Name
3. Click "Save Name"

Default names are randomly generated (e.g., "Lightning Storm", "Mega Phoenix")

## 🎵 Audio Customization

### Adding Sound Effects

Place your custom sound files in `assets/sounds/`:

- `correct.wav` - Plays when answer is correct
- `incorrect.wav` - Plays when answer is incorrect
- `coin.wav` - Plays when earning coins
- `complete.wav` - Plays when completing a game
- `click.wav` - Button click sound

**Where to find sounds**:
- freesound.org (free sound effects library)
- Generate your own with BFXR (bfxr.net)
- Record your own sounds

**Format**: WAV or OGG files

### Adding Background Music

Place music files in `assets/music/`:

- Supports MP3 and OGG formats
- The app will randomly select from available tracks
- Music loops automatically

**Where to find music**:
- incompetech.com (free royalty-free music)
- freemusicarchive.org
- YouTube Audio Library

**Tip**: Look for upbeat, instrumental rock tracks!

## 🎯 Gameplay Customization

### Difficulty Levels

Adjust in the Settings:
- **Easy**: Tables 2-5
- **Medium**: Tables 2-10 (default)
- **Hard**: Tables 2-12

### Game Modes

Each mode serves different learning needs:

1. **Garage Mode**
   - Best for: Focused practice on weak tables
   - Rewards: 10 coins per correct answer (highest!)
   - Auto-adapts to show tables that need practice

2. **Studio Mode**
   - Best for: Building speed
   - Time limit: 60 seconds
   - Tracks speed (questions per minute)
   - Unlocks Rock Status levels

3. **Jamming Mode**
   - Best for: Stress-free practice
   - No timer!
   - Choose multiplication, division, or both
   - Perfect for building confidence

4. **Soundcheck Mode**
   - Best for: Testing knowledge
   - 25 questions
   - 6 seconds per question
   - Similar to official multiplication tables check

## 📱 Child-Friendly Features

### Already Included

✅ Anonymous rock names (no personal info)
✅ No in-app purchases
✅ No ads
✅ No internet required after installation
✅ Age-appropriate interface
✅ Positive reinforcement (coins, status levels)

### Safety Tips

- The avatar customization requires image URLs
- Supervise URL entry to ensure appropriate content
- Consider pre-loading favorite images on imgur.com
- Test the app yourself before giving to your child

## 🌟 Personalization Ideas

### For Your Relative

Since she loves the game, consider:

1. **Custom avatar** of her favorite character or pet
2. **Rock star name** based on her real name or nickname
3. **Color theme** matching her favorite color
4. **Sound effects** - record your voice saying "Great job!" etc.
5. **Background music** from her favorite movie or show

### Making It Special

- Take a photo of her achievement certificates (in-app stats)
- Create a "High Score Board" at home
- Reward real-world prizes for reaching Rock Status levels
- Do "multiplayer" by taking turns and comparing scores

## 🔧 Advanced Customization

### Modifying Code

If you're comfortable with Python, you can customize:

**Color schemes** (`config/settings.py`):
```python
THEMES = {
    "custom": {
        "primary": "#YOUR_COLOR",
        "secondary": "#YOUR_COLOR",
        "background": "#YOUR_COLOR",
        "text": "#YOUR_COLOR",
        "accent": "#YOUR_COLOR",
    }
}
```

**Coin rewards** (`config/settings.py`):
```python
GARAGE_COINS_PER_ANSWER = 10  # Change to any value
```

**Rock status levels** (`config/settings.py`):
```python
ROCK_STATUS = {
    0: "Custom Name",
    20: "Another Name",
    # Add your own levels
}
```

**Question time limits** (`config/settings.py`):
```python
SOUNDCHECK_TIME_LIMIT = 6  # Seconds per question
STUDIO_TIME_LIMIT = 60     # Total time for studio mode
```

### Adding Custom Screens

You can add new screens or modify existing ones in `ui/screens.py`.

Ideas:
- Achievement gallery
- Leaderboard (for siblings)
- Daily challenges
- Progress charts

## 📊 Understanding Statistics

Help your child track progress:

- **Overall Accuracy**: Percentage of all questions answered correctly
- **Studio Speed**: Questions answered correctly per minute
- **Rock Status**: Based on average studio speed
  - Wannabe: 0+ q/min
  - Gigging: 10+ q/min
  - Breakthrough Artist: 30+ q/min
  - Rock Star: 60+ q/min
  - Rock Hero: 80+ q/min

- **Table Performance**: Individual accuracy for each times table (2-12)

**Tips**:
- Celebrate improvements, not just perfect scores
- Focus on weak tables in Garage mode
- Use Jamming mode to build confidence before Soundcheck

## 🎁 Sharing Your Customizations

If you create great themes or modifications:

1. Take screenshots
2. Document your changes
3. Consider sharing with other parents/developers
4. This is a learning project - experiment freely!

## Need Help?

Common customization questions:

**Q: How do I reset progress?**
A: Delete the `data/profile.json` file to start fresh

**Q: Can I have multiple profiles?**
A: Currently single profile, but you could manually backup/swap profile.json files

**Q: How do I make the text bigger?**
A: Edit font_size values in `ui/widgets.py` and `ui/screens.py`

**Q: Can I add more times tables (13+)?**
A: Yes! Modify the range in `game/questions.py` (line with `range(2, 13)`)

Enjoy customizing! 🎸
