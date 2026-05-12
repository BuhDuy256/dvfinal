# Data Visualization Report Audit Framework

> **How to use this document:** Read it before writing your report. Use Section 3 (Checklist) to self-audit your report before submission. Use Section 4 (Mapping Template) to check each concept one by one. This framework is extracted directly from the course slides (Chapters 1–8).

---

## Section 1: Overall Data Visualization Project Flow

A complete Data Visualization project follows this end-to-end cycle. Your report should address every stage below, in roughly this order.

```
[1] Understand the Problem / Business Context
        ↓
[2] Identify Users & Analytical Goals (Domain Task)
        ↓
[3] Understand and Profile the Dataset
        ↓
[4] Data Cleaning / Preparation
        ↓
[5] Data Abstraction (What kind of data is it?)
        ↓
[6] Task Abstraction (What does the user want to DO with the data?)
        ↓
[7] Choose Visual Encodings (Marks & Channels)
        ↓
[8] Select Charts / Idioms
        ↓
[9] Design Dashboard / Narrative Flow
        ↓
[10] Derive Insights & Tell the Story
        ↓
[11] Evaluate, Discuss Limitations, Make Recommendations
```

The workflow is **iterative**: after evaluation, you may loop back to find better data or refine your questions (as shown in the Visualization Workflow diagram from slides).

---

## Section 2: Key Concepts and How They Should Appear in a Report

### 2.1 Why Visualize? (The Core Motivation)

| | |
|---|---|
| **What it is** | Visualization transforms raw data into a form the human visual system can process efficiently. Raw tables are extremely slow to read; charts exploit perceptual shortcuts. |
| **Why it matters** | Anscombe's Quartet proves that four datasets with identical mean, variance, and correlation look completely different when plotted. Statistics alone can mislead; visualization reveals the true shape of data. |
| **In the report** | Briefly justify why visualization is the right approach for your problem. What would be lost if you only showed a table? |
| **Common mistake** | Students skip justification entirely and jump straight to charts. |
| **Review question** | Does the report explain what the visualization helps the user see that they couldn't see in raw data? |

---

### 2.2 The Science of How We See

| | |
|---|---|
| **What it is** | Human visual perception follows predictable rules that should guide design decisions: (1) Eyes jump around, starting top-left/center. (2) Contrast grabs attention first. (3) Working memory holds only 3–4 items at once. (4) The brain seeks meaning (Gestalt: grouping, proximity, similarity). (5) We rely on conventions (red = danger, up = good). |
| **Why it matters** | Violating these rules makes visualizations harder to read, even if technically correct. |
| **In the report** | When you justify design choices (color, layout, ordering), reference these principles. E.g., "We sorted bars in descending order because eyes immediately read the largest value first." |
| **Common mistake** | Using too many colors (overloads working memory), placing the most important metric at the bottom, using red for a positive value. |
| **Review question** | Does each design choice have a perceptual justification? |

---

### 2.3 Data Profiling

| | |
|---|---|
| **What it is** | The process of examining, analyzing, reviewing, and summarizing a dataset to understand its quality. Three types: **Structure Discovery** (Is the data formatted correctly?), **Content Discovery** (Do the values make sense?), **Relationship Discovery** (How does data connect?). |
| **Why it matters** | "Garbage In, Garbage Out" (GIGO). If you build visualizations on bad data, every insight is wrong. Profiling makes data quality visible and traceable. |
| **In the report** | Must include a **profiling table** for every column with: NULL count, Actual count, Completeness %, Cardinality, Uniqueness %, Distinctness %, Min, Max, Mode, AVG, Median, Validity Regex, Validity %. Also a **defect analysis** section. |
| **Common mistake** | Doing profiling only in code and not explaining what the numbers mean. Listing the table without discussing the findings. |
| **Review question** | Does the report interpret the profiling results? Does it name which columns have data quality issues and why this matters for the analysis? |

**The 6 Data Quality Dimensions (DAMA-DMBOK):**

