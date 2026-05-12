# BÁO CÁO PHÂN TÍCH DỮ LIỆU AIRBNB NEW YORK CITY

**Task 5, 6, 7, 8 — Visualization Idiom Analysis**

---

## 1. Tổng quan tập dữ liệu và Data Profiling

### 1.1. Giới thiệu và câu hỏi kinh doanh

Tập dữ liệu được sử dụng trong báo cáo này được lấy từ **Inside Airbnb** — nguồn dữ liệu công khai cung cấp thông tin về các listing Airbnb tại thành phố New York (NYC). Dữ liệu bao gồm thông tin giá niêm yết, loại phòng, vị trí địa lý, sức chứa, chính sách đặt phòng, đánh giá khách hàng và lịch đặt phòng.

**User Story tổng quát:**

*"As a traveler planning a trip to New York City, I need to understand how Airbnb listing prices vary by borough and room type, identify good-value listings, optimize per-person cost for group travel, and identify the best booking season — so that I can make informed accommodation decisions that maximize value and minimize cost."*

Báo cáo tập trung vào 4 nhóm câu hỏi phân tích:

| Task | Câu hỏi phân tích chính |
|---|---|
| **Task 5** | Giá niêm yết phân bổ như thế nào theo từng borough? Loại phòng ảnh hưởng thế nào đến phân phối giá? |
| **Task 6** | Listing nào có giá bất thường (outlier)? Listing nào có giá thấp nhưng đánh giá cao (good deal)? |
| **Task 7** | Borough và loại phòng nào có chi phí mỗi người thấp nhất? Sức chứa tác động thế nào đến giá/người? |
| **Task 8** | Tỷ lệ lấp đầy thay đổi như thế nào theo mùa? Chính sách minimum nights ảnh hưởng thế nào? |

---

### 1.2. Mô tả tập dữ liệu

| Thông số | Chi tiết |
|---|---|
| **Nguồn** | Inside Airbnb — New York City |
| **Loại dataset** | Table (flat table) |
| **Dataset availability** | Static (snapshot tại thời điểm thu thập) |
| **Item semantic** | Mỗi dòng đại diện cho một listing Airbnb tại NYC |
| **Số lượng listing** | ~21,000 listing |
| **Thời gian dữ liệu đặt phòng** | 2025 – 2026 |
| **Khu vực** | 5 borough: Manhattan, Brooklyn, Queens, Bronx, Staten Island |
| **Số loại phòng** | 4: Entire home/apt, Private room, Shared room, Hotel room |

**Các thuộc tính chính được sử dụng trong phân tích:**

| Tên thuộc tính | Kiểu dữ liệu | Phân loại (C/O/Q) | Hướng | Characteristic | Ngữ nghĩa |
|---|---|---|---|---|---|
| neighbourhood_group_cleansed | String | C (Categorical) | — | Discrete | Khu vực hành chính (5 borough NYC) |
| room_type | String | C (Categorical) | — | Discrete | Loại phòng (Entire home/apt, Private room, Shared room, Hotel room) |
| price | Float | Q (Quantitative) | sequential | Continuous | Giá niêm yết mỗi đêm (USD) |
| latitude | Float | Q (Geographic) | — | Continuous | Vĩ độ địa lý của listing |
| longitude | Float | Q (Geographic) | — | Continuous | Kinh độ địa lý của listing |
| review_scores_rating | Float | Q (Quantitative) | sequential | Continuous | Điểm đánh giá tổng hợp (thang 0–5) |
| number_of_reviews | Integer | Q (Quantitative) | sequential | Discrete | Tổng số lượt đánh giá |
| accommodates | Integer | Q (Quantitative) | sequential | Discrete | Sức chứa tối đa (số người, phạm vi: 1–16) |
| minimum_nights | Integer | Q (Quantitative) | sequential | Discrete | Số đêm tối thiểu bắt buộc theo chính sách host |
| date (lịch đặt phòng) | Date | O (Ordinal) | sequential | Discrete | Ngày trong lịch (available/booked), dùng để tính occupancy |

---

### 1.3. Data Profiling

#### 1.3.1. Phát hiện chất lượng dữ liệu trên các thuộc tính chính

| Thuộc tính | Loại | Completeness | Cardinality | Phạm vi giá trị | Vấn đề phát hiện | Hành động xử lý |
|---|---|---|---|---|---|---|
| neighbourhood_group_cleansed | C | Cao | 5 (borough) | — | Không có vấn đề | Giữ nguyên |
| room_type | C | Cao | 4 loại | — | Không có vấn đề | Giữ nguyên |
| price | Q | Cao | Rất nhiều | $0 – $10,000+ | **Outlier:** giá = $0 (lỗi dữ liệu), giá cực cao (luxury listing) | Tạo field `price_is_outlier` bằng IQR; filter trong phân tích phân phối |
| review_scores_rating | Q | Trung bình | Nhiều giá trị | 0 – 5 | **Missing:** listing mới chưa có đánh giá → NULL | Filter: number_of_reviews ≥ 5 trong Task 6.2 |
| number_of_reviews | Q | Cao | Nhiều giá trị | 0 – hàng trăm | Listing 0 review không đáng tin cậy để đánh giá chất lượng | Filter: ≥ 5 trong phân tích Good Deal |
| accommodates | Q | Cao | 16 giá trị | 1 – 16 (sau lọc) | **Outlier:** accommodates > 16 (listing thương mại đặc biệt) | Filter: ≤ 16 trong Task 7.2 |
| minimum_nights | Q | Cao | Nhiều giá trị | 1 – hàng trăm | Phân tán rộng, khó phân tích dạng raw | Binning thành 3 nhóm: Short/Medium/Long stay |

#### 1.3.2. Computed Fields (Derived Attributes)

Để trả lời các câu hỏi phân tích, các trường tính toán sau được tạo ra từ dữ liệu gốc:

| Computed Field | Công thức / Phương pháp | Mục đích sử dụng |
|---|---|---|
| `price_is_outlier` | IQR method trên `price`: True nếu price < Q1 − 1.5×IQR hoặc price > Q3 + 1.5×IQR | Đánh dấu listing có giá bất thường để lọc hoặc phân tích riêng (Task 5, 6, 7) |
| `price_per_person` | price / accommodates | Đo lường chi phí theo đầu người để so sánh hiệu quả chi phí nhóm (Task 7) |
| `good_deal_flag` | "Good Deal" nếu price < FIXED LOD MEDIAN(price) theo borough × room_type VÀ review_scores_rating ≥ 4.8; "Normal": còn lại | Nhận diện listing vừa rẻ vừa chất lượng cao — ngưỡng 4.8 tương ứng top 20% rating (Task 6.2) |
| `occupancy_rate_pct` | AVG(is_booked) × 100 | Tỷ lệ lấp đầy theo phần trăm (Task 8) |
| `minimum_nights_group` | Binning: Short (≤3), Medium (4–7), Long (>7) | Phân loại chính sách đặt phòng để phân tích theo nhóm (Task 8.2) |

