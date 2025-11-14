# SessionTokenSandbox/session_manager.py

import datetime

from session_token import SessionToken

class SessionManager:
    def __init__(self):
        self.active_tokens = []
        self.paused_tokens = []
        self.completed_tokens = []

    def create_new_session(self, token: SessionToken):
        token.start_time = datetime.now()
        self.active_tokens.append(token)
        return token

    def end_session(self, token: SessionToken):
        token.end_time = datetime.now()
        self.active_tokens.remove(token)
        self.completed_tokens.append(token)
        return token