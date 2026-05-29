# Day 7 — Timed Mock + Spaced Review

**Goal:** rehearse the real 45-minute format under time pressure and consolidate.
Today is about *confidence and recall*, not new material.

### Warm-up (10 min)
From blank, re-type: a top-N-per-group query, a moving-average query, the
conditional-aggregation pattern, and `two_sum`. These are your "money" patterns —
they should flow now.

---

### Mock Interview A — Data/SQL focus (45 min, timed) ⏱
Simulate the real thing. **Talk out loud the entire time** using the 7-step script
from `cheatsheets/communication.md`. No peeking at solutions until the timer ends.

1. (2 min) Warm-up question — *aloud*: "What's the difference between WHERE and
   HAVING, and between RANK and DENSE_RANK?"
2. (12 min) **Q22** redo from scratch (top-2 utilized servers per region) — but
   first *clarify requirements out loud* as if the schema were new.
3. (12 min) **Q27** (week-over-week fleet cost growth %).
4. (12 min) **Q24 or Q30** (streak via gaps-and-islands, or recursive date spine).
5. (5 min) Out loud: how would these queries feed a capacity forecast? What would
   you index? How does it scale to billions of rows?

Then check all answers against `sql/solutions.sql`. Score yourself: correct?
fluent? did you narrate?

---

### Mock Interview B — Mixed (45 min, timed) ⏱ — *do later in the day*
1. (5 min) Python warm-up aloud: `group_by_sum` + complexity.
2. (10 min) One Tier-2 Python problem (P7 longest-unique-substring or P9
   merge-intervals), brute-force-then-optimize narration.
3. (10 min) One SQL window problem you haven't redone today (e.g., **Q18**).
4. (15 min) **Systems design**: deliver the `worked_example.md` design from the 6
   headers, plus one curveball.
5. (5 min) Ask your 3 prepared questions aloud (from `communication.md`).

---

### Gap-fill (remaining time)
Go back to every problem you failed twice this week (your reflect notes). Redo each
cold. Anything still shaky, write the pattern on a physical index card and review
it tonight and tomorrow morning.

### Final confidence checklist
- [ ] I can write a 3-table join + anti-join cold.
- [ ] WHERE vs HAVING, RANK vs DENSE_RANK vs ROW_NUMBER — instant explanation.
- [ ] Conditional aggregation `SUM(CASE WHEN…)` — automatic.
- [ ] Moving average, running total, `LAG` delta — from blank.
- [ ] Top-N-per-group with a CTE + window — from blank.
- [ ] Recursive CTE date spine — I understand and can attempt it.
- [ ] `group_by_sum`, dict-index join, `two_sum`, sliding window — from blank.
- [ ] I can run the 6-step design framework + the capacity/forecasting example.
- [ ] I narrate the whole time using the 7-step script.
- [ ] I have 3 questions ready for the interviewer.

### The night before the real interview
- One slow re-type of both cheatsheets from memory. Stop early.
- Test your tools (editor, screen-share, the DB/REPL).
- Sleep. Calm + fluent > tired + crammed. You've put in the reps — trust them.