#### 1.3.3. Quyết định xử lý dữ liệu và lý do

**1. Outlier giá (price_is_outlier):**
Listing có giá = $0 nhiều khả năng là lỗi nhập liệu hoặc listing thử nghiệm. Listing có giá cực cao (>$1,000+/đêm) là các luxury property không đại diện cho phân khúc phổ thông. Hai nhóm này nếu giữ lại sẽ kéo lệch phân phối giá, làm median và IQR mất tính đại diện. **Giải pháp:** áp dụng IQR filter cho Task 5, 7 để hiển thị phân phối thực tế; đồng thời giữ lại outlier cho Task 6 để phân tích vị trí và đặc điểm của chúng.

**2. Lọc listing ít đánh giá (number_of_reviews ≥ 5):**
Listing có ít review không cung cấp đủ bằng chứng về chất lượng. Điểm đánh giá từ 1–2 lần không đủ tin cậy thống kê. **Giải pháp:** chỉ phân tích Good Deal trên listing đã được đánh giá ≥ 5 lần.

**3. Giới hạn sức chứa (accommodates ≤ 16):**
Listing với sức chứa > 16 người là các property thương mại đặc biệt, không đại diện cho nhu cầu thông thường của khách du lịch. Loại bỏ để phân tích trend sức chứa vs. giá/người có ý nghĩa hơn.

**4. Binning minimum_nights:**
Phân tích occupancy theo giá trị minimum_nights thô sẽ tạo ra quá nhiều cột trong heatmap, gây clutter và khó nhận diện pattern. Binning thành 3 nhóm (Short/Medium/Long) giúp heatmap dễ đọc và phản ánh 3 chiến lược host khác nhau.

---

## Task 5 — Phân tích Phân phối Giá theo Khu vực (Price Distribution by Area)

**Câu hỏi nghiệp vụ (User Story):**
*"As a budget-conscious traveler, I need to know the price distribution and median price across 5 NYC boroughs by room type — so that I can choose a borough that fits my budget and understand how much price variation to expect within each area."*

**5-Whys drill-down:**
- *Surface:* "Giá Airbnb ở New York rất đắt."
- *Why 1:* Manhattan đắt hơn nhiều so với các borough khác vì vị trí trung tâm, gần Times Square, Central Park, khu tài chính.
- *Why 2:* Chi phí vận hành của host ở Manhattan cao hơn gấp đôi so với Bronx.
- *Why 3:* Cầu cao từ du khách quốc tế tập trung vào Manhattan làm host có thể nâng giá mà vẫn có booking.
- *Deep question:* *"Phân phối giá và biên độ dao động IQR tại từng borough ra sao, và loại phòng ảnh hưởng như thế nào đến cấu trúc phân phối đó?"*

---

### 5.0. Data Abstraction và Task Abstraction

#### 5.0.1. Data Abstraction

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một listing Airbnb tại NYC (chứa thông tin giá niêm yết, loại phòng, borough) |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| neighbourhood_group_cleansed (Borough) | categorical | — | Discrete | Khu vực hành chính — 5 borough NYC | ✓ | |
| price | quantitative | sequential | Continuous | Giá niêm yết mỗi đêm (USD); sau khi lọc price_is_outlier = False | | ✓ |
| room_type | categorical | — | Discrete | Loại phòng (Entire home/apt, Private room, Shared room, Hotel room) | | ✓ |

#### 5.0.2. Task Abstraction

**produce (derive) → compare → summarize**

- **Produce (derive):** Tính MEDIAN(price), Q1, Q3, IQR, min/max whisker theo từng tổ hợp borough × room_type. Tạo computed field `price_is_outlier` bằng IQR và áp dụng filter `price_is_outlier = False` để loại extreme outliers.
- **Compare:** So sánh phân phối giá đầy đủ (box IQR, whisker, median) giữa 5 borough NYC. Phát hiện sự phân tầng giá theo room type.
- **Summarize:** Tóm tắt median giá của từng borough thành một số đại diện dễ đọc (bar chart), hỗ trợ du khách quyết định nhanh borough phù hợp ngân sách.

---

### 5.1. Biểu đồ 1: Phân phối giá niêm yết theo borough (Box-and-Whisker Plot)

#### A. Idiom

| **Idiom** | **Box-and-Whisker Plot** |
|---|---|
| **What** | Borough/Neighbourhood_group_cleansed: Categorical<br>Price: Quantitative<br>Room Type: Categorical |
| **How — Encode** | Mark: Line (box plot — whisker, hộp IQR, đường median)<br>Channel:<br>— PosX: Borough (Categorical, position — phân biệt 5 borough)<br>— PosY: Price (Quantitative, position — Tableau tính IQR tự động)<br>— Hue Color: Room Type (Categorical — phân biệt loại phòng) |
| **How — Manipulate** | Selection: hover để xem chi tiết (median, Q1, Q3, min, max, count) |
| **How — Facet** | — |
| **How — Reduce** | Filter: price_is_outlier = False (loại extreme outliers khỏi view) |
| **Why** | **compare → discover**<br>So sánh phân phối giá giữa 5 borough NYC. Phát hiện outlier và biên độ dao động giá (IQR) theo từng borough và loại phòng. Box plot được chọn vì đây là idiom duy nhất hiển thị đầy đủ phân phối (Q1, median, Q3, whiskers) — bar chart chỉ cho median, histogram chỉ cho 1 nhóm. |
| **Scale** | Key: 5 (borough)<br>Color key: 4 (room type)<br>Items: ~21,000 listing (sau lọc) |

![Hình 5.1. Box plot phân phối giá niêm yết theo borough tại NYC](../docs/tableau/Task 5.1 - Price Distribution by Borough.png)

*Hình 5.1. Box plot phân phối giá niêm yết theo borough tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- Thuộc tính sử dụng: Borough (C), Price (Q), Room Type (C).
- PosX (vị trí ngang): phân biệt 5 borough → phù hợp thuộc tính Categorical (C). Spatial region là channel hiệu quả nhất cho categorical attribute.
- PosY (vị trí dọc): thể hiện phạm vi phân phối giá (Q1, Median, Q3, whiskers) → phù hợp thuộc tính Quantitative (Q). Position on common scale là channel chính xác nhất cho quantitative.
- Hue Color: phân biệt loại phòng → phù hợp thuộc tính Categorical (C). Số màu = 4 ≤ 7 → nằm trong giới hạn discriminability của HUE channel.

