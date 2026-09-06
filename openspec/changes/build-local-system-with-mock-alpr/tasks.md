## 1. Local Gate — cả 5 người

- [ ] 1.1 [Người 1] Chốt `.env.example`, port `5173/8000/5432`, named volumes và `ALPR_PROVIDER=mock`
- [ ] 1.2 [Người 2] Khởi tạo backend tối thiểu để Uvicorn và `/health/live` chạy trực tiếp trên local
- [ ] 1.3 [Người 5] Khởi tạo frontend tối thiểu để Vite mở `/login` và build thành công
- [ ] 1.4 [Người 3] Export Lane router tối thiểu để Người 2 đăng ký mà không sửa `main.py`
- [ ] 1.5 [Người 4] Export Station route tối thiểu để Người 5 đăng ký mà không sửa app router
- [ ] 1.6 [Cả đội] Chạy `docker compose up --build` trên ít nhất hai máy và chỉ merge baseline khi frontend, backend, PostgreSQL đều healthy

## 2. Người 1 — AI Core, ALPR API, Compose và QA

- [ ] 2.1 Chốt `ALPRResult`, bbox `[x1,y1,x2,y2]`, confidence và `requires_confirmation` với Người 3/4
- [ ] 2.2 Implement ALPR runtime protocol và typed errors theo change `scaffold-alpr-boundary`
- [ ] 2.3 Implement plate normalizer và unit test cho chữ hoa, khoảng trắng, dấu chấm, dấu gạch, null/rỗng
- [ ] 2.4 Implement bbox clamp và test tọa độ âm, vượt biên, đảo trục, không còn diện tích
- [ ] 2.5 Implement confidence policy cấu hình và test dưới/bằng/trên threshold
- [ ] 2.6 Implement deterministic mock provider cho success, low-confidence, no-plate, unavailable và processing-error
- [ ] 2.7 Cung cấp canonical JSON fixtures và model manifest `mock-alpr-0.1.0`; không thêm model weight
- [ ] 2.8 Định nghĩa schema HTTP cho multipart `image` + `lane_id`, ALPR response và error response
- [ ] 2.9 Implement giới hạn file, MIME validation và image decode; ảnh sai trả `422` mà không gọi runtime
- [ ] 2.10 Định nghĩa các port `ActiveLaneChecker`, `ImageStorage`, `DetectionRecorder` để Người 3 cung cấp adapter
- [ ] 2.11 Implement ALPR application service: kiểm tra lane, gọi runtime, lưu kết quả qua port và giữ AI Core độc lập ORM/repository
- [ ] 2.12 Implement `POST /api/v1/alpr/detections` và map `DETECTED/NO_PLATE -> 200`, not-ready/processing-error -> `503`
- [ ] 2.13 Viết contract/integration tests cho success, low confidence, no-plate, ảnh/lane lỗi, unavailable và processing-error
- [ ] 2.14 Hoàn thiện provider factory để sau train thay mock bằng YOLO + OCR mà không đổi API/Frontend
- [ ] 2.15 Bàn giao readiness contract cho Người 2 và Detection OpenAPI/fixtures cho Người 4
- [ ] 2.16 Hoàn thiện Compose cho `postgres`, `backend`, `frontend` cùng local storage volume
- [ ] 2.17 Viết smoke/E2E checklist cho login, RBAC, Lane, detection, confirmation, timeout và clean restart
- [ ] 2.18 Chạy regression cuối, tổng hợp evidence và xác nhận UI/health công bố rõ provider mock

## 3. Người 2 — Backend Core, PostgreSQL và Auth

