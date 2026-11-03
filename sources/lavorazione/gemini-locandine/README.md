# Input per il restauro Gemini — locandine Festa dell'Arte (dal video)

Cartella di lavoro. **Non** sono file pubblicati: servono da input per il restauro AI.

Fonte: canale **Elisabetta Bevilacqua (@niktuberto1)**
- storico delle locandine 1995-2012: https://www.youtube.com/watch?v=qxwoVUxzl0Q
- volantino 2013: https://www.youtube.com/watch?v=MDVrWE6kzJc (Decennale San Pessimino 2003-2013)

## Come sono stati preparati

Ogni file e' la copia ingrandita dell'immagine pubblicata in
`archivio_festa_dell_arte/volantini/` (originali **non modificati**):

1. ingrandimento **x3** con interpolazione Lanczos4;
2. riduzione del rumore `fastNlMeansDenoisingColored` (h = 3);
3. contrasto: allungamento del canale L ai percentili 1-99;
4. unsharp mask leggero (sigma 1,2; 1,5 / -0,5).
Nessuna ricostruzione: e' solo una base pulita e piu' grande per Gemini.

## File

| file | dimensioni | edizione |
|---|---|---|
| `1995-01ed-locandina-hd.png` | 1254x1731 | 1ª edizione — 17-18 giugno 1995 — «di Gravellona e Barbavara». Temi: San Giorgio / XX secolo. |
| `1996-02ed-locandina-hd.png` | 1275x1773 | 2ª edizione — 8-9 giugno 1996 |
| `1997-03ed-locandina-hd.png` | 1245x1692 | 3ª edizione — 7-8 giugno 1997. Temi: «Medio Evo» (San Giorgio e il drago) / «XX Secolo» (l'uomo libero e la burocrazia). |
| `1998-04ed-locandina-hd.png` | 1284x1743 | 4ª edizione — 6-7 giugno 1998. Enti: Comune, Provincia di Pavia, Regione Lombardia. |
| `1999-05ed-locandina-hd.png` | 1284x1737 | 5ª edizione — 4-5-6 giugno 1999. Sponsor: Enel, Banca Popolare di Novara. |
| `2000-06ed-locandina-hd.png` | 1260x1692 | 6ª edizione — 3-4 e 10-11 giugno 2000 |
| `2001-07ed-locandina-hd.png` | 1281x1755 | 7ª edizione — 2-3 e 9-10 giugno 2001. Convegno «Bellezza Natura Arte come fattori di sviluppo economico» (10 giugno, teatro dell'oratorio). |
| `2002-08ed-locandina-hd.png` | 1158x1902 | 8ª edizione — giugno 2002 (sabato 8 - domenica 9; la data della prima giornata è poco leggibile). |
| `2003-09ed-locandina-hd.png` | 1263x1746 | 9ª edizione — da sabato 31 maggio a domenica 8 giugno 2003. Con Parrocchia B.V.M. Assunta e Scuola di Musica di Gravellona. |
| `2004-10ed-locandina-hd.png` | 1314x1914 | 10ª edizione — 5-6 e 12-13 giugno 2004. Tema/immagine «libero 2004». |
| `2005-11ed-locandina-hd.png` | 1488x1917 | 11ª edizione — 4-5 e 11-12 giugno 2005. Agg. 25-10-2026: ricomposta anche l'intestazione «XI FESTA DELL'ARTE / di GRAVELLONA LOMELLINA (PAVIA)»; il video taglia solo il margine sopra le lettere. |
| `2006-12ed-locandina-hd.png` | 1434x1977 | 12ª edizione — 2-3-4 e 10-11 giugno 2006. «Festa dell'Arte e dell'Artigianato Creativo». |
| `2007-13ed-locandina-hd.png` | 1212x1791 | 13ª edizione — 2-3 e 9-10 giugno 2007. «il paese dove arte natura e fantasia crescono ogni anno»; «Libero 2007». |
| `2008-14ed-locandina-hd.png` | 1314x1068 | 14ª edizione — 31 maggio, 1-2 e 7-8 giugno 2008. Fotogramma singolo (fetta parziale): per questa edizione esiste il manifesto ufficiale a 4 pagine, già restaurato. |
| `2009-15ed-locandina-hd.png` | 1428x1068 | 15ª edizione — 30-31 maggio e 1-2 giugno 2009. Fotogramma singolo (fetta parziale): per questa edizione esiste il manifesto ufficiale. |
| `2010-16ed-locandina-hd.png` | 1512x2151 | 16ª edizione — 29-30 maggio e 1-2 giugno 2010, con festa celtica. |
| `2011-17ed-locandina-hd.png` | 1359x1068 | 17ª edizione — 1-5 giugno 2011, con festa celtica. Fotogramma singolo: per questa edizione esiste la copertina ufficiale e il volantino a 3 pagine. |
| `2012-18ed-locandina-hd.png` | 888x1068 | 18ª edizione — 2-3 e 9-10 giugno 2012. «UN PAESE UN LIBRO D'ARTE A CIELO APERTO». Fotogramma singolo: per questa edizione esistono le locandine ufficiali (tema e date). |
| `2013-19ed-volantino-hd.png` | 1827x1440 | 19ª edizione — 1-2 e 8-9 giugno 2013. Volantino ripreso di sbieco nel video «Decennale San Pessimino 2003-2013»: va raddrizzato. |

## Prompt suggerito (uno per immagine)

```
Agisci come restauratore di manifesti a stampa. Ti allego la scansione (ingrandita) di una locandina della Festa dell'Arte di Gravellona Lomellina: <didascalia della riga corrispondente>
È ricavata da un video a bassa risoluzione, quindi presenta sfocatura, rumore e artefatti di compressione.

Ricostruisci l'immagine in alta qualità, senza cambiare il contenuto:
- conserva esattamente testi, loghi, stemmi, date e impaginazione originali;
- ripulisci il fondo, elimina il rumore e gli artefatti di compressione, non inventare dettagli che non si leggono;
- rendi il testo nitido e leggibile, con bordi puliti; raddrizza se serve;
- mantieni le proporzioni e i colori originali (non aggiungere cornici o scritte);
- dove un testo è illeggibile, lascialo tale: non interpretarlo.
Restituisci l'immagine restaurata alla massima risoluzione possibile.
```

## Nota

Gli originali pubblicati restano quelli a bassa risoluzione in
`archivio_festa_dell_arte/volantini/` (`AAAA-NNed-locandina-video.jpg`).
I restaurati andranno salvati come `AAAA-NNed-locandina-hd.jpg` con la nota
«restaurato con Gemini».
