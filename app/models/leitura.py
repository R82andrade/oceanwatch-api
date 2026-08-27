from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Leitura(Base):
    __tablename__ = "leituras"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    boia_id: Mapped[int] = mapped_column(
        ForeignKey("boias.id"),
        nullable=False
    )

    temperatura_agua: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    altura_onda: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    velocidade_vento: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
