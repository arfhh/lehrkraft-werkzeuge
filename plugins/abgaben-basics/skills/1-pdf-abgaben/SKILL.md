---
name: 1-pdf-abgaben
description: Einen Satz gleichartiger PDF-Abgaben tokensparsam und vollständig auslesen — Vordruck-Abzug, Duplikaterkennung, Kontaktbogen für Handschrift.
---

# PDF-Abgaben auslesen

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — technisch, frei weitergebbar

Es geht um viele Abgaben **desselben** Formulars, von verschiedenen Personen.
Genau daraus entstehen die Tricks: was bei allen gleich ist, ist Vordruck.

## Die drei Textquellen — alle drei sind Pflicht

Wer nur den Seitentext liest, übersieht einen Teil der Antworten. Belegt an
zwei unabhängigen Sätzen: einmal hätten 11 von 20 Personen fälschlich als
„nicht bearbeitet" gegolten, im anderen Satz standen sämtliche 369 Antworten
ausschließlich in Formularfeldern.

| Quelle | Befehl | Steckt dort |
|---|---|---|
| Seitentext | `pdftotext -q datei.pdf -` | gedruckter Text, meist auch Anmerkungen |
| Formularfelder | `qpdf --json --json-key=acroform` → `fields[].value` | **alles, was in ein ausfüllbares Feld getippt wurde** |
| Anmerkungen | `qpdf --json --json-key=objects` → `/Type /Annot`, `/Subtype /FreeText`, `/Contents` | eigene Textkästen, die Lesegeräte hinzufügen |

Der Seitentext zeigt Formularfeldwerte **nicht**. Anmerkungen zeigt er
meistens, aber nicht immer. Deshalb: alle drei holen, dann gegen den
Seitentext entdoppeln (normalisierte Kleinschreibung vergleichen).

Bleibt nach allen drei Quellen nichts übrig, ist es wirklich eine Zeichnung
oder ein Scan — erst dann lohnt die Bildansicht.

## Vordruck-Abzug

Zeilen, die bei mindestens der Hälfte der Abgaben desselben Formulars
wortgleich vorkommen, sind der gedruckte Rahmen und fliegen raus. Das
halbiert den Text, braucht weder Musterlösung noch Farbinformation und
funktioniert ab etwa drei Abgaben desselben Formulars.

## Zeichenaufgaben und Handschrift

Ob eine Zeichenaufgabe überhaupt bearbeitet wurde, verrät der Anteil dunkler
Pixel: Seite mit `pdftoppm -gray -r 40` rendern, im mittleren Bereich (etwa 15
bis 78 Prozent der Höhe) die dunklen Pixel zählen. Das leere Formular liefert
einen festen Grundwert; jede Bearbeitung liegt darüber. Gemessen an einem
echten Satz: leer 0,67 Prozent, bearbeitet 2,3 bis 6,8 Prozent.

Den Grundwert nicht raten — an einem nachweislich leeren Exemplar messen. Die
Zahl gilt pro Formular, nicht allgemein, und sie **entscheidet nichts**, sie
sortiert nur vor (siehe Fallstricke).

Wie handschriftliche Abgaben danach beurteilt werden, ohne dass die Kosten
explodieren, steht in der Begleitdatei **`kontaktbogen.md`**. Kurz: Vordruck
abziehen, zuschneiden, alle Abgaben in EIN Bild. Faktor 7 bis 10.

## Prüfsummen

SHA-256 über den Dateiinhalt beantwortet zwei Fragen zum Nulltarif:

- **Geändert seit dem letzten Durchgang?** Gleiche Summe heißt unverändert,
  muss also nicht erneut gelesen werden.
- **Dublette?** Gleiche Summe bei zwei Personen heißt: dieselbe Datei.

Für inhaltliche Ähnlichkeit reicht die Dateisumme nicht — dafür SHA-256 über
den **normalisierten Eigenanteil** (Vordruck abgezogen, Leerraum
vereinheitlicht, kleingeschrieben). Identisch ist dann ein harter Befund;
alles darunter ist Graubereich und wird inhaltlich beurteilt, nicht über
eine Zahl entschieden.