- [x] 3.1 Khởi tạo `pyproject.toml`, FastAPI app, API v1 router registry và backend test configuration
- [x] 3.2 Tạo settings loader, CORS, environment validation và cấu hình upload/storage/JWT
- [x] 3.3 Tạo SQLAlchemy engine/session, declarative base và request-scoped database dependency
- [x] 3.4 Cấu hình Alembic và kiểm tra upgrade/downgrade trên database rỗng
- [x] 3.5 Tạo shared timestamp/UUID conventions và import registry cho migration
- [x] 3.6 Tạo Role/User ORM models cùng migration, unique constraint và active status
- [x] 3.7 Tạo seed idempotent cho `ADMIN`, `OPERATOR`, tài khoản demo và gọi seed trong local bootstrap
- [x] 3.8 Implement Argon2id password hashing, JWT creation/validation và không log credential/token
- [x] 3.9 Implement `POST /api/v1/auth/login` cho success, wrong password và inactive user
- [x] 3.10 Implement `GET /api/v1/auth/me` và current-user dependency
- [x] 3.11 Implement role checker dùng chung để Người 1 bảo vệ ALPR Detection API và Người 3 bảo vệ Lane/history/confirmation API
- [x] 3.12 Implement correlation-ID middleware và error response `{code,message,details,correlation_id}`
- [x] 3.13 Implement `/health/live` và `/health/ready`, nhận DB status và ALPR readiness từ interface Người 1
- [x] 3.14 Viết test migration, seed lặp, login đúng/sai/inactive, token lỗi, current user và RBAC helper
- [x] 3.15 Bàn giao DB/auth dependencies và router registration convention cho Người 1/3

## 4. Người 3 — Backend Lane, Persistence, Storage và Confirmation

- [ ] 4.1 Tạo module `lanes` theo model/schema/repository/service/router boundary
- [ ] 4.2 Tạo Lane ORM model và migration với name unique, direction `IN/OUT`, video source và active status
- [ ] 4.3 Bổ sung seed idempotent `LANE_IN_01` và `LANE_OUT_01` qua seed infrastructure Người 2
- [ ] 4.4 Implement Lane repository/service, kiểm tra tên trùng và không hard delete
- [ ] 4.5 Implement Lane list/detail/create/update API; list cho user xác thực, mutation chỉ Admin
- [ ] 4.6 Tạo local filesystem storage adapter có save/delete, object key, checksum, MIME và size
- [ ] 4.7 Tạo `media_objects`, `alpr_detections`, `audit_logs` models và migration theo design
- [ ] 4.8 Implement `ActiveLaneChecker` adapter cho port Người 1, trả lane tồn tại/active/direction
- [ ] 4.9 Implement `ImageStorage` adapter cho port Người 1 bằng local storage
- [ ] 4.10 Implement `DetectionRecorder` adapter với transaction lưu media metadata và detection; cleanup file nếu transaction lỗi
- [ ] 4.11 Viết adapter contract tests để Người 1 có thể dùng fake hoặc PostgreSQL implementation mà không đổi ALPR service
- [ ] 4.12 Implement recent detection list có filter `lane_id`, limit được chặn tối đa và authorization
- [ ] 4.13 Implement confirmation service cho accepted/corrected/no-plate manual input, normalize ở backend
- [ ] 4.14 Implement confirmation API, conflict khi Operator xác nhận lại và audit before/after
- [ ] 4.15 Viết test Lane CRUD/RBAC, storage failure, detection persistence và confirmation/audit
- [ ] 4.16 Bàn giao ba persistence adapters cho Người 1; bàn giao history/confirmation OpenAPI cho Người 4/5

## 5. Người 4 — Station Frontend

