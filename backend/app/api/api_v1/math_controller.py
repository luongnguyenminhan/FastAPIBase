from fastapi import APIRouter, Depends
from app.services.services.math_service import MathService
from app.schemas.request_schema import MathOperationRequest

math_router = APIRouter()


# Math operations endpoints
@math_router.post("/{operation}", operation_id="calculate_math_v1")
async def calculate(
        operation: str,
        request: MathOperationRequest,
        math_service: MathService = Depends(MathService.get_self)
):
    return await math_service.calculate_operation(operation, request.x, request.y)
