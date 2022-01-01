# endpoints registration
from resources.admin import CreateStaff, CreateFirstAdmin, CreateAdmin
from resources.auth import SignUpCustomer, SignInCustomer, SignInAdmin, SignInStaff
from resources.categories import CreateCategory, CategoryDetails
from resources.food_and_drinks import CreateFoodAndDrinks, FoodAndDrinksDetails
from resources.orders import CreateOrder, OrderDetails
from resources.public_part import PublicView

routes = (
    # to get all food_and_drinks by category
    (PublicView, "/all"),  # (?category=some-Enum-value)

    # public endpoints
    (SignUpCustomer, "/users/customers/signup"),
    (SignInCustomer, "/users/customers/signin"),
    (SignInStaff, "/users/staff/signin"),
    (SignInAdmin, "/admin/signin"),

    # private endpoints
    (CreateStaff, "/admin/create-staff"),
    (CreateAdmin, "/admin/create-admin"),

    (CreateFirstAdmin, "/admin/first-admin"),

    (CreateCategory, "/orders/categories"),  # all, create
    (CategoryDetails, "/orders/categories/<int:id_>"),  # read,update,delete

    (CreateFoodAndDrinks, "/orders/food-and-drinks"),
    (FoodAndDrinksDetails, "/orders/food-and-drinks/<int:id_>"),

    (CreateOrder, "/orders/customers/order"),  # orders.py   - by customer
    (OrderDetails, "/orders/details/<int:id_>",),  # orders.py -> update,delete,view  approve,reject
)
