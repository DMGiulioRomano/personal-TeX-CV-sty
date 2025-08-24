# CV Generator - Sistema Dinamico LaTeX

Un generatore di CV moderno che trasforma dati YAML in documenti LaTeX professionali. Progettato per musicisti e professionisti creativi, con supporto per multiple tipologie di contenuto e stili personalizzabili.

## 🚀 Caratteristiche principali

- **📊 Dati strutturati**: Gestione centralizzata in formato YAML
- **🎨 Multi-stile**: Supporto per stili Europeo e Accademico
- **🎵 Contenuti specializzati**: Gestione ottimizzata per attività concertistiche e progetti artistici
- **🛠 Automazione completa**: Build system con GNU Make
- **📦 Build isolato**: Compilazione in directory separata per mantenere pulito il workspace
- **🔧 Sviluppo modulare**: Stili LaTeX separati e riutilizzabili

## 📋 Requisiti

### Software necessario
- **Python 3.11+** con PyYAML
- **XeLaTeX** (TeX Live o MiKTeX)
- **GNU Make** (opzionale ma consigliato)

### Verifica dipendenze
```bash
make check
```

### Installazione dipendenze Python
```bash
make install-deps
# oppure manualmente:
pip install PyYAML
```

## 📁 Struttura del progetto

```
cv-generator/
├── cv_data.yaml          # Dati del CV (fonte unica)
├── generate_cv.py        # Script di generazione Python
├── Makefile             # Sistema di build automatizzato
├── styles/              # Stili LaTeX modulari
│   ├── CV_temp_common.sty    # Stile base condiviso
│   ├── style_european.sty    # Stile europeo
│   └── style_academic.sty    # Stile accademico
├── build/               # Directory di compilazione (auto-generata)
│   ├── cv_data.tex          # LaTeX generato
│   ├── CV_GIULIO_DE_MATTIA.tex  # Documento principale
│   └── CV_GIULIO_DE_MATTIA.pdf  # Output finale
└── img/                 # Risorse immagini
```

## 🎯 Utilizzo rapido

### Generazione CV Europeo (default)
```bash
make european
```

### Generazione CV Accademico
```bash
make academic
```

### Generazione entrambi gli stili
```bash
make both
```

## 🛠 Comandi avanzati

### Sviluppo e debug
```bash
make debug          # Compilazione con output dettagliato
make watch          # Ricompilazione automatica
make info           # Stato file e configurazione
```

### Gestione file
```bash
make clean          # Rimuove file temporanei LaTeX
make clean-all      # Rimozione completa (elimina build/)
make export         # Copia PDF dalla build/ alla directory principale
make open           # Apre il PDF generato
```

### Personalizzazione
```bash
make STYLE=academic compile    # Forza uno stile specifico
make generate STYLE=european  # Solo generazione LaTeX
```

## 📝 Personalizzazione dei dati

Modifica il file `cv_data.yaml` per aggiornare:

### Dati personali
```yaml
dati_personali:
  nome: "Nome Cognome"
  ruolo: "Ruolo Professionale"
  email: "email@example.com"
  telefono: "+39 XXX XXX XXXX"
  # ... altri campi
```

### Esperienze professionali
```yaml
esperienze_professionali:
  - periodo: "MM/YYYY -- oggi"
    organizzazione: "Nome Organizzazione"
    ruolo: "Posizione ricoperta"
    mansioni:
      - "Descrizione attività 1"
      - "Descrizione attività 2"
```

### Attività concertistiche/artistiche
```yaml
attivita_concertistica:
  - data: "DD/MM/YYYY"
    venue: "Luogo"
    organizzatore: "Organizzatore"
    titolo: "Titolo opera/evento"
    tipo: "Prima assoluta/Repertorio"
    organico: "Strumentazione"
    ruolo: "Compositore/Interprete/Tecnico"
```

### Competenze tecniche
```yaml
tool_digitali:
  competenze_audio:
    - "Competenza tecnica 1"
    - "Competenza tecnica 2 (con specifiche)"
  linguaggi_programmazione:
    - "Python"
    - "C++"
```

## 🎨 Creazione di nuovi stili

### 1. Crea un nuovo file di stile
```bash
touch styles/style_mio_stile.sty
```

### 2. Struttura base del file di stile
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{style_mio_stile}[2025/08/21 Mio stile personalizzato]

% Importa le impostazioni comuni
\usepackage{styles/CV_temp_common}

% Definisci i comandi personalizzati
\newcommand{\experience}[4]{%
  % Tua formattazione per le esperienze
}

\newcommand{\artisticevent}[6]{%
  % Tua formattazione per gli eventi artistici
}
```

### 3. Utilizza il nuovo stile
```bash
make generate STYLE=mio_stile
make compile
```

## 🔧 Architettura tecnica

### Flusso di elaborazione
1. **Parsing YAML**: `generate_cv.py` legge `cv_data.yaml`
2. **Generazione LaTeX**: Crea `cv_data.tex` con i comandi LaTeX
3. **Documento principale**: Genera `CV_GIULIO_DE_MATTIA.tex` che importa lo stile
4. **Compilazione**: XeLaTeX produce il PDF finale in `build/`

### Escape LaTeX automatico
Il generatore applica automaticamente l'escape dei caratteri speciali LaTeX (`&`, `%`, `$`, `#`, ecc.) per evitare errori di compilazione.

### Sistema di stili modulare
- **`CV_temp_common.sty`**: Stile base con header, font, geometria
- **`style_*.sty`**: Stili specifici che estendono quello comune
- **Comandi standardizzati**: `\experience{}`, `\artisticevent{}`, `\education{}`

## 🐛 Risoluzione problemi

### Errore "File style_X.sty non trovato"
```bash
ls styles/          # Verifica presenza file di stile
make check          # Controlla dipendenze
```

### Errore di compilazione LaTeX
```bash
make debug          # Mostra output dettagliato LaTeX
make clean          # Rimuove file temporanei
```

### Caratteri speciali non visualizzati
- Il generatore applica escape automatico
- Per simboli speciali, usa i comandi LaTeX nel YAML (es. `\\&` per &)

## 📄 Licenza

Questo progetto è rilasciato sotto [Unlicense](LICENSE) - dominio pubblico.

## 🤝 Contribuire

1. Fai fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nuova-feature`)
3. Commit delle modifiche (`git commit -am 'Aggiunge nuova feature'`)
4. Push del branch (`git push origin feature/nuova-feature`)
5. Crea una Pull Request

### Idee per contributi
- Nuovi stili LaTeX (minimal, creative, tech-focused)
- Supporto per nuovi tipi di contenuto (pubblicazioni, certificazioni)
- Integrazione con altri formati di output (HTML, Markdown)
- Interfaccia web per l'editing del YAML

---

> 💡 **Suggerimento**: Usa `make help` per vedere tutti i comandi disponibili!
