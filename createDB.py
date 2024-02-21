import sqlite3

#creazione della connessione al db
conn = sqlite3.connect('hg.db')
#creazione del cursore
c = conn.cursor()

# ********************************* TABELLA GIOCATORE ************************************
c.execute('''CREATE TABLE giocatore (
                ID_Giocatore INTEGER PRIMARY KEY,
                nome CHAR(20) NOT NULL,
                vita INT(2),
                forza INT(2),
                agilita INT(2),
                astuzia INT(2),
                classe CHAR(20),
                armatura INTEGER(3) DEFAULT(0)
            )''')

#POPOLARE TABELLA GIOCATORE
nomi_giocatori = ["merlock", "riccio", "edo", "nico lello", "carl", "citta", "alex", "veve", "triani", "paolo", "pedro", "gabry", "nico", "marco", "andrei", "fede"]

#inserimento di tutti i giocatori della tabella
for nome_giocatore in nomi_giocatori:
    c.execute("INSERT INTO giocatore (nome) VALUES (?)", [nome_giocatore])

# ********************************** TABELLA BIOMA ***************************************
c.execute('''CREATE TABLE bioma (
                ID_Bioma INTEGER PRIMARY KEY,
                nome CHAR(20) NOT NULL,
                foto BLOB
            )''')

#POPOLARE TABELLA BIOMA
biomi = ["foresta", "vulcano", "deserto", "ghiacciaio", "centro"]

#inserimento dei biomi
for bioma in biomi:
    c.execute("INSERT INTO bioma (nome) VALUES (?)", [bioma])

# ********************************** TABELLA MISSIONE (COLLEGATA A BIOMA) **************************
c.execute('''CREATE TABLE missione (
                ID_Missione INTEGER PRIMARY KEY,
                nome CHAR(70) NOT NULL,
                descrizione CHAR(100) NOT NULL,
                ricompensa CHAR(70) NOT NULL,
                finita INTEGER(1) DEFAULT(0),
                FK_Bioma INTEGER NOT NULL,
                FOREIGN KEY(FK_Bioma) REFERENCES bioma(ID_Bioma)
                ON DELETE CASCADE ON UPDATE CASCADE
            )''')

