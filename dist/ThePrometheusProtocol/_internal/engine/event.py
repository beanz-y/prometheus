"""
Event system - handles scripted events, triggers, and time-based occurrences.

Events can be:
- One-shot: fire once when triggered
- Repeating: fire each time the trigger condition is met
- Scheduled: fire on a specific turn or time
- Conditional: fire when multiple flags align
- Cascading: one event fires another

Events have conditions that must be met and actions to execute.
"""

from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field


@dataclass
class Event:
    """A scripted event in the game world."""

    id: str
    description: str = ""               # Author note
    fired: bool = False                 # Has this event run?
    repeatable: bool = False            # Can it fire multiple times?

    # Trigger conditions
    triggers: List[str] = field(default_factory=list)  # Trigger type: "enter:room_id", "take:item_id", etc.

    # Prerequisites
    required_flags: List[str] = field(default_factory=list)      # Flags that must be set
    forbidden_flags: List[str] = field(default_factory=list)     # Flags that must NOT be set
    required_items: List[str] = field(default_factory=list)      # Items player must have
    required_turn: Optional[int] = None                           # Minimum turn
    required_time: Optional[int] = None                           # Game time threshold
    interval: Optional[int] = None                                # Fire every N turns (repeating)

    # Effects
    narrative: str = ""                 # Text to display
    set_flags: List[str] = field(default_factory=list)
    clear_flags: List[str] = field(default_factory=list)
    give_items: List[str] = field(default_factory=list)
    remove_items: List[str] = field(default_factory=list)
    spawn_items: List[Dict[str, str]] = field(default_factory=list)  # [{'item': id, 'room': id}]
    move_npc: Optional[Dict[str, str]] = None                        # {'npc': id, 'to': room_id}
    unlock_exit: Optional[Dict[str, str]] = None                     # {'room': id, 'direction': d}
    lock_exit: Optional[Dict[str, str]] = None
    reveal_exit: Optional[Dict[str, str]] = None

    # Objectives
    add_objective: Optional[Dict[str, Any]] = None  # {'id': id, 'description': text}
    complete_objective: Optional[str] = None

    # Player effects
    damage: int = 0
    heal: int = 0
    sanity_change: int = 0
    infection_change: int = 0
    knowledge_added: List[str] = field(default_factory=list)

    # Cascading
    trigger_events: List[str] = field(default_factory=list)  # Other event IDs to fire
    end_game: Optional[str] = None                           # Ending ID to trigger

    # Callback function for complex events
    callback: Optional[Callable] = None

    def can_fire(self, game) -> bool:
        """Check if this event's prerequisites are met."""
        if self.fired and not self.repeatable:
            return False

        player = game.player
        world = game.world

        # Check required flags
        for flag in self.required_flags:
            if not (player.has_flag(flag) or world.has_flag(flag)):
                return False

        # Check forbidden flags
        for flag in self.forbidden_flags:
            if player.has_flag(flag) or world.has_flag(flag):
                return False

        # Check required items
        for item_id in self.required_items:
            if not player.has_item(item_id):
                return False

        # Check turn count
        if self.required_turn is not None and player.turn_count < self.required_turn:
            return False

        if self.required_time is not None and player.game_time_minutes < self.required_time:
            return False

        return True

    def fire(self, game):
        """Execute this event."""
        if not self.can_fire(game):
            return False

        player = game.player
        world = game.world
        display = game.display

        # Display narrative
        if self.narrative:
            display.print("")
            display.narrate(self.narrative)

        # Set flags
        for flag in self.set_flags:
            if flag.startswith('world.'):
                world.set_flag(flag[6:])
            else:
                player.add_flag(flag)

        # Clear flags
        for flag in self.clear_flags:
            if flag.startswith('world.'):
                world.clear_flag(flag[6:])
            else:
                player.remove_flag(flag)

        # Give items
        for item_id in self.give_items:
            player.add_item(item_id)
            item = world.get_item(item_id)
            if item:
                display.success(f"You now have: {item.name}")

        # Remove items
        for item_id in self.remove_items:
            player.remove_item(item_id)
            world.destroy_item(item_id)

        # Spawn items
        for spawn in self.spawn_items:
            world.spawn_item(spawn['item'], spawn['room'])

        # Move NPC
        if self.move_npc:
            world.move_npc(self.move_npc['npc'], self.move_npc.get('to'))

        # Unlock/lock/reveal exits
        if self.unlock_exit:
            room = world.get_room(self.unlock_exit['room'])
            if room and self.unlock_exit['direction'] in room.exits:
                room.exits[self.unlock_exit['direction']].locked = False

        if self.lock_exit:
            room = world.get_room(self.lock_exit['room'])
            if room and self.lock_exit['direction'] in room.exits:
                room.exits[self.lock_exit['direction']].locked = True

        if self.reveal_exit:
            room = world.get_room(self.reveal_exit['room'])
            if room and self.reveal_exit['direction'] in room.exits:
                room.exits[self.reveal_exit['direction']].discovered = True
                room.exits[self.reveal_exit['direction']].hidden = False

        # Objectives
        if self.add_objective:
            player.add_objective(
                self.add_objective['id'],
                self.add_objective['description'],
                self.add_objective.get('priority', 1)
            )
            display.success(f"New objective: {self.add_objective['description']}")

        if self.complete_objective:
            if player.complete_objective(self.complete_objective):
                display.success("Objective complete!")

        # Player effects
        if self.damage > 0:
            player.take_damage(self.damage)
            display.warning(f"You take {self.damage} damage.")

        if self.heal > 0:
            player.heal(self.heal)
            display.success(f"You recover {self.heal} health.")

        if self.sanity_change < 0:
            player.lose_sanity(-self.sanity_change)
        elif self.sanity_change > 0:
            player.restore_sanity(self.sanity_change)

        if self.infection_change != 0:
            if self.infection_change > 0:
                player.infect(self.infection_change)
            else:
                player.treat_infection(-self.infection_change)

        # Knowledge
        for fact in self.knowledge_added:
            player.add_knowledge(fact)

        # Callback for complex events
        if self.callback:
            self.callback(game)

        # Chain other events
        for event_id in self.trigger_events:
            other = game.event_manager.get_event(event_id)
            if other:
                other.fire(game)

        # Ending
        if self.end_game:
            game.trigger_ending(self.end_game)

        self.fired = True
        return True


