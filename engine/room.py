"""
Room system - represents locations in the game world.

Rooms can be:
- Connected to other rooms in 8+ directions
- Contain items and NPCs
- Have locked/gated exits requiring conditions
- Have ambient descriptions that change based on game state
- Trigger events upon entry/exit
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Exit:
    """Represents a passage between rooms."""
    direction: str                      # 'north', 'up', 'forward', etc.
    destination: str                    # Room ID
    description: str = ""               # Text shown when moving this way
    locked: bool = False                # Cannot traverse
    lock_message: str = "That way is blocked."
    key_id: Optional[str] = None        # Item ID that unlocks
    required_flag: Optional[str] = None # Player/world flag required
    hidden: bool = False                # Hidden until discovered
    discovered: bool = False


@dataclass
class Room:
    """Represents a location in the game world."""

    # Identity
    id: str                             # Unique identifier
    name: str                           # Display name
    deck: str = ""                      # Which deck of the ship

    # Descriptions - can change based on state
    description: str = ""               # Primary description
    first_visit_text: str = ""          # Extra text shown only on first visit
    dark_description: str = ""          # Shown when no light
    alt_descriptions: Dict[str, str] = field(default_factory=dict)  # flag-based

    # Connections
    exits: Dict[str, Exit] = field(default_factory=dict)

    # Contents
    items: List[str] = field(default_factory=list)  # Item IDs
    npcs: List[str] = field(default_factory=list)   # NPC IDs

    # State
    visited: bool = False
    dark: bool = False                  # Requires light source
    flags: List[str] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)

    # Sensory
    smell_text: str = ""
    touch_text: str = ""

    # Atmosphere
    ambient_sounds: List[str] = field(default_factory=list)  # Random ambient text
    scripted_events: List[str] = field(default_factory=list) # Event IDs tied to room

    # Hooks
    on_enter: Optional[str] = None      # Event ID on first entry
    on_look: Optional[str] = None       # Event ID when looking
    on_leave: Optional[str] = None      # Event ID when leaving
    on_enter_repeat: Optional[str] = None  # Event ID on every entry

    # Meta
    danger_level: int = 0               # 0=safe, higher=dangerous
    oxygen_level: float = 1.0           # 1.0 = normal, 0 = vacuum
    temperature: int = 20               # Celsius
    radiation: int = 0                  # Radiation exposure

    def get_description(self, world_flags: set = None) -> str:
        """Return current description based on state."""
        if world_flags is None:
            world_flags = set()

        # Check for alt descriptions triggered by flags
        for flag, text in self.alt_descriptions.items():
            if flag in world_flags or flag in self.flags:
                return text

        if self.dark and 'has_light' not in world_flags:
            return self.dark_description or "It is pitch black. You can't see anything."

        desc = self.description
        if not self.visited and self.first_visit_text:
            desc = self.first_visit_text + "\n\n" + desc

        return desc

    def get_exits_description(self) -> str:
        """Return a description of available exits."""
        visible_exits = [
            d for d, e in self.exits.items()
            if not e.hidden or e.discovered
        ]
        if not visible_exits:
            return "There are no obvious exits."
        if len(visible_exits) == 1:
            return f"The only exit leads {visible_exits[0]}."
        exits_str = ', '.join(visible_exits[:-1]) + f", and {visible_exits[-1]}"
        return f"Exits lead {exits_str}."

    def add_exit(self, direction: str, destination: str, **kwargs):
        """Add an exit to this room."""
        self.exits[direction] = Exit(
            direction=direction,
            destination=destination,
            **kwargs
        )

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from this room."""
        if item_id in self.items:
            self.items.remove(item_id)
            return True
        return False

    def add_item(self, item_id: str):
        """Add an item to this room."""
        if item_id not in self.items:
            self.items.append(item_id)

    def has_item(self, item_id: str) -> bool:
        return item_id in self.items

    def remove_npc(self, npc_id: str) -> bool:
        if npc_id in self.npcs:
            self.npcs.remove(npc_id)
            return True
        return False

    def add_npc(self, npc_id: str):
        if npc_id not in self.npcs:
            self.npcs.append(npc_id)

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def add_flag(self, flag: str):
        if flag not in self.flags:
            self.flags.append(flag)

    def remove_flag(self, flag: str):
        if flag in self.flags:
            self.flags.remove(flag)

    def to_dict(self) -> dict:
        """Serialize for save games."""
        return {
            'id': self.id,
            'visited': self.visited,
            'items': self.items,
            'npcs': self.npcs,
            'flags': self.flags,
            'state': self.state,
            'dark': self.dark,
            'oxygen_level': self.oxygen_level,
            'exits_discovered': {
                d: e.discovered for d, e in self.exits.items() if e.hidden
            },
            'exits_locked': {
                d: e.locked for d, e in self.exits.items()
            },
        }

    def from_dict(self, data: dict):
        """Restore state from save game."""
        self.visited = data.get('visited', self.visited)
        self.items = data.get('items', self.items)
        self.npcs = data.get('npcs', self.npcs)
        self.flags = data.get('flags', self.flags)
        self.state = data.get('state', self.state)
        self.dark = data.get('dark', self.dark)
        self.oxygen_level = data.get('oxygen_level', self.oxygen_level)

        for direction, discovered in data.get('exits_discovered', {}).items():
            if direction in self.exits:
                self.exits[direction].discovered = discovered
        for direction, locked in data.get('exits_locked', {}).items():
            if direction in self.exits:
                self.exits[direction].locked = locked
