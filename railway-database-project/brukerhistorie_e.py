""" En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres. """

import sqlite3
import re


# Opprett tilkobling til databasen
con = sqlite3.connect("jernbaneDatabase.db")
cursor = con.cursor()


# Skript for å spørre brukeren om nødvendig informasjon
def get_user_info():
    name = input("Skriv inn fornavnet ditt: ").capitalize()
    # Sjekker at navnet består av bare bokstaver og er 2-30 tegn, og gir brukeren et nytt forsøk dersom det ikke er det
    while not re.fullmatch('[A-Za-z]{2,30}', name):
        print("Ugyldig navn! Navnet må bestå av bokstaver og være 2-30 tegn langt")
        name = input("Skriv inn fornavnet ditt: ").capitalize()
    # Gjør forbokstaven i navnet stor

    email = input("Skriv inn e-postadressen din: ").lower()
    # Sjekker at e-posten er på gyldig format, og gir brukeren et nytt forsøk dersom det ikke er det
    while not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        print("Ugyldig e-postadresse!")
        email = input("Skriv inn e-postadressen din: ").lower()
    
    while email in get_registered_emails():
        print("Den e-postadressen er allerede registrert!")
        email = input("Skriv inn e-postadressen din: ").lower()

    phoneno = input("Skriv inn mobilnummeret ditt (uten landskode): ")
    # Sjekker at nummeret er et gyldig norsk telefonnummer, og gir brukeren et nytt forsøk dersom det ikke er det
    while not re.fullmatch('[49]{1}[0-9]{7}', phoneno):
        print("Ugyldig mobilnummer! Nummeret må være et gyldig norsk telefonnummer (begynner med 4 eller 9)")
        phoneno = input(
            "Skriv inn mobilnummeret ditt (uten landskode): ")
    return (name, email, phoneno)


# Henter neste kundenr ved å sjekke kundenr som sist ble lagret i databasen
def get_next_customerno():
    cursor.execute("SELECT kundenr FROM Kunde")
    rows = cursor.fetchall()

    max_customerno = 0
    for row in rows:
        if row[0] > max_customerno:
            max_customerno = row[0]
    return max_customerno + 1

def get_registered_emails():
    cursor.execute("SELECT epost FROM Kunde")
    rows = cursor.fetchall()
    
    registered_emails = []
    for row in rows:
        registered_emails.append(row[0])
    return registered_emails


# Kjører SQL-skript for å sette inn verdiene i databasen
def insert_values(customerno, name, email, phoneno):
    insert = """INSERT INTO Kunde (kundenr, navn, epost, telefonnr) 
            VALUES (?, ?, ?, ?)"""
    data_tuple = (customerno, name, email, phoneno)
    cursor.execute(insert, data_tuple)

    con.commit()


def main():
    print("----------------------------Registrer ny bruker----------------------------")
    print("")

    (name, email, phoneno) = get_user_info()
    new_customerno = get_next_customerno()

    insert_values(new_customerno, name, email, phoneno)

    print("")
    print("Brukeren ble registrert")
    print("")
    print("---------------------------------------------------------------------------")


if __name__ == "__main__":
    main()


# Lukker tilkobling til databasen
con.close()
