import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host='localhost',
        database='osfingerprint',
        user='root',
        password='1234'
    )

    # Check the total count of records
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM fingerprints")
    total_count = cursor.fetchone()[0]

    # Define the limit
    limit = 1000000

    # Check if the total count exceeds the limit
    if total_count > limit:
        # Calculate the number of records to delete
        excess_count = total_count - limit

        # Delete the oldest records
        delete_query = f"DELETE FROM fingerprints ORDER BY id LIMIT {excess_count}"
        cursor.execute(delete_query)
        connection.commit()  # Commit the transaction

except Error as error:
    print("Error:", error)

finally:
    # Close the cursor and connection
    # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
