# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Author:       Lorenzo Valtriani
# Data:         6/02/2021 V 1.0
#               6/08/2024 V 2.0
#
# Descrizione:  Funzione usati per il file HgGuran_bot.py
# Versione:     2.0
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from pyrogram import Client, filters
import sqlite3
import math

nomi_giocatori = []
classi = ["riftwalker", "alchimista", "dragomante", "mannaro", "appestatore", "cartomante", "samurai", "ranger", "minatore", "barbaro", "valchiria", "guerriero", "predatore", "arciere", "cacciatore", "druido", "mago", "monaco", "paladino", "spia", "bardo", "pirata", "giullare", "piromane", "re", "ninja", "cavaliere", "sciamano"]

def calcolaBonus(stat):
    if (stat == 1 or stat == 2):
        return -2
    elif (stat == 3 or stat == 4):
        return -1
    elif (stat == 5 or stat == 6):
        return 0
    elif (stat == 7 or stat == 8):
        return 1
    elif (stat == 9 or stat == 10):
        return 2
    else:
        # il numero delle statistiche sopra il 10
        stat -= 10
        fascia = float(stat/2)
        # ritorna un vettore contenente la parte frazionaria e la parte intera
        x = math.modf(fascia)
        # se la parte frazionaria è 0 significa che l'ultimo della fascia
        if x[0] == 0:
            return int(x[1]+2)
        # se la parte frazionaria non è 0 allora è in mezzo alla fascia
        else:
            return int(x[1]+3)

def isCorrectName(nome):
    for nome_giocatore in nomi_giocatori:
        if nome == nome_giocatore:
            return True
    return False

# funzione che controlla se la classe inserita è valida (nel senso che non c'è già un altro giocatore nello stesso girone con quella classe)
def isCorrectClass(nomeClasse, giocatore):
    for classe in classi:
        if nomeClasse == classe:
            #creazione della connessione al db
            conn = sqlite3.connect('hg.db')
            #creazione del cursore
            c = conn.cursor()
            query = "SELECT * FROM giocatore WHERE classe = ? AND nome != ? AND FK_Girone = (SELECT FK_Girone FROM giocatore WHERE nome = ?)"
            c.execute(query, [nomeClasse, giocatore, giocatore])
            row = c.fetchall()
            # se non c'è nessun altro giocatore con la stessa classe
            if len(row) == 0:
                return True
    return False

def listaNomiGiocatori():
    testo = "I nomi dei giocatori dovranno essere: \n\n"
    for nome_giocatore in nomi_giocatori:
        testo += nome_giocatore + "\n"
    return testo

def listaClassi():
    testo = "I nomi delle classi sono: \n\n"
    for classe in classi:
        testo += classe + "\n"
    return testo

def getNomeGiocatoreByTag(tag):
    return None

def getGironeByGiocatore(giocatore):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    query = "SELECT FK_Girone FROM giocatore WHERE nome = ?"
    c.execute(query, [giocatore])
    row = c.fetchall()
    # se non c'è il giocatore cercato allora può accedere ai comandi perchè non sta giocando agli hg come giocatore
    if len(row) == 0:
        return False
    return row[0]["FK_Girone"]

# FUNZIONE PER CONVERTIRE IN FILE BINARIO FILE DI GRANDI DIMENSIONI
def convertToBinaryData(path):
    #converti in dato binario un file in memoria
    with open(path, "rb") as file:
        blobData = file.read()
    return blobData

def benvenuto(message):
    stringa = "Ei **"+message.from_user.username+"** benvenuto nel Bot degli Hunger Games di __GURAN TURINO__, premi /help "
    stringa += "per visualizzare tutti i comandi che hai a disposizione!"
    message.reply_text(stringa)

# visualizza la lista dei comandi che un utente non master può eseguire
def listaComandi(message):
    stringa = "💬 LISTA DEI COMANDI 💬\n\n"
    stringa += "/help \n__mostra nuovamente questa lista di comandi__\n\n"
    stringa += "/missioni **[bioma]** \n__usato per visualizzare tutte le missioni di quello specifico bioma__\n\n"
    stringa += "/classi \n__attendi pochi secondi e ricevi il pdf delle classi__\n\n"
    stringa += "/boss \n__attendi pochi secondi e ricevi il pdf dei boss__\n\n"
    stringa += "/regolamento \n__attendi pochi secondi e ricevi il pdf del regolamento__\n\n"
    stringa += "/mappa \n__foto della mappa generale__\n\n"
    stringa += "/myInfo \n__visualizzare il proprio inventario__\n\n"
    stringa += "/master \n__comando per accedere a comandi: SOLO PER IL MASTER__\n\n"
    message.reply_text(stringa)

