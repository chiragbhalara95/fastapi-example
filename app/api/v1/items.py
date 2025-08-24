from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Annotated

from app.db import get_session
from app.models.item import Item

router = APIRouter(prefix="/items", tags=["items"])

# ✅ Pydantic v2 schema with proper validation
class ItemCreate(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            pattern=r"^[a-zA-Z0-9 ]+$",
            description="Name must be 3–50 characters, only letters, numbers, and spaces"
        )
    ]

@router.post("/")
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    new_item = Item(name=item.name)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

@router.get("/")
async def list_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item))
    return result.scalars().all()

@router.get("/{item_id}")
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
