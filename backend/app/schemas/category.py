from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: str

    class Config:
        from_attributes = True

