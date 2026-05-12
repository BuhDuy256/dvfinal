# Task 5, 6, 7, 8 — Visualization Idiom Specifications

> Dataset chính: `cleaned_listings.csv` (Task 5–7), `cleaned_calendar.csv` (Task 8)
> Không dùng `cleaned_calendar.price` cho phân tích giá.

---

## Calculated Fields — Tạo trước khi làm chart

```
// Task 7
price_per_person =
IF [accommodates] > 0 THEN [price] / [accommodates] END

// Task 8 — occupancy
occupancy_rate_pct = AVG([is_booked]) * 100

// Task 8 — grouping minimum nights
Minimum Nights Group =
IF [minimum_nights] <= 3 THEN "Short minimum stay"
ELSEIF [minimum_nights] <= 7 THEN "Medium minimum stay"
ELSE "Long minimum stay"
END

// Task 6 — LOD version (khuyến nghị)
Good Deal Flag =
IF [price] < { FIXED [neighbourhood_group_cleansed], [room_type] : MEDIAN([price]) }
AND [review_scores_rating] >= 4.8
THEN "Good Deal"
ELSE "Normal"
END

// Task 6 — Simple fallback nếu LOD lỗi
Good Deal Flag (simple) =
IF [price] < 154 AND [review_scores_rating] >= 4.8
THEN "Good Deal"
ELSE "Normal"
END
```

**Cách tạo trong Tableau:** Analysis → Create Calculated Field → đặt tên → paste công thức → OK.

---

## Summary Table — 8 Idioms

| # | Task | Idiom | Dataset | Main fields | Purpose | Difficulty |
|---|------|-------|---------|-------------|---------|------------|
| 1 | 5 | Box Plot — Price by Borough | listings | `neighbourhood_group_cleansed`, `price` | Distribution, outlier detection | Medium |
| 2 | 5 | Bar Chart — Median Price by Borough | listings | `neighbourhood_group_cleansed`, `price` | Compare median price | Easy |
| 3 | 6 | Point Map — Outlier Locations | listings | `latitude`, `longitude`, `price_is_outlier` | Locate spatial outliers | Medium-Hard |
| 4 | 6 | Scatter Plot — Price vs Rating | listings | `price`, `review_scores_rating`, `Good Deal Flag` | Dependency, good deal detection | Medium |
| 5 | 7 | Bar Chart — Price/Person by Borough | listings | `neighbourhood_group_cleansed`, `price_per_person` | Compare cost efficiency | Easy |
| 6 | 7 | Scatter Plot — Capacity vs Price/Person | listings | `accommodates`, `price_per_person`, `room_type` | Trend, dependency | Medium |
| 7 | 8 | Line Chart — Monthly Occupancy | calendar | `month`, `occupancy_rate_pct` | Trend, seasonality | Easy-Medium |
| 8 | 8 | Heatmap — Month × Min Nights Group | calendar | `month`, `Minimum Nights Group`, `occupancy_rate_pct` | Distribution across 2 categorical dims | Medium |

---

## Recommended Order (Dễ → Khó)

```
1. [EASY]        Chart #2  — Bar Chart: Median Price by Borough
2. [EASY]        Chart #5  — Bar Chart: Median Price per Person by Borough
3. [EASY-MED]    Chart #7  — Line Chart: Monthly Occupancy Rate
4. [MEDIUM]      Chart #1  — Box Plot: Price Distribution by Borough
5. [MEDIUM]      Chart #6  — Scatter Plot: Capacity vs Price per Person
6. [MEDIUM]      Chart #4  — Scatter Plot: Price vs Rating (Good Deal)
7. [MEDIUM]      Chart #8  — Heatmap: Month × Min Nights Group
8. [MEDIUM-HARD] Chart #3  — Point Map: Price Outlier Locations
```

---

## Task 5 — Price Distribution by Area

---

