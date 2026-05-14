# Review tổng quan

Phần idiom design của Bảo Duy (Task 5–8) có mức độ phủ task tương đối tốt — 2 chart mỗi task, hướng đúng vào data attributes đã khai báo trong midterm_report. Tuy nhiên có **một lỗi nghiêm trọng (Critical)** ở Task 6 làm sai hoàn toàn mục tiêu chart, **một lỗi Medium** về filter thời gian ở Task 8, và **nhiều lỗi Minor** về channel dư thừa (Color Hue lặp lại PosX) xuất hiện ở Task 5, 6, 7. Bản hiện tại chưa sẵn sàng nộp nếu chưa sửa Chart 6.1.

---

# Review chi tiết theo Domain Task

---

## Domain Task 5

### Task abstraction từ midterm_report

- **Action:** Discover, Explore, Locate, Compare, Summarize
- **Target:** Distribution, Features, Extremes
- **Data attributes:** `price` (Q, Continuous), `neighbourhood_group_cleansed` (C, Nominal), `room_type` (C, Nominal)
- **Mục tiêu người dùng:** Hiểu mức giá thuê chênh lệch như thế nào giữa 5 quận NYC; nhận biết quận nào đắt/rẻ nhất; khám phá phân bố giá theo loại phòng trong từng quận.

### Idiom design hiện tại

- **Chart 5.1:** Box plot — "Price Distribution by Borough"
  - Mark: Box + Point (jittered overlay)
  - Channel: PosX = Borough (Nominal), PosY = Price (Quantitative), Color Hue = Room Type (Nominal)
  - Filter: `Price Is Outlier = False`

- **Chart 5.2:** Bar chart — "Median Price by Borough"
  - Mark: Bar
  - Channel: PosX = Borough (Nominal), PosY = Median Price (Quantitative), Color Hue = Borough (Nominal), Label = giá trị median
  - Filter: `Price Is Outlier = False`

### Đánh giá theo 3 giai đoạn

**1. Task & Data Abstraction:**
Chart 5.1 phục vụ tốt action **Discover/Compare Distribution** — box plot hiển thị IQR, whisker, và individual points. Chart 5.2 phục vụ tốt action **Summarize + Locate Extremes** (median từng quận, Manhattan = $200 rõ ràng nhất). Hai chart bổ trợ nhau hợp lý: một hiển thị toàn phân bố, một tóm tắt central tendency. Task khớp tốt.

**2. Marks & Channels:**
- Chart 5.1: Mark = Box là lựa chọn chuẩn cho distribution. PosY = Price (Q) là channel mạnh nhất — đúng. Color Hue = Room Type encode thêm chiều categorical là hợp lý về mặt nguyên tắc. Tuy nhiên, box chỉ vẽ **một box duy nhất** cho toàn borough, các điểm màu room type chỉ overlay lên trên — người dùng không thể so sánh distribution của từng room type một cách chính xác (không có box riêng theo room type).
- Chart 5.2: Color Hue = Borough trong khi PosX đã là Borough — đây là **channel dư thừa**. Theo Mackinlay, với dữ liệu Nominal, Color Hue phù hợp, nhưng khi Position đã encode cùng attribute thì Color Hue không bổ sung thêm thông tin. 5 màu khác nhau cho 5 cột không giúp phân biệt tốt hơn vì các cột đã được tách biệt bởi vị trí.

**3. Perceptual Check:**
- Chart 5.1: Dễ đọc. Trục giá rõ. Tuy nhiên, các điểm cá thể chồng lấp khá nhiều (overplotting) đặc biệt ở Manhattan và Brooklyn. Không có baseline annotation (e.g., reference line trung bình NYC) để hỗ trợ "Locate Extremes" nhanh hơn.
- Chart 5.2: Rất rõ ràng. Label trực tiếp trên bar ($200, $129...) giúp người dùng đọc giá trị ngay mà không cần dò trục Y. Tốt.
- Chuỗi nhiệm vụ: 5.1 (overview distribution) → 5.2 (summary ranking) là flow hợp lý.

### Vấn đề phát hiện

