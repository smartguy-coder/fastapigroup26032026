from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    title: str = Field(examples=['Я, легенда'])
    author: str
    price: int = Field(ge=2)
    description: str = ''