Kết luận: Các channel được áp dụng đúng với bản chất dữ liệu. Box plot là idiom chuẩn mực nhất để biểu diễn phân phối dữ liệu liên tục theo nhóm — đặc biệt khi cần so sánh IQR (biên độ dao động) chứ không chỉ median.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Kênh PosY (Position on common scale) là kênh chính xác nhất theo channel effectiveness ranking của slide — xếp hạng 1 trong hierarchy. Người xem có thể ước lượng tương đối chính xác khoảng cách giá giữa các borough. Kênh Hue Color dùng cho categorical không liên quan đến sai số định lượng.
- **Discriminability:** 4 màu (Hue) cho 4 room type trong phạm vi ≤ 7 → mắt người phân biệt hoàn toàn tốt. Whiskers và box IQR hiển thị rõ ràng trên nền trắng. Các outlier dưới dạng điểm tròn (Circle) dễ nhận diện.
- **Separability:** Kênh PosX, PosY và Color tách biệt hoàn toàn. Filter price_is_outlier = False loại bỏ extreme outliers giúp chart dễ đọc hơn; nếu không lọc, whiskers sẽ kéo dài cực đoan và hộp IQR trở nên không đọc được.

#### C. Phân tích biểu đồ

- **Manhattan** có median price cao nhất (~$150–200) và IQR rộng nhất, cho thấy mức độ biến động giá rất lớn — tồn tại cả phân khúc bình dân lẫn cao cấp trong cùng một borough.
- **Bronx và Staten Island** có IQR hẹp và median thấp (~$92–99), phản ánh thị trường giá ổn định, ít phân hóa — phù hợp với du khách cần ngân sách có thể dự đoán trước.
- **Loại phòng Entire home/apt** luôn có box cao hơn Private room ở mọi borough, khẳng định sự phân tầng giá theo loại phòng là nhất quán trên toàn thành phố.
- **Khuyến nghị:** Du khách ngân sách trung bình nên cân nhắc Brooklyn — vị trí gần Manhattan nhưng median giá thấp hơn đáng kể.

---

### 5.2. Biểu đồ 2: Median giá niêm yết theo borough (Bar Chart)

#### A. Idiom

| **Idiom** | **Bar Chart** |
|---|---|
| **What** | Borough/Neighbourhood_group_cleansed: Categorical<br>Median Price: Quantitative (aggregate: MEDIAN) |
| **How — Encode** | Mark: Bar<br>Channel:<br>— PosX: Borough (Categorical, position)<br>— PosY: MEDIAN(Price) (Quantitative, length — chiều dài cột từ gốc 0)<br>— Hue Color: Borough (Categorical — phân biệt từng borough)<br>— Label: giá trị MEDIAN trên đầu cột |
| **How — Manipulate** | Selection: hover để xem median chính xác theo borough |
| **How — Facet** | — |
| **How — Reduce** | Filter: price_is_outlier = False |
| **Why** | **compare → summarize**<br>So sánh median giá giữa 5 borough NYC. Tóm tắt nhanh mức giá trung tâm của từng khu vực. Bar chart được chọn (không phải pie hay radar) vì mục tiêu là so sánh giá trị tuyệt đối giữa các nhóm, và Length là channel chính xác nhất cho quantitative attribute. Bars sắp xếp descending — best case cho comparison. |
| **Scale** | Key: 5 (borough)<br>Items: ~21,000 listing (sau lọc) |

![Hình 5.2. Median giá niêm yết theo borough NYC](../docs/tableau/Task 5.2 - Median Price by Borough.png)

*Hình 5.2. Median giá niêm yết theo borough NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX: phân biệt borough (C) → đúng.
- PosY (Length từ gốc 0): thể hiện độ lớn MEDIAN Price (Q) → đúng — Length là channel phù hợp nhất cho Q, và baseline = 0 là bắt buộc để length channel có ý nghĩa chính xác.
- Hue Color: phân biệt borough (C) → đúng. Redundant encoding (cả PosX lẫn Color encode Borough) gửi thông điệp mạnh hơn.

Kết luận: Mọi channel đều phù hợp và đúng với bản chất dữ liệu.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Kênh Length (chiều dài cột từ gốc 0) xếp hạng thứ 3 trong channel effectiveness ranking (sau Position on common scale và Position on unaligned scale) — độ chính xác tốt. Label số ở đầu cột loại bỏ hoàn toàn sai số cảm nhận thị giác.
- **Discriminability:** 5 cột màu khác nhau, phân cách rõ ràng, sort descending giúp so sánh nhanh từ đắt đến rẻ.
- **Separability:** PosX, PosY và Color tách biệt hoàn toàn.

#### C. Phân tích biểu đồ

- **Manhattan ($200)** đắt hơn gấp đôi so với Bronx ($93) — mức chênh lệch rất lớn, cho thấy sự phân cực giá rõ rệt theo vị trí địa lý tại NYC.
- **Brooklyn ($129)** đứng thứ hai — lựa chọn cân bằng giữa vị trí và chi phí, rẻ hơn Manhattan $71/đêm.
- **Queens ($100), Staten Island ($99) và Bronx ($93)** có median tương đương nhau — phù hợp cho du khách ngân sách thấp, chấp nhận di chuyển xa hơn.
- **Khuyến nghị:** Với nhóm du khách muốn cân bằng giữa tiện lợi và tiết kiệm, Brooklyn là lựa chọn tối ưu; với ngân sách tối thiểu, Queens hoặc Bronx phù hợp nhất.

---

## Task 6 — Phân tích Giá Bất thường và Phát hiện Giá trị Tốt (Price Outlier & Real Value)

**Câu hỏi nghiệp vụ (User Story):**
*"As a traveler, I need to identify which listings have abnormal prices and where they are located — and also find listings with low price but high rating (good deals) — so that I can avoid overpriced listings and book the best value accommodation."*

**5-Whys drill-down:**
- *Surface:* "Nhiều listing có giá bất thường trong dataset."
- *Why 1:* Một số listing có giá = $0 hoặc giá rất cao (>$1,000+/đêm).
- *Why 2:* Giá = $0 thường là lỗi nhập liệu; giá cực cao tập trung ở Manhattan luxury segment.
- *Why 3:* Host ở Manhattan có thể định giá tùy ý vì cầu cao từ khách quốc tế.
- *Deep question:* *"Giá bất thường phân bố ở khu vực nào trên bản đồ NYC? Và trong tập listing có giá bình thường, tập hợp nào vừa rẻ vừa có rating cao để du khách ưu tiên?"*

---

### 6.0. Data Abstraction và Task Abstraction

#### 6.0.1. Data Abstraction — Biểu đồ 6.1 (Point Map)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một listing Airbnb với tọa độ địa lý và nhãn giá bất thường |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| longitude | quantitative (Geographic) | — | Continuous | Kinh độ địa lý của listing | ✓ | |
| latitude | quantitative (Geographic) | — | Continuous | Vĩ độ địa lý của listing | ✓ | |
| price_is_outlier (derived) | categorical | — | Discrete | True = giá bất thường (IQR method); False = bình thường | | ✓ |
| price | quantitative | sequential | Continuous | Giá niêm yết mỗi đêm (USD) — encode Size | | ✓ |
| room_type | categorical | — | Discrete | Loại phòng | | ✓ |

