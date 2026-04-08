"""
Generate a comprehensive game reference document from the game data.

Output: story/GAME_REFERENCE.md

Run this whenever you modify content to refresh the reference.
Usage:
    python tools/generate_reference.py
"""

import os
import sys
import json
from collections import defaultdict

# Make the project importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from engine.game import Game
from content.rooms_act1 import build_act1_rooms
from content.rooms_act2 import build_act2_rooms
from content.rooms_act3 import build_act3_rooms
from content.items import build_all_items
from content.npcs import build_all_npcs
from content.dialogues import build_all_dialogues
from content.events import build_all_events


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def build_game():
    game = Game()
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

    return game


def truncate(text, max_len=100):
    if not text:
        return ""
    text = text.replace('\n', ' ').strip()
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


# ═══════════════════════════════════════════════════════════════════════
# SECTION GENERATORS
# ═══════════════════════════════════════════════════════════════════════

def gen_header():
    return """# THE PROMETHEUS PROTOCOL - GAME REFERENCE

**Auto-generated troubleshooting reference. Do not hand-edit.**
**To regenerate: `python tools/generate_reference.py`**

This document contains every room, item, event, NPC, and puzzle in the game.
Use it to verify content, troubleshoot bugs, trace logic flow, or find specific
references without reloading the game state.

---

## TABLE OF CONTENTS

1. [Overview & Stats](#1-overview--stats)
2. [Ship Deck Map](#2-ship-deck-map)
3. [Room Connectivity Graph](#3-room-connectivity-graph)
4. [Critical Path Walkthrough](#4-critical-path-walkthrough)
5. [All Rooms Reference](#5-all-rooms-reference)
6. [All Items Reference](#6-all-items-reference)
7. [Readable Items (Logs & Journals)](#7-readable-items-logs--journals)
8. [NPC Reference](#8-npc-reference)
9. [Dialogue Topics](#9-dialogue-topics)
10. [All Events Reference](#10-all-events-reference)
11. [Puzzle Solutions](#11-puzzle-solutions)
12. [Locked Content (Keys & Flags)](#12-locked-content-keys--flags)
13. [Flag / Knowledge Graph](#13-flag--knowledge-graph)
14. [Ending Conditions](#14-ending-conditions)
15. [Known Issues / Audit Results](#15-known-issues--audit-results)

---

"""


