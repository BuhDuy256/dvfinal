# Report Audit — Airbnb NYC Data Visualization Report

**Auditor role:** Senior Data Visualization Professor  
**Report audited:** docs/report/report.md (Tasks 5–8)  
**Framework reference:** docs/guide/data_visualization_report_audit_framework.md  
**Sample reference:** docs/sample/baimau.pdf  
**Date:** 2026-05-12

---

## Executive Summary

The current report demonstrates solid understanding of visualization idioms, Expressiveness/Effectiveness evaluation, and chart-level analysis. However, it is missing all of the foundational academic layers that the course requires: there is no introduction, no data profiling section, no data abstraction tables, and no task abstraction sections. The report jumps directly from the task title into the idiom table without any analytical setup. There are also no limitations or conclusion sections. Every one of these is required by the course framework and present in the sample report.

**Overall status: Needs significant additions — existing content quality is good and should be preserved.**

---

## Issue List

### CRITICAL — Missing Sections

| # | Issue | Location | Impact |
|---|---|---|---|
| C1 | No introduction or dataset context | Beginning of report | Reader has no idea what dataset is being analyzed or why |
| C2 | No dataset overview section | Beginning of report | Item semantic, dataset type, availability — all unstated |
| C3 | No data profiling section | Beginning of report | No evidence that data quality was assessed; violates GIGO principle |
| C4 | No data abstraction table for any task | All tasks | Missing the formal C/O/Q classification, Key/Value, Direction — core course requirement |
| C5 | No task abstraction section for any task | All tasks | No abstract task chain (e.g., produce → compare → summarize) — core course requirement |
| C6 | No limitations section | End of report | Reader cannot assess validity of insights |
| C7 | No conclusion or synthesis section | End of report | Insights from 4 tasks are never synthesized; no recommendations |

### MAJOR — Analytical Gaps

| # | Issue | Location | Impact |
|---|---|---|---|
| M1 | Business question present but not formatted as User Story | Each task header | Misses the formal "As a [Role], I need [Metric+Breakdown] so I can [Action]" structure |
| M2 | 5-Whys analysis absent | Each task | Surface-level problem statement; no root cause exploration |
| M3 | Computed/derived fields not documented anywhere | Entire report | Fields like `price_is_outlier`, `price_per_person`, `good_deal_flag`, `occupancy_rate_pct`, `minimum_nights_group` appear in idiom tables without being formally introduced as derived attributes |
| M4 | No "Insights" synthesis section | End of report | Each chart's findings are isolated; no cross-task conclusions or actionable recommendations |
| M5 | Why the chart type was chosen is implicit | Each idiom | The connection between data type + task → chart type is not explicitly stated before the idiom table |

### MINOR — Improvements

| # | Issue | Location | Suggestion |
|---|---|---|---|
| S1 | Stevens' Law reference in Effectiveness section lacks connection to design decision | Tasks 5–8 | After citing Stevens' Law, add one sentence on how this influenced the choice of encoding |
| S2 | Filter decisions (price_is_outlier, number_of_reviews ≥ 5) stated in idiom table but not justified anywhere | Tasks 5–8 | Justify these in a data cleaning/profiling section |
| S3 | Chart analysis sections (Section C) are good but could end with a "So what?" — an actionable recommendation | All charts | Add one sentence per chart: "Therefore, du khách nên..." |
| S4 | Task 6.1 overplotting issue is mentioned but no solution is proposed | Task 6.1 Section B | Suggest a solution (opacity reduction, clustering, zoom view) |
| S5 | The "Scale" row in idiom tables only counts keys but not total items | All idiom tables | Add approximate item count (e.g., "Items: ~21,000 listing") |

---

## Required Additions (Prioritized)

### Priority 1 — Must Add

1. **Section 1: Dataset Overview + Data Profiling**
   - Dataset description (source, row count, time period, item semantic, dataset type/availability)
   - Profiling table for key attributes (known from chart filters and computed fields)
   - Document computed fields and why they were created
   - Document filter decisions and their justification

2. **Per-task: Data Abstraction table** (before the idiom tables in each task)
   - Format: dataset level | data level | item semantic | dataset availability
   - Attribute table: Tên | Phân loại (C/O/Q) | Hướng | Characteristic | Ngữ nghĩa | Key | Value

3. **Per-task: Task Abstraction** (following the data abstraction table)
   - Abstract task chain (e.g., produce → compare → summarize)
   - Bullet explanation of each step

4. **Limitations section** (after Task 8)
   - At least 5 specific, evidence-based limitations

5. **Conclusion section** (after Limitations)
   - Synthesis of cross-task insights
   - Actionable recommendations for travelers

### Priority 2 — Should Add

6. **Reformatted User Story** per task (using the formal template)
7. **5-Whys analysis** for at least 2 tasks (Task 5 and Task 6 are the best candidates)
8. **"So what?" recommendation** at end of each chart analysis (Section C)

### Priority 3 — Nice to Have

9. **Inverted Pyramid description** explaining the overall dashboard logic
10. **Cross-task insight synthesis** table

---

## Sections to Preserve (Do Not Change)

The following sections in the current report are correct and well-written — keep them intact:

- All idiom tables (Section A of each chart) — structure and content are correct
- All Expressiveness evaluations (Section B, part 1) — correct application of channel principles
- All Effectiveness evaluations (Section B, part 2) — Stevens' Law references are accurate
- All chart analysis conclusions (Section C) — observations are specific and evidence-based

---

## Sample Report Compliance Check

Based on the sample report (baimau.pdf) structure:

| Sample Section | Status in Current Report |
|---|---|
| Data Profiling (Section 1) | ❌ Missing |
| Data Abstraction per task (Section 2.x.1) | ❌ Missing |
| Task Abstraction per task (Section 2.x.2) | ❌ Missing |
| Visualization idiom tables | ✅ Present and well-done |
| Chart evaluation (Expressiveness/Effectiveness) | ✅ Present |
| Chart analysis | ✅ Present |
| Limitations | ❌ Missing |
| Conclusion | ❌ Missing |
