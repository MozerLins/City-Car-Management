from app import db, bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum

class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False) 

    def set_password(self, password: str) -> None:
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

class Owner(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    opportunity: Mapped[bool] = mapped_column(db.Boolean, default=True)
    cars = relationship('Car', backref='owner', lazy=True)

class Car(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    color: Mapped[str] = mapped_column(Enum('yellow', 'blue', 'gray', name='car_color'), nullable=False)
    model: Mapped[str] = mapped_column(Enum('hatch', 'sedan', 'convertible', name='car_model'), nullable=False)
    owner_id: Mapped[int] = mapped_column(db.ForeignKey('owner.id'), nullable=False)
