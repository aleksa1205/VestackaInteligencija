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


## Autori

- [Aleksa Perić](https://github.com/aleksa1205)

- [Jovan Cvetković](https://github.com/CJovan02)

- [Anja Janković](https://github.com/saznanyaa)