1. **[Minor]** Chart 5.1: Box plot chỉ vẽ **một box chung** cho toàn borough, trong khi Color Hue encode Room Type — người dùng kỳ vọng thấy box riêng theo room type nhưng thực tế không có. Gây hiểu nhầm về vai trò của Color Hue.
2. **[Minor]** Chart 5.2: Color Hue = Borough là channel dư thừa với PosX = Borough. Không vi phạm nghiêm trọng nhưng lãng phí channel và tạo thêm legend không cần thiết.
3. **[Minor]** Chart 5.1 không có reference line (ví dụ median toàn NYC) để hỗ trợ "Locate Extremes" trực quan hơn.

### Đề xuất sửa

- Chart 5.1: Thêm **reference line = Median giá toàn NYC** (constant line) trên PosY để hỗ trợ "Locate Extremes". Hoặc tách box theo room_type (tạo box plot theo nhóm Borough × Room Type) nếu muốn Color Hue có nghĩa.
- Chart 5.2: **Xóa Color Hue** (hoặc giữ 1 màu trung tính cho tất cả bars). Dùng Color Luminance nếu muốn highlight cột cao nhất/thấp nhất.

---

## Domain Task 6

### Task abstraction từ midterm_report

- **Action:** Discover, Explore, Locate, Compare
- **Target:** Outliers, Features, Dependency
- **Data attributes:** `price_is_outlier` (C, derived flag), `price` (Q), `review_scores_rating` (Q), `latitude/longitude` (Q, spatial), `neighbourhood_group_cleansed` (C), `room_type` (C)
- **Mục tiêu người dùng:** (1) Tìm các listing bị gắn cờ ngoại lệ giá (`price_is_outlier = True`) và xác định chúng tập trung ở đâu không gian; (2) Nhận diện "món hời" (giá dưới trung vị nhưng rating cao) trong cùng khu vực/loại phòng.

### Idiom design hiện tại

- **Chart 6.1:** Point map — "Price Outlier Map"
  - Mark: Point trên bản đồ NYC
  - Channel: PosXY = Longitude/Latitude, Color Hue = Price Is Outlier (True/False), Size = Price
  - Filter: **`Price Is Outlier = False`** (giữ lại các listing KHÔNG phải outlier)

- **Chart 6.2:** Scatter plot — "Price vs Rating"
  - Mark: Point
  - Channel: PosX = Price (Q), PosY = Review Scores Rating (Q), Color Hue = Good Deal Flag (Nominal), Size = Number Of Reviews (Q)
  - Reference lines: Median price (dọc), Good Deal threshold 4.8 (ngang)
  - Filter: `Price Is Outlier = False`, `Number Of Reviews >= 5`

### Đánh giá theo 3 giai đoạn

**1. Task & Data Abstraction:**
- Chart 6.1 **bị lệch hoàn toàn với task**: Task yêu cầu **Locate Outliers** — tức là hiển thị các listing có `price_is_outlier = True` trên bản đồ. Nhưng filter đang giữ `False`, tức là chỉ hiển thị các listing bình thường. Đây là lỗi nghiêm trọng làm đảo ngược mục đích chart.
- Chart 6.2 phục vụ đúng mục tiêu thứ hai ("món hời" = giá thấp hơn median + rating cao) qua action **Compare Dependency** giữa price và rating. Tuy nhiên, filter `Price Is Outlier = False` ở Chart 6.2 là hợp lý (loại outlier giá trước khi tìm good deal).

**2. Marks & Channels:**
- Chart 6.1: Mark = Point trên map là đúng cho spatial data. Tuy nhiên do filter sai, toàn bộ encoding Color Hue = Price Is Outlier không có ý nghĩa (chỉ còn màu False). Size = Price là channel yếu cho việc so sánh chính xác — ổn nếu chỉ để context.
- Chart 6.2: PosX = Price (Q) và PosY = Rating (Q) là hai channel mạnh nhất — đúng. Color Hue = Good Deal Flag (Nominal) phân biệt rõ 2 nhóm bằng màu xanh/xám — hợp lý. Size = Number Of Reviews: channel yếu (area/size ít chính xác), dùng như "tín hiệu độ tin cậy" là chấp nhận được nhưng tạo thêm visual clutter. Reference lines giúp định nghĩa "Good Deal" trực quan — tốt.