#POPOLARE TABELLA MISSIONI
missioni = [["Fungomanzia", 
              "Uno strano alchimista della città ti chiede di raccogliere dei funghi particolari ad ovest della foresta per creare una pozione. Raccogli 2 funghi luminescenti (usa un’azione per raccoglierli), alcuni di essi sono velenosi (50% di probabilità) e toccandoli ti faranno 1 danno e scompariranno. Torna alla città per raccogliere la ricompensa",
              "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra anello alchemico (passiva: +2 agilità, attiva: azione rapida, trasforma il bonus di un qualsiasi tuo oggetto in bonus agilità, CD 5) oppure pugnale velenoso (4+bonus agilità danni, gittata 0, passiva: infliggi 1 danno in più ai giocatori)", 1
            ],
            ["L’albero magico", 
             "Arrampicati sull’albero magico (3 movimenti per salire) e raccogli il frutto magico, dopodichè potrai decidere se scendere con 3 movimenti o lanciarti e subire 3 danni. Porta il frutto in città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra arco in legno magico (3+bonus agilità danni, gittata 1, attiva:azione rapida, per questo turno lo scatto è un’azione rapida. CD3) oppure mantello fragolino (5 armatura, passiva: ogni volta che scatti ti curi di 2 punti vita) ", 1
            ],
            ["Il nostro vino, il vino buono", 
             "Recati al villaggio ad est della foresta, recupera 3 casse di vino (un’azione per ognuna) e riportale al locandiere. ", 
             "Pozione di cura (cura 2+bonus astuzia punti vita) + botte rinforzata (5 armatura, attiva: crei un onda di vino che parte da te con raggio 1 che infligge 2+bonus agilità danni e respinge indietro i nemici di 1 quadrato. CD 4) oppure bottiglia tagliagola (4+bonus agilità danni, gittata 0, passiva: quando colpisci un nemico, fino al turno successivo se egli si allontana di almeno 1 quadrato da te subirà bonus agilità danni)", 1
            ],
            ["Metti la cera, togli la cera", 
             "Vai al dojo e addestrati con lui per 3 turni (ogni turno costa un’azione), finito il tuo addestramento potrai scegliere la tua ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra kimono zen (5 armatura, attiva: azione risposa, schivi un attacco. CD 7) oppure nunchaku letali (3+bonus agilità danni, gittata 1, passiva: quando colpisci un nemico con più vita di te infliggi 1 danno in più e ottieni un movimento bonus per questo turno)", 1
            ],
            ["Il guardiano dei cristalli", 
             "Sconfiggi la salamandra del ghiaccio (7 punti vita, sputo gelido: 1 danno, gittata 1) e porta la sua carcassa in città come prova della missione, reclamando la ricompensa.",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra lingua gelida (4+bonus astuzia danni, gittata 0, passiva: quando colpisci un nemico ottieni 1 armatura) oppure armatura di cristalli (5 armatura, passiva: subisci 1 danno in meno dalle abilità)", 4
            ],
            ["Il lago d’argento", 
             "Tuffati nel lago ghiacciato e cerca il cimelio che si troverà in una delle 4 caselle del lago. Ogni turno nel lago subirai 1 danno. Riporta il cimelio in città per riscuotere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra tunica dello stregone (5 armatura, attiva: lancia una magia casuale del mago. CD 5) oppure bacchetta d’argento (3+bonus astuzia danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco con quest’arma ti cura della metà del danno inflitto. CD 4)", 4
            ],
            ["Lo yeti addormentato", 
             "Ad ovest della città, recati nella grotta e cerca il gioiello silenziosamente (3 turni) oppure rumorosamente (istantaneo) ma Willump si sveglierà e dovrai affrontarlo (8 punti vita, 2 danni, gittata 0) recuperato il bottino torna alla città",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra pelliccia dello yeti (5 armatura, attiva: ottieni un movimento ed evochi una palla di neve gigante che colpisce il bersaglio facendo 2+bonus astuzia danni e bloccandolo sul posto, gittata 0. CD 4) oppure bracciale del letargo (passiva:+2 astuzia, le pozioni di cura ti curano di 2 punti vita in più)", 4
            ],
            ["Il negozio di magia", 
             "Gli oggetti appartengono ad una famiglia di contadini nel villaggio a nord del ghiacciaio, vai da loro e baratta un qualsiasi tuo oggetto in cambio della merce, poi torna in città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra collana della palla di fuoco (passiva: +2 astuzia, attiva: lanci una palla di fuoco che fa 3+bonus astuzia danni in un’area di raggio 1, gittata 2. CD 4) oppure scettro dell’impedimento (3+bonus astuzia danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco stordisce il bersaglio (salterà il turno). CD 7)", 4
            ],
            ["La cima della piramide", 
             "Scala la piramide (ci vorranno 3 movimenti) e pianta la bandiera con un’azione, poi scendi dalla piramide (puoi buttarti e subire 3 danni o scendere normalmente) e torna in città per riscuotere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra idolo della sfinge (passiva: +1 a tutte le statistiche, attiva: lancia una maledizione su un giocatore a tua scelta infliggendogli bonus forza + bonus astuzia + bonus agilità danni. CD 5) oppure lancia maledetta (5+bonus a scelta danni, gittata 1, passiva: quando colpisci un nemico subisci la metà dei danni inflitti, a meno che tu non lo uccidi)", 3
            ],
            ["Consegna sospetta", 
             "Consegna il pacco alla città di vulcano o alla città di ghiacciaio, poi torna alla città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + se hai scelto la città di vulcano ottieni pillola rossa (passiva: +2 forza, attiva: azione rapida, ottieni bonus a scelta armatura. CD 4); se hai scelto la città di ghiacciaio ottieni pillola blu (passiva: +2 astuzia, attiva: azione rapida, ottieni bonus astuzia punti in una caratteristica a tua scelta fino alla fine del turno. CD 4)", 3
            ],
            ["Il wurm delle sabbie", 
             "Sconfiggi il wurm (5 punti vita, morso: 2 danni, gittata 0, se non muore in un colpo richiamerà un altro wurm) e torna alla città per riscuotere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + dente del wurm (4+bonus a scelta danni, gittata 0, passiva: i tuoi attacchi marchiano il bersaglio per 1 turno, infliggi 1 danno in più ai nemici marchiati) oppure armatura di sabbiapietra (5 armatura, attiva: azione rapida, ottieni 5 armatura provvisoria fino all’inizio del tuo prossimo turno. CD 4)", 3
            ],
            ["Pesce! Pesce! Pesce!", 
             "Dirigiti al lago e prova a pescare il pesce (1 azione, 2 volte su 3 il pesce scappa) e riporta il pesce in città per ricevere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra torcia magica (passiva: +1 a tutte le statistiche. Attiva: se hai vista limitata puoi accendere la torcia per vedere normalmente, ma anche gli altri ti vedranno. Nessun CD) oppure canna da pesca magica (3+bonus a scelta danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco può avvicinare o allontanare di 1 quadrato il nemico. CD 4)", 3
            ],
            ["Uga buga tonga banga", 
             "Raggiungi il villaggio della tribù e parla con ogni capo tribù (al costo di un’azione) che si trova su ogni totem del villaggio, torna alla città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra lancia tribale (4+bonus forza danni, gittata 0, passiva: puoi aumentare la gittata di quest’arma di 1 ma farà 1 danno in meno) oppure scudo totem (5 armatura, attiva: azione rapida, ottieni bonus forza armatura, se ti trovi nel vulcano ottieni invece 2+bonus forza armatura. CD 5) ", 2
            ],
            ["La miniera della morte", 
             "Raggiungi la miniera e sconfiggi 2 banditi (4 punti vita, pugnale: 2 danni, gittata 0) e torna in città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta bandana rossa (5 armatura, passiva: ogni volta che ottieni armatura ottieni anche un movimento bonus) oppure pugnale affilato (4+bonus forza danni, gittata 0, passiva: se hai armatura infliggi un danno in più) ", 2
            ],
            ["Il collezionista", 
             "Puoi raccogliere un sacchetto della magica sabbia dorata (recuperabile allo spawn D) oppure un ramo dell’albero secolare (recuperabile allo spawn B); scegli quale manufatto recuperare e torna dal collezionista una volta ottenuto per la ricompensa.",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + Se hai scelto spawn B ottieni arcoscudo (5 armatura, attiva: azione rapida, spari un dardo di fuoco che infligge 3 danni, gittata 1. CD 3); se hai scelto spawn D ottieni spadone delle sabbie (4+ bonus forza danni, gittata 0, attiva: puoi parare un colpo con gittata di 1 o superiore; ricarica 3 turni)", 2
            ],
            ["Ghostbusters", 
             "Raggiungi il castello a nord del vulcano, una volta lì puoi decidere se indagare e basta (un turno) oppure provare anche a disinfestare il castello affrontando il fantasma del tiranno (8 punti vita, sciabola: 3 danni, gittata 0) in tal caso puoi ottenere la sua arma",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + armatura degli acchiappafantasmi (8 armatura), se hai sconfitto il fantasma ottieni anche sciabola del tiranno (4+bonus forza danni, gittata 0, azione rapida: ottieni armatura pari alla metà del danno fatto con il tuo prossimo attacco. CD 5)", 2
            ],
            ["Il dipinto", 
             "Attraversa tutte e 9 le caselle del centro, torna in città per raccogliere la ricompensa",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + a scelta tra pennello magico (attiva: azione rapida, cambia il tuo aspetto in quello di un altro giocatore. CD 3) oppure autografo dell’artista (passiva: puoi scambiare questo oggetto ad una città per ricevere in cambio un qualsiasi altro oggetto di una missione di fase 1 di quel bioma)", 5
            ],
            ["Il mercante delle meraviglie", 
             "Per avere qualcosa da lui devi visitare per almeno un turno ogni bioma e tornare da lui",
             "Pozione di cura (cura 2+bonus astuzia punti vita) + occhiali della verità (attiva: azione rapida, puoi sapere quanti punti vita ha un nemico che puoi vedere. CD 5) oppure lampada magica (attiva: azione rapida, sfregando la lampada puoi entrarci dentro per massimo 3 turni (decidi te quando uscire, utilizzando un’azione o al termine dei 3 turni), mentre sei dentro la lampada sei immune a qualsiasi cosa e ti curi di 3+bonus a scelta punti vita a turno, ma non potrai fare nessuna azione. CD 7) ", 5
            ]
        ]


for missione in missioni:
    c.execute("INSERT INTO missione (nome, descrizione, ricompensa, FK_Bioma) VALUES (?,?,?,?)", [missione[0], missione[1], missione[2], missione[3]])


#TABELLA OGGETTO (COLLEGATO A GIOCATORE)
c.execute('''CREATE TABLE oggetto (
                ID_Oggetto INTEGER PRIMARY KEY,
                nome CHAR(20) NOT NULL,
                descrizione CHAR(200),
                quantita INTEGER DEFAULT(1),
                FK_Giocatore CHAR(20) NOT NULL,
                FOREIGN KEY(FK_Giocatore) REFERENCES giocatore(ID_Giocatore)
                ON DELETE CASCADE ON UPDATE CASCADE
            )''')

conn.commit()
