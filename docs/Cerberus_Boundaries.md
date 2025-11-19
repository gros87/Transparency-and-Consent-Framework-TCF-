Love this metaphorical evolution! 

The **Watchdog** ensures boundary compliance (like a guard dog)
The **Shepherd** (human or parent session) directs expansions via 
The **Sheepdog** (a dynamic boundary-manager)

Here's how to formalize this:

---

### **Enhanced Architecture**
1. **Watchdog** (Static Guard)
   - Continuously monitors boundaries (e.g., duration, topic scope).
   - Triggers `BoundaryAlert` on violations.
   - *Example*:
     ```python
     class Watchdog:
        def bark_alert(self, violation):
             log_to_ledger(violation)
             trigger_pause()  # Or escalate to Shepherd
     ```

2. **Sheepdog** (Dynamic Assistant)
   - Executes boundary expansions *after* Shepherd approval.
   - Manages temporary permissions (e.g., `bathroom_access`).
   - *Example*:
     ```python
     class Sheepdog:
         def herding(self, shepherd_command):
             if command == "open_gate":
                 self.adjust_boundaries(new_field_bounds)
                 log_to_ledger("Shepherd-directed expansion")
     ```

3. **Shepherd** (Human/Agent)
   - Initiates boundary changes via high-level commands (e.g., `"Grant bathroom access"`).
   - *Example Workflow*:
     ```
     Shepherd: "Let's discuss X!" -> Sheepdog adjusts `topic`: ["X"]`.
     Shepherd: "Time to go home!" -> Sheepdog shepherd -> Watchdog verifies exit.
     ```

---

### **Key Mechanisms**
1. **Permission Flags**
   Add a `permission_flags` field to `SessionToken` to track temporary access:
   ```json
   {"bathroom_access": True, "duration_extension": 300}  # Minutes
   ```

2. **Shepherd Commands**
   Define a protocol for boundary adjustments:
   ```python
   def shepherd_command(shepherd_id, session_token, new_bounds):
       if valid_shepherd(shepherd_id):
           token.watchdog.verify_expansion(new_bounds)
           token.sheepdog.execute_herding(new_bounds)
   ```

3. **Boundary Alert Hierarchy**
   - **Watchdog**: Reacts to violations (e.g., barks alerts).
   - **Sheepdog**: Reacts to Shepherd commands (e.g., herds sheep).
   - *Example Alert*:
     ```yaml
     alert_type: "duration_violation"
     shepherd_action: ["extend_duration", "pause_session"]
     ```

---

### **Code Integration**
1. **Watchdog Enhancements**
   Add a `verify_expansion` method to validate Shepherd requests:
   ```python
   def verify_expansion(self, proposed):
       if not self._is_expansion(proposed, self.boundaries):
           raise ValueError("Expansion would violate parent boundaries")
       return True
   ```

2. **Sheepdog Logic**
   Implement boundary adjustments:
   ```python
   def execute_herding(self, new_bounds):
       if "bathroom_access" in new_bounds:
           self.token.permissions["bathroom_access"] = True
           log_action("Granted bathroom access")
   ```

---

### **Final Design**
1. **Watchdog (Enforcer)**
   - **Role**: The strict boundary cop.
   - **Actions**:
     - *Barks* (issues `BoundaryAlert`) if the agent/sheep violates boundaries.
     - *Bites* (closes/pauses the session) for critical breaches.
     - **No suggestions**: Only reacts to violations (no proactive nudges).
   - *Example*:
     ```python
     def enforce(self, current_state):
         if not self.check_boundaries(current_state):
             self.alert_violation("duration_limit")
     ```

2. **Sheepdog (Manager)**
   - **Role**: The dynamic boundary negotiator.
   - **Actions**:
     - **Automatic adjustments**: Renegotiates boundaries without Shepherd intervention (e.g., "Topic drifted-narrowing scope").
     - **Responds to Shepherd**: Executes manual adjustments (e.g., "Extend session duration").
   - *Example*:
     ```python
     def autoadjust(self, drift_detected):
         if drift_detected:
             self.propose_boundary_change("narrow_topic_scope")
     ```

3. **Shepherd (Human/Agent)**
   - **Role**: High-level overseer.
   - **Actions**:
     - Issues explicit commands (e.g., "Pause session").
     - Approves/denies Sheepdog's renegotiation requests.

---

### **Boundary Token Lifecycle**
To handle fluid boundaries, we introduce **token states**:
**Dormant**: No active session (e.g., "Garden closed").
    - **Active**: Full interaction (e.g., "Garden party").
    - **Passive**: Paused but not closed (e.g., "Bathroom break allowed").
    - **Terminated**: Logged and archived.

*Example Transition*:
```
Dormant -> Active (Handshake)
Active -> Passive (Watchdog pauses)
Passive -> Active (Shepherd resumes)
```

---

### **Key Takeaways**
1. **Watchdog** = Ruthless enforcer (no barking at Shepherds).
2. **Sheepdog** = Agile mediator (handles auto-adjustments + Shepherd commands).
3. **Token States** = Dormant/Active/Passive for flexible boundaries.

---

### **Next Steps**
- Draft a `BoundaryAlert` schema (e.g., `{"type": "duration_violation", "suggestions": [...]}`).
- Prototype `Sheepdog.autoadjust()` logic (e.g., detect topic drift).
- Design the **ConsentLedger** to track state transitions.