# visualizzare le missioni generali e quelle dei singoli biomi (gestendo il multigirone)
def echoMissioni(message, giocatore):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    specifco = None
    # ottenere il girone del giocatore
    girone = getGironeByGiocatore(giocatore)
    if (girone == False):   # se il giocatore non ha girone significa che non sta giocando agli hg
        return
    
    try:
        bioma = message.command[1]
        if message.command[1] in ["foresta", "vulcano", "deserto", "ghiacciaio", "centro"]:
            testo = "🎯 ECCO LA LISTA DELLE MISSIONI 🎯\n\n"
            if bioma == "foresta":
                testo += "                  🌲🌲🌲🌲\n"
            elif bioma == "vulcano":
                testo += "                  🌋🌋🌋🌋\n"
            elif bioma == "deserto":
                testo += "                  🏜️🏜️🏜️🏜️\n"
            elif bioma == "ghiacciaio":
                testo += "                  🧊🧊🧊🧊\n"
            elif bioma == "centro":
                testo += "                  🧊🌋🌲🏜️\n"

            if(message.command[1] == "centro" or message.command[1] == "foresta" or message.command[1] == "vulcano" or message.command[1] == "deserto" or message.command[1] == "ghiacciaio"):
                # otteniamo le missioni di quel bioma specificato, che siano attive (finite o da concludere) e facciano parte del girone del giocatore
                query = """SELECT * 
                           FROM missione M, bioma B
                           WHERE M.FK_Bioma = B.ID_Bioma 
                                 AND B.nome = ? AND M.FK_Girone = ? AND attiva = 1"""
                c.execute(query, [message.command[1], girone])
                specifco = True
                if specifco != None:
                    rows = c.fetchall()
                    for row in rows:
                        testo += f"[{row[0]}] - "
                        testo += "**" + row[1] + "** "
                        if int(row[4]) == 0:    # missione conclusa
                            testo += "✅\n"
                        else:                   # missione da finire
                            testo += "❌\n"     
                        testo += row[2] + "\n"
                        testo += "\n**Ricompensa:** __" + row[3] + "__\n\n"
                    
                    message.reply_text(testo)
                    c.close()
            else:
                return

    except IndexError:
        message.reply_text("Devi specificare il bioma, il messaggio risulterebbe troppo lungo.")
        return

def mappaGenerale(app, message):
    app.send_photo(message.from_user.username, "archivio/mappa.jpg")

# funzione che invia la mappa del bioma sotto forma di foto
def mappaBioma(app, message):
    #il nome bioma comprende la "/" perchè un comando, quindi approfittiamo
    app.send_photo(message.from_user.username, "archivio/"+message.text+".jpg")

def pdfClassi(app, message):
    # 1: destinatario
    # 2: il path del documento
    # 3: la miniatura
    # 4: la didascalia
    app.send_document(message.from_user.username, "archivio/classi.pdf", "archivio/guran.jpg", "le classi.");

def pdfBoss(app, message):
    app.send_document(message.from_user.username, "archivio/boss.pdf", "archivio/boss.png", "i boss.");

def pdfRegolamento(app, message):
    app.send_document(message.from_user.username, "archivio/regolamento.pdf", "archivio/guran.jpg", "il regolamento.");

