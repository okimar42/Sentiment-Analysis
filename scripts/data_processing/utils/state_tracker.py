from __future__ import annotations

import json
from pathlib import Path
from typing import Set, Dict, Any


class StateTracker:
    """Track processed IDs to enable incremental processing."""

    def __init__(self, state_dir: str | Path = "./.state"):
        self.path = Path(state_dir)
        self.path.mkdir(parents=True, exist_ok=True)

    def _file_for(self, key: str) -> Path:
        safe = key.replace("/", "_")
        return self.path / f"{safe}.json"

    def load_ids(self, key: str) -> Set[str]:
        file = self._file_for(key)
        if file.exists():
            with file.open("r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def save_ids(self, key: str, ids: Set[str]) -> None:
        file = self._file_for(key)
        with file.open("w", encoding="utf-8") as f:
            json.dump(sorted(ids), f, indent=2)

    # Convenience helpers ------------------------------------------------

    def filter_new(self, key: str, items: list[Dict[str, Any]], id_field: str = "post_id") -> list[Dict[str, Any]]:
        """Return only items whose id_field is not yet stored under *key*."""
        seen = self.load_ids(key)
        new_items = [itm for itm in items if str(itm.get(id_field)) not in seen]
        # Update state with new IDs
        seen.update(str(itm[id_field]) for itm in new_items if id_field in itm)
        self.save_ids(key, seen)
        return new_items