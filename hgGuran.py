from pyrogram import Client, filters
from funzioni import *

app = Client("", bot_token="")

#SALUTO DELLA PERSONA
@app.on_message(filters.command(["start"]))
def start(_, message):
    benvenuto(message)

@app.on_message(filters.command(["help"]))
def help(_, message):
    listaComandi(message)

# MAPPA GENERALE
@app.on_message(filters.command(["mappa"]))
def mappa(_, message):
    mappaGenerale(app, message)

#GESTIONE DEI COMANDI PER LA VSUALIZZAZIONE DELLE MISSIONI
@app.on_message(filters.command(["missioni"]))
def missioni(_, message):
    # viene calcolato il nome del giocatore dal suo tag telegram
    giocatore = getNomeGiocatoreByTag(message.from_user.username)
    if giocatore != None:
        echoMissioni(message, giocatore)
    else:
        message.reply_text("Non sei un giocatore agli Hunger Games")
        return

# invio della mappa
@app.on_message(filters.command(["foresta"]) | filters.command(["vulcano"]) | filters.command(["deserto"]) | filters.command(["ghiacciaio"]) | filters.command(["centro"]))
def bioma(_, message):
    mappaBioma(app, message)

@app.on_message(filters.command(["regolamento"]))
def regolamento(_, message):
    pdfRegolamento(app, message)

@app.on_message(filters.command(["classi"]))
def classi(_, message):
    pdfClassi(app, message)

@app.on_message(filters.command(["boss"]))
def boss(_, message):
    pdfBoss(app, message)

# PER OGNI GIOCATORE, VISUALIZZA IL SUO INVENTARIO
@app.on_message(filters.command(["myInfo"]))
def inventario(_, message):
    # viene calcolato il nome del giocatore dal suo tag telegram
    giocatore = getNomeGiocatoreByTag(message.from_user.username)
    if giocatore != None:
        echoInfo(message, giocatore)
    else:
        message.reply_text("Non sei un giocatore agli Hunger Games")
        return

@app.on_message(filters.command(["master"]))
def master(_, message):
    if  autenticazioneMaster(message.from_user.username):
        #accesso permesso al master
        listaComandiMaster(message)
        
        # --------- GESTIONE DELLE STATISTICHE DEL GIOCATORE
        # Settare i dati di un giocatore dello diverso girone del master tutti assieme
        # /set [player] [life] [forza] [agilita] [astuzia] [classe] [girone]
        @app.on_message(filters.command(["set"]))
        def setPg(_, message):
            if autenticazioneMaster(message.from_user.username):
                settaGiocatore(message)

        # Gestire i danni del giocatori dello diverso girone
        # /danno [player] [danno]
        @app.on_message(filters.command(["danno"]))
        def danno(_, message):
            if autenticazioneMaster(message.from_user.username):
                gestisciDanno(message)

        # Modificare l'armatura dei giocatori dello diverso girone
        # /armatura [player] [+/- modif]
        @app.on_message(filters.command(["armatura"]))
        def armatura(_, message):
            if autenticazioneMaster(message.from_user.username):
                modArmatura(message)

        # Modificare le statistiche di un giocatore dello diverso girone del master
        # /stat [player] [stat] [+/- modifca]
        @app.on_message(filters.command(["stat"]))
        def stat(_, message):
            if autenticazioneMaster(message.from_user.username):
                modificaStatGiocatore(message)
        # ---------------------------------------------------------------

        # -------- GESTIONE DELLE MISSIONI MULTIGIRONE
        # mostra una lista completa di tutte le missioni esistenti per tutti i gironi
        # /listaMissioni
        @app.on_message(filters.command(["listaMissioni"]))
        def listaMissioni(_, message):
            if autenticazioneMaster(message.from_user.username):
                listaMissioniMaster(message)
        
        # modificare stati della missione
        # /missione [idMissione] [attiva/conclusa/disattiva | otp]
        @app.on_message(filters.command(["missione"]))
        def completa(_, message):
            if autenticazioneMaster(message.from_user.username):
                modMissione(message)
        # ---------------------------------------------------------------

        # ---------- GESTIONE DELL'INVENTARIO
        # Visualizzare inventario di un giocatore di un girone diverso da quello del master giocatore
        @app.on_message(filters.command(["info"]))
        def inventarioMaster(_,message):
            if autenticazioneMaster(message.from_user.username):
                try:
                    giocatore = message.command[1]
                    if isCorrectName(giocatore) == True:
                        echoInfo(message, giocatore)
                    else:
                        message.reply_text("Non è un giocatore degli Hunger Games")
                        return
                except IndexError:
                    message.reply_text("Non hai inserito il nome del giocatore a cui vuoi vedere l'inventario!")
            else:
                message.reply_text("Stronzo non puoi vedere le statistiche dei tuoi avversari!")

        # Togliere oggetti dall'inventario di un giocatore di un girone diverso da quello del girone del master giocatore
        # /togliOggetto [giocatore] [oggetto]
        @app.on_message(filters.command(["levaOggetto"]))
        def levaOggetto(_, message):
            if autenticazioneMaster(message.from_user.username):
                riduciInventario(message, app)

        # Inserire oggetti nell'inventario di un giocatore di un girone diverso da quello del girone del master giocatore
        # /nuovoOggetto [giocatore] [oggetto] [descr|opt]
        @app.on_message(filters.command(["mettiOggetto"]))
        def mettiOggetto(_, message):
            if autenticazioneMaster(message.from_user.username):
                inserisciOggetto(message)
        # -------------------------------------------------------------------------

        # ------------------ GESTIONE DELLE ATTIVE / ABILITA' 
        # mostra le attive usate da giocatori del girone che vogliamo ma che non sia quello del master giocatore
        # /listaAttive [girone]
        @app.on_message(filters.command(["listaAttive"]))
        def listaAbilta(_, message):
            if autenticazioneMaster(message.from_user.username):
                listaAttive(message)

        # funzione per aggiungere/rimuovere attiva 
        # /attiva aggiungi [giocatore] [cd] [nome]
        # /attiva rimuovi [id]
        @app.on_message(filters.command(["attiva"]))
        def settaAttiva(_, message):
            if autenticazioneMaster(message.from_user.username):
                settaRimuoviAttiva(message)

        # funzione per modificare i cd dell'attiva
        # /modCd [id_attiva] [cd]
        @app.on_message(filters.command(["modCd"]))
        def modAttiva(_, message):
            if autenticazioneMaster(message.from_user.username):
                modificaCd(message)

        # decrementa cd di un attiva o di tutte, se il master non inserisce un parametro
        # /decrementaAttive [id_girone] [id/opt]
        @app.on_message(filters.command(["decrementaAttive"]))
        def decrementaAttive(_, message):
            if autenticazioneMaster(message.from_user.username):
                decrementaCd(message)
        # -------------------------------------------------------

        
    else:
        # accesso negato al NON master
        message.reply_text("Hey furbetto, a questa edizione il master non sei te!")


app.run()
