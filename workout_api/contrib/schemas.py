from typing import Annotated
from pydantic import UUID4, BaseModel, Field
from datetime import datetime


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True


class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Daata de criação")]