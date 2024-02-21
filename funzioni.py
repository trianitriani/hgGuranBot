# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Author:       Lorenzo Valtriani
# Data:         6/02/2021
# Descrizione:  Funzione usati per il file HgGuran_bot.py
# Versione:     1.0
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

# funzione che controlla se la classe inserita è valida
def isCorrectClass(nomeClasse, giocatore):
    for classe in classi:
        if nomeClasse == classe:
            #creazione della connessione al db
            conn = sqlite3.connect('hg.db')
            #creazione del cursore
            c = conn.cursor()
            query = "SELECT * FROM giocatore WHERE classe = ? AND nome != ?"
            c.execute(query, [nomeClasse, giocatore])
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
    if tag == "prova_tag":
        return "prova"
    else:
        return None

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
    stringa += "/missioni **[bioma]** \n__usato per visualizzare tutte le missioni di quello specifico bioma__\n\n"
    stringa += "/classi \n__attendi pochi secondi e ricevi il pdf delle classi__\n\n"
    stringa += "/boss \n__attendi pochi secondi e ricevi il pdf dei boss__\n\n"
    stringa += "/mappa \n__foto della mappa generale__\n\n"
    stringa += "/foresta \n__ottieni la mappa della foresta__\n\n"
    stringa += "/deserto \n__ottieni la mappa dell deserto__\n\n"
    stringa += "/vulcano \n__ottieni la mappa del vulcano__\n\n"
    stringa += "/ghiacciaio \n__ottieni la mappa del ghiacciaio__\n\n"
    stringa += "/centro \n__ottieni la mappa del centro__\n\n"
    stringa += "/myInfo \n__visualizzare il proprio inventario__\n\n"
    stringa += "/master \n__comando per accedere a comandi: SOLO PER IL MASTER__\n\n"
    message.reply_text(stringa)

# visualizzare le missioni generali e quelle dei singoli biomi
def echoMissioni(message):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    specifco = None
    try:
        bioma = message.command[1]
        if message.command[1] in ["foresta", "vulcano", "deserto", "ghiacciaio", "centro"]:
            testo = "🎯 ECCO LA LISTA DELLE MISSIONI 🎯\n\n"
            if bioma == "foresta":
                testo += "                  🌲🌲🌲🌲\n"
            elif bioma == "vulcano":
                testo += "                  🌋🌋🌋🌋\n"
            elif bioma == "deserto":
                testo += "                  🏖️🏖️🏖️🏖️\n"
            elif bioma == "ghiacciaio":
                testo += "                  🧊🧊🧊🧊\n"
            elif bioma == "centro":
                testo += "                  🧊🌋🌲🏖️\n"

            if(message.command[1] == "centro" or message.command[1] == "foresta" or message.command[1] == "vulcano" or message.command[1] == "deserto" or message.command[1] == "ghiacciaio"):
                query = """SELECT * FROM missione M, bioma B
                           WHERE M.FK_Bioma = B.ID_Bioma AND B.nome = ?"""
                c.execute(query, [message.command[1]])
                specifco = True
                if specifco != None:
                    rows = c.fetchall()

                    for row in rows:
                        #if (biomi_scritti[row[5]-1] == False and specifco == False):
                            #if row[5] == 1:
                            #    testo += "                  🌲🌲🌲🌲\n"
                            #elif row[5] == 2:
                            #    testo += "                  🌋🌋🌋🌋\n"
                            #elif row[5] == 3:
                            #    testo += "                  🏖️🏖️🏖️🏖️\n"
                            #elif row[5] == 4:
                            #    testo += "                  🧊🧊🧊🧊\n"
                            #setta che il nome del bioma è stato scritto
                            #biomi_scritti[row[5]-1] = True

                        testo += f"[{row[0]}] - "
                        testo += "**" + row[1] + "** "
                        if int(row[4]) == 0:
                            testo += "✅\n"
                        else:
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
        # query = """SELECT * FROM missione ORDER BY ID_Missione"""
        # c.execute(query)
        # specifco = False

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


# funzione per visualizzare le informazioni
def echoInfo(message, giocatore):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
    
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
    testo += "\t\t🏃‍♀️ Agilità: "+str(agilita)+"__\t\t\t\t\t(bonus: "+str(calcolaBonus(agilita))+")__\n"
    testo += "\t\t🧠 Astuzia: "+str(astuzia)+"__\t\t\t\t\t(bonus: "+str(calcolaBonus(astuzia))+")__\n"
    # ----- VISUALIZZAZIONE INVENTARIO ------
    query = "SELECT nome, descrizione, quantita FROM oggetto WHERE FK_Giocatore = ? AND quantita != 0"
    c.execute(query, [giocatore])
    rows = c.fetchall()
    testo += "\n🎒--Inventario:--\n"
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

