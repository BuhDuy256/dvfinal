# Requirement for Claude - Data Visualization Tasks 5, 6, 7, 8

## Role

You are a senior data visualization expert specializing in Tableau, D3.js, and data visualization idiom design.

I am working on a university Data Visualization final project about Airbnb NYC.

The data has already been cleaned. Do not redo data cleaning unless it is necessary to create calculated fields for visualization.

My responsibility is to complete:

- Domain Task 5
- Domain Task 6
- Domain Task 7
- Domain Task 8

The expected output is not only charts, but also visualization idiom specifications for each chart, following the style of a data visualization report.

---

## Project folder structure

```text
DATA VISUALIZATION_FINAL_PROJECT/
├── data/
│   ├── cleaned_calendar.csv
│   ├── cleaned_listings.csv
│   ├── cleaned_reviews.csv
│   └── neighbourhoods.geojson
├── docs/
│   └── midterm/
│       └── midterm_report.pdf
├── requirement/
│   └── req.md
└── src/
````

---

## Available datasets

## 1. cleaned_listings.csv

Granularity:

```text
1 row = 1 Airbnb listing
```

Columns:

```text
id
host_id
neighbourhood_group_cleansed
neighbourhood_cleansed
latitude
longitude
room_type
price
number_of_reviews
reviews_per_month
review_scores_rating
availability_365
accommodates
price_is_outlier
```

Column meanings:

```text
id: listing ID
host_id: host ID
neighbourhood_group_cleansed: borough / large area group
neighbourhood_cleansed: neighbourhood / smaller area
latitude: listing latitude
longitude: listing longitude
room_type: type of room
price: listing price
number_of_reviews: total number of reviews
reviews_per_month: review frequency per month
review_scores_rating: rating score
availability_365: number of available days in a year
accommodates: maximum number of guests
price_is_outlier: whether the listing price is an outlier
```

Main usage:

```text
Task 5: price distribution by area
Task 6: price outliers and good-value listings
Task 7: cost efficiency per guest
```

---

## 2. cleaned_reviews.csv

Granularity:

```text
1 row = 1 review
```

Columns:

```text
listing_id
date
comments
```

Column meanings:

```text
listing_id: listing ID, foreign key to cleaned_listings.id
date: review date
comments: review text
```

Main usage:

```text
This dataset is not required for my assigned Task 5, 6, 7, 8 unless you want to use it as optional context.
```

---

## 3. cleaned_calendar.csv

Granularity:

```text
1 row = 1 listing per date
```

Columns:

```text
listing_id
date
available
price
minimum_nights
maximum_nights
is_available
is_booked
year
month
price_is_outlier
```

Column meanings:

```text
listing_id: listing ID, foreign key to cleaned_listings.id
date: calendar date
available: raw availability state
price: calendar price, but DO NOT use it because the original report says calendar.price is not reliable / missing
minimum_nights: minimum nights required
maximum_nights: maximum nights allowed
is_available: derived availability state
is_booked: derived booking state, 1 means booked/not available, 0 means available
year: year extracted from date
month: month extracted from date
price_is_outlier: whether the calendar price is an outlier, but avoid using this unless necessary
```

Main usage:

```text
Task 8: occupancy trend and seasonality
```

Important constraint:

```text
Do NOT use cleaned_calendar.price for price analysis.
For price analysis, use cleaned_listings.price only.
For temporal analysis, use is_booked and calculate occupancy rate.
```

---

## 4. neighbourhoods.geojson

This is the spatial polygon dataset.

Possible fields:

```text
neighbourhood
neighbourhood_group
```

Possible join:

```text
cleaned_listings.neighbourhood_cleansed = neighbourhoods.geojson.neighbourhood
```

Use only if needed for map visualization.

---

# My assigned domain tasks

## Task 5 - Price Distribution by Area

Business question:

```text
How does rental price differ across the 5 boroughs of New York?
Which boroughs are more expensive, and which are cheaper?
Are there strong price outliers in specific areas?
```

Relevant dataset:

```text
cleaned_listings.csv
```

Relevant fields:

```text
neighbourhood_group_cleansed
neighbourhood_cleansed
room_type
price
id
price_is_outlier
```

Recommended analytical focus:

```text
Distribution of price
Comparison between boroughs
Median price by borough
Price outliers
```

Expected idioms:

```text
1. Box Plot - Price Distribution by Borough
2. Bar Chart - Median Price by Borough
```

---

## Task 6 - Price Outlier Map and Real Value

Business question:

```text
Where are price outliers located?
Which listings are potentially good deals, meaning relatively low price but high rating?
```

Relevant dataset:

```text
cleaned_listings.csv
```

Relevant fields:

```text
id
latitude
longitude
neighbourhood_group_cleansed
neighbourhood_cleansed
room_type
price
price_is_outlier
review_scores_rating
number_of_reviews
```

Recommended analytical focus:

```text
Spatial distribution of price outliers
High-rating low-price listings
Relationship between price and rating
```

Recommended calculated field:

```text
Good Deal Flag =
IF [price] < { FIXED [neighbourhood_group_cleansed], [room_type] : MEDIAN([price]) }
AND [review_scores_rating] >= 4.8
THEN "Good Deal"
ELSE "Normal"
END
```

If the LOD version is too complex, use this simpler version:

```text
Good Deal Flag =
IF [price] < 154 AND [review_scores_rating] >= 4.8
THEN "Good Deal"
ELSE "Normal"
END
```

Expected idioms:

```text
1. Point Map - Price Outliers by Location
2. Scatter Plot - Price vs Rating for Good Deal Detection
```

---

## Task 7 - Cost Efficiency of Accommodation

Business question:

```text
Which borough or room type provides the best value per guest?
How does price per person change as accommodation capacity increases?
```

Relevant dataset:

```text
cleaned_listings.csv
```

Relevant fields:

```text
id
neighbourhood_group_cleansed
neighbourhood_cleansed
room_type
price
accommodates
```

Required calculated field:

```text
price_per_person =
IF [accommodates] > 0 THEN [price] / [accommodates] END
```

Recommended analytical focus:

```text
Median price per person by borough
Cost efficiency by room type
Relationship between capacity and price per person
```

Expected idioms:

```text
1. Bar Chart - Median Price per Person by Borough
2. Line Chart or Scatter Plot - Accommodates vs Price per Person
```

---

## Task 8 - Seasonality and Booking Opportunity

Business question:

```text
How does occupancy rate change across months?
Which months are high-demand or low-demand?
Does the minimum-night policy affect occupancy opportunity?
```

Relevant dataset:

```text
cleaned_calendar.csv
```

Optional join:

```text
cleaned_calendar.listing_id = cleaned_listings.id
```

Relevant fields:

```text
listing_id
date
year
month
available
is_available
is_booked
minimum_nights
maximum_nights
```

Required calculated field:

```text
occupancy_rate_pct = AVG([is_booked]) * 100
```

Required calculated field for grouping minimum nights:

```text
Minimum Nights Group =
IF [minimum_nights] <= 3 THEN "Short minimum stay"
ELSEIF [minimum_nights] <= 7 THEN "Medium minimum stay"
ELSE "Long minimum stay"
END
```

Recommended analytical focus:

```text
Monthly occupancy trend
High season and low season
Occupancy difference between short, medium, and long minimum-stay policies
```

Expected idioms:

```text
1. Line Chart - Monthly Occupancy Rate
2. Heatmap - Month x Minimum Nights Group
```

---

# Required output

For each domain task, propose exactly 2 visualization idioms.

Since I am responsible for Task 5, 6, 7, and 8, the total expected output is:

```text
Task 5: 2 idioms
Task 6: 2 idioms
Task 7: 2 idioms
Task 8: 2 idioms