# funzione per visualizzare le informazioni (con controllo girone != master)
def echoInfo(message, giocatore):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()

    girone = getGironeByGiocatore(message.command[1])
    if(gironeDiverso(message.from_user.username, girone) == False):
        message.reply_text("Non puoi visualizzare roba nel tuo stesso girone...")
        return
    
    query = "SELECT vita, forza, agilita, astuzia, classe, armatura FROM giocatore WHERE nome = ?"
    c.execute(query, [giocatore])
    row = c.fetchall()
    if len(row) == 0:
        message.reply_text("Il giocatore non è ancora stato settato!")
        return

    vita = row[0][0]
    forza = row[0][1]
    agilita = row[0][2]
    astuzia = row[0][3]
    classe = row[0][4]
    armatura = row[0][5]
    if (vita == None or forza == None or agilita == None or astuzia == None):
        message.reply_text("Il giocatore non è ancora stato settato!")
        return

    testo = "🧑‍🦱--Info Giocatore--\n\n"
    testo += "\t\tNome: "+giocatore.upper()+"__\t\t\t\t\t("+classe.title()+")__\n"
    if vita >= 20:
        testo += "\t\t💚"
    elif (vita >= 15 and vita < 20):
        testo += "\t\t❤️"
    elif (vita >= 10 and vita < 15):
        testo += "\t\t🧡"
    elif (vita >= 5 and vita < 10):
        testo += "\t\t💛"
    else:
        testo += "\t\t💔"
    testo += f" Vita: {vita}\t\t\t"
    # INSERISCI L'ARMATURA
    testo += f"🛡️ Armatura: {armatura}\n"
    testo += "\t\t💪 Forza: "+str(forza)+"__\t\t\t\t\t\t\t(bonus: "+str(calcolaBonus(forza))+")__\n"
    testo += "\t\t🏃 Agilità: "+str(agilita)+"__\t\t\t\t\t(bonus: "+str(calcolaBonus(agilita))+")__\n"
    testo += "\t\t🧠 Astuzia: "+str(astuzia)+"__\t\t\t\t\t(bonus: "+str(calcolaBonus(astuzia))+")__\n"
    # ----- VISUALIZZAZIONE INVENTARIO ------
    query = "SELECT nome, descrizione, quantita FROM oggetto WHERE FK_Giocatore = ? AND quantita != 0"
    c.execute(query, [giocatore])
    rows = c.fetchall()
    # calcola il numero degli oggetti nell'inventario
    nobj = 0
    for row in rows:
        nobj += row[2]

    testo += "\n🎒-- Inventario:  ("+str(nobj)+"/"+str(10 + calcolaBonus(forza))+") --\n"
    if len(rows) == 0:
        testo += "\t\tvuoto"
    else:
        for row in rows:
            # nome dell'oggetto
            testo += "\t\t**" + row[0].title() + "**:"
            # SE IL NUMERO DELLE OCCORRENE E' SUPERIORE A 1 ALLORA VISUALIZZALO
            if row[2] != 1:
                testo += " (" + str(row[2]) + ")"
            # SE E' STATO INSERITA LA Descrizione ALLORA VISUALIZZALA
            if row[1] != None:
                testo += "\t\t__" + row[1].lower() + "__\n"
            else:
                testo += "\n"

    message.reply_text(testo)

#################################### FUNZIONI PER IL MASTER #######################################

# ritorna true se e solo se il girone in cui gioca il master è diverso da quello che sta modificando
def gironeDiverso(usernameMaster, gironeAzionato):
    giocatore = getNomeGiocatoreByTag(usernameMaster)
    girone = getGironeByGiocatore(giocatore)
    if(girone == gironeAzionato):
        return False
    else:
        return True

# visualizza la lista dei comandi del master
def listaComandiMaster(message):
    stringa = "**LISTA DEI COMANDI PER IL MASTER**\n"
    stringa += "/set **[player] [life] [forza] [agilita] [astuzia] [classe] [girone] **\n__setta le statistiche del giocatore__\n"
    stringa += "/info **[player]**\n__visulizza le informazioni di quel giocatore__\n"
    stringa += "/armatura **[player] [+/- modif]**\n__modifica l'armatura, questa funzione è stata inserita nel caso sbagliassi e dovessi correggere lo sbaglio.__\n"
    stringa += "/danno **[player] [danno]**\n__funzione per gestire i danni subiti da un giocatore, gestisce il perforamento dell'armatura e avvisa in caso di morte__\n"
    stringa += "/stat **[player] [stat] [-/+ modif]** \n__modifica la singola statistica del giocatore (vita, forza, agilità, astuzia)__\n"
    stringa += "/listaMissioni \n__mostra id, nome e girone di tutte le missioni, che siano attivate o meno__\n"
    stringa += "/missione **[idMissione] [attiva/conclusa/disattiva | otp]** \n__disattiva, concludi o attiva la missione rispetto al suo ID. Il secondo argomento si può omettere e la missione si concluderà__\n"
    stringa += "/levaOggetto **[player] [obj]**\n__modifica gli oggetti che ha il giocatore selezionato__\n"
    stringa += "/mettiOggetto **[player] [obj] [info|opt]**\n__aggiunge un oggetto, le info comprendono il danno, non sono obbligatorie__\n"
    message.reply_text(stringa)

