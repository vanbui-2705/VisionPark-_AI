## Purpose

Cho phép nhân viên xác nhận kết quả AI đúng hoặc nhập biển số thay thế, đồng thời lưu đầy đủ dấu vết phục vụ kiểm tra và huấn luyện sau này.

## ADDED Requirements

### Requirement: Xác nhận kết quả đúng
Operator hoặc Admin MUST có thể chấp nhận biển số AI của một detection chưa hoàn tất; hệ thống MUST lưu biển số chuẩn hóa làm giá trị cuối cùng cùng người và thời điểm xác nhận.

#### Scenario: Chấp nhận biển số AI
- **WHEN** user có quyền gửi `accepted=true` cho detection có biển số AI
- **THEN** detection chuyển `CONFIRMED` và lưu final plate, confirmer cùng confirmation time

### Requirement: Sửa hoặc nhập tay biển số
Operator hoặc Admin MUST có thể gửi biển số cuối cùng khi AI sai hoặc không đọc được; Backend MUST chuẩn hóa và lưu cả giá trị AI ban đầu lẫn giá trị cuối cùng.

#### Scenario: Sửa biển số AI
- **WHEN** user gửi `accepted=false` và một biển số thay thế hợp lệ
- **THEN** detection chuyển `CORRECTED`, giữ dữ liệu AI gốc và lưu biển số cuối cùng đã chuẩn hóa

#### Scenario: Không có biển số AI
- **WHEN** detection no-plate được nhập biển số thủ công hợp lệ
- **THEN** detection chuyển `CORRECTED` và lưu người xác nhận

### Requirement: Không xác nhận lặp ngoài kiểm soát
Detection đã `CONFIRMED` hoặc `CORRECTED` MUST không được Operator xác nhận lại.

#### Scenario: Operator xác nhận lần hai
- **WHEN** Operator gửi confirmation cho detection đã hoàn tất
- **THEN** API trả conflict và không ghi đè dữ liệu trước

### Requirement: Ghi audit cho confirmation
Mỗi confirmation hoặc correction MUST tạo audit log chứa actor, detection, giá trị trước/sau và timestamp.

#### Scenario: Biển số được sửa
- **WHEN** confirmation thay đổi biển số AI thành biển số cuối cùng khác
- **THEN** audit log lưu cả hai giá trị và người thực hiện

