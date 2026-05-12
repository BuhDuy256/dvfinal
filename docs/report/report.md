# BÁO CÁO PHÂN TÍCH DỮ LIỆU AIRBNB NEW YORK CITY

**Task 5, 6, 7, 8 — Visualization Idiom Analysis**

---

## Task 5 — Phân tích Phân phối Giá theo Khu vực (Price Distribution by Area)

**Câu hỏi nghiệp vụ:** *"Khu vực nào tại New York có mức giá niêm yết cao nhất/thấp nhất, và phân phối giá ở từng borough khác nhau như thế nào?"*

Mục đích: Giúp hiểu rõ bức tranh giá cả, mức độ phân tán và cấu trúc nguồn cung theo từng borough để định vị phân khúc thị trường Airbnb tại NYC.

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
| **Why** | **compare → discover**<br>So sánh phân phối giá giữa 5 borough NYC. Phát hiện outlier và biên độ dao động giá (IQR) theo từng borough và loại phòng. |
| **Scale** | Key: 5 (borough)<br>Color key: 4 (room type) |

![Hình 5.1. Box plot phân phối giá niêm yết theo borough tại NYC](../docs/tableau/Task 5.1 - Price Distribution by Borough.png)

*Hình 5.1. Box plot phân phối giá niêm yết theo borough tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- Thuộc tính sử dụng: Borough (C), Price (Q), Room Type (C).
- PosX (vị trí ngang): phân biệt 5 borough → phù hợp thuộc tính Categorical (C).
- PosY (vị trí dọc): thể hiện phạm vi phân phối giá (Q1, Median, Q3, whiskers) → phù hợp thuộc tính Quantitative (Q).
- Hue Color: phân biệt loại phòng → phù hợp thuộc tính Categorical (C).

Kết luận: Các channel được áp dụng đúng với bản chất dữ liệu. Box plot là idiom chuẩn mực nhất để biểu diễn phân phối dữ liệu liên tục theo nhóm.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Kênh PosY (vị trí trên thang đo chung) tuân theo Stevens' Psychophysical Law với n = 1.0 — đây là kênh chính xác nhất, Log_error thấp nhất. Người xem có thể ước lượng tương đối chính xác khoảng cách giá giữa các borough. Kênh Hue Color dùng cho categorical không liên quan đến sai số định lượng.
- **Discriminability:** 5 màu (Hue) cho 5 room type trong phạm vi ≤ 7 → mắt người phân biệt hoàn toàn tốt. Whiskers và box IQR hiển thị rõ ràng trên nền trắng. Các outlier dưới dạng điểm tròn (Circle) dễ nhận diện.
- **Separability:** Kênh PosX, PosY và Color tách biệt hoàn toàn — vị trí không làm nhiễu nhận diện màu sắc. Filter price_is_outlier = False loại bỏ extreme outliers giúp chart dễ đọc hơn.

#### C. Phân tích biểu đồ

- Manhattan có median price cao nhất (~$150–200) và IQR rộng nhất, cho thấy mức độ biến động giá rất lớn — tồn tại cả phân khúc bình dân lẫn cao cấp.
- Bronx và Staten Island có IQR hẹp và median thấp (~$92–99), phản ánh thị trường giá ổn định, ít phân hóa.
- Loại phòng Entire home/apt luôn có box cao hơn Private room ở mọi borough, khẳng định sự phân tầng giá theo loại phòng là nhất quán trên toàn thành phố.

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
| **Why** | **compare → summarize**<br>So sánh median giá giữa 5 borough NYC. Tóm tắt nhanh mức giá trung tâm của từng khu vực, dễ đọc cho người dùng phổ thông hơn box plot. |
| **Scale** | Key: 5 (borough) |

![Hình 5.2. Median giá niêm yết theo borough NYC](../docs/tableau/Task 5.2 - Median Price by Borough.png)

