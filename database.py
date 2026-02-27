import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="travel_agency"
    )

# 🔹 récupérer ville d'arrivée
def get_city_from_vol(vol_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT arrivee FROM vols WHERE id = %s", (vol_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None


# 🔹 récupérer suggestions existantes
def get_suggestions_from_db(city, type_lieu):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nom, description, type, ville
        FROM suggestions
        WHERE ville = %s AND type = %s
    """, (city, type_lieu))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


# 🔹 insérer suggestion
def insert_suggestion(description, nom, type_lieu, ville):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suggestions (description, nom, type, ville)
        VALUES (%s, %s, %s, %s)
    """, (description, nom, type_lieu, ville))

    conn.commit()
    cursor.close()
    conn.close()
