# alpr-runtime-boundary Specification

## Purpose
Cung cấp contract ALPR ổn định, có thể kiểm thử và chạy local để Backend và Frontend phát triển độc lập trước khi model nhận diện thật sẵn sàng.
## Requirements
### Requirement: Kết quả ALPR có cấu trúc ổn định
Mỗi lần xử lý frame hợp lệ MUST tạo một kết quả có cùng cấu trúc gồm kết quả thô, kết quả chuẩn hóa, bounding box, confidence detector, confidence recognition, confidence tổng hợp, thời gian xử lý, phiên bản model và cờ yêu cầu xác nhận.

#### Scenario: Nhận diện thành công
- **WHEN** runtime phát hiện và đọc được biển số
- **THEN** kết quả chứa biển số thô, biển số chuẩn hóa, bounding box, các confidence trong khoảng `0.0..1.0`, `processing_time_ms`, `model_version` và `requires_confirmation`

#### Scenario: Không có biển số
- **WHEN** frame hợp lệ nhưng runtime không phát hiện được biển số
- **THEN** runtime trả kết quả hợp lệ với plate và bbox bằng null, confidence bằng `0.0` và `requires_confirmation=true` mà không phát sinh exception

### Requirement: Runtime có interface độc lập implementation
Module ALPR MUST cung cấp một runtime interface nhận một frame ảnh và trả kết quả ALPR mà không để downstream phụ thuộc vào YOLO, PaddleOCR hoặc OpenCV implementation.

#### Scenario: Backend gọi runtime
- **WHEN** Backend Domain nhận một frame đã decode
- **THEN** Backend có thể gọi runtime qua interface duy nhất mà không import detector hoặc recognizer cụ thể

### Requirement: Readiness và lỗi chưa sẵn sàng có kiểu
Runtime MUST công bố trạng thái sẵn sàng và phiên bản model. Khi implementation chưa có model, lệnh xử lý MUST kết thúc bằng lỗi `ALPR_NOT_READY` có kiểu để API map thành HTTP `503`.

#### Scenario: Model chưa được cung cấp
- **WHEN** runtime chưa có model weight hoặc implementation thật
- **THEN** readiness là false, model version phản ánh trạng thái chưa sẵn sàng và xử lý frame tạo lỗi `ALPR_NOT_READY`

### Requirement: Mock runtime tất định
Module ALPR MUST cung cấp mock runtime có thể chọn trước kịch bản thành công, confidence thấp, không có biển số, chưa sẵn sàng và lỗi xử lý; cùng input và cấu hình MUST cho cùng output.

#### Scenario: Test chọn kịch bản thành công
- **WHEN** test cấu hình mock runtime ở chế độ thành công và gửi frame hợp lệ
- **THEN** runtime trả fixture thành công cố định và không dùng random

#### Scenario: Test chọn kịch bản lỗi
- **WHEN** test cấu hình mock runtime ở chế độ chưa sẵn sàng hoặc lỗi xử lý
- **THEN** runtime tạo đúng lỗi có kiểu tương ứng

### Requirement: Chuẩn hóa biển số
Normalizer MUST chuyển chữ cái thành chữ hoa, loại bỏ khoảng trắng, dấu chấm và dấu gạch; đầu vào null hoặc rỗng sau chuẩn hóa MUST trả null.

#### Scenario: Chuẩn hóa biển số thông thường
- **WHEN** đầu vào là ` 29a-123.45 `
- **THEN** kết quả là `29A12345`

#### Scenario: Không tự sửa ký tự OCR
- **WHEN** đầu vào chứa ký tự dễ nhầm như `O`, `0`, `I` hoặc `1`
- **THEN** normalizer giữ nguyên loại ký tự và chỉ áp dụng các phép chuẩn hóa đã quy định

### Requirement: Bounding box không vượt biên ảnh
Hàm clamp MUST giới hạn bounding box theo kích thước ảnh và MUST từ chối bounding box không còn diện tích sau khi clamp.

#### Scenario: Bounding box vượt biên
- **WHEN** một hoặc nhiều tọa độ nằm ngoài ảnh
- **THEN** tọa độ được giới hạn vào miền `[0, width]` và `[0, height]`

#### Scenario: Bounding box không hợp lệ
- **WHEN** bounding box sau clamp có `x1 >= x2` hoặc `y1 >= y2`
- **THEN** kết quả bbox là null và caller không thực hiện crop

### Requirement: Confidence policy có cấu hình
Confidence tổng hợp MUST được tính bằng giá trị nhỏ hơn giữa detector confidence và recognition confidence; kết quả không phải nhận diện thành công hoặc thấp hơn ngưỡng cấu hình MUST yêu cầu xác nhận.

#### Scenario: Confidence thấp hơn ngưỡng
- **WHEN** confidence tổng hợp thấp hơn `ALPR_CONFIDENCE_THRESHOLD`
- **THEN** kết quả có `requires_confirmation=true`

#### Scenario: Confidence không hợp lệ
- **WHEN** confidence không hữu hạn hoặc nằm ngoài `0.0..1.0`
- **THEN** module từ chối giá trị bằng lỗi validation có kiểu

### Requirement: Manifest phản ánh đúng tình trạng model
Model manifest MUST chứa tên, phiên bản, trạng thái, loại detector/recognizer, đường dẫn và checksum nếu có; manifest scaffold MUST ghi `not_ready` và không khai báo weight giả.

#### Scenario: Chưa có model train
- **WHEN** repository chỉ mới dựng AI boundary
- **THEN** manifest có trạng thái `not_ready`, weight path/checksum là null và không có model weight trong Git

### Requirement: ALPR không sở hữu nghiệp vụ bãi xe
Module ALPR MUST không import hoặc quyết định logic thuộc lane, parking, ticket, pricing, payment, barrier hay database.

#### Scenario: Trả kết quả nhận diện
- **WHEN** runtime hoàn thành xử lý frame
- **THEN** nó chỉ trả dữ liệu nhận diện và không xác định loại vé, hướng làn, quyền mở cổng hoặc trạng thái giao dịch

