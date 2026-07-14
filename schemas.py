from pydantic import BaseModel, Field
from datetime import datetime


class BookPriceSchema(BaseModel):
    price: int = Field(ge=2)


class BookCreateSchema(BookPriceSchema):
    title: str = Field(examples=['Я, легенда'])
    author: str
    description: str = ''


class BookSavedSchema(BookCreateSchema):
    id: str = Field(examples=['6a512ade462303c800b8bead'])
    created_at: datetime
