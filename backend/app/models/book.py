from datetime import datetime
from typing import Optional, TYPE_CHECKING 
from sqlalchemy import Text, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    # This import only happens for VSCode, not when the app runs.
    from app.models.user import User

class Book(Base):
    __tablename__ = "books"

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_1_to_5'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(Text)
    
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    user: Mapped["User"] = relationship(back_populates="books")