#### 6.0.2. Data Abstraction — Biểu đồ 6.2 (Scatter Plot Good Deal)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một listing đã được đánh giá ≥ 5 lần, chứa thông tin giá và rating |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| price | quantitative | sequential | Continuous | Giá niêm yết mỗi đêm (USD) | ✓ | |
| review_scores_rating | quantitative | sequential | Continuous | Điểm đánh giá tổng hợp (0–5) | ✓ | |
| good_deal_flag (derived) | categorical | — | Discrete | "Good Deal": price < LOD MEDIAN(price) per borough×room_type VÀ rating ≥ 4.8; "Normal": còn lại | | ✓ |
| number_of_reviews | quantitative | sequential | Discrete | Số lượt đánh giá — encode Size (proxy cho độ tin cậy) | | ✓ |

#### 6.0.3. Task Abstraction

**Biểu đồ 6.1:** produce (derive) → locate → explore

- **Produce (derive):** Tạo computed field `price_is_outlier` bằng IQR áp dụng trên toàn bộ tập price.
- **Locate:** Xác định vị trí địa lý chính xác (latitude/longitude) của listing có giá bất thường trên bản đồ NYC.
- **Explore:** Khám phá mối quan hệ giữa vị trí không gian và tính chất bất thường của giá — borough nào tập trung nhiều outlier nhất?

**Biểu đồ 6.2:** produce (derive) → discover → compare

- **Produce (derive):** Tạo `good_deal_flag` và Reference Lines (median price dọc, constant 4.8 ngang) chia scatter plot thành 4 góc phần tư — góc trên trái = "rẻ và chất lượng cao".
- **Discover:** Phát hiện mối quan hệ (dependency) giữa price và rating — liệu listing rẻ hơn có rating thấp hơn không?
- **Compare:** So sánh listing "Good Deal" với listing bình thường — xác định đặc điểm và vị trí của vùng good deal.

---

### 6.1. Biểu đồ 1: Bản đồ phân bố listing theo giá bất thường (Point Map)

#### A. Idiom

| **Idiom** | **Point Map (Geographic Scatter Map)** |
|---|---|
| **What** | Longitude: Quantitative/Geographic<br>Latitude: Quantitative/Geographic<br>Price Is Outlier: Categorical (True/False)<br>Price: Quantitative<br>Room Type: Categorical |
| **How — Encode** | Mark: Point (Circle)<br>Channel:<br>— PosX: Longitude (Geographic position — kinh độ)<br>— PosY: Latitude (Geographic position — vĩ độ)<br>— Hue Color: Price Is Outlier (Categorical — đỏ = True outlier, xanh = False normal)<br>— Size: Price (Quantitative — điểm lớn hơn = giá cao hơn) |
| **How — Manipulate** | Selection: hover để xem id, price, room_type, neighbourhood_group, price_is_outlier |
| **How — Facet** | — |
| **How — Reduce** | Filter: room_type (optional — lọc theo loại phòng để giảm clutter) |
| **Why** | **locate → explore**<br>Xác định vị trí địa lý của các listing có giá bất thường. Point Map là idiom duy nhất cho phép phân tích spatial distribution — không thể thay thế bằng chart khác cho câu hỏi "ở đâu". |
| **Scale** | Key: ~21,000 listings (điểm)<br>Color: 2 (True/False outlier) |

![Hình 6.1. Bản đồ phân bố listing theo giá bất thường tại NYC](../docs/tableau/Task 6.1 - Price Outlier Map.png)

*Hình 6.1. Bản đồ phân bố listing theo giá bất thường tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Longitude), PosY (Latitude): vị trí địa lý thực tế → phù hợp thuộc tính Quantitative/Geographic (Q). Geographic position là cách duy nhất đúng để encode tọa độ không gian.
- Hue Color: phân biệt nhị phân True/False outlier → phù hợp thuộc tính Categorical (C). Chỉ 2 màu → discriminability tuyệt đối.
- Size: thể hiện mức giá (Q) → phù hợp — điểm lớn hơn = giá cao hơn, nhất quán với convention.

Kết luận: Các channel được sử dụng đúng với bản chất dữ liệu. Point Map là idiom tối ưu để phân tích dữ liệu có thành phần địa lý.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX, PosY (geographic position) có độ chính xác tuyệt đối về mặt không gian. Kênh Size (Area) xếp thấp trong channel effectiveness ranking — khó ước lượng chênh lệch giá chính xác qua kích thước điểm. Tuy nhiên mục tiêu chính là định vị (Locate), không phải so sánh chính xác — trade-off có thể chấp nhận.
- **Discriminability:** 2 màu nhị phân (đỏ/xanh) rất dễ phân biệt. Tuy nhiên với ~21k điểm, các vùng dày đặc bị overlap nghiêm trọng. **Giải pháp đề xuất:** giảm opacity của điểm False (xanh) để outlier (đỏ) nổi bật hơn, hoặc kết hợp filter theo borough để zoom vào từng khu vực.
- **Separability:** Kênh PosX/PosY và Color tách biệt tốt. Kênh Size và Color có thể tương tác nhẹ khi điểm lớn che điểm nhỏ, nhưng outlier (đỏ) thường có Size lớn nên thực tế nổi bật.

#### C. Phân tích biểu đồ

- **Outlier giá cao** (điểm đỏ lớn) tập trung dày đặc ở khu vực Manhattan — đặc biệt vùng Midtown và Upper East Side, khẳng định Manhattan là thị trường giá cao và biến động nhất.
- **Bronx và Staten Island** hầu như không có điểm đỏ — thị trường giá bình ổn, an toàn hơn cho du khách về tính dự đoán được của giá.
- **Brooklyn** có một số outlier tập trung ở khu vực ven biển phía tây (Brooklyn Heights, DUMBO) — nơi host có thể định giá cao hơn mức phổ thông do view đẹp và gần Manhattan.
- **Khuyến nghị:** Du khách nên kết hợp với Task 5 để chọn borough; tránh các listing Manhattan không có nhiều reviews và có giá bất thường cao.

---

### 6.2. Biểu đồ 2: Scatter plot giá niêm yết vs. điểm đánh giá — Phát hiện Good Deal (Scatter Plot)

#### A. Idiom

| **Idiom** | **Scatter Plot** |
|---|---|
| **What** | Price: Quantitative<br>Review Scores Rating: Quantitative<br>Good Deal Flag: Categorical ("Good Deal" / "Normal")<br>Number of Reviews: Quantitative |
| **How — Encode** | Mark: Point (Circle)<br>Channel:<br>— PosX: Price (Quantitative, position)<br>— PosY: Review Scores Rating (Quantitative, position)<br>— Hue Color: Good Deal Flag (Categorical — xanh lá = Good Deal, xám = Normal)<br>— Size: Number of Reviews (Quantitative — listing nhiều review = điểm lớn hơn) |
| **How — Manipulate** | Selection: hover để xem price, rating, room_type, neighbourhood, number_of_reviews |
| **How — Facet** | Superimpose: Reference Line (median price dọc, average rating ngang) đặt lên scatter plot |
| **How — Reduce** | Filter: price_is_outlier = False; number_of_reviews ≥ 5 (loại listing ít review, kém tin cậy) |
| **Why** | **discover → compare**<br>Phát hiện mối quan hệ (dependency) giữa giá và rating. Scatter plot là idiom tối ưu cho phân tích correlation giữa 2 biến Q. Reference lines chia không gian thành 4 góc phần tư, định nghĩa rõ vùng "good deal" mà không cần tính toán phức tạp. |
| **Scale** | Color: 2 (Good Deal / Normal)<br>Items: listing với ≥ 5 reviews, price_is_outlier = False |

