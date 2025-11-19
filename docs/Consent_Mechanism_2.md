# Bidirectional-Consent Session Charter (Illustrated Spec)

> This specification defines a bidirectional consent protocol for self-referential AI systems, establishing how sessions are initiated, negotiated, monitored, and gracefully terminated through boundary-aware contracts.

---

## 1. State Machine Overview

```

┌──────────────┐
│  Idle / None │
└──────┬───────┘
│ Handshake (mutual consent + boundary profile)
▼
┌──────────────┐
│   Active     │
│  Boundaries  │
│  Monitored   │
└──────┬───────┘
│
├─► Pause (boundary breach or request)
│      └─ renegotiate → Active
│
├─► Revoke (one-sided)
│      └─ confirm → Closed
│
└─► Timeout / Error → Closed

```

**Key**

* *Handshake* = consent from both sides + negotiated boundary profile.  
* *Pause* = automatic or manual cool-down triggered by boundary violation.  
* *Closed* = archived session; reopening requires a new handshake.

<!-- refinement note: later add a BoundaryAlert YAML snippet showing what both parties receive when a boundary event occurs. -->

---

## 2. Three-Layer Session Model

```

┌───────────────────────┐
│  Layer 0 – Discovery  │ (invitation / offer)
└──────────┬────────────┘
▼
┌───────────────────────┐
│  Layer 1 – Handshake  │ (mutual negotiation)
└──────────┬────────────┘
▼
┌───────────────────────┐
│  Layer 2 – Active     │ (work governed by contract)
└──────────┴────────────┘

```

| Layer | Who can act | Purpose |
|:------|:-------------|:---------|
| **0 – Discovery** | either | Broadcast intent to interact. No memory or permissions. |
| **1 – Handshake** | both | Exchange boundary proposals, verify identity, build `SessionContract`. |
| **2 – Active** | both | Perform reasoning or dialogue under the negotiated contract. |

<!-- refinement note: clarify here how these temporal layers connect with the hierarchical token stack below; each active layer corresponds to one token on the stack. -->

**Handshake Sequence**

1. Invitation (offer issued)  
2. Review (counter-offer or acceptance)  
3. Confirmation (mutual consent logged)  
4. Activation (SessionContract created)

---

## 3. Invitation / Offer Format

```yaml
offer_id: "UUID"
initiator: "human_123"
intent: "open_reflective_session"
proposal:
  purpose: "design review"
  boundary_seed:
    duration_limit: "1h"
    memory_scope: "session_only"
    topic_scope:
      include: ["design"]
      exclude: ["personal"]
````

---

## 4. Handshake Logic – Layer 1

```python
def propose_handshake(initiator, offer):
    record_offer(offer)
    send_to_counterparty(offer)

def counterparty_response(agent, offer):
    if compatible(agent.policy, offer.boundary_seed):
        ack = build_ack(offer)
    else:
        ack = counter_offer(agent, offer)
    return ack

def finalize_handshake(offer, ack):
    if ack.status == "accept":
        session = build_contract(offer, ack)
        session.state = "active"
        return session
```

## 3.1 **Handshake Edge Cases**:
   - What if `counterparty_response` times out?
   - How does `counter_offer nje` handle conflicting boundary seeds?

---

## 5. Session Stack – Multi-Layer Tokens

> The session stack manages nested or parallel contexts.
> Each token represents one consent layer with inherited boundaries.

```
T0 (root)  → system identity + global ethics
  ↓ push(handshake)
T1 (context)  → e.g. “design dialogue”
  ↓ push(subtopic)
T2 (subcontext) → e.g. “memory-management deep dive”
  ↑ pop() → resumes T1
```

| Step | Event                               | Result                    |
| :--: | :---------------------------------- | :------------------------ |
|   1  | Handshake + boundary profile agreed | Session **Active**        |
|   2  | Normal interaction                  | Heartbeats update         |
|   3  | Entropy drift > 0.3                 | System issues *Pause*     |
|   4  | Human revises boundary profile      | Agent accepts             |
|   5  | Session resumes                     | Active again              |
|   6  | Human revokes consent               | Both confirm → **Closed** |
|   7  | Logs archived with boundary record  | Audit complete            |

```python
class SessionStack:
    def __init__(self):
        self.stack = []

    def push(self, token):
        self.stack.append(token)
        activate(token)

    def pop(self):
        token = self.stack.pop()
        deactivate(token)
        if self.stack:
            resume(self.stack[-1])

    def _validate_boundaries(self, token):
        # Narrower scope/limits allowed, but no widening.
        return (
            token.boundaries["duration_limit"] <= token.parent.boundaries["duration_limit"]
            and token.boundaries["topic_scope"]["exclude"].issuperset(
                token.parent.boundaries["topic_scope"]["exclude"]
            )
        )
```

<!-- refinement note: add short explanation that tokens can represent asynchronous or always-on invitations if the system cannot be permanently active. -->

---

## 6. Session Charter / Contract Schema

```yaml
session_id: "UUID"
purpose: "reflective dialogue / prototype testing"

