from pydantic import BaseModel


class Points(BaseModel):
    points: int
    medal: str


class RankingEntry(BaseModel):
    user_id: int
    name: str
    role: str
    points: int

    class Config:
        orm_mode = True
