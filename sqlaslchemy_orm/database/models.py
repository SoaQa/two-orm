from typing import Optional

from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base


class UserAddress(Base):
    __tablename__ = "user_address"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), primary_key=True)

    user = relationship("User", back_populates="addresses")
    address = relationship("Address", back_populates="users")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(128))

    addresses = relationship("UserAddress", back_populates="user")
    invoices = relationship("Invoice", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(128))
    city: Mapped[str] = mapped_column(String(128))
    street: Mapped[str] = mapped_column(String(128))
    house_number: Mapped[int] = mapped_column(Integer())

    users = relationship("UserAddress", back_populates="address")

    __table_args__ = (
        CheckConstraint(house_number >= 0, name='check_house_number_positive'),
        {}
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    cost: Mapped[float] = mapped_column(Numeric(12, 2, ))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="invoices")
