"""
THE PROMETHEUS PROTOCOL
An interactive fiction game by Claude Opus 4.6

Main entry point. Run this file to start the game.
"""

import sys
import os

# Handle both normal Python and PyInstaller bundled execution
if getattr(sys, 'frozen', False):
    # Running as compiled .exe (PyInstaller)
    _BASE_DIR = sys._MEIPASS
    _APP_DIR = os.path.dirname(sys.executable)
else:
    # Running as normal Python script
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _APP_DIR = _BASE_DIR

sys.path.insert(0, _BASE_DIR)

from engine.game import Game
from content.rooms_act1 import build_act1_rooms
from content.rooms_act2 import build_act2_rooms
from content.rooms_act3 import build_act3_rooms
from content.items import build_all_items
from content.npcs import build_all_npcs
from content.dialogues import build_all_dialogues
from content.events import build_all_events
from content.memories import build_memory_events
from content.puzzles import build_puzzle_events
from content.companion_lines import build_companion_commentary


def initialize_game():
    """Create and populate the game world."""
    game = Game()

    # Build all content
    print("Initializing the Prometheus...")

    # Rooms across three acts
    build_act1_rooms(game.world)
    build_act2_rooms(game.world)
    build_act3_rooms(game.world)

    # Items, NPCs, dialogue
    build_all_items(game.world)
    build_all_npcs(game.world)
    build_all_dialogues(game.dialogue_manager)
    build_all_events(game.event_manager)
    build_memory_events(game.event_manager, game.world)
    build_puzzle_events(game.event_manager, game.world)

    # Companion commentary
    build_companion_commentary(game.companion)

    # Place starting items in the starting room
    # (most items are placed via their room definitions)

    # Sync NPC locations with rooms
    for npc in game.world.npcs.values():
        if npc.location and npc.location in game.world.rooms:
            room = game.world.get_room(npc.location)
            if npc.id not in room.npcs:
                room.npcs.append(npc.id)

    return game


def main_menu():
    """Display the main menu."""
    from engine.updater import get_current_version
    ver = get_current_version()
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║     THE PROMETHEUS PROTOCOL          ║")
    print(f"  ║     v{ver:<33s}║")
    print("  ║                                      ║")
    print("  ║  1. New Game                         ║")
    print("  ║  2. Load Game                        ║")
    print("  ║  3. About                            ║")
    print("  ║  4. Check for Updates                ║")
    print("  ║  5. Quit                             ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    choice = input("  Enter choice: ").strip()
    return choice


def show_about():
    """Display about text."""
    print()
    print("  THE PROMETHEUS PROTOCOL")
    print("  An interactive fiction by Claude Opus 4.6")
    print()
    print("  A narrative-heavy text adventure inspired by Zork, Hitchhiker's")
    print("  Guide to the Galaxy, and classic sci-fi horror games like")
    print("  System Shock 2, Dead Space, Event Horizon, Alien, and SOMA.")
    print()
    print("  You play as Dr. Alex Chen, awakening from cryo-sleep aboard")
    print("  the ISV Prometheus to find the crew dead, the ship dying,")
    print("  and 18 hours until catastrophe.")
    print()
    print("  Type 'help' in-game for command reference.")
    print("  Multi-command support: 'take key then unlock door and go north'")
    print()
    input("  [Press ENTER to return to menu]")


def _startup_update_check():
    """Quick background check on startup. Just notifies, doesn't download."""
    try:
        from engine.updater import check_for_update, UPDATE_CHECK_URL
        if not UPDATE_CHECK_URL:
            return
        result = check_for_update()
        if result and result['available']:
            print(f"\n  * Update available: v{result['latest']} "
                  f"(you have v{result['current']})")
            print("  * Select 'Check for Updates' from the menu to install.\n")
    except Exception:
        pass  # Silently fail - don't block game startup


def main():
    """Main entry point."""
    _startup_update_check()
    while True:
        choice = main_menu()

        if choice == '1':
            # New game
            game = initialize_game()
            try:
                game.start(skip_intro=False)
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Returning to menu.")
            except Exception as e:
                print(f"\n\nAn error occurred: {e}")
                import traceback
                traceback.print_exc()

        elif choice == '2':
            # Load game
            game = initialize_game()
            saves = game.save_manager.list_saves()
            if not saves:
                print("\n  No saved games found.")
                input("  [Press ENTER]")
                continue
            print("\n  Available saves:")
            for i, save in enumerate(saves, 1):
                print(f"    {i}. {save['slot']} - Turn {save['turn']} - {save['location']}")
            slot_choice = input("  Enter slot name to load: ").strip()
            if game.save_manager.load_game(game, slot_choice):
                print("  Game loaded.")
                try:
                    game.start(skip_intro=True)
                except KeyboardInterrupt:
                    print("\n\nGame interrupted.")
            else:
                print("  Load failed.")
                input("  [Press ENTER]")

        elif choice == '3':
            show_about()

        elif choice == '4':
            # Check for updates
            from engine.updater import run_update_check
            updated = run_update_check()
            if updated:
                print("\n  Restart the game to use the new version.")
                break
            input("  [Press ENTER to return to menu]")

        elif choice == '5' or choice.lower() in ('quit', 'exit', 'q'):
            print("\n  Thank you for playing. The stars are waiting.")
            break

        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