### Idiom 1 — Box Plot: Price Distribution by Borough

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `neighbourhood_group_cleansed`, `price`, `room_type`, `price_is_outlier`
- **Attribute types:**
  - Categorical: `neighbourhood_group_cleansed`, `room_type`
  - Quantitative: `price`
- **Calculated fields:** Không cần.

#### Why

- **Action:** Compare, Discover
- **Target:** Distribution, Outliers
- **Purpose:** So sánh distribution của price giữa 5 borough NYC. Phát hiện borough nào có nhiều outlier giá cao.

#### How

- **Mark:** Line (box plot dùng multiple lines: whisker, box, median line)
- **Channels:**
  - X: `neighbourhood_group_cleansed` (categorical, position)
  - Y: `price` (quantitative, position — Tableau tự tính IQR)
  - Color: `room_type` (categorical, hue — breakdown phân phối theo loại phòng trong mỗi borough)
  - Filter: `price_is_outlier = False` để loại extreme outliers khỏi view
  - Tooltip: median, Q1, Q3, min, max, count

#### Tableau steps

1. Kéo `neighbourhood_group_cleansed` vào **Columns**.
2. Kéo `price` vào **Rows**.
3. Trên toolbar: **Show Me** → chọn **Box-and-Whisker Plot**. (Nếu không thấy: right-click `price` trên Rows → chọn **Dimension**.)
4. Kéo `room_type` vào **Color** nếu muốn breakdown theo loại phòng.
5. Kéo `price_is_outlier` vào **Filters** → chọn **False** để ẩn extreme outliers.
6. Format trục Y: right-click → **Format** → Number → Currency ($).
7. Sort borough theo median price: right-click trục X → **Sort** → **Median of price**.

> **Warning:** Box plot trong Tableau yêu cầu disaggregate data. Nếu chart không hiển thị đúng, vào **Analysis → Aggregate Measures → tắt**.

#### Expected insight

Manhattan có median price cao nhất và IQR rộng nhất — nghĩa là giá dao động lớn. Staten Island và Bronx có median thấp hơn đáng kể. Entire home/apt luôn cao hơn Private room trên mọi borough.

#### Vietnamese caption for report

> **Hình X.** Box plot phân phối giá niêm yết theo borough tại NYC. Manhattan có mức giá trung vị cao nhất và nhiều outlier nhất, trong khi Bronx và Staten Island có giá thấp và ổn định hơn.

---

### Idiom 2 — Bar Chart: Median Price by Borough

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `neighbourhood_group_cleansed`, `price`
- **Attribute types:**
  - Categorical: `neighbourhood_group_cleansed`
  - Quantitative: `price` (aggregate: MEDIAN)
- **Calculated fields:** Không cần.

#### Why

- **Action:** Compare, Summarize
- **Target:** Extremes, Distribution (summary level)
- **Purpose:** So sánh nhanh median price giữa 5 borough — dễ đọc hơn box plot khi cần trình bày summary.

#### How

- **Mark:** Bar
- **Channels:**
  - X: `neighbourhood_group_cleansed` (categorical, position)
  - Y: `MEDIAN([price])` (quantitative, length)
  - Color: `neighbourhood_group_cleansed` (categorical, hue)
  - Label: giá trị MEDIAN trên đầu cột
  - Tooltip: median, count listings
  - Filter: `price_is_outlier = False`

#### Tableau steps

1. Kéo `neighbourhood_group_cleansed` vào **Columns**.
2. Kéo `price` vào **Rows**.
3. Right-click `SUM(price)` trên Rows → **Measure** → **Median**.
4. Kéo `neighbourhood_group_cleansed` vào **Color**.
5. Kéo `price_is_outlier` vào **Filters** → chọn **False**.
6. Kéo `MEDIAN(price)` vào **Label** (drag từ Rows xuống Label shelf).
7. Sort descending: click icon sort trên header cột.
8. Format Label: Currency ($), 0 decimal.

#### Expected insight

