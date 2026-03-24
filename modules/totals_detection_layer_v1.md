# TOTALS DETECTION LAYER V1

## CORE OBJECTIVE
Detect when NBA game totals will deviate from baseline projections due to pace, efficiency, and volatility spikes.

---

## PRIMARY SIGNALS

### 1. PACE SPIKE TRIGGER
- Possessions projected > +5 above baseline
- Early game fastbreak points > 10 (1H pace indicator)

→ Effect: +6 to +12 total points

---

### 2. ASSIST NETWORK SURGE
- Team assists trending > 30
- Ball movement high (low isolation rate)

→ Effect: Increased shot quality → Over bias

---

### 3. 3PT VARIANCE SPIKE
- 3PA volume high (30+ attempts)
- 3PT% > 40%

→ Effect: Explosive scoring environment

---

### 4. TRANSITION LOOP
- Fastbreak points > 15
- Turnovers fueling runouts

→ Effect: Sustained scoring loops

---

### 5. BLOWOUT DISTORTION
- Score gap > 15
- Bench units increase pace instead of slowing

→ Effect: Totals inflate (contrary to under assumption)

---

## SUPPRESSION SIGNALS (UNDER FLAGS)

### 1. HALFCOURT LOCK
- Pace < 95 possessions
- Isolation heavy offenses

→ Effect: -6 to -10 points

---

### 2. FOUL STAGNATION
- Low FTA early
- No bonus pressure

→ Effect: Slows scoring rhythm

---

### 3. SHOOTING REGRESSION WINDOW
- FG% unsustainably high early (>60%)
- Low assist support

→ Effect: Regression expected → Under lean

---

## DECISION ENGINE

### OVER ACTIVATION
Trigger if ≥ 2 of:
- Pace Spike
- Assist Surge
- 3PT Spike
- Transition Loop

---

### UNDER ACTIVATION
Trigger if ≥ 2 of:
- Halfcourt Lock
- Foul Stagnation
- Regression Window

---

## LIVEFLOW RULE
If OVER signals activate → avoid unders entirely
If UNDER signals activate → avoid overs entirely

---

## TAG OUTPUTS
- OVER_ENVIRONMENT_CONFIRMED
- UNDER_ENVIRONMENT_CONFIRMED
- NO_EDGE_ZONE

---

## VERSION
B.004_TOTALS_ENGINE_V1