| Dimension | Definition | How to Measure |
|---|---|---|
| **Completeness** | Is all required data present? | % of Null/Blank values |
| **Uniqueness** | Are there duplicates? | % of duplicate rows or IDs |
| **Timeliness** | Is the data up to date? | Time gap between event and availability |
| **Validity** | Does data follow defined rules (format, type, range)? | % of failing records |
| **Accuracy** | Does data reflect the real world? | Requires external reference |
| **Consistency** | Is data the same across systems? | Compare across sources |

**Common Data Defects to Look For:**

| Defect | Example |
|---|---|
| Missing Values | Blank cells (NaN/null) |
| Duplicates | Same ID appearing twice |
| Outliers | Age = 500, Salary = 8,000,000 |
| Invalid Values | Age = -5, Date = 2023-13-01 (month 13) |
| Wrong Data Types | Age stored as text "twenty" |
| Inconsistent Formatting | Dates as '2023-01-01', '01/02/2023', 'Jan 1st 23' |
| Invalid Patterns | Emails like 'bob@invalid', countries as 'USA', 'US', 'United States' |

---

### 2.4 Missing Data Classification

| Type | Definition | How to Handle |
|---|---|---|
| **MCAR** (Missing Completely At Random) | Missing randomly across all observations | Deletion or imputation |
| **MAR** (Missing At Random) | Missing randomly only within sub-samples | Imputation |
| **MNAR** (Missing Not At Random) | Structured missingness — the fact it's missing is informative | Investigate the cause |

**Imputation Methods:**
- Mean/Median/Mode substitution
- LOCF (Last Observation Carried Forward) — for time-series
- Linear Interpolation — for time-series
- K-NN Imputation — borrow from similar rows
- ML Prediction — train a model to predict missing values

---

### 2.5 Data Abstraction

| | |
|---|---|
| **What it is** | Formally describing your dataset in abstract, tool-independent terms. This forces you to think carefully about the nature of your data before picking charts. |
| **Why it matters** | Different data types require different chart types. A categorical attribute should never be mapped to a continuous color scale. A temporal attribute implies a line chart, not a bar chart. |
| **In the report** | Must include an **attribute table** (see template below) and must state: dataset type, dataset availability, item semantic. |
| **Common mistake** | Skipping data abstraction entirely. Describing data informally ("this column is about prices") instead of formally ("Price: Quantitative, Sequential, Continuous"). |
| **Review question** | Has the student formally classified every attribute? Does the attribute type (C/O/Q) match the chart type used? |

**Data Abstraction Components:**

| Component | Options |
|---|---|
| **Data type** (element level) | Item, Attribute, Link, Position, Grid |
| **Dataset type** | Table, Network, Field, Geometry |
| **Dataset availability** | Static (entire dataset available at once), Dynamic (continuously generated stream) |
| **Item semantic** | What does each row represent? (e.g., "each row is one order") |

**Attribute Classification Table (required in every report):**

| Attribute Name | Type (C/O/Q) | Key/Value | Direction | Hierarchical | Continuous/Discrete | Semantic |
|---|---|---|---|---|---|---|
| OrderID | C | Key | — | — | Discrete | Order identifier |
| Price | Q | Value | Sequential | — | Continuous | Price in USD |
| ... | ... | ... | ... | ... | ... | ... |

**Attribute Type Guide:**

| Code | Name | Meaning | Examples |
|---|---|---|---|
| **C** | Categorical (Nominal) | Only equal/not-equal; no ordering | Gender, City, Category |
| **O** | Ordinal | Ordered, but no meaningful arithmetic | T-shirt size (S/M/L), Month |
| **Q** | Quantitative | Ordered + full arithmetic | Price, Revenue, Age |

**Direction (for Q/O attributes):**
- **Sequential**: Homogeneous range (min → max); e.g., Revenue
- **Diverging**: Measured from a midpoint in both directions; e.g., Profit/Loss
- **Cyclic**: Wraps around; e.g., Day of week, Time of day

---

### 2.6 Task Abstraction (Domain Task → Abstract Task)

