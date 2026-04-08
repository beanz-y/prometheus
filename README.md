# THE PROMETHEUS PROTOCOL

A narrative-heavy interactive fiction game inspired by Zork, Hitchhiker's Guide to the Galaxy, and classic sci-fi horror (System Shock 2, Dead Space, Event Horizon, Alien, SOMA).

You are **Dr. Alex Chen**, Chief Xenobiologist of the ISV *Prometheus* - a kilometer-long interstellar research vessel. You awaken from emergency cryogenic stasis to find the crew dead or missing, the ship drifting toward a rogue brown dwarf, and only 18 hours before the ship is torn apart.

You have no memory of the last 18 months. The ship's AI, **ARIA**, has kept you alive for a reason. The reason may be the only hope humanity has.

## Running the Game

**Requirements:** Python 3.8+  (no external dependencies)

```bash
cd prometheus
python main.py
```

The game auto-detects whether your terminal supports Unicode and falls back to ASCII if not. Colors work in any modern terminal (including Windows 10+ cmd, PowerShell, Terminal, macOS Terminal, and most Linux terminals).

## Basic Commands

### Movement
- `north`, `south`, `east`, `west`, `up`, `down`
- Shortcuts: `n`, `s`, `e`, `w`, `u`, `d`
- `go <direction>`, `enter <place>`

### Observation
- `look` - describe current room
- `examine <thing>` (or `x <thing>`) - look closely at something
- `search <area>` - search for hidden items
- `read <item>` - read a document
- `listen`, `smell`, `touch` - use other senses

### Inventory
- `take <item>`, `get <item>`, `grab <item>`
- `drop <item>`
- `inventory` (or `i`) - list what you're carrying
- `take all` - grab everything in the room

### Interaction
- `open <X>`, `close <X>`
- `unlock <X>` (with appropriate key)
- `use <X>`, `use <X> on <Y>`
- `type <code> into <keypad>`
- `insert <X> into <Y>`
- `combine <X> with <Y>`
- `push <X>`, `pull <X>`, `turn <X>`

### Social
- `talk to <npc>`
- `ask <npc> about <topic>`
- `say <text>`
- `give <item> to <npc>`

### Meta
- `save [slot]` / `load [slot]` - save/load game
- `status` - check health, sanity, time remaining
- `objectives` - review current quest log
- `think` - review what you've learned
- `map` - see discovered locations
- `help` - full command reference
- `hint` - get a contextual hint
- `quit` - exit game

## Compound Commands

One of the Prometheus Protocol's unique features is a powerful command parser that lets you chain actions:

```
take key and unlock door
go north then take card
shoot enemy while moving to cover
take keycard, read log, go east
```

You can even use quoted strings to input specific text:

```
type "override alpha" into console
type "4815" into keypad
```

### Conjunctions
- `and`, `,` - sequential actions
- `then`, `next`, `after` - sequential actions
- `while`, `whilst`, `as` - simultaneous actions (noted narratively)

## Gameplay Tips

1. **Read everything.** The story is told through crew logs, personal journals, and environmental details. The readable items contain crucial puzzle clues and backstory.

2. **Examine scenery, not just items.** Bodies, consoles, stains, graffiti - many things can be examined for clues.

3. **Time is limited.** You have 18 in-game hours (roughly 1080 turns) before the ship falls into GRB-7734. Don't waste turns, but also don't rush past important clues.

4. **Talk to ARIA when you find her.** She has answers to many questions, but she won't volunteer them. Ask specific topics.

5. **Trust your gut, then verify.** The game's narrative includes unreliable memories, mysterious messages, and characters who may be lying. Cross-reference sources.

6. **Save often.** Save before making major decisions - there are 5 distinct endings, each accessible through different choices.

7. **Manage your sanity.** Seeing horrors will lower your sanity. Low sanity can distort your perceptions. Find safe moments. Rest.

8. **The Seed is in you.** You have low-level infection that increases in certain areas. A high infection level affects your choices and ending possibilities.

## The Five Endings

Without spoiling specifics, the game has multiple endings based on choices you make throughout:

