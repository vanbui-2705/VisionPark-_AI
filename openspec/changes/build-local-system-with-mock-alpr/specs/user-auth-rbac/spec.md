## Purpose

Cung cấp đăng nhập và phân quyền tối thiểu để Admin quản lý làn còn Operator chỉ sử dụng Station và xác nhận biển số.

## ADDED Requirements

### Requirement: Đăng nhập bằng tài khoản hoạt động
Backend MUST xác minh username/password đã băm và cấp JWT access token cho tài khoản hoạt động; thông tin sai hoặc tài khoản inactive MUST không tạo token.

#### Scenario: Đăng nhập đúng
- **WHEN** người dùng gửi đúng thông tin tài khoản đang hoạt động
- **THEN** API trả access token và thông tin role

#### Scenario: Đăng nhập sai
- **WHEN** username/password sai hoặc tài khoản inactive
- **THEN** API trả `401` và không tạo phiên hợp lệ

### Requirement: Backend thực thi RBAC
Backend MUST kiểm tra role trên mọi API ngoài health và login; Frontend route guard không được thay thế kiểm tra phía server.

#### Scenario: Operator gọi Lane mutation
- **WHEN** user role `OPERATOR` gọi API tạo, sửa hoặc inactive Lane
- **THEN** Backend trả `403`

#### Scenario: Admin quản lý Lane
- **WHEN** user role `ADMIN` gọi Lane mutation với token hợp lệ
- **THEN** request được chuyển đến Lane service

### Requirement: Current user có thể truy xuất
Người dùng đã xác thực MUST lấy được ID, username, display name, role và trạng thái của chính mình mà không nhận password hash.

#### Scenario: Lấy current user
- **WHEN** client gửi access token hợp lệ đến current-user endpoint
- **THEN** API trả thông tin public của user và không trả dữ liệu bí mật

