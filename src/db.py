import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="weather_db"
    )


def save_weather_to_db(city, temperature, description):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT IGNORE INTO cities (name) VALUES (%s)", (city,))
    conn.commit()

    cursor.execute("SELECT id FROM cities WHERE name = %s", (city,))
    city_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM weather WHERE city_id = %s", (city_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            """
            UPDATE weather 
            SET temperature = %s, description = %s
            WHERE city_id = %s
        """,
            (temperature, description, city_id),
        )
    else:
        cursor.execute(
            """
            INSERT INTO weather (city_id, temperature, description)
            VALUES (%s, %s, %s)
        """,
            (city_id, temperature, description),
        )

    conn.commit()
    conn.close()


def delete_weather_by_city(city_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM cities WHERE name = %s", (city_name,))
    city = cursor.fetchone()
    if not city:
        print("Город не найден.")
        return

    city_id = city[0]

    cursor.execute("DELETE FROM weather WHERE city_id = %s", (city_id,))
    cursor.execute("DELETE FROM cities WHERE id = %s", (city_id,))
    conn.commit()
    conn.close()
    print(f"Удалены данные о погоде и сам город: {city_name}")


def get_all_weather():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.name, w.temperature, w.description, w.updated_at
        FROM weather w
        JOIN cities c ON w.city_id = c.id
    """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_city_weather(city_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.name, w.temperature, w.description, w.updated_at
        FROM weather w
        JOIN cities c ON w.city_id = c.id
        WHERE c.name = %s
    """,
        (city_name,),
    )
    result = cursor.fetchone()
    conn.close()
    return result
