""" For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
reiser. Denne funksjonaliteten skal programmeres. """

from datetime import date, datetime
import sqlite3

# Kobler til databasen
con = sqlite3.connect("jernbaneDatabase.db")
cursor = con.cursor()

# Hjelpemetoder:

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


# Returnerer avgangstiden for en gitt togrute fra en gitt stasjon
def get_departure_time(routeno, start_station):
    cursor.execute("SELECT avgangstid FROM Togrutetabell WHERE rutenr = ? AND stasjon = ?", (routeno, start_station))
    departure_time = cursor.fetchall()
    if len(departure_time) > 0:
        return departure_time[0][0]
    else:
        return 0


# Legger registrerte e-postadresser i en liste for validering
def get_registered_emails():
    cursor.execute("SELECT epost FROM Kunde")
    rows = cursor.fetchall()
    registered_emails = []
    for row in rows:
        registered_emails.append(row[0])
    return registered_emails


# Henter email fra bruker
print("----------------------------Fremtidige bestillinger----------------------------")
print("")
email = input("Skriv inn e-postadressen din: ").lower()
while email not in get_registered_emails():
    email = input("Skriv inn e-postadressen din: ").lower()

# Finner dagens dato
today_date = date.today()
date_format = today_date.strftime("%Y-%d-%m")
date_format = datetime.strptime(date_format, "%Y-%d-%m")

# Henter brukerens ordre og billetter fra databasen og skriver dem ut
cursor.execute("select ordrenr, dato, tid, forekomstdato, rutenr from (Kunde join Kundeordre using (kundenr)) where epost = ?", (email,))
orders = cursor.fetchall()

print("")
print("Skriver ut dine fremtidige bestillinger: ")
for i in range(len(orders)):
    orderno = orders[i][0]
    order_date = orders[i][1]
    order_time = orders[i][2]
    ticket_date = orders[i][3]
    routeno = orders[i][4]

    # Viser bare billetter med forekomst etter dagens dato
    date_check = datetime.strptime(ticket_date, "%Y-%d-%m")
    if not date_check >= date_format:
        continue

    print("")
    print("----------------------------------------------")
    print("Ordrenr: " + str(orderno))
    print("Bestillingsdato: " + str(order_date))
    print("Bestillingstidspunkt: " + str(order_time)[0:-3])
    print("----------------------------------------------")

    cursor.execute("select * from Billett where ordrenr = ?", (orderno,))
    tickets = cursor.fetchall()
    for j in range(len(tickets)):
        ticketno = tickets[j][0]
        ticket_seat = tickets[j][1]
        ticket_wagon = tickets[j][2]
        wagon_layout = get_wagon_layout(routeno)
        wagon_number = get_wagon_number(ticket_wagon, wagon_layout)
        ticket_start = tickets[j][4]
        ticket_end = tickets[j][5]
        depature_time = get_departure_time(routeno, ticket_start)

        print("Billettnr: " + str(ticketno))
        print("Strekning for reisen: " + str(ticket_start) + " - " + str(ticket_end))
        print("Dato for avreisen: " + str(ticket_date))
        print("Tidspunkt for avreisen: " + str(depature_time)[0:-3])
        print("Vognnr: " + str(wagon_number))
        print("Setenr: " + str(ticket_seat))
        print("----------------------------------------------")

# Lukker database
con.close()