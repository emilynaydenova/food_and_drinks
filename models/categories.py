from db import db
from models.enums import CategoryEnum


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.Enum(CategoryEnum),
        default=CategoryEnum.salad,
        unique=True,
        index=True,
        nullable=False,
    )
    image_url = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    food_and_drinks = db.relationship(
        "FoodAndDrinks", backref="category", lazy="dynamic"
    )

    def __repr__(self):
        return self.title.value
