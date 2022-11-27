import mysql.connector 
from mysql.connector import errorcode
config = {
    "user": "movies_user",
    "password":"popcorn",
    "host":"127.0.0.1",
    "database":"movies",
    "raise_on_warnings":True
}

try:
    db = mysql.connector.connect(**config)

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()
    query = "SELECT * from studio"
    cursor.execute(query)
    results = cursor.fetchall()
    print(" -- DISPLAYING Studio Records --")

    for studio in results:
        print("Studio ID:", studio[0])
        print("Studio Name: ", studio[1])
        print(" ")

    query = "SELECT * from genre"
    cursor.execute(query)
    results = cursor.fetchall()
    print(" -- DISPLAYING Genre Records --")

    for genre in results:
        print("Genre ID:", genre[0])
        print("Genre Name: ", genre[1])
        print(" ")

    query = "SELECT film_name, film_runtime from film where film_runtime <120"
    cursor.execute(query)
    results = cursor.fetchall()
    print(" -- DISPLAYING Short film Records --")

    for film in results:
        print("Film Name:", film[0])
        print("Runtime: ", film[1])
        print(" ")

    query = "SELECT film_name, film_director from film order by film_director"
    cursor.execute(query)
    results = cursor.fetchall()
    print(" -- DISPLAYING Director RECORDS in Order by --")

    for director in results:
        print("Film name:", director[0])
        print("Director Name: ", director[1])
        print(" ")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)
    
finally:
    db.close()