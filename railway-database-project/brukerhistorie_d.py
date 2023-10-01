""" Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
returneres, sortert på tid. Denne funksjonaliteten skal programmeres. """

import sqlite3
import re
import datetime

# Opprett tilkobling til databasen
con = sqlite3.connect("jernbaneDatabase.db")
cursor = con.cursor()

# Henter lagrede jernbanestasjoner (for validering)
cursor.execute("SELECT navn FROM Jernbanestasjon")
rows = cursor.fetchall()
saved_stations = []
for row in rows:
    saved_stations.append(row[0])


# Ber brukeren om å skrive inn startstasjon, endestasjon, dato og tidspunkt, validerer disse, og lagrer dem dersom de er gyldige
def get_user_input():
    start_station = input("Skriv inn en startstasjon: ").lower().title()

    while not start_station in saved_stations:
        print("Den stasjonen finnes ikke!")
        start_station = input("Skriv inn en startstasjon: ").lower().title()

    end_station = input(
        "Skriv inn en endestasjon: ").lower().title()

    while not end_station in saved_stations:
        print("Den stasjonen finnes ikke!")
        end_station = input(
            "Skriv inn en endestasjon: ").lower().title()

    while end_station == start_station:
        print("Endestasjon må være forskjellig fra startstasjon!")
        end_station = input(
            "Skriv inn en endestasjon: ").lower().title()

    datestr = input("Skriv inn en dato på formatet 'YYYY-DD-MM': ")
    while not date_valid(datestr):
        print("Ugyldig dato! Datoen må være på riktig format og i fremtiden (eller i dag)")
        datestr = input("Skriv inn en dato på formatet 'YYYY-DD-MM': ")
    (year, day, month) = datestr.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)

    timestr = input("Skriv inn et klokkelsett på formatet 'HH:MM': ")
    while not time_valid(timestr):
        print("Ugyldig klokkeslett! Klokkeslettet må være på riktig format")
        timestr = input("Skriv inn et klokkelsett på formatet 'HH:MM': ")
    (hours, minutes) = timestr.split(":")
    hours = int(hours)
    minutes = int(minutes)
    time = datetime.time(hours, minutes)

    return (start_station, end_station, date, time)


# Validering for dato
def date_valid(datestr):
    validformat = re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}', datestr)
    if not validformat:
        return False

    (year, day, month) = datestr.split('-')

    year = int(year)
    month = int(month)
    day = int(day)
    if year < 0 or month < 0 or day < 0:
        return False
    elif month > 12 or day > 31:
        return False
    elif day > 30 and month in [4, 6, 9, 11]:
        return False
    elif (day > 29 and month == 2) or (day > 28 and month == 2 and year % 4 != 0):
        return False

    today = datetime.date.today()
    date = datetime.date(year, month, day)

    if date < today:
        return False

    return True


# Validering for tidspunkt
def time_valid(timestr):
    validformat = re.fullmatch('[0-9]{2}:[0-9]{2}', timestr)
    if not validformat:
        return False

    (hours, minutes) = timestr.split(':')

    hours = int(hours)
    minutes = int(minutes)
    if hours < 0 or minutes < 0:
        return False
    elif hours > 23 or minutes > 59:
        return False

    return True


# Returnerer ukedag for datoen brukeren skrev inn, samt neste ukedag
def get_weekdays(date):
    weekday_int = date.weekday()

    match weekday_int:
        case 0:
            curr_weekday = "mandag"
            next_weekday = "tirsdag"
        case 1:
            curr_weekday = "tirsdag"
            next_weekday = "onsdag"
        case 2:
            curr_weekday = "onsdag"
            next_weekday = "torsdag"
        case 3:
            curr_weekday = "torsdag"
            next_weekday = "fredag"
        case 4:
            curr_weekday = "fredag"
            next_weekday = "lørdag"
        case 5:
            curr_weekday = "lørdag"
            next_weekday = "søndag"
        case 6:
            curr_weekday = "søndag"
            next_weekday = "mandag"

    return (curr_weekday, next_weekday)


# Returnerer en oversikt over tidspunkt et tog er innom en stasjon på en gitt ukedag
def get_station_rows(station, weekday):
    cursor.execute("SELECT * FROM Togrutetabell WHERE stasjon = ? AND (rutenr IN (SELECT rutenr From Driftsdager WHERE ukedag = ?))",
                   (station, weekday))
    return cursor.fetchall()


# Henter ut ruter som går fra startstasjonen til endestasjonen på brukerens gitte ukedag
def get_valid_routes(start_station_rows, end_station_rows):
    valid_routes = []
    for start_station_row in start_station_rows:
        start_station_routeno = start_station_row[0]
        start_station_stationno = start_station_row[4]

        for end_station_row in end_station_rows:
            end_station_routeno = end_station_row[0]
            end_station_stationno = end_station_row[4]

            if (start_station_routeno == end_station_routeno) and (start_station_stationno < end_station_stationno):
                start_departing_time = start_station_row[3]
                if start_departing_time is not None:
                    start_departing_times = start_departing_time.split(":")
                    start_departing_hours = int(start_departing_times[0])
                    start_departing_minutes = int(start_departing_times[1])
                    start_departing_time = datetime.time(
                        start_departing_hours, start_departing_minutes)
                    valid_routes.append(
                        (start_station_routeno, start_departing_time))
    sorted_valid_routes = sorted(valid_routes, key=lambda x: x[1])

    return sorted_valid_routes


def main():
    print("------------------------------------------------Finn togruter-------------------------------------------------")
    print("")

    print("Tilgjengelige stasjoner:")
    for station in saved_stations:
        print(station)
    print("")

    (start_station, end_station, date, time) = get_user_input()
    (curr_weekday, next_weekday) = get_weekdays(date)

    timestr = time.strftime("%H:%M")

    start_station_rows_current = get_station_rows(
        start_station, curr_weekday)
    end_station_rows_current = get_station_rows(
        end_station, curr_weekday)
    start_station_rows_next = get_station_rows(
        start_station, next_weekday)
    end_station_rows_next = get_station_rows(
        end_station, next_weekday)

    valid_routes_current = get_valid_routes(start_station_rows_current, end_station_rows_current)
    valid_routes_next = get_valid_routes(start_station_rows_next, end_station_rows_next)


    print("")
    if len(valid_routes_current) > 0 or len(valid_routes_next) > 0:
        print(
            f"Disse rutene går fra {start_station} til {end_station} fra klokka {timestr} på {curr_weekday} eller {next_weekday}:")
        for route in valid_routes_current:
            if (route[1] >= time):
                routeno = route[0]
                timestamp_formatted = route[1].strftime("%H:%M")
                print(
                    f"Rutenr: {routeno}, Tidspunkt: {timestamp_formatted}, Ukedag: {curr_weekday}")
        for route in valid_routes_next:
            routeno = route[0]
            timestamp_formatted = route[1].strftime("%H:%M")
            print(
                f"Rutenr: {routeno}, Tidspunkt: {timestamp_formatted}, Ukedag: {next_weekday}")
    else:
        print(
            f"Det går dessverre ingen ruter fra {start_station} til {end_station} fra klokka {timestr} på {curr_weekday} eller {next_weekday}")
    print("")
    print("--------------------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()

# Lukker tilkobling til databasen
con.close()