*Hình 5.2. Median giá niêm yết theo borough NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX: phân biệt borough (C) → đúng.
- PosY (Length từ gốc 0): thể hiện độ lớn MEDIAN Price (Q) → đúng — Length là channel phù hợp nhất cho Q.
- Hue Color: phân biệt borough (C) → đúng, tăng tính nhận diện.

Kết luận: Mọi channel đều phù hợp và đúng với bản chất dữ liệu.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Kênh Length (chiều dài cột từ gốc 0) theo Stevens' Law có n = 1.0 — độ chính xác tuyệt vời, Log_error cực thấp. Label số ở đầu cột loại bỏ hoàn toàn sai số cảm nhận thị giác, người đọc biết chính xác giá trị.
- **Discriminability:** 5 cột màu khác nhau, phân cách rõ ràng, sort descending giúp so sánh nhanh từ đắt đến rẻ. Không có hiện tượng overlap hay clutter.
- **Separability:** PosX, PosY và Color tách biệt hoàn toàn. Bar chart đơn giản, không có kênh nào cạnh tranh nhau.

#### C. Phân tích biểu đồ

- Manhattan ($200) đắt hơn gấp đôi so với Bronx ($93) — mức chênh lệch rất lớn, cho thấy sự phân cực giá rõ rệt theo vị trí địa lý.
- Brooklyn ($129) đứng thứ hai, là lựa chọn cân bằng giữa vị trí và chi phí so với Manhattan.
- Queens ($100), Staten Island ($99) và Bronx ($93) có median tương đương nhau, phù hợp cho du khách có ngân sách thấp.

---

## Task 6 — Phân tích Giá Bất thường và Phát hiện Giá trị Tốt (Price Outlier & Real Value)

**Câu hỏi nghiệp vụ:** *"Listing nào có giá bất thường (outlier)? Chúng phân bố ở đâu trên bản đồ? Và listing nào có giá thấp nhưng rating cao — tức là "good deal" cho du khách?"*

Mục đích: Xác định vị trí và đặc điểm các listing giá bất thường, đồng thời tìm kiếm các listing có giá trị thực sự tốt (giá thấp, chất lượng cao) để hỗ trợ quyết định đặt phòng.

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
| **Why** | **locate → explore**<br>Xác định vị trí địa lý của các listing có giá bất thường. Khám phá mối quan hệ giữa vị trí không gian và đặc điểm giá bất thường tại từng khu vực NYC. |
| **Scale** | Key: ~21,000 listings (điểm)<br>Color: 2 (True/False outlier) |

![Hình 6.1. Bản đồ phân bố listing theo giá bất thường tại NYC](../docs/tableau/Task 6.1 - Price Outlier Map.png)

*Hình 6.1. Bản đồ phân bố listing theo giá bất thường tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Longitude), PosY (Latitude): vị trí địa lý thực tế → phù hợp thuộc tính Quantitative/Geographic (Q).
- Hue Color: phân biệt nhị phân True/False outlier → phù hợp thuộc tính Categorical (C).
- Size: thể hiện mức giá (Q) → phù hợp — điểm lớn hơn = giá cao hơn, trực quan.

Kết luận: Các channel được sử dụng đúng với bản chất dữ liệu. Point Map là idiom tối ưu để phân tích dữ liệu có thành phần địa lý.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX, PosY (geographic position) có độ chính xác tuyệt đối về mặt không gian. Kênh Size (Area) biểu diễn Price theo Stevens' Law với n ≈ 0.7, Log_error ≈ T9 ± 2.5 — khó ước lượng chênh lệch giá chính xác qua kích thước điểm. Tuy nhiên đây là hạn chế có thể chấp nhận vì mục tiêu chính là định vị (Locate), không phải so sánh chính xác.
- **Discriminability:** 2 màu nhị phân (đỏ/xanh) cho True/False rất dễ phân biệt. Tuy nhiên với ~21k điểm, các vùng dày đặc listing bị overlap nghiêm trọng — khó nhận diện từng điểm riêng lẻ.
- **Separability:** Kênh PosX/PosY và Color tách biệt tốt. Kênh Size và Color có thể tương tác nhẹ khi điểm lớn che điểm nhỏ, nhưng vì outlier (đỏ) thường có Size lớn nên thực tế rất nổi bật.

