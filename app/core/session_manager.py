"""
مدیریت Session تماس‌ها
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class CallSession:
    """یک Session تماس"""
    session_id: str
    caller_phone: str
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: datetime | None = None
    status: str = "active"  # active | ended | failed

    # Context مکالمه
    conversation: list[dict] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, text: str):
        """افزودن پیام به مکالمه"""
        self.conversation.append({
            "role": role,  # user | bot | system
            "text": text,
            "timestamp": datetime.now().isoformat(),
        })

    def end(self):
        """پایان تماس"""
        self.ended_at = datetime.now()
        self.status = "ended"

    @property
    def duration(self) -> float:
        """مدت تماس به ثانیه"""
        end = self.ended_at or datetime.now()
        return (end - self.started_at).total_seconds()


class SessionManager:
    """مدیریت همه Session ها"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._sessions: dict[str, CallSession] = {}
        self._initialized = True

    def create_session(self, caller_phone: str) -> CallSession:
        """ساخت Session جدید"""
        session_id = str(uuid.uuid4())
        session = CallSession(
            session_id=session_id,
            caller_phone=caller_phone,
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> CallSession | None:
        return self._sessions.get(session_id)

    def end_session(self, session_id: str) -> CallSession | None:
        session = self._sessions.get(session_id)
        if session:
            session.end()
        return session

    def get_active_sessions(self) -> list[CallSession]:
        return [s for s in self._sessions.values() if s.status == "active"]

    def remove_session(self, session_id: str):
        self._sessions.pop(session_id, None)