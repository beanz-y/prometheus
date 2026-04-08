"""
Command parser - translates natural language input into structured commands.

Supports:
- Simple commands: "look", "inventory", "north"
- Object commands: "take key", "examine terminal"
- Preposition commands: "put key in lock", "type 4815 into keypad"
- Compound commands: "take key and unlock door"
- Sequential commands: "go north then take card"
- Simultaneous commands: "shoot target while running to cover"
- Quoted strings: 'type "override alpha" into console'
- Pronouns: "look at it", "take them"
"""

import re
import shlex
from dataclasses import dataclass, field
from typing import List, Optional


# Direction synonyms
DIRECTIONS = {
    'n': 'north', 'north': 'north',
    's': 'south', 'south': 'south',
    'e': 'east', 'east': 'east',
    'w': 'west', 'west': 'west',
    'ne': 'northeast', 'northeast': 'northeast',
    'nw': 'northwest', 'northwest': 'northwest',
    'se': 'southeast', 'southeast': 'southeast',
    'sw': 'southwest', 'southwest': 'southwest',
    'u': 'up', 'up': 'up',
    'd': 'down', 'down': 'down',
    'in': 'in', 'inside': 'in', 'enter': 'in',
    'out': 'out', 'outside': 'out', 'exit': 'out',
    'forward': 'forward', 'fore': 'forward',
    'aft': 'aft', 'back': 'aft',
    'port': 'port', 'starboard': 'starboard',
}

# Verb synonyms - maps user input to canonical verbs
VERB_SYNONYMS = {
    # Movement
    'go': 'go', 'move': 'go', 'walk': 'go', 'run': 'go', 'travel': 'go',
    'head': 'go', 'proceed': 'go',

    # Observation
    'look': 'look', 'l': 'look', 'observe': 'look', 'survey': 'look',
    'examine': 'examine', 'x': 'examine', 'inspect': 'examine',
    'check': 'examine', 'study': 'examine', 'analyze': 'examine',
    'search': 'search', 'rummage': 'search',
    'read': 'read', 'peruse': 'read',

    # Inventory management
    'take': 'take', 'get': 'take', 'grab': 'take', 'pick': 'take',
    'obtain': 'take', 'acquire': 'take', 'snag': 'take',
    'drop': 'drop', 'discard': 'drop', 'leave': 'drop', 'release': 'drop',
    'inventory': 'inventory', 'i': 'inventory', 'inv': 'inventory',
    'items': 'inventory', 'carrying': 'inventory',

    # Interaction
    'use': 'use', 'activate': 'use', 'operate': 'use',
    'open': 'open', 'unlock': 'unlock', 'unseal': 'open',
    'close': 'close', 'shut': 'close', 'seal': 'close',
    'lock': 'lock',
    'push': 'push', 'press': 'push',
    'pull': 'pull', 'yank': 'pull',
    'turn': 'turn', 'rotate': 'turn', 'twist': 'turn',
    'type': 'type', 'input': 'type', 'enter': 'type', 'key': 'type',
    'insert': 'insert', 'slot': 'insert',
    'remove': 'remove', 'extract': 'remove', 'eject': 'remove',
    'attach': 'attach', 'connect': 'attach', 'plug': 'attach',
    'detach': 'detach', 'unplug': 'detach', 'disconnect': 'detach',
    'combine': 'combine', 'join': 'combine',

    # Combat/physical
    'attack': 'attack', 'hit': 'attack', 'strike': 'attack', 'fight': 'attack',
    'punch': 'attack', 'kick': 'attack', 'stab': 'attack', 'slash': 'attack',
    'shoot': 'shoot', 'fire': 'shoot',
    'throw': 'throw', 'toss': 'throw', 'hurl': 'throw',
    'kill': 'attack',
    'break': 'break', 'smash': 'break', 'destroy': 'break',

    # Social/dialogue
    'talk': 'talk', 'speak': 'talk', 'ask': 'ask', 'tell': 'tell',
    'say': 'say', 'shout': 'say', 'yell': 'say', 'whisper': 'say',
    'greet': 'talk',
    'answer': 'answer', 'respond': 'answer',

    # Meta
    'save': 'save', 'load': 'load', 'quit': 'quit', 'exit': 'quit',
    'help': 'help', '?': 'help', 'commands': 'help',
    'wait': 'wait', 'z': 'wait', 'rest': 'wait',
    'sleep': 'sleep',
    'hint': 'hint', 'hints': 'hint',
    'map': 'map',
    'status': 'status', 'stat': 'status', 'stats': 'status', 'condition': 'status',
    'objectives': 'objectives', 'objective': 'objectives', 'goals': 'objectives',
    'goal': 'objectives', 'quest': 'objectives', 'task': 'objectives',
    'tasks': 'objectives',
    'location': 'location', 'where': 'location', 'whereami': 'location',
    'place': 'location',
    'think': 'think', 'recall': 'think', 'remember': 'think',

    # Special
    'climb': 'climb', 'jump': 'jump', 'crawl': 'crawl',
    'hide': 'hide', 'sneak': 'sneak',
    'listen': 'listen', 'hear': 'listen',
    'smell': 'smell', 'sniff': 'smell',
    'touch': 'touch', 'feel': 'touch',
    'taste': 'taste',
    'drink': 'drink', 'sip': 'drink',
    'eat': 'eat', 'consume': 'eat',
    'wear': 'wear', 'equip': 'wear', 'don': 'wear',
    'remove': 'remove', 'unequip': 'remove', 'doff': 'remove',
    'give': 'give', 'offer': 'give', 'hand': 'give',
    'show': 'show', 'display': 'show',
}

