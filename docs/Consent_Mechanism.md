# Bidirectional-Consent Session Charter (Illustrated Spec)

### 1. State Machine Overview

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

**Key:**

* *Handshake* = consent from both sides + negotiated boundary profile.
* *Pause* = automatic or manual cool-down triggered by boundary violation.
* *Closed* = archived session; reopening requires a new handshake.

---

### 1  |  Three-Layer Session Model

```
┌───────────────────────┐
│  Layer 0 – Discovery  │  (invitation / offer)
└──────────┬────────────┘
           ▼
┌───────────────────────┐
│  Layer 1 – Handshake  │  (mutual negotiation)
└──────────┬────────────┘
           ▼
┌───────────────────────┐
│  Layer 2 – Active     │  (work governed by contract)
└──────────┴────────────┘
```

### 2 | Concept: the Session Stack

| Layer             | Who can act | Purpose                                                                |
| ----------------- | ----------- | ---------------------------------------------------------------------- |
| **0 – Discovery** | either      | Broadcast intent to interact. No memory or permissions.                |
| **1 – Handshake** | both        | Exchange boundary proposals, verify identity, build `SessionContract`. |
| **2 – Active**    | both        | Perform actual reasoning or dialogue under negotiated contract.        |


| Step | Actor  | Action                                           | Result                                         |
| ---- | ------ | ------------------------------------------------ | ---------------------------------------------- |
| 0    | Human  | Sends *offer*                                    | Discovery layer open                           |
| 1    | Agent  | Reviews policy, counter-offers extended duration | Negotiation                                    |
| 2    | Human  | Accepts new boundary                             | Contract created                               |
| 3    | Both   | Confirm handshake                                | Session enters **Active**                      |
| 4    | Either | Revoke consent                                   | Returns to **Discovery** (awaiting next offer) |


### 3  |  Invitation / Offer Format

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
```

### 4  |  Handshake Logic (Layer 1)

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

### 5  |  Layered Session Example

┌──────────────────────┐
│  Root Token (T0)     │  → system identity + global ethics
├──────────────────────┤
│  Context Token (T1)  │  → e.g. “design dialogue”
├──────────────────────┤
│  Sub-context Token   │  → e.g. “memory-management deep dive”
└──────────────────────┘

| Step | Event                               | Result                    |
| ---- | ----------------------------------- | ------------------------- |
| 1    | Handshake + boundary profile agreed | Session **Active**        |
| 2    | Normal interaction                  | Heartbeats update         |
| 3    | Entropy drift > 0.3                 | System issues *Pause*     |
| 4    | Human revises boundary profile      | Agent accepts             |
| 5    | Session resumes                     | Active again              |
| 6    | Human revokes consent               | Both confirm → **Closed** |
| 7    | Logs archived with boundary record  | Audit complete            |

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
```

### 5.1  | Session Charter Schema (YAML)

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

---

### 6 | Runtime Logic (Simplified)

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

### 6.1 | Example Lifecycle


| Step | Action                                    | Active Token | Result                                |
| ---- | ----------------------------------------- | ------------ | ------------------------------------- |
| 1    | System boot                               | T0           | Root context active                   |
| 2    | Human initiates “design discussion”       | T1           | Consent handshake → T1 pushed         |
| 3    | Discussion narrows to “memory management” | T2           | New token layered; inherits from T1   |
| 4    | Boundary hit (duration limit)             | T2           | Auto-pause; then pop()                |
| 5    | Resume broader topic                      | T1           | Continues under prior boundaries      |
| 6    | Human revokes root consent                | T0           | All tokens invalidated; stack cleared |

---


### 6 | Boundary Inheritance Rules

| Property                       | Inherited | Overridable       |
| ------------------------------ | --------- | ----------------- |
| Ethical core (safety, privacy) | ✓         | ✗                 |
| Duration / topic scope         | ✓         | ✓ (narrower only) |
| Memory scope                   | ✓         | ✓                 |
| Revocation policy              | ✓         | ✓ (stricter only) |



### 6.1 Why Boundaries Matter

| Benefit                 | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| **Purposeful sessions** | Each exchange begins with declared goals and limits.        |
| **Early containment**   | Boundary monitoring halts escalation before instability.    |
| **Negotiable context**  | Boundaries can be re-established mid-session without reset. |
| **Accountable logs**    | Every action is tied to its governing boundary conditions.  |


| Aspect                   | Effect                                                           |
| ------------------------ | ---------------------------------------------------------------- |
| **Modularity**           | Each topic or purpose can have its own contract.                 |
| **Concurrency control**  | Multiple contexts exist but never merge unsafely.                |
| **Graceful degradation** | When resources are limited, lower tokens can be suspended first. |
| **Audit clarity**        | Logs show which boundary set governed each interaction.          |

---