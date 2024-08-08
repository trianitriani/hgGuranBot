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
                armatura INTEGER(3) DEFAULT(0),
                FK_Girone INTEGER NOT NULL
            )''')

#POPOLARE TABELLA GIOCATORE
nomi_giocatori = []

#inserimento di tutti i giocatori della tabella
for nome_giocatore in nomi_giocatori:
    if nome_giocatore == "prova1":
        girone = 1
    elif nome_giocatore == "prova2":
        girone = 2
    elif nome_giocatore == "prova3":
        girone = 3
    else:
        girone = 0
    c.execute("INSERT INTO giocatore (nome, FK_Girone) VALUES (?, ?)", [nome_giocatore, girone])

# ********************************** TABELLA BIOMA ***************************************
c.execute('''CREATE TABLE bioma (
                ID_Bioma INTEGER PRIMARY KEY,
                nome CHAR(20) NOT NULL,
                foto BLOB
            )''')

# ******************************** TABELLA ATTIVE ****************************************
# le attive sono le abilità di oggetti o delle classi, e hanno un cd
c.execute('''CREATE TABLE attiva (
                ID_Attiva INTEGER PRIMARY KEY,
                nome CHAR(100) NOT NULL,
                cd INTEGER NOT NULL,
                FK_Giocatore INTEGER NOT NULL,
                FOREIGN KEY(FK_Giocatore) REFERENCES giocatore(ID_Giocatore)
                ON DELETE CASCADE ON UPDATE CASCADE
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
                attiva INTEGER(1) DEFAULT(0),
                FK_Girone INTEGER NOT NULL,
                FK_Bioma INTEGER NOT NULL,
                FOREIGN KEY(FK_Bioma) REFERENCES bioma(ID_Bioma)
                ON DELETE CASCADE ON UPDATE CASCADE
            )''')

#POPOLARE TABELLA MISSIONI
missioni = [

            # Missioni Foresta
            ["Infestazione",
              "Qualcosa sta facendo appassire gli alberi di foresta, recati sul posto e indaga sull'accaduto. Sconfiggi 3 zombie putridi nella foresta marcescente (3 punti vita, artiglio: 1 danno, gittata 0) e torna alla città per raccogliere la ricompensa",
              "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra cerbottana infestata (3+bonus agilità danni, gittata 1, passiva: se un nemico ti colpisce nello stesso turno in cui lo hai colpito con quest’arma subisce bonus agilità danni) oppure corpetto putrido (5+bonus forza armatura, attiva: azione rapida, evoca uno zombie putrido (3 punti vita, 1 danno). Ricarica 2) ",
              1
            ],
            ["Fungomanzia",
              "Uno strano alchimista della città ti chiede di raccogliere dei funghi particolari ad ovest della foresta per creare una pozione. Raccogli 2 funghi luminescenti (usa un’azione per raccoglierli), alcuni di essi sono velenosi (25% di probabilità) e toccandoli ti faranno 1 danno e scompariranno. Torna alla città per raccogliere la ricompensa",
              "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra turbante alchemico (5+bonus forza armatura, attiva: azione rapida, trasforma il bonus di un qualsiasi tuo oggetto in bonus agilità. Ricarica 4) oppure pugnale velenoso (5+bonus agilità danni, gittata 0, passiva: infliggi 1 danno in più ai giocatori)",
              1
            ],
            ["L’albero magico",
             "Arrampicati sull’ albero magico (3 movimenti per salire) e raccogli il frutto magico, dopodichè potrai decidere se scendere con 3 movimenti o lanciarti, come azione rapida, e subire 1 danno per ogni movimento mancante. Porta il frutto in città per raccogliere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra arco in legno magico (3+bonus agilità danni, gittata 1, attiva: azione rapida, per questo turno lo scatto è un’azione rapida. Ricarica 2) oppure mantello fragolino (5+bonus forza armatura, passiva: ogni volta che scatti ti curi di 2 punti vita)",
             1
            ],
            ["Il nostro vino, il vino buono",
             "Recati al villaggio contadino ad est della foresta, recupera una cassa di vino utilizzando un’azione e riportala al locandiere in città. Finchè trasporti la cassa di vino non potrai scattare",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + botte rinforzata (5+bonus forza armatura, attiva: crei un onda di vino che parte da te con raggio 1 che infligge 2+bonus agilità danni e respinge indietro i nemici di 1 quadrato. Ricarica 3) oppure bottiglia tagliagola (5+bonus agilità danni, gittata 0, passiva: quando colpisci un nemico, fino al turno successivo se egli si allontana di almeno 1 quadrato da te subirà bonus agilità danni)",
             1
            ],
            ["Metti la cera, togli la cera",
             "Vai al dojo nascosto e addestrati con il maestro per 2 turni (ogni turno costa un’azione), finito il tuo addestramento potrai tornare in città e raccogliere la ricompensa.",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra kimono zen (5+bonus forza armatura, attiva: azione rapida, dimezzi il danno del prossimo attacco o abilità nemica. Ricarica 3) oppure nunchaku letali (3+bonus agilità danni, gittata 1, passiva: quando colpisci un nemico con più vita di te infliggi 1 danno in più e ottieni un movimento bonus per questo turno)",
             1
            ],
            ["La caccia è aperta",
             "Due nobili rivali della città di foresta ti chiedono di cacciare per loro due bestie pericolose.. Il primo ti chiede la testa del puma di montagna che si trova alle miniere della morte (13 di vita, 3 danni, gittata 0); l’altro chiede la testa dell’aquila di ghiaccio che dimora sopra il lago d’argento (9 di vita, 5 danni; gittata 1), torna in città con una delle due teste per riscuotere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + se hai sconfitto il puma ottieni pelliccia del predatore (8+bonus forza armatura, attiva: azione rapida: il tuo prossimo attacco in questo turno fa 1 danno in più e marchia il bersaglio, permettendoti di conoscere la sua posizione per 2 turni. Ricarica 2) oppure se hai sconfitto l’aquila ottieni balestra del predatore (3+bonus agilità danni, gittata 2, attiva: azione rapida, il tuo prossimo attacco ti fa scambiare di posizione con il nemico colpito. Ricarica 4)",
             1
            ],
            ["Jack sto volando!",
             "Raggiungi l’ albero magico a nord est di foresta, sconfiggi Jack lo squartatore (12 punti vita, 6 danni, gittata 0) e riporta la sua testa in città per raccogliere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra mantello da ricercato (8+bonus forza armatura, attiva: azione rapida, ottieni 3+bonus agilità armatura e bonus agilità movimenti per questo turno ma la tua posizione viene rilevata da tutti i giocatori. Ricarica 3) oppure pugnali da lancio assassini (4+bonus agilità danni, gittata 1, passiva: se colpisci un nemico e lo lasci con 3 punti vita o meno, lo uccidi)",
             1
            ],
            ["Arma scoppiettante",
             "Raccogli a scelta (al costo di un’azione) un cristallo ai cristalli del fuoco, una manciata di limo nel lago dell’oasi o una borraccia di acqua della fonte nel lago d’argento e porta il materiale al cacciatore nella città di foresta per ricevere la ricompensa.",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + se hai portato la pietra vulcanica fucile scoppiettante (4+bonus agilità danni, gittata 1, attiva: azione rapida, ottieni un movimento, il tuo prossimo attacco con quest’arma in questo turno ottiene 1 in più di gittata. Ricarica 4), se hai portato la manciata di limo ottieni polvere da sparo magica (passiva: i tuoi attacchi saranno sempre ad area ed infliggeranno 2 danni in più), se hai portato la borraccia d’acqua ottieni giubbotto rifocillante (8+bonus forza armatura, attiva: azione rapida, ti curi di 4+bonus agilità punti vita. Ricarica 3)",
             1
            ],

            # Missioni di Ghiacciaio
            ["Il villaggio dei regali",
             "Apri i regali di Babbo Guran nel villaggio natalizio per trovare la lettera (aprire un regalo costerà un’azione, il 50% dei regali sono vuoti), torna alla città per raccogliere la ricompensa",
             "Pozione di cura piccola(consumabile: cura 2+bonus astuzia punti vita) + a scelta tra spara regali (3+bonus astuzia danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco con quest’arma in questo turno spara un regalo esplosivo che fa bonus astuzia danni in più ed è ad area 1. Ricarica 3) oppure berretto natalizio (5+bonus forza armatura, passiva: le tue abilità fanno 1 danno in più)",
             4
            ],
            ["Il guardiano dei cristalli",
             "Sconfiggi la salamandra del ghiaccio ai cristalli del ghiaccio (7 punti vita, sputo gelido: 1 danno, gittata 1) e porta la sua carcassa in città come prova della missione, reclamando la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra lingua gelida (5+bonus astuzia danni, gittata 0, passiva: quando colpisci un nemico ottieni 1 armatura) oppure armatura di cristalli (5+bonus forza armatura, passiva: subisci 1 danno in meno dalle abilità)",
             4
            ],
            ["Il lago d’argento",
             "Tuffati nel lago d’argento e cerca il cimelio che si troverà in una delle 4 caselle del lago. Ogni turno nel lago subirai 1 danno. Riporta il cimelio in città per riscuotere la ricompensa.",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra tunica dello stregone (5+bonus forza armatura, attiva: azione rapida, ottieni una magia casuale del mago, puoi usarla fino alla fine del giorno. Ricarica 3) oppure bacchetta d’argento (3+bonus astuzia danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco con quest’arma ti cura della metà del danno inflitto. Ricarica 3)",
             4
            ],
            ["Lo yeti addormentato",
             "Ad ovest della città, recati nella tana dello yeti e cerca il gioiello silenziosamente (3 turni) oppure rumorosamente (istantaneo) ma Willump si sveglierà e dovrai affrontarlo (8 punti vita, 2 danni, gittata 0) recuperato il bottino torna alla città",
             "pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra palla di neve più grande del mondo (3+bonus astuzia danni, gittata 1, attiva: ottieni un movimento ed evochi una palla di neve gigante che colpisce il bersaglio facendo 2+bonus astuzia danni e bloccandolo sul posto, gittata 0. Ricarica 3) oppure bracciale del letargo (5+bonus forza armatura, passiva: le pozioni di cura ti curano di 2 punti vita in più)",
             4
            ],
            ["Il negozio di magia",
             "Gli oggetti appartengono ad una famiglia di contadini nell’ approdo invernale a nord del ghiacciaio, vai da loro e baratta un qualsiasi tuo oggetto in cambio della merce, poi torna in città per raccogliere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra spallacci della palla di fuoco (5+bonus forza armatura, attiva: lanci una palla di fuoco che fa 3+bonus astuzia danni in un’area di raggio 1, gittata 2. Ricarica 3) oppure scettro dell’impedimento (3+bonus astuzia danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco rende incapacitato il nemico. Ricarica 4)",
             4
            ],
            ["Al ladro!!",
             "I ladri si sono divisi, uno si è nascosto al villaggio contadino e uno all’osservatorio, non perdere tempo, insegui uno dei due, sconfiggilo (12 punti vita, 4 danni, gittata 1), recupera la refurtiva e riportala alla città per ottenere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + se hai inseguito il ladro a foresta ottieni bastone dell’evocazione bestiale (4+bonus astuzia danni, gittata 1, attiva: evoca un lupo che combatterà per te, ha 8 punti vita e farà 4 danni con gittata 0. Ricarica 9); se hai inseguito il ladro a deserto ottieni schinieri della tempesta di sabbia (8+bonus forza armatura, attiva: crei una tempesta di sabbia centrata su di te con raggio 1 quadrato, tutti i nemici al suo interno subiscono 2+bonus astuzia danni a turno e hanno vista limitata, dura bonus astuzia turni. Ricarica 4)",
             4
            ],
            ["Il grinch",
             "Dirigiti al villaggio natalizio e sconfiggi il grinch (12 punti vita, graffio: 4 danni, gittata 0, passiva: quando muore crea una nube verde che fa 5 danni) e torna alla città di ghiacciaio per riscuotere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra maschera del grinch (8+bonus forza armatura, attiva: azione rapida, spaventi un nemico, il prossimo turno dovrà usare l’azione di movimento per allontanarsi da te. Ricarica 3) oppure bastone del vischio (6+bonus astuzia danni, gittata 0, attiva: il tuo prossimo attacco con quest’arma in questo turno provoca affascinamento sul nemico. Ricarica 3)",
             4
            ],
            ["La prova dell’arcimago",
             "Vai dal mago alla cascata e scegli una delle sue prove: Raccogli il loto dorato (si trova nel lago dell’oasi, usa un’azione per raccoglierlo, 50% di probabilità di raccogliere un loto normale) Sconfiggi l’elementale di fuoco (si trova ai cristalli del fuoco, 10 punti vita, 5 danni, gittata 1) Corri come il vento (raggiungi l’ infestazione fungina e torna alla città di ghiacciaio in meno di un giorno, se non riuscirai in tempo la missione si annullerà) Torna in città per ricevere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + se hai scelto la prova di deserto ottieni loto dorato (attiva: azione rapida, ti curi di 2+bonus astuzia punti vita e ottieni 2+bonus astuzia armatura. Ricarica 4), se hai scelto la prova di vulcano ottieni scettro elementale (4+bonus astuzia danni, gittata 1, passiva: ottieni l’incantesimo del mago palla di fuoco permanentemente), se hai scelto la prova di foresta ottieni stivali del vento (8+bonus forza armatura, attiva: azione rapida, ottieni bonus astuzia movimenti per questo turno. Ricarica 2)",
             4
            ],

            # Missioni Deserto
            ["Voragine",
             "Entra nel primo livello della voragine (1 movimento in profondità) e sconfiggi il cucciolo di verme del deserto (6 punti vita, morso: 2 danni, gittata 0) e torna alla città per raccogliere la ricompensa",
             "Pozione di cura piccola(consumabile: cura 2+bonus astuzia punti vita) + a scelta tra badile rinforzato (5+bonus a scelta danni, gittata 0, attiva: azione rapida, il tuo prossimo attacco con quest’arma in questo turno immobilizza l’avversario. Ricarica 2) oppure elmo con lente da ricercatore (5+bonus forza armatura, attiva: azione rapida, scopri la posizione di un giocatore a tua scelta. Ricarica 4) ",
             3
            ],
            ["La cima della piramide",
             "Scala la piramide (ci vorranno 3 movimenti) e pianta la bandiera con un’azione, poi scendi dalla piramide (puoi buttarti e subire 3 danni o scendere normalmente) e torna in città per riscuotere la ricompensa",
             "Pozione di cura piccola(consumabile: cura 2+bonus astuzia punti vita) + a scelta tra nemes della sfinge (5+bonus forza armatura, attiva: lancia una maledizione su un giocatore a tua scelta infliggendogli bonus forza + bonus astuzia + bonus agilità danni. Ricarica 4) oppure lancia maledetta (3+bonus a scelta danni, gittata 1, passiva: quando colpisci un nemico infliggi 2 danni in più, ma se lo uccidi subisci la metà dei danni inflitti con quell’attacco)",
             3
            ],
            ["Consegna sospetta",
             "Consegna il pacco alla città di vulcano (spawn E) o alla città di ghiacciaio (spawn C), poi torna alla città per raccogliere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + se hai scelto la città di vulcano ottieni kukri dell’assassino (5+bonus a scelta danni, gittata 0, attiva: azione rapida, il tuo prossimo attacco con quest’arma in questo turno provoca sanguinamento sul nemico. Ricarica 2); se hai scelto la città di ghiacciaio ottieni corpetto spinato (5+bonus forza armatura, passiva: quando un nemico ti colpisce con un attacco subisce 2 danni)",
             3
            ],
            ["Il wurm delle sabbie",
             "Sconfiggi il wurm alle rovine antiche (5 punti vita, morso: 2 danni, gittata 0, se non muore in un colpo richiamerà un altro wurm) e torna alla città per riscuotere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + dente del wurm (5+bonus a scelta danni, gittata 0, passiva: i tuoi attacchi marchiano il bersaglio per 1 turno, conosci la posizione e infliggi 1 danno in più ai nemici marchiati) oppure armatura di sabbiapietra (5+bonus forza armatura, attiva: azione rapida, ottieni 3+bonus a scelta armatura provvisoria fino all’inizio del tuo prossimo turno. Ricarica 3)",
             3
            ],
            ["Pesce! Pesce! Pesce!",
             "Dirigiti al lago e prova a pescare il pesce (1 azione, 2 volte su 3 il pesce scappa) e riporta il pesce in città per ricevere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra berretto da pescatore con torcia (5+bonus forza armatura, attiva: azione rapida, se è notte puoi accendere la torcia e vedere normalmente ma anche i nemici ti vedranno fino alla fine del turno. Ricarica 0) oppure canna da pesca magica (3+bonus a scelta danni, gittata 1, attiva: azione rapida, il tuo prossimo attacco con quest’arma in questo turno può avvicinare o allontanare di 1 quadrato il nemico. Ricarica 3)",
             3
            ],
            ["Mezzogiorno di fuoco",
             "Sconfiggi il leggendario pistolero a spawn D per raccogliere la ricompensa (20 punti vita: 7 danni, gittata 1, aspetterà 2 turni prima di attaccare)",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra revolver d’oro (4+bonus a scelta danni, gittata 1, attiva: azione rapida, puoi sparare un secondo colpo in questo turno, farà 2 danni in meno e dovrai utilizzare un’azione per ricaricare per riutilizzare quest’arma. Ricarica 3) oppure cappello da cow-boy (8+bonus forza armatura, attiva: azione rapida, provochi il nemico, il suo prossimo attacco farà 3 danni in meno. Ricarica 3 )",
             3
            ],
            ["L’invasione di mummie",
             "Raggiungi la piramide e sconfiggi le 4 mummie al suo interno (3 punti vita, 2 danni, gittata 0, passiva: la prima volta che muoiono hanno il 50% di resuscitare) e torna alla città per ricevere la ricompensa ",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra bende della mummia (8+bonus forza armatura, passiva: dimezza i tuoi punti vita attuali, ma la prima volta che muori torni in vita con metà dei tuoi punti vita totali) oppure scettro maledetto (4+bonus a scelta danni, gittata 1, attiva: azione rapida, maledici un giocatore che riesci a vedere, per il prossimo turno tutti i danni che ricevi da lui li riceve anche quel giocatore. Ricarica 5)",
             3
            ],
            ["In fondo alla voragine",
             "Arriva in fondo alla voragine (3 movimenti) e sconfiggi il verme primordiale (15 punti vita, morso: 3 danni, gittata 0) poi torna alla città per riscuotere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra muta del verme primordiale (8+bonus forza armatura, passiva: hai un verme che ti segue con 8 punti vita che fa 3 danni con gittata 0, ogni giorno cresce aumentando di 2 i punti vita e i danni, se muore torna dopo un giorno con le statistiche originali) oppure scacciavermi (6+bonus a scelta danni, gittata 0, passiva: fa il doppio dei danni contro i nemici non giocanti) ",
             3
            ],

            # Missioni Vulcano
            ["Uga buga tonga banga",
             "Raggiungi il villaggio della tribù e parla con ogni capo tribù (al costo di un’azione) che si trova su ogni totem del villaggio, torna alla città per raccogliere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra lancia tribale (5+bonus forza danni, gittata 0, passiva: puoi aumentare la gittata di quest’arma di 1 ma farà 1 danno in meno) oppure scudo totem (5+bonus forza armatura, attiva: azione rapida, ottieni bonus forza armatura, se ti trovi nel vulcano ottieni invece 2+bonus forza armatura. Ricarica 4) ",
             2
            ],
            [
             "La miniera della morte",
             "Raggiungi la miniera e sconfiggi 2 banditi (3 punti vita, pugnale: 2 danni, gittata 0) e torna in città per raccogliere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra bandana rossa (5+bonus forza armatura, passiva: ogni volta che ottieni armatura ottieni anche un movimento bonus) oppure pugnale affilato (5+bonus forza danni, gittata 0, passiva: se hai armatura infliggi un danno in più)",
             2
            ],
            [
             "La spaccatura",
             "Raggiungi la spaccatura, calati dentro ad essa (3 movimenti), raccogli un frammento di meteorite e riportalo in città per ottenere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra corazza gravitazionale (5+bonus forza armatura, attiva: azione rapida, per i prossimi bonus forza turni sei inarrestabile. Ricarica 3) oppure piccoli meteoriti da lancio (3+bonus forza danni, gittata 1, attiva: azione rapida, puoi decidere se il tuo prossimo attacco con quest’arma in questo turno immobilizza o incapacita il bersaglio. Ricarica 5)",
             2
            ],
            [
             "Il collezionista",
             "Puoi raccogliere un sacchetto della magica sabbia dorata (recuperabile allo spawn D) oppure un ramo dell’albero secolare (recuperabile allo spawn B); scegli quale manufatto recuperare e torna dal collezionista una volta ottenuto per la ricompensa.",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + se hai scelto spawn B ottieni arcoscudo di fuoco (5+bonus forza armatura, attiva: azione rapida,  spari un dardo di fuoco che infligge bonus forza danni, gittata 1. Ricarica 2); se hai scelto spawn D ottieni spadone delle sabbie (5+bonus forza danni, gittata 0, attiva: azione rapida, il prossimo attacco con gittata di 1 o superiore viene parato. Ricarica 4)",
             2
            ],
            ["Ghostbusters",
             "Raggiungi il castello infestato a nord del vulcano, una volta lì dovrai disinfestare il castello affrontando il fantasma del tiranno (8 punti vita, sciabola: 1 danni, gittata 0), torna in città per ottenere la ricompensa",
             "Pozione di cura piccola (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra armatura degli acchiappafantasmi (5+bonus forza armatura, attiva: azione rapida, tutti i nemici nel raggio di 3 quadrati da te diventano confusi per il prossimo turno. Ricarica 3), oppure sciabola del tiranno (5+bonus forza danni, gittata 0, azione rapida: ottieni armatura pari alla metà del danno fatto con il tuo prossimo attacco in questo turno con quest’arma. Ricarica 4)",
             2
            ],
            ["Il gemmologo",
             "Recati ai cristalli del fuoco e recupera un campione di cristallo sconfiggendo 2 salamandre di fuoco (7 di vita, 3 danni; gittata 0) recuperato il campione riportalo al gemmologo",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra spada di rubino (6+bonus forza danni, gittata 0, attiva: azione rapida, il tuo prossimo attacco con quest’arma in questo turno infligge 5 danni in più se il nemico ha più armatura di te. Ricarica 4) oppure scudo di zaffiro (8+bonus forza armatura, passiva: quando un nemico nel raggio di 2 quadrati da te ottiene armatura grazie ad un’abilità, ottieni anche te lo stesso ammontare di armatura)",
             2
            ],
            ["L’arma perfetta",
             "Raccogli ferro nanico sconfiggendo il re dei nani nella grotta del vulcano (10 vita, martello: 3 danni, gittata 0) e liane elfiche del re degli elfi all’albero magico (8 vita, arco: 2 danni, gittata 1) poi torna in città per ricevere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra spaccacrani nanico (6+bonus forza danni, gittata 0, attiva: carichi un nemico a 1 quadrato di distanza, facendo i danni dell’arma e immobilizzandolo) oppure veste del grande forgiatore (8+bonus forza armatura, passiva: finchè hai armatura i tuoi attacchi infliggono 2 danni in più)",
             2
            ],
            ["Il saggio delle tartarughe",
             "Vai in mezzo alle montagne e cercalo, il saggio può trovarsi in qualsiasi quadrato con montagne. Dopo ogni 3 quadrati attraversati per cercarlo ti sarà fornito un indizio. Torna alla città per raccogliere la ricompensa",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra bastone allungabile (6+bonus forza danni, gittata 0, passiva: puoi aumentare a piacimento la gittata degli attacchi con quest’arma, ma ogni quadrato in più farà 1 danno in meno) oppure guscio di tartaruga (20+bonus forza armatura, passiva: non puoi scattare)",
             2
            ],

            # Missioni Centro
            [
             "Il dipinto",
             "Attraversa tutte e 9 le caselle del centro, torna in città per raccogliere la ricompensa",
             "Pozione di cura (consumabile: cura 2+bonus astuzia punti vita) + a scelta tra pennello magico (attiva: azione rapida, cambia il tuo aspetto in quello di un altro giocatore. Ricarica 2) oppure autografo dell’artista (passiva: puoi scambiare questo oggetto ad una città per ricevere in cambio un qualsiasi altro oggetto di una missione presente in questa edizione di fase 1 di quel bioma)",
             5
            ],
            [
             "Il mercante delle meraviglie",
             "Per avere qualcosa da lui devi visitare per almeno un turno ogni bioma e tornare da lui",
             "Pozione di cura (consumabile: cura 2+bonus astuzia punti vita) + occhiali della verità (attiva: azione rapida, puoi sapere quanti punti vita o armatura ha un nemico che puoi vedere. Ricarica 4) oppure lampada magica (attiva: sfregando la lampada puoi entrarci dentro per massimo 3 turni (decidi te quando uscire, utilizzando un’azione o al termine dei 3 turni), mentre sei dentro la lampada sei immune e inarrestabile, ti curi di 3 punti vita a turno, ma non potrai fare nessuna azione. Ricarica 7)",
             5
            ],
            ["Il monolite",
             "Segui le indicazioni del monolite che saranno: raggiungi una città casuale, infliggi 5 danni ad un giocatore e torna al centro dove dovrai sacrificare 5 punti vita.",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra frammento del monolite (passiva: all’inizio di ogni turno il monolite ti darà un’informazione utile casuale che può essere vita, armatura, posizione o arma con più danno di un giocatore casuale) oppure dna alieno (consumabile: ottieni permanentemente le abilità dell’alieno ma perdi la tua abilità passiva e attiva: Evoluzione (passiva): ogni volta che utilizzi un’abilità aumenta il suo danno di 1 permanentemente. Falciata (attiva): azione rapida, infliggi 1 danno ad un nemico, gittata 1. Assalto (attiva) : azione rapida, balzi di 1 quadrato, infiggi 1 danni a tutti i nemici su quel quadrato. Ricarica 2. Nube (attiva): azione rapida, infliggi 1 danni a tutti i nemici nel raggio di 1 quadrato, poi diventi invisibile fino alla fine del tuo prossimo turno. Ricarica 2)",
             5
            ],
            ["Lo spirito del barone",
             "Sconfiggi lo spirito del Barone al centro della mappa (15 punti vita, tentacolo: 3 danni, gittata 1) e torna in città per riscuotere la ricompensa.",
             "Pozione di cura media (consumabile: cura 4+bonus astuzia punti vita) + a scelta tra piuma di fenice (consumabile: la prima volta che muori torni in vita con metà dei tuoi punti vita totali e sei immune fino all’inizio del tuo prossimo turno) oppure effige del Barone (consumabile: ottieni permanentemente le abilità del barone ma non potrai più uscire del centro: Simbiosi con l’isola (passiva): puoi attaccare un nemico a qualsiasi gittata ma farai 1 danno in meno per ogni quadrato di gittata in più. Scudo d’ombra (attiva): azione rapida, ottieni 3+bonus a scelta armatura, affascini tutti i nemici nel raggio di 1 quadrato da te. Ricarica 3. Tentacolo avvinghiante (attiva): azione rapida, il tuo prossimo attacco infligge bonus a scelta danni in più, trascina il bersaglio verso di te di bonus a scelta quadrati e lo immobilizza. Ricarica 3)",
             5
            ],
        ]

# Inserire tutte le missioni per tutti i gironi
for missione in missioni:
    for i in range(3):
        c.execute("INSERT INTO missione (nome, descrizione, ricompensa, FK_Bioma, FK_Girone) VALUES (?,?,?,?,?)", [missione[0], missione[1], missione[2], missione[3], i+1])

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