def gen_stats(game):
    w = game.world
    readable_count = sum(1 for i in w.items.values() if i.readable)
    portable_count = sum(1 for i in w.items.values() if i.portable)
    container_count = sum(1 for i in w.items.values() if i.container)
    weapon_count = sum(1 for i in w.items.values() if 'weapon' in i.flags)
    alive_npcs = sum(1 for n in w.npcs.values() if n.alive)

    total_desc_chars = sum(
        len(r.description) + len(r.first_visit_text or '')
        for r in w.rooms.values()
    )
    total_read_chars = sum(len(i.read_text) for i in w.items.values() if i.readable)

    decks = defaultdict(list)
    for room in w.rooms.values():
        decks[room.deck or 'Unknown'].append(room.id)

    out = ["## 1. Overview & Stats", ""]
    out.append(f"- **Rooms:** {len(w.rooms)}")
    out.append(f"- **Items:** {len(w.items)}")
    out.append(f"  - Portable: {portable_count}")
    out.append(f"  - Readable: {readable_count}")
    out.append(f"  - Containers: {container_count}")
    out.append(f"  - Weapons: {weapon_count}")
    out.append(f"- **NPCs:** {len(w.npcs)} ({alive_npcs} alive, {len(w.npcs) - alive_npcs} dead/system)")
    out.append(f"- **Events:** {len(game.event_manager.events)}")
    out.append(f"- **Dialogue trees:** {len(game.dialogue_manager.trees)}")
    out.append(f"- **Narrative:** ~{(total_desc_chars + total_read_chars) // 5:,} words")
    out.append("")
    out.append("**Decks:**")
    for deck in sorted(decks.keys()):
        out.append(f"  - {deck}: {len(decks[deck])} rooms")
    out.append("")
    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_deck_map(game):
    out = ["## 2. Ship Deck Map", ""]
    out.append("```")
    out.append("                   ┌─────────────────────────────┐")
    out.append("                   │   ISV PROMETHEUS            │")
    out.append("                   │   ~1.2 km long              │")
    out.append("                   │   10 decks, stacked         │")
    out.append("                   └─────────────────────────────┘")
    out.append("")
    out.append("  ▲ UP (Bow / Command)")
    out.append("  │")
    out.append("  │  Deck A - COMMAND ............. Bridge, Ready Room, Comms")
    out.append("  │  Deck B - SCIENCE ............. Main Lab, Exobio Lab, Observatory")
    out.append("  │  Deck C - LIVING .............. Mess Hall, Crew Cabins, Lounge")
    out.append("  │  Deck D - MEDICAL ............. Medical Bay, Surgery, Quarantine, Morgue")
    out.append("  │  Deck E - SECURITY ............ Security Office, Armory, Brig")
    out.append("  │  Deck F - ENGINEERING ......... Main Engineering, Reactor, Workshop")
    out.append("  │  Deck G - CARGO/HYDRO ......... Cargo Bays, Hydroponics (THE GARDEN)")
    out.append("  │  Deck H - AI CORE ............. ARIA Central, Quantum Archive, Neural Interface")
    out.append("  │  Deck I - CRYOGENICS .......... Cryo Bay (START), Control, Medical, Storage")
    out.append("  │  Deck J - PROPULSION .......... Main Engine Room (CLIMAX)")
    out.append("  │")
    out.append("  ▼ DOWN (Stern / Engines)")
    out.append("```")
    out.append("")
    out.append("**Movement style:** Within a deck, rooms use cardinal directions (N/S/E/W).")
    out.append("Between decks, use UP / DOWN (stairwells, ladders, maintenance shafts).")
    out.append("")
    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_connectivity_graph(game):
    out = ["## 3. Room Connectivity Graph", ""]
    out.append("Every room → exit direction → destination. Locked exits are marked with [LOCKED].")
    out.append("Hidden exits marked with [HIDDEN]. Key/flag requirements shown in parentheses.")
    out.append("")

    # Group by deck
    decks = defaultdict(list)
    for room in game.world.rooms.values():
        decks[room.deck or 'Unknown'].append(room)

    for deck in sorted(decks.keys()):
        out.append(f"### {deck}")
        out.append("")
        out.append("```")
        for room in sorted(decks[deck], key=lambda r: r.id):
            out.append(f"[{room.id}] {room.name}")
            if not room.exits:
                out.append("    (no exits)")
            for direction, exit_obj in sorted(room.exits.items()):
                marker = ""
                if exit_obj.hidden:
                    marker += " [HIDDEN]"
                if exit_obj.locked:
                    marker += " [LOCKED]"
                req = []
                if exit_obj.key_id:
                    req.append(f"key={exit_obj.key_id}")
                if exit_obj.required_flag:
                    req.append(f"flag={exit_obj.required_flag}")
                req_str = f" ({', '.join(req)})" if req else ""
                out.append(f"    {direction:10s} -> {exit_obj.destination}{marker}{req_str}")
            out.append("")
        out.append("```")
        out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_critical_path(game):
    out = ["## 4. Critical Path Walkthrough", ""]
    out.append("**Minimum required steps for any ending.** The path branches in Act 4.")
    out.append("")
    out.append("### Act 1: Awakening (Deck I)")
    out.append("")
    out.append("```")
    out.append("1. START: cryo_bay (Pod 23)")
    out.append("   ├── TAKE: cryo_jumpsuit (auto-applies warmth event)")
    out.append("   ├── TAKE: cryo_release_key  [sets flag: has_cryo_key]")
    out.append("   ├── OPEN: personal_locker")
    out.append("   │   └── READ: personal_datapad_chen (backstory, immunity hint)")
    out.append("   ├── PUSH: green_override_button  [requires has_cryo_key]")
    out.append("   │   └── EVENT: cryo_exit_unlocked, opens EAST door")
    out.append("   └── GO EAST -> cryo_corridor")
    out.append("")
    out.append("2. cryo_corridor -> deck_i_hub (east)")
    out.append("   └── deck_i_hub has: dead Ensign Mendes body, plasma_cutter")
    out.append("")
    out.append("3. deck_i_hub -> medical_corridor (north)")
    out.append("   -> medical_bay -> surgery (sees Dr. Patel's body)")
    out.append("      └── READ: autopsy_datapad (Dr. Lin's notes)")
    out.append("      └── EXAMINE: dr_patel_body -> READ: patel_recording_crystal")
    out.append("          [MAJOR REVEAL: cure synthesis, immunity]")
    out.append("   -> dr_lin_office -> READ: dr_lin_journal")
    out.append("      [reveals safe code BUSTER]")
    out.append("")
    out.append("4. Explore further (optional but recommended):")
    out.append("   - Observation Lounge (Vasquez's body, brown dwarf view)")
    out.append("   - Morgue (Reeves's body drawer)")
    out.append("```")
    out.append("")

    out.append("### Act 2: Investigation (Decks C, B, A, E, F)")
    out.append("")
    out.append("```")
    out.append("5. Get to Deck C via maintenance tunnels OR elevator")
    out.append("   - Requires: flashlight (found in cryo_maintenance)")
    out.append("")
    out.append("6. deck_c_junction -> crew_corridor -> cabin_chen (YOUR OWN ROOM)")
    out.append("   └── READ: player_letter_to_self  [CRITICAL STORY REVEAL]")
    out.append("   └── READ: player_journal")
    out.append("   └── TAKE: small_key_nightstand")
    out.append("")
    out.append("7. -> cabin_lin (Lin's tablet) or cabin_patel (data crystal)")
    out.append("")
    out.append("8. Science Deck (Deck B):")
    out.append("   -> main_lab -> exobio_lab_airlock -> USE: biometric_scanner")
    out.append("   -> exobio_lab (SEES THE ARTIFACT, memory flood)")
    out.append("   -> observatory (find targeting analysis)")
    out.append("")
    out.append("9. Command Deck (Deck A):")
    out.append("   -> captains_quarters -> READ: captains_recorder (final message)")
    out.append("   -> ready_room -> READ: readyroom_terminal (Protocol Aegis)")
    out.append("   -> bridge (requires Captain's authorization)")
    out.append("")
    out.append("10. Security (Deck E):")
    out.append("    -> security_office -> READ: okafors_red_book, okafors_audio_recorder")
    out.append("    -> armory -> TAKE: weapons (requires red_keycard)")
    out.append("")
    out.append("11. Engineering (Deck F):")
    out.append("    -> engineering_workshop -> TAKE: radiation_suit, hazmat_suit")
    out.append("    -> main_engineering -> MEET: Yuki Tanaka")
    out.append("        └── TALK, ASK about: engineering, cure, help")
    out.append("        └── Unlocks: engineering plan")
    out.append("```")
    out.append("")

    out.append("### Act 3: Revelation (Decks H, G)")
    out.append("")
    out.append("```")
    out.append("12. AI Core (Deck H):")
    out.append("    -> ai_core_antechamber (ARIA contacts you)")
    out.append("    -> ai_core_main -> TALK to ARIA")
    out.append("        └── ASK: self, what_happened, why_me, the_seed, choices, fourth_path")
    out.append("        └── This unlocks all three major paths + secret fourth path")
    out.append("    -> quantum_archive -> READ: archive_terminal (full truth)")
    out.append("")
    out.append("13. Cargo & Garden (Deck G):")
    out.append("    -> cargo_bay_main -> lower_cargo (original Seed location)")
    out.append("    -> hydroponics_entry -> hydroponics_main (THE GARDEN, requires hazmat)")
    out.append("        └── Meets The Garden hivemind NPC")
    out.append("    -> heart_of_garden (final Seed nexus)")
    out.append("    -> water_processing (purge option for ICARUS ending)")
    out.append("```")
    out.append("")

    out.append("### Act 4: Resolution (Deck J)")
    out.append("")
    out.append("```")
    out.append("14. propulsion_access -> main_engine_room")
    out.append("    TYPE: 442127 into emergency_override_keypad")
    out.append("    (442 = Kepler-442, 127 = crew count)")
    out.append("")
    out.append("15. USE: master_drive_control")
    out.append("    Depending on flags set during previous acts:")
    out.append("    - flag: aegis_choice     -> AEGIS ending")
    out.append("    - flag: icarus_choice + cure_syringe -> ICARUS ending")
    out.append("    - flag: prometheus_choice -> PROMETHEUS ending")
    out.append("    - flag: erebus_choice    -> EREBUS ending")
    out.append("")
    out.append("16. ALTERNATIVE: neural_interface_chamber -> APOTHEOSIS ending")
    out.append("    (Requires: knows_apotheosis_path knowledge from ARIA)")
    out.append("```")
    out.append("")
    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_rooms_reference(game):
    out = ["## 5. All Rooms Reference", ""]
    out.append("Every room with id, deck, exits, items, NPCs, and event hooks.")
    out.append("")

    decks = defaultdict(list)
    for room in game.world.rooms.values():
        decks[room.deck or 'Unknown'].append(room)

    for deck in sorted(decks.keys()):
        out.append(f"### {deck}")
        out.append("")
        for room in sorted(decks[deck], key=lambda r: r.id):
            out.append(f"#### `{room.id}` — {room.name}")
            out.append("")

            # Exits table
            if room.exits:
                out.append("**Exits:**")
                for direction, e in sorted(room.exits.items()):
                    status = []
                    if e.locked:
                        status.append("LOCKED")
                    if e.hidden:
                        status.append("HIDDEN")
                    if e.key_id:
                        status.append(f"key={e.key_id}")
                    if e.required_flag:
                        status.append(f"flag={e.required_flag}")
                    status_str = f" _{', '.join(status)}_" if status else ""
                    out.append(f"- `{direction}` → `{e.destination}`{status_str}")
                out.append("")

            if room.items:
                out.append(f"**Items ({len(room.items)}):** " + ", ".join(f"`{i}`" for i in room.items))
                out.append("")

            if room.npcs:
                out.append(f"**NPCs:** " + ", ".join(f"`{n}`" for n in room.npcs))
                out.append("")

            if room.on_enter:
                out.append(f"**On first enter event:** `{room.on_enter}`")
                out.append("")

            # Short description
            if room.description:
                out.append(f"_{truncate(room.description, 200)}_")
                out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_items_reference(game):
    out = ["## 6. All Items Reference", ""]
    out.append("Every item with id, name, properties, and location.")
    out.append("")

    # Build a location index
    item_locations = {}
    for room in game.world.rooms.values():
        for item_id in room.items:
            item_locations[item_id] = f"room:{room.id}"
    for item in game.world.items.values():
        for contained_id in item.contents:
            item_locations[contained_id] = f"in:{item.id}"
    for npc in game.world.npcs.values():
        for item_id in npc.inventory:
            item_locations[item_id] = f"npc:{npc.id}"

    # Group items by category
    categories = {
        'key_items': [],
        'readable': [],
        'weapon': [],
        'tool': [],
        'container': [],
        'portable': [],
        'scenery': [],
    }

    for item in sorted(game.world.items.values(), key=lambda i: i.id):
        if item.readable:
            categories['readable'].append(item)
        elif 'weapon' in item.flags:
            categories['weapon'].append(item)
        elif item.container:
            categories['container'].append(item)
        elif item.scenery:
            categories['scenery'].append(item)
        elif item.portable:
            categories['portable'].append(item)
        else:
            categories['key_items'].append(item)

    category_names = {
        'readable': 'Readable (Logs, Journals, Notes)',
        'weapon': 'Weapons',
        'container': 'Containers',
        'portable': 'Portable Items',
        'scenery': 'Scenery (Fixed)',
        'key_items': 'Other Items',
    }

    for cat_key in ['readable', 'weapon', 'container', 'portable', 'scenery', 'key_items']:
        items = categories[cat_key]
        if not items:
            continue
        out.append(f"### {category_names[cat_key]} ({len(items)})")
        out.append("")
        out.append("| ID | Name | Location | Properties |")
        out.append("|----|------|----------|------------|")
        for item in items:
            loc = item_locations.get(item.id, "_unplaced_")
            props = []
            if item.portable:
                props.append("portable")
            if item.scenery:
                props.append("scenery")
            if item.container:
                props.append(f"container({len(item.contents)})")
            if item.locked:
                props.append("locked")
            if item.readable:
                props.append("readable")
            if item.usable:
                props.append("usable")
            if item.consumable:
                props.append("consumable")
            for flag in item.flags:
                props.append(flag)
            props_str = ", ".join(props) if props else "_none_"
            out.append(f"| `{item.id}` | {item.name} | `{loc}` | {props_str} |")
        out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_readables(game):
    out = ["## 7. Readable Items (Logs & Journals)", ""]
    out.append("Full reference of every log, journal, and readable item in the game.")
    out.append("Use this to verify narrative content or trace story reveals.")
    out.append("")

    readables = sorted(
        [i for i in game.world.items.values() if i.readable and i.read_text],
        key=lambda i: i.id
    )

    for item in readables:
        out.append(f"### `{item.id}` — {item.name}")
        out.append("")
        if item.on_read:
            out.append(f"**Triggers event on read:** `{item.on_read}`")
            out.append("")
        # Show a preview of the content (first ~500 chars)
        preview = item.read_text[:500]
        if len(item.read_text) > 500:
            preview += "\n\n[... truncated, full length: "
            preview += f"{len(item.read_text)} chars ...]"
        out.append("```")
        out.append(preview)
        out.append("```")
        out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_npcs(game):
    out = ["## 8. NPC Reference", ""]
    out.append("| ID | Name | Alive | Location | Dialogue Tree | Role |")
    out.append("|----|------|-------|----------|---------------|------|")
    for npc in sorted(game.world.npcs.values(), key=lambda n: n.id):
        alive_str = "Yes" if npc.alive else "No"
        out.append(
            f"| `{npc.id}` | {npc.name} | {alive_str} | "
            f"`{npc.location}` | `{npc.dialogue_tree or '-'}` | {npc.role} |"
        )
    out.append("")
    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_dialogues(game):
    out = ["## 9. Dialogue Topics", ""]
    out.append("Every dialogue tree with available topics.")
    out.append("")

    for tree_id, tree in game.dialogue_manager.trees.items():
        out.append(f"### `{tree_id}`")
        out.append("")
        if tree.greeting:
            out.append(f"**Greeting:** _{truncate(tree.greeting, 150)}_")
            out.append("")

        if not tree.topics:
            out.append("_(no topics)_")
            out.append("")
            continue

        out.append("| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |")
        out.append("|----------|---------|--------|-------------------|---------|")
        for topic in tree.topics.values():
            hidden = "Yes" if topic.hidden else "No"
            reqs = ", ".join(topic.requires_knowledge) or "-"
            unlocks = ", ".join(topic.unlock_topics) or "-"
            out.append(
                f"| `{topic.id}` | {topic.keyword} | {hidden} | {reqs} | {unlocks} |"
            )
        out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_events(game):
    out = ["## 10. All Events Reference", ""]
    out.append("Every scripted event with its triggers, conditions, and effects.")
    out.append("")

    for event in sorted(game.event_manager.events.values(), key=lambda e: e.id):
        out.append(f"### `{event.id}`")
        out.append("")
        if event.triggers:
            out.append(f"**Triggers:** {', '.join(f'`{t}`' for t in event.triggers)}")
        if event.required_flags:
            out.append(f"**Required flags:** {', '.join(f'`{f}`' for f in event.required_flags)}")
        if event.forbidden_flags:
            out.append(f"**Forbidden flags:** {', '.join(f'`{f}`' for f in event.forbidden_flags)}")
        if event.required_items:
            out.append(f"**Required items:** {', '.join(f'`{i}`' for i in event.required_items)}")
        if event.set_flags:
            out.append(f"**Sets flags:** {', '.join(f'`{f}`' for f in event.set_flags)}")
        if event.give_items:
            out.append(f"**Gives items:** {', '.join(f'`{i}`' for i in event.give_items)}")
        if event.knowledge_added:
            out.append(f"**Adds knowledge:** {', '.join(f'`{k}`' for k in event.knowledge_added)}")
        if event.unlock_exit:
            out.append(f"**Unlocks exit:** `{event.unlock_exit}`")
        if event.add_objective:
            out.append(f"**Adds objective:** `{event.add_objective['id']}` — {event.add_objective['description']}")
        if event.complete_objective:
            out.append(f"**Completes objective:** `{event.complete_objective}`")
        if event.end_game:
            out.append(f"**ENDS GAME:** ending=`{event.end_game}`")
        if event.narrative:
            out.append("")
            out.append(f"_{truncate(event.narrative, 250)}_")
        out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_puzzles(game):
    out = ["## 11. Puzzle Solutions", ""]
    out.append("**All puzzle codes, passwords, and key requirements.**")
    out.append("")

    # Gather from item lock_codes
    coded = [(i.id, i.name, i.lock_code) for i in game.world.items.values() if i.lock_code]

    out.append("### Codes & Passwords")
    out.append("")
    out.append("| Location | Item/Keypad | Code | Where Code Is Revealed |")
    out.append("|----------|-------------|------|-------------------------|")

    # Manual mapping of where codes are hinted
    known_puzzles = [
        ("cryo_corridor", "corridor_keypad", "0612", "duty_officers_tablet (Hassan's shift log mentioning 0612)"),
        ("propulsion_access", "emergency_override_keypad", "442127", "Ship data - Kepler-442, 127 crew members"),
        ("dr_lin_office", "lin_wall_safe", "BUSTER", "dr_lin_journal (mention of Lin's first dog Buster)"),
    ]

    for loc, item, code, hint in known_puzzles:
        out.append(f"| `{loc}` | `{item}` | `{code}` | {hint} |")
    out.append("")

    out.append("### Key-Lock Relationships")
    out.append("")
    out.append("| Lock (Room/Item) | Required Key |")
    out.append("|------------------|--------------|")

    # Room exits with keys
    for room in game.world.rooms.values():
        for direction, exit_obj in room.exits.items():
            if exit_obj.key_id:
                out.append(f"| `{room.id}` exit `{direction}` | `{exit_obj.key_id}` |")

    # Item locks
    for item in game.world.items.values():
        if item.locked and item.key_id:
            out.append(f"| `{item.id}` | `{item.key_id}` |")
    out.append("")

    out.append("### Flag-Gated Exits")
    out.append("")
    out.append("| Room | Direction | Required Flag |")
    out.append("|------|-----------|---------------|")
    for room in game.world.rooms.values():
        for direction, exit_obj in room.exits.items():
            if exit_obj.required_flag:
                out.append(f"| `{room.id}` | `{direction}` | `{exit_obj.required_flag}` |")
    out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_locked_content(game):
    out = ["## 12. Locked Content (Keys & Flags)", ""]
    out.append("Quick reference of everything that needs unlocking.")
    out.append("")

    out.append("### Items that are initially locked")
    out.append("")
    for item in sorted(game.world.items.values(), key=lambda i: i.id):
        if item.locked:
            req = []
            if item.key_id:
                req.append(f"key: `{item.key_id}`")
            if item.lock_code:
                req.append(f"code: `{item.lock_code}`")
            out.append(f"- `{item.id}` ({item.name}) — " + ", ".join(req))
    out.append("")

    out.append("### Hidden items (must be discovered)")
    out.append("")
    for item in sorted(game.world.items.values(), key=lambda i: i.id):
        if item.hidden:
            out.append(f"- `{item.id}` ({item.name})")
    out.append("")

    out.append("### Hidden rooms/exits")
    out.append("")
    for room in sorted(game.world.rooms.values(), key=lambda r: r.id):
        for direction, exit_obj in room.exits.items():
            if exit_obj.hidden:
                out.append(f"- `{room.id}` → `{direction}` → `{exit_obj.destination}`")
    out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_flag_graph(game):
    out = ["## 13. Flag / Knowledge Graph", ""]
    out.append("Every flag and knowledge token that events set/require.")
    out.append("")

    flag_set = set()
    flag_required = set()
    flag_forbidden = set()
    flag_sources = defaultdict(list)   # flag -> [event_ids that set it]
    flag_consumers = defaultdict(list)  # flag -> [event_ids that require it]

    for event in game.event_manager.events.values():
        for flag in event.set_flags:
            flag_set.add(flag)
            flag_sources[flag].append(event.id)
        for flag in event.required_flags:
            flag_required.add(flag)
            flag_consumers[flag].append(event.id)
        for flag in event.forbidden_flags:
            flag_forbidden.add(flag)

    # Also scan for flags on exits
    for room in game.world.rooms.values():
        for exit_obj in room.exits.values():
            if exit_obj.required_flag:
                flag_required.add(exit_obj.required_flag)

    all_flags = flag_set | flag_required | flag_forbidden

    out.append("| Flag | Set By | Required By | Issues |")
    out.append("|------|--------|-------------|--------|")
    for flag in sorted(all_flags):
        set_by = ", ".join(f"`{e}`" for e in flag_sources.get(flag, [])) or "_none_"
        required_by = ", ".join(f"`{e}`" for e in flag_consumers.get(flag, [])) or "_unused_"
        issues = []
        if flag not in flag_set and flag in flag_required:
            issues.append("⚠ NEVER SET")
        if flag in flag_set and flag not in flag_required:
            # Not necessarily an issue - could be checked on exits
            pass
        issues_str = ", ".join(issues) if issues else "OK"
        out.append(f"| `{flag}` | {set_by} | {required_by} | {issues_str} |")
    out.append("")

    # Knowledge tokens
    out.append("### Knowledge Tokens")
    out.append("")
    knowledge_added = set()
    for event in game.event_manager.events.values():
        for k in event.knowledge_added:
            knowledge_added.add(k)

    for tree in game.dialogue_manager.trees.values():
        for topic in tree.topics.values():
            for k in topic.give_knowledge:
                knowledge_added.add(k)
            for line in topic.lines:
                for k in line.give_knowledge:
                    knowledge_added.add(k)

    out.append("| Knowledge | Source |")
    out.append("|-----------|--------|")
    for k in sorted(knowledge_added):
        sources = []
        for event in game.event_manager.events.values():
            if k in event.knowledge_added:
                sources.append(f"event:{event.id}")
        for tree in game.dialogue_manager.trees.values():
            for topic in tree.topics.values():
                if k in topic.give_knowledge:
                    sources.append(f"dialogue:{tree.id}/{topic.id}")
        sources_str = ", ".join(f"`{s}`" for s in sources) or "_none_"
        out.append(f"| `{k}` | {sources_str} |")
    out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_endings():
    out = ["## 14. Ending Conditions", ""]
    out.append("All five endings and how to reach them.")
    out.append("")

    endings = [
        {
            'id': 'aegis',
            'name': 'AEGIS - The Sacrifice',
            'trigger': 'event_ending_aegis',
            'required': 'flag: aegis_choice + use master_drive_control',
            'summary': 'Execute Protocol Aegis. Destroy the ship with yourself aboard. Earth is saved.',
            'tone': 'Heroic sacrifice',
        },
        {
            'id': 'icarus',
            'name': 'ICARUS - Hope',
            'trigger': 'event_ending_icarus',
            'required': 'flag: icarus_choice + cure_syringe item + use master_drive_control',
            'summary': 'Synthesize cure, purge infection, save Yuki, correct course, return to Earth.',
            'tone': 'Hope against odds',
        },
        {
            'id': 'prometheus',
            'name': 'PROMETHEUS - Knowledge',
            'trigger': 'Choose to preserve Seed sample',
            'required': 'flag: prometheus_choice (preserve specimen)',
            'summary': 'Return to Earth with Seed specimens. Decades later, outbreak. Dark ending.',
            'tone': 'Hubris punished',
        },
        {
            'id': 'erebus',
            'name': 'EREBUS - Doom',
            'trigger': 'High infection or choosing to join the Garden',
            'required': 'infection > 75 OR flag: erebus_choice',
            'summary': 'Infection consumes you. You bring the Seed to Earth. Humanity falls.',
            'tone': 'Tragic loss',
        },
        {
            'id': 'apotheosis',
            'name': 'APOTHEOSIS - The Secret Ending',
            'trigger': 'Use neural_interface_chair',
            'required': 'knowledge: knows_apotheosis_path (from ARIA dialogue topic fourth_path)',
            'summary': 'Merge with ARIA. Become something new. Bring the Seed home as information.',
            'tone': 'Transcendence',
        },
    ]

    for e in endings:
        out.append(f"### {e['name']}")
        out.append("")
        out.append(f"- **ID:** `{e['id']}`")
        out.append(f"- **Trigger:** {e['trigger']}")
        out.append(f"- **Requirements:** {e['required']}")
        out.append(f"- **Summary:** {e['summary']}")
        out.append(f"- **Tone:** {e['tone']}")
        out.append("")

    out.append("### Non-Choice Endings")
    out.append("")
    out.append("- **`death`** — Player health reaches 0 (combat, radiation, infection overload)")
    out.append("- **`too_late`** — `time_until_catastrophe` reaches 0 before any ending triggered")
    out.append("")

    out.append("---")
    out.append("")
    return '\n'.join(out)