# lista di tutti i master
def autenticazioneMaster(username):
    return False

# gestisci l'eliminazione di un oggetto dall'inventario di un giocatore (con controllo su girone != master)
def riduciInventario(message, app):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    #controllare che il master non modifichi l'inventario di un giocatore del suo stesso girone
    girone = getGironeByGiocatore(message.command[1])
    if(gironeDiverso(message.from_user.username, girone) == False):
        message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
        return

    query = "SELECT quantita, ID_Oggetto FROM oggetto WHERE nome = ? AND FK_Giocatore = ?"
    try:
        giocatore = message.command[1]
        oggetto = message.command[2]
        c.execute(query, [oggetto, giocatore])
        row = c.fetchall()
        if len(row) == 1:
            print(row)
            q = row[0][0]
            ogg = row[0][1]
            if q > 0:
                #bisogna sottrarre un'occorrenza
                query = "UPDATE oggetto SET quantita = ? WHERE ID_Oggetto = ?"
                c.execute(query, [q-1, ogg])
                conn.commit()
                message.reply_text("L'oggetto si trova nell'inventario ed è stata tolta una sua occorrenza")
            else:
                message.reply_text("L'oggetto non si trovava già più nel suo inventario")
        else:
            message.reply_text("I dati inseriti sono sbagliati")
            #accesso riuscito, adesso togliamo gi oggetti

    except IndexError:
        message.reply_text("Non è stato indicato il giocatore o l'oggetto")
        return

# FUNZIONE PER INSERIRE L'OGGETTO (con controllo su girone != master)
def inserisciOggetto(message):
    try:
        giocatore = message.command[1]
        ogg = message.command[2]
        # controllo che il master non modifichi l'inventario di un giocatore del proprio girone  (false se il giocatore non ha girone aka non gioca)
        girone = getGironeByGiocatore(giocatore)
        if(gironeDiverso(message.from_user.username, girone) == False):
            message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
            return
        
        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        query = "SELECT quantita, ID_Oggetto FROM oggetto WHERE nome = ? AND FK_Giocatore = ?"
        c.execute(query, [ogg, giocatore])
        row = c.fetchall()
        occorrenza = None
        if len(row) == 1:
            occorrenza = row[0][0]
        try:
            descr = " ".join(message.command[3:])
            # NON ESISTE NEL DB
            if occorrenza == None:
                # INSERT NEL DB
                query = "INSERT INTO oggetto(nome, descrizione, FK_Giocatore) VALUES (?,?,?)"
                c.execute(query, [ogg, descr, giocatore])
                message.reply_text("Oggetto: **"+ogg+"** aggiunto all'inventario di "+giocatore)
            # ESISTE NEL DB
            else:
                # UPDATE NEL DB
                print(descr)
                query = "UPDATE oggetto SET quantita = ?, descrizione = ? WHERE nome = ? AND FK_Giocatore = ?"
                c.execute(query, [occorrenza+1, descr, ogg, giocatore])
                message.reply_text("Oggetto: **"+ogg+"** aggiunto all'inventario di "+giocatore+" ora ne possiede "+str(occorrenza+1))
            conn.commit()
        # SE NON E' STATA DICHIARATA LA Descrizione
        except IndexError:
            # NON ESISTE NEL DB
            if occorrenza == None:
                # INSERT NEL DB
                query = "INSERT INTO oggetto(nome, FK_Giocatore) VALUES (?,?)"
                c.execute(query, [ogg, giocatore])
                message.reply_text("Oggetto: **"+ogg+"** aggiunto (senza descrizione) all'inventario di "+giocatore)
            # ESISTE NEL DB
            else:
                # UPDATE NEL DB
                query = "UPDATE oggetto SET quantita = ? WHERE nome = ? AND FK_Giocatore = ?"
                c.execute(query, [occorrenza+1, ogg, giocatore])
                message.reply_text("Oggetto: **"+ogg+"** aggiunto (senza descrizione) all'inventario di "+giocatore+" ora ne possiede "+str(occorrenza+1))
            conn.commit()

    except IndexError:
        message.reply_text("Non è stato correttamente inviato il comando!")

