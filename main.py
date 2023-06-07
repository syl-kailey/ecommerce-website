import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash
import datetime

app = Flask('app')
app.secret_key = "secret"


@app.route('/', methods = ['GET','POST'])
def login():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  
  if request.method == 'POST' and "username" in request.form and "password" in request.form:
    username = request.form["username"]
    password = request.form["password"]
    cursor.execute("SELECT * FROM people WHERE username = ? AND password = ?", (username, password,))
    person = cursor.fetchall()
    if person:
      session["username"] = username
      return render_template("m_products.html", username = username)
    else:
      error1 = "Incorrect log in information. You may continue as a guest."
      return render_template("login.html", error1 = error1)
  return render_template("login.html")

#GUEST USER
@app.route('/g_products')
def g_products():
  return render_template("g_products.html")

#MEMBER USER
@app.route('/m_products')
def m_products():
  username = session["username"]
  session['cart'] = []
  connection = sqlite3.connect('myDatabase.db')
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM people WHERE username = ?", (username,))
  people = cursor.fetchone()
  name = people["name"]
  username = people["username"]
  return render_template("m_products.html", name = name, username = username)

#SEARCH
@app.route('/search', methods = ["POST", "GET"])
def search():
  member=False
  if 'username' in session:
    member=True
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  print ("hello")
  if request.method == 'POST' and "product_name" in request.form:
    product_name = request.form['product_name']
    cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
    product = cursor.fetchone()
    print (product)
  
    if product:
      return render_template("search.html", product = product, show_result=True, member=member)
    else:
      return render_template("search.html", error = "Item not found", show_result=False)
      
  if request.method == 'POST' and "category_name" in request.form:
    category_name = request.form['category_name']
    cursor.execute("SELECT * FROM products WHERE category = ?", (category_name,))
    products = cursor.fetchall()
    connection.commit()
    print (products)
  
    if products:
      return render_template("search.html", products = products, show_results=True, member =member)
    else:
      return render_template("search.html", error = "Item not found", show_results=False)
  else:
    return render_template("search.html", show_results=False)
    
#VIEW CART
@app.route('/cart')
def view_cart():
  if 'username' in session:
    if 'cart' not in session:
      session['cart'] = []
      
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cart WHERE user_name = ?", (session["username"],))
    connection.commit()
    contents = cursor.fetchall()
  
    cart = []
    for product in contents:
      cart.append({'product': product['product'], 'quantity': product['quantity']})
    session['cart'] = cart
    
    return render_template("cart.html", cart=session['cart'], username = session['username'])
  return render_template("cart.html")

#ADD TO CART
@app.route('/add_to_cart', methods=["POST", "GET"])
def add_to_cart():
  if 'username' in session:
    member=True
    
    if 'cart' not in session:
      session['cart'] = []
    if request.method == 'POST' and "product" in request.form and "quantity" in request.form: 
      product = request.form['product']
      quantity = request.form['quantity']
      item = {'product': product, 'quantity': int(quantity)}
      session['cart'].append(item)

      connection = sqlite3.connect("myDatabase.db")
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      cursor.execute("INSERT INTO cart (user_name, product, quantity) VALUES (?,?,?)",(session["username"], product, quantity))
      connection.commit()
      
      return redirect(url_for('m_products'))
  return redirect(url_for('view_cart'))
  

#EDIT CART
@app.route('/edit_cart', methods=["POST", "GET"])
def edit_cart():
  if 'username' in session:

    if 'cart' not in session:
      session['cart'] = []
      
    if request.method == 'POST' and "product" in request.form and "quantity" in request.form:
      user_name = session["username"]
      product = request.form['product']
      quantity = int(request.form['quantity'])
      item = {'product': product, 'quantity': int(quantity)}

      connection = sqlite3.connect("myDatabase.db")
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      cursor.execute("UPDATE cart SET quantity = ? WHERE product = ?", (quantity, product,))
      connection.commit()
      
      for item in session['cart']:
        if product == product:
          item['quantity'] = quantity
          break
            
  return redirect(url_for('view_cart'))


#REMOVE FROM CART
@app.route('/remove_from_cart', methods=["POST", "GET"])
def remove_from_cart():
  if 'username' in session:

    if 'cart' not in session:
      session['cart'] = []
      
    if request.method == 'POST' and "product" in request.form:
      product = request.form['product']
      
      connection = sqlite3.connect("myDatabase.db")
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      cursor.execute("DELETE FROM cart WHERE product = ? AND user_name = ?", (product, session['username'],))
      connection.commit()
      item = {'product': product}
      for item in session['cart']:
        if item['product'] == product:
          session['cart'].remove(item)
          break
  print(session['cart'])          
  return redirect(url_for('view_cart'))

#CHECKOUT
@app.route('/checkout', methods=["POST", "GET"])
def checkout():
  if 'username' in session:
    if 'cart' not in session:
      session['cart'] = []
      
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    total = 0
    for item in session['cart']:
      product = item['product']
      quantity = item['quantity']
      
      if quantity < 0:
        error = "You cannot buy a negative amount of items"
        return render_template("checkout.html", total = total, error=error)
        
      cursor.execute("SELECT * FROM products WHERE name = ?", (product,))
      connection.commit()
      product_info = cursor.fetchone()
      print(product_info)
      
      if product_info is not None:
        if quantity > product_info['stock']:
          error = "We are out of stock for one or more of your items"
          return render_template("checkout.html", total = total, error=error)
  
        price = product_info['price']
        total += quantity*price

        if request.method == 'POST':
          new_stock =  product_info['stock'] - quantity
          cursor.execute("UPDATE products SET stock = ? WHERE name = ?", (new_stock, product,))
          connection.commit()

    if request.method == 'POST':
      user_name = session["username"]
      order_date = datetime.datetime.now()
      cursor.execute("INSERT INTO orders (user_name, order_date, total) VALUES (?,?,?)", (user_name, order_date, total) )
      orders = cursor.fetchall()
      connection.commit()
      print(orders)
      
      session.pop('cart', None)
      cursor.execute("DELETE FROM cart WHERE user_name = ?", (session["username"],))
      connection.commit()
      return redirect(url_for('m_products'))
    return render_template("checkout.html", total = total)

  return render_template("checkout.html", total = total)

@app.route('/sign_up', methods = ['GET','POST'])
def sign_up():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  
  if request.method == 'POST' and "username" in request.form and "password" in request.form and "name" in request.form and "email" in request.form:
    
    username = request.form["username"]
    password = request.form["password"]
    name = request.form["name"]
    email = request.form["email"]
    cursor.execute("SELECT * FROM people WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
      error = "Username is taken. Try a new username."
      return render_template('login.html', error = error)
      
    cursor.execute("INSERT INTO people (username, password, name, email) VALUES (?,?,?,?)", (username, password, name, email,))
    connection.commit()
    error = "Now log in to the website."
  return render_template('login.html', error = error)

#VIEW ORDERS
@app.route('/view_orders')
def view_orders():
  if 'username' in session:
    
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE user_name = ?", (session['username'],))
    orders = cursor.fetchall()
    connection.close()
    return render_template("orders.html", orders = orders)
    
  return redirect(url_for('login'))

#VIEW ORDERS
@app.route('/sign_out')
def sign_out():
  if 'username' in session:
    session.pop('username', None)
  return redirect(url_for('login'))

app.run(host='0.0.0.0', port=8080)