- [ ] 5.1 Tạo `StationLayout` và module entrypoint chỉ dùng router/auth/API client của Người 5
- [ ] 5.2 Tạo active Lane selector lấy dữ liệu từ Lane API và xử lý loading/empty/error
- [ ] 5.3 Tạo MP4 selector, validation và object URL lifecycle không rò rỉ tài nguyên
- [ ] 5.4 Tạo video player với play, pause, replay, progress và EOF behavior
- [ ] 5.5 Tạo canvas capture trả JPEG theo interval cấu hình, mặc định 200 ms
- [ ] 5.6 Tạo request controller bảo đảm tối đa một detection request pending và bỏ frame khi bận
- [ ] 5.7 Hủy timer/request hợp lý khi pause, EOF, đổi video, đổi Lane hoặc unmount route
- [ ] 5.8 Tạo Station state machine cho idle, video-ready, processing, detected, needs-confirmation, confirmed và error
- [ ] 5.9 Tạo bbox overlay quy đổi đúng từ kích thước ảnh gốc sang video hiển thị
- [ ] 5.10 Tạo result panel hiển thị raw/normalized plate, confidence, latency, model version và nhãn mock
- [ ] 5.11 Tạo nút “Biển số đúng”, form “Chưa đúng”, manual input cho no-plate và validation
- [ ] 5.12 Tạo recent detection list và đồng bộ sau confirmation thành công
- [ ] 5.13 Xử lý `401/403/422/409/503/timeout`: dừng loading, thông báo rõ, retry an toàn
- [ ] 5.14 Viết test video state, one-request rule, bbox scaling, confirmation, correction, no-plate và timeout
- [ ] 5.15 Bàn giao Station route/component entrypoint và test evidence cho Người 5/1

## 6. Người 5 — Frontend Foundation, Login và Admin Lane

- [ ] 6.1 Khởi tạo React/TypeScript/Vite, lint/test/build scripts và frontend Dockerfile
- [ ] 6.2 Tạo app router, `AuthLayout`, `StationLayout` slot, `AdminLayout` và not-found route
- [ ] 6.3 Tạo API client chung với base URL environment, Bearer token, timeout và common error mapping
- [ ] 6.4 Tạo AuthProvider cho login/logout/current user và khôi phục phiên sau refresh
- [ ] 6.5 Tạo role route guards cho Admin/Station nhưng giữ backend là nơi authorization cuối cùng
- [ ] 6.6 Tạo Login page với validation, loading, sai mật khẩu, inactive/unauthorized và redirect đúng role
- [ ] 6.7 Tạo shared button/input/select/table/dialog/feedback components cho Người 4 tái sử dụng
- [ ] 6.8 Tạo Admin navigation và hiển thị user/role hiện tại
- [ ] 6.9 Tạo Lane list với loading/empty/error, direction/status filter và refresh
- [ ] 6.10 Tạo Lane create/edit form, validate name/direction/video source và map duplicate-name error
- [ ] 6.11 Tạo active/inactive action có confirm dialog và cập nhật danh sách sau success
- [ ] 6.12 Hiển thị banner `DEMO — ALPR provider mock` trên Station và nơi phù hợp dựa trên health response
- [ ] 6.13 Gắn Station entrypoint của Người 4 vào router mà không sửa code nội bộ Station
- [ ] 6.14 Viết test API client, auth restore, route guard, Login, Lane CRUD UI và mock-provider banner
- [ ] 6.15 Bàn giao app shell, API client và shared components sớm để Người 4 không bị chặn

## 7. Mốc bàn giao và tích hợp

- [ ] 7.1 Cuối ngày 1: đạt Local Gate trên hai máy; Người 1 giao ALPR Detection API contract, Người 2 giao backend dependencies, Người 5 giao app shell/API client
- [ ] 7.2 Cuối ngày 2: auth và Lane API chạy thật; Login/Admin Lane gọi API thật; mock ALPR unit test đạt
- [ ] 7.3 Cuối ngày 3: Người 1 hoàn thiện detection upload/API, Người 3 hoàn thiện persistence adapters, Station video/capture chạy độc lập và confirmation contract được khóa
- [ ] 7.4 Cuối ngày 4: chạy end-to-end login → Lane → MP4 → frame → mock result → confirmation → database/audit
- [ ] 7.5 Ngày 5: chạy clean setup, regression, lint/test/build và sửa toàn bộ lỗi Critical/High
- [ ] 7.6 Xác nhận không có YOLO/PaddleOCR/model weight, không có ảnh blob trong DB và không có logic vé/IN-OUT transaction ngoài Lane direction
- [ ] 7.7 Cập nhật README với lệnh local, tài khoản demo, API/port, mock limitations và cách thay provider thật sau này
