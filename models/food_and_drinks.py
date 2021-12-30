from db import db


class FoodAndDrinks(db.Model):
    __tablename__ = "food_and_drinks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, index=True, unique=True)
    description = db.Column(db.UnicodeText)
    image_url = db.Column(db.String)
    price = db.Column(db.Float, nullable=False, default=0)
    is_available = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False, default=1
    )

    def __repr__(self):
        return self.title