Manhattan rõ ràng đắt nhất (~$150–200+), Brooklyn ở mức trung bình, còn Bronx / Staten Island là lựa chọn rẻ nhất. Chart này dễ dùng trong executive summary.

#### Vietnamese caption for report

> **Hình X.** Median giá niêm yết theo borough NYC. Manhattan là borough đắt nhất, Bronx là rẻ nhất — phù hợp cho du khách có ngân sách thấp.

---

## Task 6 — Price Outlier Map and Real Value

---

### Idiom 3 — Point Map: Price Outliers by Location

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `latitude`, `longitude`, `price_is_outlier`, `price`, `neighbourhood_group_cleansed`, `room_type`
- **Attribute types:**
  - Categorical: `price_is_outlier`, `neighbourhood_group_cleansed`, `room_type`
  - Quantitative: `price`, `latitude`, `longitude`
- **Calculated fields:** Không cần.

#### Why

- **Action:** Locate, Explore
- **Target:** Outliers, Features (spatial)
- **Purpose:** Xác định vị trí địa lý của các listing có giá bất thường (outlier). Kiểm tra xem outlier tập trung ở khu vực nào.

#### How

- **Mark:** Point (circle)
- **Channels:**
  - X: `longitude` → Tableau tự nhận là geographic
  - Y: `latitude` → Tableau tự nhận là geographic
  - Color: `price_is_outlier` (categorical: True = đỏ, False = xanh)
  - Size: `price` (quantitative — điểm lớn hơn = giá cao hơn)
  - Tooltip: `id`, `price`, `room_type`, `neighbourhood_group_cleansed`, `price_is_outlier`
  - Filter: `room_type` (optional)

#### Tableau steps

1. Kéo `latitude` vào **Rows**, `longitude` vào **Columns**.
2. Tableau sẽ tự chuyển sang Map view. Nếu không: **Show Me → Maps**.
3. Kéo `price_is_outlier` vào **Color** → đổi màu: True = cam/đỏ, False = xanh nhạt.
4. Kéo `price` vào **Size** → adjust size range nhỏ lại (~2–8px) để không overlap.
5. Kéo các field cần thiết vào **Tooltip**: `price`, `room_type`, `neighbourhood_group_cleansed`.
6. (Optional) Thêm `room_type` vào **Filters** để user lọc theo loại phòng.
7. Vào **Map → Map Layers** → bật Street map cho dễ nhìn.

> **Warning:** Nếu có quá nhiều điểm (~50k listings), Tableau sẽ chậm. Có thể filter `price_is_outlier = True` only để focus vào outliers.

#### Expected insight

Outlier giá cao tập trung chủ yếu ở Manhattan (đặc biệt Midtown, Upper East Side) và một số khu vực ven biển Brooklyn. Bronx và Staten Island hầu như không có outlier.

#### Vietnamese caption for report

> **Hình X.** Bản đồ phân bố listing theo giá niêm yết tại NYC. Các điểm màu cam đại diện cho listing có giá bất thường (outlier), tập trung chủ yếu ở Manhattan.

---

### Idiom 4 — Scatter Plot: Price vs Rating (Good Deal Detection)

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `price`, `review_scores_rating`, `Good Deal Flag`, `neighbourhood_group_cleansed`, `room_type`, `number_of_reviews`
- **Attribute types:**
  - Categorical: `Good Deal Flag`, `neighbourhood_group_cleansed`, `room_type`
  - Quantitative: `price`, `review_scores_rating`, `number_of_reviews`
- **Calculated fields:** `Good Deal Flag` (xem phần Calculated Fields ở trên)

#### Why

- **Action:** Discover, Compare
- **Target:** Dependency, Outliers
- **Purpose:** Tìm các listing có giá thấp nhưng rating cao — tức là "good deal" cho du khách. Xem mối quan hệ giữa price và rating.

#### How

