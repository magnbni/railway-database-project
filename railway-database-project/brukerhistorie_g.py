""" Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute
og kjøpe de billettene hen ønsker. Denne funksjonaliteten skal programmeres.
• Pass på at dere bare selger ledige plasser """

import sqlite3
import datetime
import brukerhistorie_d

# Opprett tilkobling til databasen
con = sqlite3.connect("jernbaneDatabase.db")
cursor = con.cursor()

# Henter lagrede jernbanestasjoner (for validering)
cursor.execute("SELECT navn FROM Jernbanestasjon")
rows = cursor.fetchall()
saved_stations = []
for row in rows:
    saved_stations.append(row[0])


# Henter inn brukerens kundenr vha. e-postadressen som en slags primitiv form for innlogging
def get_customerno():
    # Henter registrerte e-postadresser
    cursor.execute("SELECT epost FROM Kunde")
    saved_emails = [email[0] for email in cursor.fetchall()]
    if not len(saved_emails) == 0: 
        # Henter inn e-postadresse fra bruker
        print("")
        email = input("Skriv inn e-posten din: ").lower()
        while not email in saved_emails:
            print("Den e-postadressen finnes ikke i registeret!")
            email = input("Skriv inn e-posten din: ").lower()

        # Finner kundenummer til bruker gitt email
        cursor.execute("SELECT kundenr FROM Kunde WHERE epost = ?", (email,))
        customerno = cursor.fetchall()[0][0]
        return customerno
    else:
        return 0


# Henter inn start- og endestasjon fra brukerinput, og sjekker at de er gyldige
def get_stations():
    print("")
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

    return (start_station, end_station)


# Henter alle togrutenummer
def get_all_routenos():
    cursor.execute("SELECT rutenr FROM Togrute")
    route_numbers = cursor.fetchall()
    return route_numbers


# Liste for togruter med oppgitt strekning
def get_train_routes(route_numbers, start_station, end_station):
    train_routes = []

    # Itererer gjennom alle togruter
    for i in range(len(route_numbers)):
        # Henter alle stasjoner på ruten, samt deres stasjonsnr
        cursor.execute("SELECT stasjon, stasjonsnr FROM Togrutetabell WHERE rutenr = ?",
                    (str(route_numbers[i][0]),))
        stationQuery = cursor.fetchall()

        stations_dict = {}

        # Lager map mellom stasjoner og deres stasjonnr
        for row in stationQuery:
            stations_dict[row[0]] = row[1]

        # Sjekker om start- og endestasjonen er i togruten
        if ((start_station in stations_dict.keys()) and (end_station in stations_dict.keys())):
            # Sjekker at endestasjon kommer etter startstasjon
            if stations_dict[end_station] > stations_dict[start_station]:
                train_routes.append(route_numbers[i][0])
    return train_routes


# Spør brukeren om å velge en togrute fra en liste med mulig togruter
def get_train_route_input(train_routes, available_routes):
    # Skriver ut hvilke togruter bruker kan velge mellom
    print("")
    print("Mulige togruter for strekning: ")
    for k in range(available_routes):
        print("Togrute nr. " + str(train_routes[k]))

    # Henter ønsket togrutenummer fra bruker
    routeno = input("Velg én togrute: ")
    while not routeno in [str(train_route) for train_route in train_routes]:
        routeno = input(
            "Velg én togrute: ")
    print("Du har valgt togrute " + str(routeno))
    return routeno


