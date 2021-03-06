# Detective Game
Ein Projekt im Rahmen des Game Programming Seminars am HPI im Wintersemester 2019.

Dieses Readme beschreibt das gesamte Projekt und enthält außerdem die Beschreibung und Installationsanleitung der Serverkomponente (siehe [Server](https://github.com/EatingBacon/gameprog-detective-server#server)).  
Dieses Repo enthält einerseits den Code der Serverkomponente und außerdemdas [Wiki](https://github.com/EatingBacon/gameprog-detective-server/wiki) unseres Projekts.

## Einführung
Im Rahmen dieses Seminars soll anhand von Spielprototypen demonstriert werden, wie Technologien missbraucht werden können. Wir versuchen in diesem Prototypen weitreichende Berechtigungen auf dem Smartphone des Spielers zu erlangen, um die gespielte Krimigeschichte adaptiv auf den Spieler anzupassen. Außerdem möchten wir die Grenze zwischen dem Spiel und der Realität des Spielers verwischen.
Letztendlich möchten wir anhand des Spielprinzips (Interaktion durch Chat und GPS Daten) einerseits demonstrieren, dass solche Daten anfällig für Manipulation sind (indem wir den Spieler dazu zu bringen, ungewöhliche Dinge zu tun z.B. Besuche von (ungewöhnlichen) Orten, Aufstehen zu ungewöhnlichen Zeiten). Andererseits lenken wir Aufmerksamkeit darauf, dass vielen Menschen nicht bewusst ist, welche Daten man aus gewöhnlichen Standortdaten (die viele einfach preis geben) ableiten kann, so zB den Wohnort durch Messung des Standorts an einem Montag und Dienstag nachts um 2oo Uhr (Standort des Bettes = Wohnort).

## Ergebnis
Im Rahmen des Seminars haben wir ein Framework für text-basierte Spiele entworfen. Das Framework benötigt `story.json` und `story.py` seitens des Framework-Nutzers. Anschließend kann das so spezifizierte Spiel über Telegram mithilfe eines Chatbots gespielt werden. Dabei bietet unser Framework vor allem an, sich Zugriff auf das Telefon des Nutzers zu verschaffen, damit an dessen Daten zu kommen und mit diesen Daten die Story zu personalisieren. Durch Nutzen des Chatbots schaffen wir außerdem eine "Erzählerfigur", mit der der Spieler direkt in Kontakt treten kann.

## Beispiel-Storyline
Der Spieler übernimmt die Rolle eines frisch beförderten Kommissars. Er erhält von seinem Vorgesetzten Hauptkommissar Anweisungen. Diese erfüllt er mithilfe der App, um sich in der Story voranzuspielen. (siehe [story.json](https://github.com/EatingBacon/gameprog-detective-server/blob/master/app/story/story.json))

## Requirements
- Ein Smartphone (Minimale Android API Version 23)
- Eine Telegram-Account

## Softwarekomponenten
Die Software besteht aus 3 Hauptkomponenten, der datensammelnden App (im Folgenden "App" genannt), dem Chatbot (im Folgenden "Bot" genannt) und dem orchestrierendem Server (im Folgenden "Server" genannt).

![Game Architecture](/docs/gameprog_architecture.png)

### App
Diese App ist der Hauptdatensammler des Spiels. Da wir über die Telegram-API nur an sehr begrenzte Daten kommen, versuchen wir mit dieser App an Berechtigungen auf dem Smartphone des Spielers zu erlangen. Die aus solchen Berechtigungen resultierenden Daten können wir dann über das Internet teilen und anhand dieser Daten das Verhalten des Bots anpassen.  
Die App muss vom Spieler heruntergeladen werden, um den Telegram-Chat mit dem Bot zu starten (dabei wird ein Schlüssel übermittelt, damit die gesammelten Daten der App mit einem Telegram-User korreliert werden können). Für eine Liste der möglichen spionierten User Daten siehe [Spied User Data](https://github.com/EatingBacon/gameprog-detective-server/wiki/Spied-User-Data)

[Link zum Repo der App](https://github.com/ADimeo/gameprog-detective-app)

### Bot
Der Telegram-Bot simuliert die Kommunikation des Hauptkommissars mit dem Spieler. Über ihn wird die (adaptive) Spielgeschichte erzählt und die Aufgaben des Hauptkommissars an den Spieler kommuniziert.

[Link zum Repo des Bots](https://github.com/EatingBacon/gameprog-detective-bot)

### Server
Der Server bietet sowohl für die App als auch für den Bot die notwendigen API Endpunkte. Er erhält Daten von der App und speichert und analysiert diese. Er liefert dem Bot die Story, bereits personalisiert für den jeweiligen User. Dafür verwaltet der Server sowohl die Grundstory als auch die Userdaten (persönliche Daten und story-relevante Daten wie aktuellen Spielstand).

Der Source-Code und Dokumentation des Servers ist in diesem Repo zu finden.

#### Install and Start
Voraussetzung ist ein Linux System mit installiertem python 3.8
1. `./manage.sh install` um den Server zu installieren
1. `./manage.sh start` um den Server zu starten
1. für weitere Befehle `./manage.sh help` benutzen
1. siehe [Bot Repo](https://github.com/EatingBacon/gameprog-detective-bot) für Installation und Start des Bots
1. nach Start von Server und Bot kann die App und damit das Spiel gestartet werden

#### Architektur-Überblick
Der Server wird durch eine Flask App (`/app`) implementiert. Diese verwaltet verschiedene API-Endpunkte (`/app/routes`). Außerdem wird eine Datenbank verwaltet. Deren ORM wird in `/app/models` implementiert. Der Story-Inhalt und der Story-verwaltende Code liegt unter `/app/story`.  

#### Spielen ohne Freigeben persönlicher Daten
Unsere App ist sehr datenhungrig. Deswegen startet die App per default in einem Sicherheitsmodus, der das Senden persönlicher Daten verhindert.
Um das Spiel trotzdem spielen zu können, haben wir ein Postman package erstellt. Dieses bietet Mock-Daten an, welche die sonst von der App gestohlenen Daten ersetzen.
1. `detective-game-no-app-walkthrough.json` mit Postman **Desktop** importieren
1. Die Postman Umgebungsvariable `server_ip` auf die Adresse des Rechners setzten, auf dem die Serverkomponente (der Code dieses Repos) läuft
1. Die App starten und *"Kommissar Rex kontaktieren"* tippen und in Telegram auf `STARTEN` tippen
   - alternativ (aber nicht empfohlen) kann komplett ohne App gespielt werden, indem die debug request `create user` gesendet wird
     und der erhaltene `telegram.me` Link geöffnet wird. Dann entfällt der nächste Schritt.
1. mit der debug request `display all users` die eigene user id finden und in die Postman Umgebungsvariable `user_id` eintragen
1. `send mocked contacts` senden, um das Stehlen von Kontakten für "Personalisierung" zu mocken
1. Die Story spielen und neue Aufgaben erfüllen, indem die entsprechende Postman request geschickt wird
   - die Aufgaben requests sind Story-chronologisch geordnet
   - **Achtung!** - für den `take photo of cameras` task muss zuerst ein Bild in Postman ausgewählt werden
   - alternativ kann auch jederzeit der Sicherheitsmodus deaktiviert und die Aufgabe mit der App erfüllt werden,
     indem erst die Daten produziert werden und dann auf die Aufgabe getippt wird

#### Telegram Highjack
Das Finale unseres Spiels ist der Highjack des Telgram Accounts des Nutzers durch die "Mafia".
Dies funktioniert offensichtlich nur, wenn der Sicherheitsmodus deaktiviert ist.
Es reicht jedoch, den Sicherheitsmodus ausschließlich für den Highjack zu deaktivieren, sodass keine weiteren persönlichen Daten gesendet werden
Bevor die Story endet (dies kann auch manuell mit der debug request `set current story point` und dem Parameter `end` hervorgerufen werden) muss:
- Der Sicherheitsmodus deaktiviert werden
- Die Telefonnummer in den Einstellungen der App gesetzt werden (auch falls schon die richtige Nummer da steht muss sie noch einmal bestätigt werden)
- Die App SMS Berechtigungen haben
**Disclaimer**: Unser Highjack richtet keinen Schaden an, trotzdem sollte die "gehackte" Session danach in den Telegram Einstellungen entfernt werden

## FAQ
- *Warum benutzen wir Telegram und simulieren die Kommunikation nicht auch in der App?*  
Da Telegram das Hauptkommunikationsmittel am HPI ist, hoffen wir durch das Integrieren dieser Plattform die Grenzen zwischen dem Programm und echten Personen zu verwischen (indem der Botaccount zwischen echten Kontakten auftaucht, die Nachrichten von echten Menschen und die des Bots in einer Push-Notification stehen, usw.). Außerdem spart uns diese Entscheidung die Arbeit an einem Chatprogramm, welche für einen Prototypen nicht notwendig ist.
- *Welche Annahmen wurden für den Prototypen getroffen?*  
Folgende Annahmen wurden getroffen, damit wir an der Kernidee des Spiels arbeiten konnten. Die Annahmen haben einfache, aber zeitintensive Lösungen, die zur Demonstration des Game Konzeptes nicht notwendig sind:

1. Der Spieler nutzt bereits Telegram (dies ist ein HPI Seminar und der IM-Dienst des HPIs (unter Studierenden)  ist Telegram) (Würde durch eigenen Chatclient in der App gelöst werden)
2. Die App wird während des Spiels nicht vom Spieler deinstalliert (Würde durch "uninstall" Nachricht der App an den Server gelöst werden)
3. Die App hat eine ununterbrochene Internetverbindung (Würde durch interne Queue in der App und regelmäßige Checks seitens des Servers gelöst werden)
