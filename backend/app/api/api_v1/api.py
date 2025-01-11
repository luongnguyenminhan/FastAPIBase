from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.item import ItemCreate, ItemUpdate
from typing import List
import logging
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository

api_router = APIRouter()
logger = logging.getLogger(__name__)

@api_router.post("/users/", response_model=dict)
async def create_user_with_items(
    user_data: UserCreate,
    items: List[ItemCreate],
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        with user_repo.transaction():
            # Create user and items in a single transaction
            user = await user_service.create(user_data)
            
            created_items = []
            for item in items:
                item.owner_id = user.id
                created_item = await item_service.create(item)
                created_items.append(created_item)

            return {
                "user": user,
                "items": created_items
            }
    except Exception as e:
        logger.error(f"Error in create_user_with_items: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.put("/users/{user_id}/bulk-update")
async def bulk_update_user_and_items(
    user_id: int,
    user_update: UserUpdate,
    items_update: List[ItemUpdate],
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        with user_repo.transaction():
            # Update user
            user = await user_service.update(user_id, user_update.dict(exclude_unset=True))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Update items
            updated_items = []
            for item_update in items_update:
                if item_update.id is None:
                    raise HTTPException(status_code=400, detail="Item ID is required")
                
                item = await item_service.get(item_update.id)
                if not item or item.owner_id != user_id:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Item {item_update.id} not found or doesn't belong to user"
                    )
                
                updated_item = await item_service.update(
                    item_update.id, 
                    item_update.dict(exclude_unset=True)
                )
                updated_items.append(updated_item)

            return {
                "user": user,
                "updated_items": updated_items
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk_update_user_and_items: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/users/complex-operation")
async def complex_user_operation(
    user_data: UserCreate,
    items: List[ItemCreate],
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        with user_repo.transaction():
            # Create user
            user = await user_service.create(user_data)
            
            # Create items and associate with user
            created_items = []
            for item in items:
                item.owner_id = user.id
                created_item = await item_service.create(item)
                created_items.append(created_item)

            return {"user": user, "items": created_items}

    except Exception as e:
        logger.error(f"Error in complex_user_operation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/users/batch-processing")
async def batch_process_users_and_items(
    users_data: List[UserCreate],
    items_per_user: List[List[ItemCreate]],
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        async def batch_transaction():
            results = []
            for user_data, user_items in zip(users_data, items_per_user):
                # Create user
                user = await user_service.create(user_data)
                
                # Create items for this user
                user_items_created = []
                for item in user_items:
                    item.owner_id = user.id
                    created_item = await item_service.create(item)
                    user_items_created.append(created_item)
                
                results.append({
                    "user": user,
                    "items": user_items_created
                })
            
            return results

        return await user_service.execute_in_transaction(batch_transaction)

    except Exception as e:
        logger.error(f"Error in batch_process_users_and_items: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.put("/items/bulk-transfer")
async def transfer_items_between_users(
    from_user_id: int,
    to_user_id: int,
    item_ids: List[int],
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        async def transfer_transaction():
            # Verify both users exist
            from_user = await user_service.get(from_user_id)
            to_user = await user_service.get(to_user_id)
            
            if not from_user or not to_user:
                raise HTTPException(status_code=404, detail="User not found")

            transferred_items = []
            for item_id in item_ids:
                item = await item_service.get(item_id)
                if item and item.owner_id == from_user_id:
                    await item_service.update(item_id, {"owner_id": to_user_id})
                    transferred_items.append(item)

            # Update item counts for both users
            await user_service.update(from_user_id, 
                {"items_count": from_user.items_count - len(transferred_items)})
            await user_service.update(to_user_id, 
                {"items_count": to_user.items_count + len(transferred_items)})

            return {
                "transferred_items": transferred_items,
                "from_user": from_user,
                "to_user": to_user
            }

        return await user_service.execute_in_transaction(transfer_transaction)

    except Exception as e:
        logger.error(f"Error in transfer_items_between_users: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.delete("/users/{user_id}")
async def delete_user_and_items(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        with user_repo.transaction():
            # Get user's items
            user = await user_service.get(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Delete all user's items first
            items = await item_service.get_by_owner(user_id)
            for item in items:
                await item_service.delete(item.id)

            # Delete user
            deleted_user = await user_service.delete(user_id)

            return {
                "message": "User and associated items deleted successfully",
                "user": deleted_user,
                "deleted_items_count": len(items)
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_user_and_items: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/users/{user_id}/statistics")
async def get_user_statistics(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepository(db)
        item_repo = ItemRepository(db)
        user_service = UserService(user_repo)
        item_service = ItemService(item_repo)

        with user_repo.transaction():
            user = await user_service.get(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            items = await item_service.get_by_owner(user_id)
            total_items = len(items)
            active_items = sum(1 for item in items if item.is_active)
            total_value = sum(item.price for item in items)

            return {
                "user": user,
                "statistics": {
                    "total_items": total_items,
                    "active_items": active_items,
                    "inactive_items": total_items - active_items,
                    "total_value": total_value
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_statistics: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))