# Dokumentacija projekta Triggle

# NAPOMENA
**Član tima kod koga se nalazi source kod za logiku aplikacije se uspavao i nije poslao kod. U ovom dokumentu se trenutno nalazi stara logika aplikacije i UI. Ostatak aplikacije mozemo da pošaljemo sutra.**

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