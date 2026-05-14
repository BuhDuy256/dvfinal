# Step 06 — [Minor] Thêm định nghĩa nhóm minimum_nights và xử lý tháng 12 thiếu data ở Chart 8.2

## Vấn đề

Chart 8.2 "Heatmap Occupancy" có 2 vấn đề nhỏ:

### Vấn đề 1 — Thiếu định nghĩa nhóm minimum_nights

Trục Y hiển thị: **Long minimum stay / Medium minimum stay / Short minimum stay**

Nhưng **không có chỗ nào trong chart giải thích** ngưỡng phân chia:
- Short = minimum_nights ≤ ?
- Medium = minimum_nights từ ? đến ?
- Long = minimum_nights ≥ ?

Người xem không biết các nhóm này được phân chia như thế nào → không thể đánh giá insight một cách chắc chắn.

### Vấn đề 2 — Tháng 12 thiếu data nhưng không có ghi chú

Tháng 12 (cột cuối) xuất hiện nhưng ô để trống. Người xem có thể hiểu nhầm là occupancy = 0% thay vì "không có dữ liệu".

## Cách sửa

### Sửa Vấn đề 1 — Thêm định nghĩa nhóm

**Phương án A — Subtitle (khuyến nghị)**

Thêm subtitle hoặc caption vào chart:
> "Minimum Nights Groups: Short = 1–3 nights, Medium = 4–7 nights, Long ≥ 8 nights"

Trong Tableau:
1. Double-click vào vùng caption phía dưới chart
2. Gõ định nghĩa nhóm
3. Hoặc: dùng **Text object** trong Dashboard để đặt ghi chú bên cạnh chart

**Phương án B — Đổi tên nhóm trực tiếp (nếu có thể)**

Nếu nhóm được tạo từ Calculated Field trong Tableau:
```
IF [minimum_nights] <= 3 THEN "Short (1–3 nights)"
ELSEIF [minimum_nights] <= 7 THEN "Medium (4–7 nights)"
ELSE "Long (≥ 8 nights)"
END
```
Đổi tên nhóm thành dạng có ngưỡng luôn trong label → không cần subtitle thêm.

**Phương án C — Tooltip**

Thêm vào Tooltip của chart:
```
Minimum Nights Group: <Minimum Nights Group>
Definition: Short (1–3), Medium (4–7), Long (≥8)
Month: <Month>
Occupancy Rate: <AVG(Occupancy Rate Pct)>%
```

---

### Sửa Vấn đề 2 — Xử lý tháng 12 thiếu data

**Phương án A — Ẩn tháng 12**

Nếu tháng 12 hoàn toàn không có dữ liệu:
1. Vào **Filters** → thêm filter `Month` → bỏ chọn tháng 12
2. Heatmap sẽ hiển thị tháng 1–11 rõ ràng
3. Caption: "Data available for January through November."

**Phương án B — Hiển thị "N/A" thay ô trống**

Nếu muốn giữ tháng 12 để người dùng biết là missing:
1. Tạo calculated field:
   ```
   IF ISNULL(AVG([is_booked])) THEN "N/A" ELSE STR(ROUND(AVG([is_booked])*100, 1)) + "%" END
   ```
2. Thêm label vào cell
3. Gán màu riêng (trắng hoặc vạch chéo) cho cell N/A

**Phương án C — Giải thích trong caption (nhanh nhất)**

Thêm vào caption:
> "December data not available in current dataset snapshot."

---

## Cập nhật mô tả idiom trong báo cáo

Trong phần mô tả Chart 8.2, thêm:
> "Trục Y phân 3 nhóm theo chính sách minimum_nights: Short (1–3 đêm), Medium (4–7 đêm), Long (≥ 8 đêm). Color Luminance encode Occupancy Rate Pct theo thang sequential — ô càng tối, tỷ lệ lấp đầy càng cao. Dữ liệu có sẵn từ tháng 1 đến tháng 11."

## Checklist sau khi sửa

- [ ] Định nghĩa nhóm Short/Medium/Long đã xuất hiện trong chart (subtitle/caption/tên nhóm)
- [ ] Tháng 12 đã được ẩn hoặc đánh dấu "N/A" rõ ràng
- [ ] Caption tổng thể đã cập nhật
- [ ] Tooltip đã bổ sung thông tin nhóm

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 8 → Vấn đề #3, #4 [Minor]
- Task Abstraction: `midterm_report.pdf` → Section 2.8 → Query: Action "Compare" → Target "Dependency" (minimum_nights vs occupancy)
- Derived attribute: `midterm_report.pdf` → Data Abstraction → calendar_clean → `minimum_nights` (Constraint)
