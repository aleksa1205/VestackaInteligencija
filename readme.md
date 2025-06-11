# Veštačka inteligencija (Triggle)

## Faza I

### UI

Za UI smo koristili biblioteku **pygame**. Aplikacije sadrži 3 glavna menija:
- Main menu,
- Opcije i
- Menu sa igrom

U main meniju stoji se nalaze dugmići za početak igre i za izlaz iz aplikacije. Kada se pritisne dugme *Play* otvara se prozor sa mogućim opcijama. 
U meniju sa opcijama korisnik bira da li želi da igra protiv računara ili protiv drugog igrača. Nakon toga korisnik bira da li želi da prvi igra on ili njegov protivnik (AI ili drugi igrač u zavisnosti od prethodnog izbora). Na samom kraju korisnik bira veličinu stranice table koja se iscrtava (u rasponu od 4 do 8) i pritiskom na dugme *Play* otvara se novi prozor i igra počinje.

### Logika
Za izradu aplikacije korišćene su sledeće strukture podataka:

#### Matrica
**Matricu** koristimo kao pomoćnu strukturu za crtanje table uz pomoću *pygame* biblioteke i funkcija za pozicioniranje stubića. Dimenzije matrice zavise od izbora korisnika i mogu da budu u rasponu od 4 do 8.

#### Graf
**Graf** je glavna struktura u ovom projektu i implementiran je kao **Dictionary**. U grafu pamtimo indekse svakog čvora kao **tuple (i,j)** i on nam predstavlja *key*, dok nam *value* predstavlja **set** susednih čvorova između kojih je razvučena gumica.

#### Set
**Set-ove** koristimo za čuvanje specifičnih podataka u toku igre zbog njihove mogućnosti da čuvaju samo jednistvene elemente. Prema tome set-ove koristimo za:
- praćenje formiranih puteva (razvučenih gumica) i 
- praćenje formiranih ciklusa dužine 3 (formiranih trouglova posebno za svakog igrača).

### Funkcije

#### Funkcije provere (checker.py)
Kada su u pitanju ove funkcije proveravamo sledeće tri stvari:
- **in_boundaries** - Proverava da li su prosleđene koordinate u granicama "*matrice*". Samim tim osigurava da potezi igrača ne izlaze iz dozvoljenog opsega table.
- **check_length** - Proverava udaljenosti između stubića. Proverava da li je udaljenost između dva stubića tačno 3.
- **end_game** - Proverava da li je igra završena.

#### Funkcije za crtanje (draw.py)
Funkciju u ovom prozoru koristimo za vizuelizaciju igre i prikaz trenutnog stanja table. Funkcije su sledeće:
- **coordinates_to_pixel** - Konvertuje koordinate čvorova (indekse) u piksele za crtanje na ekranu. Ova funkcija se koristi za pozicioniranje elemenata u tabli u skladu sa odabranim dimenzijama.
- **create_empty_board** - Crtamo praznu tablu (matricu) sa svim stubićima na osnovu dimenzije koju je izabrao korisnik (od 4 do 8).
- **create_graph** - Generiše graf na osnovu dimenzije table. Ovaj graf koristimo za praćenje čvorova i njihovih potega. 
- **draw_line** - Crtamo linije između dva čvora (stubića) koja predstavlja razvučene gumice.
- **draw_triangles** - Crtamo trouglove koje je formirao aktivni igrač, u određenoj boji u zavisnosti koji je igrač aktivan.

#### Funkcije za kretanje (move.py)
Funkcije u ovom modulu zadužene su za realizaciju poteza u igri, navigaciju po tabli i identifikaciju trouglova koje su igrači formirali u toku igre.

**Navigacione funkcije**
- **desno** - Prelazi na sledeći čvor koji se nalazi desno od trenutnog čvora.
- **dole_desno** - Prelazi na sledeći čvor dijagonalno dole udesno u odnosu na trenutni čvor.
- **dole_levo** - Prelazi na sledeći čvor dijagonalno dole ulevo u odnosu na trenutni čvor.

