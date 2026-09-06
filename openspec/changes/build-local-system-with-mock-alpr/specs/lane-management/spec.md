## Purpose

Cung cấp dữ liệu làn `IN/OUT` thật để Admin quản lý và Station lựa chọn làn đang hoạt động trước khi gửi frame.

## ADDED Requirements

### Requirement: Admin quản lý Lane
Admin MUST có thể tạo, xem và sửa Lane với tên duy nhất, hướng `IN/OUT`, nguồn video và trạng thái hoạt động.

#### Scenario: Tạo Lane hợp lệ
- **WHEN** Admin tạo Lane với tên chưa tồn tại và direction hợp lệ
- **THEN** Lane được lưu và trả về với ID cùng timestamp

#### Scenario: Tên Lane trùng
- **WHEN** Admin tạo hoặc đổi tên Lane thành tên đã tồn tại
- **THEN** API từ chối bằng lỗi nghiệp vụ và không tạo bản ghi trùng

### Requirement: Lane được inactive thay vì xóa
Lane đã tạo MUST được vô hiệu hóa bằng cập nhật trạng thái và MUST không bị hard delete qua API Phase 1.

#### Scenario: Inactive Lane
- **WHEN** Admin đặt `is_active=false`
- **THEN** Lane vẫn tồn tại trong lịch sử nhưng không xuất hiện trong danh sách chọn làn hoạt động của Station

### Requirement: Seed hai Lane demo
Local environment MUST có `LANE_IN_01` direction `IN` và `LANE_OUT_01` direction `OUT` sau khi seed.

#### Scenario: Seed trên database rỗng
- **WHEN** seed chạy lần đầu
- **THEN** hai Lane demo được tạo đúng direction và ở trạng thái active

