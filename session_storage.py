# SessionTokenSandbox/session_storage.py

from pathlib import Path
import yaml

from session_token import SessionToken

class SessionStorage:
    def __init__(self, storage_dir="sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def save_token(self, token: SessionToken, filename: str):
        with open(self.storage_dir / f"{filename}.yaml", 'w') as f:
            yaml.dump(token, f)

    def load_token(self, filename: str) -> SessionToken:
        with open(self.storage_dir / f"{filename}.yaml", 'r') as f:
            return SessionToken(**yaml.safe_load(f))