**Glavne funkcije**
- **make_move** - Kao parametre prima početni ciljni čvor. Proverava da li je udaljenost između dva čvora validna (mora biti 3). Simulira kretanje iz početnog čvora u svim mogućim smerovima, i to tačno četiri koraka, kako bi proverila da li je moguće doći do ciljnog čvora. Ako je potez validan crta liniju koja predstavlja razvučenu gumicu, nakon čega poziva funkcije *find_triangles* i *draw_triangles*. U suprotnom vraća grešku koja ukazuje da potez nije dozvoljen.

- **make_move_tournament** - Slična funkciji *make_move*, ali je prilagođena zahtevima formata kretanja datih na času. Za razliku od funkcije *make_move*:
    - Funkcija unapred dobija smer kretnja samim tim ne proverava sve smerove.
    - Proverava da li potez izlazi iz granica table.
    - Ne proverava dolazak do ciljnog čvora jer se on ne definiše eksplicitno.

- **find_triangles** - Nakon svakog poteza igrača, proverava da li su formirani novi trouglovi. Identifikovani trouglovi se dodaju u skup trouglova aktivnog igrača. Trouglovi se kasnije vizualizuju preko funkcije *draw_triangles*.

## Faza II

U ovoj fazi je ceo kod refaktorisan zbog čitljivosti i dodate su sledeće funkcionalnosti:
- Omogućeno je odigravanje Triggle igre između dva igrača biranjem odgovarajuće opcije pre početka igre.
- Pre početka igra može da se bira koji igrač će igrati prvi.
- Klikom na jedan stub se on selektuje i crta se imiticaje gumice između tog stuba i cursor-a.
- Ponovnim klikon na neki drugi stub se potez odigrava, odnosno, prvo se proverava da li je unesen potez ispravan
	- Ako jeste, potez se odigrava. Sitna animacija se prikaže i pusti se zvuk, menja se stanje igre i to stanje se odmah prikaže. Nakon toga se menja aktivni igrač.
	- Ako nije, druga animacija se pusta kao i drugi zvuk, prikaže se poruka zašto potez nije ispravan i aktivan igrač ostaje isti sve dok se ispravan potez ne unese.
- Nakon odigranog poteza se menja broj bodava za aktivnog igrača.
- Dok je selektovan jedan stub, desnim klikom ili pritiskom na taster "esc" se briše selekcija tog stuba.
- Kada se skupi dovoljan broj poena igra se završava i prikazuje se pobednik.
- Pauziranje igre je moguće pritiskom na taster "esc" ako nije selektovan nijedan stub i prikazuje se "pause menu".
- Dodata je funkcija koja na osnovu jednog stanje igre generiše sva moguća stanja igre koja mogu da postoje nekon tog stanja.

### Refaktorisanje
Dobar deo koda koji je pisan u 1. fazi je refaktorisan. Refaktorisana je sama struktura pygame aplikacija kao i sve funkcionalnosti. 

Funkcionalnosti su sada enkapsulirane u zasebnim klasama.
#### PyGame struktura aplikacije
Postoji jedan fajl **'game.py'** koji zadrži sve bitne informacija o pygame aplikaciji i u toj klasi se pokreće game loop.

Game klasa i sve ostale klase koje trebaju nešto da renderuju u pygame prozoru su strukturisane na sledeći nacin:
- U **konstruktoru** se inicijalizuju atributi klase, atributi klase pamte informacije na osnovu kojih se ta instanca crta u pygame prozoru.
- **Render** funkcija renderuje sve na ekranu koristeći informacije iz atribute klase.
- **Update** funkcija menja vrednosti atributima na osnovu user input-a.
Ovime se omogućava da se na osnovu user input-a izgled elemenata menja. Ovom strukturom kod aplikacije izgleda **čitljivo i pregledno**.

