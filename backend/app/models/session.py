from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class WritingSession(Base):
    """Stores a writing action: input, mode, and AI output for history."""

    __tablename__ = "writing_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(50), nullable=False)
    # rewrite | tone | email | expand | shorten
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[str | None] = mapped_column(String(255), nullable=True)  # e.g. tone name
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    owner = relationship("User", back_populates="sessions")
