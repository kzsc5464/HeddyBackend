# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List, Optional

# # from api import deps
# from schemas.item import ItemCreate, ItemUpdate, Item
# from crud.item import item_crud

# router = APIRouter()

# @router.get("/", response_model=List[Item])
# async def list_items(
#     skip: int = 0,
#     limit: int = Query(default=10, le=100),
#     category: Optional[str] = None,
#     db: AsyncSession = Depends(deps.get_db)
# ):
#     """
#     List items with optional filtering
#     """
#     items = await item_crud.get_multi(
#         db,
#         skip=skip,
#         limit=limit,
#         category=category
#     )
#     return items

# @router.post("/", response_model=Item)
# async def create_item(
#     item_in: ItemCreate,
#     db: AsyncSession = Depends(deps.get_db),
#     current_user = Depends(deps.get_current_active_user)
# ):
#     """
#     Create new item
#     """
#     item = await item_crud.create_with_owner(
#         db,
#         obj_in=item_in,
#         owner_id=current_user.id
#     )
#     return item

# @router.get("/{item_id}", response_model=Item)
# async def get_item(
#     item_id: int,
#     db: AsyncSession = Depends(deps.get_db)
# ):
#     """
#     Get item by ID
#     """
#     item = await item_crud.get(db, id=item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

# @router.put("/{item_id}", response_model=Item)
# async def update_item(
#     item_id: int,
#     item_in: ItemUpdate,
#     db: AsyncSession = Depends(deps.get_db),
#     current_user = Depends(deps.get_current_active_user)
# ):
#     """
#     Update item
#     """
#     item = await item_crud.get(db, id=item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if item.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     item = await item_crud.update(db, db_obj=item, obj_in=item_in)
#     return item

# @router.delete("/{item_id}")
# async def delete_item(
#     item_id: int,
#     db: AsyncSession = Depends(deps.get_db),
#     current_user = Depends(deps.get_current_active_user)
# ):
#     """
#     Delete item
#     """
#     item = await item_crud.get(db, id=item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if item.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     await item_crud.remove(db, id=item_id)
#     return {"status": "success"}