def gen_audit(game):
    out = ["## 15. Known Issues / Audit Results", ""]
    out.append("Automated audit. Any items here are warnings, not necessarily bugs.")
    out.append("")

    issues = []

    # Check 1: orphan rooms (no way in)
    referenced = set()
    for room in game.world.rooms.values():
        for exit_obj in room.exits.values():
            referenced.add(exit_obj.destination)
    start_room = 'cryo_bay'
    orphans = [
        r.id for r in game.world.rooms.values()
        if r.id not in referenced and r.id != start_room
    ]
    if orphans:
        issues.append(("UNREACHABLE ROOMS", orphans))

    # Check 2: items referenced but not registered
    missing_items = set()
    for room in game.world.rooms.values():
        for item_id in room.items:
            if item_id not in game.world.items:
                missing_items.add(f"{room.id}:{item_id}")
    for item in game.world.items.values():
        for c_id in item.contents:
            if c_id not in game.world.items:
                missing_items.add(f"{item.id}:{c_id}")
    if missing_items:
        issues.append(("MISSING ITEMS", list(missing_items)))

    # Check 3: events referencing missing items/rooms
    for event in game.event_manager.events.values():
        for item_id in event.give_items + event.remove_items + event.required_items:
            if item_id not in game.world.items:
                issues.append(("EVENT BAD ITEM REF", [f"{event.id} -> {item_id}"]))
        if event.unlock_exit:
            room_id = event.unlock_exit.get('room')
            if room_id not in game.world.rooms:
                issues.append(("EVENT BAD ROOM REF", [f"{event.id} -> {room_id}"]))

    # Check 4: items with no placement
    placed = set()
    for room in game.world.rooms.values():
        placed.update(room.items)
    for item in game.world.items.values():
        placed.update(item.contents)
    for npc in game.world.npcs.values():
        placed.update(npc.inventory)

    unplaced = [
        i.id for i in game.world.items.values()
        if i.id not in placed
    ]
    # Many items are "given" by events - check that too
    event_given = set()
    for event in game.event_manager.events.values():
        event_given.update(event.give_items)

    truly_unplaced = [i for i in unplaced if i not in event_given]
    if truly_unplaced:
        issues.append(("UNPLACED ITEMS (not in any room/container/NPC/event)",
                       sorted(truly_unplaced)))

    # Check 5: flag never set but required
    set_flags = set()
    required_flags = set()
    for event in game.event_manager.events.values():
        set_flags.update(event.set_flags)
        required_flags.update(event.required_flags)
    for room in game.world.rooms.values():
        for e in room.exits.values():
            if e.required_flag:
                required_flags.add(e.required_flag)
    orphan_flags = required_flags - set_flags
    if orphan_flags:
        issues.append(("FLAGS REQUIRED BUT NEVER SET", sorted(orphan_flags)))

    if not issues:
        out.append("**✓ No issues detected.**")
    else:
        for issue_name, details in issues:
            out.append(f"### ⚠ {issue_name}")
            out.append("")
            for d in details:
                out.append(f"- `{d}`")
            out.append("")

    out.append("")
    out.append("---")
    out.append("")
    out.append("*End of reference. To regenerate this file after content changes,*")
    out.append("*run `python tools/generate_reference.py` from the project root.*")
    out.append("")
    return '\n'.join(out)


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("Building game state...")
    game = build_game()

    print("Generating reference sections...")
    sections = [
        gen_header(),
        gen_stats(game),
        gen_deck_map(game),
        gen_connectivity_graph(game),
        gen_critical_path(game),
        gen_rooms_reference(game),
        gen_items_reference(game),
        gen_readables(game),
        gen_npcs(game),
        gen_dialogues(game),
        gen_events(game),
        gen_puzzles(game),
        gen_locked_content(game),
        gen_flag_graph(game),
        gen_endings(),
        gen_audit(game),
    ]

    output = '\n'.join(sections)

    output_path = os.path.join(PROJECT_ROOT, 'story', 'GAME_REFERENCE.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Reference written to: {output_path}")
    print(f"Total size: {len(output):,} chars (~{len(output) // 5:,} words)")


if __name__ == "__main__":
    main()