def get_chosen_date(routeno):
    # Henter datoer for forekomster på den oppgitte togruta
    valid_dates = []
    cursor.execute(
        "SELECT dato FROM Togruteforekomst WHERE rutenr = ?", (routeno,))
    avaliable_dates = cursor.fetchall()
    # Hvis det ikke finnes noen forekomster, informer bruker
    if (len(avaliable_dates) == 0):
        print("Det er dessverre ingen registrerte forekomster av den oppgitte togruten for øyeblikket. Prøv igjen senere.")
        return None
    else:
        date_today = datetime.date.today()
        for i in range(len(avaliable_dates)):
            date_element = str(avaliable_dates[i][0])
            year, day, month = date_element.split("-")
            date = datetime.date(int(year), int(month), int(day))
            if (date >= date_today):
                valid_dates.append(date.strftime("%Y-%d-%m"))

    # Hent ønsket dato fra bruker og sjekk at den er gyldig
    print("")
    print("Gyldige datoer for reisen:", end=" ")
    for valid_date in valid_dates:
        print(valid_date, end="")
        if (valid_dates.index(valid_date) != len(valid_dates) - 1):
            print(",", end=" ")
        else:
            print("")

    chosen_datestr = input(
        "Skriv inn datoen du vil reise på formatet 'YYYY-DD-MM': ")
    while not brukerhistorie_d.date_valid(chosen_datestr):
        print("Datoen du skrev inn er ikke gyldig!")
        chosen_datestr = input(
            "Skriv inn datoen du vil reise på formatet 'YYYY-DD-MM': ")

    while chosen_datestr not in valid_dates:
        print("Det går ingen forekomster av togruten du valgte på den datoen!")
        chosen_datestr = input(
            "Skriv inn datoen du vil reise på formatet 'YYYY-DD-MM': ")

    # Konverterer den valgte forekomstdatoen til gyldig format for databasen
    year, day, month = chosen_datestr.split("-")
    chosen_date = datetime.date(int(year), int(month), int(day))
    return chosen_date


# Henter mulige vogner for togruten
def get_all_wagons(routeno):
    cursor.execute(
        "SELECT vognID FROM Togrute JOIN VognIOppsett USING (oppsettID) JOIN Vogn USING (vognID) WHERE rutenr = ?", (routeno,))
    wagons = cursor.fetchall()
    return [wagon[0] for wagon in wagons]


def get_available_spots_in_wagons(wagons, chosen_date, routeno, start_station, end_station):
    layout_ID = get_wagon_layout(routeno)
    sub_routes_for_journey = get_sub_routes_for_stretch(start_station, end_station, routeno)

    cursor.execute("""SELECT Billett.vognID, plassnr, startstasjon, endestasjon FROM Billett JOIN Kundeordre USING (ordrenr) JOIN VognIOppsett USING (vognID) 
                        WHERE forekomstDato = ? AND oppsettID = ?
                        ORDER BY Billett.vognID""",
                        (chosen_date.strftime("%Y-%d-%m"), layout_ID))
    rows = cursor.fetchall()

    wagon_unavailable_spots_dict = {}
    for wagon in wagons:
        wagon_unavailable_spots_dict[wagon] = set()
    
    for row in rows:
        wagon = row[0]
        type = get_wagon_type(wagon)
        spot = row[1]
        ticket_start_station = row[2]
        ticket_end_station = row[3]

        sub_routes_on_ticket = get_sub_routes_for_stretch(ticket_start_station, ticket_end_station, routeno)
        unavailable_spots = set()
        for sub_route in sub_routes_for_journey:
            if sub_route in sub_routes_on_ticket:
                if (type == 'Sovevogn'):
                    compartments, beds_per_compartment = get_sleeping_wagon_arrangement(wagon)
                    position_in_compartment = spot % beds_per_compartment
                    # Modulo-aritmetikk gir at vognen på "siste plass i kupeen" er lik 0, vi vil ha den lik antallet senger i stedet
                    if position_in_compartment == 0:
                        position_in_compartment = beds_per_compartment
                    diff_top = beds_per_compartment - position_in_compartment
                    diff_bottom = position_in_compartment - 1
                    for i in range(1, diff_top + 1):
                        unavailable_spots.add(spot + i)
                    for j in range(1, diff_bottom + 1):
                        unavailable_spots.add(spot - j)
                unavailable_spots.add(spot)
                break
        wagon_unavailable_spots_dict[wagon].update(unavailable_spots)

    wagon_available_spots_dict = {}
    for wagon in wagons:
        cursor.execute(
                "SELECT plassnr FROM Plass WHERE vognID = ?", (wagon,))
        spots = {spot[0] for spot in cursor.fetchall()}
        available_spots = list(spots - wagon_unavailable_spots_dict[wagon])
        available_spots.sort()
        wagon_available_spots_dict[wagon] = available_spots
    return wagon_available_spots_dict

    
    # Liten forklaring for hva vi har tenkt her:
    # Vi ønsker å bare vise vogner som har ledige plasser på hele ruten brukeren har valgt. 
    # Vi henter derfor inn alle billettene som er bestilt på brukerens valgte dato. 
    # Deretter sjekker vi for hver mulige plass i hver vogn, om denne plassen er utilgengelig på noen av delstrekningene. Dersom den er det,
    # legg den til i en mengde med utilgjengelige plasser. For sovevogner står det spesifisert i oppgaven at en ikke skal kunne booke en seng i en kupé
    # der noen andre allerede har booket en seng, derfor legges alle sengene i en sovekupé til i listen over utilgjengelige plasser dersom en av dem er booket.
    # De plassene som er tilgjengelige under hele ruten i en vogn er da differansen mellom mengden 
    # av alle mulige plasser i denne vognen og de plassene som er opptatt på minst én delstrekning i vognen. 


