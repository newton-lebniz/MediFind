import mysql.connector

def get_connection():
    return mysql.connector.connect( 
        host="localhost",
        user="root",
        password="Bhargav@2008",
        database="medifind"
    )
def get_doctors_by_specialization(specialization):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
   SELECT d.*
    FROM doctors d
    JOIN specializations s ON d.specialization_id = s.specialization_id
    WHERE LOWER(s.specialization_name) = LOWER(%s)
    ORDER BY d.rating DESC
    LIMIT 5
   
    """

    cursor.execute(query, (specialization,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
