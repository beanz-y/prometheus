"""
Companion system - manages an NPC companion that follows the player.

Tracks trust, provides contextual commentary, and influences story outcomes.
"""

from typing import Optional, Dict


class Companion:
    """Represents an NPC companion that can follow the player."""

    def __init__(self):
        self.npc_id: str = ""           # NPC this companion represents
        self.trust: int = 0             # 0-100
        self.following: bool = False     # Currently following player
        self.commentary: Dict[str, str] = {}  # room_id/item_id -> comment text
        self.last_comment_turn: int = 0  # Prevent spam

    def adjust_trust(self, amount: int, display=None):
        """Adjust trust level, optionally showing a message."""
        old = self.trust
        self.trust = max(0, min(100, self.trust + amount))
        if display and self.trust != old:
            if amount > 0:
                display.hint("(Yuki's trust in you has increased.)")
            elif amount < 0:
                display.hint("(Yuki's trust in you has decreased.)")

    def get_trust_level(self) -> str:
        """Return a descriptive trust level string."""
        if self.trust < 25:
            return "hostile"
        if self.trust < 50:
            return "cautious"
        if self.trust < 75:
            return "cooperative"
        if self.trust < 100:
            return "ally"
        return "bonded"

    def get_commentary(self, room_id: str, game) -> Optional[str]:
        """Return contextual comment for current room, if any."""
        if not self.following:
            return None
        if game.player.turn_count - self.last_comment_turn < 3:
            return None  # Don't comment every turn
        comment = self.commentary.get(room_id)
        if comment:
            self.last_comment_turn = game.player.turn_count
        return comment

    def to_dict(self) -> dict:
        """Serialize companion state for save games."""
        return {
            'npc_id': self.npc_id,
            'trust': self.trust,
            'following': self.following,
            'last_comment_turn': self.last_comment_turn,
        }

    def from_dict(self, data: dict):
        """Restore companion state from save game."""
        self.npc_id = data.get('npc_id', '')
        self.trust = data.get('trust', 0)
        self.following = data.get('following', False)
        self.last_comment_turn = data.get('last_comment_turn', 0)
