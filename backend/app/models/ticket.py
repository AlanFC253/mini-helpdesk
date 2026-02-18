from datetime import datetime
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
import enum





class TicketStatus(str,enum.Enum):
    open ="open"
    in_progress = "in_progress"
    done = "done"

class TicketPriority(str,enum.Enum):
    low  = 'low'
    medium = "medium"
    high = "high"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100),nullable=False)
    description: Mapped[str] = mapped_column(String(1000),nullable=False)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus),default = TicketStatus.open,nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority),default = TicketPriority.medium,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.utcnow,onupdate=datetime.utcnow)