**3. Perceptual Check:**
- Chart 6.1: Rất khó đọc — map quá nhỏ trong ảnh, các điểm chồng lấp dày đặc. Không thể phân biệt vị trí tập trung của outlier (và thực ra không có outlier nào hiển thị do filter).
- Chart 6.2: Vùng trên-trái (rating cao, giá thấp) bị overplotting nặng — rất nhiều điểm chồng nhau. Green = "Good Deal" khó tách biệt với nền xám do độ bão hòa màu không đủ tương phản trong vùng đông điểm. Reference lines hỗ trợ tốt việc chia không gian thành 4 quadrant. Chuỗi nhiệm vụ: map spatial (6.1) → scatter dependency (6.2) là flow logic nhưng Chart 6.1 đang sai filter.

### Vấn đề phát hiện

1. **[Critical]** Chart 6.1: Filter `Price Is Outlier = False` giữ lại NON-outliers. Task yêu cầu tìm và locate các listing có `price_is_outlier = True`. Toàn bộ mục đích của map bị đảo ngược. Không một outlier nào được hiển thị.
2. **[Medium]** Chart 6.2: Overplotting nặng ở vùng điểm tập trung (rating 4.5–5.0, price 0–150). Good Deal points bị che khuất bởi Normal points. Khó "Locate" các "món hời" cụ thể.
3. **[Minor]** Chart 6.2: Size = Number Of Reviews là channel thứ ba khó đọc; nếu mục tiêu là "độ tin cậy", có thể dùng Transparency hoặc Filter thay thế.

### Đề xuất sửa

- **Chart 6.1 — Phải sửa:** Đổi filter thành **`Price Is Outlier = True`** (hoặc hiển thị cả hai True/False nhưng làm nổi bật outlier). Color Hue nên encode outlier = True bằng màu nổi bật (đỏ/cam), non-outlier màu xám mờ. Tăng kích thước điểm outlier để pop-out. Phóng to map hoặc thêm tooltip chi tiết.
- **Chart 6.2:** Thêm **Jitter** hoặc dùng **opacity thấp hơn** (transparency) để giảm overplotting. Hoặc thêm filter Borough/Room Type để người dùng drill-down theo khu vực.

---

## Domain Task 7

### Task abstraction từ midterm_report

- **Action:** Discover, Explore, Compare, Summarize
- **Target:** Dependency, Features, Distribution
- **Data attributes:** `price` (Q), `accommodates` (Q, Discrete), `neighbourhood_group_cleansed` (C), `room_type` (C), derived `price_per_person = price / accommodates`
- **Mục tiêu người dùng:** Khu vực nào mang lại giá trị tốt nhất tính trên đầu người; chi phí bình quân đầu người thay đổi như thế nào khi quy mô nhóm khách tăng lên.

### Idiom design hiện tại

- **Chart 7.1:** Grouped bar chart — "Price per Person by Borough"
  - Mark: Bar
  - Channel: PosX = Room Type (Nominal, trong panel), PosY = Median Price Per Person (Q), Color Hue = Room Type (Nominal), Panel (Column) = Borough, Label = giá trị
  - Filter: `Price Is Outlier = False`

- **Chart 7.2:** Scatter + Trend lines — "Accommodates vs Price per Person"
  - Mark: Point + Line (trend per room type)
  - Channel: PosX = Accommodates (Q/Ordinal), PosY = Median Price Per Person (Q), Color Hue = Room Type (Nominal), Trend line per group
  - Filter: `Price Is Outlier = False`, `Accommodates 1–16`

### Đánh giá theo 3 giai đoạn

**1. Task & Data Abstraction:**
- Chart 7.1 phục vụ action **Compare Distribution** (chi phí đầu người giữa các khu vực và loại phòng) — hợp lý. Tuy nhiên, task abstraction của Task 7 đặt **Dependency** là action chính (giữa accommodates và chi phí bình quân). Chart 7.1 không encode `accommodates` — đây là lệch action chính.
- Chart 7.2 phục vụ đúng action **Discover Dependency** — scatter + trend line cho thấy khi số người tăng, chi phí đầu người giảm như thế nào. Đây là chart quan trọng nhất của Task 7.
- Nhìn chung, cặp chart phủ được cả Distribution lẫn Dependency, nhưng thứ tự ưu tiên có thể nên đặt Chart 7.2 trước.