- **Mark:** Point (circle)
- **Channels:**
  - X: `price` (quantitative, position)
  - Y: `review_scores_rating` (quantitative, position)
  - Color: `Good Deal Flag` (categorical: "Good Deal" = xanh nổi, "Normal" = xám)
  - Size: `number_of_reviews` (quantitative — listing nhiều review = điểm lớn hơn, đáng tin hơn)
  - Tooltip: `price`, `review_scores_rating`, `room_type`, `neighbourhood_group_cleansed`, `number_of_reviews`
  - Filter: `number_of_reviews >= 5` (loại listing ít review)

#### Tableau steps

1. Tạo calculated field `Good Deal Flag` trước (xem phần đầu).
2. Kéo `price` vào **Columns**, `review_scores_rating` vào **Rows**.
3. Tableau sẽ tự chuyển sang Scatter Plot. Đảm bảo cả hai đều là **Measure** (không phải Dimension).
4. Kéo `Good Deal Flag` vào **Color** → đổi màu: "Good Deal" = màu nổi (xanh lá / cam), "Normal" = xám.
5. Kéo `number_of_reviews` vào **Size**.
6. Kéo `number_of_reviews` vào **Filters** → chọn **Range** → đặt **At least = 5** (giữ listing có ≥ 5 review). Kiểm tra caption Tableau phải ghi "at least 5", không phải "0 to 5".
7. Kéo thêm `price_is_outlier` vào **Filters** → chọn **False** để loại extreme outliers khỏi view.
8. Thêm các field vào **Tooltip**.
9. Thêm Reference Lines:
   - **Analytics pane → Reference Line → Table** → Axis X → Value = Median (price) → dòng dọc phân cách giá cao/thấp.
   - **Analytics pane → Reference Line → Table** → Axis Y → Value = Constant = **4.8** → dòng ngang tại ngưỡng Good Deal Flag (không dùng Average — Average rating ~4.5 không khớp với ngưỡng 4.8 của Good Deal Flag).

#### Expected insight

Góc trên-trái của chart (price thấp, rating cao) là vùng "good deal". Phần lớn listing tốt giá nằm ở Brooklyn và Queens. Manhattan có nhiều điểm bên phải (giá cao) với rating không tương xứng.

#### Vietnamese caption for report

> **Hình X.** Scatter plot giá niêm yết vs. điểm đánh giá. Các điểm màu xanh (Good Deal) là listing có giá dưới median của khu vực nhưng rating ≥ 4.8 — lựa chọn tối ưu cho du khách.

---

## Task 7 — Cost Efficiency of Accommodation

---

### Idiom 5 — Bar Chart: Median Price per Person by Borough

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `neighbourhood_group_cleansed`, `price_per_person`, `room_type`
- **Attribute types:**
  - Categorical: `neighbourhood_group_cleansed`, `room_type`
  - Quantitative: `price_per_person` (aggregate: MEDIAN)
- **Calculated fields:** `price_per_person = IF [accommodates] > 0 THEN [price] / [accommodates] END`

#### Why

- **Action:** Compare, Summarize
- **Target:** Extremes
- **Purpose:** Xác định borough nào có chi phí mỗi người thấp nhất — phù hợp cho nhóm du lịch muốn chia tiền.

#### How

- **Mark:** Bar
- **Channels:**
  - X: `neighbourhood_group_cleansed` (categorical, position)
  - Y: `MEDIAN([price_per_person])` (quantitative, length)
  - Color: `room_type` (categorical — breakdown theo loại phòng, dùng grouped bar)
  - Label: giá trị MEDIAN trên đầu cột
  - Tooltip: median price/person, count, room_type
  - Filter: `price_is_outlier = False`

#### Tableau steps

