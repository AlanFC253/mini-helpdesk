from math import ceil
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketStatus,TicketPriority
from datetime import datetime


def list_tickets_paginated(db: Session, page: int, page_size: int,sort : str, order:str,status: TicketStatus | None ,priority: TicketPriority | None ,created_from: datetime  | None ,created_to: datetime  | None )-> tuple[list[Ticket], int, int]:

    
    SORT_MAP = {
    "created_at": Ticket.created_at,
    "updated_at": Ticket.updated_at,
    "priority": Ticket.priority,
    }

    query = db.query(Ticket)
    column = SORT_MAP[sort]

    if order == "desc":
        column = column.desc()
    else:
        column = column.asc()

    if status:
        query = query.filter(Ticket.status == status)

    if priority :
        query = query.filter(Ticket.priority == priority)


    if created_from is not None:
        query = query.filter(Ticket.created_at >= created_from)

    if created_to is not None:
        query = query.filter(Ticket.created_at <= created_to)


    offset = (page - 1) * page_size
    items = query.order_by(column).offset(offset).limit(page_size).all()
    total = query.count()
    pages = ceil(total / page_size) if total > 0 else 0
    return items, total, pages