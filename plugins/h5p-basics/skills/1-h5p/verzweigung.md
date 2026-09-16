# Verzweigte Lernpfade: H5P.BranchingScenario

Ein **Branching Scenario** (deutsch „Verzweigung") ist ein Lernpfad, bei dem
die Antwort auf eine Frage bestimmt, welcher Inhalt als nächstes kommt.
Diese Referenz beschreibt, wie so ein Paket auf Dateiebene aufgebaut und
gebaut wird. Für Packen, Bibliotheksprüfung und Fehlersuche gilt unverändert
`technik.md`, für die Herkunft der Bibliotheksordner `basispakete.md`.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' verzweigung.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | 1. Der Baum läuft immer von oben nach unten | 27–47 |
> | 2. Bibliotheksversionen — die benannte Ausnahme | 48–77 |
> | 3. Aufbau der `content.json` | 78–119 |
> | 4. Ein `BranchingQuestion`-Knoten | 120–175 |
> | 5. Routing über `nextContentId` | 176–186 |
> | 6. Bau-Pipeline | 187–288 |
> | 7. Vor dem Upload prüfen | 289–301 |
> | 8. Häufige Fehlermeldungen | 302–309 |
<!-- /INDEX -->

## 1. Der Baum läuft immer von oben nach unten

Ein Branching Scenario ist intern ein **gerichteter Baum**, der von der
Startfrage nach unten wächst; der Editor zeichnet ihn genau so.

- Der **Vorwärtsweg** und alle **Verzweigungen** zeigen auf einen Knoten
  weiter unten — nie nach oben.
- **Rücksprünge** („bei falscher Antwort eine Ebene zurück") sind deshalb
  kein nach oben wachsender Ast, sondern ein **Verweis auf einen bereits
  vorhandenen Knoten**. Im Editor erscheint das als „Zu vorhandenem Inhalt
  springen" — eine beschriftete Verknüpfung, kein neuer Kasten.

**Folge für die Planung:** erst den kompletten Vorwärts-Baum von oben nach
unten aufbauen, dann die Rücksprünge als Verweise setzen. Jeder Knoten kennt
nur seine eigene Nummer (= Position im Array) und zeigt per Nummer auf sein
Ziel: **vorwärts = größere Nummer, Rücksprung = kleinere Nummer.**

Der Editor kann **keine zwei echt parallelen Stränge** nebeneinander
zeichnen — er stellt immer einen Baum dar (Tiefensuche). Zwei „parallele"
Stränge sind also eine Frage der Darstellung, kein Verdrahtungsfehler.

## 2. Bibliotheksversionen — die benannte Ausnahme

Sonst gilt in dieser Skill: Versionsnummern werden aus der Datei ausgelesen,
nie fest verdrahtet. Hier gibt es eine belegte Ausnahme:

| Punkt | Wert | Warum |
|---|---|---|
| Hauptbibliothek | **H5P.BranchingScenario 1.8** (z. B. 1.8.10) | Version **1.11 / master** setzt H5P Core-API **1.28** voraus. Diese Core-Version ist auf vielen Servern (u. a. verbreiteten Community-Instanzen und Lumi) nicht erfüllt; der Import scheitert dann mit „missing main library" bzw. „api-version-unsupported". |
| Fragetyp | **H5P.BranchingQuestion 1.0** (z. B. 1.0.20) | Die zu 1.8 passende Verzweigungsfrage. |
| `embedTypes` | `["div"]` | Wie in den Exporten der gängigen Zielsysteme. |

Praktische Konsequenzen:

- **Bibliotheken nie von Hand zusammensuchen.** Ein Basispaket oder ein
  Export einer leeren Verzweigung aus dem Zielsystem bringt alle
  Bibliotheken in zueinander passenden Versionen mit; ausgetauscht wird nur
  `content/content.json` plus einzelne Felder in `h5p.json` (Ablauf:
  `basispakete.md`).
- **„Neuer ist besser" gilt hier nicht.** Beim Lauf von `find_outdated()`
  (siehe `technik.md`) bleiben `H5P.BranchingScenario` und
  `H5P.BranchingQuestion` bewusst auf dem Stand des Basispakets — ein
  Anheben macht das Paket auf dem Zielserver unbrauchbar.
- Vor dem Anheben in einem konkreten Fall zuerst prüfen, welche Core-API
  der Zielserver anbietet. Erfüllt er 1.28, entfällt die Einschränkung.

Typische Bibliotheken in so einem Paket — nur zur Orientierung, maßgeblich
ist immer das eigene Paket: `H5P.BranchingScenario`, `H5P.BranchingQuestion`,
`H5P.CoursePresentation`, `H5P.AdvancedText`, `H5P.Image`, `H5P.Audio`,
`H5P.JoubelUI`, `H5P.FontIcons`, `H5P.Transition`, `FontAwesome`.

## 3. Aufbau der `content.json`

Oberste Ebene ist der Schlüssel `branchingScenario`:

```json
{
  "branchingScenario": {
    "startScreen": {
      "startScreenTitle": "Titel des Pfades",
      "startScreenSubtitle": "Ein Satz zur Aufgabe"
    },
    "endScreens": [
      {
        "endScreenTitle": "Geschafft!",
        "endScreenSubtitle": "Abschlusstext.",
        "contentId": -1,
        "endScreenScore": 0
      }
    ],
    "content": [ "… Array aller Knoten …" ],
    "scoringOptionGroup": {
      "scoringOption": "no-score",
      "includeInteractionsScores": true
    },
    "behaviour": {
      "enableBackwardsNavigation": false,
      "forceContentFinished": false,
      "randomizeBranchingQuestions": true
    },
    "l10n": { }
  }
}
```

- **`content` ist das Array aller Knoten, und die Position im Array *ist*
  die Knotennummer** (Index 0 = erster Knoten). Die Knoten haben kein
  eigenes `contentId`-Feld — ihre Identität ist allein die Array-Position.
  Wird ein Knoten eingefügt oder gelöscht, verschieben sich alle folgenden
  Nummern und **alle** Verweise darauf müssen mitgezogen werden.
- **`l10n`** (alle Beschriftungen der Oberfläche) 1:1 aus dem Basispaket
  übernehmen, nicht selbst schreiben.

## 4. Ein `BranchingQuestion`-Knoten

```json
{
  "type": {
    "library": "H5P.BranchingQuestion 1.0",
    "params": {
      "branchingQuestion": {
        "question": "<h3><strong>Welche Aussage passt?</strong></h3><p>Wähle eine Antwort:</p>",
        "alternatives": [
          {
            "text": "Antwort A",
            "nextContentId": 5,
            "feedback": { "title": "Richtig!", "subtitle": "Weiter geht es." }
          },
          {
            "text": "Antwort B",
            "nextContentId": 4,
            "feedback": { "title": "Leider falsch.", "subtitle": "Eine Stufe zurück." }
          }
        ]
      }
    },
    "subContentId": "<zufällige UUID>",
    "metadata": {
      "contentType": "Branching Question",
      "license": "U",
      "title": "Frage 2A"
    }
  },
  "showContentTitle": false,
  "proceedButtonText": "Weiter",
  "forceContentFinished": "useBehavioural",
  "feedback": { "title": "", "subtitle": "" },
  "contentBehaviour": "useBehavioural"
}
```

- **`question` ist HTML** (innerHTML): Überschrift über
  `<h3><strong>…</strong></h3>`, Fließtext über `<p>…</p>`.
- **`metadata.title`** ist der Titel im Editor-Baum. Sprechende Namen
  vergeben — in einem größeren Baum ist das der einzige Anhaltspunkt, um
  einen Knoten wiederzufinden.
- **`subContentId`** muss je Knoten eine eigene UUID sein. Doppelte
  `subContentId`s lassen den Inhalt still nicht laden.
- Jede `alternative` hat `feedback.title` und `feedback.subtitle`; dort
  lassen sich im Editor später auch Bilder ergänzen.
- **`metadata.license: "U"`** an einem Knoten ohne Medien ist unkritisch:
  Es ist die Lizenz **dieses einen Elements**, nicht die des Pakets. Die
  Paketlizenz steht getrennt davon in `h5p.json` (`license` als Code ohne
  Versionsnummer, `licenseVersion` separat — siehe `basispakete.md`), und
  beide Angaben dürfen sich unterscheiden. Sobald ein Bild oder Audio im
  Knoten oder im Feedback liegt, gilt dafür die Medien-Regel aus
  `medien.md`: Metadaten vollständig füllen und `"U"` nicht blind in eine
  freie Lizenz umdeuten.

## 5. Routing über `nextContentId`

- **`nextContentId`** = Array-Index des Zielknotens.
- **`nextContentId: -1`** = Sprung auf den Endbildschirm.
- **Vorwärts** = größere Nummer, **Rücksprung** = kleinere Nummer (das ist
  technisch dasselbe wie „zu vorhandenem Inhalt springen").
- **`randomizeBranchingQuestions: true`** mischt die Antwortreihenfolge zur
  Laufzeit. Deshalb darf die richtige Antwort im Array an erster Stelle
  stehen: in der Quelldatei bleibt alles übersichtlich, angezeigt wird
  trotzdem gemischt.

## 6. Bau-Pipeline

1. Basispaket entpacken (`h5p_pack.unpack()`).
2. `content/content.json` neu erzeugen — Knoten von oben nach unten in ein
   Array schreiben.
3. In `h5p.json` nur `title`, `authors`, `license`, `licenseVersion`
   anpassen; `mainLibrary` und `preloadedDependencies` unverändert lassen.
4. Selbst-Check laufen lassen (unten).
5. Packen mit `h5p_pack.pack()`. Rohe `zip`-Aufrufe sind auch hier kein
   eigener Weg — die Regel „keine Verzeichniseinträge im Archiv" und alles
   Weitere zum Packen steht in `technik.md`.

**Knoten erzeugen:**

```python
# -*- coding: utf-8 -*-
import json, uuid

def frage(titel, frage_html, antworten):
    """antworten = [(text, ziel_index, fb_titel, fb_text), …]"""
    alts = [{"text": t, "nextContentId": z,
             "feedback": {"title": ft, "subtitle": fx}}
            for (t, z, ft, fx) in antworten]
    return {
        "type": {
            "library": "H5P.BranchingQuestion 1.0",
            "params": {"branchingQuestion": {"alternatives": alts,
                                             "question": frage_html}},
            "subContentId": str(uuid.uuid4()),
            "metadata": {"contentType": "Branching Question",
                         "license": "U", "title": titel},
        },
        "showContentTitle": False,
        "proceedButtonText": "Weiter",
        "forceContentFinished": "useBehavioural",
        "feedback": {"title": "", "subtitle": ""},
        "contentBehaviour": "useBehavioural",
    }

def html(ueberschrift, aufforderung):
    return f"<h3><strong>{ueberschrift}</strong></h3><p>{aufforderung}</p>"

# --- Knoten von OBEN nach UNTEN aufbauen (Index = Reihenfolge) ---
content = []

# 0: Startfrage; die falsche Antwort springt auf denselben Knoten zurück
content.append(frage("Frage 1",
    html("Erste Frage", "Wähle eine Antwort:"),
    [("Antwort A", 1, "Richtig!", "Weiter."),
     ("Antwort B", 0, "Falsch.",  "Noch einmal.")]))

# 1: letzte Frage; die richtige Antwort zeigt mit -1 auf den Endbildschirm
content.append(frage("Frage 2",
    html("Zweite Frage", "Wähle eine Antwort:"),
    [("Antwort A", -1, "Geschafft!", ""),
     ("Antwort B",  0, "Falsch.",    "Zurück zum Start.")]))

# --- Basispaket laden, Inhalt ersetzen, speichern ---
vorlage = json.load(open("arbeit/content/content.json"))
bs = vorlage["branchingScenario"]
bs["content"] = content
bs["startScreen"] = {"startScreenTitle": "Titel",
                     "startScreenSubtitle": "Untertitel"}
bs["endScreens"] = [{"endScreenTitle": "Geschafft!",
                     "endScreenSubtitle": "Abschlusstext.",
                     "contentId": -1, "endScreenScore": 0}]
bs["behaviour"]["randomizeBranchingQuestions"] = True
json.dump(vorlage, open("arbeit/content/content.json", "w"),
          ensure_ascii=False, indent=2)
print("content.json geschrieben:", len(content), "Knoten")
```

**Selbst-Check vor dem Packen — Pflicht.** Er prüft zwei Dinge, die man
einem Baum von Hand nicht ansieht: dass jedes Sprungziel existiert und dass
jeder Knoten vom Start aus erreichbar ist.

```python
import json
from collections import deque
c = json.load(open("arbeit/content/content.json"))["branchingScenario"]["content"]
N = len(c)

def ziele(n):
    bq = n["type"]["params"].get("branchingQuestion")
    return [a["nextContentId"] for a in bq["alternatives"]] if bq else [n.get("nextContentId")]

for i, n in enumerate(c):                       # alle Ziele gültig?
    for t in ziele(n):
        assert t == -1 or 0 <= t < N, f"Knoten {i}: ungültiges Ziel {t}"

seen, q = {0}, deque([0])                       # erreichbar von 0?
while q:
    for t in ziele(c[q.popleft()]):
        if t != -1 and t not in seen:
            seen.add(t); q.append(t)
print("erreichbar:", len(seen), "/", N,
      "| nicht erreichbar:", sorted(set(range(N)) - seen) or "keine")
```

Der Check wird **nach jeder Bearbeitung im Editor erneut** gefahren:
Editoren nummerieren Knoten beim Speichern um.

## 7. Vor dem Upload prüfen

Zusätzlich zum allgemeinen Selbstcheck (`checkliste.md`):

- [ ] Bibliotheken aus einem Basispaket/Export, `BranchingScenario 1.8`.
- [ ] `h5p.json`: `mainLibrary` = `H5P.BranchingScenario`, Lizenzcode ohne
      Versionsnummer.
- [ ] Jeder Knoten hat eine eigene `subContentId`.
- [ ] Alle `nextContentId` zeigen auf gültige Indizes oder `-1`.
- [ ] Selbst-Check: alle Knoten erreichbar, keine ungültigen Ziele.
- [ ] Vorwärtsweg und Verzweigungen zeigen nach unten, Rücksprünge sind
      Verweise auf vorhandene Knoten.

## 8. Häufige Fehlermeldungen

| Meldung beim Import | Ursache | Lösung |
|---|---|---|
| „missing main library" / „api-version-unsupported" | BranchingScenario 1.11/master, das Core-API 1.28 verlangt | Bibliotheken aus einem Basispaket mit 1.8 nehmen (Abschnitt 2) |
| „File 'content/' not allowed" | Verzeichnis-Eintrag im ZIP | mit `h5p_pack.pack()` packen (`technik.md`) |
| Lizenz-/Validierungsfehler | `license` in `h5p.json` enthält die Versionsnummer | Code und `licenseVersion` trennen |
| Inhalt lädt nicht, ein Knoten fehlt | ungültige `nextContentId` oder doppelte `subContentId` | Selbst-Check laufen lassen (Abschnitt 6) |
