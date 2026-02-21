from datetime import datetime
import enum
from pydantic import BaseModel, Field
from typing import List

class TicketPriority(str,enum.Enum):
    low  = 'low'
    medium = "medium"
    high = "high"

class TicketStatus(str,enum.Enum):
    open ="open"
    in_progress = "in_progress"
    done = "done"

class TicketCreate(BaseModel):
    title: str = Field(min_length = 3, max_length=100)
    description: str = Field(min_length = 3, max_length=2000)
    priority: TicketPriority = TicketPriority.medium

class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
    priority: TicketPriority | None = None
    status: TicketStatus | None = None



class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    items: List[TicketOut]
    total: int
    page: int
    page_size: int
    pages: int