# Step 03 — [Medium] Xử lý trend line bất thường của Hotel Room ở Chart 7.2

## Vấn đề

Chart 7.2 "Accommodates vs Price per Person" dùng **linear trend line** cho từng Room Type. Trend line của **Hotel room** dốc bất thường từ ~$150 (accommodates = 1) xuống ~$0 (accommodates = 10), sau đó extrapolate ra ngoài phạm vi dữ liệu thực.

**Nguyên nhân:** Hotel room rất hiếm khi có `accommodates > 4` trong dữ liệu Airbnb NYC. Chỉ có vài điểm data ở accommodates cao → linear regression bị kéo lệch, tạo ra slope quá dốc và extrapolation phi thực tế.

**Vấn đề perceptual:** Người xem nhìn vào có thể hiểu sai "Hotel room trở thành rẻ nhất khi nhóm khách đông" — điều này không phản ánh thực tế.

**Task 7 yêu cầu (midterm_report):**
> Action: "Discover" → Target: "Dependency" — Phát hiện mối quan hệ phụ thuộc giữa sức chứa và biến động chi phí bình quân.

## Cách sửa (chọn 1 trong 3 phương án)

### Phương án A — Loại Hotel room khỏi trend line (khuyến nghị đơn giản nhất)

Trong Tableau:
1. Click vào trend line của Hotel room
2. Right-click → **Edit Trend Line**
3. Bỏ chọn Hotel room khỏi danh sách áp dụng trend line
4. Giữ trend line cho Entire home/apt, Private room, Shared room
5. Thêm note trong caption: "Hotel room excluded from trend line due to limited sample size at higher occupancy levels."

### Phương án B — Thêm annotation số lượng data points

1. Thêm **Label** hiển thị số lượng listing cho mỗi điểm (COUNT)
2. Hoặc thêm **Tooltip** hiển thị: `Accommodates: X | Room Type: Y | Median Price/Person: $Z | n listings: N`
3. Người dùng thấy Hotel room ở accommodates cao chỉ có 1–2 listings → tự hiểu trend line không đáng tin

### Phương án C — Dùng polynomial hoặc bỏ trend line, thêm confidence band

1. Trong **Edit Trend Line**: đổi model sang **Polynomial (degree 2)** — phù hợp hơn cho quan hệ giảm dần theo quy mô
2. Bật **Show 95% Confidence Bands**: vùng band rộng ở Hotel room sẽ tự nhiên signal "ít dữ liệu, không đáng tin"
3. Hoặc đơn giản: bỏ trend line cho Hotel room, chỉ giữ scatter points

## Cập nhật caption

Thêm vào caption Chart 7.2:
> "Trend lines show linear regression per room type. Hotel room trend line omitted / shown with caution due to limited data points at higher accommodates values."

## Cập nhật mô tả idiom trong báo cáo

Trong phần mô tả Chart 7.2:
> "Chart 7.2 sử dụng scatter plot với trend line để thể hiện mối quan hệ giữa sức chứa (`accommodates`) và chi phí bình quân đầu người. Trend line áp dụng cho các room type có đủ dữ liệu; Hotel room được loại khỏi regression do sample size hạn chế ở nhóm `accommodates` cao."

## Mức độ ảnh hưởng

| Trước sửa | Sau sửa |
|-----------|---------|
| Hotel room trend line extrapolate xuống $0 | Trend line dừng tại phạm vi data thực, hoặc bị loại |
| Người đọc có thể hiểu sai cost efficiency của Hotel room | Insight rõ ràng, không mislead |
| Chỉ có 3 room types còn lại vẫn cho thấy pattern giảm dần | Không mất insight chính của Task 7 |

## Liên kết

- Tham chiếu: `validate_report.md` → Domain Task 7 → Vấn đề #2 [Medium]
- Task Abstraction: `midterm_report.pdf` → Section 2.7 → Analyze: Action "Discover" → Target "Dependency"
