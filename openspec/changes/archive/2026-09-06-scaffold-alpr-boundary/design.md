## Context

Repository hiện mới có tài liệu kiến trúc và backlog; backend chưa được khởi tạo và model YOLO/PaddleOCR chưa được huấn luyện hoặc tích hợp. Theo `docs/architecture.md`, ALPR là bounded module tại `backend/app/alpr`, chạy cùng backend trong MVP nhưng không sở hữu nghiệp vụ bãi xe. Người 1 sở hữu AI Core, runtime contract và HTTP detection endpoint; Người 3 cung cấp Lane/storage/persistence adapters và sở hữu history/confirmation.

## Goals / Non-Goals

**Goals:**

- Cho phép Backend, Frontend và health check tích hợp qua contract ổn định khi chưa có model.
- Giữ code AI độc lập với FastAPI, database và domain modules.
- Cung cấp các phép biến đổi thuần có unit test trước khi detector/OCR thật xuất hiện.
- Làm cho việc thay mock bằng runtime thật không đổi public response schema.

**Non-Goals:**

- Train hoặc tích hợp YOLO/PaddleOCR.
- Đọc MP4 hoặc điều phối frame sampling; Station Frontend sở hữu việc lấy frame từ video.
- Decode multipart request; Backend Domain sở hữu HTTP boundary và chuyển frame đã decode vào runtime.
- Tra cứu vé, cache, xác định IN/OUT, tạo giao dịch hoặc quyết định mở barrier.
- Benchmark accuracy khi chưa có model và test set đại diện.

## Decisions

### 1. Contract nội bộ độc lập public API

`ALPRResult` là kiểu nội bộ bất biến gồm:

- `outcome`: `DETECTED` hoặc `NO_PLATE`.
- `raw_plate_number`, `normalized_plate_number`.
- `bbox` theo thứ tự `[x1, y1, x2, y2]` hoặc null.
- `detector_confidence`, `recognition_confidence`, `confidence`.
- `processing_time_ms`, `model_version`, `requires_confirmation`.

`detection_id` không thuộc `ALPRResult` vì ID do API/persistence layer sinh. Public API có thể ẩn hai confidence thành phần và chỉ trả `confidence` theo contract hiện tại.

Lựa chọn này giữ được dữ liệu cần benchmark trong AI nhưng không ép public API công bố chi tiết implementation. Phương án dùng trực tiếp Pydantic response của FastAPI bị loại vì làm ALPR phụ thuộc transport layer.

### 2. Runtime dùng Protocol và lỗi có kiểu

Runtime công bố ba thành phần:

```python
is_ready: bool
model_version: str
detect_and_read(frame) -> ALPRResult
```

`NO_PLATE` là kết quả xử lý hợp lệ. `ALPRNotReadyError`, `ALPRProcessingError` và `ALPRValidationError` dành cho dependency/runtime/input failure. Backend Domain chịu trách nhiệm map lỗi sang HTTP; ALPR không import FastAPI.

Phương án trả một object chứa lỗi cho mọi failure bị loại vì dễ khiến caller bỏ qua lỗi hệ thống và nhầm `NOT_READY` với `NO_PLATE`.

### 3. Mock runtime chọn mode tường minh

Mock runtime nhận mode khi khởi tạo: `SUCCESS`, `LOW_CONFIDENCE`, `NO_PLATE`, `NOT_READY`, `PROCESSING_ERROR`. Không dùng random, thời gian thực hoặc đọc fixture video để unit test có thể lặp lại.

Canonical examples được ghi trong tài liệu contract; backend và frontend duy trì fixture riêng nhưng phải có contract test để phát hiện drift.

### 4. Quy ước bounding box

Tọa độ dùng pixel nguyên với biên phải/dưới exclusive: `x1 <= x < x2`, `y1 <= y < y2`. Clamp giới hạn vào `[0, width]` và `[0, height]`; bbox không có diện tích trả null. Hàm không crop ảnh, nhờ đó có thể test không cần OpenCV.

### 5. Confidence baseline bảo thủ

Confidence tổng hợp tạm dùng:

```text
min(detector_confidence, recognition_confidence)
```

Ngưỡng xác nhận đọc từ `ALPR_CONFIDENCE_THRESHOLD`, mặc định `0.80` cho mock/local. Đây là policy có thể thay sau benchmark nhưng contract không đổi. Product không được công bố đây là accuracy của model.

### 6. Dependency tối thiểu

Contracts, normalizer, bbox và confidence policy dùng Python chuẩn. Runtime interface nhận frame theo type alias/documentation và không buộc cài OpenCV, Ultralytics hoặc PaddleOCR trong scaffold. Dependency nặng chỉ được thêm ở change tích hợp model thật.

### 7. Model manifest đặt ngoài application code

Manifest nằm tại `backend/models/alpr-manifest.yaml` theo kiến trúc repository. Bản scaffold ghi `status: not_ready`, `weight_path: null`, `checksum: null`; không tạo weight placeholder. Runtime config đọc đường dẫn manifest/model qua environment trong giai đoạn tích hợp sau.

### 8. Ranh giới bàn giao

- Người 1 sở hữu detection endpoint: decode ảnh, gọi runtime, map response và điều phối qua các persistence port.
- Người 3 nhận contract của `ActiveLaneChecker`, `ImageStorage`, `DetectionRecorder` để cài đặt adapter mà không sửa AI Core.
- Người 4 nhận JSON examples cho năm trạng thái Station; Frontend không suy luận confidence ngoài `requires_confirmation`.
- Người 2 nhận `is_ready` và `model_version`; readiness phải báo riêng DB và ALPR.

## Risks / Trade-offs

- [Contract được chốt trước dữ liệu model thật] → Giữ contract tối thiểu; chỉ thay policy nội bộ sau benchmark, không đổi tên/trường công khai tùy tiện.
- [Mock tạo cảm giác tính năng AI đã xong] → Hiển thị rõ `mock-alpr`/`not_ready`, health không báo ready và tài liệu cấm dùng số liệu mock làm accuracy.
- [Fixture Backend/Frontend bị lệch] → Thêm contract test so với canonical examples và yêu cầu Người 1 duyệt thay đổi contract.
- [Công thức confidence không phù hợp model thật] → Đóng gói thành policy riêng và benchmark trước khi đổi giá trị mặc định.
- [Runtime thật có thể không thread-safe] → Giai đoạn tích hợp model phải bổ sung concurrency decision; scaffold không cam kết thread safety giả.

## Migration Plan

1. Triển khai contract, utility thuần, mock runtime và manifest `not_ready`.
2. Người 1 tích hợp mock/runtime boundary vào detection endpoint; Người 3 nối Lane/storage/persistence adapters; Người 2 nối readiness; Người 4 dùng examples dựng UI.
3. Khi có `best.pt` và OCR plan, tạo change riêng cho runtime thật.
4. Runtime thật implement cùng interface, chạy benchmark rồi mới đổi cấu hình local từ mock sang real.
5. Rollback bằng cách chuyển provider về mock/not-ready; public API và UI contract không thay đổi.

## Open Questions

- Định dạng/export cụ thể của model YOLO, thiết bị CPU/GPU và phiên bản OCR sẽ được chốt trong change tích hợp model thật.
- Ngưỡng confidence production chỉ được chốt sau khi có validation set đại diện.
