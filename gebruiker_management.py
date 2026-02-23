#functies gerelateerd aan het inloggen en registreren van gebruiker in de database
import argon2.exceptions
import mysql.connector
from argon2 import PasswordHasher



def antwoord_ja_of_nee_geven():
    antwoord = input()
    while antwoord.lower() != 'ja' and antwoord.lower() != 'nee':
        antwoord = input('Fout in de input, alleen "ja" of "nee" is mogelijk, voer opnieuw in')
    return antwoord

#wachtwoord hashen met argon2
def wachtwoord_hashen(wachtwoord):
    ph = PasswordHasher()
    hash = ph.hash(wachtwoord)
    return hash

#laat de gebruiker een gebruikersnaam aanmaken
#vergelijkt gebruikersnaam met gebruikersnamen in de database voor uniciteit
def gebruikersnaam_aanmaken():
    gebruikersnaam_check = False
    while not gebruikersnaam_check:
        print('Voer een nieuwe gebruikersnaam in')
        gebruikersnaam = input()
        print(f'Uw gebruikersnaam is: {gebruikersnaam}')
        mycursor.execute(f'SELECT gebruikersnaam FROM Gebruiker WHERE gebruikersnaam =%s', (gebruikersnaam,))
        gebruiker = mycursor.fetchone()
        if gebruiker:
            print('Gebruikersnaam bestaat al, probeer een andere naam')
        else:
            print('Is dit uw gewenste gebruikersnaam? ja/nee')
            antwoord = antwoord_ja_of_nee_geven()
            if antwoord == 'ja':
                gebruikersnaam_check = True
    return gebruikersnaam

#laat de gebruiker een wachtwoord aanmaken
#stelt eisen aan het wachtwoord
def wachtwoord_aanmaken():
    wachtwoord_check = False
    eis_lengte = False
    eis_upper = False
    eis_num = False
    eis_alnum = False
    #Controleren wachtwoord op eisen
    while not wachtwoord_check:
        while not eis_lengte or not eis_upper or not eis_num or not eis_alnum:
            #eisen weergeven
            print('Een wachtwoord moet minimaal:')
            print('-8 tekens lang zijn')
            print('-1 upper case letter bevatten')
            print('-1 getal bevatten')
            print('-1 symbool bevatten')
            print('Voer uw gewenste wachtwoord in')
            wachtwoord = input()

            #ingevoerde wachtwoord testen op eisen
            if len(wachtwoord) < 8:
                print('Wachtwoord is te kort, minimum is 8 tekens')
            else:
                eis_lengte = True
                for teken in wachtwoord:
                    if teken.isupper():
                        eis_upper = True
                    if teken.isdigit():
                        eis_num = True
                    if not teken.isalnum():
                        eis_alnum = True
                if not eis_upper:
                    print('Wachtwoord bevat geen hoofdletters')
                if not eis_num:
                    print('Wachtwoord bevat geen cijfers')
                if not eis_alnum:
                    print('Wachtwoord bevat geen symbolen')

        #wachtwoord natypen om zeker te zijn van goede invoer
        while not wachtwoord_check:
            wachtwoord_opnieuw = input('Voer wachtwoord nogmaals in ')
            if wachtwoord == wachtwoord_opnieuw:
                wachtwoord_check = True
            else:
                print('Wachtwoorden komen niet overeen probeer opnieuw')
        hash = wachtwoord_hashen(wachtwoord)
    return hash

#laat de gebruiker een favoriete kleur invullen
#voor een herstelvraag
def favoriete_kleur_kiezen():
    favoriete_kleur_check = False
    while favoriete_kleur_check == False:
        #uitleg favoriete kleur/herstellen
        print('Mocht je je gegevens kwijtraken, dan is er een hestelvraag')
        print('Geef antwoord op de volgende vraag:')
        print('Wat is je favoriete kleur?')
        favoriete_kleur = input('Mijn favoriete kleur is: ')
        print(f'Is deze kleur correct? {favoriete_kleur} (ja/nee)')
        antwoord = antwoord_ja_of_nee_geven()
        if antwoord == 'ja':
            favoriete_kleur_check = True
        else:
            print('Voer opnieuw in')
    return favoriete_kleur

#Functie die aanmaken gebruikersnaam, wachtwoord en favoriete kleur afhandelt
#en informatie opslaat in de database
def gebruiker_registreren():
    #benodigde gegevens laten invoeren door gebruiker
    gebruikersnaam = gebruikersnaam_aanmaken()
    hash = wachtwoord_aanmaken()
    favoriete_kleur = favoriete_kleur_kiezen()
    #gegevens in database plaatsen
    sql = 'INSERT INTO Gebruiker (gebruikersNaam, hash, favorieteKleur) VALUES(%s, %s, %s)'
    val = (gebruikersnaam, hash, favoriete_kleur)
    mycursor.execute(sql, val)
    mydb.commit()
    print('registratie succesvol')

