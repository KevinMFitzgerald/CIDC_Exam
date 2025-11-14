from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class AuthorDB(Base):
    __tablename__="AuthorDB"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    email:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    year_started:Mapped[int]=mapped_column(Integer(),nullable=False)
    
book:Mapped[list["bookdb"]]=relationship(back_populates="owner",cascade="all")

class bookdb(Base):
    __tablename__="Book"
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(255),nullable=False)
    pages:Mapped[int]=mapped_column(Integer(),nullable=False)
    Author_id:Mapped[int]=mapped_column(ForeignKey("Author.id",ondelete="CASCADE"),nullable=False)

Author=Mapped["AuthorDB"]=relationship(back_populates="book")