# Ber brukeren om å velge tilgjengelige vogner og plasser og lagrer disse i en dictionary
def get_chosen_wagons_and_spots(wagon_available_spots_dict, routeno):
    # Finner gyldige IDer for vognene i ruten

    print("")
    if len(wagon_available_spots_dict.keys()) == 0:
        print("Denne togruten er dessverre utsolgt")
        return None
    
    wagon_number_to_id_dict = {}
    for wagon_id in wagon_available_spots_dict.keys():
        wagon_number = get_wagon_number(wagon_id, get_wagon_layout(routeno));
        wagon_number_to_id_dict[wagon_number] = wagon_id

    valid_numbers = []
    print("Tilgjengelige vogner på ruten:")
    for wagon_id in wagon_available_spots_dict.keys():
        wagon_number = get_wagon_number(wagon_id, get_wagon_layout(routeno))
        valid_numbers.append(wagon_number)
        print(f"Nummer: {wagon_number}, Type: {get_wagon_type(wagon_id)}")

    print("")
    # Spør bruker om å oppgi én vogn til billettbestilling
    print("Velg vognene du ønsker å kjøpe plasser i. For å velge en vogn, skriv vognnummeret i innskrivings-feltet og trykk 'Enter'.")
    print("Dersom du ikke ønsker å velge flere vogner, skriv 'Stopp' i innskrivings-feltet.")
    chosen_wagons = []
    chosen_number = ""

    wagon_chosen_spots_dict = {}

    finish = False
    while not finish:
        chosen_number = input("Skriv inn vognnummer: ")
        if (chosen_number.lower() == "stopp"):
            finish = True
            break
        while chosen_number not in [str(number) for number in valid_numbers]:
            print("Ugyldig vognnummer!")
            chosen_number = input("Skriv inn vognnummer: ")
            if (chosen_number.lower() == "stopp"):
                finish = True
                break
        if finish:
            break
        if int(chosen_number) not in chosen_wagons:
            print("Du har valgt vogn med nummer " + chosen_number)
            chosen_wagons.append(int(chosen_number))
            wagon_chosen_spots_dict[wagon_number_to_id_dict[int(chosen_number)]] = []
        else:
            print("Du har allerede valgt den vognen!")

    for wagon_number in chosen_wagons:
        wagon_id = wagon_number_to_id_dict[wagon_number]
        spots = wagon_available_spots_dict[wagon_id]

        valid_spots = []
        print("")
        print("Tilgjengelige plasser i vognen:", end=" ")
        for spot in spots:
            valid_spots.append(spot)
            print(spot, end="")
            if (spots.index(spot) != len(spots) - 1):
                print(",", end=" ")

        print("")
        print("Velg plassene du ønsker å kjøpe billetter for. For å velge en plass, skriv plassnummeret i innskrivings-feltet og trykk 'Enter'.")
        print(
            "Dersom du ikke ønsker å velge flere plasser, skriv 'Stopp' i innskrivings-feltet.")
        chosen_spots = []
        chosen_spot = ""

        finish = False
        while not finish:
            chosen_spot = input(
                f"Skriv inn plassnummer for vogn med nummer {wagon_number}: ")
            if (chosen_spot.lower() == "stopp"):
                finish = True
                break
            while chosen_spot not in [str(spot) for spot in valid_spots]:
                print("Ugyldig plassnummer!")
                chosen_spot = input(
                    f"Skriv inn plassnummer for vogn med nummer {wagon_number}: ")
                if (chosen_spot.lower() == "stopp"):
                    finish = True
                    break
            if finish:
                break
            if int(chosen_spot) not in chosen_spots:
                print(
                    f"Du har valgt plass med nummer {chosen_spot} i vogn med nummer {wagon_number}")
                chosen_spots.append(int(chosen_spot))
                wagon_chosen_spots_dict[wagon_id].append(int(chosen_spot))
            else:
                print("Du har allerede valgt den plassen!")

    chosen = False
    if len(wagon_chosen_spots_dict) > 0:
        for wagon in wagon_chosen_spots_dict.keys():
            if len(wagon_chosen_spots_dict[wagon]) > 0:
                chosen = True

    if not chosen:
        print("")
        print("Du har ikke valgt noen vogner eller plasser, bestillingen avbrytes")
        return None

    return wagon_chosen_spots_dict