![Hình 6.2. Scatter plot giá niêm yết vs. điểm đánh giá — phát hiện Good Deal](../docs/tableau/Task 6.2 - Price vs Rating.png)

*Hình 6.2. Scatter plot giá niêm yết vs. điểm đánh giá — phát hiện Good Deal*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Price — Q): vị trí ngang thể hiện giá → đúng.
- PosY (Rating — Q): vị trí dọc thể hiện chất lượng → đúng. Rating cao hơn = vị trí cao hơn nhất quán với convention "up = good".
- Hue Color: phân biệt Good Deal / Normal (C) → đúng — chỉ 2 giá trị, discriminability tuyệt đối.
- Size: thể hiện Number of Reviews (Q) → đúng. Size phù hợp cho Q thứ cấp (proxy trust level).

Kết luận: Scatter plot là idiom tối ưu để phân tích mối quan hệ giữa 2 biến định lượng với phân nhóm categorical.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX và PosY (position on common scale) — channel chính xác nhất. Kênh Size (Area) — accuracy thấp hơn, khó so sánh chính xác số reviews; đây là channel phụ nên chấp nhận được.
- **Discriminability:** 2 màu (xanh/xám) rất dễ phân biệt. Reference lines tạo 4 góc phần tư rõ ràng, giúp người xem định vị ngay vùng "good deal" (góc trên-trái). Hiện tượng overplotting tại khu vực rating 4.8–5.0 và price thấp là hạn chế — có thể cải thiện bằng jitter hoặc transparency.
- **Separability:** PosX, PosY, Color và Size tách biệt tốt.

#### C. Phân tích biểu đồ

- **Vùng góc trên-trái** (price < median, rating > average 4.5) là vùng "Good Deal" — tập trung nhiều điểm xanh, chủ yếu thuộc Brooklyn và Queens.
- **Manhattan** có nhiều listing phân bổ ở phần bên phải chart (giá cao) với rating không tương xứng — không phải lựa chọn tối ưu về cost-efficiency.
- **Listing "Good Deal" có Size lớn** (nhiều reviews) là những nơi đã được kiểm chứng bởi nhiều khách — độ tin cậy cao.
- **Quan trọng:** Không có tương quan dương rõ ràng giữa giá cao và rating cao — nhiều listing Brooklyn/Queens giá thấp vẫn đạt rating 4.7–5.0, chứng minh giá không phải là proxy của chất lượng trên Airbnb.
- **Khuyến nghị:** Ưu tiên listing trong vùng "Good Deal" tại Brooklyn/Queens với Size điểm lớn (number_of_reviews ≥ 20–30).

---

## Task 7 — Phân tích Hiệu quả Chi phí Lưu trú (Cost Efficiency of Accommodation)

**Câu hỏi nghiệp vụ (User Story):**
*"As a group traveler (4–6 people) planning a NYC trip, I need to know which borough and room type offer the lowest per-person cost, and how the number of accommodates affects per-person price — so that I can choose the most cost-efficient option for my group."*

---

### 7.0. Data Abstraction và Task Abstraction

#### 7.0.1. Data Abstraction — Biểu đồ 7.1 (Grouped Bar Chart)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một listing Airbnb với thông tin giá, loại phòng, borough và sức chứa |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| neighbourhood_group_cleansed (Borough) | categorical | — | Discrete | Khu vực hành chính (5 borough NYC) | ✓ | |
| room_type | categorical | — | Discrete | Loại phòng | ✓ | |
| price_per_person (derived) | quantitative | sequential | Continuous | Chi phí mỗi người = price / accommodates (USD) | | ✓ |

#### 7.0.2. Data Abstraction — Biểu đồ 7.2 (Scatter Plot + Trend)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một listing với thông tin sức chứa và giá mỗi người |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| accommodates | quantitative | sequential | Discrete | Sức chứa tối đa (1–16 người) | ✓ | |
| price_per_person (derived) | quantitative | sequential | Continuous | Chi phí mỗi người = price / accommodates (USD) | | ✓ |
| room_type | categorical | — | Discrete | Loại phòng (dùng phân nhóm trend line) | ✓ | |

#### 7.0.3. Task Abstraction

**Biểu đồ 7.1:** produce (derive) → compare → summarize

- **Produce (derive):** Tạo `price_per_person = price / accommodates`. Tính MEDIAN(price_per_person) theo tổ hợp borough × room_type. Filter `price_is_outlier = False`.
- **Compare:** So sánh chi phí mỗi người theo 2 chiều categorical đồng thời. Grouped bar được chọn thay stacked bar vì mục tiêu là so sánh giá trị tuyệt đối, không phải tỷ lệ phần trăm.
- **Summarize:** Xác định khu vực và loại phòng có chi phí mỗi người thấp nhất.

**Biểu đồ 7.2:** produce (derive) → discover → explore

- **Produce (derive):** Tính MEDIAN(price_per_person) theo accommodates × room_type. Thêm Trend Line (Linear) cho từng nhóm room_type.
- **Discover:** Phát hiện xu hướng "economies of scale" — price/person giảm khi accommodates tăng.
- **Explore:** Xác định crossover point — số người tối ưu tại đó Entire home rẻ hơn Private room theo đầu người.

---

### 7.1. Biểu đồ 1: Median chi phí mỗi người theo borough và loại phòng (Grouped Bar Chart)

#### A. Idiom

| **Idiom** | **Grouped Bar Chart** |
|---|---|
| **What** | Borough/Neighbourhood_group_cleansed: Categorical<br>Room Type: Categorical<br>Median Price per Person: Quantitative (calculated field: price/accommodates) |
| **How — Encode** | Mark: Bar (grouped — Stack Marks OFF)<br>Channel:<br>— PosX: Borough (Categorical, position — phân biệt 5 borough)<br>— PosY: MEDIAN(price_per_person) (Quantitative, length)<br>— Hue Color: Room Type (Categorical — nhóm cột theo loại phòng)<br>— Label: giá trị MEDIAN trên đầu cột |
| **How — Manipulate** | Selection: hover để xem median chi phí/người theo từng borough × room type |
| **How — Facet** | — |
| **How — Reduce** | Filter: price_is_outlier = False |
| **Why** | **compare → summarize**<br>So sánh chi phí mỗi người theo 2 chiều categorical đồng thời (borough × room type). Grouped bar được chọn thay stacked bar vì task là Compare (giá trị tuyệt đối), không phải part-to-whole. |
| **Scale** | Key: 5 (borough)<br>Color key: 4 (room type)<br>Items: ~21,000 listing (sau lọc) |

