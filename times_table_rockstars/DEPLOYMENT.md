# Deployment Guide

This guide covers deploying Times Table Rockstars to iOS (iPad) and Android devices.

## Prerequisites

### For Both Platforms
- Python 3.8 or higher
- Git
- A computer (Mac required for iOS, Linux/Mac/Windows for Android)

### Platform-Specific
- **iOS**: macOS with Xcode installed
- **Android**: Linux, macOS, or Windows with Android SDK

## Desktop Testing (Recommended First Step)

Before deploying to mobile, test on desktop:

```bash
cd times_table_rockstars
pip install -r requirements.txt
python main.py
```

## iOS Deployment (iPad)

### Method 1: Using Kivy-iOS (Recommended)

1. **Install Kivy-iOS**
   ```bash
   # Install prerequisites (macOS)
   brew install autoconf automake libtool pkg-config
   brew install openssl readline sqlite3 xz zlib

   # Install Kivy-iOS
   pip install kivy-ios
   ```

2. **Build Dependencies**
   ```bash
   toolchain build python3 kivy pillow
   ```

3. **Create Xcode Project**
   ```bash
   cd times_table_rockstars
   toolchain create TimesTableRockstars .
   ```

4. **Open in Xcode**
   - Open the generated `.xcodeproj` file
   - Connect your iPad via USB
   - Select your iPad as the target device
   - Update the Bundle Identifier in Xcode
   - Sign the app with your Apple Developer account (free account works)
   - Click "Run" to build and deploy

5. **Trust Developer on iPad**
   - Go to Settings > General > Device Management
   - Trust your developer certificate
   - The app should now launch

### Method 2: Using Kivy Launcher (Testing Only)

1. Install Kivy Launcher from the App Store on your iPad
2. Transfer the project files to your iPad via iTunes or AirDrop
3. Place in the Kivy Launcher directory
4. Launch through Kivy Launcher app

**Note**: This method is for testing only and has limitations.

## Android Deployment

### Using Buildozer (Recommended)

1. **Install Buildozer**
   ```bash
   # Linux/WSL
   pip install buildozer

   # Install Android SDK dependencies
   sudo apt update
   sudo apt install -y git zip unzip openjdk-11-jdk wget
   sudo apt install -y python3-pip autoconf libtool pkg-config zlib1g-dev
   sudo apt install -y libncurses5:i386 libstdc++6:i386 zlib1g:i386
   ```

2. **Build APK**
   ```bash
   cd times_table_rockstars
   buildozer android debug
   ```

   First build takes 30-60 minutes as it downloads Android SDK/NDK.

3. **Install on Android Device**
   ```bash
   # Enable USB debugging on your Android device
   # Connect device via USB
   buildozer android deploy run
   ```

4. **Or Transfer APK Manually**
   - Find the APK in `bin/` directory
   - Transfer to your Android device
   - Install the APK
   - Allow installation from unknown sources if prompted

### Building Release APK (For Distribution)

```bash
buildozer android release

# Sign the APK
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/*.apk alias_name
```

## Troubleshooting

### iOS Issues

**Problem**: Code signing errors
- **Solution**: In Xcode, go to Signing & Capabilities, select your team, and enable "Automatically manage signing"

**Problem**: App crashes on launch
- **Solution**: Check Xcode console for errors. Ensure all Python dependencies are included in the toolchain build.

**Problem**: Black screen on iPad
- **Solution**: Kivy might need GPU drivers. Try updating Kivy or checking device compatibility.

### Android Issues

**Problem**: Buildozer build fails
- **Solution**:
  ```bash
  buildozer android clean
  rm -rf .buildozer
  buildozer android debug
  ```

**Problem**: App won't install
- **Solution**: Enable "Install from Unknown Sources" in Android settings

**Problem**: App crashes on startup
- **Solution**: Check logcat logs:
  ```bash
  buildozer android logcat
  ```

### General Issues

**Problem**: Import errors or missing modules
- **Solution**: Ensure all dependencies are in requirements.txt and installed

**Problem**: Audio doesn't play
- **Solution**: Add sound files to assets/sounds/ directory. The app will run without them but silently.

**Problem**: Slow performance
- **Solution**: Optimize graphics, reduce animation complexity, test on a device instead of emulator

## Performance Tips for iPad 2021

Your target device (iPad 2021) is powerful, but keep these in mind:

1. **Optimize Images**: Use appropriately sized images (max 1024x1024)
2. **Audio**: Use compressed formats (OGG for Android, M4A for iOS)
3. **Testing**: Always test on the actual device, not just desktop
4. **Battery**: Background music can drain battery; consider making it optional

## Next Steps

1. Test thoroughly on desktop
2. Add your custom sounds and music to assets/
3. Customize graphics and themes
4. Build for iOS and test on iPad
5. Share with your relative!

## Additional Resources

- Kivy Documentation: https://kivy.org/doc/stable/
- Kivy-iOS: https://github.com/kivy/kivy-ios
- Buildozer: https://github.com/kivy/buildozer
- Apple Developer: https://developer.apple.com/
