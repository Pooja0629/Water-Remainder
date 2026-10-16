[app]

# (str) Title of your application
title = AquaPal

# (str) Package name
package.name = aquapal

# (str) Package domain (needed for android/ios packaging)
package.domain = org.aquapal

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,gif

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3==3.11.9,kivy==2.3.0,plyer,pillow

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = POST_NOTIFICATIONS, WAKE_LOCK

# (int) Target Android API
android.api = 34

# (int) Minimum API required
android.minapi = 21

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Accept the Android SDK license automatically
android.accept_sdk_license = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
