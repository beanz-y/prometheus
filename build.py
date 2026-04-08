"""
Build script - creates a distributable .exe using PyInstaller.

Usage:
    python build.py

Output:
    dist/ThePrometheusProtocol/
        ThePrometheusProtocol.exe
        saves/          (empty, for save games)
        README.txt      (gameplay instructions)
"""

import os
import sys
import shutil
import subprocess


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_NAME = "ThePrometheusProtocol"


def build():
    print("=" * 60)
    print("  Building The Prometheus Protocol")
    print("=" * 60)
    print()

    # Clean previous builds
    for d in ['build', 'dist']:
        path = os.path.join(PROJECT_ROOT, d)
        if os.path.exists(path):
            print(f"Cleaning {d}/...")
            shutil.rmtree(path)

    spec_file = os.path.join(PROJECT_ROOT, f"{DIST_NAME}.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # Run PyInstaller - find it on PATH or in known locations
    print("Running PyInstaller...")
    pyinstaller_exe = shutil.which("pyinstaller")
    if not pyinstaller_exe:
        # Try common Windows install locations
        for ver in ['312', '311', '310']:
            candidate = os.path.expandvars(
                rf"%LOCALAPPDATA%\Programs\Python\Python{ver}\Scripts\pyinstaller.exe"
            )
            if os.path.exists(candidate):
                pyinstaller_exe = candidate
                break
    if not pyinstaller_exe:
        print("ERROR: pyinstaller not found. Install it with: pip install pyinstaller")
        return False
    print(f"Using: {pyinstaller_exe}")

    cmd = [
        pyinstaller_exe,
        "--name", DIST_NAME,
        "--console",                    # Console app (text game)
        "--noconfirm",                  # Overwrite without asking
        "--clean",                      # Clean cache
        "--onedir",                     # Directory mode (faster startup than --onefile)
        "--icon", "NONE",               # No custom icon
        # Hidden imports for our content modules
        "--hidden-import", "content",
        "--hidden-import", "content.intro",
        "--hidden-import", "content.rooms_act1",
        "--hidden-import", "content.rooms_act2",
        "--hidden-import", "content.rooms_act3",
        "--hidden-import", "content.items",
        "--hidden-import", "content.npcs",
        "--hidden-import", "content.dialogues",
        "--hidden-import", "content.events",
        "--hidden-import", "content.endings",
        "--hidden-import", "content.memories",
        "--hidden-import", "content.puzzles",
        "--hidden-import", "content.companion_lines",
        "--hidden-import", "engine",
        "--hidden-import", "engine.game",
        "--hidden-import", "engine.parser",
        "--hidden-import", "engine.display",
        "--hidden-import", "engine.world",
        "--hidden-import", "engine.room",
        "--hidden-import", "engine.item",
        "--hidden-import", "engine.npc",
        "--hidden-import", "engine.player",
        "--hidden-import", "engine.event",
        "--hidden-import", "engine.dialogue",
        "--hidden-import", "engine.save_load",
        "--hidden-import", "engine.companion",
        # Add data files
        "--add-data", f"engine{os.pathsep}engine",
        "--add-data", f"content{os.pathsep}content",
        "--add-data", f"story{os.pathsep}story",
        "--add-data", f"VERSION{os.pathsep}.",
        # Entry point
        "main.py",
    ]

    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("\nBuild FAILED!")
        return False

    # Post-build: create saves directory and README
    dist_dir = os.path.join(PROJECT_ROOT, "dist", DIST_NAME)

    # Create saves folder
    saves_dir = os.path.join(dist_dir, "saves")
    os.makedirs(saves_dir, exist_ok=True)

    # Create a player-facing README
    readme_path = os.path.join(dist_dir, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("""THE PROMETHEUS PROTOCOL
======================

An interactive fiction game.

HOW TO PLAY:
  Double-click ThePrometheusProtocol.exe to start.
  The game runs in your terminal/command prompt.

  For the best experience, maximize your terminal window.

COMMANDS:
  Movement:    north, south, east, west, up, down (or n, s, e, w, u, d)
  Look:        look, examine <thing>, search
  Items:       take <item>, drop <item>, inventory (i)
  Interact:    use <item>, open <thing>, read <item>, talk to <person>
  Combat:      attack <target>, use <weapon> on <target>, hide, sneak, flee
  Senses:      listen, smell, touch
  Meta:        save, load, status, map, think, objectives, help, quit

  Compound:    take key and unlock door
               go north then examine terminal
               type "1234" into keypad

SAVES:
  Save games are stored in the 'saves' folder next to the .exe.
  You can copy this folder to back up your progress.

TIPS:
  - Read everything. Crew logs contain crucial story and puzzle clues.
  - Examine everything. Environmental details tell stories.
  - Save often. There are 5 endings based on your choices.
  - Time is limited. The ship has 18 hours before destruction.
  - Use 'think' to review what you've learned.
  - Use 'map' to see where you are and where you can go.

Credits:
  Design & narrative by Claude Opus 4.6
  Engine built in Python

""")

    # Read version for zip naming
    version = "0.0.0"
    try:
        with open(os.path.join(PROJECT_ROOT, 'VERSION'), 'r') as f:
            version = f.read().strip()
    except FileNotFoundError:
        pass

    # Copy VERSION into dist for the updater
    shutil.copy2(
        os.path.join(PROJECT_ROOT, 'VERSION'),
        os.path.join(dist_dir, 'VERSION')
    )

    # Create a distributable zip
    zip_name = f"{DIST_NAME}-v{version}-win64"
    zip_path = os.path.join(PROJECT_ROOT, "dist", f"{zip_name}.zip")
    print(f"Creating {zip_name}.zip...")
    shutil.make_archive(
        os.path.join(PROJECT_ROOT, "dist", zip_name),
        'zip',
        os.path.join(PROJECT_ROOT, "dist"),
        DIST_NAME
    )

    print()
    print("=" * 60)
    print(f"  BUILD SUCCESSFUL!  (v{version})")
    print(f"  Folder: dist/{DIST_NAME}/")
    print(f"  Zip:    dist/{zip_name}.zip")
    print(f"  Run:    dist/{DIST_NAME}/{DIST_NAME}.exe")
    print("=" * 60)
    print()
    print("  To create a GitHub release:")
    print(f"    gh release create v{version} dist/{zip_name}.zip \\")
    print(f'      --title "v{version}" --notes "Playtest build"')
    print()
    return True


def release():
    """Create a GitHub release with the current build."""
    version = "0.0.0"
    try:
        with open(os.path.join(PROJECT_ROOT, 'VERSION'), 'r') as f:
            version = f.read().strip()
    except FileNotFoundError:
        pass

    zip_name = f"{DIST_NAME}-v{version}-win64"
    zip_path = os.path.join(PROJECT_ROOT, "dist", f"{zip_name}.zip")

    if not os.path.exists(zip_path):
        print(f"  Build not found at {zip_path}. Run 'python build.py' first.")
        return False

    print(f"  Creating GitHub release v{version}...")
    cmd = [
        "gh", "release", "create",
        f"v{version}",
        zip_path,
        "--title", f"v{version}",
        "--notes", f"Playtest build v{version}",
    ]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode == 0:
        print(f"  Release v{version} created!")
        return True
    else:
        print("  Release creation failed. Make sure 'gh' CLI is installed and authenticated.")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build The Prometheus Protocol")
    parser.add_argument('--release', action='store_true',
                       help='Also create a GitHub release after building')
    args = parser.parse_args()

    success = build()
    if success and args.release:
        release()
    sys.exit(0 if success else 1)
