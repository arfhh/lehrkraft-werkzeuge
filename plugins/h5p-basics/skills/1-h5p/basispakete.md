# Eine .h5p-Datei aus einem Basispaket bauen

Ein **Basispaket** ist eine schlanke `.h5p`-Datei, die die vollständigen
H5P-Programmbibliotheken (JavaScript, CSS) eines Inhaltstyps enthält, aber
nur einen generischen Platzhalterinhalt. Damit lässt sich eine fertige
Datei bauen, ohne den grafischen Editor zu öffnen: entpacken,
`content/content.json` durch den eigenen Inhalt ersetzen, neu packen.

Das löst das schwierigste Problem beim Bauen von Hand — vollständige
Bibliotheksordner in zueinander passenden Versionen zu beschaffen.

Die Pakete liegen als `.h5p`-Dateien im Unterordner `H5P-Basispakete/`
desselben Werkzeug-Ordners, in dem auch diese Datei liegt. Diese Referenz
beschreibt, wie mit ihnen gearbeitet wird.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' basispakete.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | Herkunft und Lizenz der hier beschriebenen Pakete | 32–42 |
> | Inventar | 43–60 |
> | Ablauf: ein vorhandenes Basispaket nutzen | 61–81 |
> | Ablauf: ein neues Basispaket aufbereiten | 82–101 |
> | Zwei Fallstricke | 102–116 |
> | Prüfung eines Basispakets | 117–125 |
<!-- /INDEX -->

## Herkunft und Lizenz der hier beschriebenen Pakete

Die Sammlung stammt aus dem Toolkit der Barcamp-Session „KI und ZUM-Apps",
OERcamp 2026. Lizenz **CC BY 4.0**. Bei Weitergabe sind zu nennen:

- **ZUM Deutsch Lernen** (alle Pakete)
- **Ralf Klötzke** (das Branching-Scenario-Paket)

Die enthaltenen H5P-Bibliotheken sind überwiegend MIT-lizenziert; Ausnahmen
sind MaterialDesignIcons (GPL3) und TextUtilities (Public Domain).

## Inventar

| Basispaket | Hauptbibliothek | mitgelieferte Bibliotheken |
|---|---|---|
| BranchingScenario | H5P.BranchingScenario 1.8 | + H5P.BranchingQuestion 1.0, AdvancedText, Image, FontAwesome |
| CoursePresentation | H5P.CoursePresentation 1.25 | 6 |
| DialogCards | H5P.Dialogcards 1.9 | 6 |
| ImageHotspots | H5P.ImageHotspots 1.10 | 5 |
| ImageHotspotsZUM | H5P.ImageHotspotsZUM 1.9 | 11 |
| InteractiveVideo | H5P.InteractiveVideo 1.26 | 12 |
| Matching | H5P.Matching 1.0 | 5 |
| SortParagraphs | H5P.SortParagraphs 0.11 | 7 |
| Summary | H5P.Summary 1.10 | 6 |
| „Verständnischeck" | H5P.QuestionSet 1.20 | + Blanks 1.14, DragQuestion 1.14, DragText 1.10, Essay 1.5, MarkTheWords 1.11, MultiChoice 1.16, MultiMediaChoice 0.3, TrueFalse 1.8 |

Die Versionen sind der Stand der jeweiligen Sammlung, keine Sollwerte —
vor dem Bauen immer aus dem Paket auslesen.

## Ablauf: ein vorhandenes Basispaket nutzen

1. **Passendes Paket wählen.** Fehlt der Inhaltstyp, zuerst den Abschnitt
   „Ein neues Basispaket aufbereiten" durchgehen.
2. **Entpacken** in ein leeres Arbeitsverzeichnis (`h5p_pack.unpack()`).
   Liegt das Paket als Base64-Textdatei vor, vorher `base64 -d`
   dekodieren — solche Dateien haben bis zu drei Millionen Zeichen und
   werden **niemals** als Text geöffnet oder in den Kontext geladen.
3. **`content/content.json` ersetzen.** Welche Felder Pflicht sind und wie
   sie verschachtelt werden, steht in der `semantics.json` der
   Hauptbibliothek — sie liegt im gleichnamigen Bibliotheksordner und ist
   die verlässliche Quelle, wenn ein Feld unklar ist.
4. **`h5p.json` anpassen:** `title` auf den neuen Inhalt setzen.
   `mainLibrary` und `preloadedDependencies` **unverändert lassen** — sie
   beschreiben die mitgelieferten Bibliotheken. Lizenzfeld als
   Top-Level-Feld, Lizenzcode ohne Version (`"license": "CC BY"` plus
   `"licenseVersion": "4.0"`), nicht als kombinierter String.
5. **Packen** mit `h5p_pack.pack()`, also ohne Verzeichniseinträge im ZIP.
6. **Abschluss-Selbstcheck** nach `references/checkliste.md`, dann hochladen
   und im Vorschaumodus testen: Interaktion, Feedback, mobile Ansicht.

## Ablauf: ein neues Basispaket aufbereiten

Nötig, wenn ein Inhaltstyp in der Sammlung fehlt.

1. **Rohexport besorgen:** eine bestehende Übung des gewünschten
   Inhaltstyps aus dem Zielsystem als `.h5p` exportieren.
2. **Entpacken und sichten:** `content/`, `h5p.json` und alle
   Bibliotheksordner (`H5P.*`, `H5PEditor.*`, …).
3. **Laufzeit-Abhängigkeiten ermitteln:** nur die `preloadedDependencies`
   der Hauptbibliothek, rekursiv verfolgt. Die `H5PEditor.*`-Bibliotheken
   werden zur Anzeige nicht gebraucht und bleiben draußen — sie machen
   einen großen Teil der Dateigröße aus.
4. **Inhalt auf Platzhalter reduzieren:** `content/content.json` auf ein
   minimales, generisches Beispiel kürzen, alle Mediendateien entfernen.
   Die vorhandenen Pakete liegen damit bei 600 Byte bis 2 KB Inhalt.
5. **`h5p.json` bereinigen:** generischer Titel, Lizenzfelder setzen,
   `preloadedDependencies` auf die ermittelte Liste kürzen.
6. **Packen und testen:** hochladen, im Vorschaumodus prüfen, erst dann in
   die Sammlung aufnehmen.

## Zwei Fallstricke

**Nie zwei Basispakete zusammenkopieren.** Die Bibliotheksversionen
widersprechen sich zwischen den Paketen — belegt sind MultiChoice 1.14
gegen 1.16, Question 1.4 gegen 1.5, TrueFalse 1.6 gegen 1.8. Wer Ordner aus
zwei Paketen mischt, erzeugt genau den Versionsfehler aus
`references/technik.md`. Wird ein Inhaltstyp gebraucht, den ein Paket nicht
mitbringt, wird stattdessen ein neues Basispaket nach dem Verfahren oben
aufbereitet.

**Interactive Book fehlt in der Sammlung.** Ausgerechnet der Inhaltstyp,
der mehrere CoursePresentations zu einem Buch bündelt, ist nicht dabei und
muss über das Aufbereitungsverfahren aus einem frischen Export selbst
gebaut werden.

## Prüfung eines Basispakets

Ein brauchbares Basispaket erfüllt alle vier Punkte:

- `zipfile.testzip()` meldet keinen Fehler
- keine Verzeichniseinträge im Archiv (kein Eintragsname endet auf `/`)
- `content/content.json` ist vorhanden
- `h5p.json` nennt `mainLibrary`, und der zugehörige Bibliotheksordner
  liegt im Paket
