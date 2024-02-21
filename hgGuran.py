from pyrogram import Client, filters
from funzioni import *

app = Client("", bot_token="")
master = "prova_master"

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
    echoMissioni(message)

# INVIO DELLA MAPPA DI CIASCUN BIOMA
@app.on_message(filters.command(["foresta"]) | filters.command(["vulcano"]) | filters.command(["deserto"]) | filters.command(["ghiacciaio"]) | filters.command(["centro"]))
def bioma(_, message):
    mappaBioma(app, message)

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
    if  message.from_user.username == "prova_master":
        #accesso permesso al master
        listaComandiMaster(message)

        # Gestire i danni tramite una semplice FUNZIONE
        # /danno [player] [danno]
        @app.on_message(filters.command(["danno"]))
        def danno(_, message):
            if message.from_user.username == "prova_master":
                gestisciDanno(message)

        # Modificare l'armatura
        # /armatura [player] [+/- modif]
        @app.on_message(filters.command(["armatura"]))
        def armatura(_, message):
            if message.from_user.username == "prova_master":
                modArmatura(message)
        
        # COMPLETARE LA MISSIONE
        # /missione [idMissione] [attiva/disattiva |otp]
        @app.on_message(filters.command(["missione"]))
        def completa(_, message):
            if message.from_user.username == "prova_master":
                modMissione(message)
        
        # SETTARE I DATI DI UN GIOCATORE TUTTI ASSIEME
        # /set [player] [life] [forza] [agilita] [astuzia] [classe]
        @app.on_message(filters.command(["set"]))
        def setPg(_, message):
            if message.from_user.username == "prova_master":
                message.reply_text("Dentro")
                settaGiocatore(message)
            else:
                message.reply_text("Fuori!")

        # MODIFICA LE STATISTICHE DEL GIOCATORE
        # /stat [player] [stat] [+/- modifca]
        @app.on_message(filters.command(["stat"]))
        def stat(_, message):
            if message.from_user.username == "prova_master":
                modificaStatGiocatore(message)

        # VISUALIZZARE L'INVENTARIO DI UN GIOCATORE DEGLI HG
        @app.on_message(filters.command(["info"]))
        def inventarioMaster(_,message):
            if message.from_user.username == "prova_master":
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

        # TOGLIERE OGGETTI DALL'INVENTARIO DI UN GIOCAOTRE PRECISO
        # /togliOggetto [giocatore] [oggetto]
        @app.on_message(filters.command(["levaOggetto"]))
        def levaOggetto(_, message):
            if message.from_user.username == "prova_master":
                riduciInventario(message, app)

        # INSERIRE NUOVI OGGETTI NELL'INVENTARIO DI UN GIOCATORE
        # /nuovoOggetto [giocatore] [oggetto] [descr|opt]
        @app.on_message(filters.command(["mettiOggetto"]))
        def mettiOggetto(_, message):
            if message.from_user.username == "prova_master":
                inserisciOggetto(message)

    else:
        #accesso negato al NON master
        message.reply_text("Hey furbetto, a questa edizione il master non sei te!")


app.run()
