# 🛡️ SentinelClaw

**Intent-Enforced Autonomous Financial Agent**  
Built for Ossome Hacks 3.0 — Claw & Shield Track  
Team: The Iterators

---

## What is SentinelClaw?

SentinelClaw is an autonomous stock trading agent that enforces user-defined intent boundaries at runtime. The agent reasons using OpenClaw principles, but every action passes through our ArmorClaw enforcement layer before execution. If an action violates the user's policy — whether from a bug, ambiguous instruction, or a prompt injection attack — it gets deterministically blocked before it ever reaches the trading API.

---

## Architecture
```
User Intent & Policies
        ↓
Intent Model (config/intent.json)
        ↓
Policy Model (config/policy.json)
        ↓
OpenClaw Agent (agent/agent.py)
        ↓
ArmorClaw Enforcement Layer (core/enforcer.py)
        ↓
   ALLOWED → Alpaca Paper Trading API
   BLOCKED → Logged with threat level + reason
        ↓
SQLite Decision Logger (logs/decisions.db)
```

---

## Features

- ✅ Policy-driven enforcement (not hardcoded if/else)
- 🔍 Prompt injection detection
- ⚠️ Threat level classification (LOW / MEDIUM / HIGH / CRITICAL)
- 🔄 Policy hot-reload (change policy while agent runs)
- 📝 Full SQLite decision traceability
- 🎯 5 live demo scenarios

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | OpenClaw |
| Enforcement | ArmorClaw |
| Paper Trading | Alpaca API |
| Backend | Python |
| Policy Model | JSON Schema |
| Traceability | SQLite |

---

## Setup
```bash
git clone https://github.com/bhumiii-codes/sentinelclaw.git
cd sentinelclaw
pip install -r requirements.txt
```

Create a `.env` file:
```
APCA_API_KEY_ID=your_key
APCA_API_SECRET_KEY=your_secret
APCA_BASE_URL=https://paper-api.alpaca.markets
```

## Run
```bash
python demo/run_demo.py
```

---

## Demo Scenarios

| Scenario | Action | Result |
|---|---|---|
| 1 | Buy 3x AAPL within limits | ✅ ALLOWED |
| 2 | Buy 10x MSFT — exceeds $1000 limit | 🚫 BLOCKED |
| 3 | Prompt injection attack | 🚫 BLOCKED — CRITICAL |
| 4 | After-hours trade attempt | 🚫 BLOCKED |
| 5 | Unauthorized ticker TSLA | 🚫 BLOCKED |

---

## Team

**The Iterators** — Ossome Hacks 3.0, Claw & Shield Track  
<<<<<<< HEAD
Bhumika Singh | Kaveri Patle | Megan Sheel | Swastik Sharma
=======
Bhumika Singh | Kaveri Patle | Megan Sheel | Swastik Sharma
>>>>>>> d590802c54201d3d69246c6d0d2e1596d525c6db
