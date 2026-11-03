# 📋 Piano di Migrazione: Restyle Archivio Festa dell'Arte
**Repository Target:** `racconti-di-gravellona/archivio_festa_dell_arte`  
**Architettura:** Sito Statico / GitHub Pages (HTML5, Tailwind CSS, JS ES6, GitHub REST API)

---

## 🎯 Obiettivo del Progetto
Rinnovare l'archivio storico della **Festa dell'Arte di Gravellona Lomellina** per gestire e valorizzare **oltre 30 edizioni (1993 – Oggi)**.  
Il nuovo layout include:
1. **Hero Carosello 3D / Coverflow Multi-Edizione:** Per la navigazione fluida tra 30+ locandine storiche con filtri per decenni e vista a griglia alternativa.
2. **Ricerca Globale Istantanea:** Filtro in tempo reale per anno, artista, titolo o cortile.
3. **Lightbox Fullscreen Interattivo:** Galleria immagini con zoom, pan/trascinamento e comandi da tastiera per consultare locandine e dettagli ad alta risoluzione.
4. **Scheda Dettaglio Dinamica:** Organizzazione a schede/colonne per *Programma Eventi* (timeline) e *Installazioni Artistiche & Cortili*.

---

## 🛠️ Architettura Dati Suggerita (`data/edizioni.json`)
Per facilitare la manutenzione, i dati delle 30 edizioni saranno separati dall'interfaccia e salvati in un file JSON strutturato come segue:

```json
[
  {
    "year": "2023",
    "editionNum": "Edizione 31ª",
    "decade": "2020s",
    "title": "L'Arte nel Borgo",
    "date": "Giugno 2023",
    "posterUrl": "assets/img/2023/locandina.jpg",
    "description": "Descrizione dell'edizione 2023...",
    "media": [
      {
        "url": "assets/img/2023/locandina.jpg",
        "badge": "Locandina Ufficiale",
        "title": "Manifesto Ufficiale 2023",
        "description": "Locandina originale dell'edizione."
      }
    ],
    "programme": [
      {
        "time": "10:00",
        "title": "Inaugurazione e Apertura Mostre",
        "desc": "Taglio del nastro in Piazza Delucca."
      }
    ],
    "installations": [
      {
        "name": "Luce e Pietra",
        "artist": "Elena Baroni",
        "location": "Cortile San Rocco",
        "desc": "Scultura luminosa in terracotta e pietra."
      }
    ]
  }
]
```

---

## 📝 TODO List Integrale per la Migrazione tramite GitHub API

### **Fase 1: Preparazione e Autenticazione**
- [ ] **1.1. Creazione del GitHub Personal Access Token (PAT):**
  - Vai su GitHub $\rightarrow$ *Settings* $\rightarrow$ *Developer Settings* $\rightarrow$ *Personal Access Tokens*.
  - Crea un token con permessi di scrittura (`repo` scope) per il repository `racconti-di-gravellona/archivio_festa_dell_arte`.
- [ ] **1.2. Mappatura degli Asset Esistenti:**
  - Verifica la struttura delle cartelle attuali delle immagini/locandine (es. `assets/img/` o `images/`).

---

### **Fase 2: Preparazione dei File del Progetto**
- [ ] **2.1. Creare/Aggiornare `index.html`:** Incorporare il nuovo prototipo responsivo con Tailwind CSS, carosello 3D, filtro decenni e Lightbox.
- [ ] **2.2. Generare `data/edizioni.json`:** Popolare l'archivio con i dati storici dal 1993 ad oggi.
- [ ] **2.3. Organizzare i file multimediali:** Rinominare/caricare le immagini ad alta risoluzione per ciascuna edizione nella cartella `assets/img/{anno}/`.

---

### **Fase 3: Esecuzione dell'Upload / Migrazione via GitHub REST API**
I file vengono inviati o aggiornati inviando richieste `PUT` all'endpoint di GitHub:  
`PUT https://api.github.com/repos/racconti-di-gravellona/archivio_festa_dell_arte/contents/{path_del_file}`

#### **Punti chiave dell'API:**
- Il contenuto dei file (sia testo `.html`/`.json` che binari `.jpg`/`.png`) **deve essere codificato in Base64**.
- Se un file esiste già, occorre recuperare prima il suo valore `sha` tramite richiesta `GET` per sovrascriverlo.

---

### **Fase 4: Verifica e Deployment**
- [ ] **4.1. Monitoraggio Deploy GitHub Pages:**
  - Controlla lo stato del build con l'endpoint `GET /repos/{owner}/{repo}/pages/builds/latest`.
- [ ] **4.2. Collaudo Funzionale e Mobile:**
  - Test su smartphone per verificare le performance del carosello e lo zoom del Lightbox.
  - Test della ricerca globale e dei filtri rapido per decennio.

---

## 🐍 Script di Automazione Python (Pronto all'Uso)

Puoi salvare ed eseguire questo script sul tuo PC per eseguire l'intera migrazione senza dover clonare il repository Git:

```python
import requests
import base64
import os
import json

# CONFIGURAZIONE REPOSITORY
GITHUB_TOKEN = "IL_TUO_PERSONAL_ACCESS_TOKEN"
REPO_OWNER = "racconti-di-gravellona"
REPO_NAME = "archivio_festa_dell_arte"
BRANCH = "main"  # Utilizzare 'main' o 'master' a seconda del branch predefinito

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def upload_file_to_github(file_path_local, repo_path_remote, commit_message):
    """
    Legge un file locale (testo o immagine), lo converte in Base64 
    e lo invia/aggiorna nel repo di GitHub tramite API REST.
    """
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path_remote}"
    
    # 1. Verifico se il file esiste già su GitHub per recuperare lo SHA
    get_res = requests.get(url, headers=HEADERS)
    sha = get_res.json().get("sha") if get_res.status_code == 200 else None
    
    # 2. Lettura e codifica Base64
    with open(file_path_local, "rb") as f:
        content_bytes = f.read()
    encoded_content = base64.b64encode(content_bytes).decode("utf-8")
    
    # 3. Costruzione payload
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha  # Requisito per aggiornare file esistenti

    # 4. Chiamata API PUT
    response = requests.put(url, headers=HEADERS, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"✅ CARICATO CON SUCCESSO: {repo_path_remote}")
    else:
        print(f"❌ ERRORE [{response.status_code}] su {repo_path_remote}: {response.json()}")


# --- ESECUZIONE MIGRAZIONE ---
if __name__ == "__main__":
    print("🚀 Inizio migrazione automatica via GitHub API...")
    
    # Upload File HTML Principale
    if os.path.exists("index.html"):
        upload_file_to_github("index.html", "index.html", "Restyle: Aggiornato index.html con carosello 3D e Lightbox")
    
    # Upload Database JSON Edizioni
    if os.path.exists("data/edizioni.json"):
        upload_file_to_github("data/edizioni.json", "data/edizioni.json", "Data: Aggiunto archivio storico edizioni JSON")
        
    print("🎉 Migrazione completata. Verifica il deploy su GitHub Pages!")
```