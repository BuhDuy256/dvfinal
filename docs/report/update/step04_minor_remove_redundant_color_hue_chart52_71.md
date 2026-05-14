# Step 04 — [Minor] Xóa Color Hue dư thừa ở Chart 5.2 và Chart 7.1

## Vấn đề chung

Cả hai chart đang dùng **Color Hue encode cùng attribute với PosX** — đây là vi phạm nguyên tắc channel efficiency theo Mackinlay:

> Không dùng 2 channel để encode cùng 1 attribute, trừ khi có lý do cụ thể để redundant encode (ví dụ: accessibility cho colorblind).

| Chart | Channel dư thừa | Attribute bị encode 2 lần |
|-------|-----------------|--------------------------|
| Chart 5.2 | Color Hue = Borough | PosX đã là Borough |
| Chart 7.1 | Color Hue = Room Type | PosX đã là Room Type (trong panel) |

## Hậu quả

- Thêm **legend không cần thiết** chiếm diện tích chart
- Tạo **visual noise** — người xem mất thêm thời gian xử lý legend dù nó không mang thông tin mới
- Đặc biệt Chart 5.2: 5 màu sắc rực rỡ trên bar chart 1 dimension làm chart trông "busy" hơn mức cần thiết

---

## Cách sửa Chart 5.2 — Median Price by Borough

### Phương án A — Xóa Color Hue, dùng 1 màu neutral (khuyến nghị)

1. Kéo `Neighbourhood Group Cleansed` ra khỏi **Color shelf**
2. Chọn màu neutral cho tất cả bars: `#4E79A7` (xanh đơn sắc)
3. Kết quả: chart sạch hơn, tập trung vào PosY (Median Price)

### Phương án B — Highlight outlier bằng Color Luminance

1. Xóa Color Hue = Borough
2. Tạo calculated field: `IF [Neighbourhood Group Cleansed] = "Manhattan" THEN "Highest" ELSE "Others" END`
3. Đưa calculated field vào **Color shelf**
4. Gán màu: "Highest" = cam đậm, "Others" = xám nhạt
5. Kết quả: Manhattan nổi bật, các quận còn lại đồng nhất — hỗ trợ action "Locate Extremes"

---

## Cách sửa Chart 7.1 — Price per Person by Borough

### Phương án A — Xóa Color Hue, giữ màu consistent với Chart 7.2 (khuyến nghị)

1. Kéo `Room Type` ra khỏi **Color shelf** của Chart 7.1
2. Gán màu bars đồng nhất: `#4E79A7`
3. Hoặc: giữ màu nhưng **đồng bộ bảng màu Room Type** giống hệt Chart 7.2 (để người xem có thể liên kết 2 chart dễ hơn)

### Phương án B — Giữ Color Hue nhưng lý giải trong văn bản

Nếu muốn giữ màu khác nhau cho Room Type trong Chart 7.1 để cross-chart linking:
- Đảm bảo bảng màu **hoàn toàn giống** Chart 7.2 (Entire home = xanh đậm, Hotel = cam, Private = đỏ, Shared = teal)
- Thêm note: "Color consistent with Chart 7.2 for cross-chart comparison"
- Đây là **Redundant Encoding có chủ đích** — chấp nhận được nếu giải thích rõ

---

## Nguyên tắc Mackinlay áp dụng

Theo **Effectiveness Principle** của Mackinlay:
- Với dữ liệu **Quantitative**: Position > Length > Angle > Color Luminance > Color Hue > Area
- Với dữ liệu **Nominal**: Position > Color Hue > Shape > Size

Khi Position đã encode Nominal attribute, thêm Color Hue chỉ có giá trị nếu:
1. Tăng khả năng phân biệt (discriminability) — không cần thiết ở đây vì các bars đã tách biệt
2. Cross-chart linking — hợp lý nhưng cần nhất quán
3. Accessibility (colorblind) — nên cân nhắc nếu thêm lại

---

## Checklist sau khi sửa

- [ ] Chart 5.2: Tất cả bars cùng 1 màu neutral hoặc highlight Manhattan
- [ ] Chart 7.1: Màu bars đồng nhất hoặc nhất quán với Chart 7.2
- [ ] Legend được xóa nếu không còn cần thiết
- [ ] Caption được cập nhật (bỏ dòng "Color shows details about...")

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 5 → Vấn đề #2 [Minor]; Domain Task 7 → Vấn đề #1 [Minor]
- Mackinlay's Effectiveness Principle: slides `chapter#3.pdf`