| | |
|---|---|
| **What it is** | Translating what the user *actually wants to do* (domain-specific language) into abstract analytical tasks. This bridges business needs and visualization design. |
| **Why it matters** | The abstract task drives chart selection. If the task is "compare values," a bar chart is correct. If the task is "find trends," a line chart is correct. Without clear task abstraction, chart choices are arbitrary. |
| **In the report** | Must include at least one **User Story**, a **5-Whys analysis**, an **Inverted Pyramid** structure, and a **3-Tier Logic Chain** per KPI. Must map each chart to a specific abstract task. |
| **Common mistake** | Writing domain tasks only ("The manager wants to know sales") without abstracting them. Not connecting tasks to charts. |
| **Review question** | For each chart, can you state: "This chart supports the task of [Action] on [Target]"? |

**4 Methods for Domain-Task Analysis:**

**Method 1 — User Story Formula:**
```
As a [Role], I need [Metric + Breakdown] so I can [Decision/Action]
```
Example: *As a Store Manager, I need the top 10 slow-moving SKUs by shipping city so I can apply 30–50% discounts to reduce inventory.*

**Method 2 — 5-Whys Drill-Down:**
Keep asking "Why?" until you reach the root cause and formulate a **deep analytical question**.

Example:
- Surface: "Revenue is low."
- Why 1: "Several orders have Price = 0."
- Why 2: "These are Trial/Error orders."
- Why 3: "No automatic validation for these order types."
- Deep Question: "How are Price = 0 orders distributed by Category, PaymentStatus, and ShippingCity, and is the root cause missing validation for Trial/Error orders?"

**Method 3 — Inverted Pyramid (Dashboard Structure):**

| Layer | Time to Read | Content |
|---|---|---|
| **Top** | 5–10 seconds | KPIs, current revenue, % vs target, MoM change, top 3 alerts |
| **Middle** | 30–60 seconds | Context & Trends: revenue trend last 12 months, category/region breakdown, top vs bottom performers |
| **Bottom** | On demand | Details: drill-down table, filtered list, product × store × day |

**Method 4 — 3-Tier Logic Chain (per KPI):**

| Tier | Type | Question |
|---|---|---|
| **Tier 1** | Descriptive | WHAT is happening? (the current status) |
| **Tier 2** | Diagnostic | WHY is it happening? (the cause) |
| **Tier 3** | Prescriptive | NEXT: what action should be taken? |

**Abstract Task Vocabulary (Task = Action + Target):**

*Actions:*
- **Analyze → Consume:** Discover (find unknown patterns), Present (communicate known facts), Enjoy (casual exploration)
- **Analyze → Produce:** Annotate, Record, Derive (create new computed attributes)
- **Search:** Lookup (find known item at known location), Locate (find item at unknown location), Browse (explore known characteristics), Explore (open-ended discovery)
- **Query:** Identify (one target), Compare (multiple targets), Summarize (all data)

*Targets:*
- All data → trends, outliers, features
- Attributes (one) → distribution, extremes
- Attributes (many) → dependency, correlation, similarity

---

### 2.7 Marks and Channels (Visual Encoding)