# Articles and fillers to strip
ARTICLES = {'the', 'a', 'an', 'some', 'that', 'this', 'these', 'those'}
FILLERS = {'please', 'kindly'}

# Prepositions
PREPOSITIONS = {
    'in', 'into', 'inside', 'within',
    'on', 'onto', 'upon', 'over',
    'at', 'to', 'toward', 'towards',
    'with', 'using', 'via',
    'from', 'off',
    'under', 'beneath', 'below',
    'about', 'regarding',
    'against',
    'behind', 'beside', 'near',
    'through', 'across',
    'for',
}

# Conjunctions for compound commands
AND_CONJUNCTIONS = {'and', ',', '&', 'also', 'plus'}
THEN_CONJUNCTIONS = {'then', 'after', 'afterward', 'afterwards', 'next', ';'}
WHILE_CONJUNCTIONS = {'while', 'whilst', 'as', 'during'}


@dataclass
class Command:
    """A parsed command ready for execution."""
    verb: str = ""
    direct_object: Optional[str] = None    # The thing being acted on
    indirect_object: Optional[str] = None  # The target/recipient
    preposition: Optional[str] = None      # How it relates (in/on/with/etc.)
    modifier: Optional[str] = None         # Text content (for "type X into Y")
    raw_text: str = ""                     # Original input segment
    error: Optional[str] = None            # Parse error message

    def __str__(self):
        parts = [self.verb]
        if self.modifier:
            parts.append(f'"{self.modifier}"')
        if self.direct_object:
            parts.append(self.direct_object)
        if self.preposition:
            parts.append(self.preposition)
        if self.indirect_object:
            parts.append(self.indirect_object)
        return ' '.join(parts)


@dataclass
class CommandSequence:
    """A sequence of commands from a single input, with execution mode."""
    commands: List[Command] = field(default_factory=list)
    simultaneous: bool = False  # True if "while" was used
    sequential: bool = True     # True if "then" was used (default)

    def __iter__(self):
        return iter(self.commands)

    def __len__(self):
        return len(self.commands)

    def __bool__(self):
        return bool(self.commands)


