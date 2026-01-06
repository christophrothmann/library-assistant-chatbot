Rothmann Christoph, 22411549

Goleo - Der Bibliotheksassistent

# Project description

[Link zum Code-Repo](https://mygit.th-deg.de/cr29549/sas-de-ws-25-26.git)

[Link zum Wiki](https://mygit.th-deg.de/cr29549/sas-de-ws-25-26/-/wikis/home)

Der **Goleo Bibliotheksassistent** ist eine interaktive Anwendung zur Unterstützung von Bibliotheksnutzern. Er ermöglicht die Prüfung der Verfügbarkeit von Büchern, Reservierungen, das Lokalisieren von Büchern im Regal sowie eine Volltextsuche innerhalb des Buchbestands.

Das Projekt nutzt **Streamlit** für das Frontend und verschiedene Python-Bibliotheken für Sprachverarbeitung (NLP) und Sprachausgabe (TTS).

---

## Installation

Um das Projekt lokal auszuführen, folgen Sie diesen Schritten:

### 1. Repository klonen

Laden Sie das Projektverzeichnis auf Ihren lokalen Rechner.

```bash
git clone https://mygit.th-deg.de/cr29549/sas-de-ws-25-26.git
cd sas-de-ws-25-26
```

### 2. Virtuelle Umgebung erstellen (Optional, aber empfohlen)

Es wird empfohlen, eine virtuelle Python-Umgebung zu nutzen, um Abhängigkeitskonflikte zu vermeiden.

**Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

Installieren Sie alle benötigten Bibliotheken aus der `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Anwendung starten

Starten Sie die Streamlit-Anwendung über das Terminal:

```bash
streamlit run app.py
```

Die Anwendung wird automatisch in Ihrem Standard-Browser unter `http://localhost:8501` geöffnet.

---

## Basic Usage

Link zum Screencast: [Youtube Video](https://youtu.be/ZQLCibq9WOg)

Hier eine Übersicht der wichtigsten verwendeten Bibliotheken und deren Funktion im Projekt:

### **NLTK (Natural Language Toolkit)**

Die Bibliothek **NLTK** wird für das Verständnis der natürlichen Sprache des Nutzers verwendet (Natural Language Understanding).

- **Funktion**: Sie ermöglicht dem Chatbot, die Intention (Absicht) hinter einer Nutzereingabe zu erkennen (Intent Classification).
- **Einsatz**: Mithilfe eines Naive-Bayes-Klassifikators analysiert der Bot Sätze wie "Wo finde ich das Buch?" oder "Ich möchte reservieren" und ordnet sie den entsprechenden Funktionen (`regalsuche`, `reservieren`) zu.

### **edge_tts (Edge Text-to-Speech)**

**edge_tts** ist eine Python-Bibliothek, die die Text-to-Speech-Engine von Microsoft Edge nutzt.

- **Funktion**: Sie wandelt die Textantworten des Chatbots in natürlich klingende Sprache um.
- **Einsatz**: Wenn die Audioausgabe aktiviert ist, generiert diese Bibliothek MP3-Audiodaten, die dem Nutzer direkt im Chat vorgespielt werden. Sie bietet eine hohe Sprachqualität ohne komplexe API-Schlüssel-Konfiguration.

### **Streamlit**

Das Framework für die Benutzeroberfläche.

- Ermöglicht die schnelle Entwicklung einer interaktiven Web-App rein mit Python.

### **SpeechRecognition**

Ermöglicht die Umwandlung von gesprochener Sprache (via Mikrofon) in Text, sodass der Nutzer mit dem Assistenten sprechen kann.

---

## Projektstruktur

- `app.py`: Hauptdatei der Anwendung (Einstiegspunkt).
- `assets/`: Enthält statische Dateien wie JSON-Datenbanken (`buecher_bestand.json`, `training_data.json`) und Bilder.
- `services/`: Beinhaltet die Logikmodule für die verschiedenen Funktionen (z.B. `reservieren.py`, `verfuegbarkeit.py`, `intent_classifier.py`).

---

Disclaimer:
Die README Datei wurde mithilfe von Gemini 3 Pro generiert und manuell ausgestaltet.

> Prompt: Update die requirement.txt und erweitere die README Datei, wo die Einrichtung für das lokale Ausführen beschrieben wird und die einzelnen Keyfunktionen wie NLTK und edge_tts beschrieben werden
