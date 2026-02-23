#functies gerelateerd aan de timer
import time
from pynput import keyboard
from playsound3 import playsound

MINUUT_LENGTE_IN_SEC = 60
RONDE_AANTAL_MAX = 4

#weghalen
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

def timer_laten_lopen(timer_lengte_sec):
    #doorgaan tot dat doeltijd bereikt is
    vroeg_einde = False
    doel_tijd = time.time() + timer_lengte_sec
    print('Timer begint')
    print('Pauzeer de timer door esc in te drukken')
    while doel_tijd > time.time():
        listener = keyboard.Listener( on_press=on_press)
        listener.start()

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

def pomodoro_ronde_doen(lengte_sec, ronde_aantal_huidig):
    vroeg_einde = timer_laten_lopen(lengte_sec)
    if not vroeg_einde:
        print(f'Goed gedaan! Je hebt ronde {ronde_aantal_huidig + 1} afgemaakt!')
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
def pomodoro_sessie_doen(instellingen_lengte_sec, gebruiker, sessie):
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
            vroeg_einde = pomodoro_ronde_doen(instellingen_lengte_sec['ronde_lengte'], ronde_aantal_huidig)
            if not vroeg_einde:
                ronde_aantal_huidig += 1
                gebruiker.ronde_totaal += 1
                sessie.sessie_aant_rondes += 1
                sessie.sessie_pom_tijd_totaal += instellingen_lengte_sec['ronde_lengte']
                gebruiker.tijd_totaal += instellingen_lengte_sec['ronde_lengte']
            #normale rondes hebben een korte pauze
            if ronde_aantal_huidig < RONDE_AANTAL_MAX and not vroeg_einde:
                pauze_doen(instellingen_lengte_sec['korte_pauze_lengte'])
            #ronde 4 heeft een lange pauze
            elif ronde_aantal_huidig == RONDE_AANTAL_MAX and not vroeg_einde:
                print('Goed gedaan, je hebt een hele sessie afgerond, geniet van je lange pauze!')
                pauze_doen(instellingen_lengte_sec['lange_pauze_lengte'])
    print('Terugkeren naar het hoofdmenu')