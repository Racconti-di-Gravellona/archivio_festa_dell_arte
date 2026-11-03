# Piano di restyle — Archivio Festa dell'Arte

Fork di lavoro: `CoachGodzup/archivio_festa_dell_arte_restyle` (branch `restyle/plan`).
Repo sorgente: `Racconti-di-Gravellona/archivio_festa_dell_arte` (main, 1995–2026, 30 edizioni).

## 1. Stato attuale (audit)

- 30 edizioni reali: 1995 → 2026, con lacune (2020, 2021), 1996–2007 parziali.
- Ogni edizione ha più file (locandine, volantini, trascrizioni AI, programmi, PDF).
- Esistono `thumb/*.webp` (carousel) e `volantini/*` (full).
- Struttura dati: solo HTML statico + JSON-LD. Nessun JSON esterno.
- Assets: ~85 MB in `volantini/`, 193 file totali in `thumb/`+`volantini/`.

## 2. Criticità del piano fornito (piano_di_migrazione_restyle_archivio.md)

1. **Date/edizioni errate**: dichiara 1993–oggi e 31 edizioni; in realtà 1995–2026, 30 edizioni (2026 = 30ª).
2. **Contenuti inventati**: temi, artisti, cortili, programmi, Unsplash. Non pubblicabili: materiale documentario reale.
3. **Numerazione edizione sbagliata** (2023 = 31ª nel draft).
4. **Schema JSON insufficiente**: mancano trascrizioni, multi-file, PDF, link esterni, crediti/copyright, edizioni mancanti.
5. **Upload via GitHub REST API con token nel codice**: anti-pattern; usare git + PR. Token mai in repo.
6. **Tailwind CDN in produzione**: FOUC, dipendenza runtime, no offline. Preferire CSS compilato (Tailwind CLI) o CSS custom sullo stile attuale.
7. **Ricerca "globale" su campi non esistenti** nel dataset reale.

## 3. Obiettivi del restyle

- Preservare 100% del contenuto e degli anchor `#edYYYY` (JSON-LD, SEO, link esterni).
- Carosello locandine fluido, filtro decennio, ricerca per anno/testo/trascrizione.
- Lightbox zoom/pan, navigazione tastiera, supporto PDF (link esterno).
- Schede edizione: descrizione, galleria file, trascrizione collassabile, link esterni.
- Accessibilità: `prefers-reduced-motion`, focus trap nel lightbox, alt text.
- Performance: lazy loading, thumbs nel carousel, full on demand, no preload di tutti i full.
- Nessuna perdita di informazione rispetto all'HTML attuale.

## 4. Modello dati (data/edizioni.json) — schema corretto

```json
{
  "year": "2024",
  "edition": 28,
  "date": "19-20 settembre 2026",
  "title": "…",
  "description": "…",
  "decade": "2020s",
  "primaryPoster": "volantini/…jpg",
  "thumb": "thumb/…webp",
  "files": [{"url":"…","kind":"image|pdf","caption":"…"}],
  "transcription": "testo…",
  "externalLinks": [{"label":"…","url":"…"}],
  "credits": "…"
}
```

## 5. Fasi (milestone)

- M0: Audit automatico (script) → `docs/audit.md` con inventario edizioni/file/pesi/alt-text.
- M1: Estrattore `scripts/extract-edizioni.mjs` che converte l'HTML attuale in `data/edizioni.json` (senza perdita), + test di round-trip (HTML generato == sezioni originali).
- M2: Nuovo template HTML (Tailwind CLI o CSS custom) che consuma il JSON; parità visiva + feature restyle.
- M3: Lightbox + ricerca + filtri.
- M4: Accessibilità + performance + Lighthouse.
- M5: Deploy Pages sul fork (preview) + PR verso upstream.

## 6. Decisioni confermate

- **Stack stile:** Tailwind CLI (build) — CSS compilato, no CDN runtime.
- **Deploy preview:** subito, su branch `gh-pages` del fork, per iterare visivamente.
- **Trascrizioni AI:** migrarle in `data/edizioni.json` e renderizzarle collassabili, con ricerca full-text.

## 7. Rischio principale

Perdere informazione (trascrizioni, crediti, link) durante la migrazione. Mitigazione: estrattore + test di round-trip prima di toccare il markup.