| | |
|---|---|
| **What it is** | The fundamental building blocks of any chart. A **mark** is a geometric primitive (the shape used). A **channel** is a visual property that encodes a data attribute (how the shape's appearance conveys data). Every chart is a combination of marks + channels. |
| **Why it matters** | Choosing the wrong channel for a data type creates misleading or unreadable charts. Position is the most accurate channel; color hue cannot encode quantity accurately. |
| **In the report** | For each chart, explicitly state: "Mark: [type] / Channels: [list]". Justify why those channels were chosen for those attribute types. |
| **Common mistake** | Using color (hue) to encode a quantitative attribute. Using size for a categorical attribute. Using too many channels on one chart (overloading). |
| **Review question** | Does each chart description state its marks and channels? Do the channels match the attribute types? |

**Mark Types:**

| Mark | Dimensions | Used For |
|---|---|---|
| Points (dots) | 0D | Items, scatter plots; can encode many attributes via size/shape/color |
| Lines | 1D | Trends over time; connections between points |
| Areas | 2D | Distribution, part-to-whole; bars, pie slices, heatmap cells |
| Connection | Link | Pairwise relationships (network edges) |
| Containment | Link | Hierarchical relationships (nesting) |

**Channel Types and Effectiveness (best to worst for quantitative data):**

| Rank | Channel | Best For |
|---|---|---|
| 1 | Position on common scale | Quantitative (most accurate) |
| 2 | Position on unaligned scale | Quantitative |
| 3 | Length (1D size) | Quantitative |
| 4 | Tilt/Angle | Quantitative (less accurate) |
| 5 | Area (2D size) | Quantitative (harder to compare) |
| 6 | Spatial region | Categorical (best identity channel) |
| 7 | Color Hue | Categorical (6–12 categories max) |
| 8 | Luminance / Saturation | Ordered (≤4 bins for luminance, ≤3 for saturation) |
| 9 | Shape | Categorical (limited) |
| 10 | Volume (3D size) | Least accurate — avoid |

**Redundant Encoding:** Using multiple channels to encode the same attribute (e.g., both bar length AND luminance for quantity) sends a stronger message but uses up available channels.

---

### 2.8 Color Usage

| | |
|---|---|
| **What it is** | Color is a visual channel with three components: **Hue** (the pure color — identity channel, for categories), **Saturation** (amount of white mixed in — magnitude channel, for ordered data), **Luminance** (amount of black mixed in — magnitude channel, for ordered data). |
| **Why it matters** | Using the wrong color type misleads the reader. Hue has NO natural ordering, so using rainbow colors to show revenue implies a ranking that doesn't exist. Luminance and saturation have a natural ordering. |
| **In the report** | State which colormap was used for each chart and justify it based on the attribute type. |
| **Common mistake** | Using a rainbow/sequential colormap for categorical data. Using hue to imply quantity. Using too many hues (>12 makes categories indistinguishable). Not considering colorblind-safe palettes. |
| **Review question** | Is the colormap type (categorical/sequential/diverging) matched to the attribute type (categorical/ordered/diverging)? |

**Colormap Selection Guide:**

| Data Type | Use | Example Palette |
|---|---|---|
| Categorical | Categorical colormap (distinct hues) | Set1, Set2, Paired |
| Ordered / Sequential | Sequential colormap (light → dark) | Blues, Reds, YlOrRd |
| Diverging (centered around 0) | Diverging colormap (two hues, white center) | RdBu, PiYG, Spectral |
| Two quantitative variables | Bivariate colormap | — |

**Convention rules to never break:**
- Red = Danger / Bad
- Green = Good / Safe
- Up = More / Better
- Sequential scale from light (low) to dark (high)

---

### 2.9 Chart Selection (Visual Idioms)

| | |
|---|---|
| **What it is** | Each chart type is an "idiom" — a specific combination of data type, mark, channel, and task. Chart choice must be driven by attribute types and analytical tasks, not aesthetics. |
| **Why it matters** | Using a pie chart to compare 15 categories, or a line chart for categorical data, actively misleads the reader. The course frames chart selection as a direct consequence of data abstraction + task abstraction. |
| **In the report** | For each chart, provide: data type → encoding (mark + channels) → task it supports → scale. |
| **Common mistake** | Choosing charts because they "look nice." Using pie charts for more than 5 categories. Using line charts when the X-axis is categorical (not ordered). |
| **Review question** | Can you justify each chart choice based on: (1) attribute types, (2) number of keys, (3) analytical task? |

**Chart Selection Table:**

| Chart Type | Data Requirements | Best Tasks | Scalability |
|---|---|---|---|
| **Scatter Plot** | 2 quantitative values (0 keys) | Find correlation, outliers, distribution, trends | Hundreds of items |
| **Bar Chart** | 1 categorical key + 1 quantitative value | Compare, lookup value; sort by value for best case | 10–100+ categories |
| **Line / Dot Chart** | 1 ordered key + 1 quantitative value | Show trends over time | 100+ items |
| **Heatmap** | 2 keys + 1 quantitative value | Find patterns across two dimensions | Thousands of cells |
| **Scatter Plot Matrix** | Many keys + many values | Find correlations across many pairs | Tens of attributes |
| **Pie / Donut Chart** | 1 categorical key + 1 quantitative value (part-to-whole) | Show proportions | ≤5 categories |
| **Stacked Bar** | 1 categorical key + 1 categorical breakdown + 1 quantitative value | Part-to-whole comparison across groups | Moderate |
| **Bubble Chart** | 2 quantitative values + 1 size attribute | Correlation with a third quantitative dimension | Hundreds |

**Key Rule for Bar Charts (from slides):**
The best case is: **Separated + Aligned + Ordered** (sorted by value, not alphabetically). Alphabetical order makes ranking impossible at a glance.

---

### 2.10 Dashboard Design & Storytelling

| | |
|---|---|
| **What it is** | A dashboard is not a collection of random charts — it is a structured visual narrative organized around the Inverted Pyramid model. Storytelling means guiding the reader from the big picture (KPIs) down to specific explanations and actionable details. |
| **Why it matters** | The human brain sees only 3–4 things at once. A poorly arranged dashboard forces the reader to construct the story themselves. A well-designed dashboard pre-attentively guides the eye to the most important insight. |
| **In the report** | Explain the layout logic: why are certain charts at the top, others in the middle? How does the dashboard flow from overview → context → detail? |
| **Common mistake** | Putting all charts at equal prominence. No clear "hero metric." Forcing the reader to figure out the story themselves. Charts that don't connect to each other. |
| **Review question** | Does the dashboard tell a coherent story from top to bottom? Is there a clear main message the reader gets in the first 10 seconds? |

**Dashboard Design Principles from the Slides:**
- **Perception:** Eyes start top-left, move center-right. Place the most critical KPI there.
- **Contrast:** High-contrast elements grab attention. Use contrast deliberately, not randomly.
- **Working memory limit:** No more than 3–4 elements should compete for attention in one view.
- **Gestalt:** Group related charts spatially. Proximity implies relationship.
- **Conventions:** Never violate color conventions. Red for alerts, green for healthy metrics.

---

### 2.11 Insights and Analytical Interpretation

| | |
|---|---|
| **What it is** | Insights are conclusions derived from the visualizations, stated clearly with supporting evidence. Not descriptions ("the bar is tall") but interpretations ("Electronics generates 62% of total revenue, making it the dominant category"). |
| **Why it matters** | Describing what you see is not analysis. Insight means connecting observations to business implications using the 3-Tier Logic Chain (What → Why → Next). |
| **In the report** | Each key insight must reference a specific chart. Follow the pattern: "Chart X shows [observation]. This means [interpretation]. The recommended action is [prescription]." |
| **Common mistake** | Restating what is visually obvious. Not linking insight to action. Writing generic observations with no specifics. |
| **Review question** | Does every stated insight have a supporting chart? Does every insight lead to a recommendation? |

---

### 2.12 Limitations and Recommendations

| | |
|---|---|
| **What it is** | An honest assessment of what your analysis cannot conclude, why the data may be insufficient, and what further steps would improve the analysis. |
| **Why it matters** | No dataset is perfect. Limitations protect the reader from over-trusting flawed insights. Recommendations demonstrate analytical maturity. |
| **In the report** | List at least 3–5 specific limitations (not vague ones like "the dataset is small"). For each limitation, explain the impact on the analysis. |
| **Common mistake** | Writing "the dataset might have errors" as a limitation — this is too vague. Write: "15% of Price values are 0 (likely data entry errors). Revenue calculations derived from these rows are unreliable, so total revenue may be understated by X%." |
| **Review question** | Are limitations specific and tied to the analysis? Do recommendations directly follow from the findings and limitations? |

---

## Section 3: Report Audit Checklist

Use this checklist to review your report before submission. Check off each item.

### A. Problem Context & Goals

- [ ] The business context is clearly explained (who is the user, what is their role, what decision do they need to make?)
- [ ] At least one well-formed User Story is written using the formula: "As a [Role], I need [Metric + Breakdown] so I can [Decision/Action]"
- [ ] The analytical goals are stated explicitly, not just implied

### B. Dataset Overview

- [ ] The dataset is described (source, number of rows and columns, time period)
- [ ] Each attribute (column) is named and briefly described
- [ ] The meaning of each row (item semantic) is stated (e.g., "each row represents one order")

### C. Data Profiling

- [ ] A full profiling table is present covering: NULL, Actual, Completeness %, Cardinality, Uniqueness %, Distinctness %, Min, Max, Mode, AVG, Median
- [ ] A defect analysis section covers: validity %, top patterns, outliers (IQR)
- [ ] The report interprets the profiling results (does not just list numbers)
- [ ] Missing data is classified (MCAR / MAR / MNAR) for each affected column
- [ ] The handling strategy for each data defect is documented with justification

### D. Data Cleaning

- [ ] Specific cleaning actions are documented (e.g., "Removed duplicate OrderID 101", "Standardized PaymentStatus: 'Payed' → 'Paid'")
- [ ] The cleaned dataset is described (how many rows remain, what changed)
- [ ] Remaining data quality issues after cleaning are acknowledged

### E. Data Abstraction

- [ ] Dataset type is stated (table / network / field / geometry)
- [ ] Dataset availability is stated (static / dynamic)
- [ ] Item semantic is stated (what does one row represent?)
- [ ] An attribute classification table is present with columns: Attribute Name, Type (C/O/Q), Key/Value, Direction, Hierarchical, Continuous/Discrete, Semantic
- [ ] Every attribute in the dataset is classified in this table

### F. Task Abstraction

- [ ] At least one 5-Whys analysis is completed, leading to a "deep question"
- [ ] An Inverted Pyramid structure is described (Top/Middle/Bottom layers)
- [ ] At least two 3-Tier Logic Chains are written (one per key KPI)
- [ ] Each chart in the report is linked to a specific abstract task (Analyze/Search/Query + subtypes)
- [ ] The abstract task vocabulary is used (not just domain-specific language)

### G. Visual Design

- [ ] For each chart, the mark type is explicitly stated
- [ ] For each chart, the channel(s) used are explicitly stated
- [ ] The match between attribute type and channel type is justified
- [ ] Color usage is justified (colormap type matches data type)
- [ ] Charts are ordered by value where appropriate (not alphabetically)
- [ ] No chart uses hue/rainbow color to represent a quantitative attribute
- [ ] Redundant encoding is used where emphasis is needed

### H. Dashboard / Story Flow

- [ ] The dashboard follows the Inverted Pyramid (overview → context → detail)
- [ ] The most important KPI is placed in the most prominent position
- [ ] Related charts are grouped spatially
- [ ] The report explains the layout/navigation logic
- [ ] A reader can understand the main message within 5–10 seconds of seeing the dashboard

### I. Insights

- [ ] Each insight is stated as a full sentence with a specific number or finding
- [ ] Each insight is supported by a specific named chart
- [ ] Insights follow the 3-Tier pattern: What → Why → Next
- [ ] No insight is merely a description of what is visually obvious
- [ ] At least 3–5 actionable insights are stated

### J. Limitations

- [ ] At least 3 specific limitations are listed
- [ ] Each limitation explains its impact on the analysis
- [ ] Recommendations are present and directly follow from the analysis and limitations
- [ ] The recommendations are specific and actionable (not vague)

---

## Section 4: Mapping Template

| Course Concept | What to Look For in the Report | Evidence Needed | Possible Issue if Missing |
|---|---|---|---|
| **Why Visualize** | Justification for using visualization over raw tables | A sentence explaining what charts reveal that tables hide | Reader has no reason to trust that visualization adds value |
| **Perceptual Science** | Design choices reference how humans see | Mention of contrast, saccades, working memory, Gestalt, conventions | Charts may violate perception rules without the author knowing |
| **Data Profiling** | Full profiling table + defect analysis + interpretation | Profiling table with all required metrics; text explaining findings | Reader cannot trust the quality of downstream analysis |
| **Data Quality Dimensions** | Completeness, Uniqueness, Validity, Accuracy, Consistency each assessed | Per-column quality assessment | Unknown data quality risks propagate to charts |
| **Missing Data** | MCAR/MAR/MNAR classification + handling strategy per column | Table of missing columns, type, action taken | Imputation choices may introduce bias that distorts insights |
| **Data Abstraction** | Formal attribute table (Type C/O/Q, Key/Value, Direction, etc.) | Complete attribute classification table | Chart selection becomes arbitrary; wrong chart types used |
| **Dataset Type** | Table / Network / Field / Geometry stated | One sentence | Wrong idiom family chosen for the data structure |
| **Item Semantic** | What one row represents is stated | One sentence ("each row is one order") | Reader cannot interpret the unit of analysis |
| **User Story** | As a [Role], I need [Metric+Breakdown] so I can [Action] | At least one complete User Story | Analytical goals remain vague; charts have no user purpose |
| **5-Whys** | At least one drill-down chain ending in a deep question | Chain of Why 1 → Why 5 → Deep Question | Surface-level analysis only; root causes ignored |
| **Inverted Pyramid** | Dashboard structured as Top (KPIs) / Middle (Trends) / Bottom (Details) | Description of dashboard layers | Dashboard lacks hierarchy; all elements appear equally important |
| **3-Tier Logic Chain** | WHAT → WHY → NEXT for at least 2 KPIs | Written chain per KPI | Insights stop at description; no diagnostic or prescriptive layer |
| **Task Abstraction** | Each chart linked to Analyze/Search/Query + subtypes | Phrase like "this chart supports Compare > Similarity across categories" | Charts exist without analytical purpose |
| **Marks** | Mark type stated for each chart | Per-chart: "Mark: bar (line area)" | Cannot verify if mark is appropriate for the data |
| **Channels** | Channels stated and justified for each chart | Per-chart: "Channels: vertical position (quantity), hue (category)" | Cannot verify if encoding is perceptually appropriate |
| **Channel Effectiveness** | High-ranked channels used for important attributes | Position used for key quantitative values | Key data encoded in low-accuracy channels (e.g., area for exact values) |
| **Color → Hue** | Used only for categorical attributes (≤12 categories) | Justified colormap selection | Hue falsely implies ordering if used for quantitative data |
| **Color → Luminance/Saturation** | Used only for ordered attributes (≤4 / ≤3 bins) | Sequential colormap with limited steps | Too many bins make colors indistinguishable |
| **Colormap Type** | Categorical / Sequential / Diverging matches data type | Colormap named and justified per chart | Mismatched colormap misleads about data relationships |
| **Chart Selection** | Each chart type justified by: data type + number of keys + task | Sentence per chart: "Bar chart used because: 1 categorical key + 1 quantitative value + task is Compare" | Chart choices appear arbitrary or decorative |
| **Bar Chart Ordering** | Bars sorted by value (descending), not alphabetically | Chart shows sorted bars | Alphabetical ordering hides rank — readers cannot compare at a glance |
| **Dashboard Narrative** | Overview → context → detail progression | Section describing layout logic | Dashboard is a random collection of charts without a story |
| **Insights** | Specific, numbered findings referencing charts | "Chart 3 shows Electronics accounts for 62% of revenue. This suggests…" | Analysis remains descriptive; no conclusions drawn |
| **Limitations** | Specific limitations tied to analysis impact | "15% of Price = 0; revenue estimates may be understated" | Insights may be accepted as fact when data quality is suspect |
| **Recommendations** | Actionable steps derived from insights and limitations | "Apply 30–50% discount to slow-moving SKUs in Category Furniture" | Report has no practical value for the stakeholder |

---

## Section 5: Expected Report Structure

Below is the ideal structure for a Data Visualization report based on this course. Use it as a template.

---

### 1. Introduction
- Business context: who is the user, what industry/domain, what problem exists
- Analytical goals: what questions the report answers
- Report overview: brief description of each section

### 2. Dataset Overview
- Source of the dataset
- Number of rows and columns
- Time period covered
- Item semantic: what one row represents
- List of all attributes with brief descriptions

### 3. Data Profiling
- **Statistics table**: NULL, Actual, Completeness %, Cardinality, Uniqueness %, Distinctness %, Min, Max, Mode, AVG, Median, Validity Regex, Validity %
- **Defect analysis table**: Data type, Outliers (IQR), Top 5 patterns per column
- **Quality interpretation**: For each column with issues, explain what the problem is and why it matters
- Summary of data quality score

### 4. Data Cleaning / Preparation
- Table of cleaning actions: Column → Defect Found → Action Taken → Justification
- Missing data: per-column MCAR/MAR/MNAR classification and handling method
- Final dataset description (rows remaining, changes made)
- Remaining known issues after cleaning

### 5. Data Abstraction
- Dataset type and availability
- Item semantic
- Complete attribute classification table (Attribute Name, Type C/O/Q, Key/Value, Direction, Hierarchical, Continuous/Discrete, Semantic)
- Derived/computed attributes (if any), e.g., TotalRevenue = Price × Quantity

### 6. Task Abstraction
- User Story (at least 1, preferably 2–3)
- 5-Whys analysis (at least 1 chain per key business problem)
- Inverted Pyramid: describe the three layers of the dashboard
- 3-Tier Logic Chain (for 2 key KPIs): WHAT → WHY → NEXT
- Abstract task list: map each chart to its Analyze/Search/Query sub-task

### 7. Visualization Design Rationale
- For each chart: mark type, channels used, attribute types encoded, justification
- Color usage: colormap selected and why
- Layout decisions: why charts are placed where they are

### 8. Dashboard / Chart Analysis
- Present each chart with: title, description, key observations
- Group charts according to the Inverted Pyramid (Top → Middle → Bottom)
- Use annotations to guide the reader's attention

### 9. Insights
- Numbered list of insights (3–5 minimum)
- Each insight: observation + interpretation + implication (WHAT → WHY → NEXT)
- Each insight references a specific chart by name/number

### 10. Limitations
- Numbered list of specific limitations
- Each limitation: what the problem is + its impact on the analysis

### 11. Conclusion / Recommendations
- Summary of key findings
- Specific, actionable recommendations derived from the analysis
- Suggested next steps (additional data needed, follow-up analyses)

---

## Quick Reference: Most Common Student Mistakes

| # | Mistake | Correct Approach |
|---|---|---|
| 1 | Data profiling section is just a table with no interpretation | Every metric must be explained in text: "Quantity has outliers at -1 and 1,000,000, likely data entry errors" |
| 2 | Data abstraction section is skipped or too brief | Every attribute must appear in the classification table with Type, Direction, Semantic |
| 3 | Task abstraction is only domain-level ("the manager wants X") | Must use abstract vocabulary: Analyze > Consume > Discover; Query > Compare |
| 4 | Charts have no mark/channel description | Every chart must explicitly state: "Mark: [type], Channels: [list]" |
| 5 | Color hue used for quantitative data | Hue is for categories only. Use sequential (luminance/saturation) for quantities |
| 6 | Bar charts sorted alphabetically | Always sort by value (descending) unless the category order has intrinsic meaning |
| 7 | Dashboard has no logical flow | Follow Inverted Pyramid: KPIs top, trends middle, details bottom |
| 8 | Insights just describe what is visible | Insights must interpret and prescribe: What → Why → Next |
| 9 | Limitations are vague ("the data may have errors") | Limitations must be specific: name the column, quantify the issue, state the impact |
| 10 | Chart type chosen for aesthetics (e.g., pie chart for 15 categories) | Chart type must be justified by: data type + number of keys + analytical task |

---

*Framework extracted from Data Visualization course slides — Chapters 1 (Introduction), 2 (Data Profiling), 3 (Data Abstraction), 4 (Task Abstraction), 5 (Marks & Channels), 6 (Color), 7 (Arrange Tables / Chart Idioms). Reference textbook: Tamara Munzner, Visualization Analysis and Design, AK Peters, 2015.*
