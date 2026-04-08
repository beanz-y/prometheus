"""
Main game loop and command dispatcher.

This is the heart of the engine - it receives commands from the parser
and executes them against the world state, triggering events as needed.
"""

import os
import sys
import random
from typing import Optional

from .display import Display, Color
from .parser import Parser, Command, CommandSequence
from .world import World
from .player import Player
from .event import EventManager
from .dialogue import DialogueManager
from .save_load import SaveLoadManager
from .companion import Companion


# Weapon effectiveness - damage by weapon and target type
WEAPON_DAMAGE = {
    'scalpel': {'default': 5, 'infected': 8},
    'wrench': {'default': 10, 'infected': 12},
    'sharp_knife': {'default': 8, 'infected': 10},
    'handgun': {'default': 20, 'infected': 25, 'garden_node': 15},
    'tactical_rifle': {'default': 30, 'infected': 35, 'garden_node': 25},
    'plasma_cutter': {'default': 15, 'infected': 20, 'garden_node': 35},
    'ceremonial_sidearm': {'default': 18, 'infected': 22},
    'surgical_saw': {'default': 12, 'infected': 15},
    'tear_gas_grenades': {'default': 0, 'stun_turns': 3},  # Non-lethal
    'sedative_syringe': {'default': 0, 'sedate': True},  # Non-lethal, single-target
}


