import pymysql.cursors

client = pymysql.connect("localhost", "public", "password123", "KidOYO")
try:
    # SELECTING ALL ITEMS TO DISPLAY
    cursor = client.cursor()
    query = "DELETE FROM Person WHERE ID = %s"
    cursor.execute(query, 'Tommy')
    query = "INSERT INTO Person(ID, Gender) values (%s, %s)"
    cursor.execute(query, ('Riya', 'F'))

    client.commit()
except Exception:
    print("Can not retrieve specified Entity")
    client.rollback()
finally:
    client.close()
