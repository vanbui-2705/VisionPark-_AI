from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ....alpr.schema import ALPRResult
from ....alpr.service import ALPRApplicationService
from ....alpr.errors import ALPRNotReadyError, ALPRProcessingError

router = APIRouter()

# Lưu ý: Trong hệ thống thực tế, bạn sẽ đưa instance của ALPRApplicationService
# vào hàm thông qua Dependency Injection của FastAPI (VD: Depends(get_alpr_service)).
# Hiện tại chúng ta giả lập (mock) chữ ký (signature) của dependency này.
def get_alpr_service() -> ALPRApplicationService:
    raise NotImplementedError("Dependency injection chưa được cấu hình.")

@router.post("/detections", response_model=ALPRResult)
async def create_detection(
    lane_id: str = Form(...),
    image: UploadFile = File(...),
    alpr_service: ALPRApplicationService = Depends(get_alpr_service)
):
    """
    Endpoint tiếp nhận ảnh từ camera để trả về kết quả nhận diện ALPR.
    Bên dưới gọi ALPR runtime bằng ONNX.
    """
    if not image.content_type in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Định dạng ảnh không hợp lệ. Hệ thống chỉ hỗ trợ JPEG và PNG."
        )

    # Đọc bytes từ file upload
    image_bytes = await image.read()
    
    # Kiểm tra kích thước file (ví dụ giới hạn 5MB)
    MAX_SIZE = 5 * 1024 * 1024
    if len(image_bytes) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Kích thước ảnh vượt quá giới hạn 5MB cho phép."
        )

    try:
        # Gọi Application Service
        result = alpr_service.process_detection(image_bytes, lane_id)
        return result
        
    except ValueError as ve:
        # Lỗi validate làn xe hoặc dữ liệu đầu vào
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except ALPRNotReadyError as e:
        # Model chưa sẵn sàng (chưa thả file onnx vào thư mục weights)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "ALPR_NOT_READY", "message": str(e)}
        )
    except ALPRProcessingError as e:
        # Lỗi trong quá trình chạy Inference (VD OpenCV hoặc ONNX lỗi)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "ALPR_PROCESSING_ERROR", "message": str(e)}
        )
    except Exception as e:
        # Bắt các lỗi hệ thống khác không lường trước được
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống không xác định trong quá trình nhận diện."
        )
