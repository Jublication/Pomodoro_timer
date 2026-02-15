#Thorsten Hopman
#Wat heb ik nodig?
#1. Huidige time, desired time (e.g t + 25, t+5) 2. Aantal pomodoro_sessie_doen's
#Start de timer_laten_lopen na input gebruiker over starten (ja/nee)
#bericht printen voor elke seconde die passeert
#Na bereiken doeltijd, geef een bericht dat de tijd is verlopen en feliciteren
#Pomodoro += 1
#Start de pauze timer op basis van input gebruiker (typ ja als je klaar bent)

from playsound3 import playsound
import configparser
import time
import os
import datetime
from pynput import keyboard

#Als de gebruiker niet ja of nee heeft geantwoord blijft de functie doorvragen
#Deze functie controleert of de gebruiker ja of nee heeft geantwoord
#tot er een geldig antwoord ingevoerd

MINUUT_LENGTE_IN_SEC = 60
RONDE_AANTAL_MAX = 4

def antwoord_ja_of_nee_geven():
    antwoord = input()
    while antwoord.lower() != 'ja' and antwoord.lower() != 'nee':
        antwoord = input('Fout in de input, alleen "ja" of "nee" is mogelijk, voer opnieuw in')
    return antwoord

#pauzeert de keyboard listener wanneer de spatiebalk ingedruk wordt
def on_press(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

#Functie die fungeert als timer met een parameter die aangeeft hoeveel seconden hij moet doorgaan
#Geeft de gepasseerde tijd aan in minuten en seconden sinds de start van de timer
#laat door middel van een keyboard listener de timer pauzeren wanneer de spatiebalk wordt ingedrukt

def timer_laten_lopen(timer_lengte_sec):
    #doorgaan tot dat doeltijd bereikt is
    vroeg_einde = False
    doel_tijd = time.time() + timer_lengte_sec
    print('Timer begint')
    print('Pauzeer de timer door esc in te drukken')
    while doel_tijd > time.time():
        listener = keyboard.Listener( on_press=on_press)
        listener.start()
        start_tijd = int(time.time())

        #doorgaan tot timer op is of listener geactiveerd wordt
        #Is er elegantere manier?
        while doel_tijd > time.time() and listener.is_alive() == True:
            if timer_lengte_sec % MINUUT_LENGTE_IN_SEC == 0:
                print(f'nog {round(timer_lengte_sec / MINUUT_LENGTE_IN_SEC)} minuten te gaan')
            timer_lengte_sec -= 1
            time.sleep(1)

        #Pauze in timer
        if doel_tijd > time.time():
            print('timer gepauzeerd')
            print(f'nog {round(timer_lengte_sec / MINUUT_LENGTE_IN_SEC)} minuten te gaan')
            print('Wil je doorgaan? (ja/nee)')
            antwoord = antwoord_ja_of_nee_geven()
            if antwoord == 'nee':
                doel_tijd = time.time()
                vroeg_einde = True
            elif antwoord == 'ja':
                doel_tijd = time.time() + timer_lengte_sec
                print('Timer gaat door')
        listener.stop()
    return vroeg_einde

#functie die de gebruiker vraagt of die aan de volgende pomodoro will beginnen
#afhankelijk van antwoord start het de volgende pomodoro ronde

def pomodoro_ronde_doen(lengte_sec, ronde_aantal_huidig, stats):
    vroeg_einde = timer_laten_lopen(lengte_sec)
    if not vroeg_einde:
        print(f'Goed gedaan! Je hebt ronde {ronde_aantal_huidig + 1} afgemaakt!')
        stats['aantal rondes totaal'] += 1
        stats['aantal rondes vandaag'] += 1
        stats['aantal minuten totaal'] += lengte_sec
        playsound('/home/thorsten/Music/einde_ronde_pomodoro.mp3')
    return vroeg_einde


#functie die vraagt aan de gebruiker of die de pauze wil beginnen
#afhankelijk van het antwoord begint de pauze

def pauze_doen(lengte_sec):
    print('Als je aan je pauze wil beginnen typ "ja"')
    print('Als je de pauze wilt overslaan typ "nee"')
    antwoord = antwoord_ja_of_nee_geven()
    if antwoord == 'nee':
        return
    timer_laten_lopen(lengte_sec)
    print('De pauze is afgelopen')
    playsound('/home/thorsten/Music/einde_pauze.mp3')
    return

#deze functie begin een pomodoro sessie die 4 rondes lang is
#de duur is gebasseerd op lengtes aangegeven in het hoofdmenu
def pomodoro_sessie_doen(instellingen_lengte_sec, stats):
    ronde_aantal_huidig = 0
    terug_naar_hoofdmenu = False
    #Doorgaan tot het maximaal aantal ronde is bereikt of de gebruiker heeft aangegeven
    #dat die wil stoppen

    while terug_naar_hoofdmenu == False and ronde_aantal_huidig < RONDE_AANTAL_MAX:
        print(f'Één pomodoro sessie bestaat uit {RONDE_AANTAL_MAX} rondes')
        print(f'Huige ronde: {ronde_aantal_huidig + 1}')
        print('Wil je een nieuwe ronde beginnen? (ja/nee)')
        ja_of_nee = antwoord_ja_of_nee_geven()
        #terug naar hoofdmenu
        if ja_of_nee == 'nee':
            terug_naar_hoofdmenu = True
        #beginnen pomodoro ronde
        else:
            vroeg_einde = pomodoro_ronde_doen(instellingen_lengte_sec['ronde_lengte'], ronde_aantal_huidig, stats)
            if not vroeg_einde:
                ronde_aantal_huidig += 1
            #normale rondes hebben een korte pauze
            if ronde_aantal_huidig < RONDE_AANTAL_MAX and not vroeg_einde:
                pauze_doen(instellingen_lengte_sec['korte_pauze_lengte'])
            #ronde 4 heeft een lange pauze
            elif ronde_aantal_huidig == RONDE_AANTAL_MAX and not vroeg_einde:
                print('Goed gedaan, je hebt een hele sessie afgerond, geniet van je lange pauze!')
                pauze_doen(instellingen_lengte_sec['lange_pauze_lengte'])
    print('Terugkeren naar het hoofdmenu')

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

#leest tekst bestand uit en maakt op basis hier van een dictionary aan
def stats_inlezen():
    stats_dict = {}
    huidige_datum = datetime.datetime.now()
    datum_veranderd = False
    #stats.txt aanmaken als deze niet bestaat
    if not os.path.isfile('stats.txt'):
        stats_base_value = [f'datum, {huidige_datum.strftime('%x')}\n', 'aantal rondes totaal, 0\n', 'aantal rondes vandaag, 0\n', 'aantal minuten totaal, 0\n']
        with open('stats.txt', 'w') as stats:
            stats.writelines(stats_base_value)
    #uitlezen en in losse lines, en daarna in losse variabelen opdelen
    with open('stats.txt', 'r') as stats:
        lines = stats.read().splitlines()
    for line in lines:
        gescheiden_line = line.split(', ')
        #variabelen afhandelen die niet int zijn afhandelen
        try:
            int(gescheiden_line[1])
        except:
            if 'datum' in gescheiden_line[0] and gescheiden_line[1] != huidige_datum.strftime('%x'):
                gescheiden_line[1] = huidige_datum.strftime('%x')
                datum_veranderd = True
            stats_dict.update({gescheiden_line[0]: (gescheiden_line[1])})
        else:
            if 'vandaag' in gescheiden_line[0] and datum_veranderd == True:
                gescheiden_line[1] = '0'
            stats_dict.update({gescheiden_line[0]: int(gescheiden_line[1])})
    return stats_dict

#deze functie pakt de statistieken uit de stats_dictionary
#en vergelijkt deze met de statistieken in het stats.txt bestaan
#geeft gebruiker optie om statistieken te resetten
def stats_opslaan(stats_dict):
    inhoud_lines = []
    #ophalen tekst uit text file
    with open('stats.txt', 'r') as stats:
        stats_list = stats.read().splitlines()

    #for loop die tekst file vergelijkt met dictionary
    #vult tijdelijke list in met keys en waarden voor in de tekst file
    for stat in stats_dict:
        for line in stats_list:
            if stat in line:
                gescheiden_line = line.split(', ')
                if gescheiden_line[1] != str(stats_dict[stat]):
                    gescheiden_line[1] = str(stats_dict[stat]) + '\n'
                    vernieuwde_line = ', '.join(gescheiden_line)
                    inhoud_lines.append(vernieuwde_line)
                else:
                    inhoud_lines.append(line + '\n')

#schrijft tijdelijke list met keys en waarden in het tekstbestand
    with open('stats.txt', 'w') as stats:
        stats.writelines(inhoud_lines)


#loopt door de dictionary met stats en print deze per regel
def stats_printen(stats_dict):
    for stat in stats_dict:
        if stat == 'aantal minuten totaal':
            print(f'{stat} : {int(stats_dict[stat] / 60)} minuten')
        else:
            print(stat, ':', stats_dict[stat])
    return

#printen eerste bericht aan gebruiker
def print_welkomst_bericht():
    print('Welkom bij de pomodoro timer')
    print(f'Deze pomodoro timer bestaat uit {RONDE_AANTAL_MAX} rondes')
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
def menu(instellingen_lengte_sec, stats_dict):
    print_welkomst_bericht()
    afsluiten = False
    while not afsluiten:
        #maak een keuze
        antwoord = maak_keuze()
        #begin een pomodoro sessie
        if antwoord == 'p':
            pomodoro_sessie_doen(instellingen_lengte_sec, stats_dict)
        #pas de instellingen aan
        elif antwoord == 'i':
            instellingen_veranderen(instellingen_lengte_sec)
        #print statistieken
        elif antwoord == 's':
            stats_printen(stats_dict)
        #exit programma
        elif antwoord == 'e':
            print('Het programma wordt afgesloten')
            afsluiten = True
        #incorrecte invoer
        else:
            print('incorrecte invoer, probeer opnieuw')
    #statistieken updaten aan einde van programma
    stats_opslaan(stats_dict)

instellingen_lengte = instellingen_config_lezen()
stats = stats_inlezen()
menu(instellingen_lengte, stats)

print('Je bent klaar voor vandaag! Goed gedaan en tot morgen!')
