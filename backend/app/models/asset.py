from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from ..db.session import Base
import enum


class AssetType(str, enum.Enum):
    video = "video"
    pdf = "pdf"
    infographic = "infographic"
    audio = "audio"


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    type = Column(Enum(AssetType), nullable=False)
    url = Column(String, nullable=False)