**2. Marks & Channels:**
- Chart 7.1: Color Hue = Room Type dư thừa với PosX = Room Type (tương tự lỗi Chart 5.2). Panel (Column) = Borough là cách encode spatial hierarchy hợp lý. Mark = Bar + PosY = Median Price Per Person: đúng theo Mackinlay cho Quantitative.
- Chart 7.2: Mark = Point (aggregated median per Accommodates) + Line (trend) là kết hợp tốt để thể hiện dependency. Color Hue = Room Type giúp tách biệt 4 nhóm — hợp lý khi chỉ có 4 category (discriminability tốt). Trend line = linear regression — tốt cho showing overall direction, nhưng Hotel room có chỉ vài điểm dữ liệu (1–8 accommodates) nên trend line của Hotel room xuống rất dốc và có thể misleading (extrapolation vượt ra ngoài phạm vi dữ liệu thực).

**3. Perceptual Check:**
- Chart 7.1: Rõ ràng, dễ đọc. Label giá trị trực tiếp là tốt. Tuy nhiên, với 5 borough × 4 room type = 20 bars, chart khá đông. Brooklyn Hotel room ($191) là anomaly rõ ràng — người dùng có thể bị phân tâm muốn kiểm tra lại dữ liệu này.
- Chart 7.2: Rõ ràng hơn. Trend lines giúp thấy pattern giảm dần theo accommodates. Hotel room trend line có dấu hiệu **extrapolation** (line tiếp tục dốc về phía 0 ở accommodates = 10) gây ra giá trị âm hoặc phi thực tế khi nhìn nhanh — có thể gây hiểu nhầm. Color Hue = 4 room types: phân biệt được, pop-out tốt.

### Vấn đề phát hiện

1. **[Minor]** Chart 7.1: Color Hue = Room Type dư thừa với PosX = Room Type. Không sai nhưng thêm legend không cần thiết.
2. **[Medium]** Chart 7.2: Hotel room trend line dốc bất thường (từ $150 xuống ~$0 tại accommodates = 10) có thể do sample size nhỏ — thiếu annotation hoặc disclaimer về số lượng điểm dữ liệu ít ở Hotel room. Có thể gây hiểu sai về "Hotel room trở thành rẻ nhất khi nhiều người".
3. **[Minor]** Chart 7.1: Thứ tự ưu tiên — Task 7's primary action là Dependency (accommodates vs price per person), nhưng Chart 7.1 (Distribution) được đặt trước Chart 7.2 (Dependency). Nên đặt 7.2 làm chart chính, 7.1 làm chart bổ trợ.

### Đề xuất sửa

- Chart 7.1: Xóa Color Hue = Room Type (giữ 1 màu neutral, hoặc chỉ highlight giá trị cao nhất/thấp nhất bằng màu khác).
- Chart 7.2: Thêm **annotation** hoặc **tooltip** giải thích số lượng listing trong mỗi nhóm Accommodates theo Room Type. Xem xét dùng **Band/Confidence interval** thay cho raw trend line để tránh overstatement. Hoặc **lọc bỏ Hotel room** khỏi trend line nếu sample quá nhỏ.

---

## Domain Task 8

### Task abstraction từ midterm_report

- **Action:** Discover, Browse, Locate, Compare
- **Target:** Trends, Extremes, Dependency
- **Data attributes:** `month` (O, Cyclic), `occupancy_rate_pct` (Q, derived), `minimum_nights` (Q → grouped: Short/Medium/Long)
- **Mục tiêu người dùng:** Quan sát tỷ lệ lấp đầy theo các tháng; nhận diện mùa cao/thấp điểm; xem ràng buộc `minimum_nights` có ảnh hưởng đến occupancy không.

### Idiom design hiện tại

- **Chart 8.1:** Line chart — "Monthly Occupancy Rate"
  - Mark: Line
  - Channel: PosX = Month (Ordinal, 1–12), PosY = Occupancy Rate % (Q), Reference line = Average (horizontal)
  - Filter: **`Year >= 2026`**, Month 1–12

- **Chart 8.2:** Heatmap — "Heatmap Occupancy"
  - Mark: Cell (rectangle)
  - Channel: PosX = Month (Ordinal, 1–12), PosY = Minimum Nights Group (Ordinal: Long/Medium/Short), Color Luminance = Occupancy Rate Pct (Q, sequential)

### Đánh giá theo 3 giai đoạn

**1. Task & Data Abstraction:**
- Chart 8.1 phục vụ tốt action **Discover/Browse Trends** và **Locate Extremes** (tháng nào peak, reference line average). Line chart là mark chuẩn cho temporal trend.
- Chart 8.2 phục vụ đúng action **Discover/Compare Dependency** giữa `minimum_nights` group và occupancy theo tháng — heatmap cross-tab rất phù hợp để thấy pattern này. Đây là thiết kế tốt và đúng task abstraction.
- Task phủ đầy đủ các action: Trends (8.1), Extremes (8.1 với reference line), Dependency (8.2).

