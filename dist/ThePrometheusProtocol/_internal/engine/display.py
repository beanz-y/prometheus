"""
Display module - handles all text output, formatting, colors, and typography.
Supports ANSI color codes for terminals, typewriter effects, and text wrapping.
"""

import os
import sys
import time
import textwrap
import shutil
import threading

# Enable ANSI colors and UTF-8 on Windows
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        # Set console to UTF-8
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:
        pass

# Force stdout to UTF-8 if possible
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except (AttributeError, TypeError):
    pass


class Color:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class Display:
    """Handles all text output with formatting, word wrapping, and effects."""

    def __init__(self, use_color=True, use_typewriter=True, typewriter_speed=0.015):
        self.use_color = use_color
        self.use_typewriter = use_typewriter
        self.typewriter_speed = typewriter_speed
        self.width = self._get_terminal_width()
        # Detect if unicode is supported
        self.use_unicode = self._test_unicode()

    def _test_unicode(self):
        """Test whether the terminal supports unicode output."""
        try:
            test = '─═▓▸•║╔╗╚╝'
            test.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, LookupError):
            return False

    def _safe(self, text):
        """Convert unicode chars to ASCII fallbacks if needed."""
        if self.use_unicode:
            return text
        replacements = {
            '─': '-', '═': '=', '▓': '#', '▸': '>', '•': '*',
            '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
            '┌': '+', '┐': '+', '└': '+', '┘': '+',
            '│': '|', '├': '+', '┤': '+', '┬': '+', '┴': '+',
            '┼': '+', '←': '<-', '→': '->', '↑': '^', '↓': 'v',
            '✓': 'v', '╭': '+', '╮': '+', '╯': '+', '╰': '+',
            '«': '<<', '»': '>>', '…': '...',
        }
        for uni, ascii_char in replacements.items():
            text = text.replace(uni, ascii_char)
        return text

    def _get_terminal_width(self):
        """Get terminal width, defaulting to 80 if detection fails."""
        try:
            return min(shutil.get_terminal_size().columns, 100)
        except Exception:
            return 80

    def _strip_color(self, text):
        """Remove ANSI color codes for width calculation."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)

    def colorize(self, text, color):
        """Wrap text in color codes if colors are enabled."""
        if not self.use_color:
            return text
        return f"{color}{text}{Color.RESET}"

    def wrap_text(self, text, width=None, indent=""):
        """Word-wrap text to fit terminal width, preserving paragraphs."""
        if width is None:
            width = self.width - 2

        # Split into paragraphs, preserving line breaks
        paragraphs = text.split('\n')
        wrapped_paragraphs = []

        for para in paragraphs:
            if not para.strip():
                wrapped_paragraphs.append('')
                continue
            wrapped = textwrap.fill(
                para,
                width=width,
                initial_indent=indent,
                subsequent_indent=indent,
                break_long_words=False,
                replace_whitespace=False
            )
            wrapped_paragraphs.append(wrapped)

        return '\n'.join(wrapped_paragraphs)

    def print(self, text, color=None, wrap=True, typewriter=None, end='\n'):
        """Print text with optional color, wrapping, and typewriter effect."""
        if typewriter is None:
            typewriter = self.use_typewriter

        # Apply ASCII fallback if unicode isn't supported
        text = self._safe(text)

        if wrap:
            text = self.wrap_text(text)

        if color and self.use_color:
            text = f"{color}{text}{Color.RESET}"

        if typewriter:
            self._typewriter_print(text, end=end)
        else:
            try:
                print(text, end=end, flush=True)
            except UnicodeEncodeError:
                # Last-resort encoding fallback
                safe_text = text.encode('ascii', errors='replace').decode('ascii')
                print(safe_text, end=end, flush=True)

    def _typewriter_print(self, text, end='\n'):
        """Print text character by character with skip-on-keypress.

        While animating, pressing ENTER (or any key) instantly renders the
        remaining text. That keypress is consumed so it does NOT carry
        forward to the next input() / pause() call.
        """
        if not text:
            sys.stdout.write(end)
            sys.stdout.flush()
            return

        # Use a flag that the listener thread can set
        skip_event = threading.Event()

        def _listen_for_skip():
            """Background thread: wait for a keypress, then signal skip."""
            try:
                if os.name == 'nt':
                    # Windows: use msvcrt for non-blocking key detection
                    import msvcrt
                    while not skip_event.is_set():
                        if msvcrt.kbhit():
                            msvcrt.getch()  # consume the keypress
                            skip_event.set()
                            return
                        time.sleep(0.02)
                else:
                    # Unix/Mac: read one byte from stdin (blocks until key)
                    import select
                    while not skip_event.is_set():
                        ready, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if ready:
                            sys.stdin.readline()  # consume the line
                            skip_event.set()
                            return
            except Exception:
                pass  # If anything fails, just let animation play normally

        # Start the listener thread
        listener = threading.Thread(target=_listen_for_skip, daemon=True)
        listener.start()

        try:
            for i, char in enumerate(text):
                if skip_event.is_set():
                    # Player pressed a key - dump the rest instantly
                    sys.stdout.write(text[i:])
                    sys.stdout.flush()
                    break
                sys.stdout.write(char)
                sys.stdout.flush()
                if char not in ' \n\t':
                    time.sleep(self.typewriter_speed)
                elif char == '\n':
                    time.sleep(self.typewriter_speed * 3)
        except KeyboardInterrupt:
            # Ctrl+C also skips (dump remaining text, don't disable permanently)
            remaining = text[text.index(char):] if char in text else ''
            sys.stdout.write(remaining)
            sys.stdout.flush()

        sys.stdout.write(end)
        sys.stdout.flush()

        # Signal the listener to stop (in case animation finished naturally)
        skip_event.set()
        # Give the thread a moment to clean up
        listener.join(timeout=0.1)

        # Flush any remaining buffered input so it doesn't bleed into
        # the next input()/pause() call
        self._flush_stdin()

    def _flush_stdin(self):
        """Flush any buffered stdin so queued keypresses don't bleed through."""
        try:
            if os.name == 'nt':
                import msvcrt
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                import select
                while select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.readline()
        except Exception:
            pass

    def narrate(self, text):
        """Print narrative text in default style."""
        self.print(text, color=Color.WHITE)

    def describe(self, text):
        """Print room/object descriptions."""
        self.print(text, color=Color.BRIGHT_WHITE)

    def dialogue(self, speaker, text):
        """Print character dialogue."""
        if self.use_color:
            header = f"{Color.BRIGHT_CYAN}{speaker}{Color.RESET}"
        else:
            header = speaker
        print(header)
        self.print(f'  "{text}"', color=Color.CYAN, typewriter=self.use_typewriter)

    def system(self, text):
        """Print system messages (ship computer, alerts)."""
        self.print(f"[SYSTEM] {text}", color=Color.BRIGHT_GREEN)

    def warning(self, text):
        """Print warning messages."""
        self.print(f"!!! {text} !!!", color=Color.BRIGHT_YELLOW)

    def error(self, text):
        """Print error messages (for game errors, not parser errors)."""
        self.print(text, color=Color.RED)

    def critical(self, text):
        """Print critical alerts."""
        self.print(f"*** {text} ***", color=Color.BRIGHT_RED)

    def success(self, text):
        """Print success messages."""
        self.print(text, color=Color.BRIGHT_GREEN)

    def hint(self, text):
        """Print hints and subtle suggestions."""
        self.print(text, color=Color.BRIGHT_BLACK)

    def location(self, name):
        """Print location name header."""
        sep_char = '─' if self.use_unicode else '-'
        if self.use_color:
            separator = f"{Color.BRIGHT_BLUE}{sep_char * min(len(name) + 4, self.width)}{Color.RESET}"
            header = f"{Color.BOLD}{Color.BRIGHT_BLUE}{name.upper()}{Color.RESET}"
        else:
            separator = sep_char * (len(name) + 4)
            header = name.upper()
        try:
            print()
            print(header)
            print(separator)
        except UnicodeEncodeError:
            print()
            print(name.upper().encode('ascii', 'replace').decode('ascii'))
            print('-' * (len(name) + 4))

    def title_screen(self, lines):
        """Print ASCII art title with color."""
        for line in lines:
            if self.use_color:
                print(f"{Color.BRIGHT_CYAN}{line}{Color.RESET}")
            else:
                print(line)

    def prompt(self, text="> "):
        """Display the input prompt. Flushes buffered input first."""
        self._flush_stdin()
        if self.use_color:
            return input(f"{Color.BRIGHT_GREEN}{text}{Color.RESET}")
        return input(text)

    def separator(self, char='─', color=None):
        """Print a horizontal separator."""
        if not self.use_unicode and ord(char) > 127:
            char = '-'
        line = char * self.width
        try:
            if color and self.use_color:
                print(f"{color}{line}{Color.RESET}")
            else:
                print(line)
        except UnicodeEncodeError:
            print('-' * self.width)

    def pause(self, text="[Press ENTER to continue]"):
        """Pause execution and wait for user input. Flushes buffered input first."""
        self.hint(text)
        self._flush_stdin()
        input()

    def clear(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def log_entry(self, author, date, title, content):
        """Format a log/journal entry."""
        self.separator('═', Color.BRIGHT_YELLOW)
        if self.use_color:
            print(f"{Color.BRIGHT_YELLOW}LOG ENTRY - {date}{Color.RESET}")
            print(f"{Color.YELLOW}AUTHOR: {author}{Color.RESET}")
            print(f"{Color.YELLOW}SUBJECT: {title}{Color.RESET}")
        else:
            print(f"LOG ENTRY - {date}")
            print(f"AUTHOR: {author}")
            print(f"SUBJECT: {title}")
        self.separator('─', Color.BRIGHT_YELLOW)
        self.print(content, color=Color.YELLOW, typewriter=False)
        self.separator('═', Color.BRIGHT_YELLOW)

    def ship_alert(self, message):
        """Emergency ship-wide alert styling."""
        self.separator('▓', Color.BRIGHT_RED)
        if self.use_color:
            header = " PROMETHEUS-WIDE ALERT ".center(self.width)
            print(f"{Color.BG_RED}{Color.BRIGHT_WHITE}{Color.BOLD}{header}{Color.RESET}")
        else:
            print(" PROMETHEUS-WIDE ALERT ".center(self.width, '='))
        self.print(message, color=Color.BRIGHT_RED, typewriter=False)
        self.separator('▓', Color.BRIGHT_RED)
