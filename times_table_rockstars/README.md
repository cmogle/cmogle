# Times Table Rockstars Replica

A Python replica of the Times Table Rockstars game, designed for mobile devices (iPad/Android).

## Features

- **Multiple Game Modes**:
  - **Garage**: Practice individual times tables with high rewards
  - **Studio**: Set speed records and earn rock status
  - **Jamming**: Timer-free practice at your own pace
  - **Soundcheck**: 25-question timed challenge

- **Customization**:
  - Personalized avatars
  - Custom themes and colors
  - Choose images from online sources
  - Custom rock star names

- **Progression System**:
  - Earn coins for correct answers
  - Track your speed and accuracy
  - Level up your rock status
  - View personal statistics

- **Audio & Visuals**:
  - Sound effects for correct/incorrect answers
  - Background music
  - Colorful rock-themed interface

## Installation

### Desktop (for development/testing)

```bash
pip install -r requirements.txt
python main.py
```

### iOS (iPad)

```bash
# Install dependencies
brew install autoconf automake libtool pkg-config
pip install kivy-ios

# Build for iOS
toolchain build python3 kivy pillow
toolchain create TimesTableRockstars .
```

### Android

```bash
# Install buildozer
pip install buildozer

# Build APK
buildozer android debug
```

## Usage

1. Launch the app
2. Create your rock star profile
3. Choose a game mode
4. Answer times table questions
5. Earn coins and improve your speed!

## Customization

Access Settings to:
- Change your avatar
- Select custom images
- Adjust difficulty
- Choose your favorite tables to practice

## Requirements

- Python 3.8+
- iPad (2021 or later) or Android device
- Internet connection for downloading custom images

## License

Personal use and educational purposes.
