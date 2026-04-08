"""
Save/load system - persists game state to JSON files.
"""

import os
import json
import time
from typing import Optional


class SaveLoadManager:
    """Handles serialization and restoration of game state."""

    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def save_game(self, game, slot: str = "autosave") -> bool:
        """Save the full game state to a file."""
        try:
            save_data = {
                'version': '1.0.0',
                'timestamp': time.time(),
                'readable_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'player': game.player.to_dict(),
                'world': game.world.to_dict(),
                'events': game.event_manager.to_dict(),
                'turn_count': game.player.turn_count,
                'current_room_name': game.world.get_room(game.player.current_room).name if game.world.get_room(game.player.current_room) else 'Unknown',
            }

            path = os.path.join(self.save_dir, f"{slot}.save.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False

    def load_game(self, game, slot: str = "autosave") -> bool:
        """Load game state from a file."""
        try:
            path = os.path.join(self.save_dir, f"{slot}.save.json")
            if not os.path.exists(path):
                return False

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            game.player.from_dict(data.get('player', {}))
            game.world.from_dict(data.get('world', {}))
            game.event_manager.from_dict(data.get('events', {}))
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False

    def list_saves(self) -> list:
        """Return a list of save slots and their metadata."""
        saves = []
        if not os.path.exists(self.save_dir):
            return saves

        for filename in os.listdir(self.save_dir):
            if filename.endswith('.save.json'):
                slot = filename.replace('.save.json', '')
                path = os.path.join(self.save_dir, filename)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    saves.append({
                        'slot': slot,
                        'timestamp': data.get('readable_time', 'Unknown'),
                        'turn': data.get('turn_count', 0),
                        'location': data.get('current_room_name', 'Unknown'),
                    })
                except Exception:
                    continue
        return sorted(saves, key=lambda s: s.get('timestamp', ''), reverse=True)

    def delete_save(self, slot: str) -> bool:
        path = os.path.join(self.save_dir, f"{slot}.save.json")
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except Exception:
                return False
        return False
