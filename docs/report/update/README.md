# Update Steps — Idiom Design Task 5, 6, 7, 8

Thư mục này chứa các bước sửa chi tiết được sinh ra từ review trong `../validate_report.md`.
Mỗi file = 1 bước sửa độc lập, đặt tên theo thứ tự ưu tiên và focus chính.

---

## Thứ tự sửa theo mức độ ưu tiên

| File | Mức độ | Chart | Focus |
|------|--------|-------|-------|
| `step03_medium_fix_chart72_hotel_trendline_annotation.md` | **Medium** | Chart 7.2 | Xử lý trend line bất thường của Hotel room |
| `step04_minor_remove_redundant_color_hue_chart52_71.md` | **Minor** | Chart 5.2, 7.1 | Xóa Color Hue dư thừa encode cùng attribute với PosX |
| `step05_minor_fix_chart62_overplotting.md` | **Minor** | Chart 6.2 | Giảm overplotting bằng opacity / z-order / filter |
| `step06_minor_fix_chart82_heatmap_group_definition_and_missing_month.md` | **Minor** | Chart 8.2 | Thêm định nghĩa nhóm minimum_nights; xử lý tháng 12 thiếu data |
| `step07_minor_fix_chart81_month_axis_labels.md` | **Minor** | Chart 8.1 | Đổi trục X từ số → tên tháng (Jan, Feb...) |
| `step08_minor_improve_chart51_boxplot_reference_line.md` | **Minor** | Chart 5.1 | Thêm reference line median NYC; làm rõ vai trò Color Hue |

---

## Đã xử lý / Đã đóng

| Step | Chart | Kết quả |
|------|-------|---------|
| ~~step01~~ | Chart 6.1 | Không có lỗi filter trong file Tableau thực tế. Color Hue True/False đã đúng. Cần giảm opacity non-outlier (Minor). |
| ~~step02~~ | Chart 8.1 | Đã validate bằng Python: November spike là data artifact (2025 data chỉ có Nov–Dec, mixing với 2026 forward data). Quyết định: **giữ Year = 2026, thêm caption giải thích** (xem mục "Cập nhật Chart 8.1" bên dưới). |

---

## Cập nhật Chart 8.1 — Quyết định cuối (thêm vào Bao_Duy_updated.docx)

**Kết quả validate từ `validate_occupancy.py`:**

Dataset chỉ có 2 năm:
- **2025:** chỉ có tháng 11 (620,952 records, occ = 52.04%) và tháng 12 (663,865 records, occ = 35.86%)
- **2026:** tháng 1–11 (20–40%), không có tháng 12

November spike trong Phương án B (All Years) là **data artifact**: 96.7% records tháng 11 đến từ 2025 (historical booked) — bản chất khác hoàn toàn với 2026 (forward-looking availability). So sánh hai loại dữ liệu này là không hợp lệ.

**Quyết định: Giữ Year = 2026 + thêm caption sau vào Chart 8.1:**

> *"Data reflects 2026 forward calendar availability (Jan–Nov 2026). Occupancy Rate Pct = mean(is_booked) per month. Values represent proportion of listing-days marked as booked relative to available inventory. December 2026 data not yet available at time of dataset snapshot."*

**Cập nhật mô tả idiom Chart 8.1 trong docx:**

> "Chart 8.1 sử dụng line chart để hiển thị xu hướng Occupancy Rate (%) theo từng tháng trong năm 2026. Trục X là Month (Ordinal), trục Y là mean(is_booked) — tỷ lệ ngày được đặt trên tổng ngày có lịch. Reference line ngang tại mức trung bình (~30%) giúp xác định các tháng vượt ngưỡng (action: Locate Extremes). Dữ liệu được giới hạn trong năm 2026 để đảm bảo tính nhất quán: dữ liệu 2025 chỉ bao gồm tháng 11–12 (historical booked) và sẽ tạo bias so sánh nếu mix với dữ liệu 2026 (forward-looking availability)."

---

## Tóm tắt nhanh — Còn cần làm

### Nên làm để tăng chất lượng
- **Step 03** — Chart 7.2: Hotel room trend line misleading
- **Step 04** — Chart 5.2 & 7.1: xóa Color Hue dư thừa
- **Step 05** — Chart 6.2: giảm overplotting

### Nâng cao readability
- **Step 06** — Chart 8.2: định nghĩa nhóm minimum_nights + tháng 12
- **Step 07** — Chart 8.1: tên tháng thay số trên trục X
- **Step 08** — Chart 5.1: reference line NYC median

---

## Nguồn tham chiếu

- Review gốc: `../validate_report.md`
- Validation script: `../../validate_occupancy.py`
- Midterm report: `../midterm/midterm_report.pdf`
- Chart images: `../tableau/`
