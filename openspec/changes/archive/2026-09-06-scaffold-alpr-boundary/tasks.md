## 1. Contract và cấu trúc module

- [x] 1.1 Xác nhận backend foundation của Người 2 đã có `backend/app` và cấu hình test; không tự sửa `main.py`, database hoặc API router
- [x] 1.2 Tạo các package `backend/app/alpr/{detector,recognition,normalization,runtime}` và `backend/tests/unit/alpr`
- [x] 1.3 Định nghĩa immutable `BoundingBox`, `ALPROutcome` và `ALPRResult` theo design, kèm validation invariant
- [x] 1.4 Định nghĩa `ALPRRuntime` protocol với `is_ready`, `model_version` và `detect_and_read(frame)`
- [x] 1.5 Định nghĩa `ALPRError`, `ALPRNotReadyError`, `ALPRProcessingError` và `ALPRValidationError` không phụ thuộc FastAPI

## 2. Phép biến đổi thuần

- [x] 2.1 Implement normalizer viết hoa và loại bỏ khoảng trắng, dấu chấm, dấu gạch; null/rỗng trả null
- [x] 2.2 Viết test bảng dữ liệu cho normalizer, bao gồm ký tự `O/0/I/1` không bị tự sửa
- [x] 2.3 Implement bbox clamp theo tọa độ pixel, biên phải/dưới exclusive và trả null khi không còn diện tích
- [x] 2.4 Viết test bbox trong ảnh, âm, vượt biên, ngoài hoàn toàn, đảo trục và kích thước ảnh không hợp lệ
- [x] 2.5 Implement confidence validation, công thức `min(detector, recognition)` và policy `requires_confirmation`
- [x] 2.6 Viết test confidence tại dưới/bằng/trên threshold và các giá trị âm, lớn hơn một, NaN, infinity

## 3. Runtime ONNX thực tế

- [x] 3.1 Implement ONNX Runtime (`OnnxALPRRuntime`) với `onnxruntime.InferenceSession`
- [x] 3.2 Tích hợp OpenCV (`cv2.imdecode`, `cv2.resize`) để tiền xử lý ảnh và crop biển số
- [x] 3.3 Chạy inference qua 2 mô hình `plate_detector.onnx` và `ocr_model.onnx`
- [x] 3.4 Bắt lỗi `ALPRNotReadyError` nếu file trọng số chưa được thả vào thư mục `weights/`
- [x] 3.5 Bắt lỗi `ALPRProcessingError` nếu quá trình OCR/Detection gặp lỗi từ ONNX

## 4. Manifest và contract fixtures

- [x] 4.1 Thêm `.gitignore` chặn file `*.onnx` để không bị push trọng số lớn lên repo
- [x] 4.2 Viết canonical response examples cho success, low-confidence, no-plate, not-ready và processing-error
- [x] 4.3 Kiểm tra fixture không chứa ảnh base64, filesystem path, dữ liệu thật hoặc accuracy claim

## 5. Bàn giao tích hợp

- [x] 5.1 Implement tại endpoint `/api/v1/alpr/detections`, map `ALPRNotReadyError` -> `503`, validation input -> `422`
- [x] 5.2 Bàn giao các port (`ActiveLaneChecker`, `DetectionRecorder`, `ImageStorage`) cho module nghiệp vụ khác tự nối vào
- [x] 5.3 Review code tích hợp để xác nhận ALPR endpoint gọi đúng `ALPRApplicationService`
- [x] 5.4 AI Core hoàn toàn không dính dáng đến ORM/Repository của các module khác

## 6. Xác minh và hoàn tất

- [x] 6.1 Chạy thử luồng xử lý Backend đã tích hợp sẵn ONNX và OpenCV
- [x] 6.2 Cập nhật file kiến trúc `architecture.md` để phản ánh đúng cấu trúc ONNX runtime
- [x] 6.3 Chạy Ruff check/format cho phạm vi ALPR
- [x] 6.4 Ghi nhận hoàn tất luồng AI và lưu log vào OpenSpec