# Regner ut antall billetter
def get_ticket_count(wagon_spot_dict):
    ticket_count = 0
    for key in wagon_spot_dict.keys():
        for value in wagon_spot_dict[key]:
            ticket_count += 1
    return ticket_count


# Registrerer en ny kundeordre for bestillingen
def place_order(customerno, ticket_count, chosen_date, routeno):
    orderno = get_next_orderno()
    cursor.execute("""INSERT INTO Kundeordre (ordrenr, dato, tid, antall, kundenr, forekomstDato, rutenr) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (orderno, datetime.date.today().strftime("%Y-%d-%m"), datetime.datetime.now().strftime("%H:%M:%S"), ticket_count, customerno, chosen_date.strftime("%Y-%d-%m"), routeno))
    con.commit()
    return orderno


# Oppretter en billett for hver valgte plass i de valgte vognene for strekningen
def create_tickets(orderno, wagon_chosen_spots_dict, start_station, end_station):
    for wagon in wagon_chosen_spots_dict.keys():
        for spot in wagon_chosen_spots_dict[wagon]:
            cursor.execute("""INSERT INTO Billett (billettnr, plassnr, vognID, ordrenr, startstasjon, endestasjon) 
                VALUES (?, ?, ?, ?, ?, ?)""", (get_next_ticketno(), spot, wagon, orderno, start_station, end_station))
    con.commit()


# Hjelpemetoder:

# Henter delstrekninger på en strekning mellom start- og endestasjon på en gitt rute
def get_sub_routes_for_stretch(start_station, end_station, routeno):
    cursor.execute("SELECT * FROM Togrutetabell WHERE rutenr = ?", (routeno,))
    stationQuery = cursor.fetchall()
    stations_in_between = []
    stations = []
    stationno = []
    stations_dict = {}

    for row in stationQuery:
        stations.append(row[1])
        stationno.append(row[4])

    stations_dict = {stations[j]: stationno[j]
                    for j in range(len(stations))}
    
    # Sjekker om start- og endestasjonen er i togruten
    if ((start_station in stations) and (end_station in stations)):
        # Sjekker at endestasjon kommer etter startstasjon
        if stations_dict[end_station] > stations_dict[start_station]:

            # Hvis det finnes mellomstasjoner på strekningen, legg dem til i en egen liste
            for station in stations:
                if ((stations_dict[station] > stations_dict[start_station]) and (stations_dict[station] < stations_dict[end_station])):
                    stations_in_between.append(station)

    if (is_main_direction(routeno)):
        stations_in_between.reverse()
    between_length = len(stations_in_between)

    # Legger til alle delstrekninger på valgt strekning i en liste
    sub_routes = []
    if between_length != 0:
        sub_routes.append((start_station, stations_in_between[0]))
        for i in range(1, between_length):
            if (between_length > 1):
                sub_routes.append(
                    (stations_in_between[i-1], stations_in_between[i]))
        sub_routes.append(
            (stations_in_between[between_length-1], end_station))
    else:
        sub_routes.append((start_station, end_station))

    return sub_routes


# Returnerer True dersom ruten kjører hovedretningen til banestrekningen, ellers False
def is_main_direction(routeno):
    cursor.execute(
        "SELECT DISTINCT kjørerHovedretning FROM DelstrekningPåRute WHERE rutenr = ?", (routeno,))
    rows = cursor.fetchall()
    main_direction = rows[0][0]
    if (main_direction == "true"):
        return True
    return False


# Henter neste billettnr ved å sjekke billettnr som sist ble lagret i databasen og legg til 1
def get_next_ticketno():
    cursor.execute("SELECT billettnr FROM Billett")
    rows = cursor.fetchall()

    max_ticketno = 0
    for row in rows:
        if row[0] > max_ticketno:
            max_ticketno = row[0]
    return max_ticketno + 1


# Henter neste ordrenr ved å sjekke ordrenr som sist ble lagret i databasen og legg til 1
def get_next_orderno():
    cursor.execute("SELECT ordrenr FROM Kundeordre")
    rows = cursor.fetchall()

    max_orderno = 0
    for row in rows:
        if row[0] > max_orderno:
            max_orderno = row[0]
    return max_orderno + 1


# Returnerer en tuppel som inneholder antall sovekupeer og antall senger per kupé
def get_sleeping_wagon_arrangement(wagon_id):
    cursor.execute("SELECT antallSoveKupeer, sengerPrKupe FROM Sovevogn WHERE vognID = ?", (wagon_id,))
    arrangement = cursor.fetchall()[0]
    return arrangement


# Henter oppsettID-en til en oppgitt rute
def get_wagon_layout(routeno):
    cursor.execute("SELECT oppsettID FROM Togrute WHERE rutenr = ?", (routeno,))
    wagon_layout = cursor.fetchall()[0][0]
    return wagon_layout


# Returnerer vognnummeret en vogn med en gitt ID har i et gitt vognoppsett
def get_wagon_number(wagon_id, layout_id):
    cursor.execute("SELECT nummer FROM VognIOppsett WHERE vognID = ? AND oppsettID = ?", (wagon_id, layout_id))
    wagon_number = cursor.fetchall()
    if len(wagon_number) > 0:
        return wagon_number[0][0]
    else:
        return 0


# Henter ut vogntypen til vogn-iden som tas som argument
def get_wagon_type(wagon_id):
    cursor.execute("SELECT type FROM Vogn WHERE vognID = ?", (wagon_id,))
    wagon_type = cursor.fetchall()[0][0]
    return wagon_type


def main():
    print("----------------------------------------------------------Bestill togreise----------------------------------------------------------")

    customerno = get_customerno()
    if customerno != 0:
        print("")
        print("Tilgjengelige stasjoner:")
        for station in saved_stations:
            print(station)

        start_station, end_station = get_stations()
        route_numbers = get_all_routenos()

        train_routes = get_train_routes(route_numbers, start_station, end_station)
        
        # Hvis ingen togruter inneholder oppgitt strekning, informer bruker
        available_routes = len(train_routes)
        if (available_routes == 0):
            print("Det finnes ingen registrert togrute for strekning " +
                start_station + " til " + end_station + "!")
        else:
            routeno = get_train_route_input(train_routes, available_routes)

            chosen_date = get_chosen_date(routeno)
            if chosen_date is not None:
                wagons = get_all_wagons(routeno)
                wagon_available_spots_dict = get_available_spots_in_wagons(
                    wagons, chosen_date, routeno, start_station, end_station)
                wagon_chosen_spots_dict = get_chosen_wagons_and_spots(wagon_available_spots_dict, routeno)
                if wagon_chosen_spots_dict is not None:
                    ticket_count = get_ticket_count(wagon_chosen_spots_dict)
                    orderno = place_order(customerno, ticket_count, chosen_date, routeno)
                    create_tickets(orderno, wagon_chosen_spots_dict, start_station, end_station)

                    print("")
                    print("Din bestilling er nå lagt inn. God tur!")
    else:
        print("Det finnes ingen brukere i registeret!")
        print("Vennligst opprett en bruker for å bestille en togreise")

    print("")
    print("------------------------------------------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()

# Lukker tilkobling til databasen
con.close()
