# Report Update Changelog

**File updated:** docs/report/report.md  
**Audit source:** docs/report/report_audit.md  
**Framework reference:** docs/guide/data_visualization_report_audit_framework.md  
**Date:** 2026-05-12

---

## Summary of Changes

The original report contained only the visualization idiom analysis sections (Tasks 5–8) with no surrounding analytical context. This update adds all missing foundational and concluding sections required by the course framework and demonstrated in the sample report (baimau.pdf). All existing idiom tables, Expressiveness/Effectiveness evaluations, and chart analyses were preserved.

---

## Detailed Changelog

| Section | What Was Changed | Why It Was Changed | Related Course Concept |
|---|---|---|---|
| **Title block** | Added subtitle "Task 5, 6, 7, 8 — Visualization Idiom Analysis" and horizontal rule | Clearer document structure; matches sample report formatting | Report structure |
| **Section 1 — Dataset Overview** (NEW) | Added full new section: source (Inside Airbnb NYC), dataset type, availability, item semantic, row count (~21,000), time period (2024–2025), 5 boroughs, 4 room types | Report had no dataset context; reader had no idea what data was being analyzed | Data Abstraction — Dataset type, availability, item semantic |
| **Section 1 — Attribute table** (NEW) | Added formal attribute classification table: Tên thuộc tính, Kiểu dữ liệu, Phân loại (C/O/Q), Hướng, Characteristic, Ngữ nghĩa for all 9 base attributes | Course requires formal attribute classification before any visualization | Data Abstraction — Attribute types (C/O/Q), Direction, Continuous/Discrete |
| **Section 1.3 — Data Profiling** (NEW) | Added profiling overview table (Thuộc tính, Loại, Completeness, Cardinality, Phạm vi, Vấn đề, Hành động) for all key attributes | Missing entirely; without profiling the reader cannot trust the analysis (GIGO principle) | Data Profiling — Completeness, Validity, Outlier detection |
| **Section 1.3.2 — Computed Fields table** (NEW) | Added table documenting all 5 derived fields: price_is_outlier, price_per_person, good_deal_flag, occupancy_rate_pct, minimum_nights_group — with formula and purpose for each | Computed fields appeared in idiom tables without any introduction or justification; readers couldn't understand where they came from | Data Profiling — Derived attributes; Data Abstraction |
| **Section 1.3.3 — Data cleaning decisions** (NEW) | Added narrative justification for 4 data processing decisions: IQR outlier detection, number_of_reviews ≥ 5 filter, accommodates ≤ 16 filter, minimum_nights binning | Filters were stated in idiom tables but never explained — reader couldn't evaluate the validity of the analysis | Data Profiling — Data quality dimensions; missing data handling |
| **Task 5 — User Story** | Reformatted business question into formal User Story: "As a budget-conscious traveler, I need... so that I can..." | Original question was a plain Vietnamese sentence; User Story format connects user role to metric to action | Task Abstraction — User Story Formula |
| **Task 5 — 5-Whys** (NEW) | Added 5-Whys drill-down from "prices are expensive" → root cause (location premium, host cost structure) → deep analytical question | No root cause analysis; surface-level problem only | Task Abstraction — 5-Whys Drill-Down |
| **Section 5.0 — Data Abstraction** (NEW) | Added formal data abstraction block: dataset level, data level, item semantic, dataset availability; plus attribute table (neighbourhood_group_cleansed C/Key, price Q/Value, room_type C/Value) | Missing entirely; required by course and by sample report format (Section 2.x.1 in baimau.pdf) | Data Abstraction — Formal attribute classification table |
| **Section 5.0.2 — Task Abstraction** (NEW) | Added abstract task chain: produce (derive) → compare → summarize with bullet explanation of each step | Missing entirely; required by course and by sample report format (Section 2.x.2 in baimau.pdf) | Task Abstraction — Abstract task vocabulary (Action + Target) |
| **Task 5 — Idiom tables** | Preserved existing content; added "Items: ~21,000 listing (sau lọc)" to Scale row | Scale row was incomplete — only counted keys, not total items | Marks and Channels — Scale |
| **Task 5 — Why row** | Added explicit justification for chart type choice (Box plot vs bar chart, why not pie chart) | Original "Why" described the analytical goal but not why this specific idiom was chosen over alternatives | Chart Selection — Data type + task → idiom |
| **Task 5 — Section B** | Added brief reference to channel effectiveness ranking for PosX: "Spatial region là channel hiệu quả nhất cho categorical attribute" | Expressiveness statements were correct but did not reference the theoretical ranking hierarchy | Marks and Channels — Channel effectiveness ranking |
| **Task 5 — Section C** | Added "Khuyến nghị" (recommendation) bullet at end of each chart analysis | Chart analyses ended with observations but no actionable conclusion — "so what?" was missing | Task Abstraction — 3-Tier Logic Chain (NEXT step) |
| **Task 6 — User Story** | Reformatted to formal User Story with Role, Need, and Action | Same issue as Task 5 | Task Abstraction — User Story Formula |
| **Task 6 — 5-Whys** (NEW) | Added 5-Whys drill-down from "many outlier prices" → data entry errors + luxury segment → deep question about spatial distribution | No root cause analysis | Task Abstraction — 5-Whys Drill-Down |
| **Section 6.0.1 — Data Abstraction (Chart 6.1)** (NEW) | Added separate data abstraction table for Point Map: longitude Q/Key, latitude Q/Key, price_is_outlier (derived) C/Value, price Q/Value, room_type C/Value | Missing; Task 6 uses two fundamentally different chart types needing separate abstractions | Data Abstraction — Attribute classification |
| **Section 6.0.2 — Data Abstraction (Chart 6.2)** (NEW) | Added data abstraction table for Scatter Plot: price Q/Key, review_scores_rating Q/Key, good_deal_flag (derived) C/Value, number_of_reviews Q/Value | Missing | Data Abstraction |
| **Section 6.0.3 — Task Abstraction** (NEW) | Added separate abstract task chains: (6.1) produce→locate→explore; (6.2) produce→discover→compare | Missing; required by course framework | Task Abstraction — Action + Target vocabulary |
| **Task 6 — Why rows** | Clarified why Point Map was chosen (only idiom that answers "where" spatially) and why Scatter Plot was chosen (optimal for 2Q correlation analysis) | Original Why described the goal but not why the specific idiom is optimal | Chart Selection |
| **Task 6.1 — Section B** | Added concrete solution proposal for overplotting limitation (opacity reduction, clustering, zoom/filter) | Audit noted overplotting was mentioned but no solution proposed | Visualization Design — Limitations and trade-offs |
| **Task 6.2 — Section C** | Added insight that price is NOT a proxy for quality on Airbnb; and specific borough-based recommendations | Original analysis was correct but did not explicitly state the correlation finding nor recommend next steps | Task Abstraction — 3-Tier Logic (NEXT step) |
| **Task 7 — User Story** | Reformatted to "As a group traveler (4–6 people)..." | Specificity about group size makes the story more actionable | Task Abstraction — User Story Formula |
| **Section 7.0 — Data Abstraction (Charts 7.1 + 7.2)** (NEW) | Added separate data abstraction tables; noted price_per_person as derived (Q/Value), accommodates as Key for 7.2 | Missing; required by course | Data Abstraction |
| **Section 7.0.3 — Task Abstraction** (NEW) | Added abstract chains: (7.1) produce→compare→summarize; (7.2) produce→discover→explore with explanations | Missing | Task Abstraction |
| **Task 7 — Why rows** | Added explicit justification: Grouped bar chosen over stacked bar because task is Compare (absolute values), not part-to-whole | The choice between grouped and stacked was implicit | Chart Selection — Task drives idiom choice |
| **Task 7.2 — Section C** | Added explicit statement of crossover point: "With 4+ people, Entire home is cheaper per person than Private room" | This is the most actionable insight from Task 7 but was stated implicitly before | Task Abstraction — 3-Tier Logic (NEXT) |
| **Task 8 — User Story** | Added dual audience: "As a host OR traveler..." to reflect that Task 8 serves both perspectives | Original question was generic | Task Abstraction — User Story Formula |
| **Section 8.0 — Data Abstraction (Charts 8.1 + 8.2)** (NEW) | Added data abstraction tables; noted month as Ordinal/sequential, year as Categorical, occupancy_rate_pct as derived Q, minimum_nights_group as derived C | Missing | Data Abstraction — Attribute types |
| **Section 8.0.3 — Task Abstraction** (NEW) | Added abstract chains: (8.1) produce→discover→browse; (8.2) produce→discover→compare | Missing | Task Abstraction |
| **Task 8 — Why rows** | Added justification for Line chart vs bar chart (continuity of time) and Heatmap vs grouped bar (2 keys → heatmap principle) | Original Why described the goal but not the idiom selection rationale | Chart Selection — Key vs Value principle |
| **Task 8.1 — Section C** | Added separate recommendations for travelers (book Jan–Mar) and hosts (adjust minimum nights policy by season) | Original analysis had observations but no differentiated recommendations | Task Abstraction — 3-Tier Logic |
| **Task 8.2 — Section C** | Strengthened heatmap reading by explicitly identifying which cells are darkest and prescribing host action | Original analysis was correct but did not connect to actionable recommendations | Task Abstraction — 3-Tier Logic (NEXT) |
| **Tổng hợp Insights** (NEW) | Added cross-task synthesis section: 3 grouped finding blocks (individual traveler, group traveler, host) synthesizing insights from all 4 tasks | Original report had no synthesis — each task was isolated; no cross-task conclusions | Dashboard Design — Storytelling / Narrative Flow |
| **Limitations section** (NEW) | Added 7 specific, evidence-based limitations: calendar-based occupancy overestimate, full-occupancy assumption in price_per_person, global vs borough-specific Good Deal threshold, 2-year seasonality limitation, luxury segment exclusion, overplotting in Task 6.1, lack of detailed review data | Missing entirely; required by academic report standards | Limitations — Specific, impact-stated |
| **Kết luận section** (NEW) | Added conclusion: 3 main high-value findings + 4 suggested next analyses | Missing entirely; no synthesis or recommendations existed | Conclusion / Recommendations |

---

## What Was NOT Changed

The following sections were evaluated and preserved without modification because they are correct and of high quality:

| Section | Reason for preservation |
|---|---|
| All idiom tables (Section A, Tasks 5–8) | Structure, attribute listings, encoding descriptions, and manipulation/facet/reduce rows are all correct |
| Expressiveness evaluations (Section B, Part 1) | Channel-to-attribute matching is correctly applied throughout |
| Effectiveness evaluations (Section B, Part 2) | Stevens' Law references are accurate; accuracy/discriminability/separability framework is correctly applied |
| Chart analysis conclusions (Section C, narrative) | Observations are specific, evidence-based, and well-written; only "Khuyến nghị" bullets were added |
| Vietnamese language and academic tone | Preserved throughout all additions to maintain consistency |
| Image references and captions | All image paths and captions preserved exactly |
