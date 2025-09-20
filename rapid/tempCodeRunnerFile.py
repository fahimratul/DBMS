    cursor.execute("SELECT item_id, name FROM item;")
    all_items = cursor.fetchall()  or []