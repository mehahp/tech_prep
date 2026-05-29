# Day 6 — Systems Design

**Goal:** have a framework you can run on any prompt, and be able to deliver the
capacity/forecasting design fluently. For a junior-leaning role they want
**structured thinking + communication**, not encyclopedic depth.

### Warm-up (10 min)
From blank: re-type your strongest SQL window query and one Python pattern, so the
coding skills stay warm. (Design day shouldn't cost you your SQL muscle memory.)

### Learn (30 min)
Read `systems_design/framework.md` end to end. Memorize the **6 step headers** so
you can run them on autopilot:
1. Requirements & scope → 2. Estimate → 3. High-level design → 4. Data model & APIs
→ 5. Deep dive → 6. Scale/reliability/wrap-up.
Also read the **tradeoff vocabulary** and the **ML mini-framework** — this is an
ML optimization team, so expect a data/forecasting flavor.

### Drill (50 min) — out loud, this is a *speaking* skill
1. Read `systems_design/worked_example.md` once.
2. Close it. Set a 12-min timer. Deliver the capacity-monitoring/forecasting
   design from only the 6 headers, talking the whole time. Record yourself or
   pretend an interviewer is there.
3. Throw yourself one curveball and answer it:
   - "Servers report late / out of order — how do you handle it?"
   - "How would you attribute shared infra cost to each service?"
   - "Forecast says we need 20% more cores next quarter — how confident are you?"
4. Do the 12-min delivery **a second time**. It should be noticeably smoother.

### Bonus framing reps (if time)
Practice turning a vague ask into **objective + constraints + decision variables**:
- "Allocate capacity across 4 regions to minimize cost while meeting p95 demand."
- Say: *variables* = cores per region; *objective* = minimize total cost;
  *constraints* = provisioned ≥ forecasted peak × safety factor, ≤ DC capacity.
This phrasing is exactly the team's day job — it lands well.

### Spaced repetition (10 min)
Redo **Q27 (week-over-week growth, Day 4)** cold.

### Reflect (5 min)
Which of the 6 steps did you rush or skip? That's where you'll freeze under
pressure — note it and re-run that step tomorrow.

**Done when:** you can deliver the worked design in ~12 minutes from the 6 headers
without notes, and frame a capacity problem as objective/constraints/variables.