#### C. Phân tích biểu đồ

- Outlier giá cao (điểm đỏ lớn) tập trung dày đặc ở khu vực Manhattan — đặc biệt vùng Midtown và Upper East Side, khẳng định Manhattan là thị trường giá cao và biến động nhất.
- Bronx và Staten Island hầu như không có điểm đỏ — thị trường giá bình ổn, ít listing bất thường.
- Brooklyn có một số outlier tập trung ở khu vực ven biển phía tây (Brooklyn Heights, DUMBO) — khu vực có view đẹp và gần Manhattan.

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
| **Why** | **discover → compare**<br>Phát hiện mối quan hệ (dependency) giữa giá và rating. So sánh listing "Good Deal" với listing bình thường để hỗ trợ quyết định đặt phòng tối ưu cho du khách. |
| **Scale** | Color: 2 (Good Deal / Normal) |

![Hình 6.2. Scatter plot giá niêm yết vs. điểm đánh giá — phát hiện Good Deal](../docs/tableau/Task 6.2 - Price vs Rating.png)

*Hình 6.2. Scatter plot giá niêm yết vs. điểm đánh giá — phát hiện Good Deal*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Price — Q): vị trí ngang thể hiện giá → đúng.
- PosY (Rating — Q): vị trí dọc thể hiện chất lượng → đúng.
- Hue Color: phân biệt Good Deal / Normal (C) → đúng — màu sắc nổi bật giúp nhận diện vùng "good deal" ngay lập tức.
- Size: thể hiện Number of Reviews (Q) — listing có nhiều review đáng tin hơn → đúng.

Kết luận: Scatter plot là idiom tối ưu để phân tích mối quan hệ giữa 2 biến định lượng với phân nhóm categorical.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX và PosY (vị trí trên thang đo chung) có n = 1.0 theo Stevens' Law — rất chính xác. Kênh Size (Area) có n ≈ 0.7, Log_error ≈ T9 ± 2.5 — khó so sánh chính xác số review, nhưng đây là channel phụ (encoding trust level) nên chấp nhận được.
- **Discriminability:** 2 màu (xanh/xám) rất dễ phân biệt. Reference lines tạo 4 góc phần tư rõ ràng, giúp người xem định vị ngay vùng "good deal" (góc trên-trái). Hiện tượng overplotting tại khu vực rating 4.8–5.0 và price thấp là hạn chế cần lưu ý.
- **Separability:** PosX, PosY, Color và Size tách biệt tốt. Kênh Size không làm nhiễu nhận diện màu sắc Good Deal Flag.

#### C. Phân tích biểu đồ

- Vùng góc trên-trái (price < median, rating > average 4.5) là vùng "Good Deal" — tập trung nhiều điểm xanh, chủ yếu thuộc Brooklyn và Queens.
- Manhattan có nhiều listing phân bổ ở phần bên phải chart (giá cao) với rating không tương xứng — không phải lựa chọn tối ưu về mặt cost-efficiency.
- Các listing "Good Deal" có nhiều review (Size lớn) cho thấy đây là những nơi đã được kiểm chứng bởi nhiều khách — độ tin cậy cao.

---

## Task 7 — Phân tích Hiệu quả Chi phí Lưu trú (Cost Efficiency of Accommodation)

**Câu hỏi nghiệp vụ:** *"Borough nào có chi phí lưu trú mỗi người thấp nhất? Sức chứa (số người tối đa) ảnh hưởng như thế nào đến chi phí trên mỗi người?"*