# INSERIMENTO DEI DATI TUTTI ASSIEME (con controllo su girone != master)
def settaGiocatore(message):
    try:
        girone = message.command[7]
        # controlla che non si stia inserendo un giocatore nello stesso girone in cui gioca il master
        if(gironeDiverso(message.from_user.username, girone) == False):
            message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
            return
        
        nome = message.command[1]
        if isCorrectName(nome) == False:
            message.reply_text("Il nome inserito non è corretto!")
            message.reply_text(listaNomiGiocatori())
            return

        vita = int(message.command[2])
        forza = int(message.command[3])
        agilita = int(message.command[4])
        astuzia = int(message.command[5])
        bonusForza = calcolaBonus(forza)
        if (forza+agilita+astuzia) != 21:
            message.reply_text("La somma delle statistiche non fa 21!")
            return

        bForza = calcolaBonus(forza)
        # la classe del giocatore
        classe = message.command[6]
        if isCorrectClass(classe, nome) == False:
            message.reply_text("La classe inserita non è valida o è già occupata!")
            message.reply_text(listaClassi())
            return

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        query = "SELECT * FROM giocatore WHERE nome = ?"
        c.execute(query, [nome])
        row = c.fetchall()
        if len(row) == 0:
            # INSERT
            query = "INSERT INTO giocatore(nome, vita, forza, agilita, astuzia, classe, FK_Girone) VALUES(?,?,?,?,?,?,?)"
            c.execute(query, [nome, vita+bonusForza, forza, agilita, astuzia, classe, girone])
            message.reply_text("Il giocatore: **"+nome+"** è stato creato!")
        else:
            # UPDATE
            query = "UPDATE giocatore SET vita = ?, forza = ?, agilita = ?, astuzia = ?, classe = ?, FK_Girone = ? WHERE nome = ?"
            c.execute(query, [vita+bonusForza, forza, agilita, astuzia, classe, girone, nome])
            message.reply_text("Il giocatore: **"+nome+"** è stato modificato!")
        conn.commit()

    except IndexError:
        message.reply_text("Mancano alcuni dati...")
    except ValueError:
        message.reply_text("I dati inseriti sono sbagliati...")

# MODIFICA UNA STATISTICA DI UN GIOCATORE (con controllo su girone != master)
def modificaStatGiocatore(message):
    try:
        nome = message.command[1]
        # controlla che non si stia modificando un giocatore nello stesso girone in cui gioca il master
        girone = getGironeByGiocatore(nome)
        if(gironeDiverso(message.from_user.username, girone) == False):
            message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
            return
        
        stat = message.command[2]
        modif = int(message.command[3])
        # RISOLVE IL PROBLEMA DI UNA STATISTICA CHE NON ESISTE
        if (stat != "forza" and stat != "agilita" and stat != "astuzia" and stat != "vita"):
            message.reply_text("La statistica che hai inserito non esiste!")
            return

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        query = "SELECT "+stat+" FROM giocatore WHERE nome = ?"
        c.execute(query, [nome])
        row = c.fetchall()
        if (len(row) == 1 and row[0][0] != None):
            valore = row[0][0]
            query = "UPDATE giocatore SET "+stat+" = ? WHERE nome = ?"
            c.execute(query, [valore+modif, nome])
            conn.commit()

            # AVVISO SE E' MORTO IL GIOCATORE
            if (stat == "vita" and modif < 0 and valore < (modif*(-1))):
                message.reply_text("Cazzo.. il combattente **"+nome+".. \nE' CADUTO!**")
                return

            message.reply_text("Hai modificato la statistica: **"+stat+"**")

        else:
            message.reply_text("Il giocatore: **"+nome+"** non esiste ancora o non è ancora stato settato!")

    except IndexError:
        message.reply_text("Mancano alcuni dati...")
    except ValueError:
        message.reply_text("I dati sono sbagliati...")