- **AEGIS** - The sacrifice ending. Execute Captain Reeves's original protocol.
- **ICARUS** - The hope ending. Synthesize the cure, save the crew, course-correct.
- **PROMETHEUS** - The knowledge ending. Return with specimens for study.
- **EREBUS** - The dark ending. Succumb to the infection.
- **APOTHEOSIS** - The secret ending. Requires specific actions. Look for clues about the Neural Interface Chamber.

## Project Structure

```
prometheus/
├── main.py                    # Entry point
├── README.md                  # This file
├── engine/                    # Game engine (modular, reusable)
│   ├── __init__.py
│   ├── game.py               # Main game loop and command handlers
│   ├── parser.py             # Advanced multi-command parser
│   ├── world.py              # World state manager
│   ├── room.py               # Room class
│   ├── item.py               # Item class
│   ├── npc.py                # NPC class
│   ├── player.py             # Player character
│   ├── event.py              # Event/trigger system
│   ├── dialogue.py           # Dialogue trees
│   ├── save_load.py          # Save/load system
│   └── display.py            # Text output, colors, effects
├── content/                   # Game content (edit to expand the story)
│   ├── __init__.py
│   ├── intro.py              # Opening sequence
│   ├── rooms_act1.py         # Deck I, Deck D rooms
│   ├── rooms_act2.py         # Decks H, F, E, C, B, A rooms
│   ├── rooms_act3.py         # AI Core, Garden, deep rooms
│   ├── items.py              # All items and readables
│   ├── npcs.py               # Non-player characters
│   ├── dialogues.py          # Dialogue trees
│   ├── events.py             # Story events and triggers
│   └── endings.py            # The five endings
├── story/                     # Reference materials for authors
│   └── world_bible.md        # Complete story/character reference
└── saves/                     # Save game directory (auto-created)
```

## Extending the Game

The engine is designed to be data-driven. You can easily add content:

### Add a New Room

Edit any `rooms_act*.py` file:

```python
world.add_room(Room(
    id="my_new_room",
    name="My New Room",
    deck="Deck F - Engineering",
    description="A richly detailed description...",
    exits={
        'north': Exit(direction='north', destination='existing_room'),
    },
    items=["some_item_id"],
))
```

### Add a New Item

Edit `items.py`:

```python
world.add_item(Item(
    id="my_item",
    name="mysterious object",
    aliases=["object", "thing"],
    description="Long description shown when examined.",
    portable=True,
    readable=True,
    read_text="Text shown when the item is read.",
))
```

### Add a New Event

Edit `events.py`:

```python
event_manager.add_event(Event(
    id="event_something_happens",
    triggers=["enter:my_new_room", "take:my_item"],
    required_flags=["some_flag"],
    narrative="Description of what the player sees/feels.",
    set_flags=["new_flag"],
    give_items=["reward_item"],
))
```

### Event Triggers Supported

- `enter:<room_id>` - Entering a specific room
- `examine:<item_id>` - Examining an item
- `take:<item_id>` - Taking an item
- `read:<item_id>` - Reading an item
- `use:<item_id>` - Using an item
- `use:<item_id>:<target_id>` - Using item on target
- `talk:<npc_id>` - Talking to an NPC
- `push:<item_id>` - Pushing a button/object
- `type:<item_id>:<text>` - Typing specific text into something
- `attack:<npc_id>` - Attacking an NPC
- Custom triggers can be fired from anywhere via `game.event_manager.fire_trigger()`

## Credits

- **Design & Implementation:** Claude Opus 4.6
- **Inspired by:** Infocom's Zork, Infocom's Hitchhiker's Guide to the Galaxy, Looking Glass Studios' System Shock 2, Visceral Games' Dead Space, Paul W.S. Anderson's Event Horizon, Ridley Scott's Alien, Frictional Games' SOMA, Stanisław Lem's Solaris, Arthur C. Clarke's 2001: A Space Odyssey

## License

Personal/educational use. Modify freely.

---

*"We sent the ISV Prometheus to find out who was calling.*
*We found out.*
*We should not have gone looking."*

 - From the final entry of Captain Marcus Reeves, Day 423
