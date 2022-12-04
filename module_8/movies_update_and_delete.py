#Bethany Mehring
#CSD310
#Assignment 8.2
#11/27/2022
import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)

    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))
    cursor = db.cursor()


    def show_films(cursor, title):
        cursor.execute(
            "SELECT film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio "
            "Name' from film INNER JOIN genre ON film.genre_id = genre.genre_id INNER JOIN studio ON "
            "film.studio_id = studio.studio_id ")

        films = cursor.fetchall()

        print("\n  -- {} --".format(title))
        for film in films:
            print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2]
                                                                                             , film[3]))


    show_films(cursor, "DISPLAYING FILMS")
    print()
    cursor.execute("INSERT INTO film ( film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)"
                   "Values ('Back to the Future','1985','116','Robert Zemeckis',3, 2)")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
    print()

    cursor.execute("UPDATE film "
                   "SET genre_id = 1 "
                   "WHERE film_name = 'Alien'")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")
    print()

    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
    print()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    db.close()
