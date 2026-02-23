-- Schema aanmaken
CREATE SCHEMA Pomodoro;

USE POMODRO;

-- Table gebruiker aanmaken met statistieken
CREATE TABLE Gebruiker(
	gebruikerId INT NOT NULL AUTO_INCREMENT,
    gebruikersnaam VARCHAR(45) not null,
    wachtwoord VARCHAR(45) not null,
    favorieteKleur VARCHAR(20) not null,
    aantRondesTotaal INT DEFAULT 0 not null,
    tijdTotaal INT DEFAULT 0 not null,
    CONSTRAINT pk_gebruiker
    PRIMARY KEY (gebruikerId)
)
;

-- Table Sessie aanmaken met sessie en statistieken
CREATE TABLE Sessie(
	sessieID INT NOT NULL  AUTO_INCREMENT,
    gebruikerId INT NOT NULL,
    sessieStartTijd DATETIME NOT NULL,
    sessieLengte INT NOT NULL,
    aantRondesSessie INT NOT NULL,
    aantPauzesSessie INT NOT NULL,
    aantInstelSessie INT NOT NULL,
    
    CONSTRAINT pk_Sessie
    PRIMARY KEY(sessieID),
    CONSTRAINT fk_Sessie_Gebruiker
	FOREIGN KEY(gebruikerId) REFERENCES Gebruiker(gebruikerId)
)
;
