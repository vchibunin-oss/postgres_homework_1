CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    title VARCHAR(100),
    birth_date DATE,
    notes TEXT
);

CREATE TABLE customers (
    customer_id VARCHAR(5) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id VARCHAR(5) NOT NULL,
    employee_id INTEGER NOT NULL,
    order_date DATE,
    ship_city VARCHAR(100),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_orders_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);