class Parser:
    """Parses raw input into structured Command objects."""

    def __init__(self):
        self.last_object = None  # For pronoun resolution ("take it")
        self.last_verb = None

    def parse(self, raw_input: str) -> CommandSequence:
        """Parse raw user input into a CommandSequence."""
        if not raw_input or not raw_input.strip():
            return CommandSequence()

        text = raw_input.strip()

        # Extract quoted strings to preserve them as single tokens
        text, quotes = self._extract_quotes(text)

        # Split into segments based on conjunctions
        segments, sim_flag = self._split_compound(text)

        sequence = CommandSequence(simultaneous=sim_flag)

        for segment in segments:
            # Restore quotes in segments
            segment = self._restore_quotes(segment, quotes)
            cmd = self._parse_segment(segment)
            if cmd:
                sequence.commands.append(cmd)

        return sequence

    def _extract_quotes(self, text):
        """Replace quoted strings with placeholders and return them separately."""
        quotes = {}
        counter = [0]

        def replace(match):
            key = f"__QUOTE{counter[0]}__"
            quotes[key] = match.group(1)
            counter[0] += 1
            return key

        # Handle both single and double quotes
        text = re.sub(r'"([^"]*)"', replace, text)
        text = re.sub(r"'([^']*)'", replace, text)
        return text, quotes

    def _restore_quotes(self, text, quotes):
        """Restore quoted strings from placeholders."""
        for key, value in quotes.items():
            text = text.replace(key, f'"{value}"')
        return text

    def _split_compound(self, text):
        """Split compound commands on conjunctions.

        Returns (list_of_segments, simultaneous_flag).
        """
        # Lowercase for matching but preserve for content
        lower_text = text.lower()

        # Check for 'while' indicating simultaneous actions
        simultaneous = False
        for conj in WHILE_CONJUNCTIONS:
            if f' {conj} ' in f' {lower_text} ':
                simultaneous = True
                break

        # Build regex for all conjunctions
        all_conjunctions = AND_CONJUNCTIONS | THEN_CONJUNCTIONS | WHILE_CONJUNCTIONS
        # Escape and sort by length (longer first) to match multi-char first
        sorted_conj = sorted(all_conjunctions, key=len, reverse=True)
        pattern_parts = []
        for conj in sorted_conj:
            if conj in (',', ';', '&'):
                pattern_parts.append(re.escape(conj))
            else:
                pattern_parts.append(r'\b' + re.escape(conj) + r'\b')
        pattern = r'\s*(?:' + '|'.join(pattern_parts) + r')\s*'

        segments = re.split(pattern, text, flags=re.IGNORECASE)
        segments = [s.strip() for s in segments if s and s.strip()]

        return segments, simultaneous

    def _parse_segment(self, segment: str) -> Optional[Command]:
        """Parse a single command segment into a Command object."""
        if not segment:
            return None

        # Preserve the original
        original = segment

        # Extract quoted content first for use as modifier
        quoted_content = None
        quote_match = re.search(r'"([^"]*)"', segment)
        if quote_match:
            quoted_content = quote_match.group(1)
            segment = segment.replace(quote_match.group(0), '__QUOTED__')

        # Tokenize
        tokens = segment.lower().split()

        # Remove fillers
        tokens = [t for t in tokens if t not in FILLERS]

        if not tokens:
            return None

        # Check for direction-only commands (e.g., "north", "n")
        if len(tokens) == 1 and tokens[0] in DIRECTIONS:
            return Command(
                verb='go',
                direct_object=DIRECTIONS[tokens[0]],
                raw_text=original
            )

        # Check for "go <direction>" pattern
        if len(tokens) == 2 and tokens[0] in ('go', 'move', 'walk', 'run', 'head'):
            if tokens[1] in DIRECTIONS:
                return Command(
                    verb='go',
                    direct_object=DIRECTIONS[tokens[1]],
                    raw_text=original
                )

        # Extract verb (first token)
        verb_raw = tokens[0]
        verb = VERB_SYNONYMS.get(verb_raw, verb_raw)

        # Handle "pick up" as take
        if verb == 'take' and len(tokens) > 1 and tokens[1] == 'up':
            tokens.pop(1)

        # Handle "look at X" -> examine X
        if verb == 'look' and len(tokens) > 1:
            if tokens[1] in ('at', 'into', 'inside', 'in', 'through', 'through'):
                verb = 'examine'
                tokens.pop(1)
            elif tokens[1] in ('around', 'here'):
                tokens.pop(1)
                verb = 'look'

        # Handle "talk to X", "speak with X"
        if verb == 'talk' and len(tokens) > 1:
            if tokens[1] in ('to', 'with'):
                tokens.pop(1)

        # Remove verb token
        tokens = tokens[1:]

        # Strip articles
        tokens = [t for t in tokens if t not in ARTICLES]

        if not tokens:
            return Command(verb=verb, raw_text=original)

        # Find preposition to split direct/indirect object
        prep_index = -1
        prep_word = None
        for i, token in enumerate(tokens):
            if token in PREPOSITIONS:
                prep_index = i
                prep_word = token
                break

        if prep_index >= 0:
            direct_tokens = tokens[:prep_index]
            indirect_tokens = tokens[prep_index + 1:]
            direct = ' '.join(direct_tokens) if direct_tokens else None
            indirect = ' '.join(indirect_tokens) if indirect_tokens else None
        else:
            direct = ' '.join(tokens)
            indirect = None
            prep_word = None

        # Handle quoted content as modifier (e.g., type "override" into console)
        modifier = None
        if quoted_content is not None:
            modifier = quoted_content
            if direct and '__quoted__' in direct:
                direct = direct.replace('__quoted__', '').strip() or None
            if indirect and '__quoted__' in indirect:
                indirect = indirect.replace('__quoted__', '').strip() or None

        # Special handling for "type" - the direct object is the text typed
        if verb == 'type' and not modifier:
            # "type 1234 into keypad" -> modifier="1234", indirect="keypad"
            if direct and indirect:
                modifier = direct
                direct = None
            elif direct and not indirect:
                # "type 1234" - incomplete, but preserve
                modifier = direct
                direct = None

        # Handle pronoun resolution
        if direct in ('it', 'them', 'him', 'her', 'that', 'this'):
            if self.last_object:
                direct = self.last_object

        # Update context for pronoun resolution
        if direct and direct not in ('it', 'them'):
            self.last_object = direct
        self.last_verb = verb

        return Command(
            verb=verb,
            direct_object=direct,
            indirect_object=indirect,
            preposition=prep_word,
            modifier=modifier,
            raw_text=original
        )

    def normalize_object(self, obj_str: str) -> str:
        """Normalize an object string for matching (strip articles, lowercase)."""
        if not obj_str:
            return ""
        tokens = obj_str.lower().split()
        tokens = [t for t in tokens if t not in ARTICLES]
        return ' '.join(tokens).strip()
