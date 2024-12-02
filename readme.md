# Dokumentacija projekta Triggle

# NAPOMENA
**Član tima kod koga se nalazi source kod za logiku aplikacije se uspavao i nije poslao kod. U ovom dokumentu se trenutno nalazi stara logika aplikacije i UI. Ostatak aplikacije mozemo da pošaljemo sutra.**
**Stara logika aplikacije se nalazi u fajlu *Trigle.py* **

GitHub link projekta: https://github.com/aleksa1205/VestackaInteligencija

## Zadatak I

### UI

Za UI smo koristili biblioteku *pygame*. Aplikacije sadrži 3 glavna menija:
- Main menu
- Opcije
- Menu sa igrom

U glavnom meniju stoji samo dugme za izlaz iz aplikacije i dugme za početak igre. Kada se pritisne dugme 'Play' otvara se prozor sa opcijama.
U meniju sa opcijama korisnik bira da li želi da igra protiv računara ili protiv drugog igrača. Nakon toga mora da izabere da li želi da on prvi igra ili njegov protivnik (AI ili drugi igrač).
Nakon toga korisnik bira veličinu stranice table koja se iscrtava i pritiskom na dugme *play* otvara se novi prozor i započinje se igra.

### Logika

Koristili smo nekoliko struktura podataka kako bi smo opsiali stanje igre.

#### Matrica stubova:

Koristili smo matricu kako bi smo indeksirali svaki stub radi lakseg proveravanja poteza i crtanja stanja igre korišćenjem pygame biblioteke.

Za ispravnost poteza koristili smo par pomoćnih funkija:
- Funkcije koje daju indeks suseda na osnovu poteza koji se izabere (desno, dole levo, dole desno),
- Funkcija koja provera da li je dati indeks unutar indeksa matrice,
- Funkcija koja raćuna dužinu izmedju uneta 2 čvora.

Isprevnost poteza se ispituje tako što se od pocetnog čvora 4 puta pozovu funkcije za pronalaženje suseda (4 desna suseda, 4 suseda dole levo i 4 suseda dole desno).
Nakon toga se 3 dobijena stuba ispituju da li se poklapaju sa krajnjim stubom, ako se poklapaju potez je pravilno unesen, ako nije nije pravilno unesen.
Takodje se, korišćenjem pomoćne strukture *set*, proverava da li je takav identičan potez već unet, ako jeste potez se smatra neispravnim.

#### Graf

Graf se koristi da bi se pronasli trouglići.
Graf je neusmeren, pamti se kao dictionary i trouglić se pronalazi tako sto se pronadje ciklus duzine 3.
Igrač koji je poslednji odigrao taj potez dobija onoliko bodova koliko je trouglića sklopio.

#### Set strukture

Pamti se *set* puteva u grafu kako bi smo proverili ispravnost sledećeg poteza.
Ako se unese put koji već postoji potez je neispravan.

#### Funkcije ispitivanja
*in_boundaries* ispituje da li smo izašli iz opsega matrice i ako jesmo vraća False.
*check_length* proverava da li je udaljenost između dva prosleđena stuba 3 da bi znali da li smemo da povučemo poteg.
*end_game* proverava da li je došlo do kraja igre i ako jeste ko je pobedio.

#### Funkcije za pomeranje
Funkcije *desno*, *dole_desno* i *dole_levo* izvršavaju poteze.
Funkcija *make_move* kao parametre ima startni i ciljni čvor. Ona polazi od čvora *start* i ide u svim mogućim smerovima (desno, dole levo i dole desno) i proveri da li je nekim od tih puteva stigao do čvora *end*. Ako jeste došao do njega i taj put već nije korišćen da se dođe do tog čvora dodaje se u set puteva, ažurira se graf i crta se linija.
Funkcija *make_move_tournament* ima sličnu funkcionalnost kao i funkcija *make_move* samo što odgovara formatu koji je dat na prezentaciji.
Funkcija *find_triangle* traži ciklus dužine 3 i ako ga nađe i on nije već uzet od starne nekog od igrača dodaje ga trenutno aktivnom igraču i crta trougao.

#### Pomoćne funkcije
U fajlu *draw.py* su samo pomoćne funkcije za iscrtavanje koje ne bi imalo potrebe objašnjavati dodatno.