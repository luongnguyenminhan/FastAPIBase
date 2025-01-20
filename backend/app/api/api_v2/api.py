from fastapi import APIRouter, Depends
from typing import Optional
from app.controllers.api_controller_base import APIControllerBase, handle_exceptions, get_uow
from app.schemas.request_schema import (
    MathOperationRequest, UserMetricsRequest,
    ItemValueRequest, ItemDiscountRequest
)
from app.schemas.response_schema import (
    MessageResponse, EchoResponse, MathOperationResponse,
    UserMetricsResponse, ItemValueResponse, ItemDiscountResponse
)
from app.services.services.math_service import MathService
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService

api_router = APIRouter()

class APIv2Controller(APIControllerBase):
    """API v2 specific controller methods"""
    
    @handle_exceptions
    async def calculate_math_operation(self, operation: str, x: float, y: float) -> float:
        math_service = self.get_service(MathService)
        return await math_service.calculate_operation(operation, x, y)

    @handle_exceptions
    async def calculate_user_metrics(self, metric_values: list[float]) -> dict:
        user_service = self.get_service(UserService)
        return await user_service.calculate_user_metrics(metric_values)

    @handle_exceptions
    async def calculate_item_value(self, price: float, quantity: int) -> float:
        item_service = self.get_service(ItemService)
        return await item_service.calculate_total_value(price, quantity)

    @handle_exceptions
    async def calculate_item_discount(self, price: float, discount_percentage: float) -> float:
        item_service = self.get_service(ItemService)
        return await item_service.calculate_discount(price, discount_percentage)

@api_router.get("/hello", response_model=MessageResponse)
async def get_hello_v2():
    return MessageResponse(message="Hello from API v2!")

@api_router.get("/echo/{message}", response_model=EchoResponse)
async def get_echo_v2(message: str, prefix: Optional[str] = None):
    response = message if not prefix else f"{prefix}: {message}"
    return EchoResponse(echo=response, version="v2")

@api_router.post("/math/{operation}", response_model=MathOperationResponse)
async def calculate_math_operation(
    operation: str,
    request: MathOperationRequest,
    controller: APIv2Controller = Depends(lambda uow: APIv2Controller(next(get_uow())))
):
    result = await controller.calculate_math_operation(operation, request.x, request.y)
    return MathOperationResponse(operation=operation, result=result)

@api_router.post("/users/metrics", response_model=UserMetricsResponse)
async def calculate_user_metrics(
    request: UserMetricsRequest,
    controller: APIv2Controller = Depends(lambda uow: APIv2Controller(next(get_uow())))
):
    metrics = await controller.calculate_user_metrics(request.metric_values)
    return UserMetricsResponse(**metrics)

@api_router.post("/items/value", response_model=ItemValueResponse)
async def calculate_item_value(
    request: ItemValueRequest,
    controller: APIv2Controller = Depends(lambda uow: APIv2Controller(next(get_uow())))
):
    total = await controller.calculate_item_value(request.price, request.quantity)
    return ItemValueResponse(total_value=total)

@api_router.post("/items/discount", response_model=ItemDiscountResponse)
async def calculate_item_discount(
    request: ItemDiscountRequest,
    controller: APIv2Controller = Depends(lambda uow: APIv2Controller(next(get_uow())))
):
    discounted_price = await controller.calculate_item_discount(
        request.price, request.discount_percentage
    )
    return ItemDiscountResponse(
        original_price=request.price,
        discount_percentage=request.discount_percentage,
        discounted_price=discounted_price
    )
