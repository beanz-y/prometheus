"""
Dialogue system - manages conversations with NPCs.

Supports:
- Dialogue trees with branching paths
- Topics that unlock based on player knowledge/flags
- State-dependent responses
- Multi-turn conversations
- Side effects (giving items, setting flags, learning knowledge)
"""

from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field


@dataclass
class DialogueLine:
    """A single line of dialogue with optional conditions and effects."""
    speaker: str            # "player" or NPC name
    text: str

    # Conditions to show this line
    required_flags: List[str] = field(default_factory=list)
    forbidden_flags: List[str] = field(default_factory=list)
    required_knowledge: List[str] = field(default_factory=list)

    # Effects
    set_flags: List[str] = field(default_factory=list)
    give_knowledge: List[str] = field(default_factory=list)
    give_items: List[str] = field(default_factory=list)
    unlock_topics: List[str] = field(default_factory=list)


@dataclass
class DialogueTopic:
    """A conversation topic the player can ask about."""
    id: str
    keyword: str                        # What the player says/asks
    aliases: List[str] = field(default_factory=list)
    lines: List[DialogueLine] = field(default_factory=list)

    # Availability
    requires_knowledge: List[str] = field(default_factory=list)
    requires_flags: List[str] = field(default_factory=list)
    forbidden_flags: List[str] = field(default_factory=list)
    hidden: bool = False                # Must be unlocked

    # After-effects
    set_flags: List[str] = field(default_factory=list)
    give_knowledge: List[str] = field(default_factory=list)
    unlock_topics: List[str] = field(default_factory=list)
    lock_topic: bool = False            # Topic can only be discussed once
    discussed: bool = False

    def is_available(self, player) -> bool:
        """Check if this topic can be discussed right now."""
        if self.hidden:
            return False
        if self.lock_topic and self.discussed:
            return False
        for knowledge in self.requires_knowledge:
            if not player.knows(knowledge):
                return False
        for flag in self.requires_flags:
            if not player.has_flag(flag):
                return False
        for flag in self.forbidden_flags:
            if player.has_flag(flag):
                return False
        return True


@dataclass
class DialogueTree:
    """A full conversation tree for an NPC."""
    id: str
    greeting: str = ""                  # Opening text
    default_response: str = "They don't respond to that."
    topics: Dict[str, DialogueTopic] = field(default_factory=dict)

    def add_topic(self, topic: DialogueTopic):
        self.topics[topic.id] = topic

    def find_topic(self, keyword: str, player) -> Optional[DialogueTopic]:
        """Find an available topic matching a keyword."""
        keyword = keyword.lower().strip()
        for topic in self.topics.values():
            if not topic.is_available(player):
                continue
            if keyword == topic.keyword.lower() or keyword == topic.id.lower():
                return topic
            if keyword in topic.keyword.lower():
                return topic
            for alias in topic.aliases:
                if keyword == alias.lower() or keyword in alias.lower():
                    return topic
        return None

    def get_available_topics(self, player) -> List[DialogueTopic]:
        """Return list of currently available topics."""
        return [t for t in self.topics.values() if t.is_available(player)]


class DialogueManager:
    """Manages all dialogue trees and conversations."""

    def __init__(self):
        self.trees: Dict[str, DialogueTree] = {}
        self.active_conversation: Optional[str] = None  # NPC ID currently talking to

    def add_tree(self, tree: DialogueTree):
        self.trees[tree.id] = tree

    def get_tree(self, tree_id: str) -> Optional[DialogueTree]:
        return self.trees.get(tree_id)

    def talk_to(self, npc, player, display):
        """Initiate or continue conversation with an NPC."""
        if not npc.dialogue_tree:
            display.print(npc.default_response or "They have nothing to say.")
            return

        tree = self.get_tree(npc.dialogue_tree)
        if not tree:
            display.print("They have nothing to say.")
            return

        self.active_conversation = npc.id

        # Greeting
        if npc.id not in player.flags and tree.greeting:
            if npc.greeting:
                display.dialogue(npc.name, npc.greeting)
            else:
                display.dialogue(npc.name, tree.greeting)
            player.add_flag(f"met_{npc.id}")

        # Show available topics
        topics = tree.get_available_topics(player)
        if not topics:
            display.print(f"{npc.name} has nothing more to say right now.")
            return

        display.print("")
        display.print("You can ask about:")
        for i, topic in enumerate(topics, 1):
            marker = " (new)" if not topic.discussed else ""
            display.print(f"  {i}. {topic.keyword}{marker}")
        display.print("  (Type 'ask <topic>' or number, or 'end' to stop talking)")

    def ask_about(self, npc, topic_keyword: str, game):
        """Ask an NPC about a specific topic."""
        if not npc.dialogue_tree:
            game.display.print(f"{npc.name} doesn't respond.")
            return

        tree = self.get_tree(npc.dialogue_tree)
        if not tree:
            return

        topic = tree.find_topic(topic_keyword, game.player)
        if not topic:
            game.display.print(f"{npc.name} doesn't know anything about that.")
            return

        # Play out dialogue lines
        for line in topic.lines:
            # Check line conditions
            skip = False
            for flag in line.required_flags:
                if not game.player.has_flag(flag):
                    skip = True
                    break
            for flag in line.forbidden_flags:
                if game.player.has_flag(flag):
                    skip = True
                    break
            for knowledge in line.required_knowledge:
                if not game.player.knows(knowledge):
                    skip = True
                    break
            if skip:
                continue

            if line.speaker.lower() == "player":
                game.display.dialogue(game.player.name, line.text)
            else:
                game.display.dialogue(npc.name, line.text)

            # Apply line effects
            for flag in line.set_flags:
                game.player.add_flag(flag)
            for knowledge in line.give_knowledge:
                game.player.add_knowledge(knowledge)
            for item_id in line.give_items:
                game.player.add_item(item_id)
                item = game.world.get_item(item_id)
                if item:
                    game.display.success(f"{npc.name} gives you the {item.name}.")
            for topic_id in line.unlock_topics:
                if topic_id in tree.topics:
                    tree.topics[topic_id].hidden = False

        # Apply topic effects
        for flag in topic.set_flags:
            game.player.add_flag(flag)
        for knowledge in topic.give_knowledge:
            game.player.add_knowledge(knowledge)
        for topic_id in topic.unlock_topics:
            if topic_id in tree.topics:
                tree.topics[topic_id].hidden = False

        topic.discussed = True
