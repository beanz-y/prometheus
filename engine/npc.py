"""
NPC system - non-player characters including crew, AI, and creatures.

NPCs can be:
- Dead (provide logs, items, story clues)
- Alive (talk, give quests, combat)
- Hostile (attack, must be avoided or fought)
- Systems (AIs, computer terminals with personality)
- Dynamic (change state based on story progression)
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NPC:
    """Represents a non-player character in the game."""

    # Identity
    id: str
    name: str
    title: str = ""                       # "Captain", "Dr.", etc.
    aliases: List[str] = field(default_factory=list)

    # Descriptions
    description: str = ""                  # When examined
    short_description: str = ""            # Brief mention in rooms

    # State
    alive: bool = True
    hostile: bool = False
    present: bool = True                   # Currently in the world
    location: str = ""                     # Current room ID

    # Dialogue
    dialogue_tree: Optional[str] = None    # Dialogue tree ID to use
    current_topic: Optional[str] = None
    topics_discussed: List[str] = field(default_factory=list)
    default_response: str = "They don't respond."
    greeting: str = ""                     # First time seeing them
    farewell: str = ""

    # Combat / interaction
    health: int = 100
    damage: int = 10
    defense: int = 0

    # State flags
    flags: List[str] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)

    # Items they carry (dead NPCs drop items)
    inventory: List[str] = field(default_factory=list)

    # Hooks
    on_meet: Optional[str] = None          # First encounter event
    on_talk: Optional[str] = None          # Every talk event
    on_death: Optional[str] = None         # When killed
    on_examine: Optional[str] = None

    # Patrol / AI
    patrol_route: List[str] = field(default_factory=list)  # Room IDs for patrol
    vulnerability: str = ""                 # Weak point (e.g., "fire", "plasma")

    # Metadata for story
    role: str = ""                         # "crew", "enemy", "ally", "system"
    backstory: str = ""                    # Reference for author

    def matches(self, name: str) -> bool:
        """Check if name refers to this NPC."""
        return self.match_score(name) > 0

    def match_score(self, name: str) -> int:
        """Return match quality score (0 = no match, higher = better)."""
        if not name:
            return 0
        name = name.lower().strip()
        if name == self.id.lower():
            return 100
        if name == self.name.lower():
            return 90
        for alias in self.aliases:
            if name == alias.lower():
                return 80
        # State-based aliases: "body"/"corpse" for dead NPCs, "unconscious" for sedated
        if not self.alive and name in ('body', 'corpse', 'dead body', 'remains'):
            return 60
        if self.has_flag('sedated') and name in ('body', 'unconscious', 'unconscious body',
                                                  'sleeping', 'sedated', 'collapsed'):
            return 60
        # Full title+name match
        full = f"{self.title} {self.name}".lower().strip()
        if name == full:
            return 85
        # Last name exact match
        last_name = self.name.split()[-1].lower() if self.name else ""
        if last_name and name == last_name:
            return 70
        # Partial name match (substring)
        if name in self.name.lower():
            coverage = len(name) / max(len(self.name), 1)
            return 40 + int(coverage * 20)
        if name in full:
            return 35
        # Partial alias match
        for alias in self.aliases:
            alias_lower = alias.lower()
            if name in alias_lower:
                return 30
            if alias_lower in name:
                return 20
        return 0

    def get_description(self) -> str:
        """Return description based on current state."""
        if self.has_flag('sedated'):
            return (
                f"{self.name} lies crumpled on the deck, unconscious. The "
                f"sedative has taken full effect. Their breathing is shallow "
                f"but steady, and the silver veins beneath their skin have "
                f"dimmed to a faint grey. They are alive, but not a threat. "
                f"For now."
            )
        desc = self.description
        if not self.alive:
            desc += "\n\nThey are not moving. Not breathing. Dead."
        elif self.hostile:
            desc += "\n\nThey regard you with open hostility."
        return desc

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
            'alive': self.alive,
            'hostile': self.hostile,
            'present': self.present,
            'location': self.location,
            'health': self.health,
            'topics_discussed': self.topics_discussed,
            'inventory': self.inventory,
            'flags': self.flags,
            'state': self.state,
        }

    def from_dict(self, data: dict):
        """Restore state from save game."""
        self.alive = data.get('alive', self.alive)
        self.hostile = data.get('hostile', self.hostile)
        self.present = data.get('present', self.present)
        self.location = data.get('location', self.location)
        self.health = data.get('health', self.health)
        self.topics_discussed = data.get('topics_discussed', self.topics_discussed)
        self.inventory = data.get('inventory', self.inventory)
        self.flags = data.get('flags', self.flags)
        self.state = data.get('state', self.state)
