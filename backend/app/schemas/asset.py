from pydantic import BaseModel
from typing import Optional
from ..models.asset import AssetType


class AssetBase(BaseModel):
    module_id: int
    type: AssetType
    url: str


class AssetCreate(AssetBase):
    pass


class AssetRead(AssetBase):
    id: int

    class Config:
        orm_mode = True
