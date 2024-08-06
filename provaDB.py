import sqlite3

#creazione della connessione al db
conn = sqlite3.connect('hg.db')
#creazione del cursore
c = conn.cursor()

#esegue la query per visualizzare i giocatori
c.execute("SELECT * FROM giocatore")

#ritorna le righe della tabella ottenute
rows = c.fetchall()

print("\nECCO I GIOCAORI PRONTI")
#visualizza tutte le righe
for row in rows:
    print(row[1])

c.execute("SELECT * FROM oggetto")
#ritorna le righe
rows = c.fetchall()

print("\n ECCO TUTTI GLI OGGETTI")
#visualizzare
for row in rows:
    print(row[1])

c.execute("SELECT * FROM bioma")
rows = c.fetchall()

print("\n ECCO TUTTI I BIOMI")
#visualizza
for row in rows:
    print(row[1])

c.execute("SELECT * FROM missione")
rows = c.fetchall()

print("\n ECCO TUTTE LE MISSIONI")
#visualizza
for row in rows:
    print(row)

giocatore = input("Di quale giocatore vuoi conoscere le armi? ")

c.execute('''SELECT *
             FROM oggetto O, giocatore G
             WHERE O.FK_Giocatore = G.ID_Giocatore AND G.nome = ?''', [giocatore])

rows = c.fetchall()
#visualizzazione
print("OGGETTI DI "+giocatore)
for row in rows:
    print(row[1]+": "+row[2])

conn.commit()
