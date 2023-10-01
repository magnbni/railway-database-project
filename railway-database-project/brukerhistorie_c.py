""" For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
Denne funksjonaliteten skal programmeres. """

import sqlite3

# Oppretter tilkobling til databasen
con = sqlite3.connect("jernbaneDatabase.db")
cursor = con.cursor()

# Lager en variabel for å sjekke om programmet er ferdig
success = 0

print("-----------------------------------Togruter-----------------------------------")
print("")

# Henter lagrede jernbanestasjoner
cursor.execute("SELECT navn FROM Jernbanestasjon")
rows = cursor.fetchall()
saved_stations = []
for row in rows:
    saved_stations.append(row[0])

# Skriver ut tilgjengelige stasjoner
print("Tilgjengelige stasjoner:")
for station in saved_stations:
    print(station)
print("")

# Løkke som kjører fram til begge brukerinputene er validert og returnerer utskriften
while success == 0:
    station = input("Velg stasjon: ").lower().title()
    weekday = input("Velg ukedag: ").lower()

    # Oversikt over gyldige ukedager
    valid_weekdays = ["mandag", "tirsdag", "onsdag",
                      "torsdag", "fredag", "lørdag", "søndag"]

    cursor.execute(
        "select rutenr, ankomsttid, avgangstid from Togrutetabell join Driftsdager using (rutenr) where stasjon = ? and ukedag = ?", (station, weekday))

    rows = cursor.fetchall()

    print("")

    success = 0

    # Sjekker om ukedagen er gyldig og om stasjonen er i databasen
    if weekday in valid_weekdays:
        if rows != []:
            print("Disse resultatene ble funnet for " +
                  station + " på " + weekday + ":")
            for i in range(len(rows)):
                arrival = rows[i][1]
                departure = rows[i][2]
                if arrival is None:
                    arrival = "-- -- --"
                if departure is None:
                     departure = "-- -- --"
                print("Rutenr: " + str(rows[i][0]), end=", ")
                print("Ankomsttid: " + str(arrival)[0:-3], end=", ")
                print("Avgangstid: " + str(departure)[0:-3])
            success = 1
        else:
            print("Stasjon eksisterer ikke! Vennligst prøv igjen")
    else:
        print("Ukedag er ikke gyldig! Vennligst prøv igjen")

# Lukker databasen
con.close()
print("")
print("------------------------------------------------------------------------------")