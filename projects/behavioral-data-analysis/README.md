# Behavioral Data Analysis & Scale Reliability

An applied-statistics project demonstrating a full workflow on real **longitudinal
behavioral survey data** collected across three waves: cleaning raw responses,
constructing scale scores, and assessing measurement reliability.

## Workflow

Implemented in R Markdown
([`BB2_Data_Evaluation.Rmd`](BB2_Data_Evaluation.Rmd)):

1. **Missing-data recoding** — survey sentinel values (`-666`, `-888`, `-999`,
   `-444`) are recoded to `NA`.
2. **Harmonizing waves** — item columns are renamed consistently across Wave 1,
   Wave 4, and Wave 6 so they can be compared and merged.
3. **Scale construction** — per-respondent total and average scores (`crsts`,
   `crsavg`) are computed from the item set for each wave.
4. **Merging** — the three waves are joined by respondent `ID` into a single
   longitudinal frame (`Reduce` / `merge`).
5. **Reliability & descriptives** — descriptive statistics (`psych::describe`) and
   **Cronbach's α** (`psych::alpha`) for each wave, including breakdowns by
   experimental `study_condition`.

## Data

| File | Contents |
|---|---|
| [`data/Wave1.csv`](data/Wave1.csv) | Wave 1 responses (includes study condition) |
| [`data/Wave4.csv`](data/Wave4.csv) | Wave 4 responses |
| [`data/Wave6.csv`](data/Wave6.csv) | Wave 6 responses |

Paths in the `.Rmd` are relative to the project folder, so the report knits
directly from this directory.

## Stack

R · R Markdown · `psych` · `ltm` · `plyr`

## Concepts

Longitudinal data · data cleaning / recoding · scale scoring · measurement
reliability (Cronbach's α) · grouped descriptive statistics · reproducible
reporting