1. Tạo calculated field `price_per_person` trước.
2. Kéo `neighbourhood_group_cleansed` vào **Columns**.
3. Kéo `price_per_person` vào **Rows** → right-click → **Measure → Median**.
4. Kéo `room_type` vào **Color**.
5. **QUAN TRỌNG — Chuyển sang Grouped bar:** Vào menu **Analysis → Stack Marks → Off**. Nếu không làm bước này, Tableau sẽ tạo Stacked bar (cộng dồn giá trị) thay vì Grouped bar (cột đứng cạnh nhau) — làm sai hoàn toàn mục đích Compare.
6. Kéo `price_is_outlier` vào **Filters** → **False**.
7. Kéo `MEDIAN(price_per_person)` vào **Label**.
8. Format: Currency ($), 0 decimal.
9. Sort borough theo median (tổng) descending.

#### Expected insight

Khi chia theo đầu người, Entire home/apt ở Queens hoặc Brooklyn thường rẻ hơn Private room ở Manhattan. Nhóm du khách đông người sẽ thấy Entire home hiệu quả hơn về chi phí.

#### Vietnamese caption for report

> **Hình X.** Median chi phí mỗi người (price/person) theo borough và room type. Queens và Brooklyn có cost efficiency cao nhất cho nhóm đặt Entire home.

---

### Idiom 6 — Scatter Plot: Accommodates vs Price per Person

#### What

- **Dataset:** `cleaned_listings.csv`
- **Fields:** `accommodates`, `price_per_person`, `room_type`, `neighbourhood_group_cleansed`
- **Attribute types:**
  - Categorical: `room_type`, `neighbourhood_group_cleansed`
  - Quantitative: `accommodates`, `price_per_person`
- **Calculated fields:** `price_per_person`

#### Why

- **Action:** Discover, Explore
- **Target:** Trend, Dependency
- **Purpose:** Kiểm tra xem sức chứa tăng thì price/person có giảm không — tức là listing lớn có "economies of scale" không.

#### How

- **Mark:** Point (circle)
- **Channels:**
  - X: `accommodates` (quantitative, position) — dùng **Dimension** để tránh aggregate
  - Y: `MEDIAN([price_per_person])` (quantitative, position)
  - Color: `room_type` (categorical, hue)
  - Size: count of listings (optional)
  - Tooltip: `accommodates`, median `price_per_person`, `room_type`, count
  - Filter: `price_is_outlier = False`, `accommodates <= 16` (loại outlier capacity)

#### Tableau steps

1. Kéo `accommodates` vào **Columns** → right-click → **Dimension** (để giữ từng giá trị riêng).
2. Kéo `price_per_person` vào **Rows** → right-click → **Measure → Median**.
3. Kéo `room_type` vào **Color**.
4. Kéo `price_is_outlier` vào **Filters** → **False**.
5. Kéo `accommodates` vào **Filters** → Range → 1 đến 16.
6. (Optional) Thêm **Trend Line**: **Analytics pane → Trend Line → Linear** cho mỗi color group.
7. Thêm Tooltip đầy đủ.

#### Expected insight

Thường thấy trend giảm: accommodates tăng thì price/person giảm — Entire home với 4–6 người thường là điểm ngọt nhất về giá. Private room ít thay đổi hơn theo capacity.

#### Vietnamese caption for report

> **Hình X.** Mối quan hệ giữa sức chứa (accommodates) và chi phí mỗi người. Listing Entire home sức chứa 4–6 người cho thấy cost efficiency tốt nhất tại NYC.

---

## Task 8 — Seasonality and Booking Opportunity

---

### Idiom 7 — Line Chart: Monthly Occupancy Rate

#### What

- **Dataset:** `cleaned_calendar.csv`
- **Fields:** `month`, `year`, `is_booked`
- **Attribute types:**
  - Ordinal: `month` (tháng 1–12, có thứ tự)
  - Categorical: `year`
  - Quantitative: `occupancy_rate_pct = AVG([is_booked]) * 100`
- **Calculated fields:** `occupancy_rate_pct`

#### Why

- **Action:** Discover, Browse
- **Target:** Trends, Extremes (high season / low season)
- **Purpose:** Xác định tháng nào có occupancy cao (high season) và thấp (low season) tại NYC Airbnb.

