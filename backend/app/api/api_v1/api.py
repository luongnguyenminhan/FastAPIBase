from fastapi import APIRouter, Depends
from app.controllers.api_controller_base import APIControllerBase, handle_exceptions, get_uow
from app.schemas.user import UserCreate
from app.schemas.item import ItemCreate
from app.services.services.user_service import UserService
from app.services.services.item_service import ItemService

api_router = APIRouter()

class APIv1Controller(APIControllerBase):
    """API v1 specific controller methods"""
    
    @handle_exceptions
    async def get_users(self):
        user_service = self.get_service(UserService)
        return await user_service.get_all()

    @handle_exceptions
    async def create_user(self, user_data):
        user_service = self.get_service(UserService)
        return await user_service.create(user_data)

    @handle_exceptions
    async def get_items(self):
        item_service = self.get_service(ItemService)
        return await item_service.get_all()

    @handle_exceptions
    async def create_item(self, item_data):
        item_service = self.get_service(ItemService)
        return await item_service.create(item_data)

@api_router.get("/users/", response_model=list)
async def read_users(
    controller: APIv1Controller = Depends(lambda uow: APIv1Controller(next(get_uow())))
):
    return await controller.get_users()

@api_router.post("/users/", response_model=dict)
async def create_user(
    user: UserCreate,
    controller: APIv1Controller = Depends(lambda uow: APIv1Controller(next(get_uow())))
):
    return await controller.create_user(user)

@api_router.get("/items/", response_model=list)
async def read_items(
    controller: APIv1Controller = Depends(lambda uow: APIv1Controller(next(get_uow())))
):
    return await controller.get_items()

@api_router.post("/items/", response_model=dict)
async def create_item(
    item: ItemCreate,
    controller: APIv1Controller = Depends(lambda uow: APIv1Controller(next(get_uow())))
):
    return await controller.create_item(item)