# Lista delle missioni tutte, così che possa conoscere gli id di quest'ultime e il relativo girone
def listaMissioniMaster(message):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    query = """SELECT ID_Missione, nome, attiva, FK_Girone
               FROM missione
               ORDER BY FK_Girone, ID_Missione"""
    c.execute(query)
    rows = c.fetchall()
    stringa = ""
    #mostrare la lista delle missioni che sono state inserite nel database (anche quelle non giocabili)
    for row in rows:
         stringa += row[0]+") "+row[1]+" [G"+row[3]+"] "
         if(row[2] == True): 
            stringa += "✅\n"
         else: 
            stringa += "\n"
        
    c.close()
    conn.close()
    message.reply_text(stringa)
    return

# Modificare la missione del girone stesso del master
def modMissione(message):
    try:
        mission = message.command[1]
        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        try:
            what = message.command[2]
            if what == "conclusa":     # la missione è stata completata (il giocatore la vede completata)
                finita = 1 
                attiva = 1
            elif what == "attiva":     # la missione è attualmente attiva (il giocatore la vede da completare)
                finita = 0
                attiva = 1
            elif what == "disattiva":  # la missione non è attualmente attiva (il giocatore non la vede)
                finita = 0
                attiva = 0
            else:
                message.reply_text("Secondo comando non riconosciuto..")
                return
            query = "UPDATE missione SET finita = ?, attiva = ? WHERE ID_Missione = ?"
            c.execute(query, [finita, attiva, mission])
            conn.commit()
            query = "SELECT nome FROM missione WHERE ID_Missione = ?"
            c.execute(query, [mission])
            row = c.fetchall()
            if finita == 1:
                message.reply_text("Hai concluso la missione: **"+row[0][0]+"**\n")
            else:
                message.reply_text("Hai attivato la missione: **"+row[0][0]+"**\n")

            if attiva == 1:
                message.reply_text("Hai aggiunto la missione: **"+row[0][0]+"**\n")
            else:
                message.reply_text("Hai disattivato la missione: **"+row[0][0]+"**\n")
            c.close()
            conn.close()
        # se non è stato inserito il parametro "attiva" "disattiva" "conclusa" si presuppone di concluderla
        except IndexError:
            query = "UPDATE missione SET finita = 1 WHERE ID_Missione = ?"
            c.execute(query, [mission])
            conn.commit()
            query = "SELECT nome FROM missione WHERE ID_Missione = ?"
            c.execute(query, [mission])
            row = c.fetchall()
            message.reply_text("Hai concluso la missione: \n**"+row[0][0]+"**")
            c.close()
            conn.close()
    except IndexError:
        message.reply_text("Non hai specificato il numero della missione, oppure non è valida!")
        c.close()
        conn.close()
        return
    except ValueError:
        message.reply_text("I dati sono sbagliati...")

# MODIFICARE L'ARMATURA (con controllo su girone != master)
def modArmatura(message):
    try:
        giocatore = message.command[1]
        # controllo che non si modifichi l'armatura se il master gioca nello stesso girone
        girone = getGironeByGiocatore(giocatore)
        if(gironeDiverso(message.from_user.username, girone) == False):
            message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
            return
        
        if isCorrectName(giocatore) == False:
            message.reply_text("Il giocatore inserito non è valido")
            message.reply_text(listaNomiGiocatori())
            return

        modif = int(message.command[2])
        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        query = "SELECT ID_Giocatore, armatura FROM giocatore WHERE nome = ?"
        c.execute(query, [giocatore])
        row = c.fetchall()
        if len(row) == 0:
            message.reply_text("Il giocatore inserito non è ancora stato settato")
            return
        armaturaOra = row[0][1]
        armatura = armaturaOra + modif
        if armatura < 0:
            armatura = 0
        query = "UPDATE giocatore SET armatura = ? WHERE ID_Giocatore = ?"
        c.execute(query, [armatura, row[0][0]])
        conn.commit()
        message.reply_text(f"Hai settato l'armatura di **{giocatore}** a **{armatura}**")
        c.close()
        conn.close()

    except IndexError:
        message.reply_text("Mancano alcuni dati!")
        return

