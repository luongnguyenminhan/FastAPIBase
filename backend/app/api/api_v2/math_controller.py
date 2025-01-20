from fastapi import APIRouter, Depends
from typing import List
from app.services.services.math_service import MathService
from app.schemas.request_schema import MathOperationRequest

math_router = APIRouter()

# Advanced Math operations
@math_router.post("/batch")
async def batch_calculate(
    operations: List[MathOperationRequest],
    math_service: MathService = Depends(MathService.get_self)
):
    results = []
    for op in operations:
        result = await math_service.calculate_operation(
            op.operation,
            op.x,
            op.y
        )
        results.append({
            "operation": op.operation,
            "result": result
        })
    return results