Total: 8 idioms
```

For each idiom, use this exact structure:

```text
## Idiom name

### What

- Dataset:
- Fields:
- Attribute types:
  - Categorical:
  - Ordinal:
  - Quantitative:
- Calculated fields, if any:

### Why

- Action:
  - Discover / Explore / Locate / Browse / Compare / Summarize
- Target:
  - Distribution / Trends / Outliers / Features / Dependency / Extremes
- Purpose:

### How

- Mark:
- Channels:
  - X:
  - Y:
  - Color:
  - Size:
  - Text / Label:
  - Tooltip:
  - Filter:

### Tableau steps

Give step-by-step Tableau instructions:

1.
2.
3.
4.
5.

### Expected insight

Explain what pattern this chart is expected to reveal.

### Vietnamese caption for report

Write a short Vietnamese caption that can be pasted below the chart in Google Docs.
```

---

# Summary table requirement

Before writing the detailed idioms, create a summary table with these columns:

```text
Task
Idiom
Dataset
Main fields
Main purpose
Difficulty
```

---

# Important constraints

1. Do not use `cleaned_calendar.price` for price analysis.
2. For price analysis, use `cleaned_listings.price`.
3. For occupancy analysis, use `cleaned_calendar.is_booked`.
4. Do not spend time on data cleaning.
5. The output must be suitable for Tableau implementation.
6. The output must match data visualization theory:

   * What
   * Why
   * How
   * Marks
   * Channels
   * Attribute types: Categorical, Ordinal, Quantitative
7. Write most of the explanation in Vietnamese.
8. Keep explanations practical because I need to finish the assignment quickly.
9. Mention which charts should be made first if time is limited.
10. If you suggest D3.js, keep it optional. Tableau implementation is the priority.

---

# Final deliverables expected from Claude

Please produce:

1. A summary table of the 8 idioms.
2. Detailed specification for each idiom.
3. Tableau calculated fields.
4. Tableau implementation steps.
5. Vietnamese captions and insight comments.
6. Recommended order of implementation from easiest to hardest.
7. Any warnings about fields that should not be used or charts that may be too difficult.

```