# FUNZIONE PER IL GIOCATORE CHE RICEVE DANNI (con controllo girone != master)
def gestisciDanno(message):
    try:
        giocatore = message.command[1]
        if isCorrectName(giocatore) == False:
            message.reply_text("Il giocatore inserito non è valido!")
            return
        
        # controllo che non si infligga danno se il master gioca nello stesso girone
        girone = getGironeByGiocatore(giocatore)
        if(gironeDiverso(message.from_user.username, girone) == False):
            message.reply_text("Non puoi modificare roba nel tuo stesso girone...")
            return
        
        danno = int(message.command[2])
        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        query = "SELECT vita, armatura FROM giocatore WHERE nome = ?"
        c.execute(query, [giocatore])
        row = c.fetchall()
        if len(row) == 0:
            message.reply_text("Non hai ancora settato il giocatore!")
            return
        vita = int(row[0][0])
        armatura = int(row[0][1])
        if danno <= armatura:
            # SOTTRARRE IL DANNO ALL'ARMATURA
            armaturaRimasta = armatura - danno
            query = "UPDATE giocatore SET armatura = ? WHERE nome = ?"
            c.execute(query, [armaturaRimasta, giocatore])
            message.reply_text(f"Al giocatore **{giocatore}** rimane {armaturaRimasta} di armatura")
        else:
            # MODIFICARE ANCHE LA VITA, ARMATURA A 0
            # bisogna vedere di quanto sfora
            armaturaSforata = armatura - danno
            # armaturaSforata: è negativo, quindi serve effettuare una somma, che diventa una sottrazione
            vitaRimasta = vita + armaturaSforata
            query = "UPDATE giocatore SET armatura = 0, vita = ? WHERE nome = ?"
            c.execute(query, [vitaRimasta, giocatore])
            if vitaRimasta <= 0:
                message.reply_text(f"Cazzo.. il combattente **{giocatore}..\nE' CADUTO**")
            else:
                message.reply_text(f"Al giocatore **{giocatore}** rimane {vitaRimasta} di vita e nessun'armatura")
        conn.commit()
        c.close()
        conn.close()
    except IndexError:
        message.reply_text("Mancano alcuni dati...")
        return

# ottieni il girone dall'id dell'attiva
def getGironeByAttiva(id_attiva):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    query = """SELECT G.FK_Girone
                FROM attiva A, giocatore G
                WHERE A.FK_Giocatore = G.ID_Giocatore AND A.ID_Attiva = ?"""
    c.execute(query, [id_attiva])
    girone_target = c.fetchone()[0]
    c.close()
    conn.close()

    return girone_target

# ottieni la lista delle attive in cd nel proprio girone (con controllo girone != girone master)
def listaAttive(message):
    girone = getGironeByGiocatore(message.from_user.username)
    girone_target = message.command[1]
    if(girone == girone_target):
        message.reply_text("Mica puoi controllare le informazioni del tuo girone")
        return

    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    query = """SELECT A.ID_Attiva, A.nome, A.cd, G.nome
               FROM attiva A, giocatore G 
               WHERE A.FK_Giocatore = G.ID_Giocatore AND G.FK_Girone = ?"""
    c.execute(query, [girone_target])
    rows = c.fetchall()
    if len(rows) == 0:
            message.reply_text("Non ci sono ancora attive attivate!")
            return

    stringa = ""
    #mostrare la lista delle attive usate
    for row in rows:
         stringa += row[0] + ") "+row[1]+" ["+row[3]+"] CD: **"+row[2]+"**\n"
    c.close()
    conn.close()
    message.reply_text(stringa)
    return

