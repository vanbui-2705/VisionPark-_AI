BỘ NGUYÊN TẮC BẮT BUỘC TRONG DỰ ÁN (PROJECT WORKING AGREEMENT)
PHẦN 1: QUY CHUẨN VỀ GIT & QUẢN LÝ SOURCE CODE

1. Nguyên tắc đồng bộ code (Sync First)
   Luôn git pull trước khi bắt đầu: Mỗi buổi sáng hoặc trước khi tạo nhánh mới/bắt đầu code tiếp, bắt buộc phải git pull --rebase (hoặc merge) nhánh chính (develop / main) về máy để cập nhật code mới nhất từ đồng đội.

Quy tắc giải quyết xung đột (Conflict): Tuyệt đối không tự ý ấn merge bừa khi có conflict. Nếu đụng code của người khác, phải ngồi lại cùng người đó để resolve conflict, không tự đoán logic để xóa code của đồng đội.

2. Chiến lược phân nhánh (Git Flow)
   Cấm push thẳng vào nhánh chính: Khóa (protect) nhánh main và develop. Không ai (kể cả PM/Tech Lead) được phép git push trực tiếp hay git push --force lên 2 nhánh này.

Quy chuẩn đặt tên nhánh:

Tính năng mới: feature/<mã-task>-<tên-ngắn-gọn> (ví dụ: feature/TASK-102-auth-login)

Sửa lỗi: bugfix/<mã-task>-<tên-lỗi>

Lỗi khẩn cấp production: hotfix/<mã-task>-<mô-tả>

3. Quy chuẩn Commit & Điều hướng lịch sử (Version Navigation)
   Atomic Commit: Mỗi commit chỉ giải quyết 1 đơn vị công việc rõ ràng. Không dồn code của 3 ngày vào 1 commit rồi ghi fix bug hay update.

Thông điệp rõ ràng: Áp dụng chuẩn Conventional Commits: feat: ..., fix: ..., refactor: ..., docs: ... kèm mã task.

Bảo toàn lịch sử: Luôn đảm bảo lịch sử Git sạch sẽ để khi cần rollback hoặc nhảy branch:

Tránh rác uncommitted: Trước khi chuyển nhánh (git checkout), phải commit hoặc dùng git stash lưu lại thay đổi, không để code bẩn dính sang nhánh khác.

Tránh Detached HEAD: Khi muốn xem lại phiên bản cũ bằng git checkout <commit-hash>, chỉ dùng để đọc/debug. Nếu muốn phát triển tiếp từ đó, bắt buộc tạo nhánh mới: git checkout -b <tên-nhánh-mới>. Sau đó luôn biết cách quay về đầu nhánh mới nhất bằng git checkout <tên-nhánh-chính> (nhảy về HEAD hiện tại).

Sử dụng Git Tag (v1.0.0, v1.1.0-beta) cho mỗi lần release để rollback tức thì khi có sự cố.

PHẦN 2: QUY CHUẨN VỀ DATABASE & DATA MIGRATION (RẤT QUAN TRỌNG)
Tuyệt đối cấm can thiệp trực tiếp bằng tay vào Database chung (Staging/Production) như mở DBeaver/pgAdmin lên gõ ALTER TABLE hay tự bấm thêm cột.

1. Quản lý thay đổi cấu trúc qua Code (Database Migrations)
   Mọi thao tác thêm/sửa/xóa bảng, thêm cột, đổi kiểu dữ liệu, đánh index... đều bắt buộc phải viết qua Migration script (ví dụ: Alembic, Prisma, Flyway, TypeORM, Knex...).

Bắt buộc có 2 chiều (Up & Down / Upgrade & Downgrade):

Script nâng cấp (upgrade / up): Thêm cột mới, tạo bảng mới.

Script rollback (downgrade / down): Phải có câu lệnh hủy bỏ (ví dụ: DROP COLUMN, DROP TABLE) để nếu deploy lỗi, hệ thống có thể quay ngược lại phiên bản DB cũ một cách an toàn mà không làm sập ứng dụng.

2. Nguyên tắc an toàn dữ liệu (Backward Compatibility)
   Khi thêm cột mới: Ưu tiên đặt giá trị mặc định (DEFAULT) hoặc cho phép NULL để tránh làm crash các phiên bản code cũ đang chạy song song.

Khi đổi tên cột hoặc xóa cột: Tuyệt đối không xóa ngay. Phải trải qua quy trình 2 bước: Bước 1 (thêm cột mới + sync data), Bước 2 (release code mới trỏ vào cột mới), Bước 3 (sau khi ổn định mới chạy migration xóa cột cũ).

PHẦN 3: CODE REVIEW VÀ TIÊU CHUẨN XUẤT XƯỞNG (PULL REQUEST - PR)
Quy tắc 4 mắt (Peer Review): Một Pull Request muốn được merge vào develop bắt buộc phải có ít nhất 1–2 Approved từ đồng đội hoặc Tech Lead.

Dung lượng PR vừa phải: Mỗi PR không nên vượt quá 400 dòng code thay đổi. PR càng to thì review càng ẩu và càng dễ lọt bug.

Tự test trước khi tạo PR (Self-Review): Người tạo PR phải tự chạy kiểm thử trên máy cá nhân, đảm bảo không có warning/lỗi cú pháp (linter), không làm hỏng các tính năng liên quan trước khi gửi cho người khác review.

CI/CD Check: Code push lên phải vượt qua kiểm tra tự động (build thành công, pass toàn bộ unit test/linter) thì nút Merge mới được mở.

PHẦN 4: QUẢN LÝ MÔI TRƯỜNG & BẢO MẬT (ENVIRONMENT & SECRETS)
Không bao giờ commit file bí mật: File .env, secret key, password DB, API keys, credentials tuyệt đối phải nằm trong .gitignore.

Cung cấp file mẫu: Khi thêm một biến môi trường mới (ví dụ REDIS_URL), người làm bắt buộc phải cập nhật ngay vào file .env.example kèm giải thích để các thành viên khác kéo code về biết cần cấu hình gì.

PHẦN 5: TÍNH MINH BẠCH VÀ BÁO CÁO CÔNG VIỆC (TASK & COMMUNICATION)
Cập nhật trạng thái Task theo thời gian thực:

Bắt đầu làm: Chuyển task sang In Progress.

Có PR: Chuyển sang In Review và đính kèm link PR vào ticket.

Đang test: Chuyển sang Testing / QA.

Quy tắc "Không chịu trận 1 mình": Nếu một thành viên gặp lỗi/vấn đề kỹ thuật (Blocker) mà tự nghiên cứu quá 2 giờ không ra hướng giải quyết, bắt buộc phải báo ngay trên kênh chat nhóm hoặc hỏi Lead, không được âm thầm ôm việc đến sát deadline mới thông báo.