# visualizza la lista dei comandi del master
def listaComandiMaster(message):
    stringa = "**LISTA DEI COMANDI PER IL MASTER**\n"
    stringa += "/levaOggetto **[player] [obj]**\n__modifica gli oggetti che ha il giocatore selezionato__\n"
    stringa += "/mettiOggetto **[player] [obj] [info|opt]**\n__aggiunge un oggetto, le info comprendono il danno, non sono obbligatorie__"
    stringa += "/info **[player]**\n__visulizza le informazioni di quel giocatore__\n"
    stringa += "/set **[player] [life] [forza] [agilita] [astuzia] [classe]**\n__setta le statistiche del giocatore__\n"
    stringa += "/stat **[player] [stat] [-/+ modif]** \n__modifica la singola statistica del giocatore (vita, forza, agilità, astuzia)__\n"
    stringa += "/missione **[idMiss] [attiva/disattiva |otp]** \n__disattiva o attiva la missione rispetto al suo ID. Il secondo argomento si può omettere e la missione si disattiverà__\n"
    stringa += "/armatura **[player] [+/- modif]**\n__modifica l'armatura, questa funzione è stata inserita nel caso sbagliassi e dovessi correggere lo sbaglio.__\n"
    stringa += "/danno **[player] [danno]**\n__funzione per gestire i danni subiti da un giocatore, gestisce il perforamento dell'armatura e avvisa in caso di morte__\n"
    message.reply_text(stringa)

# gestisci l'eliminazione di un oggetto dall'inventario di un giocatore
def riduciInventario(message, app):
    #creazione della connessione al db
    conn = sqlite3.connect('hg.db')
    #creazione del cursore
    c = conn.cursor()
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

# FUNZIONE PER INSERIRE L'OGGETTO
def inserisciOggetto(message):
    try:
        giocatore = message.command[1]
        ogg = message.command[2]
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
            descr = message.command[3]
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

# INSERIMENTO DEI DATI TUTTI ASSIEME
def settaGiocatore(message):
    try:
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
            query = "INSERT INTO giocatore(nome, vita, forza, agilita, astuzia, classe) VALUES(?,?,?,?,?,?)"
            c.execute(query, [nome, vita+bonusForza, forza, agilita, astuzia, classe])
            message.reply_text("Il giocatore: **"+nome+"** è stato creato!")
        else:
            # UPDATE
            query = "UPDATE giocatore SET vita = ?, forza = ?, agilita = ?, astuzia = ?, classe = ? WHERE nome = ?"
            c.execute(query, [vita+bonusForza, forza, agilita, astuzia, classe, nome])
            message.reply_text("Il giocatore: **"+nome+"** è stato modificato!")
        conn.commit()

    except IndexError:
        message.reply_text("Mancano alcuni dati...")
    except ValueError:
        message.reply_text("I dati inseriti sono sbagliati...")

# MODIFICA UNA STATISTICA DI UN GIOCATORE
def modificaStatGiocatore(message):
    try:
        nome = message.command[1]
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

# COMPLETA LA MISSIONE
def modMissione(message):
    try:
        mission = message.command[1]
        # ESEGUI UN CONTROLLO SUL NUMERO

        #creazione della connessione al db
        conn = sqlite3.connect('hg.db')
        #creazione del cursore
        c = conn.cursor()
        try:
            what = message.command[2]
            if what == "disattiva":
                disactive = 1
            elif what == "attiva":
                disactive = 0
            else:
                message.reply_text("Secondo comando non riconosciuto..")
                return
            query = "UPDATE missione SET finita = ? WHERE ID_Missione = ?"
            c.execute(query, [disactive, mission])
            conn.commit()
            query = "SELECT nome FROM missione WHERE ID_Missione = ?"
            c.execute(query, [mission])
            row = c.fetchall()
            if disactive == 1:
                message.reply_text("Hai disattivato la missione: \n**"+row[0][0]+"**")
            else:
                message.reply_text("Hai attivato la missione: \n**"+row[0][0]+"**")
            c.close()
            conn.close()
        # SE NON E' STATO SPECIFICATO IL "metti" "leva" SI PRESUPPONE DI DISATTIVARLA
        except IndexError:
            query = "UPDATE missione SET finita = 1 WHERE ID_Missione = ?"
            c.execute(query, [mission])
            conn.commit()
            query = "SELECT nome FROM missione WHERE ID_Missione = ?"
            c.execute(query, [mission])
            row = c.fetchall()
            message.reply_text("Hai disattivato la missione: \n**"+row[0][0]+"**")
            c.close()
            conn.close()
    except IndexError:
        message.reply_text("Non hai specificato il numero della missione, oppure non è valida!")
        c.close()
        conn.close()
        return
    except ValueError:
        message.reply_text("I dati sono sbagliati...")

# MODIFICARE L'ARMATURA
def modArmatura(message):
    try:
        giocatore = message.command[1]
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

# FUNZIONE PER IL GIOCATORE CHE RICEVE DANNI
def gestisciDanno(message):
    try:
        giocatore = message.command[1]
        if isCorrectName(giocatore) == False:
            message.reply_text("Il giocatore inserito non è valido!")
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