Svaki state aplikacije (meniji, pause manu, promena igraca, game world...) je zasebna klasa koja sadrzi update i render funkciju. Game klasa state-ove pamti u stack strukturi i zove render i update funkcije samo onog state-a **koji je na vrhu stack-a**.

Sve iz draw.py i checker.py je sada enkapsulirano u zasebne klase.

Jos dosta stvari je refaktorisano i to će biti objašnjeno kasnije.

### Funkcionalnosti potrebne za II fazu

Funkcionalnosti potrebne za ovu fazu biće objašnjene kroz klase.

#### Game World klasa

Game world je state u kome se triggle odigrava. Na vrhu ekrana se pise koji igrač igra prvi i koji je prethodni potez bio. Sa leve i desne strane stoje poeni koji su oba igrača osvojila.

Na sredini se iscrtava triggle board. To se radi kroz klasu Board.

#### Board klasa

Board klasa je zaslužna za crtanje board-a i za dobar deo funkcionalnosti.

Kao što je objašnjeno na početku ove sekcije **atributi** ove klase su sve informacije bitne za isrtavanje board-a: *pegs (stubovi), game state (on će biti kasnije objašnjen) i još neki menje bitni atributi*.
**Render funkcija** sadrži logiku za iscrtavanje board-a tako što koristi atribute klase.
**Update funkcije** sadži logiku za čitanje inputa korisnika i na osnovu input-a menja odgovarajuće vrednosti atributa.

Stubovi se pamte kao zasebna klasa jer moraju da imaju logiku za detektovanje kolizije (da bi se znalo na koji stub je kliknuto) i zbog toga se pamti niz ove strukture. Takođe svaka instanca stuba pamti i svoj indeks.

U update funkciji se poziva funkcija za odigravanje poteza ako se izaberu dva stuba.
**make_move funkcija** se izvršava na sledeći način:
- Proverava input korisnika, ako nije dobar prikazuje se greška i isti igrač mora ponovo da unese potez, ako je input validan funkcija nastavlja izvršenje.
- Menja se instaca game state-a koja se pamti u board klasi.
- Generisu se svi mogući novi game state-ovi za trenutni game state (verovatno će ovo biti pomereno negde drugde u narednoj fazi).

#### Game state klasa

Pamti trenutno stanje igre, objašnjeno je u prethodnoj fazi u poglavlju *Logika* koje informacije se pamte.

**update_state funkcija** kao parametar ima putanju koja se pravi između dva izabrana stuba kako bi promenila stanje igre. 
Funkcija se izvršava na sledeći način:
- Prvo se ta putanja doda u niz "paths" i u graf.
- Zatim se pronađu svi trouglići koji se formiraju na osnovu te nove putanje.
- Menja se aktivan igrac i pamti se taj zadnji potez.
*Update state* menja instancu nad kojom se zove.

**get_new_state funkcija** radi isto što i *update_state* samo što ona vrati novoformirani state umesto da menja instancu nad kojom se zove.

**generate_all_possible_moves funkcija** generiše sva moguća stanja koja mogu da postoje nakon trenutnog stanja. 
To radi tako što generiše sve moguće poteze koji mogu da se odigraju nakon trenutnog stanja igre.
Za svaki potez kreira deep copy trenutnog stanja i za njega pozove *get_new_state* funkciju kako bi ona vratila novo stanje igre bez da promeni trenutno. To novo stanje se dodaje u niz i taj niz je povratna vrednost ove funkcije.
Deep copy je jako skupa operacija i trebala bi da se optimituje u narednoj fazi kako ne bi bilo problema sa performansama igrice.

## Autori

- [Aleksa Perić](https://github.com/aleksa1205)

- [Jovan Cvetković](https://github.com/CJovan02)

- [Anja Janković](https://github.com/saznanyaa)