Mục đích: Xác định borough và loại phòng nào cho hiệu quả chi phí tốt nhất khi đi theo nhóm, đồng thời khám phá mối quan hệ giữa sức chứa và giá theo đầu người.

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
| **Why** | **compare → summarize**<br>So sánh chi phí mỗi người giữa các borough và loại phòng. Xác định khu vực có cost efficiency tốt nhất cho nhóm du lịch muốn chia tiền. |
| **Scale** | Key: 5 (borough)<br>Color key: 4 (room type) |

![Hình 7.1. Median chi phí mỗi người theo borough và room type](../docs/tableau/Task 7.1 - Price per Person by Borough.png)

*Hình 7.1. Median chi phí mỗi người theo borough và room type*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX: phân biệt borough (C) → đúng.
- PosY (Length từ 0): thể hiện giá trị MEDIAN price/person (Q) → đúng, Length là channel chính xác nhất cho Q.
- Hue Color: phân biệt room type (C) trong grouped bar → đúng.

Kết luận: Grouped Bar Chart là lựa chọn đúng đắn khi cần so sánh đồng thời theo 2 chiều categorical (borough × room type).

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Length (chiều dài cột từ gốc 0) theo Stevens' Law n = 1.0 — cực kỳ chính xác. Label số trên đầu cột loại bỏ sai số cảm nhận hoàn toàn.
- **Discriminability:** 3–4 màu (room types) trong phạm vi ≤ 7 → phân biệt tốt. Grouped layout (không stack) cho phép so sánh trực tiếp từng room type giữa các borough.
- **Separability:** PosX, PosY và Color hoạt động độc lập tốt. Grouped bar rõ ràng hơn stacked bar vì không có hiện tượng cộng dồn gây nhầm lẫn.

#### C. Phân tích biểu đồ

- Entire home/apt (cam) có price/person cao nhất ở Brooklyn ($191) và Queens ($114) — tuy nhiên khi chia theo đầu người trong nhóm lớn, đây vẫn có thể rẻ hơn Private room ở Manhattan.
- Private room (đỏ) và Shared room (xanh lá) luôn có price/person thấp hơn Entire home, phù hợp cho khách du lịch solo hoặc đôi.
- Bronx và Staten Island có price/person thấp nhất trong mọi room type — lựa chọn tối ưu cho nhóm khách ngân sách thấp.

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
| **Why** | **discover → explore**<br>Phát hiện xu hướng giảm của price/person khi sức chứa tăng (economies of scale). Khám phá sự khác biệt về trend này giữa các loại phòng khác nhau. |
| **Scale** | Key: 16 (giá trị accommodates 1–16)<br>Color: 4 (room type) |

![Hình 7.2. Mối quan hệ giữa sức chứa và chi phí mỗi người](../docs/tableau/Task 7.2 - Accommodates vs Price per Perso.png)

*Hình 7.2. Mối quan hệ giữa sức chứa và chi phí mỗi người*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Accommodates): Q/Ordinal → position thích hợp.
- PosY (MEDIAN price/person): Q → position thích hợp.
- Hue Color: Room Type (C) → đúng, phân biệt 3–4 loại phòng.
- Trend Line: hiển thị xu hướng tổng thể → tăng thêm thông tin về dependency.

Kết luận: Scatter plot với Trend Line là lựa chọn chuẩn mực nhất để phân tích mối quan hệ giữa 2 biến Q.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosX và PosY (n = 1.0) — rất chính xác. Trend Line (dashed) thể hiện xu hướng dốc xuống rõ ràng. Mỗi điểm là MEDIAN của một nhóm accommodates × room type — aggregation giúp giảm nhiễu so với raw data.
- **Discriminability:** 3 màu room type (xanh, đỏ, cam) dễ phân biệt. Số lượng điểm vừa phải (~42 marks) không bị clutter. Trend lines màu tương ứng với điểm giúp tracking dễ dàng.
- **Separability:** PosX, PosY và Color tách biệt hoàn toàn. Trend lines không làm rối các điểm dữ liệu thực.

#### C. Phân tích biểu đồ

