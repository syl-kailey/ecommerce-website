PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS products;
CREATE TABLE products (
	name VARCHAR(50),
	price DECIMAL (10,2),
  stock INT,
	category VARCHAR(50),
  primary key (name)
  foreign key (category) references categories (name)
);

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
	name VARCHAR,
  primary key (name)
);

DROP TABLE IF EXISTS  people;
CREATE TABLE people (
	username VARCHAR(50) UNIQUE,
	password VARCHAR(50),
  name VARCHAR(50),
	email VARCHAR(50),
  primary key (username, password)
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product VARCHAR(50),
  user_name VARCHAR(50),
	quantity INTEGER,
  FOREIGN KEY(product) REFERENCES product(name)
    ON DELETE NO action
    ON UPDATE CASCADE,
  FOREIGN KEY(user_name) REFERENCES people(username)
    ON DELETE NO action
    ON UPDATE CASCADE
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_name VARCHAR(50),
  total DECIMAL,
  order_date TIMESTAMP,
  FOREIGN KEY(user_name) REFERENCES people(username)
    ON DELETE NO action
    ON UPDATE CASCADE
);


--products
INSERT INTO products VALUES ('Midnights', 10, 20, "Taylor Swift");
INSERT INTO products VALUES ('1989', 10, 20, "Taylor Swift");
INSERT INTO products VALUES ('Fearless (Taylor"s Version)', 10, 20, "Taylor Swift");
INSERT INTO products VALUES ('Reputation', 10, 20, "Taylor Swift");
INSERT INTO products VALUES ('Good Riddance', 10, 20, "Gracie Abrams");
INSERT INTO products VALUES ('This Is What It Feels Like', 10, 20, "Gracie Abrams");
INSERT INTO products VALUES ('Minor', 10, 20, "Gracie Abrams");
INSERT INTO products VALUES ('Mess It Up', 10, 20, "Gracie Abrams");
INSERT INTO products VALUES ('You Signed Up For This', 10, 20, "Maisie Peters");
INSERT INTO products VALUES ('Dressed Too Nice For A Jacket', 10, 20, "Maisie Peters");
INSERT INTO products VALUES ('Good Witch', 10, 20, "Maisie Peters");
INSERT INTO products VALUES ('It"s Your Bed Babe, It"s Your Funeral', 10, 20, "Maisie Peters");

-- categories
INSERT INTO categories VALUES ("Taylor Swift");
INSERT INTO categories VALUES ("Ariana Grande");
INSERT INTO categories VALUES ("Maisie Peters");

--people
INSERT INTO people VALUES ("testuser", "testpass", "Syl Kailey", "testuser@gmail.com");
