import { readFileSync, writeFileSync } from 'node:fs';

const data = JSON.parse(readFileSync('data/edizioni.json', 'utf8'));

// Testi per edizione — fonte: Wikipedia, "Gravellona Lomellina",
// sezione "Elenco delle opere realizzate durante la Festa dell'Arte e delle sue tematiche"
// (sources/wikipedia/paese-d-arte.md).
const contextByYear = {
  1995: "Concorso di pittura a tema «Medioevo: San Giorgio combatte contro il drago — XX Secolo: l'uomo libero combatte contro la burocrazia». Vincitore G. Crippa con i pannelli di ceramica in piazza.",
  1996: "2º Concorso sul tema «Medioevo: San Giorgio combatte contro il drago — XX Secolo: l'uomo libero combatte contro la burocrazia».",
  1997: "3º Concorso sul tema «Medioevo: San Giorgio combatte contro il drago — XX Secolo: l'uomo libero combatte contro la burocrazia e altri mostri».",
  1998: "Festa dedicata all'arte dei popoli che vissero in simbiosi con la natura: Indiani d'America, aborigeni australiani, Celti.",
  1999: "Tre cabine dell'Enel vengono trasformate in giganti.",
  2000: "Vecchie macchine agricole come sculture.",
  2001: "Spaventapasseri e spazzacamini. Durante questa festa si tiene la prima edizione del Campionato Europeo di Caccia alla Zanzara. Inizio dei lavori di costruzione del Parco dei Tre Laghi.",
  2002: "Enormi giganti di balle di paglia in piazza e a lato delle strade che conducono a Gravellona (presto andati perduti a causa di un atto vandalico). Il lavatoio di Barbavara diventa palcoscenico.",
  2003: "I muri di cinta diventano monumento.",
  2004: "Sui margini delle strade paracarri e spartitraffico colorati. Durante questa festa vengono realizzati i bicchieri celtici.",
  2005: "Termine dei lavori del Parco dei Tre Laghi. Compare una rana in granito a complemento della fontana.",
  2006: "Inaugurazione del Parco dei Tre Laghi. Triciclo sul nuovo sagrato della chiesa parrocchiale.",
  2007: "Sagome riferite alla vita contadina: pastori, capre, pecore, carro trainato da buoi, cavallo.",
  2008: "Totem al Parco dei Tre Laghi.",
  2009: "Sagome di zebre.",
  2010: "Dolmen e Cromlech al Parco dei Tre Laghi.",
  2011: "Muro decorativo all'Oratorio San Faustino.",
  2012: "Inizio del progetto «Art'è — Libro d'arte all'aperto»: installate riproduzioni di opere dell'Ottocento italiano, tra cui Segantini, Signorini e Pellizza da Volpedo. «Vicoli e strade diventano così come le pagine di un libro d'arte all'aperto».",
  2013: "Prosecuzione del progetto «Art'è», principalmente con riproduzioni di Telemaco Signorini e Francesco Hayez. Processione goliardica di San Pessimino. Esibizione di Davide Van De Sfroos.",
  2014: "Prosecuzione del progetto «Art'è», in particolare lungo la via Marconi. Cartelli di benvenuto nel paese, opera di Libero Greco.",
  2015: "Ombrelli (installazione temporanea) nel cortile comunale. Prosecuzione di «Art'è».",
  2016: "Ombrelli nel cortile antistante la scuola (installazione temporanea). Prosecuzione di «Art'è».",
  2017: "Orologio-bicicletta in Via Circonvallazione.",
  2018: "Tema medievale. Presentazione del progetto «Monforte della Palude» per la realizzazione di un borgo altomedievale al Parco dei Tre Laghi.",
  2019: "Prosecuzione del progetto «Art'è» e di «Monforte della Palude».",
  2022: "Monforte della Palude: proiezione dell'incendio e richiesta ai cittadini se proseguire o meno il progetto.",
  2023: "Festa interamente al Parco dei Tre Laghi.",
  2024: "Tema dell'edizione: i gatti.",
  2025: "«Mousiké — l'arte delle muse».",
  2026: "Festa spostata in settembre. Inaugurazione del Museo della Bicicletta Luciano Geddo.",
  2006: "Inaugurazione del Parco dei Tre Laghi: costruzione di un paesaggio naturale a Gravellona Lomellina.",
  2008: "Totem di palude con gli animali totemici della nostra terra (zanzara, airone, pesce, rana). Idea Gravellonese, disegno di Libero Greco, 14ª festa dell'Arte.",
  2010: "Dolmen e Cromlech al Parco dei Tre Laghi; il dolmen era stato installato per la Festa dell'Arte 1998 sul Valdarengo e spostato al parco nella primavera 2010.",
  2013: "Prima festa de «Il fiore e il lago» e nuova scalinata in granito nel Parco dei Tre Laghi.",
  2018: "Nuovo progetto di Monforte della Palude: cantiere di costruzione di un villaggio incastellato della seconda metà dell'XI secolo con fattoria medievale (4 obiettivi: archeologia sperimentale, cultura artigianale, ecologia, turismo di qualità).",
  2019: "Prolungamento del progetto Monforte della Palude; il Gravellona Express diventa spazio pub.",
};

const SOURCES = [
  {
    label: "Wikipedia — Gravellona Lomellina (Paese d'arte)",
    url: "https://it.wikipedia.org/wiki/Gravellona_Lomellina#Paese_d'arte",
  },
  {
    label: "GravellonArtistica — Cento anni",
    url: "https://www.gravellonartistica.com/cento-anni",
  },
];

for (const ed of data) {
  const ctx = contextByYear[ed.year];
  if (ctx) ed.context = ctx;
  ed.sources = SOURCES;
}

writeFileSync('data/edizioni.json', JSON.stringify(data, null, 2) + '\n');
console.log(`Integrati contesti per ${data.filter(e => e.context).length}/${data.length} edizioni.`);