- Trend line của Entire home/apt (cam) dốc xuống mạnh nhất — xác nhận "economies of scale": càng nhiều người, giá mỗi người càng giảm. Sweet spot ở 4–6 người.
- Private room (xanh) gần như phẳng — sức chứa không ảnh hưởng nhiều đến price/person, vì mỗi phòng chỉ cho 1–2 người.
- Với 4+ người, Entire home trở nên rẻ hơn Private room tính theo đầu người — insight quan trọng cho nhóm du lịch.

---

## Task 8 — Phân tích Tính Mùa vụ và Cơ hội Đặt phòng (Seasonality & Booking Opportunity)

**Câu hỏi nghiệp vụ:** *"Tỷ lệ lấp đầy (occupancy rate) thay đổi như thế nào qua các tháng trong năm? Chính sách số đêm tối thiểu (minimum nights) ảnh hưởng như thế nào đến occupancy theo mùa?"*

Mục đích: Xác định mùa cao điểm/thấp điểm của thị trường Airbnb NYC và tìm hiểu mối quan hệ giữa chính sách minimum nights với tỷ lệ lấp đầy, từ đó hỗ trợ host và khách hàng tối ưu chiến lược.

---

### 8.1. Biểu đồ 1: Tỷ lệ lấp đầy theo tháng (Line Chart)

#### A. Idiom

| **Idiom** | **Line Chart (Multi-line)** |
|---|---|
| **What** | Month: Ordinal (tháng 1–12, có thứ tự)<br>Year: Categorical (2024/2025)<br>Occupancy Rate Pct: Quantitative (calculated: AVG(is_booked) × 100) |
| **How — Encode** | Mark: Line + Point<br>Channel:<br>— PosX: Month (Ordinal, Discrete — tiến trình thời gian tháng 1–12)<br>— PosY: Occupancy Rate (%) (Quantitative, position)<br>— Hue Color: Year (Categorical — so sánh 2024 vs 2025) |
| **How — Manipulate** | Selection: hover để xem tháng, năm, occupancy rate (%) cụ thể |
| **How — Facet** | Superimpose: Reference Line (average occupancy ngang) đặt lên biểu đồ |
| **How — Reduce** | Filter: year (optional — để focus vào 1 năm cụ thể) |
| **Why** | **discover → browse**<br>Phát hiện xu hướng mùa vụ (seasonality) trong dữ liệu occupancy. Duyệt qua từng tháng để xác định high season và low season tại thị trường Airbnb NYC. |
| **Scale** | Key: 12 (tháng)<br>Color: 2 (năm: 2024, 2025) |

![Hình 8.1. Tỷ lệ lấp đầy (occupancy rate) theo tháng tại NYC](../docs/tableau/Task 8.1 - Monthly Occupancy Rate.png)

*Hình 8.1. Tỷ lệ lấp đầy (occupancy rate) theo tháng tại NYC*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Month — Ordinal): trục thời gian có thứ tự → đúng, Ordinal phù hợp với Position.
- PosY (Occupancy Rate — Q): thể hiện mức độ lấp đầy → đúng.
- Hue Color: phân biệt Year (C) → đúng — Line chart kết hợp Hue Color là chuẩn mực phân tích time series theo nhóm.

Kết luận: Line chart là idiom tối ưu cho dữ liệu chuỗi thời gian (time series), đặc biệt khi cần phát hiện trend và seasonality.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** PosY (vị trí điểm trên thang đo chung) có n = 1.0 theo Stevens' Law — rất chính xác. Người xem dễ dàng so sánh mức occupancy giữa các tháng và nhận diện tháng cao điểm/thấp điểm.
- **Discriminability:** 2 đường (2 năm) rất dễ phân biệt. Reference line Average tạo mốc tham chiếu giúp nhanh chóng xác định tháng nào trên/dưới trung bình. Line chart thể hiện liên tục của dữ liệu theo thời gian tốt hơn bar chart.
- **Separability:** PosX (thời gian) và PosY (occupancy) và Color (năm) tách biệt hoàn toàn. Không có hiện tượng nhiễu giữa các kênh.

