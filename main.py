"""
Gemaakt door Thorsten Hopman
Het programma bevat is een pomodoro timer
Dit houdt in dat een gebruiker 4 sessie van 25 minuten doet
Waarin die zich volledig focust op studeren
En daartussenin 3 korte pauzes van 5 minuten heeft om bij te komen
Met aan het einde een lange pauze van 30 minuten
In de main bevindt zicht het hoofdmenu
De bijbehorende module gebruiker management heeft betrekking op het inloggen van de gebruiker
Op basis van informatie uit een SQL-database
De bijbehorende module timer, heeft alle functies voor het uitvoeren van de pomodoro timer
"""

import gebruiker_management as gm
import timer as tm
import configparser
import os
from datetime import datetime

#constanten als globaal declareren
MINUUT_LENGTE_IN_SEC = 60

#filtert antwoorden behalve ja of nee bij ja of nee vragen
def antwoord_ja_of_nee_geven():
    antwoord = input()
    while antwoord.lower() != 'ja' and antwoord.lower() != 'nee':
        antwoord = input('Fout in de input, alleen "ja" of "nee" is mogelijk, voer opnieuw in')
    return antwoord

#leest instellingen in uit een config bestand
def instellingen_config_lezen():
    config = configparser.ConfigParser()
    #controleren of er al een config file bestaat
    #als deze niet bestaat, aanmaken met standaardwaarden
    if not os.path.isfile('config.ini'):
        #testwaardes!
        config['DEFAULT'] = { 'ronde_lengte': '1500',
                              'korte_pauze_lengte': '300',
                              'lange_pauze_lengte': '1800'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')
    ronde_lengte_sec = int(config.get('DEFAULT', 'ronde_lengte'))
    korte_pauze_lengte_sec = int(config.get('DEFAULT', 'korte_pauze_lengte'))
    lange_pauze_lengte_sec = int(config.get('DEFAULT', 'lange_pauze_lengte'))
    instellingen_lengte_config = {
        'ronde_lengte': ronde_lengte_sec,
        'korte_pauze_lengte': korte_pauze_lengte_sec,
        'lange_pauze_lengte': lange_pauze_lengte_sec,
    }
    return instellingen_lengte_config

#slaat instellingen op in een ini file
def instellingen_gebruiker_opslaan(instellingen_lengte_sec):
    config = configparser.ConfigParser()
    config.read('config.ini')
    #vergelijken dictionary met config file
    #als ze niet gelijk zijn update config file met dictionary waardes
    for instelling in instellingen_lengte_sec:
        if instellingen_lengte_sec[instelling] != int(config['DEFAULT'][instelling]):
            config['DEFAULT'][instelling] = str(instellingen_lengte_sec[instelling])
    with open('config.ini', mode= 'w') as configfile:
        config.write(configfile)
    return

#Laat de gebruiker op basis van een ingevoerd aantal minuten
#de lengte van een pomodoro_sessie_doen ronde en de instellingen aanpassen
def instellingen_veranderen(instellingen_lengte_sec):
    terug_naar_hoofdmenu = False
    while not terug_naar_hoofdmenu:
        #huidige instellingen printen
        #nog niet helemaal net, misschien met if statements net laten printen
        for instelling in instellingen_lengte_sec:
            print(f'Huidige {instelling}: {int(instellingen_lengte_sec[instelling] / MINUUT_LENGTE_IN_SEC)} minuten')

        #keuzes voorschotelen en antwoord uitvragen
        print('Welke instelling wil je aanpassen?, voer het eerste karakter in van de gewenste optie')
        print('r: lengte van pomodoro ronde')
        print('k: lengte van korte pauze')
        print('l: lengte van lange pauze')
        print('e: terug naar het hoofdmenu')
        antwoord_instelling = input().lower()

        #keuzes uitvoeren
        if antwoord_instelling == 'r':
            print('Lengte van de ronde aanpassen')
            instellingen_lengte_sec['ronde_lengte'] = int(int(input('Hoeveel minuten lang moet de ronde zijn?')) * MINUUT_LENGTE_IN_SEC)
        elif antwoord_instelling == 'k':
            print('Lengte van de korte pauze aanpassen')
            instellingen_lengte_sec['korte_pauze_lengte'] = int(int(input('Hoeveel minuten lang moet de korte pauze zijn?')) * MINUUT_LENGTE_IN_SEC)
        elif antwoord_instelling == 'l':
            instellingen_lengte_sec['lange_pauze_lengte'] = int(int(input('Hoeveel minuten lang moet de lange pauze zijn?')) * MINUUT_LENGTE_IN_SEC)
        elif antwoord_instelling == 'e':
            terug_naar_hoofdmenu = True
        else:
            print('Incorrecte invoer, voer opnieuw in')
        instellingen_gebruiker_opslaan(instellingen_lengte_sec)
    return




#loopt door de dictionary met stats en print deze per regel
def stats_printen(huidige_gebruiker):
    huidige_gebruiker.display_info()
    return

#printen eerste bericht aan gebruiker
def print_welkomst_bericht():
    print('Welkom bij de pomodoro timer')
    return

#deze functie presenteert gebruiker keuzeopties en laat gebruiker een keuze maken op basis van invoer
def maak_keuze():
    print()
    print('Wat wil je doen? Voer het eerste karakter in van je gewenste optie')
    print('p: Pomodoro doen')
    print('i: instellingen tonen en/of veranderen')
    print('s: statistieken tonen')
    print('e: afsluiten')
    antwoord = input().lower()
    return antwoord

#hoofdmenu
def menu(instellingen_lengte_sec, gebruiker, sessie):
    print_welkomst_bericht()
    afsluiten = False
    while not afsluiten:
        #maak een keuze
        antwoord = maak_keuze()
        #begin een pomodoro sessie
        if antwoord == 'p':
            tm.pomodoro_sessie_doen(instellingen_lengte_sec, gebruiker, sessie)
        #pas de instellingen aan
        elif antwoord == 'i':
            instellingen_veranderen(instellingen_lengte_sec)
        #print statistieken
        elif antwoord == 's':
            stats_printen(gebruiker)
        #exit programma
        elif antwoord == 'e':
            print('Het programma wordt afgesloten')
            afsluiten = True
        #incorrecte invoer
        else:
            print('incorrecte invoer, probeer opnieuw')
    #lengte van de sessie berekenen - verplaatsen naar gebruiker uitloggen functie!
    sessie_eind_tijd = datetime.now()
    sessie_lengte = sessie_eind_tijd - sessie.sessie_start_tijd
    sessie.sessie_lengte = sessie_lengte.seconds
    #statistieken updaten aan einde van programma
    gm.gebruiker_uitloggen(gebruiker, sessie)

class User:
    def __init__(self, gebruiker_id, tijd_totaal, ronde_totaal):
        self.gebruiker_id = gebruiker_id
        self.tijd_totaal = int(tijd_totaal)
        self.ronde_totaal = int(ronde_totaal)
    def display_info(self):
        print(f'Ronde totaal: {self.ronde_totaal} \ntijd totaal: {self.tijd_totaal}')

class Session:
    def __init__(self, gebruiker_id, start_tijd):
        self.gebruiker_id = gebruiker_id
        self.sessie_start_tijd = start_tijd
        self.sessie_lengte = 0
        self.sessie_aant_rondes = 0
        self.sessie_pom_tijd_totaal = 0
    def display_info(self):
        print(f'start tijd: {self.sessie_start_tijd}')

#gebruikersattributen uit database halen
huidige_gebruiker = User(*gm.submenu_inloggen())
huidige_sessie = Session(huidige_gebruiker.gebruiker_id, datetime.now())
instellingen_lengte = instellingen_config_lezen()
menu(instellingen_lengte, huidige_gebruiker, huidige_sessie)

print('Je bent klaar voor vandaag! Goed gedaan en tot morgen!')
