# Step 05 — [Minor] Giảm overplotting ở Chart 6.2 — Price vs Rating

## Vấn đề

Chart 6.2 "Price vs Rating" có **overplotting nặng** ở vùng:
- Rating: 4.5 – 5.0 (trục Y)
- Price: $0 – $150 (trục X)

Hầu hết các điểm "Good Deal" (màu xanh) bị che khuất bởi lớp điểm "Normal" (màu xám) phía trên. Người dùng không thể "Locate" các món hời cụ thể như task yêu cầu.

**Task 6 yêu cầu (midterm_report):**
> Action: "Locate" → Target: "Outliers" — Xác định chính xác vị trí các listing có giá trị thực vượt trội.

## Nguyên nhân

- ~21,000 listings sau filter → quá nhiều điểm cho một scatter plot
- Cả 2 groups (Good Deal / Normal) dùng màu solid, opacity = 100%
- Good Deal points bị render bên dưới Normal points (z-order)

## Cách sửa (chọn 1 hoặc kết hợp)

### Phương án A — Giảm opacity (khuyến nghị nhanh nhất)

1. Click vào marks → **Color** → **Opacity**
2. Giảm opacity xuống **30–40%** cho tất cả điểm
3. Vùng đông điểm sẽ tối hơn (density visible), điểm đơn lẻ trong tâm điểm sẽ sáng hơn tương đối
4. Good Deal points (màu xanh) sẽ nổi hơn trong vùng thưa

### Phương án B — Đưa Good Deal lên z-order trên cùng

1. Tạo **dual axis**: 1 axis cho Normal (opacity thấp, màu xám nhạt), 1 axis cho Good Deal (opacity cao, màu xanh đậm)
2. Synchronize axes
3. Kết quả: Good Deal points luôn ở trên cùng, không bị che

### Phương án C — Thêm filter Borough hoặc Room Type

1. Thêm **Quick Filter** cho `Neighbourhood Group Cleansed` hoặc `Room Type`
2. Người dùng drill-down từng khu vực → số điểm giảm → overplotting giảm
3. Hỗ trợ chuỗi nhiệm vụ: overview → filter → inspect

### Phương án D — Jitter (nếu Tableau hỗ trợ)

1. Tạo calculated field:
   ```
   FLOAT([Price]) + (RANDOM() - 0.5) * 5
   ```
2. Dùng làm PosX thay cho Price gốc
3. Lưu ý: jitter làm mất một chút độ chính xác PosX — chỉ dùng khi Price không cần đọc chính xác từng điểm

## Cập nhật caption

Thêm vào caption:
> "Points shown with reduced opacity to reveal density. Green = Good Deal (price < median AND rating ≥ 4.8). Filter by Borough or Room Type to explore specific segments."

## Cập nhật mô tả idiom trong báo cáo

> "Chart 6.2 sử dụng scatter plot để so sánh tương quan giữa giá và rating. Opacity được giảm xuống để xử lý overplotting trong vùng dữ liệu dày đặc. Color Hue phân biệt nhóm 'Good Deal' (xanh) và 'Normal' (xám), với 2 reference lines xác định ngưỡng phân loại: đường dọc = median price, đường ngang = rating threshold 4.8."

## Checklist sau khi sửa

- [ ] Opacity đã giảm (~30–40%)
- [ ] Good Deal points vẫn đủ nổi bật so với Normal points
- [ ] Reference lines (Median, 4.8) vẫn rõ ràng
- [ ] Caption đã cập nhật

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 6 → Vấn đề #2 [Minor]
- Task Abstraction: `midterm_report.pdf` → Section 2.6 → Search: Action "Locate" → Target "Outliers"