#logt gebruiker in door combinatie gebruikersnaam en wachtwoord te vergelijken met informatie in de database
def gebruiker_inloggen():
    wachtwoord_check = False

     #controleren of wachtwoord past bij wachtwoord van gebruikersnaam in database
    while not wachtwoord_check:
        print('Voer uw gebruikersnaam in')
        gebruikersnaam = (input(),)
        print('Voer uw wachtwoord in')
        wachtwoord = input()
        mycursor.execute('SELECT hash FROM Gebruiker WHERE gebruikersnaam = %s', gebruikersnaam)
        try:
            hash_database = mycursor.fetchone()[0]
        #incorrecte niet bestaand gebruikers eruithalen met error handling
        except TypeError:
            print('incorrecte combinatie gebruikersnaam en wachtwoord')
        #controleren
        else:
            ph = PasswordHasher()
            #bestaande gebruikersnaam, maar wachtwoord is incorrect errorhandling
            try:
                ph.verify(hash_database, wachtwoord)
            except argon2.exceptions.VerifyMismatchError:
                print('incorrecte combinatie gebruikersnaam en wachtwoord')
            else:
                print('wachtwoord klopt')
                wachtwoord_check = True


    #ophalen gebruikersgegevens uit database
    if wachtwoord_check:
        mycursor.execute('SELECT gebruikerId, aantRondesTotaal, tijdTotaal FROM Gebruiker WHERE gebruikersnaam = %s', gebruikersnaam)
        attributen = mycursor.fetchone()
    return attributen

#laat gebruiker wachtwoord herstellen door middel van invoeren
#gebruikersnaam en favoriete kleur
def wachtwoord_herstellen():
    print('Voer de gebruikersnaam in van het te herstellen account')
    gebruikersnaam = (input(),)
    mycursor.execute('SELECT favorieteKleur FROM Gebruiker WHERE gebruikersnaam = %s;', gebruikersnaam)
    favoriete_kleur_db = str(mycursor.fetchone()[0])
    favoriete_kleur = input('Voer de bijbehorende kleur in')
    while favoriete_kleur != favoriete_kleur_db:
        print('Combinatie incorrect')
        favoriete_kleur = input('Voer de bijbehorende kleur in')
    print('Correcte combinatie van gebruikersnaam en kleur ingevoerd')
    nieuw_wachtwoord = input('Voer het nieuwe wachtwoord in')
    controle_wachtwoord = input('Voer het wachtwoord nog een keer in')
    while nieuw_wachtwoord != controle_wachtwoord:
        print('Combinatie incorrect')
        controle_wachtwoord = input('Voer het wachtwoord nog een keer in')
    mycursor.execute('UPDATE Gebruiker SET wachtwoord = %s;', (nieuw_wachtwoord,))
    mydb.commit()
    print('Wachtwoord geupdatet')


#gebruiker gegevens uitlezen
#gegevens in database updaten hiermee
def gebruiker_uitloggen(gebruiker, sessie):
    sql = 'UPDATE Gebruiker SET aantRondesTotaal = %s, tijdTotaal = %s WHERE gebruikerId = %s;'
    val =  (gebruiker.ronde_totaal, gebruiker.tijd_totaal, gebruiker.gebruiker_id)
    mycursor.execute(sql, val)
    sql = 'INSERT INTO Sessie (gebruikerId, sessieStartTijd, sessieLengte, aantRondesSessie, sessieTijdTotaal)  VALUES (%s, %s, %s, %s, %s);'
    val = sessie.gebruiker_id, sessie.sessie_start_tijd, sessie.sessie_lengte, sessie.sessie_aant_rondes, sessie.sessie_pom_tijd_totaal
    mycursor.execute(sql, val)
    mydb.commit()
    print('statistieken in database geupdatet')
    print('gebruiker uitgelogd')

#weergeeft keuzes in dit menu en laat gebruiker keuze invoeren
def maak_keuze():
    print('Maak een keuze')
    print('i: inloggen met een bestaand account')
    print('r: nieuw account registreren')
    print('w: wachtwoord herstellen')
    print('e: programma beëindigen')
    keuze = input().lower()
    return keuze

#stuurt gebruiker door naar functie die bij keuze hoort,
#geeft attributen van gebruiker door naar hoofdprogramma
def submenu_inloggen():
    ingelogd = False
    while not ingelogd:
        keuze = maak_keuze()
        if keuze == 'i':
            print('gebruiker inloggen')
            attributen = gebruiker_inloggen()
            if attributen:
                ingelogd = True
        if keuze == 'r':
            print('gebruiker registreren')
            gebruiker_registreren()
        if keuze == 'w':
            print('wachtwoord herstellen')
            wachtwoord_herstellen()
        elif keuze == 'e':
            'programma wordt beëindigd'
            exit()
    return attributen


#verbinden met database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='PiperFawn1',
    database='Pomodoro'
)
mycursor = mydb.cursor()

# test
mycursor.execute("SELECT * FROM Gebruiker")
myresult = mycursor.fetchall()
for row in myresult:
    print(row)

if __name__ == '__main__':
    submenu_inloggen()








