"""
Player system - tracks the player character's state, inventory, and progress.
"""

from typing import Optional, List, Dict, Any, Set
from dataclasses import dataclass, field


@dataclass
class Player:
    """Represents the player character."""

    # Identity
    name: str = "Dr. Alex Chen"
    title: str = "Chief Xenobiologist"

    # Location
    current_room: str = "cryo_bay"
    previous_room: Optional[str] = None

    # Inventory
    inventory: List[str] = field(default_factory=list)  # Item IDs carried
    worn: List[str] = field(default_factory=list)       # Currently worn items
    max_carry: int = 15                                  # Inventory slots

    # Stats
    health: int = 100
    max_health: int = 100
    sanity: int = 100
    max_sanity: int = 100
    oxygen: int = 100
    max_oxygen: int = 100
    infection: int = 0                                   # Hidden stat - parasitic infection

    # Progress tracking
    flags: Set[str] = field(default_factory=set)
    discovered_rooms: Set[str] = field(default_factory=set)
    read_logs: Set[str] = field(default_factory=set)
    known_codes: Dict[str, str] = field(default_factory=dict)
    objectives: List[Dict[str, Any]] = field(default_factory=list)
    completed_objectives: List[str] = field(default_factory=list)

    # Story/knowledge
    knowledge: Set[str] = field(default_factory=set)    # Facts the player has learned
    memories: List[str] = field(default_factory=list)   # Recoverable memories
    memory_fragments: Dict[str, str] = field(default_factory=dict)  # id -> display text

    # Consequence tracking
    action_log: List[str] = field(default_factory=list)

    # Meta
    turn_count: int = 0
    game_time_minutes: int = 0                           # Time elapsed in story
    time_until_catastrophe: int = 1080                   # Minutes until ship destruction (18 hours)

    def add_item(self, item_id: str) -> bool:
        """Add an item to inventory if there's space."""
        if len(self.inventory) >= self.max_carry:
            return False
        if item_id not in self.inventory:
            self.inventory.append(item_id)
        return True

    def remove_item(self, item_id: str) -> bool:
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        return item_id in self.inventory

    def add_flag(self, flag: str):
        self.flags.add(flag)

    def remove_flag(self, flag: str):
        self.flags.discard(flag)

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def add_knowledge(self, fact: str):
        self.knowledge.add(fact)

    def knows(self, fact: str) -> bool:
        return fact in self.knowledge

    def add_objective(self, obj_id: str, description: str, priority: int = 1):
        """Add a new objective to the player's quest log."""
        if not any(o['id'] == obj_id for o in self.objectives):
            self.objectives.append({
                'id': obj_id,
                'description': description,
                'priority': priority,
                'completed': False,
            })

    def complete_objective(self, obj_id: str):
        """Mark an objective as completed."""
        for obj in self.objectives:
            if obj['id'] == obj_id:
                obj['completed'] = True
                if obj_id not in self.completed_objectives:
                    self.completed_objectives.append(obj_id)
                return True
        return False

    def remove_objective(self, obj_id: str):
        self.objectives = [o for o in self.objectives if o['id'] != obj_id]

    def take_damage(self, amount: int):
        self.health = max(0, self.health - amount)

    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)

    def lose_sanity(self, amount: int):
        self.sanity = max(0, self.sanity - amount)

    def restore_sanity(self, amount: int):
        self.sanity = min(self.max_sanity, self.sanity + amount)

    def infect(self, amount: int):
        self.infection = min(100, self.infection + amount)

    def treat_infection(self, amount: int):
        self.infection = max(0, self.infection - amount)

    def add_memory(self, memory_id: str, text: str) -> bool:
        """Add a memory fragment. Returns True if new."""
        if memory_id not in self.memory_fragments:
            self.memory_fragments[memory_id] = text
            return True
        return False

    def get_memory_count(self) -> int:
        return len(self.memory_fragments)

    def has_memory(self, memory_id: str) -> bool:
        return memory_id in self.memory_fragments

    def log_action(self, action: str):
        """Record a significant player action for consequence tracking."""
        if action not in self.action_log:
            self.action_log.append(action)

    def has_done(self, action: str) -> bool:
        return action in self.action_log

    def is_alive(self) -> bool:
        return self.health > 0 and self.oxygen > 0

    def advance_time(self, minutes: int = 1):
        """Advance game time. Returns True if time runs out."""
        self.game_time_minutes += minutes
        self.time_until_catastrophe -= minutes
        self.turn_count += 1
        return self.time_until_catastrophe <= 0

    def get_time_remaining_str(self) -> str:
        """Return a formatted time-remaining string."""
        mins = self.time_until_catastrophe
        if mins <= 0:
            return "00:00:00"
        hours = mins // 60
        minutes = mins % 60
        return f"T-{hours:02d}:{minutes:02d}:00"

    def to_dict(self) -> dict:
        """Serialize for save games."""
        return {
            'name': self.name,
            'current_room': self.current_room,
            'previous_room': self.previous_room,
            'inventory': self.inventory,
            'worn': self.worn,
            'health': self.health,
            'sanity': self.sanity,
            'oxygen': self.oxygen,
            'infection': self.infection,
            'flags': list(self.flags),
            'discovered_rooms': list(self.discovered_rooms),
            'read_logs': list(self.read_logs),
            'known_codes': self.known_codes,
            'objectives': self.objectives,
            'completed_objectives': self.completed_objectives,
            'knowledge': list(self.knowledge),
            'memories': self.memories,
            'memory_fragments': self.memory_fragments,
            'action_log': self.action_log,
            'turn_count': self.turn_count,
            'game_time_minutes': self.game_time_minutes,
            'time_until_catastrophe': self.time_until_catastrophe,
        }

    def from_dict(self, data: dict):
        """Restore from save game."""
        self.name = data.get('name', self.name)
        self.current_room = data.get('current_room', self.current_room)
        self.previous_room = data.get('previous_room')
        self.inventory = data.get('inventory', [])
        self.worn = data.get('worn', [])
        self.health = data.get('health', 100)
        self.sanity = data.get('sanity', 100)
        self.oxygen = data.get('oxygen', 100)
        self.infection = data.get('infection', 0)
        self.flags = set(data.get('flags', []))
        self.discovered_rooms = set(data.get('discovered_rooms', []))
        self.read_logs = set(data.get('read_logs', []))
        self.known_codes = data.get('known_codes', {})
        self.objectives = data.get('objectives', [])
        self.completed_objectives = data.get('completed_objectives', [])
        self.knowledge = set(data.get('knowledge', []))
        self.memories = data.get('memories', [])
        self.memory_fragments = data.get('memory_fragments', {})
        self.action_log = data.get('action_log', [])
        self.turn_count = data.get('turn_count', 0)
        self.game_time_minutes = data.get('game_time_minutes', 0)
        self.time_until_catastrophe = data.get('time_until_catastrophe', 1080)
