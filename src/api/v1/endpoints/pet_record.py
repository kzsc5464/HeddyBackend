from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from core.database import get_database
from core.security import get_current_user
from models.pet_record import PetRecordCollection
from schemas.pet_record import PetRecord, PetRecordCreate, PetRecordUpdate

router = APIRouter()


@router.post("/pet-records/", response_model=PetRecord)
async def create_pet_record(
        title: str,
        description: str,
        pet_name: str,
        record_date: datetime,
        images: List[UploadFile] = File(...),
        db: AsyncIOMotorDatabase = Depends(get_database),
        current_user=Depends(get_current_user)
):
    """
    반려동물 기록 카드 생성
    """
    # 이미지 저장 로직 (예: S3나 로컬 스토리지에 저장)
    image_urls = []
    for image in images:
        # 이미지 저장 로직 구현
        image_url = await save_image(image)  # 실제 구현 필요
        image_urls.append(image_url)

    record_data = {
        "title": title,
        "description": description,
        "pet_name": pet_name,
        "record_date": record_date,
        "image_urls": image_urls,
        "user_id": str(current_user.id),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    created_record = await PetRecordCollection.create(db, record_data)
    return created_record


@router.get("/pet-records/", response_model=List[PetRecord])
async def get_pet_records(
        skip: int = 0,
        limit: int = 10,
        db: AsyncIOMotorDatabase = Depends(get_database),
        current_user=Depends(get_current_user)
):
    """
    사용자의 반려동물 기록 카드 목록 조회
    """
    records = await PetRecordCollection.get_multi(
        db,
        query={"user_id": str(current_user.id)},
        skip=skip,
        limit=limit
    )
    return records


@router.get("/pet-records/{record_id}", response_model=PetRecord)
async def get_pet_record(
        record_id: str,
        db: AsyncIOMotorDatabase = Depends(get_database),
        current_user=Depends(get_current_user)
):
    """
    특정 반려동물 기록 카드 조회
    """
    record = await PetRecordCollection.get_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this record")
    return record


@router.put("/pet-records/{record_id}", response_model=PetRecord)
async def update_pet_record(
        record_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        pet_name: Optional[str] = None,
        record_date: Optional[datetime] = None,
        new_images: List[UploadFile] = File(None),
        db: AsyncIOMotorDatabase = Depends(get_database),
        current_user=Depends(get_current_user)
):
    """
    반려동물 기록 카드 수정
    """
    record = await PetRecordCollection.get_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to modify this record")

    update_data = {}
    if title:
        update_data["title"] = title
    if description:
        update_data["description"] = description
    if pet_name:
        update_data["pet_name"] = pet_name
    if record_date:
        update_data["record_date"] = record_date

    if new_images:
        image_urls = []
        for image in new_images:
            image_url = await save_image(image)  # 실제 구현 필요
            image_urls.append(image_url)
        update_data["image_urls"] = image_urls

    update_data["updated_at"] = datetime.utcnow()

    updated_record = await PetRecordCollection.update(
        db,
        record_id,
        update_data
    )
    return updated_record


@router.delete("/pet-records/{record_id}")
async def delete_pet_record(
        record_id: str,
        db: AsyncIOMotorDatabase = Depends(get_database),
        current_user=Depends(get_current_user)
):
    """
    반려동물 기록 카드 삭제
    """
    record = await PetRecordCollection.get_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this record")

    # 이미지 파일도 함께 삭제
    for image_url in record.image_urls:
        await delete_image(image_url)  # 실제 구현 필요

    await PetRecordCollection.delete(db, record_id)
    return {"detail": "Record successfully deleted"}