#### C. Phân tích biểu đồ

- Tháng 1–4 là low season rõ rệt (occupancy ~20–21%), thị trường trống phòng nhiều — cơ hội tốt cho khách muốn giá rẻ.
- Từ tháng 5 trở đi, occupancy tăng dần và đạt đỉnh vào tháng 11 (~40%) — phản ánh nhu cầu du lịch mùa thu và dịp lễ Thanksgiving cuối năm.
- Trend tăng dần theo thời gian cho thấy thị trường Airbnb NYC đang phục hồi và tăng trưởng, với occupancy năm sau cao hơn năm trước ở cùng tháng.

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
| **Why** | **discover → compare**<br>Phát hiện pattern phân bố occupancy rate theo 2 chiều đồng thời (tháng × chính sách minimum nights). So sánh hiệu quả của từng chính sách qua các tháng trong năm. |
| **Scale** | Key: 12 (tháng)<br>Bin: 3 (nhóm minimum nights: Short ≤3, Medium ≤7, Long >7) |

![Hình 8.2. Heatmap tỷ lệ lấp đầy theo tháng và chính sách minimum nights](../docs/tableau/Task 8.2 - Heatmap Occupancy.png)

*Hình 8.2. Heatmap tỷ lệ lấp đầy theo tháng và chính sách minimum nights*

#### B. Đánh giá biểu đồ

**1. Tính biểu đạt (Expressiveness):**

- PosX (Month — O): trục thời gian theo thứ tự → đúng.
- PosY (Minimum Nights Group — C): phân loại chính sách → đúng.
- Color (Luminance/Sequential): thể hiện độ lớn occupancy (Q) → phù hợp — màu đậm/nhạt biểu diễn biến liên tục hiệu quả trong ma trận.

Kết luận: Heatmap là idiom phù hợp nhất khi cần phân tích dữ liệu 3 chiều (Month × Group × Value) đồng thời trong không gian hạn chế.

**2. Tính hiệu quả (Effectiveness):**

- **Accuracy:** Kênh Color (Luminance) biểu diễn Q theo Stevens' Law — n phụ thuộc độ tương phản, Log_error ≈ T9 ± 2.5. Hạn chế: khó ước lượng chính xác mức chênh lệch % giữa hai ô. Tuy nhiên mục tiêu của heatmap là phát hiện pattern (so sánh ordinal: cao/thấp), không phải đọc giá trị chính xác — nên hạn chế này có thể chấp nhận.
- **Discriminability:** 3 × 12 = 36 ô vuông đều nhau. Sequential palette (xanh nhạt → đậm) giúp phân biệt được ~5–7 cấp độ màu. Kích thước ô đều nhau loại bỏ nhiễu từ Area — người xem chỉ tập trung vào màu sắc.
- **Separability:** PosX, PosY và Color kết hợp tốt, không bị nhiễu lẫn nhau. Area đồng đều (ô vuông bằng nhau) không tạo ra bias về kích thước.

#### C. Phân tích biểu đồ

- Short minimum stay (≤3 đêm) có occupancy cao và ổn định quanh năm — chính sách linh hoạt thu hút nhiều khách nhất, đặc biệt trong mùa thấp điểm.
- Long minimum stay (>7 đêm) có occupancy thấp hơn trong phần lớn các tháng, nhưng có xu hướng tăng vào cuối năm — phù hợp cho khách công tác dài hạn.
- Tháng 11–12 có màu đậm nhất ở hầu hết các nhóm — xác nhận đây là high season với nhu cầu đặt phòng cao bất kể chính sách minimum nights.
- Host muốn tối đa hóa occupancy nên áp dụng Short minimum stay trong mùa thấp điểm (tháng 1–4) và có thể nâng minimum nights vào cao điểm.