**2. Marks & Channels:**
- Chart 8.1: Mark = Line phù hợp cho sequential temporal data (Month là Ordinal Cyclic). PosX/PosY = channel mạnh nhất — đúng. Reference line = Average là annotation tốt (không phải encoding chính), đúng vai trò bổ trợ. Thiếu Color Hue hay channel phụ nào — chart đơn giản, đọc nhanh.
- Chart 8.2: Mark = Cell phù hợp cho matrix (Month × Group). PosX/PosY = channel mạnh nhất cho 2 chiều categorical/ordinal — đúng. Color Luminance = Occupancy Rate Pct: theo Mackinlay, Color Luminance phù hợp cho Quantitative sequential — đúng. Palette sequential (sáng → tối) biểu đạt tốt "thấp → cao".

**3. Perceptual Check:**
- Chart 8.1: Đường trend rõ ràng, tăng mạnh từ tháng 5. Reference line "Average" giúp người dùng nhận ra tháng nào trên/dưới trung bình. **Vấn đề:** Filter `Year >= 2026` khiến dữ liệu chỉ là năm 2026 — nhưng dữ liệu Airbnb calendar thường là **forward-looking availability**, không phải historical actual occupancy. Nếu data 2026 là dự báo/availability, thì tháng 8–11 tăng cao có thể phản ánh listing đang mở lịch sẵn, không phải thực tế đặt phòng. Cần kiểm tra lại nguồn dữ liệu. Thêm vào đó, Month 12 không hiển thị (thiếu data).
- Chart 8.2: Màu sequential xanh dương rõ ràng. Short minimum stay rõ ràng có màu đậm hơn (occupancy cao hơn) ở các tháng mùa cao điểm — insight nổi bật. Tuy nhiên chart rất hẹp/mỏng theo chiều dọc (chỉ 3 hàng), khó so sánh độ đậm nhạt chính xác giữa các ô nhỏ. Tháng 12 cũng bị thiếu.

### Vấn đề phát hiện

1. **[Medium]** Chart 8.1: Filter `Year >= 2026` có thể làm lệch kết quả nếu dữ liệu 2026 là availability data (forward-looking) chứ không phải actual occupancy. Trend "tháng 8–11 cao nhất" có thể là artifact của data chứ không phải seasonal pattern thực. Không có note giải thích cho người xem.
2. **[Minor]** Chart 8.1: Trục X dùng số tháng (1, 2, 3...) thay vì tên tháng (Jan, Feb...) — giảm readability.
3. **[Minor]** Chart 8.2: Không có annotation giải thích threshold định nghĩa "Short/Medium/Long minimum_nights". Người xem không biết Short = 1–3 đêm hay khác.
4. **[Minor]** Chart 8.2: Tháng 12 không hiển thị dữ liệu — cần ghi chú rõ "dữ liệu chưa có" thay vì để ô trống.

### Đề xuất sửa

- Chart 8.1: Thêm **note/annotation** giải thích rằng dữ liệu 2026 là availability-based estimate. Hoặc bổ sung so sánh 2024/2025 (nếu có) để validate seasonal pattern. Đổi số tháng thành tên tháng viết tắt.
- Chart 8.2: Thêm **tooltip hoặc subtitle** giải thích định nghĩa nhóm (ví dụ: Short = minimum_nights ≤ 3, Medium = 4–7, Long ≥ 8). Nếu tháng 12 thiếu dữ liệu thực, dùng màu trắng với ký hiệu "N/A" thay vì ô trống.

---

# Bảng tổng hợp lỗi cần sửa

