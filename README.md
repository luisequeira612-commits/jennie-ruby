# JENNIE RUBY

A personal Android icon pack for Nova Launcher, designed around the TECNO POVA 4.

## Visual direction
- Deep black, ruby red and crimson, with dusty rose accents.
- Velvet, dark roses, ribbons, pearls and elegant jewelry details.
- App symbols should remain recognizable; decorative styling must not obscure their identity.

## Current project status
- 146 launcher activities from the TECNO POVA 4 catalogued.
- 146 custom drawable resources included in the Android project.
- 146 Nova Launcher mappings generated in `app/src/main/res/xml/appfilter.xml`.
- CI validates that the generated app filter stays synchronized with the catalog and artwork.
- The welcome screen includes the Nova Launcher selection path.
- **Physical installation and compatibility testing on the TECNO POVA 4 are still pending.** A successful CI build is not a substitute for testing on the device.

## Install and apply (after downloading the debug APK)
1. Install the APK on the TECNO POVA 4. Android may ask you to allow installation from the app used to open the file.
2. Open Nova Launcher settings.
3. Go to **Look & feel → Icon style → Icon theme**.
4. Select **JENNIE RUBY**.
5. Check the home screen and app drawer. Some apps or alternate launcher activities may need manual icon assignment if their component differs from the catalog.

The debug APK is intended for personal testing. It is not a Play Store release and is not a production-signed release build.

## Build locally
Requirements: JDK 17, Android SDK with platform 35, and Gradle 8.9.

```bash
python3 tools/generate_appfilter.py
git diff --exit-code -- app/src/main/res/xml/appfilter.xml
gradle assembleDebug
```

The debug APK is generated at `app/build/outputs/apk/debug/app-debug.apk`.

## Separate theme elements
Wallpaper and KWGT widgets are separate setup items; they are not installed automatically by the icon-pack APK.

## Constraints
- Free tools and workflows; personal use.
- No accounts, paid APIs, subscriptions or backend.
- Do not claim device compatibility until installation and launcher testing are completed.