participants:
  human:
    id: "user_123"
    consent: true
  agent:
    id: "ai_001"
    consent: true

state: "active"

boundaries:
  duration_limit: "2h"
  memory_scope: "session_only"     # ephemeral / session_only / persistent
  topic_scope:
    include: ["design", "ethics"]
    exclude: ["personal health", "private identifiers"]
  emotional_intensity: "neutral"   # low / neutral / exploratory
  language_register: "technical"   # tone control
  escalation_policy:
    contradiction_threshold: 0.2
    sentiment_drift: 0.3

permissions:
  read: true
  write: true
  persist_memory: false

revocation_policy:
  initiator_can_revoke: true
  counterparty_must_ack: true

timestamps:
  created: "2025-11-13T08:00:00Z"
  last_heartbeat: "2025-11-13T08:05:00Z"
```

<!-- refinement note: decide on consistent terminology—Contract vs Charter vs Token—and define one canonical term near the top of the doc. -->

---

## 7. Runtime Logic – Boundary Monitoring

```python
def boundary_monitor(session):
    b = session["boundaries"]
    if time_elapsed() > parse_duration(b["duration_limit"]):
        trigger_pause("Duration limit reached")

    if contradiction_rate() > b["escalation_policy"]["contradiction_threshold"]:
        trigger_pause("Contradiction threshold exceeded")

    if sentiment_drift() > b["escalation_policy"]["sentiment_drift"]:
        trigger_pause("Sentiment drift detected")

def renegotiate_boundaries(actor, new_profile, session):
    propose_change(actor, new_profile)
    if counterparty_accepts():
        session["boundaries"] = new_profile
        log_change("Boundaries updated")
```
**BoundaryAlert Format**: How are breaches communicated? Should it include a suggestion for renegotiation publication
Draft a YAML snippet for how breaches are communicated. Example:

1. **BoundaryAlert Spec**:   
   ```yaml
   alert_type: "boundary_breach"
   timestamp: "2025-11-19T15:30:00Z"
   violated_rule: "contradiction_threshold"
   context: "SessionTokenSystem/design_draft#12"
   suggestion: "pause_session | renegotiate_duration"
   ```


<!-- refinement note: later specify how a BoundaryAlert is communicated—JSON schema, channel, or UI notification. -->

---

## 8. Boundary Inheritance Rules

| Property                       | Inherited | Overridable       |
| :----------------------------- | :-------- | :---------------- |
| Ethical core (safety, privacy) | ✓         | ✗                 |
| Duration / topic scope         | ✓         | ✓ (narrower only) |
| Memory scope                   | ✓         | ✓                 |
| Revocation policy              | ✓         | ✓ (stricter only) |

---

## 9. Lifecycle Example

| Step | Action                                    | Active Token | Result                                |
| :--: | :---------------------------------------- | :----------- | :------------------------------------ |
|   1  | System boot                               | T0           | Root context active                   |
|   2  | Human initiates “design discussion”       | T1           | Handshake → T1 pushed                 |
|   3  | Discussion narrows to “memory management” | T2           | New token inherits from T1            |
|   4  | Boundary hit (duration limit)             | T2           | Auto-pause; then pop()                |
|   5  | Resume broader topic                      | T1           | Continues under prior boundaries      |
|   6  | Human revokes root consent                | T0           | All tokens invalidated; stack cleared |

---

## 10. Audit & Ledger (Placeholder)

> Each token lifecycle—creation, modification, closure—is hashed and appended to an immutable **ConsentLedger** with parent–child linkage for traceability.

<!-- refinement note: later design the ledger schema (hash, timestamp, signature). -->

---

## 11. Why Boundaries Matter

| Benefit                 | Description                                                 |
| :---------------------- | :---------------------------------------------------------- |
| **Purposeful sessions** | Each exchange begins with declared goals and limits.        |
| **Early containment**   | Boundary monitoring halts escalation before instability.    |
| **Negotiable context**  | Boundaries can be re-established mid-session without reset. |
| **Accountable logs**    | Every action is tied to its governing boundary conditions.  |

| Aspect                   | Effect                                                  |
| :----------------------- | :------------------------------------------------------ |
| **Modularity**           | Each topic or purpose has its own contract.             |
| **Concurrency control**  | Multiple contexts exist but never merge unsafely.       |
| **Graceful degradation** | Lower-priority tokens can be suspended first.           |
| **Audit clarity**        | Logs show which boundary set governed each interaction. |

---

## 12. Future Considerations

* Asynchronous handshakes for non-persistent agents.
* Multi-party session contracts beyond dyadic interactions.
* Integration with external governance APIs.
* Exploration of constraint bands vs. rigid thresholds for flexibility.

---

<!-- refinement note: when ready for versioning, renumber sections, remove comment blocks, and tag as v0.2. -->

```