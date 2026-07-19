from datetime import date
from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Problem(Base):
    __tablename__ = "Problems"
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String, 
        unique=True, 
        nullable=False
    ) 
    difficulty: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        String, 
        nullable=False
    )
    
    #subcategory might not present
    subcategory: Mapped[str | None] = mapped_column(
        String, 
        nullable=True
    )
    last_ac_date: Mapped[date] = mapped_column(
        Date, 
        nullable=False
    )
    