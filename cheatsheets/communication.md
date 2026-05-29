# Communicating in a 45-minute technical interview

Your stated #1 goal is to *think out loud and communicate clearly*. The
interviewer is scoring **how you reason**, not just the final answer. A correct
silent solution scores worse than a mostly-correct narrated one. Drill this
script until it's automatic — practice saying it on every problem this week.

---

## The 7-step script (works for SQL, Python, and design)

1. **Restate** the problem in your own words. ("So I need the top-2 servers by
   utilization per region, returning region, server, and the metric.")
2. **Clarify** with 1–3 targeted questions:
   - Data shape / grain? Nulls possible? Duplicates? Ties — keep all or pick one?
   - Expected output columns/format? Performance constraints / data size?
   - Time zone / date boundaries? Inclusive or exclusive ranges?
3. **Example + edge cases.** Name a tiny concrete example and the edge cases you
   intend to handle (empty input, ties, NULLs, single group, division by zero).
4. **State the approach** before coding. ("I'll aggregate to server grain in a
   CTE, then DENSE_RANK within region, then filter rank ≤ 2.") Mention one
   alternative and why you didn't pick it.
5. **Code it**, narrating as you go. Keep names readable. If you get stuck, say
   what you're stuck on — interviewers often nudge.
6. **Test it.** Walk a row through, or actually run it. Check the edge cases you
   named. Sanity-check row counts / magnitudes.
7. **State complexity & tradeoffs**, and what you'd improve with more time
   (indexes, handling late data, scaling).

---

## Budgeting 45 minutes (assume ~2–3 problems or 1 design)
- Intro / chitchat: ~5 min
- Per coding/SQL problem: ~2 min clarify, ~3 min approach, ~10 min code+test
- Leave ~5 min at the end for their questions and yours.
- If you're stuck >2 min, **say so and propose a brute-force first** ("let me get
  something correct, then optimize"). A working O(n²) beats a broken O(n).

---

## Phrases that signal seniority (use them honestly)
- "Let me make sure I have the grain right before I aggregate."
- "This LEFT JOIN could fan out my rows, so I'll aggregate first."
- "I'll handle the empty/NULL case explicitly."
- "Brute force is O(n²); I can get O(n) with a hash map — want me to go straight to that?"
- "Tradeoff: this is more readable but materializes an intermediate; at scale I'd…"
- "Here's how I'd verify this is correct: …"

## When you don't know something
Say what you *do* know and reason toward it. "I don't remember the exact
`PERCENTILE_CONT` syntax, but conceptually I need the median within each group;
in Postgres it's an ordered-set aggregate — let me write the structure and we can
fix syntax." Honesty + reasoning >> bluffing.

## For the role specifically (capacity / cost / forecasting)
Frame answers in their language when natural: utilization, headroom, unit cost
($/request, $/core-hour), seasonality, trend, p95 latency, SLOs, over/under-
provisioning. If a SQL question is about usage over time, mention that this is the
input you'd feed a forecast. It shows you see the bigger picture.

## Questions to ask THEM (have 3 ready)
- "What does a typical optimization or forecasting problem look like on this team?"
- "What does success look like in the first 6 months for this role?"
- "How do data scientists, finance, and engineering collaborate on cost models here?"

## The day before / day of
- Re-type both cheatsheets from memory one last time.
- Test your environment (editor, screen share, the DB/REPL).
- Have water, scratch paper, and your 3 questions written down.
- Sleep > cramming. Calm + fluent beats exhausted + having seen one more problem.
