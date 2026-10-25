# Abschluss-Selbstcheck

**Pflicht, bevor eine H5P-Datei als fertig gemeldet wird.**

Der Grund für diese Liste: Bei einer langen Bearbeitung gehen einzelne
Schritte verloren, auch wenn sie bekannt sind — allen voran Metadaten und
Quellenangaben. Ein „ich habe daran gedacht" aus der Erinnerung reicht
nicht. **Jeder Punkt wird aktiv gegen die fertige Datei geprüft**, nicht
gegen das Gedächtnis.

Vieles davon nimmt `scripts/h5p_check.py --all DATEI.h5p` ab; die Punkte,
die Urteilsvermögen brauchen, bleiben Handarbeit.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' checkliste.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | Automatisch prüfbar | 27–68 |
> | Handarbeit | 69–97 |
> | Danach | 98–109 |
<!-- /INDEX -->

## Automatisch prüfbar

- [ ] **Medien-Metadaten vollständig.** Jedes `H5P.Image`, `H5P.Audio`,
      `H5P.Video` im gesamten `content.json` — alle Kapitel, auch das
      letzte — hat nicht-leere `authors` **und** `source`.
      *Der am häufigsten vergessene Punkt.*
- [ ] **`copyright.license` nur mit zulässigen Werten.** CC0 im
      `copyright`-Objekt einer Datei als `{"license": "PD", "version":
      "CC0 1.0"}`, nie `"CC0 1.0"` (nur in `metadata` gültig). Sonst beim
      ersten Anzeigen „Ungültig ausgewählte Option bei Auswahl" —
      `medien.md`, „Zwei Copyright-Felder".
- [ ] **Interaktives Video: Aufgaben-Kreis in der Folienleiste.** Jedes
      `H5P.InteractiveVideo` mit Aufgaben (`assets.interactions`) hat
      `assets.endscreens` mit mindestens dem Eintrag am Videoende:
      `[{"time": <Dauer in s, abgerundet>, "label": "<m:ss> Antwortübermittlung"}]`.
      Fehlt `endscreens`, hält die Course Presentation die Folie nicht für
      eine Aufgabe und zeigt keinen weißen Kreis in der Leiste (die
      Bibliothek setzt `isTask` nur, wenn `endscreens` definiert ist).
      Der H5P-Editor lässt den Eintrag gelegentlich weg — **beim Bauen
      und bei jeder Überarbeitung immer gleich mitsetzen**, nicht erst
      nach Rückmeldung. **Die Länge immer aus dem Video selbst besorgen**
      (mp4 messen, `ffprobe` bzw. mvhd-Dauer), nie aus Untertiteln oder
      Interaktionszeiten schätzen. Hat die Datei nur den YouTube-Link,
      das passende mp4 suchen (Import, Archiv oder das eingebettete mp4
      der `-Video`-Fassung desselben Themas). Mehrere Videos in einer
      Datei: jedes Interaktive Video einzeln prüfen. (Fälle 5.1.7 und 5.1.9,
      12.10.26; `projekt_check.py` meldet es als FEHLER.)
- [ ] **Quellenangaben aktuell.** Keine Verweise mehr auf eine veraltete
      Domain; echte Inhaltslinks unverändert. *Der zweithäufigste.*
- [ ] **Bibliotheksversionen konsistent** (`find_mismatches`) — und bei
      einer Sammlung zusätzlich einheitlich (`find_outdated`).
- [ ] **Keine LaTeX-Reste** im gesamten `content.json`.
- [ ] **Keine unsichtbaren Sonderzeichen** (`strip_invisible` meldet 0).
- [ ] **Keine verwaisten Mediendateien** im Arbeitsverzeichnis, bevor
      gepackt wird.
- [ ] **Kein Kapitel leer** — besonders wenn zwischendurch jemand im
      Editor gespeichert hat (siehe `technik.md`, Editor-Fallstricke).
- [ ] **Zip-Integrität** (`testzip()` ergibt `None`) — auf der **final
      ausgelieferten** Datei, nicht auf einer Zwischenversion.
- [ ] **Keine Verzeichnis-Einträge**, nur ASCII-Dateinamen, Root-Ebene
      sauber (`h5p.json` und die Bibliotheksordner; ein vorhandenes
      `mimetype` ist erlaubt, sonst nichts).
- [ ] **Dateigröße plausibel** — passt sie zu dem, was in der Datei sein
      soll? Eine Variante ohne eingebettete Videos darf nicht so groß sein
      wie die mit.

## Handarbeit

- [ ] **Alt-Texte und Bildtitel** bei jedem Bild gesetzt und **passend zum
      tatsächlichen Bildinhalt** (Copy-Paste-Reste!). `decorative`-Flags
      geprüft.
- [ ] **Synonyme** bei jeder `H5P.Blanks`-Lücke ergänzt, wo sinnvoll — und
      aufgelistet, was ergänzt wurde.
- [ ] **Layout-Konsistenz-Check** über **alle** Folien gelaufen, inklusive
      Suche nach alten Layout-Resten (verwaiste Shapes, alte
      Vollbild-Audio-Player).
- [ ] **Relativ positionierte Elemente neu berechnet**, wo sich Titel
      geändert haben.
- [ ] **Rechtschreibprüfung auch über `h5p.json`** (`title`,
      `extraTitle`), nicht nur über die Folieninhalte.
- [ ] **Versteckte Inhalte geprüft** — Interaktionen in
      `H5P.InteractiveVideo`, verschachtelte Unterinhalte.
- [ ] **Dateiname und Cover-Versionstext** auf das aktuelle Datum gebracht
      — beide, auch bei einer Ein-Zeilen-Korrektur.
- [ ] **Jede Folie hat einen passenden Titel** (`keywords`).
- [ ] **Kein Scrollen**: Mock-up-Überlaufprüfung (`mockup_render.py`) für
      alle Folien gelaufen, unterste Textkante ≤ ca. 545 px.
- [ ] **Keine `<table>`** in Textfeldern (Spalten-Textfelder statt dessen).
- [ ] **Quiz-Hintergründe** nach Regel (QuestionSet-Bild; CoursePresentation
      einfarbig getönt, kein Muster).
- [ ] **Untertitelspuren** vollständig, Labels in Muttersprache,
      Reihenfolge wie festgelegt, Cue-Zahl je Sprache = Quelle.
- [ ] **Sichtprüfung**: Mock-up-Rendering angesehen oder die Datei im
      Editor gegengelesen.

## Danach

Eine Fertigmeldung von Claude ist **keine Freigabe**. Erst wenn der Mensch
die Datei tatsächlich geöffnet und akzeptiert hat, ist sie fertig.

Kommen danach noch Fehlermeldungen: **erst die Fehler beheben, neu packen
und verifizieren** — und erst dann Regeln oder Dokumentation anpassen.

Hat der Mensch zwischendurch selbst im Editor gespeichert, danach **von
sich aus** die Kapitel auf Leere prüfen, auch wenn er nichts gemeldet hat
(siehe `technik.md`). Dieser Fehler ist schon mehrfach zweimal
hintereinander an derselben Datei aufgetreten.
