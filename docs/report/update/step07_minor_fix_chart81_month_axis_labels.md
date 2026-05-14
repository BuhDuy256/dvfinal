# Step 07 — [Minor] Đổi trục X từ số sang tên tháng ở Chart 8.1

## Vấn đề

Chart 8.1 "Monthly Occupancy Rate" hiển thị trục X là số nguyên: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11`

Người xem phải tự map: 1 = January, 2 = February... → giảm readability, tốn thêm cognitive load.

**Task 8 yêu cầu (midterm_report):**
> Action: "Browse" → Target: "Trends" — Duyệt dữ liệu lấp đầy dọc theo trục thời gian.
> Action: "Locate" → Target: "Extremes" — Xác định chính xác các tháng cao điểm và thấp điểm.

Khi trục X không hiển thị tên tháng, action "Locate Extremes" bị suy yếu — người dùng không thể nhanh chóng xác định "mùa cao điểm là từ tháng mấy đến tháng mấy."

## Cách sửa trong Tableau

### Phương án A — Dùng Date field thay vì số tháng

Nếu field `month` hiện là integer:
1. Tạo Calculated Field:
   ```
   DATENAME('month', MAKEDATE(2024, [month], 1))
   ```
   → Trả về: "January", "February", ...
2. Đưa field mới này vào **Columns** thay cho `month` số nguyên
3. Sort theo thứ tự tháng (không sort alphabetically)

### Phương án B — Format axis labels (nếu field đã là Date)

Nếu `month` đã là kiểu Date/Month trong Tableau:
1. Right-click trục X → **Format**
2. Trong **Dates** → chọn format `MMM` (Jan, Feb, Mar...) hoặc `MMMM` (January, February...)

### Phương án C — Alias thủ công (nhanh nhất)

1. Right-click vào field `month` trong data pane → **Aliases**
2. Đổi: `1` → `Jan`, `2` → `Feb`, ..., `11` → `Nov`, `12` → `Dec`
3. Tableau sẽ hiển thị alias thay cho số nguyên

## Kết quả mong đợi

Trục X hiển thị: `Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov`

Người xem ngay lập tức nhận biết: "Occupancy tăng mạnh từ tháng 5 (May), đạt peak tháng 11 (Nov)."

## Bonus — Thêm annotation mùa vụ (tuỳ chọn)

Nếu muốn làm nổi bật seasonal pattern:
1. Thêm **Reference Band** từ tháng 6–9 (hoặc tháng 8–11 tùy theo data)
2. Gán màu nền nhạt (ví dụ: vàng nhạt) với label "Peak Season"
3. Hoặc dùng **Text Annotation** tại điểm cao nhất

## Cập nhật mô tả idiom trong báo cáo

> "Chart 8.1 sử dụng line chart với trục X là tháng trong năm (hiển thị tên tháng viết tắt) và trục Y là Occupancy Rate (%). Reference line ngang thể hiện mức trung bình toàn năm, giúp người dùng nhanh chóng xác định các tháng vượt trung bình."

## Checklist sau khi sửa

- [ ] Trục X hiển thị tên tháng (Jan–Nov hoặc Jan–Dec)
- [ ] Thứ tự tháng đúng từ trái sang phải (không bị sort alphabetically)
- [ ] Caption vẫn khớp với filter Month

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 8 → Vấn đề #2 [Minor]
- Task Abstraction: `midterm_report.pdf` → Section 2.8 → Search: Action "Browse/Locate" → Target "Trends/Extremes"
- Attribute: `midterm_report.pdf` → Data Abstraction → calendar_clean → `month` (O, Cyclic, Time aggregation seasonality)