class EventManager:
    """Manages all events and checks for trigger conditions."""

    def __init__(self):
        self.events: Dict[str, Event] = {}
        # Index events by trigger type for fast lookup
        self.trigger_index: Dict[str, List[str]] = {}

    def add_event(self, event: Event):
        self.events[event.id] = event
        for trigger in event.triggers:
            if trigger not in self.trigger_index:
                self.trigger_index[trigger] = []
            self.trigger_index[trigger].append(event.id)

    def get_event(self, event_id: str) -> Optional[Event]:
        return self.events.get(event_id)

    def fire_trigger(self, trigger: str, game) -> int:
        """Check all events for this trigger and fire them if conditions met.
        Returns number of events fired.
        """
        fired_count = 0
        event_ids = self.trigger_index.get(trigger, [])
        for event_id in event_ids:
            event = self.events.get(event_id)
            if event and event.can_fire(game):
                if event.fire(game):
                    fired_count += 1
        return fired_count

    def check_timed_events(self, game) -> int:
        """Check for events that should fire based on time/turn count."""
        fired_count = 0
        for event in self.events.values():
            # Check interval-based repeating events
            if event.interval is not None:
                if game.player.turn_count > 0 and game.player.turn_count % event.interval == 0:
                    if event.can_fire(game):
                        if event.fire(game):
                            event.fired = False  # Allow to fire again next interval
                            fired_count += 1
                continue
            if event.required_turn is not None or event.required_time is not None:
                if not event.fired or event.repeatable:
                    if event.can_fire(game):
                        if event.fire(game):
                            fired_count += 1
        return fired_count

    def to_dict(self) -> dict:
        return {
            'fired': [eid for eid, e in self.events.items() if e.fired]
        }

    def from_dict(self, data: dict):
        fired_ids = set(data.get('fired', []))
        for eid, event in self.events.items():
            event.fired = eid in fired_ids
