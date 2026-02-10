from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect("dbname=test_aiti_guru user=postgres password=super_secret host=postgres")
cur = conn.cursor()

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    order_id = request.args.get('order_id')
    product_id = request.args.get('product_id')
    quantity = int(request.args.get('quantity'))

    cur.execute(
        """
        SELECT quantity FROM order_items WHERE order_id=%s AND product_id=%s
        """,
        (order_id, product_id)
    )
    existing_item = cur.fetchone()

    if existing_item is not None:
        new_quantity = existing_item[0] + quantity
        cur.execute(
            """
            UPDATE order_items SET quantity=%s WHERE order_id=%s AND product_id=%s
            """,
            (new_quantity, order_id, product_id)
        )
    else:
        cur.execute(
            """
            INSERT INTO order_items(order_id, product_id, quantity) VALUES (%s, %s, %s)
            """,
            (order_id, product_id, quantity)
        )

    conn.commit()
    return jsonify({"message": f"Товар успешно добавлен в заказ {order_id}"})

if __name__ == '__main__':
    app.run(debug=True)