Rothmann, Christoph, 22411549

Goleo - Der Bibliotheksassistent für die Buchausleihe

https://mygit.th-deg.de/cr29549/sas-de-ws-25-26.git

https://mygit.th-deg.de/cr29549/sas-de-ws-25-26/-/wikis/home

# Project description

Ein Assistent für die Bibliothek, bei der man prüfen kann, ob ein Buch bereits ausgeliehen wurde oder generell verfügbar ist.
Zudem ist es möglich, ein Buch zu reservieren, unabhängig davon ob dieses bereits in der Ausleihe ist oder nicht.
Ist ein Buch bereits ausgeliehen, so bietet der Bot die Möglichkeit an, dieses für einen nach dessen Ausleihzeit automatisch vorzureservieren.
Eine weitere Funktion ist das Suchen eines Buches anhand eines sich im Buch befindlichen Textes

# Installation

```bash
pip install -r requirements.txt
```

Weitere Beschreibungen

Verwendete Versionen:

- Python 3.13.5
- streamlit 1.51.0
- nltk 3.9.2
- speechrecognition 3.10.0
- elevenlabs 0.1.1

# Basic Usage
Um streamlit lokal zu starten:

```bash
streamlit run app.py
```


Videolink Screencast: https://mygit.th-deg.de/cr29549/sas-de-ws-25-26/-/wikis/screencast

# Weitere Kapitel

Das Projekt wurde wie folgt strukturiert:

- app.py - Hauptprogramm
- assets - alle json Dateien (Buchbestand, Dialoge für die Use Cases)
- services - alle usecases inkl. Spracheingabe als auch Sprachausgabe werden hier verarbeitet