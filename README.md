# JENNIE RUBY

A personal Android icon pack for Nova Launcher, designed around the TECNO POVA 4.

## Visual direction
- Deep black and ruby red, crimson and dusty rose accents.
- Velvet, dark roses, ribbons, pearls and elegant jewelry details.
- App symbols should remain recognizable; decorative styling must not obscure their identity.

## Current project status
- 146 launcher activities from the TECNO POVA 4 catalogued.
- 146 custom drawable resources included in the Android project.
- 146 Nova Launcher mappings generated in the Android project.
- CI validates vector structure and that the generated app filter stays synchronized with the catalog and artwork.
- The APK has been installed on a TECNO POVA 4 and JENNIE RUBY was successfully discovered and applied in Nova Launcher.
- The JENNIE RUBY app now has its own Ruby monogram launcher icon.
- Visual review of individual icons at actual launcher size is ongoing; the Nova Launcher Settings icon still needs its exact component identified before adding a mapping.

## Install and apply
1. Install the debug APK on the TECNO POVA 4. Android may ask you to allow installation from the app used to open the file.
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
- Do not claim device compatibility beyond the confirmed installation and Nova theme application test.
