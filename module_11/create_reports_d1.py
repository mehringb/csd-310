from datetime import datetime, date

import mysql.connector
from Tools.scripts.pathfix import err
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "**********",
    "host": "127.0.0.1",
    "database": "outland_adventures",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                      config["database"]))

    cursor = db.cursor()
    d1Query = "select customer_id, count(purchase_id), sum(purchase_amt) as Amount, purchase_date " \
              "from purchases " \
              "group by customer_id, purchase_date order by customer_id"
    cursor.execute(d1Query)
    d1Results = cursor.fetchall()
    now = datetime.now()
    print(" -- DISPLAYING Purchases --")
    print("\n Time of report: ", now)

    for purchases in d1Results:
        print("\nCustomer ID:", purchases[0])
        print("Purchase ID:", purchases[1])
        print("Purchase Amount:", purchases[2])
        print("Purchase Date:", purchases[3])

    cursor = db.cursor()
    d2Query = (
        "SELECT COUNT(trips.trip_id), continent_name FROM orders "
        "INNER JOIN trips ON orders.trip_id = trips.trip_id "
        "INNER JOIN destination ON trips.continent_ID = destination.continent_ID "
        "WHERE order_date > DATE_SUB(curdate(), INTERVAL 90 DAY) GROUP BY continent_name "
        "ORDER BY COUNT(continent_name)")

    cursor.execute(d2Query)
    d2Results = cursor.fetchall()
    print()
    print("Report created on " + str(date.today()))
    print()
    print(" -- DISPLAYING Bookings by Continent (Past 90 Days) --")
    print()

    for booking_group in d2Results:
        print("Number of Bookings:", booking_group[0])
        print("Continent:", booking_group[1])
        print()

    d3Query = "SELECT equipment_id, equipment_name, acquisition_date " \
              "FROM equipment " \
              "WHERE acquisition_date < date_sub(curdate(), interval 5 year);"
    cursor.execute(d3Query)
    d3Results = cursor.fetchall()
    print(" -- DISPLAYING Equipments older than 5 years --")
    print("Report created on " + str(date.today()))

    for equipment in d3Results:
        print("\nEquipment ID:", equipment[0])
        print("Equipment Name:", equipment[1])
        print("Acquisition Date:", equipment[2])

    input("Press any key to close")

except mysql.connector as Error:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password is invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The supplied database does not exist")

    else:
        print(err)

finally:
    db.close()
