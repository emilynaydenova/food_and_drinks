import enum


class RoleEnum(enum.Enum):
    customer = "Customer"
    staff = "Staff"
    admin = "Admin"


class CategoryEnum(enum.Enum):
    salad = "Salad"
    soup = "Soup"
    main_dish = "Main Dish"
    dessert = "Dessert"
    drinks = "Drinks"


class StatusEnum(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
    delivered = "Delivered"


class DeliveryEnum(enum.Enum):
    takeaway = "Takeaway"
    delivery = "Home Delivery"