![Hình 7.1. Median chi phí mỗi người theo borough và room type](../docs/tableau/Task 7.1 - Price per Person by Borough.png)

*Hình 7.1. Median chi phí mỗi người theo borough và room type*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX: phân biệt borough (C) → đúng.
- PosY (Length từ 0): thể hiện MEDIAN price/person (Q) → đúng, Length là channel chính xác nhất cho Q.
- Hue Color: phân biệt room type (C) trong grouped bar → đúng.

Kết luận: Grouped Bar Chart là lựa chọn đúng đắn khi cần so sánh đồng thời theo 2 chiều categorical (borough × room type).

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Length (từ gốc 0) — channel có độ chính xác cao. Label số trên đầu cột loại bỏ sai số cảm nhận hoàn toàn.
- **Discriminability:** 3–4 màu trong phạm vi ≤ 7 → phân biệt tốt. Grouped layout rõ ràng hơn stacked bar.
- **Separability:** PosX, PosY và Color hoạt động độc lập tốt.

#### C. Phân tích biểu đồ

- **Entire home/apt** có price/person cao nhất nhìn chung — nhưng khi chia theo nhiều người (4–6 người), đây vẫn cạnh tranh với Private room ở Manhattan.
- **Bronx và Staten Island** có price/person thấp nhất trong mọi room type — lựa chọn tối ưu cho nhóm khách ngân sách thấp.
- **Private room và Shared room** luôn có price/person thấp hơn Entire home — phù hợp cho khách solo hoặc đôi.
- **Khuyến nghị:** Nhóm 4–6 người nên so sánh Entire home/apt ở Queens/Bronx với Private room ở Brooklyn — kết hợp với Task 7.2 để xác định crossover point.

---

### 7.2. Biểu đồ 2: Mối quan hệ sức chứa và chi phí mỗi người (Scatter Plot)

#### A. Idiom

| **Idiom** | **Scatter Plot với Trend Line** |
|---|---|
| **What** | Accommodates: Quantitative (dùng Dimension — 1 đến 16 người)<br>Median Price per Person: Quantitative<br>Room Type: Categorical |
| **How — Encode** | Mark: Point (Circle)<br>Channel:<br>— PosX: Accommodates (Quantitative/Dimension — giữ từng giá trị riêng 1–16)<br>— PosY: MEDIAN(price_per_person) (Quantitative, position)<br>— Hue Color: Room Type (Categorical — phân biệt loại phòng) |
| **How — Manipulate** | Selection: hover để xem accommodates, median price/person, room_type, count |
| **How — Facet** | Superimpose: Trend Line (Linear) cho từng room type (Analytics pane) |
| **How — Reduce** | Filter: price_is_outlier = False; accommodates ≤ 16 (loại outlier capacity) |
| **Why** | **discover → explore**<br>Phát hiện xu hướng giảm của price/person khi sức chứa tăng (economies of scale). Scatter + Trend Line là idiom chuẩn để phân tích relationship giữa 2 biến Q — Trend Line thể hiện hướng và tốc độ thay đổi, đặc biệt quan trọng để xác định crossover point giữa các room type. |
| **Scale** | Key: 16 (giá trị accommodates 1–16)<br>Color: 4 (room type) |

![Hình 7.2. Mối quan hệ giữa sức chứa và chi phí mỗi người](../docs/tableau/Task 7.2 - Accommodates vs Price per Perso.png)

*Hình 7.2. Mối quan hệ giữa sức chứa và chi phí mỗi người*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Accommodates): Q/Ordinal → position thích hợp.
- PosY (MEDIAN price/person): Q → position thích hợp.
- Hue Color: Room Type (C) → đúng, phân biệt 3–4 loại phòng.
- Trend Line: hiển thị xu hướng tổng thể → tăng thêm thông tin về dependency.

Kết luận: Scatter plot với Trend Line là lựa chọn chuẩn mực để phân tích mối quan hệ giữa 2 biến Q và so sánh xu hướng giữa các nhóm.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX và PosY (position on common scale) — rất chính xác. Trend Line thể hiện xu hướng dốc xuống rõ ràng. MEDIAN aggregation giúp giảm nhiễu so với raw data.
- **Discriminability:** 3–4 màu dễ phân biệt. Số lượng điểm vừa phải (~42–64 marks) không bị clutter.
- **Separability:** PosX, PosY và Color tách biệt hoàn toàn. Trend lines không làm rối các điểm dữ liệu thực.

#### C. Phân tích biểu đồ

- **Trend line của Entire home/apt** dốc xuống mạnh nhất — xác nhận "economies of scale": càng nhiều người chia phòng, giá mỗi người càng giảm. Sweet spot rõ ràng ở **4–6 người**.
- **Private room** gần như phẳng — sức chứa không ảnh hưởng nhiều đến price/person.
- **Crossover point:** Với **4+ người, Entire home trở nên rẻ hơn Private room** tính theo đầu người — insight quan trọng nhất của Task 7.
- **Khuyến nghị:** Nhóm ≥ 4 người nên ưu tiên Entire home/apt, ưu tiên Queens/Brooklyn để tối ưu cả vị trí lẫn chi phí mỗi người.

---

## Task 8 — Phân tích Tính Mùa vụ và Cơ hội Đặt phòng (Seasonality & Booking Opportunity)

**Câu hỏi nghiệp vụ (User Story):**
*"As a host or traveler on Airbnb NYC, I need to understand how occupancy rate changes across months and how minimum night policies interact with seasonal demand — so that I can time my booking (or listing) strategy to maximize occupancy or find the best rates in low season."*

---

### 8.0. Data Abstraction và Task Abstraction

#### 8.0.1. Data Abstraction — Biểu đồ 8.1 (Line Chart)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi dòng là một bản ghi lịch (calendar entry) cho một listing, ghi nhận ngày và trạng thái available/booked |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| month (derived từ date) | ordinal | cyclic | Discrete | Tháng trong năm (1–12) — trục thời gian; cyclic vì seasonality lặp lại theo chu kỳ năm | ✓ | |
| occupancy_rate_pct (derived) | quantitative | sequential | Continuous | Tỷ lệ lấp đầy = AVG(is_booked) × 100 (%) | | ✓ |

#### 8.0.2. Data Abstraction — Biểu đồ 8.2 (Heatmap)

| | |
|---|---|
| **Dataset level** | table |
| **Data level** | item |
| **Item semantic** | Mỗi ô là tổ hợp tháng × nhóm minimum nights với giá trị occupancy rate tương ứng |
| **Dataset availability** | static |