# aggiungi o rimuovi un attiva dalla lista di un girone in cui non giochi (con controllo girone != master)
# /attiva aggiungi [giocatore] [cd] [nome]
# /attiva rimuovi [id]
def settaRimuoviAttiva(message):
    what = message.command[1]
    if what == "aggiungi":
        # controllo che il master non stia aggiungendo attive per giocatori del proprio girone da giocatore
        girone = getGironeByGiocatore(message.from_user.username)
        giocatore = message.command[2]
        girone_target = getGironeByGiocatore(giocatore)
        if(girone == girone_target):
            message.reply_text("Mica puoi modificare le informazioni del tuo girone")
            return 
        
        # ottentimento del cd
        cd = message.command[3]
        if(cd > 0):
            message.reply_text("Il cd deve essere maggiore di zero.")
            return
        
        # ottenimento del nome dell'attiva
        nome = " ".join(message.command[4:])

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()

        # ottenimento dell'id del giocatore
        c.execute("SELECT ID_Giocatore FROM giocatore WHERE nome = ?", (giocatore))
        id_giocatore = c.fetchone()

        # inserimento attiva
        query = "INSERT INTO attiva(nome, cd, FK_Giocatore) VALUES (?,?,?)"
        c.execute(query, [nome, cd, id_giocatore[0]])
        conn.commit()
        c.close()
        conn.close()

    elif what == "rimuovi":
        girone = getGironeByGiocatore(message.from_user.username)
        id_attiva = message.command[2]

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()

        # controllare che il girone sia diverso da quello del master giocatore
        girone_target = getGironeByAttiva(id_attiva)
        if(girone == girone_target):
            message.reply_text("Mica puoi modificare le informazioni del tuo girone")
            c.close()
            conn.close()
            return

        # rimuovere l'attiva dal database
        query = """DELETE FROM attiva 
                   WHERE ID_Attiva = ?"""
        c.execute(query, [id_attiva])
        conn.commit()
        c.close()
        conn.close()

    else:
        message.reply_text("Parametro numero 1 non valido, controlla la sintassi con /master")
    
    return

# funzione per modificare i cd dell'attiva (con controllo girone != master)
# /modCd [id_attiva] [cd]
def modificaCd(message):
    girone = getGironeByGiocatore(message.from_user.username)
    id_attiva = message.command[1]

    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()

    # controllare che il girone sia diverso da quello del master giocatore
    girone_target = getGironeByAttiva(id_attiva)
    if(girone == girone_target):
        message.reply_text("Mica puoi modificare le informazioni del tuo girone")
        c.close()
        conn.close()
        return
    
    # modificare valore del cd
    query = """UPDATE attiva 
               SET cd = ? 
               WHERE ID_Attiva = ?"""
    c.execute(query, [id_attiva])
    conn.commit()
    c.close()
    conn.close()
    message.reply_text("Valore del cd modificato, controlla il risultato con /listaAttive")
    return

# decrementa cd di un attiva o di tutte, se il master non inserisce un parametro (con controllo girone != master)
# /decrementaAttive [id_girone] [id/opt]
def decrementaCd(message):
    # controllare che il girone non sia quello del master giocatore
    girone = getGironeByGiocatore(message.from_user.username)
    girone_target = message.command[1]
    if(girone == girone_target):
        message.reply_text("Mica puoi modificare le informazioni del tuo girone")
        return
    
    id_attiva = message.command[2]
    if id_attiva == "":
        # allora decremento tutte le attive del girone
        # creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        # allora decremento solo l'attiva target
        query = """UPDATE attiva 
                   SET cd = cd - 1
                   WHERE ID_Attiva IN (
                                        SELECT A.ID_Attiva
                                        FROM attiva A, giocatore G
                                        WHERE A.FK_Giocatore = G.ID_Giocatore 
                                              AND G.FK_Girone = ?
                                      )"""
        c.execute(query, [girone])
        conn.commit()
        c.close()
        conn.close()
        message.reply_text("Valori dei cd decrementati, controlla i risultati con /listaAttive")

    else:
        # controllo extra poichè il master può aver inserito un id_girone != da quello 
        # effettivamente relativo all'attiva
        girone_target = getGironeByAttiva(id_attiva)
        if(girone == girone_target):
            message.reply_text("Mica puoi modificare le informazioni del tuo girone")
            return

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        # allora decremento solo l'attiva target
        query = """UPDATE attiva 
                   SET cd = cd - 1
                   WHERE ID_Attiva = ?"""
        c.execute(query, [id_attiva, id_attiva])
        conn.commit()
        c.close()
        conn.close()
        message.reply_text("Valore del cd decrementato, controlla il risultato con /listaAttive")

    return
