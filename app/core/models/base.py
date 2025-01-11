#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)