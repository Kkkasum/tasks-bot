from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, BIGINT, text
from sqlalchemy.dialects.postgresql import ARRAY


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    balance: Mapped[int] = mapped_column(server_default=text('0'))
    wallet: Mapped[str | None] = mapped_column(String(48))
    ref_id: Mapped[int | None] = mapped_column(BIGINT)
    tasks: Mapped[list[str] | None] = mapped_column(ARRAY(String(10)), server_default="{}")
