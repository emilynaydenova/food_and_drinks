# Food and Drinks
**Flask RESTful SoftUni student project** <br/>

This project can be used as a flask-driven restful API backend for restaurants 
delivering food and drinks.<br/>
This is not an original idea, but can be MVPed in the future for an application,<br/>
helping a friend of mine to deliver customer orders. <br/>
My base idea comes from [Food Ordering app](https://food-ordering.app/), which backend is written in Go.<br>
My project is created by me thanks to Ines Ivanova's lectures "Web Applications with Flask"<br>
and there are scripts very similar to those shown in the videos.

**Technologies used:**

**Python3** - A programming language that lets you work more quickly (The universe loves speed!).<br/>
**Flask** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.<br/>
**Flask-Restful** - an extension for Flask that adds support for building REST APIs in Python using Flask as the backend.<br/>
**PostgreSQL** – Postgres database offers many advantages over others.<br/>
**Flask-SQLAlchemy** - provides a nice “Pythonic” way of interacting with databases.<br/>
**JWT authentication** - a secure way to authenticate users and share information.<br/>
Minor dependencies can be found in the **requirements.txt** file on the root folder.<br/>

**Third party services used:**<br/>

**AWS S3 service** - cloud storage service.<br/>
**Open Weather Map API** - can get weather data in any location on the earth.<br/>

**Short description of application usage:** 

At the first stage, admins and staff members user accounts are created by an admin.<br/>
Admin also creates some categories of food and drinks (there are 5 possible choices).<br/>
Admin or staff member add food and drinks items by category. These items can be defined <br/>
as available or not available at any moment.<br/>

Customer can view all offered items and after registration or login, can place an order.<br/>
Staff member can approve order, reject order or mark it as delivered.<br/>

At a later stage, application may track delivering and send emails to the customer account<br/>
with their order status.<br/>

**RESTful endpoints**

_**_Home page_**_

| Endpoint            | HTTP<br/> Method | Result                                                                                                    | 
|---------------------|------------------|-----------------------------------------------------------------------------------------------------------|
| /all?category="..." | GET              | shows all available food and drinks items by category<br/>and the weather data for the restaurant's place |



*... there are predefined types of categories in /models/enums.py<br/>

_Endpoints implementation can be found under:_ 
 * /resources/home_page.py <br/>

_**_Users management_**_
  
| Endpoint                | HTTP<br/> Method | Result                                       | Authorization       |
|-------------------------|------------------|----------------------------------------------|---------------------|
| /admin/first-admin      | POST             | Create first admin user<br/>with hidden data | during installation |
| /admin/create-admin     | POST             | Create admin user                            | admin               |
| /admin/create-staff     | POST             | Create staff member user                     | admin               |
| /users/customers/signup | POST             | Customer user self registration              |                     |
| /users/customers/signin | POST             | Customer user login                          |                     |
| /users/staff/signin     | POST             | Staff member user login                      |                     |
| /admin/signin           | POST             | Admin user login                             |                     |

_Endpoints implementation can be found under:_<br/>
 * /resources/admin.py <br/>
 * /resources/auth.py <br/>

Here may be added the following features:
- user's change of password
- clear password and sending password reset
- login with FB account as 3rd party service,etc.

_**_Category creation and management_**_

| Endpoint                     | HTTP<br/>Method | Result              | Authorization |
|------------------------------|-----------------|---------------------|---------------|
| /orders/categories           | POST            | Create category     | admin         |
| /orders/categories           | GET             | View all categories | admin         |
| /orders/categories/<int:id_> | GET             | View a category     | admin         |
| /orders/categories/<int:id_> | PUT             | Update a category   | admin         |
| /orders/categories/<int:id_> | DELETE          | Delete a category   | admin         |

_Endpoints implementation can be found under_: <br/>
 * /resources/categories.py <br/> 
 
_**_Food and drinks items creation and management_**_

| Endpoint                          | HTTP<br/>Method | Result                        | Authorization |
|-----------------------------------|-----------------|-------------------------------|---------------|
| /orders/food-and-drinks           | POST            | Create food or drink item     | admin,staff   |
| /orders/food-and-drinks           | GET             | View all food and drink items | admin,staff   |
| /orders/food-and-drinks/<int:id_> | GET             | View a category               | admin,staff   |
| /orders/food-and-drinks/<int:id_> | PUT             | Update a category             | admin,staff   |
| /orders/food-and-drinks/<int:id_> | DELETE          | Delete a category             | admin,staff   |

_Endpoints implementation can be found under_: <br/>
 * /resources/food_and_drinks.py <br/> 

_**_Orders creation and management_**_

| Endpoint                             | HTTP<br/>Method | Result                                                   | Authorization |
|--------------------------------------|-----------------|----------------------------------------------------------|---------------|
| /orders/customers/order              | POST            | Create an order                                          | customer      |
| /orders/customers/order?status="..." | GET             | View all orders with definite status                     | staff         |
| /orders/details/<int:id_>            | GET             | View their order                                         | customer      |
| /orders/details/<int:id_>            | PUT             | Change order's items while status is<br/>still "pending" | customer      |
| /orders/approvement/<int:id_>        | PUT             | Update order status                                      | staff         |

_Endpoints implementation can be found under_: <br/>
 * /resources/orders.py <br/> 