class Game:
    """Main game controller."""

    def __init__(self):
        self.display = Display(use_color=True, use_typewriter=True, typewriter_speed=0.008)
        self.parser = Parser()
        self.world = World()
        self.player = Player()
        self.event_manager = EventManager()
        self.dialogue_manager = DialogueManager()
        # Saves go next to the .exe (or script), not in the temp bundle dir
        if getattr(sys, 'frozen', False):
            save_dir = os.path.join(os.path.dirname(sys.executable), "saves")
        else:
            save_dir = "saves"
        self.save_manager = SaveLoadManager(save_dir=save_dir)

        self.companion = Companion()

        self.running = False
        self.ended = False
        self.ending_id: Optional[str] = None

        # Active conversation state
        self.talking_to: Optional[str] = None  # NPC ID

        # Combat state
        self._attacked_this_turn: bool = False

    # ─── Game Lifecycle ────────────────────────────────────────────────

    def start(self, skip_intro: bool = False):
        """Begin the game."""
        self.running = True

        if not skip_intro:
            self.show_intro()

        # Trigger intro events
        self.event_manager.fire_trigger("game_start", self)

        # Show starting room
        self.describe_current_room()

        # Main loop
        while self.running and not self.ended:
            try:
                self.game_turn()
            except KeyboardInterrupt:
                self.display.print("\n")
                self.display.print("Use 'quit' to exit the game.", color=Color.YELLOW)
                continue
            except EOFError:
                self.running = False
                break

        # Ending
        if self.ended:
            self.show_ending()

    def game_turn(self):
        """Execute a single turn of the game."""
        # Check for death
        if not self.player.is_alive():
            self.trigger_ending("death")
            return

        # Check time
        if self.player.time_until_catastrophe <= 0 and not self.player.has_flag("saved_ship"):
            self.trigger_ending("too_late")
            return

        # Get input
        try:
            raw_input = self.display.prompt("> ")
        except (KeyboardInterrupt, EOFError):
            raise

        if not raw_input.strip():
            return

        # Parse input
        sequence = self.parser.parse(raw_input)
        if not sequence:
            self.display.print("I don't understand.", color=Color.YELLOW)
            return

        # Check if the command is a "free action" that shouldn't cost time.
        # Status checks, help, meta commands, and failed parses are free.
        FREE_VERBS = {
            'status', 'inventory', 'help', 'hint', 'objectives', 'location',
            'think', 'map', 'save', 'load', 'quit',
        }
        first_verb = sequence.commands[0].verb if sequence.commands else ''
        is_free_action = first_verb in FREE_VERBS

        # Reset per-turn state
        self._attacked_this_turn = False

        # Execute commands
        self.execute_sequence(sequence)

        # Free actions (status, inventory, help, etc.) don't advance the clock
        if is_free_action:
            return

        # Process environmental hazards after movement
        self._process_environmental_hazards()

        # Process hostile NPC actions
        self._process_hostile_npcs()

        # Process hallucinations based on sanity
        self._process_hallucinations()

        # Advance time
        if not self.player.has_flag("paused_time"):
            if self.player.advance_time(1):
                # Time ran out
                if not self.player.has_flag("saved_ship"):
                    self.trigger_ending("too_late")
                    return

        # Advance NPC patrols
        self.world.advance_npc_patrols(self.player.turn_count, self.player.current_room)

        # Check timed events
        self.event_manager.check_timed_events(self)

    def execute_sequence(self, sequence: CommandSequence):
        """Execute a sequence of commands from a single input."""
        if sequence.simultaneous and len(sequence.commands) > 1:
            # Narrative flavor for simultaneous actions
            self.display.print("(Attempting to do multiple things at once...)",
                             color=Color.BRIGHT_BLACK)

        for i, command in enumerate(sequence.commands):
            if self.ended:
                break
            self.execute_command(command)
            # Small separator between compound commands
            if i < len(sequence.commands) - 1 and len(sequence.commands) > 1:
                self.display.print("", typewriter=False)

    def execute_command(self, command: Command):
        """Execute a single parsed command."""
        if not command.verb:
            return

        # Route to verb handler
        verb = command.verb
        handler = getattr(self, f"do_{verb}", None)
        if handler:
            handler(command)
        else:
            # Unknown verb
            self.display.print(f"I don't know how to '{command.verb}'.",
                             color=Color.YELLOW)
            self.display.hint("Try: look, examine, take, go, use, talk, inventory, help")

    # ─── Room Display ──────────────────────────────────────────────────

    def describe_current_room(self, brief: bool = False):
        """Print the current room description."""
        room = self.world.get_room(self.player.current_room)
        if not room:
            self.display.error("ERROR: You are nowhere.")
            return

        self.display.location(room.name)

        if not brief:
            desc = room.get_description(self.world.flags)
            self.display.describe(desc)

        # Mark as visited
        was_first_visit = not room.visited
        room.visited = True
        self.player.discovered_rooms.add(room.id)

        # List items
        visible_items = [
            self.world.get_item(iid) for iid in room.items
            if self.world.get_item(iid) and not self.world.get_item(iid).hidden
            and not self.world.get_item(iid).scenery
        ]
        if visible_items:
            self.display.print("")
            for item in visible_items:
                self.display.print(f"  • {item.get_short_description()}",
                                 color=Color.BRIGHT_WHITE)

        # List NPCs
        present_npcs = [
            self.world.get_npc(nid) for nid in room.npcs
            if self.world.get_npc(nid) and self.world.get_npc(nid).present
        ]
        if present_npcs:
            self.display.print("")
            for npc in present_npcs:
                # Show status-aware description
                if npc.has_flag('sedated'):
                    self.display.print(
                        f"  ▸ {npc.name} lies unconscious on the deck, breathing shallowly.",
                        color=Color.BRIGHT_BLACK
                    )
                elif not npc.alive:
                    desc = npc.short_description or f"{npc.name} (deceased)"
                    self.display.print(f"  ▸ {desc}",
                                     color=Color.BRIGHT_BLACK)
                elif npc.short_description:
                    self.display.print(f"  ▸ {npc.short_description}",
                                     color=Color.BRIGHT_CYAN)
                else:
                    self.display.print(f"  ▸ {npc.name}",
                                     color=Color.BRIGHT_CYAN)

        # Exits
        self.display.print("")
        self.display.print(room.get_exits_description(), color=Color.BRIGHT_BLUE)

        # Fire enter event
        if was_first_visit:
            self.event_manager.fire_trigger(f"enter:{room.id}", self)
            if room.on_enter:
                event = self.event_manager.get_event(room.on_enter)
                if event:
                    event.fire(self)
        else:
            if room.on_enter_repeat:
                event = self.event_manager.get_event(room.on_enter_repeat)
                if event:
                    event.fire(self)

        # Companion commentary
        comment = self.companion.get_commentary(room.id, self)
        if comment:
            self.display.print("")
            self.display.dialogue("Yuki", comment)

    # ─── Verb Handlers ─────────────────────────────────────────────────

    def do_look(self, command: Command):
        """Look around the current room."""
        if command.direct_object:
            # "look at X" was already converted to examine, but if they said
            # "look X", handle it here
            self.do_examine(command)
            return
        self.describe_current_room()

    def do_examine(self, command: Command):
        """Examine an item, NPC, or feature closely."""
        if not command.direct_object:
            self.display.print("Examine what?", color=Color.YELLOW)
            return

        target_name = command.direct_object
        room = self.world.get_room(self.player.current_room)

        # Special cases
        if target_name in ('self', 'me', 'myself'):
            self.do_status(command)
            return
        if target_name in ('room', 'here', 'around'):
            self.describe_current_room()
            return
        if target_name in ('inventory',):
            self.do_inventory(command)
            return

        # Find target
        target = self.world.find_target(self.player, room, target_name)

        if target is None:
            self.display.print(f"You don't see any '{target_name}' here.",
                             color=Color.YELLOW)
            return

        if hasattr(target, 'description') and hasattr(target, 'portable'):
            # It's an item
            self.display.print("")
            self.display.describe(target.get_description())
            if target.container and not target.closed and target.contents:
                self.display.print("")
                self.display.print(f"The {target.name} contains:", color=Color.BRIGHT_WHITE)
                for cid in target.contents:
                    contained = self.world.get_item(cid)
                    if contained and contained.visible:
                        self.display.print(f"  • {contained.name}")

            # Fire examine event
            if target.on_examine:
                event = self.event_manager.get_event(target.on_examine)
                if event:
                    event.fire(self)
            self.event_manager.fire_trigger(f"examine:{target.id}", self)
        else:
            # It's an NPC
            self.display.print("")
            self.display.describe(target.get_description())
            if target.on_examine:
                event = self.event_manager.get_event(target.on_examine)
                if event:
                    event.fire(self)

    def do_search(self, command: Command):
        """Search an area or container thoroughly."""
        if not command.direct_object:
            # Search the room thoroughly
            room = self.world.get_room(self.player.current_room)
            self.display.print("You search the area carefully...")

            found_anything = False

            # Reveal hidden items
            revealed = []
            for item_id in list(room.items):
                item = self.world.get_item(item_id)
                if item and item.hidden:
                    item.hidden = False
                    revealed.append(item)

            if revealed:
                self.display.success("You discover something hidden!")
                for item in revealed:
                    self.display.print(f"  • {item.name}", color=Color.BRIGHT_WHITE)
                found_anything = True

            # Also list visible portable items still in the room
            loose_items = []
            for item_id in room.items:
                item = self.world.get_item(item_id)
                if item and item.portable and not item.hidden and item.visible:
                    loose_items.append(item)

            if loose_items:
                if not found_anything:
                    self.display.print("Your search turns up the following:")
                else:
                    self.display.print("\nYou also notice:")
                for item in loose_items:
                    self.display.print(f"  • {item.name}", color=Color.BRIGHT_WHITE)
                found_anything = True

            # List containers and notable interactive scenery
            containers = []
            for item_id in room.items:
                item = self.world.get_item(item_id)
                if not item or item.hidden or not item.visible:
                    continue
                if item.container:
                    if item.locked:
                        containers.append(f"{item.name} (locked)")
                    elif item.closed:
                        containers.append(f"{item.name} (closed)")
                    else:
                        containers.append(f"{item.name} (open)")
                elif item.locked:
                    containers.append(f"{item.name} (locked)")

            if containers:
                self.display.print("\nYou notice containers that could be searched:")
                for c in containers:
                    self.display.print(f"  • {c}", color=Color.BRIGHT_WHITE)
                found_anything = True

            if not found_anything:
                self.display.print("You find nothing of particular interest.")

            # Fire room search event
            self.event_manager.fire_trigger(f"search:{room.id}", self)
            return

        # Search a specific object
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return

        if hasattr(target, 'container') and target.container:
            if target.closed:
                self.display.print(f"The {target.name} is closed.")
                return
            if not target.contents:
                self.display.print(f"The {target.name} is empty.")
                return
            self.display.print(f"Inside the {target.name} you find:")
            for cid in target.contents:
                ci = self.world.get_item(cid)
                if ci:
                    ci.hidden = False
                    self.display.print(f"  • {ci.name}")
        else:
            # Try examine instead
            self.do_examine(command)

    def do_take(self, command: Command):
        """Pick up an item."""
        if not command.direct_object:
            self.display.print("Take what?", color=Color.YELLOW)
            return

        # Handle "take all"
        if command.direct_object in ('all', 'everything'):
            self._take_all()
            return

        room = self.world.get_room(self.player.current_room)
        item = self.world.find_item_in_room(room, command.direct_object)

        if not item:
            # Check if item is in inventory (directly or inside a container)
            inv_item = self.world.find_item_in_inventory(
                self.player, command.direct_object
            )
            if inv_item:
                # Is it directly in inventory, or inside a container?
                if inv_item.id in self.player.inventory:
                    self.display.print("You already have that.", color=Color.YELLOW)
                    return
                else:
                    # It's inside a container in inventory - extract it
                    item = inv_item  # Fall through to the take logic below
            else:
                self.display.print(
                    f"You don't see any '{command.direct_object}' here.",
                    color=Color.YELLOW
                )
                return

        if item.scenery:
            self.display.print(f"The {item.name} cannot be taken.",
                             color=Color.YELLOW)
            return

        if not item.portable:
            self.display.print(f"You can't take the {item.name}.",
                             color=Color.YELLOW)
            return

        if len(self.player.inventory) >= self.player.max_carry:
            self.display.print("You can't carry anything more.",
                             color=Color.YELLOW)
            return

        # Take it - remove from wherever it lives:
        #   1. Directly in the room
        #   2. Inside an open container in the room
        #   3. Inside an open container in the player's inventory
        removed = room.remove_item(item.id)
        if not removed:
            # Check containers in the room
            for container_id in room.items:
                container = self.world.get_item(container_id)
                if container and container.container and not container.closed:
                    if item.id in container.contents:
                        container.contents.remove(item.id)
                        removed = True
                        break
        if not removed:
            # Check containers in player inventory (e.g., medical kit)
            for container_id in self.player.inventory:
                container = self.world.get_item(container_id)
                if container and container.container and not container.closed:
                    if item.id in container.contents:
                        container.contents.remove(item.id)
                        removed = True
                        break
        self.player.add_item(item.id)
        self.display.success(f"Taken: {item.name}")

        # Fire take event
        if item.on_take:
            event = self.event_manager.get_event(item.on_take)
            if event:
                event.fire(self)
        self.event_manager.fire_trigger(f"take:{item.id}", self)

    def _take_all(self):
        """Take all portable items in current room."""
        room = self.world.get_room(self.player.current_room)
        taken = []
        for item_id in list(room.items):
            item = self.world.get_item(item_id)
            if item and item.portable and not item.scenery and not item.hidden:
                if len(self.player.inventory) < self.player.max_carry:
                    room.remove_item(item_id)
                    self.player.add_item(item_id)
                    taken.append(item.name)
                    if item.on_take:
                        event = self.event_manager.get_event(item.on_take)
                        if event:
                            event.fire(self)
        if taken:
            self.display.success(f"Taken: {', '.join(taken)}")
        else:
            self.display.print("There's nothing here to take.", color=Color.YELLOW)

    def do_drop(self, command: Command):
        """Drop an item from inventory."""
        if not command.direct_object:
            self.display.print("Drop what?", color=Color.YELLOW)
            return

        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}'.",
                             color=Color.YELLOW)
            return

        self.player.remove_item(item.id)
        self.world.get_room(self.player.current_room).add_item(item.id)
        self.display.print(f"Dropped: {item.name}", color=Color.BRIGHT_WHITE)

        if item.on_drop:
            event = self.event_manager.get_event(item.on_drop)
            if event:
                event.fire(self)

    def do_inventory(self, command: Command):
        """Display player inventory."""
        if not self.player.inventory:
            self.display.print("You are carrying nothing.", color=Color.BRIGHT_BLACK)
            return

        self.display.print("You are carrying:", color=Color.BRIGHT_WHITE)
        for item_id in self.player.inventory:
            item = self.world.get_item(item_id)
            if item:
                if item_id in self.player.worn:
                    is_weapon = 'weapon' in item.flags
                    marker = " (equipped)" if is_weapon else " (worn)"
                else:
                    marker = ""
                self.display.print(f"  • {item.name}{marker}", color=Color.WHITE)

    def do_go(self, command: Command):
        """Move to a new room."""
        if not command.direct_object:
            self.display.print("Go where?", color=Color.YELLOW)
            return

        direction = command.direct_object.lower()

        # Normalize direction
        from .parser import DIRECTIONS
        if direction in DIRECTIONS:
            direction = DIRECTIONS[direction]

        room = self.world.get_room(self.player.current_room)
        if direction not in room.exits:
            self.display.print(f"You can't go {direction} from here.",
                             color=Color.YELLOW)
            return

        exit_obj = room.exits[direction]

        if exit_obj.hidden and not exit_obj.discovered:
            self.display.print(f"You can't go {direction} from here.",
                             color=Color.YELLOW)
            return

        if exit_obj.locked:
            self.display.print(exit_obj.lock_message or f"The way {direction} is locked.",
                             color=Color.YELLOW)
            return

        if exit_obj.required_flag and not self.player.has_flag(exit_obj.required_flag):
            self.display.print(exit_obj.lock_message or f"You can't go {direction}.",
                             color=Color.YELLOW)
            return

        # Move
        if exit_obj.description:
            self.display.print(exit_obj.description)

        # Fire leave event
        if room.on_leave:
            event = self.event_manager.get_event(room.on_leave)
            if event:
                event.fire(self)

        self.player.previous_room = self.player.current_room
        self.player.current_room = exit_obj.destination

        # Show new room
        self.describe_current_room()

    def do_open(self, command: Command):
        """Open a container or door."""
        if not command.direct_object:
            self.display.print("Open what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)

        if not target or not hasattr(target, 'container'):
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return

        if not target.openable:
            self.display.print(f"The {target.name} can't be opened.",
                             color=Color.YELLOW)
            return

        if target.locked:
            if target.key_id and self.player.has_item(target.key_id):
                # Auto-unlock if player has key
                target.locked = False
                key = self.world.get_item(target.key_id)
                self.display.print(f"You unlock the {target.name} with the {key.name}.",
                                 color=Color.BRIGHT_GREEN)
            else:
                self.display.print(f"The {target.name} is locked.",
                                 color=Color.YELLOW)
                return

        if not target.closed:
            self.display.print(f"The {target.name} is already open.",
                             color=Color.YELLOW)
            return

        target.closed = False
        self.display.success(f"You open the {target.name}.")

        if target.contents:
            visible_contents = [
                self.world.get_item(cid) for cid in target.contents
                if self.world.get_item(cid) and not self.world.get_item(cid).hidden
            ]
            if visible_contents:
                self.display.print(f"Inside you see:")
                for ci in visible_contents:
                    self.display.print(f"  • {ci.name}")

    def do_close(self, command: Command):
        """Close a container or door."""
        if not command.direct_object:
            self.display.print("Close what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)

        if not target or not hasattr(target, 'container'):
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return

        if not target.openable:
            self.display.print(f"The {target.name} can't be closed.",
                             color=Color.YELLOW)
            return

        if target.closed:
            self.display.print(f"The {target.name} is already closed.",
                             color=Color.YELLOW)
            return

        target.closed = True
        self.display.print(f"You close the {target.name}.", color=Color.BRIGHT_WHITE)

    def do_unlock(self, command: Command):
        """Unlock a container, door, or exit using a key."""
        if not command.direct_object:
            self.display.print("Unlock what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)

        # Check if it's an exit direction
        from .parser import DIRECTIONS
        direction = DIRECTIONS.get(command.direct_object.lower())
        if direction and direction in room.exits:
            exit_obj = room.exits[direction]
            if not exit_obj.locked:
                self.display.print(f"The way {direction} isn't locked.",
                                 color=Color.YELLOW)
                return
            if exit_obj.key_id and self.player.has_item(exit_obj.key_id):
                exit_obj.locked = False
                self.display.success(f"You unlock the way {direction}.")
                return
            self.display.print(f"You don't have a key for the way {direction}.",
                             color=Color.YELLOW)
            return

        # Try as an item
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return

        if not hasattr(target, 'locked') or not target.locked:
            self.display.print(f"The {target.name} isn't locked.",
                             color=Color.YELLOW)
            return

        # Check for key via 'with X'
        if command.indirect_object:
            key_item = self.world.find_item_in_inventory(self.player, command.indirect_object)
            if not key_item:
                self.display.print(f"You don't have a '{command.indirect_object}'.",
                                 color=Color.YELLOW)
                return
            if target.key_id and target.key_id == key_item.id:
                target.locked = False
                self.display.success(f"You unlock the {target.name} with the {key_item.name}.")
                return
            self.display.print(f"The {key_item.name} doesn't fit.", color=Color.YELLOW)
            return

        # Auto-find key
        if target.key_id and self.player.has_item(target.key_id):
            target.locked = False
            key = self.world.get_item(target.key_id)
            self.display.success(f"You unlock the {target.name} with the {key.name}.")
        else:
            self.display.print(f"You don't have a key for the {target.name}.",
                             color=Color.YELLOW)

    def do_read(self, command: Command):
        """Read a document, log, or sign."""
        if not command.direct_object:
            self.display.print("Read what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        item = self.world.find_item(self.player, room, command.direct_object)

        if not item:
            self.display.print(f"You don't see any '{command.direct_object}' to read.",
                             color=Color.YELLOW)
            return

        if not item.readable:
            self.display.print(f"The {item.name} isn't something you can read.",
                             color=Color.YELLOW)
            return

        self.display.print("")
        self.display.print(item.read_text, color=Color.BRIGHT_YELLOW)
        self.player.read_logs.add(item.id)

        if item.on_read:
            event = self.event_manager.get_event(item.on_read)
            if event:
                event.fire(self)
        self.event_manager.fire_trigger(f"read:{item.id}", self)

    def do_use(self, command: Command):
        """Use an item."""
        if not command.direct_object:
            self.display.print("Use what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        item = self.world.find_item(self.player, room, command.direct_object)

        if not item:
            self.display.print(f"You don't have any '{command.direct_object}'.",
                             color=Color.YELLOW)
            return

        # If there's an indirect object, use item ON that
        if command.indirect_object:
            # For "use X on Y" - check NPCs first (sedative on figure, etc.)
            target = self.world.find_npc_in_room(room, command.indirect_object)
            if not target:
                target = self.world.find_target(self.player, room, command.indirect_object)
            if not target:
                self.display.print(f"You don't see any '{command.indirect_object}' here.",
                                 color=Color.YELLOW)
                return
            self._use_on(item, target)
            return

        # Standalone use
        if not item.usable:
            self.display.print(f"You can't think of a way to use the {item.name} here.",
                             color=Color.YELLOW)
            return

        if item.use_text:
            self.display.print(item.use_text)

        # Apply built-in consumable effects based on item type
        self._apply_consumable_effects(item)

        if item.on_use:
            event = self.event_manager.get_event(item.on_use)
            if event:
                event.fire(self)
        self.event_manager.fire_trigger(f"use:{item.id}", self)

        if item.consumable:
            self.player.remove_item(item.id)

    # Consumable effect definitions
    CONSUMABLE_EFFECTS = {
        'stimpack':       {'health': 25},
        'stimpack_2':     {'health': 40},
        'stim_injector':  {'health': 15, 'sanity': 10},
        'bandages':       {'health': 10},
        'antibiotics':    {'infection': -5},
        'ration_pack':    {'health': 10, 'sanity': 5},
    }

    def _apply_consumable_effects(self, item):
        """Apply healing/stat effects for known consumable items."""
        effects = self.CONSUMABLE_EFFECTS.get(item.id)
        if not effects:
            return

        messages = []
        if 'health' in effects and effects['health'] > 0:
            old = self.player.health
            self.player.heal(effects['health'])
            gained = self.player.health - old
            if gained > 0:
                messages.append(f"+{gained} HP")
        if 'sanity' in effects and effects['sanity'] > 0:
            old = self.player.sanity
            self.player.restore_sanity(effects['sanity'])
            gained = self.player.sanity - old
            if gained > 0:
                messages.append(f"+{gained} sanity")
        if 'infection' in effects and effects['infection'] < 0:
            old = self.player.infection
            self.player.treat_infection(-effects['infection'])
            reduced = old - self.player.infection
            if reduced > 0:
                messages.append(f"-{reduced} infection")

        if messages:
            self.display.success(f"({', '.join(messages)})")

    def _use_on(self, item, target):
        """Use one item on another item/NPC."""
        # Check for a specific scripted interaction first
        key = f"use:{item.id}:{target.id}"
        fired = self.event_manager.fire_trigger(key, self)
        if fired:
            if item.consumable:
                self.player.remove_item(item.id)
            return

        # Built-in weapon/tool interactions with NPCs
        if hasattr(target, 'alive') and hasattr(target, 'health'):
            # Sedative syringe on any NPC
            if item.id == 'sedative_syringe' or item.has_flag('non_lethal'):
                if not target.alive:
                    self.display.print(f"The {target.name} is already dead.",
                                     color=Color.YELLOW)
                    return
                self.display.print(
                    f"You lunge forward and jab the sedative into {target.name}'s neck. "
                    f"They stagger, eyes going wide, then unfocused. Their body goes "
                    f"limp and they collapse to the deck, breathing shallow but steady.",
                    color=Color.BRIGHT_WHITE
                )
                target.add_flag('sedated')
                target.hostile = False
                target.state['threatening'] = False
                self.player.remove_item(item.id)
                self.player.log_action(f"sedated_{target.id}")
                # Set player flag so encounter events know not to fire
                self.player.add_flag(f"{target.id}_sedated")
                self.event_manager.fire_trigger(f"sedate:{target.id}", self)
                return

            # Weapon on any NPC - treat as attack
            if 'weapon' in item.flags:
                damage = self._calculate_weapon_damage(item.id, target)
                target.health -= damage
                self._attacked_this_turn = True
                self.display.print(
                    f"You strike {target.name} with the {item.name}! (-{damage} HP)",
                    color=Color.BRIGHT_RED
                )
                if target.health <= 0 and target.alive:
                    target.alive = False
                    target.hostile = False
                    self.display.critical(f"{target.name} falls and does not rise.")
                    self.player.log_action(f"killed_{target.id}")
                    if target.on_death:
                        event = self.event_manager.get_event(target.on_death)
                        if event:
                            event.fire(self)
                if item.consumable:
                    self.player.remove_item(item.id)
                return

        # Check generic use_target
        if item.use_target and item.use_target == target.id:
            if item.use_text:
                self.display.print(item.use_text)
            if item.on_use:
                event = self.event_manager.get_event(item.on_use)
                if event:
                    event.fire(self)
            if item.consumable:
                self.player.remove_item(item.id)
            return

        # Default response
        self.display.print(f"You can't use the {item.name} on the {target.name}.",
                         color=Color.YELLOW)

    def do_type(self, command: Command):
        """Type text into a keypad or console."""
        if not command.modifier and not command.direct_object:
            self.display.print("Type what?", color=Color.YELLOW)
            return

        text = command.modifier or command.direct_object

        if not command.indirect_object:
            self.display.print("Type where? (e.g., 'type 1234 into keypad')",
                             color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.indirect_object)

        if not target:
            self.display.print(f"You don't see any '{command.indirect_object}' here.",
                             color=Color.YELLOW)
            return

        self.display.print(f"You type '{text}' into the {target.name}...",
                         color=Color.BRIGHT_WHITE)

        # Check if this is a keypad/terminal with a code
        if hasattr(target, 'lock_code') and target.lock_code:
            if str(text).strip().upper() == str(target.lock_code).strip().upper():
                self.display.success("Access granted.")
                target.locked = False
                if hasattr(target, 'on_use') and target.on_use:
                    event = self.event_manager.get_event(target.on_use)
                    if event:
                        event.fire(self)
                self.event_manager.fire_trigger(f"unlock:{target.id}", self)
                return
            else:
                self.display.print("Access denied. Incorrect code.", color=Color.RED)
                return

        # Fire generic type event
        self.event_manager.fire_trigger(f"type:{target.id}:{text}", self)
        self.event_manager.fire_trigger(f"type:{target.id}", self)

    def do_talk(self, command: Command):
        """Talk to an NPC."""
        target_name = command.direct_object or command.indirect_object
        if not target_name:
            self.display.print("Talk to whom?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)
        npc = self.world.find_npc_in_room(room, target_name)

        if not npc:
            self.display.print(f"You don't see any '{target_name}' here.",
                             color=Color.YELLOW)
            return

        if not npc.alive:
            self.display.print(f"{npc.name} is dead. They can't respond.",
                             color=Color.YELLOW)
            return

        # Fire talk event
        if npc.on_talk:
            event = self.event_manager.get_event(npc.on_talk)
            if event:
                event.fire(self)
        self.event_manager.fire_trigger(f"talk:{npc.id}", self)

        # Use dialogue manager
        self.talking_to = npc.id
        self.dialogue_manager.talk_to(npc, self.player, self.display)

    def do_ask(self, command: Command):
        """Ask someone about a topic."""
        # Various syntax: "ask X about Y", "ask about Y" (last NPC)
        if not command.direct_object and not command.indirect_object:
            self.display.print("Ask whom about what?", color=Color.YELLOW)
            return

        # Determine NPC and topic
        topic_name = None
        npc_name = None

        if command.preposition == 'about':
            npc_name = command.direct_object
            topic_name = command.indirect_object
        else:
            # "ask X Y" - treat first as NPC, rest as topic
            if command.direct_object and command.indirect_object:
                npc_name = command.direct_object
                topic_name = command.indirect_object
            elif command.direct_object:
                # Just a topic, use talking_to NPC
                topic_name = command.direct_object
                npc_name = None

        # Find NPC
        room = self.world.get_room(self.player.current_room)
        npc = None
        if npc_name:
            npc = self.world.find_npc_in_room(room, npc_name)
            if not npc and self.talking_to:
                # Maybe npc_name is actually topic
                topic_name = npc_name
                npc = self.world.get_npc(self.talking_to)
        elif self.talking_to:
            npc = self.world.get_npc(self.talking_to)

        if not npc:
            self.display.print("Ask whom?", color=Color.YELLOW)
            return

        if not npc.alive:
            self.display.print(f"{npc.name} is dead.", color=Color.YELLOW)
            return

        if not topic_name:
            self.display.print("Ask about what?", color=Color.YELLOW)
            return

        self.dialogue_manager.ask_about(npc, topic_name, self)

    def do_tell(self, command: Command):
        """Tell an NPC about something."""
        self.do_ask(command)

    def do_say(self, command: Command):
        """Say something aloud."""
        text = command.modifier or command.direct_object
        if not text:
            self.display.print("Say what?", color=Color.YELLOW)
            return
        self.display.print(f'You say: "{text}"', color=Color.CYAN)
        # Check if anyone responds
        room = self.world.get_room(self.player.current_room)
        for npc_id in room.npcs:
            npc = self.world.get_npc(npc_id)
            if npc and npc.present and npc.alive:
                self.event_manager.fire_trigger(f"say:{text.lower()}:{npc.id}", self)
                self.event_manager.fire_trigger(f"say_to:{npc.id}", self)
        self.event_manager.fire_trigger(f"say:{text.lower()}", self)

    def do_answer(self, command: Command):
        """Answer a question posed by an NPC or the environment."""
        self.do_say(command)

    def _find_best_weapon(self):
        """Find the best weapon in player inventory based on WEAPON_DAMAGE."""
        best_weapon = None
        best_damage = 0
        for item_id in self.player.inventory:
            if item_id in WEAPON_DAMAGE:
                dmg = WEAPON_DAMAGE[item_id].get('default', 0)
                if dmg > best_damage:
                    best_damage = dmg
                    best_weapon = item_id
        return best_weapon

    def _calculate_weapon_damage(self, weapon_id, target):
        """Calculate damage for a weapon against a target type."""
        if weapon_id is None:
            return 5  # Bare hands
        weapon_data = WEAPON_DAMAGE.get(weapon_id, {})
        # Determine target type from NPC flags or role
        target_type = 'default'
        if hasattr(target, 'flags'):
            if 'infected' in target.flags:
                target_type = 'infected'
            elif 'garden_node' in target.flags:
                target_type = 'garden_node'
        if hasattr(target, 'role'):
            if target.role == 'infected':
                target_type = 'infected'
        return weapon_data.get(target_type, weapon_data.get('default', 5))

    def do_attack(self, command: Command):
        """Attack an NPC or object using the best available weapon."""
        if not command.direct_object:
            self.display.print("Attack what?", color=Color.YELLOW)
            return

        room = self.world.get_room(self.player.current_room)

        # For attack, ALWAYS check NPCs first - you attack people, not items
        target = self.world.find_npc_in_room(room, command.direct_object)
        if not target:
            # Fall back to general target (breakable objects, etc.)
            target = self.world.find_target(self.player, room, command.direct_object)

        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return

        if not hasattr(target, 'health'):
            self.display.print(f"You can't attack the {target.name}.",
                             color=Color.YELLOW)
            return

        self._attacked_this_turn = True

        # Find best weapon
        weapon_id = self._find_best_weapon()
        damage = self._calculate_weapon_damage(weapon_id, target)

        # Handle non-lethal weapons
        weapon_data = WEAPON_DAMAGE.get(weapon_id, {}) if weapon_id else {}
        if weapon_data.get('sedate'):
            self.display.print(f"You jab the {target.name} with the sedative syringe.",
                             color=Color.BRIGHT_WHITE)
            target.add_flag('sedated')
            target.hostile = False
            self.event_manager.fire_trigger(f"attack:{target.id}", self)
            self.player.log_action(f"sedated:{target.id}")
            return
        if weapon_data.get('stun_turns'):
            self.display.print(f"You hurl tear gas at the {target.name}!",
                             color=Color.BRIGHT_WHITE)
            target.add_flag('stunned')
            target.state['stun_turns'] = weapon_data['stun_turns']
            self.event_manager.fire_trigger(f"attack:{target.id}", self)
            self.player.log_action(f"stunned:{target.id}")
            return

        # Lethal attack
        if weapon_id:
            weapon_item = self.world.get_item(weapon_id)
            weapon_name = weapon_item.name if weapon_item else weapon_id
            self.display.print(f"You attack the {target.name} with the {weapon_name}! ({damage} damage)",
                             color=Color.BRIGHT_WHITE)
        else:
            self.display.print(f"You attack the {target.name} with your bare hands! ({damage} damage)",
                             color=Color.BRIGHT_WHITE)

        self.event_manager.fire_trigger(f"attack:{target.id}", self)
        target.health -= damage

        if target.health <= 0 and target.alive:
            target.alive = False
            target.hostile = False
            self.display.critical(f"The {target.name} falls.")
            # Drop NPC inventory into room
            for drop_id in list(target.inventory):
                room.add_item(drop_id)
                drop_item = self.world.get_item(drop_id)
                if drop_item:
                    self.display.print(f"  {target.name} drops: {drop_item.name}",
                                     color=Color.BRIGHT_WHITE)
            target.inventory.clear()
            if target.on_death:
                event = self.event_manager.get_event(target.on_death)
                if event:
                    event.fire(self)
            self.event_manager.fire_trigger(f"kill:{target.id}", self)
            self.player.log_action(f"killed:{target.id}")
        else:
            if hasattr(target, 'alive') and target.alive:
                self.display.print(f"The {target.name} is wounded but still standing.",
                                 color=Color.YELLOW)

    def do_shoot(self, command: Command):
        """Shoot at something with a ranged weapon."""
        # Check if player has a ranged weapon
        ranged_weapons = {'handgun', 'tactical_rifle', 'plasma_cutter', 'ceremonial_sidearm'}
        has_ranged = any(iid in ranged_weapons for iid in self.player.inventory)
        has_any_weapon = any(
            self.world.get_item(iid) and self.world.get_item(iid).has_flag('weapon')
            for iid in self.player.inventory
        )
        if not has_ranged and not has_any_weapon:
            self.display.print("You don't have a weapon to shoot with.", color=Color.YELLOW)
            return
        self.do_attack(command)

    def do_push(self, command: Command):
        """Push a button or object."""
        if not command.direct_object:
            self.display.print("Push what?", color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return
        fired = self.event_manager.fire_trigger(f"push:{target.id}", self)
        if fired == 0 and hasattr(target, 'on_use') and target.on_use:
            event = self.event_manager.get_event(target.on_use)
            if event:
                if event.fire(self):
                    fired += 1
        if fired == 0:
            self.display.print(f"You push the {target.name}. Nothing happens.",
                             color=Color.YELLOW)

    def do_pull(self, command: Command):
        """Pull a lever or object."""
        self.do_push(command)

    def do_turn(self, command: Command):
        """Turn a dial or object."""
        if not command.direct_object:
            self.display.print("Turn what?", color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return
        self.event_manager.fire_trigger(f"turn:{target.id}", self)

    def do_insert(self, command: Command):
        """Insert an item into a slot or container."""
        if not command.direct_object or not command.indirect_object:
            self.display.print("Insert what into what?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}'.",
                             color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.indirect_object)
        if not target:
            self.display.print(f"You don't see any '{command.indirect_object}' here.",
                             color=Color.YELLOW)
            return

        # Fire specific interaction
        self.event_manager.fire_trigger(f"insert:{item.id}:{target.id}", self)

        # Generic container logic
        if hasattr(target, 'container') and target.container and not target.closed:
            self.player.remove_item(item.id)
            target.contents.append(item.id)
            self.display.print(f"You put the {item.name} into the {target.name}.",
                             color=Color.BRIGHT_WHITE)

    def do_combine(self, command: Command):
        """Combine two items."""
        if not command.direct_object or not command.indirect_object:
            self.display.print("Combine what with what?", color=Color.YELLOW)
            return
        item1 = self.world.find_item_in_inventory(self.player, command.direct_object)
        item2 = self.world.find_item_in_inventory(self.player, command.indirect_object)
        if not item1 or not item2:
            self.display.print("You don't have both items.", color=Color.YELLOW)
            return
        # Fire combination event (content-specific)
        self.event_manager.fire_trigger(f"combine:{item1.id}:{item2.id}", self)
        self.event_manager.fire_trigger(f"combine:{item2.id}:{item1.id}", self)

    def do_listen(self, command: Command):
        """Listen for sounds."""
        room = self.world.get_room(self.player.current_room)
        if room.ambient_sounds:
            import random
            self.display.print(random.choice(room.ambient_sounds), color=Color.BRIGHT_BLACK)
        else:
            self.display.print("You hear nothing of note.", color=Color.BRIGHT_BLACK)
        self.event_manager.fire_trigger(f"listen:{room.id}", self)

    def do_smell(self, command: Command):
        """Smell the environment."""
        room = self.world.get_room(self.player.current_room)
        self.event_manager.fire_trigger(f"smell:{room.id}", self)
        if room.smell_text:
            self.display.print(room.smell_text, color=Color.BRIGHT_BLACK)
        elif room.state.get('smell_text'):
            self.display.print(room.state['smell_text'], color=Color.BRIGHT_BLACK)
        else:
            self.display.print("The recycled air carries no distinct odor.", color=Color.BRIGHT_BLACK)

    def do_touch(self, command: Command):
        """Touch an object or surface."""
        room = self.world.get_room(self.player.current_room)
        if not command.direct_object:
            # Touch the environment
            self.event_manager.fire_trigger(f"touch:{room.id}", self)
            if room.touch_text:
                self.display.print(room.touch_text, color=Color.BRIGHT_BLACK)
            elif room.state.get('touch_text'):
                self.display.print(room.state['touch_text'], color=Color.BRIGHT_BLACK)
            else:
                self.display.print("Cold metal under your fingertips. Standard ship hull plating.", color=Color.BRIGHT_BLACK)
            return
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return
        self.event_manager.fire_trigger(f"touch:{target.id}", self)

    def do_wait(self, command: Command):
        """Wait, passing time."""
        self.display.print("Time passes...", color=Color.BRIGHT_BLACK)
        self.player.advance_time(5)

    # Human-readable descriptions for knowledge flags
    KNOWLEDGE_DISPLAY = {
        'chose_cryo_voluntarily': 'You chose to enter cryo-sleep of your own free will.',
        'aria_protected_pod': 'ARIA isolated your cryo pod to protect you.',
        'knows_seed_origin': 'The Seed was found in a derelict alien vessel at Kepler-442.',
        'knows_protocol_aegis': 'Captain Reeves authorized Protocol Aegis - a kill-all sequence.',
        'knows_player_immunity': 'Your DNA carries resistance to the Seed infection.',
        'knows_cure_possible': 'A cure can be synthesized from your blood.',
        'knows_seed_nature': 'The Seed is an informational structure using biology as hardware.',
        'knows_infection_mechanism': 'The infection spreads through the water supply, replacing cells.',
        'knows_cure_synthesis': 'Dr. Patel confirmed antibodies in your blood can neutralize the Seed.',
        'patel_final_message': 'Dr. Patel left a final recording before his death.',
        'patel_dead': 'Dr. Raj Patel is dead. Self-inflicted, to stop the infection spreading.',
        'knows_lin_investigation': 'Dr. Lin tracked the infection from its earliest symptoms.',
        'knows_lin_safe_code': "Dr. Lin's wall safe code is BUSTER - her first dog's name.",
        'seen_brown_dwarf': 'The brown dwarf GRB-7734 is pulling the ship to its destruction.',
        'knows_aria_identity': 'ARIA is the Autonomous Reasoning and Integration Assistant.',
        'knows_three_paths': 'ARIA outlined three paths: Aegis, Icarus, and Prometheus.',
        'knows_apotheosis_path': 'A fourth path exists - merging with ARIA via the Neural Interface.',
        'knows_yuki_exists': 'Lt. Yuki Tanaka is alive in Engineering, fighting the infection.',
        'met_yuki': 'You have met Lt. Yuki Tanaka.',
        'heard_patels_truth': "You heard Patel's final recording about the Seed and the cure.",
        'core_memory_recovered': 'You remember authorizing the Seed retrieval. It was your decision.',
        'remembers_authorizing_seed': 'You remember arguing for the Seed to be brought aboard.',
        'remembers_unpacking_seed': 'You remember unpacking the Seed in the cargo bay.',
        'been_on_bridge': 'You have visited the bridge of the Prometheus.',
        'seen_the_garden': 'You have seen the Garden - the infected hydroponics bay.',
        'knows_engineering_plan': 'Yuki outlined how to repair the thrusters and escape.',
        'knows_cure_plan': 'You know the steps needed to synthesize the cure.',
        'yuki_offered_help': 'Yuki has offered to help you save the ship.',
        'chose_aegis_path': 'You have chosen to authorize Protocol Aegis.',
        'chose_icarus_path': 'You have synthesized the cure.',
        'the_deepest_truth': 'You chose the Seed. The antibodies were its gift. You always knew.',
        # From logs and readables
        'knows_lin_safe_code': "Dr. Lin's wall safe code: BUSTER (her first dog).",
        'knows_buster_code': "Lin's safe code is BUSTER.",
        'knows_comms_damage': "The comms array was sabotaged. Fletcher was killed trying to transmit.",
        'knows_power_routing': "Engineering schematics show how to reroute main power.",
        'mapped_patrols': "Security cameras revealed infected crew patrol routes.",
        'distress_sent': "A distress signal was sent to Earth.",
        'main_power_restored': "Main power has been restored to the ship.",
        'has_synthesis_protocol': "You have Dr. Lin's cure synthesis procedure.",
        'has_cure': "You have synthesized the cure.",
        'full_timeline_known': "You have pieced together the complete infection timeline.",
        'kirilov_lucid': "Kirilov has moments of lucidity between infection episodes.",
        'mora_met': "You have met Dr. Mora, hiding in the chemistry lab.",
        'mora_proven_uninfected': "You proved to Dr. Mora that you resist the infection.",
        'knows_engineering_plan': "Yuki explained the thruster repair sequence.",
        'knows_cure_plan': "You know the cure synthesis steps from Yuki and Lin's notes.",
        'pump_fixed': "The coolant pump has been repaired.",
        'power_rerouted': "Power has been rerouted through the plasma conduits.",
        'burn_calculated': "The escape burn trajectory has been calculated.",
        'relay_repaired': "The communications relay has been repaired.",
        'knows_ship_layout': "You have studied the ship's full deck schematics.",
    }

    def do_think(self, command: Command):
        """Review what the player knows and remembers."""
        has_content = False

        # Knowledge section - filter out memory_* flags and internal flags
        display_facts = []
        for fact in sorted(self.player.knowledge):
            # Skip memory tracking flags - those show in the memories section
            if fact.startswith('memory_'):
                continue
            # Look up human-readable version, or generate one
            if fact in self.KNOWLEDGE_DISPLAY:
                display_facts.append(self.KNOWLEDGE_DISPLAY[fact])
            else:
                # Fallback: clean up the flag name
                readable = fact.replace('_', ' ').strip()
                readable = readable.replace('knows ', '').replace('know ', '')
                readable = readable.capitalize() + '.'
                display_facts.append(readable)

        if display_facts:
            self.display.print("You take a moment to organize your thoughts:",
                             color=Color.BRIGHT_WHITE)
            for fact_text in display_facts:
                self.display.print(f"  - {fact_text}", color=Color.BRIGHT_WHITE)
            has_content = True

        # Memory fragments section - show full emotional summaries
        if self.player.memory_fragments:
            count = self.player.get_memory_count()
            self.display.print("")
            self.display.separator('-', Color.BRIGHT_YELLOW)
            self.display.print(
                f"Recovered memories ({count}/30):",
                color=Color.BRIGHT_YELLOW
            )
            self.display.separator('-', Color.BRIGHT_YELLOW)
            for mem_id, mem_text in self.player.memory_fragments.items():
                # Use italic + yellow for dreamy/memory feel
                self.display.print(
                    f"  {Color.ITALIC}{mem_text}{Color.RESET}",
                    color=Color.YELLOW, wrap=True, typewriter=False
                )
            has_content = True

        if not has_content:
            self.display.print(
                "You close your eyes and try to remember. Nothing comes. "
                "Not yet. The cryo-sleep stole your memories. You need to "
                "find things - objects, places, people - that trigger recall.",
                color=Color.BRIGHT_BLACK
            )

    def do_status(self, command: Command):
        """Show player status."""
        p = self.player
        self.display.separator('─', Color.BRIGHT_CYAN)
        self.display.print(f"Name: {p.name}", color=Color.BRIGHT_WHITE)
        self.display.print(f"Health:    {p.health}/{p.max_health}",
                         color=Color.BRIGHT_GREEN if p.health > 50 else Color.BRIGHT_RED)
        self.display.print(f"Sanity:    {p.sanity}/{p.max_sanity}",
                         color=Color.BRIGHT_GREEN if p.sanity > 50 else Color.BRIGHT_MAGENTA)
        self.display.print(f"Oxygen:    {p.oxygen}/{p.max_oxygen}",
                         color=Color.BRIGHT_BLUE)
        if p.infection > 0:
            self.display.print(f"Infection: {p.infection}%",
                             color=Color.BRIGHT_RED)
        self.display.print(f"Time until catastrophe: {p.get_time_remaining_str()}",
                         color=Color.BRIGHT_YELLOW)
        self.display.separator('─', Color.BRIGHT_CYAN)

    def do_objectives(self, command: Command):
        """Show current objectives."""
        active = [o for o in self.player.objectives if not o['completed']]
        completed = [o for o in self.player.objectives if o['completed']]

        if not self.player.objectives:
            self.display.print("No current objectives.", color=Color.BRIGHT_BLACK)
            return

        if active:
            self.display.print("Current objectives:", color=Color.BRIGHT_WHITE)
            for obj in active:
                self.display.print(f"  [ ] {obj['description']}", color=Color.BRIGHT_WHITE)

        if completed:
            self.display.print("", typewriter=False)
            self.display.print("Completed:", color=Color.BRIGHT_GREEN)
            for obj in completed:
                marker = "[v]" if not self.display.use_unicode else "[✓]"
                self.display.print(f"  {marker} {obj['description']}", color=Color.BRIGHT_GREEN)

    def do_location(self, command: Command):
        """Display the player's current location."""
        room = self.world.get_room(self.player.current_room)
        if not room:
            self.display.print("You are... nowhere.", color=Color.YELLOW)
            return
        self.display.location(room.name)
        if room.deck:
            self.display.print(f"Deck: {room.deck}", color=Color.BRIGHT_CYAN)
        # Show exits as a quick reference
        self.display.print(room.get_exits_description(), color=Color.BRIGHT_BLUE)

    def do_save(self, command: Command):
        """Save the game."""
        slot = command.direct_object or "quicksave"
        if self.save_manager.save_game(self, slot):
            self.display.success(f"Game saved to slot: {slot}")
        else:
            self.display.error("Save failed.")

    def do_load(self, command: Command):
        """Load a saved game."""
        slot = command.direct_object or "quicksave"
        if self.save_manager.load_game(self, slot):
            self.display.success(f"Game loaded from slot: {slot}")
            self.describe_current_room()
        else:
            self.display.error("Load failed.")

    def do_quit(self, command: Command):
        """Quit the game."""
        self.display.print("Are you sure you want to quit? (yes/no)",
                         color=Color.YELLOW)
        try:
            answer = self.display.prompt("> ").strip().lower()
            if answer in ('yes', 'y'):
                self.display.print("Goodbye, Doctor.", color=Color.BRIGHT_CYAN)
                self.running = False
        except (KeyboardInterrupt, EOFError):
            self.running = False

    def do_help(self, command: Command):
        """Show help information."""
        self.display.print("")
        self.display.print("═══ COMMAND REFERENCE ═══", color=Color.BRIGHT_CYAN)
        self.display.print("""
MOVEMENT:
  go <direction>   Move (north, south, east, west, up, down, etc.)
  n, s, e, w       Shortcuts for directions

OBSERVATION:
  look             Look around current room
  examine <thing>  Look closely at something
  search <area>    Search thoroughly (may reveal hidden items)
  read <item>      Read a document or log
  listen / smell   Use other senses

INVENTORY:
  take <item>      Pick something up
  drop <item>      Drop an item
  inventory (i)    List what you're carrying
  take all         Take everything in the room

INTERACTION:
  open/close <X>   Open or close a container/door
  unlock <X>       Unlock with a key
  use <X>          Use an item
  use <X> on <Y>   Use one thing on another
  type <code> into <keypad>  Enter a code
  insert <X> into <Y>        Put something into a slot
  combine <X> with <Y>       Join two items
  push/pull <X>    Operate a lever/button

SOCIAL:
  talk to <npc>    Start a conversation
  ask <npc> about <topic>    Inquire about something
  say <words>      Say something aloud
  give <item> to <npc>       Give an item

META:
  save / load      Save or restore game
  status           Check health, sanity, time
  location (where) Show current location and exits
  objective(s)     Review current quest log
  think            Recall what you've learned
  map              Show discovered locations
  help             Show this screen
  quit             Exit game

COMPOUND COMMANDS:
  You can chain commands using:
    and   - take key and unlock door
    then  - go north then take crystal
    while - shoot target while running to cover
    ,     - take keycard, read log, go east

Quoted strings can be typed: type "override alpha" into console
""", color=Color.WHITE, typewriter=False)

    def do_hint(self, command: Command):
        """Give a hint based on current state."""
        room = self.world.get_room(self.player.current_room)
        # Fire room-specific hint event
        hint_fired = self.event_manager.fire_trigger(f"hint:{room.id}", self)
        if hint_fired == 0:
            # Generic hint based on objectives
            active = [o for o in self.player.objectives if not o['completed']]
            if active:
                self.display.hint(f"You should focus on: {active[0]['description']}")
            else:
                self.display.hint("Explore the ship, examine everything, talk to any survivors.")

    def do_map(self, command: Command):
        """Show discovered map. 'map' for overview, 'map here' for local detail."""
        arg = (command.direct_object or '').lower().strip()

        if arg in ('here', 'local', 'nearby', 'area', ''):
            self._show_local_map()
        elif arg in ('all', 'full', 'overview', 'decks'):
            self._show_full_map()
        else:
            # Try to find a matching deck or room
            self._show_local_map()

    def _show_local_map(self):
        """Show detailed local map: current room + connections + one step out."""
        current = self.world.get_room(self.player.current_room)
        if not current:
            return

        self.display.print("")
        self.display.print(
            f"=== MAP: {current.name} ({current.deck}) ===",
            color=Color.BRIGHT_CYAN, typewriter=False
        )
        self.display.print("")

        # Show exits from current room
        self.display.print("  From here:", color=Color.BRIGHT_WHITE)
        if not current.exits:
            self.display.print("    (no exits)", color=Color.BRIGHT_BLACK)
        for direction, exit_obj in sorted(current.exits.items()):
            dest = self.world.get_room(exit_obj.destination)
            if not dest:
                continue

            # Show lock status
            if exit_obj.hidden and not exit_obj.discovered:
                continue  # Don't show hidden undiscovered exits
            if exit_obj.locked:
                lock_hint = " [LOCKED]"
            else:
                lock_hint = ""

            # Show if visited
            if dest.id in self.player.discovered_rooms:
                visited = ""
            else:
                visited = " (unexplored)"

            self.display.print(
                f"    {direction:10s} --> {dest.name}{lock_hint}{visited}",
                color=Color.BRIGHT_BLUE, typewriter=False
            )

        # Show what's one step beyond each visible exit
        self.display.print("", typewriter=False)
        self.display.print("  Nearby (one room away):", color=Color.BRIGHT_WHITE)

        shown_any = False
        for direction, exit_obj in sorted(current.exits.items()):
            if exit_obj.hidden and not exit_obj.discovered:
                continue
            if exit_obj.locked:
                continue  # Can't see beyond locked doors

            neighbor = self.world.get_room(exit_obj.destination)
            if not neighbor or neighbor.id not in self.player.discovered_rooms:
                continue

            # Show this neighbor's exits (excluding the way back)
            neighbor_exits = []
            for n_dir, n_exit in sorted(neighbor.exits.items()):
                n_dest = self.world.get_room(n_exit.destination)
                if not n_dest or n_exit.destination == current.id:
                    continue
                if n_exit.hidden and not n_exit.discovered:
                    continue
                lock = " [L]" if n_exit.locked else ""
                name = n_dest.name
                # Shorten long names
                if len(name) > 25:
                    name = name[:22] + "..."
                neighbor_exits.append(f"{n_dir}: {name}{lock}")

            if neighbor_exits:
                short_name = neighbor.name
                if len(short_name) > 25:
                    short_name = short_name[:22] + "..."
                exits_str = ", ".join(neighbor_exits)
                self.display.print(
                    f"    {short_name}: {exits_str}",
                    color=Color.BRIGHT_BLACK, typewriter=False
                )
                shown_any = True

        if not shown_any:
            self.display.print(
                "    (explore adjacent rooms to reveal more connections)",
                color=Color.BRIGHT_BLACK, typewriter=False
            )

        # Room count - total only revealed if player has ship schematics
        total_explored = len(self.player.discovered_rooms)
        if self.player.has_flag("has_ship_schematics"):
            self.display.print(
                f"\n  Rooms explored: {total_explored}/{len(self.world.rooms)}",
                color=Color.BRIGHT_BLACK, typewriter=False
            )
        else:
            self.display.print(
                f"\n  Rooms explored: {total_explored}/???",
                color=Color.BRIGHT_BLACK, typewriter=False
            )

    def _show_full_map(self):
        """Show full deck overview with exit counts."""
        self.display.print("")
        self.display.print("=== SHIP MAP (explored areas) ===",
                         color=Color.BRIGHT_CYAN, typewriter=False)

        decks = {}
        for room_id in sorted(self.player.discovered_rooms):
            room = self.world.get_room(room_id)
            if room:
                deck = room.deck or "Unknown"
                if deck not in decks:
                    decks[deck] = []
                decks[deck].append(room)

        current_room = self.world.get_room(self.player.current_room)

        for deck in sorted(decks.keys()):
            rooms = decks[deck]
            self.display.print(f"\n  {deck} ({len(rooms)} rooms):",
                             color=Color.BRIGHT_CYAN, typewriter=False)
            for room in rooms:
                marker = " <-- YOU" if room.id == self.player.current_room else ""

                # Count exits and locked exits
                total_exits = len([e for e in room.exits.values()
                                   if not e.hidden or e.discovered])
                locked = len([e for e in room.exits.values()
                              if e.locked and (not e.hidden or e.discovered)])
                lock_str = f" ({locked} locked)" if locked else ""

                self.display.print(
                    f"    - {room.name}{lock_str}{marker}",
                    color=Color.WHITE, typewriter=False
                )

        total_explored = len(self.player.discovered_rooms)
        if self.player.has_flag("has_ship_schematics"):
            self.display.print(
                f"\n  Total explored: {total_explored}/{len(self.world.rooms)} rooms",
                color=Color.BRIGHT_BLACK, typewriter=False
            )
        else:
            self.display.print(
                f"\n  Total explored: {total_explored}/??? rooms",
                color=Color.BRIGHT_BLACK, typewriter=False
            )
        self.display.hint("  (Use 'map here' for detailed local connections)")

    def do_hide(self, command: Command):
        """Hide from enemies."""
        self.player.add_flag("hiding")
        self.display.print("You try to stay out of sight...", color=Color.BRIGHT_BLACK)

    def do_climb(self, command: Command):
        """Climb something."""
        if command.direct_object:
            # Treat as movement or examination
            room = self.world.get_room(self.player.current_room)
            if 'up' in room.exits:
                command.direct_object = 'up'
                self.do_go(command)
                return
            self.event_manager.fire_trigger(f"climb:{command.direct_object}", self)
        else:
            self.display.print("Climb what?", color=Color.YELLOW)

    def do_break(self, command: Command):
        """Break/destroy something."""
        if not command.direct_object:
            self.display.print("Break what?", color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            self.display.print(f"You don't see any '{command.direct_object}' here.",
                             color=Color.YELLOW)
            return
        self.event_manager.fire_trigger(f"break:{target.id}", self)

    def do_give(self, command: Command):
        """Give an item to an NPC."""
        if not command.direct_object or not command.indirect_object:
            self.display.print("Give what to whom?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}'.",
                             color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        npc = self.world.find_npc_in_room(room, command.indirect_object)
        if not npc:
            self.display.print(f"You don't see any '{command.indirect_object}' here.",
                             color=Color.YELLOW)
            return
        self.event_manager.fire_trigger(f"give:{item.id}:{npc.id}", self)

    def do_remove(self, command: Command):
        """Remove/unequip a worn item."""
        if not command.direct_object:
            self.display.print("Remove what?", color=Color.YELLOW)
            return
        # Check worn items first
        target_name = command.direct_object.lower()
        for item_id in list(self.player.worn):
            item = self.world.get_item(item_id)
            if item and item.matches(target_name):
                self.player.worn.remove(item_id)
                # Clear associated flags
                flag_map = {
                    'radiation_suit': 'has_radiation_suit',
                    'hazmat_suit': 'has_hazmat_suit',
                    'eva_suit': 'has_eva_suit',
                    'tactical_vest': 'has_armor',
                }
                flag = flag_map.get(item_id)
                if flag:
                    self.player.remove_flag(flag)
                self.display.print(f"You take off the {item.name}.", color=Color.BRIGHT_WHITE)
                return
        # Fall back to removing from container context
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if target:
            self.event_manager.fire_trigger(f"remove:{target.id}", self)
        else:
            self.display.print(f"You don't see any '{command.direct_object}' to remove.",
                             color=Color.YELLOW)

    # ─── Phase 0 Verb Handlers ─────────────────────────────────────────

    def do_sneak(self, command: Command):
        """Move quietly to avoid detection by hostile NPCs."""
        room = self.world.get_room(self.player.current_room)
        # Check for hostile NPCs in current room
        hostiles = [
            self.world.get_npc(nid) for nid in room.npcs
            if self.world.get_npc(nid) and self.world.get_npc(nid).present
            and self.world.get_npc(nid).alive and self.world.get_npc(nid).hostile
        ]
        self.player.add_flag("sneaking")
        if not hostiles:
            self.display.print("You move quietly, keeping to the shadows...",
                             color=Color.BRIGHT_BLACK)
        else:
            # Check for stealth success
            if self.player.has_flag("hiding") or room.dark:
                self.display.print("You slip past unnoticed, moving like a shadow...",
                                 color=Color.BRIGHT_BLACK)
            else:
                self.display.print("You try to move quietly, staying low...",
                                 color=Color.BRIGHT_BLACK)
        self.event_manager.fire_trigger(f"sneak:{room.id}", self)

    def do_crawl(self, command: Command):
        """Crawl through vents, crawlspaces, or tight passages."""
        room = self.world.get_room(self.player.current_room)
        target = command.direct_object

        if target:
            # Check if target matches an exit
            for direction, exit_obj in room.exits.items():
                dest_room = self.world.get_room(exit_obj.destination)
                if dest_room and (target in direction or target in dest_room.name.lower()
                                  or target in exit_obj.destination):
                    self.event_manager.fire_trigger(f"crawl:{target}", self)
                    command.direct_object = direction
                    self.do_go(command)
                    return
            # Check if target is an item
            item = self.world.find_item(self.player, room, target)
            if item:
                self.event_manager.fire_trigger(f"crawl:{item.id}", self)
                return

        # Check room for crawlspace exits
        crawl_exits = []
        for direction, exit_obj in room.exits.items():
            dest = self.world.get_room(exit_obj.destination)
            if dest and ('vent' in direction or 'crawl' in direction
                         or 'vent' in exit_obj.destination or 'crawl' in exit_obj.destination):
                crawl_exits.append(direction)
        if crawl_exits:
            self.display.hint(f"You could try crawling {', '.join(crawl_exits)}.")
        else:
            self.display.print("There's nowhere obvious to crawl here.", color=Color.YELLOW)
        self.event_manager.fire_trigger(f"crawl:{room.id}", self)

    def do_wear(self, command: Command):
        """Wear or equip an item from inventory."""
        if not command.direct_object:
            self.display.print("Wear or equip what?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}' to equip.",
                             color=Color.YELLOW)
            return
        if item.id in self.player.worn:
            is_weapon = 'weapon' in item.flags
            if is_weapon:
                self.display.print(f"The {item.name} is already equipped.",
                                 color=Color.YELLOW)
            else:
                self.display.print(f"You are already wearing the {item.name}.",
                                 color=Color.YELLOW)
            return
        # Add to worn/equipped list
        self.player.worn.append(item.id)
        # Set relevant flags based on item
        flag_map = {
            'radiation_suit': 'has_radiation_suit',
            'hazmat_suit': 'has_hazmat_suit',
            'eva_suit': 'has_eva_suit',
            'tactical_vest': 'has_armor',
            'cryo_jumpsuit': 'dressed',
        }
        flag = flag_map.get(item.id)
        if flag:
            self.player.add_flag(flag)
        # Appropriate verb based on item type
        is_weapon = 'weapon' in item.flags
        if is_weapon:
            self.display.success(f"You ready the {item.name}.")
        else:
            self.display.success(f"You put on the {item.name}.")

    def do_eat(self, command: Command):
        """Eat a consumable item."""
        if not command.direct_object:
            self.display.print("Eat what?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}' to eat.",
                             color=Color.YELLOW)
            return
        if not item.consumable:
            self.display.print(f"The {item.name} doesn't look edible.",
                             color=Color.YELLOW)
            return
        # Apply effects
        heal_amount = item.state.get('heal', 0)
        sanity_amount = item.state.get('sanity', 0)
        if heal_amount > 0:
            self.player.heal(heal_amount)
            self.display.success(f"You eat the {item.name}. (+{heal_amount} health)")
        elif sanity_amount > 0:
            self.player.restore_sanity(sanity_amount)
            self.display.success(f"You eat the {item.name}. (+{sanity_amount} sanity)")
        else:
            self.display.print(f"You eat the {item.name}. It's not great, but it's something.",
                             color=Color.BRIGHT_WHITE)
        self.player.remove_item(item.id)
        self.event_manager.fire_trigger(f"eat:{item.id}", self)

    def do_drink(self, command: Command):
        """Drink a consumable liquid."""
        if not command.direct_object:
            self.display.print("Drink what?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            # Check room for drinkable things
            room = self.world.get_room(self.player.current_room)
            item = self.world.find_item_in_room(room, command.direct_object)
            if not item:
                self.display.print(f"You don't see any '{command.direct_object}' to drink.",
                                 color=Color.YELLOW)
                return
        # Check for contamination
        if item.has_flag('contaminated'):
            self.display.print(f"You drink from the {item.name}... It tastes wrong. Metallic.",
                             color=Color.BRIGHT_MAGENTA)
            self.player.infect(5)
            self.display.warning("You feel something spreading through you.")
        else:
            # Apply healing/sanity effects
            heal_amount = item.state.get('heal', 0)
            sanity_amount = item.state.get('sanity', 0)
            if heal_amount > 0:
                self.player.heal(heal_amount)
                self.display.success(f"You drink the {item.name}. (+{heal_amount} health)")
            elif sanity_amount > 0:
                self.player.restore_sanity(sanity_amount)
                self.display.success(f"You drink the {item.name}. (+{sanity_amount} sanity)")
            else:
                self.display.print(f"You drink the {item.name}.", color=Color.BRIGHT_WHITE)
        if item.consumable:
            self.player.remove_item(item.id)
        self.event_manager.fire_trigger(f"drink:{item.id}", self)

    def do_throw(self, command: Command):
        """Throw an item. Useful for distractions during stealth."""
        if not command.direct_object:
            self.display.print("Throw what?", color=Color.YELLOW)
            return
        item = self.world.find_item_in_inventory(self.player, command.direct_object)
        if not item:
            self.display.print(f"You don't have any '{command.direct_object}' to throw.",
                             color=Color.YELLOW)
            return
        # Remove from inventory, place in room
        self.player.remove_item(item.id)
        room = self.world.get_room(self.player.current_room)
        room.add_item(item.id)
        self.display.print(f"You throw the {item.name}. It clatters across the floor.",
                         color=Color.BRIGHT_WHITE)
        self.event_manager.fire_trigger(f"throw:{item.id}", self)
        self.player.log_action(f"threw:{item.id}")

    def do_taste(self, command: Command):
        """Taste something cautiously."""
        if not command.direct_object:
            self.display.print("Taste what?", color=Color.YELLOW)
            return
        room = self.world.get_room(self.player.current_room)
        target = self.world.find_target(self.player, room, command.direct_object)
        if not target:
            item = self.world.find_item_in_inventory(self.player, command.direct_object)
            if not item:
                self.display.print(f"You don't see any '{command.direct_object}' to taste.",
                                 color=Color.YELLOW)
                return
            target = item
        self.event_manager.fire_trigger(f"taste:{target.id}", self)
        # Default flavor text
        if hasattr(target, 'has_flag') and target.has_flag('contaminated'):
            self.display.print(f"The {target.name} tastes metallic and wrong. You spit it out.",
                             color=Color.BRIGHT_MAGENTA)
        elif hasattr(target, 'has_flag') and target.has_flag('organic'):
            self.display.print(f"The {target.name} has a faintly bitter, biological taste.",
                             color=Color.BRIGHT_BLACK)
        else:
            self.display.print(f"The {target.name} doesn't taste like much.",
                             color=Color.BRIGHT_BLACK)

    def do_sleep(self, command: Command):
        """Sleep to restore health and sanity, at the risk of infection progression."""
        room = self.world.get_room(self.player.current_room)
        # Check for immediate danger
        hostiles = [
            self.world.get_npc(nid) for nid in room.npcs
            if self.world.get_npc(nid) and self.world.get_npc(nid).present
            and self.world.get_npc(nid).alive and self.world.get_npc(nid).hostile
        ]
        if hostiles:
            self.display.print("You can't sleep here. It's too dangerous.",
                             color=Color.YELLOW)
            return

        self.display.print("")
        self.display.print(
            "You find a quiet corner and close your eyes. Sleep takes you quickly -- "
            "a mercy in this place. Dreams come, fractured and strange. "
            "Corridors that stretch forever. A voice that is not your own.",
            color=Color.BRIGHT_BLACK
        )
        self.display.print("")

        # Advance time by 30 turns
        for _ in range(30):
            if self.player.advance_time(1):
                if not self.player.has_flag("saved_ship"):
                    self.display.warning("You wake with a start. Something has changed.")
                    self.trigger_ending("too_late")
                    return

        # Restore stats
        self.player.heal(15)
        self.player.restore_sanity(20)
        self.display.success("You wake, feeling slightly better. (+15 health, +20 sanity)")

        # Infection risk while sleeping
        if self.player.infection > 25:
            self.player.infect(5)
            self.display.print(
                "Your dreams were darker than usual. You feel something moving under your skin.",
                color=Color.BRIGHT_MAGENTA
            )

        self.event_manager.fire_trigger(f"sleep:{room.id}", self)

    # ─── Processing Systems ────────────────────────────────────────────

    def _process_hostile_npcs(self):
        """Process hostile NPC behavior at end of turn.

        Combat uses a WARNING system:
        - Turn 1 (NPC arrives): Warning text, NPC is 'threatening'. No damage.
        - Turn 2+: NPC attacks if player didn't flee, hide, or neutralize.
        This gives the player a full turn to react to every threat.
        """
        room = self.world.get_room(self.player.current_room)
        if not room:
            return

        # If player is sneaking and didn't attack, skip hostiles
        if self.player.has_flag("sneaking") and not self._attacked_this_turn:
            self.player.remove_flag("sneaking")
            return

        # Clear sneaking flag
        self.player.remove_flag("sneaking")

        for npc_id in list(room.npcs):
            npc = self.world.get_npc(npc_id)
            if not npc or not npc.present or not npc.alive or not npc.hostile:
                continue

            # Skip stunned NPCs
            if npc.has_flag('stunned'):
                stun_left = npc.state.get('stun_turns', 0) - 1
                if stun_left <= 0:
                    npc.remove_flag('stunned')
                    npc.state.pop('stun_turns', None)
                    self.display.print(
                        f"{npc.name} shakes off the stun and rises unsteadily.",
                        color=Color.YELLOW
                    )
                else:
                    npc.state['stun_turns'] = stun_left
                continue

            # Skip sedated NPCs
            if npc.has_flag('sedated'):
                continue

            # WARNING SYSTEM: First turn is a warning, not an attack.
            # 'threat_turn' tracks which turn the warning was issued.
            # Attack only happens on SUBSEQUENT turns.
            if not npc.state.get('threatening'):
                # First encounter - WARNING only, no damage
                npc.state['threatening'] = True
                npc.state['threat_turn'] = self.player.turn_count
                self.display.print("")
                self.display.warning(
                    f"{npc.name} is here - hostile and dangerous!"
                )
                self.display.print(
                    "You could: attack, use sedative, hide, sneak away, "
                    "or flee to another room.",
                    color=Color.BRIGHT_YELLOW
                )
                continue

            # Don't attack on the same turn the warning was issued
            if npc.state.get('threat_turn', -1) >= self.player.turn_count:
                continue

            # Turn 2+: NPC attacks
            damage = npc.damage
            # Armor reduction
            if 'tactical_vest' in self.player.worn:
                damage = max(1, damage - 5)
            self.player.take_damage(damage)
            self.display.print(
                f"{npc.name} lunges at you! (-{damage} HP)",
                color=Color.BRIGHT_RED
            )
            # Hint if health is getting low
            if self.player.health <= 30:
                self.display.hint(
                    "(You're badly hurt. Consider fleeing, hiding, or using a sedative.)"
                )
            if not self.player.is_alive():
                self.trigger_ending("death")
                return

    def _process_environmental_hazards(self):
        """Process environmental hazards in the current room."""
        room = self.world.get_room(self.player.current_room)
        if not room:
            return

        # Oxygen - drain in low-O2 rooms, recover in normal rooms
        if room.oxygen_level < 1.0:
            has_eva = 'eva_suit' in self.player.worn
            drain = int((1.0 - room.oxygen_level) * 10)
            if has_eva:
                drain = max(1, drain // 3)
            self.player.oxygen = max(0, self.player.oxygen - drain)
            if drain > 3:
                self.display.warning(f"Low oxygen! (-{drain} O2)")
            if self.player.oxygen <= 0:
                self.trigger_ending('death')
                return
        elif self.player.oxygen < self.player.max_oxygen:
            # Normal atmosphere - recover oxygen gradually
            recovery = 5
            old = self.player.oxygen
            self.player.oxygen = min(self.player.max_oxygen, self.player.oxygen + recovery)
            gained = self.player.oxygen - old
            if gained > 0 and self.player.oxygen < 80:
                self.display.print(
                    f"You breathe deeply. The air here is good. (+{gained} O2)",
                    color=Color.BRIGHT_BLUE
                )

        # Radiation
        if room.radiation > 0:
            has_rad_suit = 'radiation_suit' in self.player.worn
            damage = room.radiation
            if has_rad_suit:
                damage = max(0, damage - 3)
            if damage > 0:
                self.player.take_damage(damage)
                self.display.warning(f"Radiation exposure! (-{damage} HP)")

        # Infection from contaminated rooms
        if room.has_flag('contaminated'):
            has_hazmat = 'hazmat_suit' in self.player.worn
            if not has_hazmat:
                self.player.infect(2)
                self.display.print("You feel the contamination seeping in...",
                                 color=Color.BRIGHT_MAGENTA)

    def _process_hallucinations(self):
        """Process hallucination events based on player sanity."""
        if self.player.sanity >= 40:
            return

        # Chance increases as sanity drops
        chance = (40 - self.player.sanity) / 100  # 0% at 40, 40% at 0
        if random.random() > chance:
            return

        mild = [
            "For a moment, you think you hear footsteps behind you. There is no one there.",
            "A shadow moves at the edge of your vision. When you look, nothing.",
            "You smell something sweet and wrong. It passes.",
            "The walls seem to breathe for a moment. Then they are still.",
            "You hear your name whispered. The voice sounds like your own.",
        ]
        severe = [
            "A crew member walks past the doorway. You call out. No one answers. No one was there.",
            "The lights dim and you see silver threads in the walls. You blink and they are gone.",
            "For one terrible second, you cannot remember your own name.",
            "The Seed's voice speaks in your head: 'Come home.' You shake it off. Barely.",
            "You look at your hands and see silver veins beneath the skin. They fade. Were they real?",
        ]

        if self.player.sanity < 20:
            pool = severe + mild
        else:
            pool = mild

        self.display.print("")
        self.display.print(random.choice(pool), color=Color.BRIGHT_MAGENTA)

    # ─── Intro / Ending ────────────────────────────────────────────────

    def show_intro(self):
        """Display the game intro."""
        from content.intro import INTRO_TEXT, TITLE_ART
        self.display.clear()
        self.display.title_screen(TITLE_ART)
        self.display.print("")
        self.display.pause()
        self.display.clear()
        for section in INTRO_TEXT:
            self.display.print(section, color=Color.BRIGHT_WHITE)
            self.display.print("")
            self.display.pause()
            self.display.clear()

    def trigger_ending(self, ending_id: str):
        """Trigger a game ending."""
        self.ended = True
        self.ending_id = ending_id

    def show_ending(self):
        """Display the appropriate ending, including conditional epilogues."""
        try:
            from content.endings import ENDINGS, _has_flag
            ending = ENDINGS.get(self.ending_id or 'death')
            if ending:
                self.display.separator('═', Color.BRIGHT_RED)
                self.display.print(ending.get('title', 'THE END'),
                                 color=Color.BRIGHT_RED)
                self.display.separator('═', Color.BRIGHT_RED)
                self.display.print("")
                self.display.print(ending.get('text', ''),
                                 color=Color.BRIGHT_WHITE)

                # Append conditional epilogue paragraphs
                for ep in ending.get('epilogues', []):
                    show = False
                    if 'condition' in ep:
                        try:
                            show = ep['condition'](self)
                        except Exception:
                            show = False
                    elif 'flag' in ep:
                        show = _has_flag(self, ep['flag'])
                    if show:
                        self.display.print("")
                        self.display.print(ep['text'],
                                         color=Color.BRIGHT_WHITE)
            else:
                self.display.print("THE END", color=Color.BRIGHT_RED)
        except ImportError:
            self.display.print("THE END", color=Color.BRIGHT_RED)
