import mysql.connector
from mysql.connector import errorcode

def db_connect():
    try:
        cnx = mysql.connector.connect(user='root', password='test_root',
                                host='127.0.0.1',
                                database='academicworld')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
           print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
           print("Database does not exist")
        else:
           print(err)
    else:
        print("Database Connection Successful")
        return cnx

def select(db, query):
    data_cursor = db.cursor()
    sql_query = query
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    return data

def university_dropdown():
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT id, name FROM university order by 2"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    processed_data = [{'label': name, 'value': id} for id, name in data]
    db.close()
    return processed_data

def faculty_dropdown(univ_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "SELECT id, name FROM faculty where university_id = " + str(univ_id) + " order by 2"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    processed_data = [{'label': name, 'value': name} for id, name in data]
    db.close()
    return processed_data

def faculty_count(univ_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "select faculty_count from faculty_count where university_id = " + str(univ_id)
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    processed_data = [faculty_count[0] for faculty_count in data]
    db.close()
    return processed_data

def faculty_table(univ_id):
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "select name, position, email, phone from faculty where university_id = " + str(univ_id) + " order by name"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchall()
    processed_data = [{'Name': row[0], 'Position': row[1], 'Email': row[2], 'Phone': row[3]} for row in data]
    db.close()
    return processed_data

def insert_faculty(name, position, email, phone, univ_affiliation):
    print(str(name) + " - " + str(position) + " - " + str(email) + " - " + str(phone) + " - " + str(univ_affiliation))
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "insert into faculty (id, name, position, email, phone, university_id) values (%s, %s , %s , %s, %s, %s)"
    values = (generate_faculty_id(), name, position, email, phone, univ_affiliation)
    data_cursor.execute(sql_query, values)
    db.commit()
    db.close()

def generate_faculty_id():
    db = db_connect()
    data_cursor = db.cursor()
    sql_query = "select MAX(id) from faculty;"
    data_cursor.execute(sql_query)
    data = data_cursor.fetchone()
    new_id = data[0] if data[0] else 0
    db.close()
    return new_id + 1

 
    
