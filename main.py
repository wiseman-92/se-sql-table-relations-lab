# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
# Return the first and last names of all employees in Boston.
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Find all offices that have zero employees.
df_zero_emp = pd.read_sql("""
    SELECT o.*
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
# Return employee names and their office city and state, including employees without an office.
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Return contact information for customers who have not placed an order.
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)

# STEP 5
# Return customer contact names and each payment's date and amount, largest amount first.
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Find employees whose customers have an average credit limit over 90,000.
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numcustomers DESC
""", conn)

# STEP 7
# Return order counts and total units sold for each product.
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Return the number of unique customers who ordered each product.
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Return the number of customers assigned to each office.
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10
# Return employees who sold products ordered by fewer than 20 customers.
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, e.officeCode
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    JOIN products p ON od.productCode = p.productCode
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE p.productCode IN (
        SELECT p2.productCode
        FROM products p2
        JOIN orderdetails od2 ON p2.productCode = od2.productCode
        JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY p2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName
""", conn)


conn.close()