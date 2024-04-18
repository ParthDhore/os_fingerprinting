import mysql.connector
from mysql.connector import Error

def insert_packet_data(packet_data, os_name):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            database='osfingerprint',
            user='root',
            password='1234'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Define your insert query
            sql = "insert into fingerprints (ip_ttl, ip_totlen, t_mss, t_wsize, t_wscale, ip_flags_df, ip_dsfield, emb1, emb2, emb3, emb4, emb5, emb6, emb7, emb8, emb9, emb10, emb11, emb12, emb13, emb14, emb15, emb16, emb17, emb18, emb19, emb20, emb21, emb22, emb23, emb24, emb25, emb26, emb27, emb28, emb29, emb30, emb31, emb32, emb33, emb34, emb35, emb36, emb37, emb38, emb39, emb40, emb41, emb42, emb43, emb44, emb45, emb46, emb47, emb48, emb49, os) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            # Execute the INSERT statement with the values from the NumPy array
            temp_list=packet_data.tolist()
            temp_list.append(os_name)
            cursor.execute(sql, tuple(temp_list))

            # Commit the transaction to save changes to the database
            connection.commit()

            # print("All data inserted successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")



# columns=["ip_ttl", "ip_totlen", "t_mss", "t_wsize", "t_wscale", "ip_flags_df", "ip_dsfield", "('?', '?')", "('?', 'eol')", "('?', 'mss')",
#        "('?', 'nop')", "('?', 'sok')", "('?', 'ts')", "('?', 'ws')",
#        "('eol', '?')", "('eol', 'eol')", "('eol', 'mss')", "('eol', 'nop')",
#        "('eol', 'sok')", "('eol', 'ts')", "('eol', 'ws')", "('mss', '?')",
#        "('mss', 'eol')", "('mss', 'mss')", "('mss', 'nop')", "('mss', 'sok')",
#        "('mss', 'ts')", "('mss', 'ws')", "('nop', '?')", "('nop', 'eol')",
#        "('nop', 'mss')", "('nop', 'nop')", "('nop', 'sok')", "('nop', 'ts')",
#        "('nop', 'ws')", "('sok', '?')", "('sok', 'eol')", "('sok', 'mss')",
#        "('sok', 'nop')", "('sok', 'sok')", "('sok', 'ts')", "('sok', 'ws')",
#        "('ts', '?')", "('ts', 'eol')", "('ts', 'mss')", "('ts', 'nop')",
#        "('ts', 'sok')", "('ts', 'ts')", "('ts', 'ws')", "('ws', '?')",
#        "('ws', 'eol')", "('ws', 'mss')", "('ws', 'nop')", "('ws', 'sok')",
#        "('ws', 'ts')", "('ws', 'ws')"]