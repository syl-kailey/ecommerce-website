## Description
This homework will have you develop a web store application.  **This is an individual** assignment; you may discuss general Python/SQL techniques with other students, but all code that you write must be your own! You are expected to implement the following "from scratch", i.e., you may use the basic Flask libraries, templating abilities, etc, but you may not use 3rd party libraries to provide significant portions of functionality such as user logins.

# Syl Kailey

## Application Requirements
The website should be able to display products being sold in several categories. A user visiting your web store can search for products (i.e., search for a specific item name and display that item) or display all items in a certain category. The website should display the available quantity and price for each product.

Only a logged in user can add products to a shopping cart and then checkout to complete a purchase and buy the products. To "buy" a product means to reduce the quantity from that product with the quantity that was "bought" (i.e. your database should be updated to reflect the reduction in quantity of items after checkout, not when added to the cart). 

A logged in user's shopping cart can be viewed, edited, checked out or deleted. A logged in user can also see her order history which should include the list of items purchased and total cost of the order.

## Implementation
- Python Flask will be used for all the server side scripting.
- The cart should be implemented with Session variables. Hint: the session should be based on the user login.
  - This means the shopping cart should *not* be stored in your database.
- Check user input: do not allow me to buy -2 boxes of detergent or, 100 boxes if you only have 1 in stock.
- Keep minimum information about customers: username and password, first and last name. We are not interested in addresses at this point.
- Where details are not specified in the assignment, you should assume something "reasonable" that you think the client will expect. You should record any design decisions or assumptions you made in your `Readme.md`.


## Requirements
- [X] The user can see all the products the store sells; minimum of 10 products.
- [X] The user can see all the products in a specific category; minimum of 3 categories.
- [X] Database schema and scripts to create and populate the tables.
  - [X] This must be kept in the `store_schema.sql` file.
- [X] Minimal web interface: web page does not look professional, minimal styling, no form checks.
- [X] The user can search for a specific item by name.
- [X] The user can login, but not create a new account.
  - [X] Users who are not in the DB can't login.
  - [X] Must include a sample user named `testuser` with password `testpass`
- [X] The logged in user can view, add to, edit, check out or delete their cart.
  - [X] The cart should be stored as a session variable.
- [X] The database is updated when a user checks out.
- [X] The store doesn't let a user buy negative amounts or more than is in the inventory.
- [X] A new user can sign up.
- [X] A logged in user can see his/her previous order history.
- [X] The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
- [X] Website style: products have pictures.

