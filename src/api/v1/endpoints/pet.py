from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.pet import PetCollection, PetType
from schemas.pet import PetCreate, PetUpdate
from core.database import get_database

router = APIRouter()

@router.post("/", response_model=dict)
async def create_pet(
    pet_data: PetCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """새로운 반려동물을 등록합니다."""
    try:
        pet_dict = pet_data.model_dump()
        pet = await PetCollection.create(db, pet_dict)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}", response_model=dict)
async def get_pet(
    pet_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """특정 ID의 반려동물 정보를 조회합니다."""
    pet = await PetCollection.get_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"status": "success", "data": pet}

@router.get("/list", response_model=dict)
async def list_pets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = None,
    email: Optional[PetType] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """반려동물 목록을 조회합니다. 검색과 필터링이 가능합니다."""
    pets = await PetCollection.list_pets(
        db,
        skip=skip,
        limit=limit,
        search=search,
        email=email
    )
    return {
        "status": "success",
        "data": pets,
        "metadata": {
            "skip": skip,
            "limit": limit,
            "search": search,
            "email": email
        }
    }

@router.put("/{pet_id}", response_model=dict)
async def update_pet(
    pet_id: str,
    pet_data: PetUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """특정 반려동물의 정보를 수정합니다."""
    # 반려동물 존재 확인
    existing_pet = await PetCollection.get_by_id(db, pet_id)
    if not existing_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # 업데이트할 데이터 준비
    update_data = pet_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    # 반려동물 정보 업데이트
    updated_pet = await PetCollection.update(db, pet_id, update_data)
    if not updated_pet:
        raise HTTPException(status_code=400, detail="Update failed")
    
    return {"status": "success", "data": updated_pet}

@router.delete("/{pet_id}", response_model=dict)
async def delete_pet(
    pet_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """특정 반려동물의 정보를 삭제합니다."""
    # 반려동물 존재 확인
    existing_pet = await PetCollection.get_by_id(db, pet_id)
    if not existing_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    # 반려동물 삭제
    success = await PetCollection.delete(db, pet_id)
    if not success:
        raise HTTPException(status_code=400, detail="Delete failed")
    
    return {"status": "success", "message": "Pet deleted successfully"}

@router.get("/type/{pet_type}", response_model=dict)
async def get_pets_by_type(
    pet_type: PetType,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """특정 타입의 반려동물 목록을 조회합니다."""
    pets = await PetCollection.get_by_type(db, pet_type)
    return {
        "status": "success",
        "data": pets,
        "metadata": {
            "pet_type": pet_type,
            "count": len(pets)
        }
    }