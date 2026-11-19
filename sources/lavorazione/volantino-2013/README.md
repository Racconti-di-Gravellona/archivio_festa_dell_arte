# Volantino 2013 (19ª edizione) — ricomposizione dalle scansioni

File pubblicati:

- `../../volantini/2013-19ed-volantino-fronte.jpg` — 5160×2464
- `../../volantini/2013-19ed-volantino-retro.jpg` — 5156×2464
- copie 1200 px in `../../medium/`

## Scansioni di partenza

Cinque scansioni a 300 dpi (`scansioni/Scansione 14-18.jpeg`, 2464×3460 px),
fatte dallo stesso curatore il 16 novembre 2026. Ogni scansione contiene una
parte del volantino appoggiata di traverso sul piano, allineata al bordo alto
e destro; il resto del foglio è bianco.

| scansione | lato | contenuto |
|---|---|---|
| 14 | fronte | copertina (gialla, San Pessimino, 1-2 / 8-9 giugno 2013) |
| 15 | fronte | speciale pomeriggio di domenica 9 giugno, concerto di Davide Van de Sfroos, ingresso € 10 |
| 16 | fronte | «Gravellona è un libro d'arte», «Suonano e ballano», elenco partner e indirizzo del Comune (ultima anta) |
| 17 | retro | «Gravellona 200 anni, chiesa e futura» e decennale di San Pessimino del 2 giugno |
| 18 | retro | due ante unite: griglia fotografica del programma delle domeniche 2 e 9 giugno |

## Passaggi applicati

1. Rotazione di 90° in senso orario (il testo era coricato).
2. Ritaglio dell'anta: riquadro `x 1716-3460`, `y 0-2464` (1744×2464 px,
   circa un A5 a 300 dpi), identico in tutte le scansioni perché il foglio era
   sempre appoggiato nello stesso punto.
3. Rifilo di 12 px per lato sui bordi verticali, per togliere l'ombra della
   piega fra un'anta e l'altra.
4. Unione orizzontale nell'ordine di lettura: fronte `14 | 15 | 16`, retro
   `17 | 18`. La scansione 18 conteneva già due ante, quindi il retro ha due
   blocchi invece di tre.
5. JPEG qualità 90, sottocampionamento 4:2:2, progressivo.

Le scansioni grezze restano in `scansioni/` e non vengono pubblicate.

## Nota sulle proporzioni

Fronte (3 ante da 1720 px) e retro (1720 + 3436 px) misurano 5160 e 5156 px:
lo scarto di 4 px dipende dal bordo tagliato dal piano dello scanner sul lato
destro della scansione 18. Non è stato corretto con un ridimensionamento,
per non alterare la scala del testo.
