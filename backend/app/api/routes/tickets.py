from fastapi import APIRouter, Depends , HTTPException, Query
from sqlalchemy.orm import Session
from math import ceil
from app.db.session import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate,TicketListResponse,TicketStatus,TicketPriority
from app.crud.ticket import list_tickets_paginated
from typing import Literal
from datetime import datetime


router = APIRouter(prefix="/tickets",tags=["ticket"])


#Post
@router.post("/",response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate,db: Session = Depends(get_db)):

    new_ticket = Ticket(
        title = payload.title,
        description = payload.description,
        priority = payload.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# Gets
@router.get("/", response_model=TicketListResponse)
def list_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort: Literal["created_at", "updated_at", "priority"] = Query("created_at"),
    order: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
    status: TicketStatus | None = Query(None),
    priority: TicketPriority | None = Query(None),
    created_from: datetime | None = Query(None),
    created_to: datetime | None = Query(None),
):
    
    if created_from and created_to and created_from > created_to:
        raise HTTPException(status_code=400, detail="created_from cannot be after created_to")

    items, total, pages = list_tickets_paginated(db, page, page_size,sort,order,status,priority,created_from,created_to)


    return {
    "items": items,
    "total":total,
    "page": page,
    "page_size": page_size,
    "pages":pages,
    }


@router.get("/{id}", response_model=TicketOut)
def get_id(id: int, db: Session=Depends(get_db)):
    ticket = db.get(Ticket,id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found") 
    return ticket


# Patch

@router.patch("/{id}", response_model=TicketOut)
def update_ticket(id:int,payload:TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket,id)

    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    
    update_data = payload.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(ticket,field,value)  

    db.commit()
    db.refresh(ticket)
    return ticket

#Delete
@router.delete("/{id}",status_code=204)
def delete_ticket(id:int,db: Session=Depends(get_db)):

    ticket = db.get(Ticket,id)

    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()

    return