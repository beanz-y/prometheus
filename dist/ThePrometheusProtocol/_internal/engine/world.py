"""
World manager - the central registry for all game entities and state.

Holds all rooms, items, NPCs, and world-level flags/state.
Handles entity lookup, relationships, and queries.
"""

from typing import Optional, List, Dict, Any, Set
from .room import Room, Exit
from .item import Item
from .npc import NPC


class World:
    """Central manager for all game entities."""

    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.items: Dict[str, Item] = {}
        self.npcs: Dict[str, NPC] = {}

        # World-level flags (tracked separately from player/room/item flags)
        self.flags: Set[str] = set()
        self.state: Dict[str, Any] = {}

        # Counters and trackers
        self.event_log: List[str] = []   # History of key events

    # ─── Registration ──────────────────────────────────────────────────

    def add_room(self, room: Room):
        self.rooms[room.id] = room

    def add_item(self, item: Item):
        self.items[item.id] = item

    def add_npc(self, npc: NPC):
        self.npcs[npc.id] = npc

    # ─── Lookup ────────────────────────────────────────────────────────

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.items.get(item_id)

    def get_npc(self, npc_id: str) -> Optional[NPC]:
        return self.npcs.get(npc_id)

    # ─── Fuzzy matching ────────────────────────────────────────────────

    def find_item_in_room(self, room: Room, name: str) -> Optional[Item]:
        """Find the BEST matching item by name in the given room."""
        name = name.lower().strip()
        best_item = None
        best_score = 0

        # Check items in the room
        for item_id in room.items:
            item = self.items.get(item_id)
            if item and item.visible and not item.hidden:
                score = item.match_score(name)
                if score > best_score:
                    best_score = score
                    best_item = item

        # Check items inside open containers in the room
        for item_id in room.items:
            container = self.items.get(item_id)
            if container and container.container and not container.closed:
                for inner_id in container.contents:
                    inner = self.items.get(inner_id)
                    if inner:
                        score = inner.match_score(name)
                        if score > best_score:
                            best_score = score
                            best_item = inner

        return best_item

    def find_item_in_inventory(self, player, name: str) -> Optional[Item]:
        """Find the BEST matching item by name in player inventory,
        including items inside open containers the player is carrying."""
        name = name.lower().strip()
        best_item = None
        best_score = 0

        for item_id in player.inventory:
            item = self.items.get(item_id)
            if not item:
                continue
            # Check the item itself
            score = item.match_score(name)
            if score > best_score:
                best_score = score
                best_item = item
            # Check inside open containers in inventory
            if item.container and not item.closed:
                for inner_id in item.contents:
                    inner = self.items.get(inner_id)
                    if inner:
                        score = inner.match_score(name)
                        if score > best_score:
                            best_score = score
                            best_item = inner

        return best_item

    def find_item(self, player, room: Room, name: str) -> Optional[Item]:
        """Find an item in inventory or current room. Prefers best match."""
        inv_item = self.find_item_in_inventory(player, name)
        room_item = self.find_item_in_room(room, name)

        if inv_item and not room_item:
            return inv_item
        if room_item and not inv_item:
            return room_item
        if inv_item and room_item:
            # Return whichever is a better match
            inv_score = inv_item.match_score(name)
            room_score = room_item.match_score(name)
            return inv_item if inv_score >= room_score else room_item
        return None

    def find_npc_in_room(self, room: Room, name: str) -> Optional[NPC]:
        """Find the BEST matching NPC by name in the given room."""
        name = name.lower().strip()
        best_npc = None
        best_score = 0
        for npc_id in room.npcs:
            npc = self.npcs.get(npc_id)
            if npc and npc.present:
                score = npc.match_score(name)
                if score > best_score:
                    best_score = score
                    best_npc = npc
        return best_npc

    def find_target(self, player, room: Room, name: str):
        """Find any entity (item or NPC) matching a name.

        Uses scoring to pick the BEST match across items and NPCs.
        This prevents 'attack kirilov' from finding 'kirilov_datapad'
        instead of the NPC Kirilov.
        """
        item = self.find_item(player, room, name)
        npc = self.find_npc_in_room(room, name)

        if item and not npc:
            return item
        if npc and not item:
            return npc
        if item and npc:
            # Both matched - compare scores, prefer the better match
            item_score = item.match_score(name)
            npc_score = npc.match_score(name)
            # Prefer NPC on ties (NPCs are more likely interaction targets)
            return npc if npc_score >= item_score else item
        return None

    # ─── Item operations ───────────────────────────────────────────────

    def move_item(self, item_id: str, from_location: str, to_location: str):
        """Move an item between rooms or containers."""
        # from_location/to_location can be room IDs, npc IDs, or 'player'
        # Remove from source
        if from_location in self.rooms:
            self.rooms[from_location].remove_item(item_id)
        elif from_location in self.items:
            self.items[from_location].contents.remove(item_id)
        # Add to destination
        if to_location in self.rooms:
            self.rooms[to_location].add_item(item_id)
        elif to_location in self.items:
            if item_id not in self.items[to_location].contents:
                self.items[to_location].contents.append(item_id)

    def destroy_item(self, item_id: str):
        """Completely remove an item from the world."""
        # Remove from all rooms
        for room in self.rooms.values():
            room.remove_item(item_id)
        # Remove from all containers
        for item in self.items.values():
            if item_id in item.contents:
                item.contents.remove(item_id)

    def spawn_item(self, item_id: str, room_id: str):
        """Place an item into a room."""
        if room_id in self.rooms:
            self.rooms[room_id].add_item(item_id)

    # ─── NPC operations ────────────────────────────────────────────────

    def move_npc(self, npc_id: str, new_room: Optional[str]):
        """Move an NPC to a new room (or None to remove)."""
        npc = self.npcs.get(npc_id)
        if not npc:
            return
        # Remove from old location
        if npc.location in self.rooms:
            self.rooms[npc.location].remove_npc(npc_id)
        # Add to new
        if new_room:
            npc.location = new_room
            if new_room in self.rooms:
                self.rooms[new_room].add_npc(npc_id)
            npc.present = True
        else:
            npc.present = False

    def advance_npc_patrols(self, turn_count: int, player_room: str = ""):
        """Move NPCs along their patrol routes.

        NPCs move every 3 turns (not every turn).
        NPCs do NOT move away from the player's room if they're in combat
        (hostile + same room as player). This gives the player time to react.
        """
        if turn_count % 3 != 0:
            return  # Only move every 3rd turn

        for npc in self.npcs.values():
            if not npc.alive or not npc.present or not npc.patrol_route:
                continue
            route = npc.patrol_route
            if not route:
                continue

            # Don't move if sedated, stunned, or in combat with player
            if npc.has_flag('sedated'):
                continue
            if npc.state.get('stunned_turns', 0) > 0:
                npc.state['stunned_turns'] -= 1
                continue
            # Don't move away from player if hostile (combat lock)
            if npc.hostile and npc.location == player_room:
                continue

            # Move to next position in route
            try:
                current_index = route.index(npc.location)
                next_index = (current_index + 1) % len(route)
            except ValueError:
                next_index = 0
            target_room = route[next_index]
            if target_room != npc.location:
                self.move_npc(npc.id, target_room)

    # ─── World flags ───────────────────────────────────────────────────

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def set_flag(self, flag: str):
        self.flags.add(flag)

    def clear_flag(self, flag: str):
        self.flags.discard(flag)

    def log_event(self, event_description: str):
        """Add to the historical event log."""
        self.event_log.append(event_description)

    # ─── Save/load ─────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize all dynamic world state."""
        return {
            'rooms': {rid: r.to_dict() for rid, r in self.rooms.items()},
            'items': {iid: i.to_dict() for iid, i in self.items.items()},
            'npcs': {nid: n.to_dict() for nid, n in self.npcs.items()},
            'flags': list(self.flags),
            'state': self.state,
            'event_log': self.event_log,
        }

    def from_dict(self, data: dict):
        """Restore from save data (assumes world was already populated)."""
        for rid, rdata in data.get('rooms', {}).items():
            if rid in self.rooms:
                self.rooms[rid].from_dict(rdata)
        for iid, idata in data.get('items', {}).items():
            if iid in self.items:
                self.items[iid].from_dict(idata)
        for nid, ndata in data.get('npcs', {}).items():
            if nid in self.npcs:
                self.npcs[nid].from_dict(ndata)
        self.flags = set(data.get('flags', []))
        self.state = data.get('state', {})
        self.event_log = data.get('event_log', [])
