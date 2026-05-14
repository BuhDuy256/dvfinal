# Step 08 — [Minor] Thêm reference line vào Chart 5.1 để hỗ trợ "Locate Extremes"

## Vấn đề

Chart 5.1 "Price Distribution by Borough" hiện tại hiển thị phân bố giá theo quận tốt nhưng **không có điểm tham chiếu chung** để người dùng nhanh chóng xác định quận nào đắt/rẻ hơn mức trung bình NYC.

**Task 5 yêu cầu (midterm_report):**
> Action: "Locate" → Target: "Extremes" — Xác định vị trí của các quận đắt đỏ nhất và rẻ nhất.

Hiện tại người dùng phải dùng mắt so sánh vị trí của từng box — tốn cognitive load và dễ sai khi các IQR chồng lấp nhau (Queens ≈ Staten Island ≈ Bronx).

## Cách sửa trong Tableau

### Phương án A — Thêm Reference Line = Median toàn NYC (khuyến nghị)

1. Right-click vào trục Y → **Add Reference Line**
2. Scope: **Table**
3. Value: `Median` của `Price` (hoặc nhập hằng số = median đã tính, ví dụ $120)
4. Label: **"NYC Median ($120)"**
5. Line style: dashed, màu xám đậm hoặc cam
6. Tooltip: "NYC-wide median price"

**Kết quả:** Người dùng ngay lập tức thấy Manhattan vượt xa median, Queens/Staten Island/Bronx nằm dưới.

### Phương án B — Thêm Reference Band cho IQR toàn NYC

1. Right-click trục Y → **Add Reference Line** → chọn **Band**
2. Từ Q1 đến Q3 của Price (IQR toàn NYC)
3. Màu nền nhạt, label "NYC IQR"
4. Giúp người dùng thấy quận nào có median trong vùng "bình thường" so với toàn thị trường

### Phương án C — Thêm annotation tại median của mỗi box

1. Bật **Show Mark Labels** → chọn hiển thị Median value
2. Hoặc tạo dual axis: scatter plot các giá trị median theo borough (dùng calculated field `MEDIAN([Price])`)
3. Label các điểm median = $79 (Bronx), $99 (Staten Is), $100 (Queens), $129 (BK), $200 (Manhattan)

*(Phương án C đã được thực hiện một phần ở Chart 5.2 — nếu giữ nguyên Chart 5.2 thì Phương án A cho Chart 5.1 là đủ)*

## Lưu ý về Color Hue trong Chart 5.1

Chart 5.1 dùng **Color Hue = Room Type** nhưng box chỉ là 1 box chung per borough (không tách theo room type). Điều này tạo ra kỳ vọng sai cho người dùng.

**Hai hướng xử lý:**

**Hướng 1 — Đơn giản hóa**: Xóa Color Hue = Room Type, giữ box + points đơn sắc. Chart rõ hơn, không gây hiểu nhầm.

**Hướng 2 — Nhất quán hóa**: Tách box theo Room Type (tạo box per Borough × Room Type). Khi đó Color Hue = Room Type có nghĩa và hỗ trợ "Compare Distribution" theo room type trong từng quận.

## Cập nhật mô tả idiom trong báo cáo

> "Chart 5.1 sử dụng box plot để hiển thị phân bố giá theo từng quận NYC. Reference line ngang tại mức median toàn NYC ($120) giúp người dùng nhanh chóng xác định quận nào có mức giá cao/thấp hơn trung bình thị trường (action: Locate Extremes). Individual points được overlay lên box để giữ nguyên density information."

## Checklist sau khi sửa

- [ ] Reference line (median NYC) đã được thêm vào Chart 5.1
- [ ] Label của reference line rõ ràng (giá trị cụ thể)
- [ ] Color Hue = Room Type đã được quyết định: xóa hoặc tách box riêng
- [ ] Caption đã cập nhật đề cập đến reference line

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 5 → Vấn đề #3 [Minor]
- Task Abstraction: `midterm_report.pdf` → Section 2.5 → Search: Action "Locate" → Target "Extremes"
