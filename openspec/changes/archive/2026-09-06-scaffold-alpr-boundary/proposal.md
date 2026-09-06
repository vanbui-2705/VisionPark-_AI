## Why

VisionPark cần một ranh giới ALPR ổn định để Backend và Station Frontend có thể phát triển, kiểm thử và chạy local trước khi model YOLO/PaddleOCR thật được huấn luyện hoặc tích hợp. Nếu API phụ thuộc trực tiếp vào implementation AI chưa tồn tại, các workstream khác sẽ bị chặn và contract dễ thay đổi khi model được đưa vào sau này.

## What Changes

- Thêm contract kết quả ALPR thống nhất cho các trường hợp nhận diện thành công, không có biển số, chưa sẵn sàng và lỗi xử lý.
- Thêm runtime interface `detect_and_read(frame)` độc lập với YOLO, PaddleOCR, API và nghiệp vụ bãi xe.
- Thêm mock runtime tất định để Backend, Frontend và test sử dụng khi chưa có model thật.
- Thêm chuẩn hóa biển số, clamp bounding box và confidence policy có cấu hình.
- Thêm model manifest trạng thái `not_ready` và readiness interface phục vụ health check.
- Thêm fixture và unit test cho toàn bộ hành vi thuộc AI boundary.
- Không train, tải hoặc tích hợp model weight trong change này.

## Capabilities

### New Capabilities

- `alpr-runtime-boundary`: Contract, readiness, mock runtime và các phép biến đổi thuần cần thiết để tích hợp ALPR mà không phụ thuộc model thật.

### Modified Capabilities

- Không có.

## Impact

- Mã mới nằm dưới `backend/app/alpr` và test nằm dưới `backend/tests/unit/alpr`.
- Backend Domain sẽ phụ thuộc vào runtime interface, result contract và lỗi có kiểu; không import detector/OCR implementation.
- Station Frontend dùng fixture JSON tương ứng với contract để dựng các trạng thái giao diện.
- Backend Core dùng readiness và model version để phản ánh trạng thái ALPR trong `/health/ready`.
- Không thay đổi database, nghiệp vụ làn/vé/giao dịch hoặc public API ngoài việc cung cấp contract cho endpoint ALPR tương lai.
