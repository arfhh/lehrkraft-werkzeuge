# Abschluss-Selbstcheck

**Pflicht, bevor eine H5P-Datei als fertig gemeldet wird.**

Der Grund für diese Liste: Bei einer langen Bearbeitung gehen einzelne
Schritte verloren, auch wenn sie bekannt sind — allen voran Metadaten und
Quellenangaben. Ein „ich habe daran gedacht" aus der Erinnerung reicht
nicht. **Jeder Punkt wird aktiv gegen die fertige Datei geprüft**, nicht
gegen das Gedächtnis.

Vieles davon nimmt `scripts/h5p_check.py --all DATEI.h5p` ab; die Punkte,
die Urteilsvermögen brauchen, bleiben Handarbeit.

## Automatisch prüfbar

- [ ] **Medien-Metadaten vollständig.** Jedes `H5P.Image`, `H5P.Audio`,
      `H5P.Video` im gesamten `content.json` — alle Kapitel, auch das
      letzte — hat nicht-leere `authors` **und** `source`.
      *Der am häufigsten vergessene Punkt.*
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
