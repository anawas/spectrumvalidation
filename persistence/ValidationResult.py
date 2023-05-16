from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class ValidationResult(Base):
    __tablename__ = "snr"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(30))
    snr: Mapped[float]

    def __repr__(self) -> str:
        return f"file={self.filename!r}, type={self.type!r}, snr={self.snr!r})"
