from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketOut

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