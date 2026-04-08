"""
Item system - handles all interactive objects in the game world.

Items can be:
- Portable (can be picked up)
- Fixed (scenery that can be examined/used)
- Containers (hold other items)
- Readable (books, logs, notes)
- Usable (keys, tools)
- Combinable (can be merged with other items)
"""

from typing import Optional, List, Dict, Callable, Any
from dataclasses import dataclass, field


@dataclass
class Item:
    """Represents an interactive object in the game world."""

    # Identity
    id: str                              # Unique identifier (e.g., "keycard_red")
    name: str                            # Display name (e.g., "red keycard")
    aliases: List[str] = field(default_factory=list)  # Alternative names

    # Descriptions
    description: str = ""                # Long description when examined
    short_description: str = ""          # Brief mention in room descriptions
    hidden_description: str = ""         # Description when hidden

    # Properties
    portable: bool = True                # Can be picked up
    visible: bool = True                 # Shows in room descriptions
    hidden: bool = False                 # Must be discovered via action
    scenery: bool = False                # Part of room, never portable

    # Container properties
    container: bool = False              # Can hold other items
    capacity: int = 999                  # Max items held
    contents: List[str] = field(default_factory=list)  # IDs of items inside
    closed: bool = False                 # Is the container closed
    openable: bool = False               # Can be opened/closed
    locked: bool = False                 # Requires key to open
    key_id: Optional[str] = None         # Required key item ID
    lock_code: Optional[str] = None      # Code to unlock (for keypads)

    # Readable properties
    readable: bool = False               # Can be read
    read_text: str = ""                  # Content when read

    # Usable properties
    usable: bool = False                 # Has a 'use' action
    use_text: str = ""                   # What happens when used
    use_target: Optional[str] = None     # What this must be used ON
    consumable: bool = False             # Destroyed when used

    # State
    state: Dict[str, Any] = field(default_factory=dict)
    flags: List[str] = field(default_factory=list)

    # Weight/size (for inventory limits)
    weight: int = 1                      # Abstract weight units

    # Event hooks
    on_examine: Optional[str] = None     # Event ID to trigger on examine
    on_take: Optional[str] = None        # Event ID to trigger on take
    on_use: Optional[str] = None         # Event ID to trigger on use
    on_drop: Optional[str] = None        # Event ID to trigger on drop
    on_read: Optional[str] = None        # Event ID to trigger on read

    def matches(self, name: str) -> bool:
        """Check if this item matches a given name (fuzzy)."""
        return self.match_score(name) > 0

    def match_score(self, name: str) -> int:
        """Return a match quality score (0 = no match, higher = better match).

        Scoring:
          100 = exact ID match
           90 = exact name match
           80 = exact alias match
           70 = input matches full name as substring AND covers most of it
           60 = all input words found in item name/aliases
           40 = input is a substring of name or alias
           20 = alias is a substring of input
           10 = partial word overlap
            0 = no match
        """
        if not name:
            return 0
        name = name.lower().strip()
        item_name = self.name.lower()

        # Exact ID match (highest priority)
        if name == self.id.lower():
            return 100

        # Exact name match
        if name == item_name:
            return 90

        # Exact alias match
        for alias in self.aliases:
            if name == alias.lower():
                return 80

        # All input words found in item name words (good specificity)
        name_words = name.split()
        item_words = item_name.split()
        if len(name_words) > 1 and all(nw in item_words for nw in name_words):
            # Bonus for matching more of the item's total words
            coverage = len(name_words) / max(len(item_words), 1)
            return 60 + int(coverage * 15)

        # Input is a substring of name (e.g., "kirilov datapad" in "kirilov's datapad")
        if name in item_name:
            # Score based on how much of the name is covered
            coverage = len(name) / max(len(item_name), 1)
            return 40 + int(coverage * 25)

        # Alias substring matches
        for alias in self.aliases:
            alias_lower = alias.lower()
            if name in alias_lower:
                coverage = len(name) / max(len(alias_lower), 1)
                return 40 + int(coverage * 20)
            if alias_lower in name:
                return 20

        # Single-word partial: input word found in item name
        if len(name_words) == 1 and name_words[0] in item_words:
            return 10

        # All input words found somewhere in name (even partial)
        if all(any(nw in iw for iw in item_words) for nw in name_words):
            return 5

        return 0

    def get_description(self) -> str:
        """Return the current description based on state."""
        desc = self.description

        if self.container and self.openable:
            if self.closed:
                desc += "\n\nIt appears to be closed."
            elif self.contents:
                desc += "\n\nIt is open."
            else:
                desc += "\n\nIt is open and empty."

        if self.locked:
            desc += "\n\nIt is locked."

        return desc

    def get_short_description(self) -> str:
        """Return brief description for room listings."""
        if self.short_description:
            return self.short_description
        return f"You see {self.name} here."

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
            'contents': self.contents,
            'closed': self.closed,
            'locked': self.locked,
            'hidden': self.hidden,
            'visible': self.visible,
            'state': self.state,
            'flags': self.flags,
        }

    def from_dict(self, data: dict):
        """Restore state from save game."""
        self.contents = data.get('contents', self.contents)
        self.closed = data.get('closed', self.closed)
        self.locked = data.get('locked', self.locked)
        self.hidden = data.get('hidden', self.hidden)
        self.visible = data.get('visible', self.visible)
        self.state = data.get('state', self.state)
        self.flags = data.get('flags', self.flags)
