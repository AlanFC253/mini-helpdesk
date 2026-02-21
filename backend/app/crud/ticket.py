from math import ceil
from sqlalchemy.orm import Session
from app.models.ticket import Ticket


def list_tickets_paginated(db: Session, page: int, page_size: int,sort : str, order:str) -> tuple[list[Ticket], int, int]:

    
    SORT_MAP = {
    "created_at": Ticket.created_at,
    "updated_at": Ticket.updated_at,
    "priority": Ticket.priority,
    }

    column = SORT_MAP[sort]

    if order == "desc":
        column = column.desc()
    else:
        column = column.asc()

    offset = (page - 1) * page_size
    items = db.query(Ticket).order_by(column).offset(offset).limit(page_size).all()
    total = db.query(Ticket).count()
    pages = ceil(total / page_size) if total > 0 else 0
    return items, total, pages