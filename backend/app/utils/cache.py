import threading
import time
from typing import Any, Optional


class SimpleTTLCache:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            rec = self._data.get(key)
            if not rec:
                return None
            value, expires_at = rec
            if expires_at is not None and time.time() > expires_at:
                del self._data[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds else None
        with self._lock:
            self._data[key] = (value, expires_at)


cache = SimpleTTLCache()
