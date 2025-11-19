from typing import Dict


class Watchdog:

    def bark_alert(self, violation):
        log_to_ledger(violation)
        trigger_pause()  # Or escalate to Shepherd

    def check_boundaries(self, current_state: Dict[str, bool]) -> bool:
        """Check if current state complies with token boundaries."""
        for boundary, required in self.boundaries.items():
            if required and not current_state.get(boundary, False):
                return False
        return True

    def request_permission(self, parent_token, new_boundary):
        if self._is_expansion(new_boundary, parent_token.boundaries):
            return self._renegotiate(parent_token, new_boundary)
        return False  # Only expansions require handshake

    def check_duration_boundary(self, current_duration: int) -> bool:
        """Check if session duration boundaries are respected"""
        return current_duration <= self.duration_minutes

    def verify_expansion(self, proposed):
       if not self._is_expansion(proposed, self.boundaries):
           raise ValueError("Expansion would violate parent boundaries")
       return True
    
class Sheepdog:

    def herding():
        if command == "open_gate":
            self.adjust_boundaries(new_field_bounds)
            log_to_ledger("Shepherd-directed expansion")