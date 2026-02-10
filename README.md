# Test_Aiti_Guru
# Задание 1

-- Таблица номенклатуры
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL
);

-- Дерево категорий (категории товаров с произвольной глубиной вложенности)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES categories(id)
);

-- Связь продуктов с категориями
CREATE TABLE product_categories (
    product_id INT REFERENCES products(id),
    category_id INT REFERENCES categories(id),
    PRIMARY KEY(product_id, category_id)
);

-- Таблица клиентов
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

-- Таблица заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Состав заказа (товары в заказе)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT DEFAULT 0 CHECK (quantity > 0)
);
# Задание 2

 Сумма товаров по каждому клиенту
 SELECT
    c.name AS client_name,
    SUM(p.price * oi.quantity) AS total_amount
FROM
    customers c
JOIN
    orders o ON c.id = o.customer_id
JOIN
    order_items oi ON o.id = oi.order_id
JOIN
    products p ON oi.product_id = p.id
GROUP BY
    c.name;

Количество дочерних элементов первого уровня вложенности для каждой категории

SELECT
    c.parent_id,
    COUNT(*) AS child_count
FROM
    categories c
WHERE
    c.parent_id IS NOT NULL
GROUP BY
    c.parent_id;

Отчет топ-5 самых продаваемых товаров за последний месяц

WITH last_month_orders AS (
    SELECT *
    FROM orders
    WHERE order_date >= NOW() - INTERVAL '1 month'
)
SELECT
    p.name AS product_name,
    cat.name AS top_level_category,
    SUM(oi.quantity) AS sold_quantity
FROM
    last_month_orders lmo
JOIN
    order_items oi ON lmo.id = oi.order_id
JOIN
    products p ON oi.product_id = p.id
LEFT JOIN
    product_categories pc ON p.id = pc.product_id
LEFT JOIN
    categories cat ON pc.category_id = cat.id AND cat.parent_id IS NULL -- выбираем корневые категории
GROUP BY
    p.name, cat.name
ORDER BY
    sold_quantity DESC
LIMIT 5;

    
