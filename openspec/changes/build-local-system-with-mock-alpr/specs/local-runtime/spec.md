## Purpose

Cho phép toàn bộ lát cắt Phase 1 khởi động, dừng và kiểm tra ổn định trên máy local bằng một quy trình được tài liệu hóa.

## ADDED Requirements

### Requirement: Khởi động local bằng một lệnh
Hệ thống MUST khởi động frontend, backend và PostgreSQL bằng Docker Compose từ cấu hình mẫu không chứa secret thật.

#### Scenario: Clean setup thành công
- **WHEN** thành viên clone repository, tạo `.env` từ `.env.example` và chạy `docker compose up --build`
- **THEN** ba service khởi động, PostgreSQL healthy, backend phục vụ API và frontend mở được trong trình duyệt

### Requirement: Migration và seed có thể chạy lặp
Backend MUST tự nâng schema lên phiên bản hiện tại và seed role, user demo cùng hai làn mẫu theo cách idempotent.

#### Scenario: Khởi động lại môi trường
- **WHEN** Compose được dừng rồi khởi động lại với volume cũ
- **THEN** migration/seed hoàn thành mà không tạo dữ liệu trùng hoặc làm backend crash

### Requirement: Health phản ánh dependency
Backend MUST cung cấp live health và ready health, trong đó ready phản ánh riêng trạng thái database, ALPR provider và phiên bản model/provider.

#### Scenario: Mock ALPR và database sẵn sàng
- **WHEN** database kết nối được và provider cấu hình là mock đã khởi tạo
- **THEN** live và ready trả `200`, đồng thời ready công bố `alpr_provider=mock`

#### Scenario: Database hoặc ALPR không sẵn sàng
- **WHEN** một dependency bắt buộc không sẵn sàng
- **THEN** live vẫn phản ánh process còn sống còn ready trả trạng thái không sẵn sàng với dependency lỗi

