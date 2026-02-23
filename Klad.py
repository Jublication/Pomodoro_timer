import time
from datetime import datetime, date

class Session:
    def __init__(self, gebruiker_id):
        self.gebruiker_id = gebruiker_id
        self.sesie_start_tijd = datetime.now()
        self.sessie_eind_tijd = 0
        self.sessie_lengte = 0
        self.sessie_aant_rondes = 0
        self.sessie_pom_tijd_totaal = 0
        self.instellingen_aangepast_keer = 0

nieuwe_sessie = Session(1)
time.sleep(2)
sessie_eind_tijd = datetime.now()
sessie_lengte = sessie_eind_tijd - nieuwe_sessie.sesie_start_tijd
nieuwe_sessie.sessie_lengte = sessie_lengte.seconds