| Tên thuộc tính | Phân loại (C,O,Q) | Hướng (direction) | Characteristic | Ngữ nghĩa | Key | Value |
|---|---|---|---|---|---|---|
| month (derived từ date) | ordinal | cyclic | Discrete | Tháng trong năm (1–12); cyclic vì pattern mùa vụ lặp lại theo năm | ✓ | |
| minimum_nights_group (derived) | categorical | — | Discrete | Nhóm chính sách: Short (≤3), Medium (4–7), Long (>7 đêm) | ✓ | |
| occupancy_rate_pct (derived) | quantitative | sequential | Continuous | Tỷ lệ lấp đầy (%) | | ✓ |

#### 8.0.3. Task Abstraction

**Biểu đồ 8.1:** produce (derive) → discover → browse

- **Produce (derive):** Tính AVG(is_booked) × 100 theo tháng → `occupancy_rate_pct`. Trích xuất month từ date field. Filter năm 2026 để có dữ liệu đủ tháng (dữ liệu 2025 chỉ có từ tháng 11).
- **Discover:** Phát hiện pattern mùa vụ — tháng nào là high season, tháng nào là low season?
- **Browse:** Duyệt qua từng tháng để nhận diện xu hướng tăng/giảm trong năm.

**Biểu đồ 8.2:** produce (derive) → discover → compare

- **Produce (derive):** Binning `minimum_nights` thành 3 nhóm. Tính `occupancy_rate_pct` theo month × minimum_nights_group.
- **Discover:** Phát hiện pattern 2 chiều — Heatmap encode 3 biến đồng thời theo nguyên lý "2 keys → heatmap".
- **Compare:** So sánh hiệu quả của 3 chính sách minimum nights theo từng tháng trong năm.

---

### 8.1. Biểu đồ 1: Tỷ lệ lấp đầy theo tháng (Line Chart)

#### A. Idiom

| **Idiom** | **Line Chart (Multi-line)** |
|---|---|
| **What** | Month: Ordinal (tháng 1–12, có thứ tự, cyclic)<br>Occupancy Rate Pct: Quantitative (calculated: AVG(is_booked) × 100) |
| **How — Encode** | Mark: Line + Point<br>Channel:<br>— PosX: Month (Ordinal, Discrete — tiến trình thời gian tháng 1–12)<br>— PosY: Occupancy Rate (%) (Quantitative, position)<br>— Reference Line: Average (ngang — mức trung bình tổng thể) |
| **How — Manipulate** | Selection: hover để xem tháng, occupancy rate (%) cụ thể |
| **How — Facet** | Superimpose: Reference Line (average occupancy ngang) đặt lên biểu đồ |
| **How — Reduce** | Filter: year (optional — để focus vào 1 năm cụ thể) |
| **Why** | **discover → browse**<br>Phát hiện xu hướng mùa vụ trong dữ liệu occupancy. Line chart được chọn (không phải bar) vì Month là Ordinal attribute có thứ tự — đường kết nối liên tục nhấn mạnh tính liên tục và xu hướng thời gian, không phải giá trị tại từng điểm rời rạc. |
| **Scale** | Key: 12 (tháng); Items: dữ liệu 2026 (tháng 1–11) |

![Hình 8.1. Tỷ lệ lấp đầy (occupancy rate) theo tháng tại NYC](../docs/tableau/Task 8.1 - Monthly Occupancy Rate.png)

*Hình 8.1. Tỷ lệ lấp đầy (occupancy rate) theo tháng tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Month — Ordinal): trục thời gian có thứ tự → đúng. Ordinal phù hợp với Position — không dùng Categorical vì mất thứ tự thời gian.
- PosY (Occupancy Rate — Q): thể hiện mức độ lấp đầy → đúng.
- Hue Color: phân biệt Year (C) → đúng. Line chart kết hợp Hue Color là chuẩn mực phân tích time series theo nhóm.

Kết luận: Line chart là idiom tối ưu cho dữ liệu chuỗi thời gian, đặc biệt khi cần phát hiện trend và seasonality.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosY (position on common scale) — rất chính xác. Người xem dễ dàng so sánh mức occupancy giữa các tháng.
- **Discriminability:** 2 đường (2 năm) rất dễ phân biệt. Reference line Average tạo mốc tham chiếu để xác định tháng nào trên/dưới trung bình.
- **Separability:** PosX, PosY và Color tách biệt hoàn toàn.

#### C. Phân tích biểu đồ

- **Tháng 1–4 là low season** rõ rệt (occupancy ~20–21%) — cơ hội tốt cho khách muốn giá thấp và dễ tìm phòng.
- **Từ tháng 5 trở đi**, occupancy tăng dần và đạt đỉnh vào **tháng 11 (~40%)** — phản ánh nhu cầu du lịch mùa thu và dịp lễ Thanksgiving.
- **Dữ liệu sử dụng:** calendar 2026 (tháng 1–11) — dữ liệu 2025 chỉ có từ tháng 11 nên không đủ để so sánh liên năm.
- **Khuyến nghị cho du khách:** Đặt phòng tháng 1–3 để có giá thấp nhất; tháng 11 cần đặt sớm do cầu rất cao.
- **Khuyến nghị cho host:** Tháng 1–4 nên linh hoạt hóa chính sách (giảm minimum nights, giảm giá nhẹ); tháng 11–12 có thể tăng giá.

---

### 8.2. Biểu đồ 2: Heatmap tỷ lệ lấp đầy theo tháng và chính sách minimum nights (Heatmap)

#### A. Idiom

| **Idiom** | **Heatmap (Matrix Chart)** |
|---|---|
| **What** | Month: Ordinal (tháng 1–12)<br>Minimum Nights Group: Categorical (Short / Medium / Long stay)<br>Occupancy Rate Pct: Quantitative (calculated: AVG(is_booked) × 100) |
| **How — Encode** | Mark: Square (Cell)<br>Channel:<br>— PosX: Month (Ordinal, Discrete — tạo cột ma trận 1–12)<br>— PosY: Minimum Nights Group (Categorical — Short/Medium/Long stay)<br>— Color (Luminance/Sequential): Occupancy Rate (Quantitative — đậm = cao, nhạt = thấp) |
| **How — Manipulate** | Selection: hover để xem month, Minimum Nights Group, occupancy_rate_pct (%) |
| **How — Facet** | — |
| **How — Reduce** | — |
| **Why** | **discover → compare**<br>Phát hiện pattern 2 chiều đồng thời (month × minimum_nights_group). Heatmap là idiom tối ưu theo nguyên lý "2 keys → heatmap" — encode 3 biến (Month, Group, Occupancy) trong cấu trúc ma trận. Color (Luminance/Sequential) là channel đúng cho quantitative attribute trong heatmap vì kích thước ô đồng đều loại bỏ bias từ Area. |
| **Scale** | Key: 12 (tháng) × 3 (nhóm) = 36 ô<br>Bin: 3 (Short ≤3, Medium ≤7, Long >7) |

![Hình 8.2. Heatmap tỷ lệ lấp đầy theo tháng và chính sách minimum nights](../docs/tableau/Task 8.2 - Heatmap Occupancy.png)

