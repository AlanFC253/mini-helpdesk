from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate

router = APIRouter(prefix="/tickets",tags=["ticket"])

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

@router.get("/", response_model=list[TicketOut])
def list_tickets(db: Session=Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets

@router.get("/{id}", response_model=TicketOut)
def get_id(id: int, db: Session=Depends(get_db)):
    ticket = db.get(Ticket,id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found") 
    return ticket

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

@router.delete("/{id}",status_code=204)
def delete_ticket(id:int,db: Session=Depends(get_db)):

    ticket = db.get(Ticket,id)

    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()

    return