#### How

- **Mark:** Line
- **Channels:**
  - X: `month` (ordinal, position — axis tháng 1–12)
  - Y: `occupancy_rate_pct` (quantitative, position)
  - Color: `year` (categorical — so sánh năm 2024 vs 2025 nếu data có nhiều năm)
  - Label: giá trị % tại điểm peak (optional)
  - Tooltip: `month`, `year`, `occupancy_rate_pct`
  - Filter: `year` (nếu muốn focus 1 năm)

#### Tableau steps

1. Tạo calculated field `occupancy_rate_pct = AVG([is_booked]) * 100`.
2. Kéo `month` vào **Columns** → right-click → **Discrete** (để hiện 1, 2, 3... thay vì continuous).
3. Kéo `occupancy_rate_pct` vào **Rows**.
4. Tableau tự nhận dạng Line chart. Nếu không: **Show Me → Lines (discrete)**.
5. **QUAN TRỌNG — Year phải là Discrete:** Right-click `year` trong Data pane → **Convert to Discrete** (hoặc right-click pill `year` trên Color shelf → **Discrete**). Sau đó kéo `year` vào **Color**. Nếu `year` vẫn là Continuous, Tableau tạo gradient 1 đường thay vì 2 đường màu riêng biệt — không so sánh được seasonality giữa 2 năm.
6. Format trục Y: Percentage, 1 decimal.
7. Đặt tên trục: right-click → **Edit Axis** → Title = "Occupancy Rate (%)".
8. Thêm **Reference Line** tại mức 50% để dễ so sánh.

#### Expected insight

NYC Airbnb thường có occupancy cao vào mùa hè (tháng 6–9) và dịp lễ cuối năm. Tháng 1–2 thường là thấp điểm. Data có thể cho thấy trend tăng dần từ 2024 sang 2025.

#### Vietnamese caption for report

> **Hình X.** Tỷ lệ lấp đầy (occupancy rate) theo tháng tại NYC. Mùa hè (tháng 6–9) là high season rõ rệt, tháng 1–2 là low season.

---

### Idiom 8 — Heatmap: Month × Minimum Nights Group

#### What

- **Dataset:** `cleaned_calendar.csv`
- **Fields:** `month`, `minimum_nights`, `Minimum Nights Group`, `is_booked`
- **Attribute types:**
  - Ordinal: `month` (tháng 1–12)
  - Categorical: `Minimum Nights Group` ("Short", "Medium", "Long")
  - Quantitative: `occupancy_rate_pct`
- **Calculated fields:** `occupancy_rate_pct`, `Minimum Nights Group`

#### Why

- **Action:** Discover, Compare
- **Target:** Distribution, Dependency
- **Purpose:** Xem chính sách minimum nights ảnh hưởng đến occupancy rate như thế nào theo từng tháng. Phát hiện pattern: tháng cao điểm thì policy nào được ưa chuộng hơn?

#### How

- **Mark:** Square (cell)
- **Channels:**
  - X: `month` (ordinal, position)
  - Y: `Minimum Nights Group` (categorical, position)
  - Color: `occupancy_rate_pct` (quantitative, sequential color — đậm = cao)
  - Label: giá trị % trong mỗi ô (optional, nếu không quá nhỏ)
  - Tooltip: `month`, `Minimum Nights Group`, `occupancy_rate_pct`

#### Tableau steps

1. Tạo cả hai calculated fields: `occupancy_rate_pct` và `Minimum Nights Group`.
2. Kéo `month` vào **Columns** → right-click → **Discrete**.
3. Kéo `Minimum Nights Group` vào **Rows**.
4. Kéo `occupancy_rate_pct` vào **Color**.
5. **Show Me → Text Tables** → sau đó đổi Mark type thành **Square** (trong dropdown Mark type).
6. Điều chỉnh màu: **Edit Colors** → chọn sequential palette (ví dụ: Blue → đậm dần theo occupancy cao).
7. (Optional) Kéo `occupancy_rate_pct` vào **Label** để hiện số trong từng ô.
8. Sort thủ công theo thứ tự logic: right-click `Minimum Nights Group` trên Rows → **Sort** → **Manual** → kéo thứ tự từ trên xuống: **Short minimum stay → Medium minimum stay → Long minimum stay**. (Mặc định Tableau sort alphabetical → Long trên cùng, không đúng thứ tự nghiệp vụ.)