| Vị trí | Mức độ | Vấn đề | Lý do | Cách sửa đề xuất |
|--------|--------|---------|-------|------------------|
| Chart 6.1 — Price Outlier Map | **Critical** | Filter `Price Is Outlier = False` khiến KHÔNG có outlier nào được hiển thị trên bản đồ — đảo ngược hoàn toàn mục đích chart | Task 6 yêu cầu **Locate Outliers** (giá bất thường) trên bản đồ; filter hiện tại loại bỏ tất cả outlier trước khi render | Đổi filter thành `Price Is Outlier = True`; dùng màu nổi bật (đỏ) cho outlier, màu xám nhạt cho non-outlier làm nền context |
| Chart 8.1 — Monthly Occupancy Rate | **Medium** | Filter `Year >= 2026` có thể tạo ra dữ liệu không phản ánh seasonal pattern thực nếu data 2026 là forward availability | Calendar data của Airbnb thường là availability schedule, không phải actual booking — tháng 8–11 "cao" có thể là artifact | Kiểm tra lại nguồn data; nếu dùng 2026, thêm annotation giải thích rõ; hoặc dùng nhiều năm để trung bình hóa seasonal pattern |
| Chart 7.2 — Accommodates vs Price per Person | **Medium** | Hotel room trend line dốc bất thường (extrapolates xuống 0 tại accommodates = 10) do ít data points | Với hotel room, accommodates lớn rất hiếm → trend line không đại diện → gây hiểu nhầm về cost efficiency | Thêm annotation số lượng điểm dữ liệu; dùng dashed line cho vùng ít data; hoặc loại Hotel room ra khỏi trend line |
| Chart 5.2 — Median Price by Borough | **Minor** | Color Hue = Borough dư thừa với PosX = Borough | Channel lặp không bổ sung thêm thông tin; thêm legend không cần thiết | Xóa Color Hue hoặc dùng 1 màu neutral, chỉ highlight Manhattan bằng màu khác |
| Chart 7.1 — Price per Person by Borough | **Minor** | Color Hue = Room Type dư thừa với PosX = Room Type | Tương tự Chart 5.2 — lãng phí channel, thêm noise visual | Xóa Color Hue hoặc giữ consistent với Chart 7.2 |
| Chart 6.2 — Price vs Rating | **Minor** | Overplotting nặng ở vùng rating 4.5–5.0, price 0–150; Good Deal points bị che | "Locate" các món hời cụ thể trở nên khó do chồng lấp điểm | Giảm opacity (~30–50%), hoặc thêm filter Borough/Room Type để drill-down; hoặc jitter |
| Chart 8.2 — Heatmap Occupancy | **Minor** | Không có annotation định nghĩa Short/Medium/Long minimum_nights; tháng 12 không có data nhưng không có ghi chú | Người xem không biết ngưỡng phân nhóm; ô trống tháng 12 gây hiểu nhầm là "0%" | Thêm subtitle hoặc tooltip định nghĩa nhóm; đánh dấu "N/A" cho ô thiếu data |
| Chart 8.1 — Monthly Occupancy Rate | **Minor** | Trục X dùng số (1–11) thay vì tên tháng | Giảm readability — người đọc phải tự map số → tháng | Đổi sang Jan, Feb, Mar... hoặc T1, T2... |

---

# Kết luận

**Bản hiện tại chưa sẵn sàng nộp** do lỗi Critical ở Chart 6.1. Cần sửa ít nhất 2 vấn đề trước khi nộp:

**Bắt buộc sửa trước khi nộp:**
1. **Chart 6.1:** Đổi filter `Price Is Outlier = False` → `True`. Đây là lỗi làm sai hoàn toàn mục tiêu của Task 6 — bộ giám khảo sẽ nhận ra ngay.
2. **Chart 8.1:** Kiểm tra lại nguồn dữ liệu `Year >= 2026`; nếu đây là availability data, cần thêm note giải thích hoặc điều chỉnh filter để dùng dữ liệu historical.

**Nên sửa để tăng chất lượng:**
3. Chart 5.2 và 7.1: Xóa Color Hue dư thừa.
4. Chart 7.2: Thêm annotation về Hotel room trend line.
5. Chart 6.2: Giảm overplotting.
6. Chart 8.2: Thêm định nghĩa nhóm minimum_nights.

**Phần đang làm tốt:**
- Task 5: Cặp box plot + bar chart phối hợp tốt, phủ đủ Distribution + Summarize.
- Task 7, Chart 7.2: Scatter + trend line thể hiện Dependency giữa accommodates và chi phí đầu người — đúng action chính.
- Task 8, Chart 8.2: Heatmap là lựa chọn idiom xuất sắc cho Dependency (minimum_nights group × tháng × occupancy) — đúng mark, đúng channel, dễ đọc pattern.
- Tất cả các chart đều filter outlier giá (`Price Is Outlier = False`) để tránh nhiễu — nhất quán và được giải thích rõ trong caption.
