## Purpose

Cho phép hệ thống nhận frame và hoàn tất luồng lưu kết quả nhận diện bằng mock ALPR tất định trong khi vẫn giữ nguyên contract dành cho model thật.

## ADDED Requirements

### Requirement: API nhận frame có xác thực
API detection MUST nhận ảnh JPEG/PNG và `lane_id`, yêu cầu token hợp lệ, xác minh Lane đang active và từ chối file hỏng hoặc không đúng loại.

#### Scenario: Frame hợp lệ
- **WHEN** Operator gửi ảnh hợp lệ cùng active Lane
- **THEN** API gọi ALPR runtime đúng một lần và tạo detection

#### Scenario: Frame hoặc Lane không hợp lệ
- **WHEN** ảnh không decode được, vượt giới hạn cấu hình, Lane không tồn tại hoặc inactive
- **THEN** API trả lỗi có kiểm soát và không gọi runtime

### Requirement: Mock ALPR tuân thủ contract thật
Local environment MUST dùng mock runtime qua cùng interface với runtime thật và MUST công bố rõ `model_version=mock-alpr-*`.

#### Scenario: Mock nhận diện thành công
- **WHEN** runtime mock xử lý frame hợp lệ
- **THEN** nó trả biển số thô/chuẩn hóa, bbox, confidence, processing time, model version và `requires_confirmation`

#### Scenario: Mock không có biển số
- **WHEN** runtime trả kết quả no-plate
- **THEN** API vẫn trả kết quả xử lý hợp lệ với plate/bbox null và cho phép luồng nhập tay tiếp tục

### Requirement: Lưu ảnh và metadata an toàn
Ảnh MUST được lưu qua storage adapter; PostgreSQL MUST chỉ lưu object key, checksum, MIME type, kích thước và liên kết detection, không lưu blob hoặc trả filesystem path công khai.

#### Scenario: Lưu detection thành công
- **WHEN** ảnh và kết quả runtime hợp lệ
- **THEN** storage object và detection được lưu nhất quán trước khi API trả thành công

#### Scenario: Storage thất bại
- **WHEN** storage không lưu được ảnh
- **THEN** detection không được xác nhận thành công và API trả lỗi có correlation ID

### Requirement: Response ALPR ổn định
Response thành công MUST chứa `detection_id`, raw/normalized plate, bbox, confidence, processing time, model version và `requires_confirmation` theo contract đã duyệt.

#### Scenario: Client nhận kết quả
- **WHEN** detection được xử lý và lưu thành công
- **THEN** API trả đầy đủ trường contract để Station không phụ thuộc implementation AI

