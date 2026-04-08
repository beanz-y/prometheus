"""
Test script - verifies game can initialize and run basic commands.
Run this to verify the installation works without launching the interactive UI.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.game import Game
from content.rooms_act1 import build_act1_rooms
from content.rooms_act2 import build_act2_rooms
from content.rooms_act3 import build_act3_rooms
from content.items import build_all_items
from content.npcs import build_all_npcs
from content.dialogues import build_all_dialogues
from content.events import build_all_events


def run_tests():
    print("=" * 60)
    print("  PROMETHEUS PROTOCOL - TEST SUITE")
    print("=" * 60)
    print()

    # Initialize
    print("1. Initializing game...")
    game = Game()
    game.display.use_typewriter = False
    game.display.use_color = False

    build_act1_rooms(game.world)
    build_act2_rooms(game.world)
    build_act3_rooms(game.world)
    build_all_items(game.world)
    build_all_npcs(game.world)
    build_all_dialogues(game.dialogue_manager)
    build_all_events(game.event_manager)

    for npc in game.world.npcs.values():
        if npc.location and npc.location in game.world.rooms:
            room = game.world.get_room(npc.location)
            if npc.id not in room.npcs:
                room.npcs.append(npc.id)
    print("   OK")

    # Stats
    print()
    print("2. Content statistics:")
    print(f"   Rooms:          {len(game.world.rooms)}")
    print(f"   Items:          {len(game.world.items)}")
    print(f"   NPCs:           {len(game.world.npcs)}")
    print(f"   Events:         {len(game.event_manager.events)}")
    print(f"   Dialogue trees: {len(game.dialogue_manager.trees)}")

    readable = sum(1 for i in game.world.items.values() if i.readable)
    print(f"   Readable logs:  {readable}")

    # World validation
    print()
    print("3. Validating world references...")
    errors = 0
    for room in game.world.rooms.values():
        for direction, exit_obj in room.exits.items():
            if exit_obj.destination not in game.world.rooms:
                print(f"   BAD EXIT: {room.id} -> {direction} -> {exit_obj.destination}")
                errors += 1
        for item_id in room.items:
            if item_id not in game.world.items:
                print(f"   MISSING ITEM: {room.id} has '{item_id}'")
                errors += 1
    if errors == 0:
        print("   OK - All references valid")
    else:
        print(f"   FAIL - {errors} errors")

    # Parser tests
    print()
    print("4. Testing command parser...")
    def check_parse(raw, validator):
        """Run parser and check with validator function."""
        try:
            seq = game.parser.parse(raw)
            return bool(validator(seq))
        except Exception:
            return False

    tests = [
        ("look", lambda s: s.commands[0].verb == 'look'),
        ("n", lambda s: s.commands[0].verb == 'go' and s.commands[0].direct_object == 'north'),
        ("take the red key", lambda s: s.commands[0].verb == 'take' and 'red key' in s.commands[0].direct_object),
        ("examine computer", lambda s: s.commands[0].verb == 'examine'),
        ("take key and open door", lambda s: len(s.commands) == 2),
        ("go north then take card then look", lambda s: len(s.commands) == 3),
        ("shoot enemy while running to cover", lambda s: s.simultaneous),
        ("type 1234 into keypad", lambda s: s.commands[0].verb == 'type' and s.commands[0].modifier == '1234'),
        ('type "override alpha" into console', lambda s: s.commands[0].modifier == 'override alpha'),
    ]

    for raw, validator in tests:
        passed = check_parse(raw, validator)
        status = "OK  " if passed else "FAIL"
        print(f"   [{status}] {raw!r}")

    # Save/load
    print()
    print("5. Testing save/load...")
    game.player.add_flag("test_save_flag")
    game.player.add_item("cryo_release_key")
    save_ok = game.save_manager.save_game(game, "test_slot")

    game.player.remove_flag("test_save_flag")
    game.player.remove_item("cryo_release_key")

    load_ok = game.save_manager.load_game(game, "test_slot")
    has_flag = "test_save_flag" in game.player.flags
    has_item = game.player.has_item("cryo_release_key")

    if save_ok and load_ok and has_flag and has_item:
        print("   OK")
    else:
        print(f"   FAIL - save:{save_ok} load:{load_ok} flag:{has_flag} item:{has_item}")

    # Cleanup
    if os.path.exists("saves/test_slot.save.json"):
        os.remove("saves/test_slot.save.json")

    # Event system
    print()
    print("6. Testing event system...")
    events_fired_before = len([e for e in game.event_manager.events.values() if e.fired])
    game.event_manager.fire_trigger("game_start", game)
    events_fired_after = len([e for e in game.event_manager.events.values() if e.fired])
    if events_fired_after > events_fired_before:
        print(f"   OK - Fired {events_fired_after - events_fired_before} events")
    else:
        print("   FAIL - No events fired")

    # Room description
    print()
    print("7. Testing room description rendering...")
    try:
        game.describe_current_room()
        print("\n   OK")
    except Exception as e:
        print(f"   FAIL - {e}")

    print()
    print("=" * 60)
    print("  TEST SUITE COMPLETE")
    print("=" * 60)
    print()
    print("Run 'python main.py' to play the game.")
    print()


if __name__ == "__main__":
    run_tests()