## Ähnlichkeit nur bei Freitext prüfen

Lücken-, Rechen- und Zuordnungsaufgaben haben je Feld genau eine richtige
Antwort. Dort sind alle richtigen Abgaben zwangsläufig fast gleich — eine
Ähnlichkeitsprüfung erzeugt nur Fehlalarme und begräbt den einen echten Fall
unter sechzig falschen.

Das Trennmaß ist die **Länge der Einzelantworten**: liegt ihr Median unter
etwa 25 Zeichen, wird das Blatt von der Ähnlichkeitsprüfung ausgenommen.
Gemessen an echten Sätzen: Lückentext 6 bis 12 Zeichen, Freitextaufgabe 140
bis 365. Die Prüfung auf **identischen** Inhalt bleibt in beiden Fällen
sinnvoll.

## Was das kostet

Gemessen an 91 Seiten:

| Weg | Größenordnung |
|---|---|
| Seiten als Bild ansehen (150 dpi) | ~200 000 Token |
| drei Textquellen zusammen | ~15 000 |
| davon Vordruck abgezogen | ~7 500 |

Faktor 25 bis 30. Deshalb gilt: Bildansicht erst, wenn alle drei Textquellen
leer sind, und dann über den Kontaktbogen statt Seite für Seite.

## Begleitdateien

Im gleichnamigen Werkzeug-Ordner:

| Datei | Wann |
|---|---|
| `kontaktbogen.md` | sobald handschriftlich oder gezeichnet bearbeitet wurde |
| `scripts/abgaben_lesen.py` | zum Auslesen; braucht nur `poppler-utils` und `qpdf` |
| `scripts/kontaktbogen.py` | für den Kontaktbogen; braucht zusätzlich `numpy` und `Pillow` |

| Aufruf von `abgaben_lesen.py` | Ergebnis |
|---|---|
| `… <wurzel>` | Eigenanteil je Person, lesbar |
| `… --json` | dasselbe maschinenlesbar, mit Prüfsummen |
| `… --leer` | nur: was hat keinen Text und braucht Bildansicht |
| `… --dubletten` | identische Inhalte und Ähnlichkeit ab 70 Prozent |

## Fallstricke

- **Erst zählen, dann glauben.** Ein Formular mit auffällig wenig Text ist
  fast immer ein Formular, dessen Felder nicht ausgelesen wurden.
- **Angehängte Zähler im Dateinamen entfernen, bevor gruppiert wird.** Beim
  zweiten Herunterladen hängen Browser und Betriebssystem ein „ 2" oder „ 3"
  an — es bleibt dasselbe Arbeitsblatt. Ohne diese Entdoppelung landen die
  Abgaben in verschiedenen Gruppen: belegt, dass zwei zeichengleiche Abgaben
  deshalb NICHT als Dublette gemeldet wurden.
- **Dateinamen zuerst nach NFC normalisieren.** Manche Systeme legen sie in
  NFD ab (Grundbuchstabe plus kombinierendes Zeichen). Eine Umlaut-Ersetzung
  greift dann nicht, und ein Namensabgleich schlägt **still** fehl — ohne
  Fehlermeldung, mit falschem Ergebnis.
- **Der Tintenanteil entscheidet nicht.** Eine blass gezeichnete Abgabe kann
  denselben Wert haben wie ein leeres Formular (belegt: 2,41 gegen 2,13
  Prozent). Der Wert sortiert vor, angesehen wird trotzdem.
- **Dateinamen sind keine verlässliche Quelle** für die Zuordnung zu einer
  Aufgabe, und sie können personenbezogene Angaben enthalten.
- **Ein Scan bleibt ein Scan.** Ohne Textebene hilft nur die Bildansicht;
  OCR über Handschrift ist unzuverlässiger als das eigene Hinsehen.