> **Tip:** Nếu heatmap ra màu không đẹp, click **Edit Colors → Advanced** → set start = 0%, end = 100%.

#### Expected insight

Short minimum stay có occupancy cao hơn ổn định quanh năm. Long minimum stay có occupancy thấp hơn nhưng có thể tăng vào mùa hè khi du khách ở dài ngày hơn. Pattern này giúp host chọn policy phù hợp theo mùa.

#### Vietnamese caption for report

> **Hình X.** Heatmap tỷ lệ lấp đầy theo tháng và chính sách số đêm tối thiểu (minimum nights). Short stay linh hoạt hơn và có occupancy ổn định hơn quanh năm.

---

## Final Checklist — Thứ tự làm chart

Đánh dấu khi hoàn thành:

```
Phase 1 — Calculated Fields (làm trước tất cả):
[ ] price_per_person
[ ] occupancy_rate_pct
[ ] Minimum Nights Group
[ ] Good Deal Flag

Phase 2 — Easy charts (làm trước):
[ ] Chart #2: Bar Chart — Median Price by Borough           (Task 5)
[ ] Chart #5: Bar Chart — Median Price per Person by Borough (Task 7)
[ ] Chart #7: Line Chart — Monthly Occupancy Rate           (Task 8)

Phase 3 — Medium charts:
[ ] Chart #1: Box Plot — Price Distribution by Borough      (Task 5)
[ ] Chart #6: Scatter Plot — Accommodates vs Price/Person   (Task 7)
[ ] Chart #4: Scatter Plot — Price vs Rating (Good Deal)    (Task 6)
[ ] Chart #8: Heatmap — Month × Min Nights Group            (Task 8)

Phase 4 — Map (làm cuối):
[ ] Chart #3: Point Map — Price Outlier Locations           (Task 6)
```

---

## Warnings

| Vấn đề | Giải thích |
|--------|-----------|
| Không dùng `calendar.price` | Field này thiếu nhiều, không reliable. Dùng `listings.price` cho phân tích giá. |
| Box plot cần disaggregate | Vào **Analysis → Aggregate Measures → tắt** nếu box plot không hiển thị đúng. |
| Good Deal Flag LOD có thể lỗi | Nếu Tableau báo lỗi LOD, dùng simple fallback: `price < 154 AND rating >= 4.8`. |
| Point Map chậm khi nhiều điểm | Filter `price_is_outlier = True` hoặc sample data nếu Tableau lag. |
| `month` phải là Discrete | Nếu để Continuous, Tableau vẽ sai trục. Luôn right-click → Discrete. |
| Task 7.1: Stacked vs Grouped bar | Sau khi kéo `room_type` vào Color, BẮT BUỘC vào **Analysis → Stack Marks → Off**. Nếu quên, chart sẽ là Stacked bar — cộng dồn giá trị, không compare được từng room type. |
| Task 8.1: Year phải là Discrete | Nếu `year` là Continuous, Tableau tạo 1 đường gradient thay vì 2 đường màu riêng. Right-click `year` → **Discrete** trước khi kéo vào Color. |
| Task 6.2: Filter number_of_reviews | Filter phải là "At least = 5" (giữ ≥5 review). Nếu set "0 to 5" sẽ giữ listing ÍT review nhất — ngược chiều hoàn toàn. |
| Task 6.2: Reference line rating | Dùng constant = **4.8** cho trục Y (khớp với Good Deal Flag threshold), không dùng Average (~4.5). |
