# SessionTokenSandbox/session_token.py

from dataclasses import dataclass, field
import yaml, uuid
from typing import Dict, Optional, List
import datetime


@dataclass
class SessionToken:
    """Represents a bounded, ritualized session."""
    session_id: uuid
    parent_session_id: Optional[str] = None  # Simple reference only
    child_session_ids: List[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    initator: str
    name: str
    intent: str  # e.g., "light candle"
    energy_cost: int  # Units of "banana fuel" <-# required tools?
    boundaries: Dict[str, bool] = None  # e.g., {"inbox_pause": True}
    duration_minutes: int = 90

    def __post_init__(self):
        """Initialize lists if not provided."""
        if self.child_tokens is None:
            self.child_tokens = []

    def to_yaml(self) -> str:
        """Serialize the token to YAML."""
        # Convert dataclass to dictionary for serialization
        token_dict = self.__dict__.copy()
        # Handle serialization of dataclasses in lists (if needed)
        return yaml.dump(token_dict)
    
    @classmethod
    def from_yaml(cls, yaml_str: str):
        """Deserialize the token from YAML."""
        data = yaml.safe_load(yaml_str)
        return cls(**data)
    
    def add_child(self, child_id: str):
        self.child_session_ids.append(child_id)

    def remove_child(self, child_id: str):
        self.child_session_ids.remove(child_id)