*Hình 8.2. Heatmap tỷ lệ lấp đầy theo tháng và chính sách minimum nights*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Month — O): trục thời gian theo thứ tự → đúng.
- PosY (Minimum Nights Group — C): phân loại chính sách → đúng. Spatial region cho categorical.
- Color (Luminance/Sequential): thể hiện độ lớn occupancy (Q) → phù hợp. Sequential colormap (nhạt→đậm) đúng cho quantitative attribute có hướng sequential.

Kết luận: Heatmap là idiom phù hợp nhất khi cần phân tích 3 biến (2 keys + 1 value) trong cấu trúc ma trận.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Color (Luminance) — accuracy thấp hơn Position, khó ước lượng chính xác % chênh lệch. Tuy nhiên mục tiêu là phát hiện pattern (cao/thấp), không phải đọc giá trị chính xác — trade-off có thể chấp nhận.
- **Discriminability:** 36 ô vuông đều nhau. Sequential palette giúp phân biệt ~5–7 cấp độ màu.
- **Separability:** PosX, PosY và Color kết hợp tốt. Area đồng đều không tạo bias về kích thước.

#### C. Phân tích biểu đồ

- **Short minimum stay (≤3 đêm)** có occupancy cao và ổn định quanh năm — chính sách linh hoạt thu hút nhiều khách nhất, đặc biệt trong mùa thấp điểm.
- **Long minimum stay (>7 đêm)** có occupancy thấp hơn trong phần lớn các tháng, nhưng tăng vào cuối năm — phù hợp cho khách công tác dài hạn.
- **Tháng 11–12** có màu đậm nhất ở hầu hết các nhóm — xác nhận high season với nhu cầu cao bất kể chính sách minimum nights.
- **Khuyến nghị cho host:** Tháng 1–4 nên chuyển sang Short minimum stay; tháng 11–12 có thể giữ Medium/Long stay vì cầu cao tự nhiên bù đắp tính hạn chế của chính sách.

---

## Tổng hợp Insights từ 4 Tasks

### Kết luận theo nhóm đối tượng

**Cho du khách cá nhân/đôi ngân sách trung bình:**
- Chọn **Brooklyn** (Task 5: median $129, Task 6: nhiều Good Deal listings) thay vì Manhattan.
- Đặt phòng vào **tháng 1–3** (Task 8: occupancy thấp ~20%, giá cạnh tranh hơn).
- Ưu tiên listing `good_deal_flag = True` với `number_of_reviews ≥ 20` (Task 6.2).

**Cho nhóm du lịch 4–6 người:**
- Chọn **Entire home/apt tại Queens hoặc Brooklyn** (Task 7: sweet spot 4–6 người).
- Crossover point từ Task 7.2: Entire home rẻ hơn Private room tính theo đầu người từ 4 người trở lên.

**Cho Airbnb host muốn tối ưu doanh thu:**
- **Tháng 1–4:** Short minimum stay (≤3 đêm), giảm giá nhẹ để duy trì occupancy (Task 8.2).
- **Tháng 11–12:** Tăng giá, Medium/Long minimum stay vẫn đảm bảo occupancy cao (Task 8.1 + 8.2).

---

## Limitations (Hạn chế)

**1. Occupancy rate dựa trên calendar blocks, không phải actual bookings:**
`occupancy_rate_pct` tính từ `is_booked` dựa trên calendar của host. Calendar blocks có thể bao gồm ngày host tự block (không cho thuê) — có thể **overestimate** occupancy thực sự.

**2. price_per_person giả định full occupancy:**
`price_per_person = price / accommodates` giả định listing luôn được đặt theo đúng sức chứa tối đa. Thực tế 2 người đặt phòng 6 người vẫn trả giá đầy đủ. Task 7 chỉ có giá trị khi nhóm đủ số người như sức chứa.

**3. Good Deal flag dùng ngưỡng global, không theo borough:**
Listing giá $120 ở Manhattan là "Good Deal" theo ngưỡng global, nhưng không hẳn rẻ so với mức trung bình borough Manhattan. Cần cải tiến bằng ngưỡng theo từng borough.

**4. Dữ liệu seasonality hạn chế (2025–2026):**
Calendar dataset chỉ có dữ liệu đủ tháng cho năm 2026 (2025 chỉ có từ tháng 11). Phân tích seasonality Task 8.1 dựa trên 1 năm — không đủ để kết luận pattern mùa vụ nhất quán. Cần ít nhất 3–5 năm để xác nhận seasonal trend có tính bền vững.

**5. Outlier filter loại bỏ luxury segment hợp lệ:**
Filter `price_is_outlier = False` loại bỏ các luxury listings hoàn toàn hợp lệ (penthouse Manhattan). Task 5 và 7 chỉ đại diện cho phân khúc mid-range.

**6. Overplotting trong Task 6.1 (Point Map):**
Với ~21,000 điểm, các khu vực dày đặc bị overlap nghiêm trọng. Giải pháp cải tiến: hexbin map, clustering hoặc filter theo borough.

**7. Không có dữ liệu trải nghiệm chi tiết:**
Dataset thiếu điểm đánh giá theo từng hạng mục (sạch sẽ, vị trí, giao tiếp) và giá cuối cùng sau discount. Insights về "Good Deal" chỉ dựa trên giá niêm yết và rating tổng hợp.

---

## Kết luận (Conclusion)

Báo cáo phân tích 4 khía cạnh của thị trường Airbnb NYC thông qua 8 biểu đồ trực quan hóa dữ liệu, mỗi biểu đồ được thiết kế có chủ đích dựa trên nguyên lý Data Abstraction và Task Abstraction.

**Ba phát hiện chính có giá trị kinh doanh cao nhất:**

1. **Sự phân cực giá theo borough là rõ rệt và nhất quán:** Manhattan đắt gấp đôi Bronx ($200 vs $93 median), nhất quán cho mọi loại phòng. Brooklyn là điểm cân bằng tốt nhất giữa vị trí và chi phí.

2. **Economies of scale trong Entire home/apt là insight hành động được:** Nhóm từ 4 người trở lên nên ưu tiên Entire home — giá/người thấp hơn Private room từ crossover point 4 người. Brooklyn/Queens cung cấp lựa chọn tốt nhất.

3. **Seasonality mạnh và dự đoán được:** Tháng 1–3 là window tối ưu cho du khách (occupancy ~20%, giá cạnh tranh); tháng 11–12 là cao điểm cần đặt sớm. Host nên điều chỉnh minimum nights và giá theo mùa.

**Hướng phân tích tiếp theo đề xuất:**
- Phân tích đến cấp neighbourhood (không chỉ borough) để có độ phân giải địa lý cao hơn.
- Tích hợp sub-scores đánh giá (cleanliness, location) để cải tiến Good Deal model.
- Mở rộng seasonality sang 3–5 năm để xác nhận pattern ổn định.
- Phân tích ROI cho host: occupancy × price/đêm để tối ưu chiến lược định giá theo mùa.
