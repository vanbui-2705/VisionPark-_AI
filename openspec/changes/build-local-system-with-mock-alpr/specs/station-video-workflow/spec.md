## Purpose

Cung cấp Station UI để Operator phát video MP4, gửi frame có kiểm soát, xem kết quả ALPR và hoàn tất xác nhận thủ công.

## ADDED Requirements

### Requirement: Station phát video local
Station MUST cho phép chọn MP4 hợp lệ, play, pause, replay và dừng xử lý khi video pause hoặc kết thúc.

#### Scenario: Phát video hợp lệ
- **WHEN** Operator chọn MP4 mà trình duyệt hỗ trợ và nhấn play
- **THEN** video phát theo thời gian thực và Station bắt đầu lịch lấy frame

#### Scenario: Video không hợp lệ
- **WHEN** file không phải video hỗ trợ hoặc không thể phát
- **THEN** Station hiển thị lỗi rõ ràng và không gửi detection request

### Requirement: Lấy frame có throttle
Station MUST lấy frame theo tần suất cấu hình, mặc định tối đa 5 frame/giây, và MUST chỉ có tối đa một detection request đang xử lý.

#### Scenario: Request trước chưa hoàn tất
- **WHEN** đến nhịp lấy frame mới nhưng request cũ còn pending
- **THEN** Station bỏ qua nhịp mới thay vì tạo request đồng thời

### Requirement: Hiển thị kết quả và bounding box
Station MUST hiển thị plate, confidence, processing time, model version, cờ confirmation và bbox đúng tỷ lệ khi video thay đổi kích thước.

#### Scenario: Nhận response detection
- **WHEN** API trả kết quả thành công
- **THEN** result panel và bbox overlay được cập nhật bằng dữ liệu response

### Requirement: Hoàn tất xác nhận trên Station
Station MUST cung cấp nút xác nhận đúng và luồng nhập lại biển số; loading MUST dừng khi thành công, timeout hoặc lỗi.

#### Scenario: Confidence thấp hoặc no-plate
- **WHEN** response yêu cầu xác nhận hoặc không có plate
- **THEN** Station làm nổi bật yêu cầu nhập/xác nhận và không tự coi kết quả là hoàn tất

#### Scenario: API timeout hoặc unavailable
- **WHEN** detection request timeout hoặc API trả `503`
- **THEN** Station dừng loading, hiển thị lỗi và cho phép retry hoặc nhập tay theo luồng được hỗ trợ

