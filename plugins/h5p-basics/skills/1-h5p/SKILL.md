---
name: "1-h5p"
description: "H5P-Dateien (.h5p) direkt auf Dateiebene erstellen, prüfen und reparieren statt nur im grafischen Editor: Paketaufbau (h5p.json, content/content.json, Bibliotheksordner), sicheres Packen (der 'File content/ not allowed'-Uploadfehler), Bibliotheksversionen ('Bibliothek H5P.X a.b ist ungültig'), Bauen aus fertigen Basispaketen ohne Editor, Medien-Metadaten und Lizenzen, Vorlese-Audio (TTS), Video einbetten statt verlinken, mehrsprachige Untertitel, Folien-Layout (Titel, kein Scrollen, Quiz-Hintergründe), Branching Scenarios, Editor-Fallstricke (Lumi löscht beim Speichern Inhalte) und eine Abschluss-Checkliste. Rein technisch und projektneutral — die didaktische Beurteilung steht in den Didaktik-Skills, Dateibenennung und Design in der Projekt-Skill. IMMER verwenden bei 'H5P', '.h5p', 'Interactive Book', 'Course Presentation', 'Lumi', 'H5P-Upload', 'Lückentext/Blanks', 'Drag and Drop', 'Branching Scenario', 'Verzweigung', 'H5P bauen/verbessern/reparieren/packen' — auch ohne Skill-Namen."
---

# H5P auf Dateiebene

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — reine Technik, frei weiterzugeben

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.

Diese Skill befähigt Claude, **H5P-Dateien direkt auf Dateiebene** zu
erstellen, zu prüfen und zu verbessern — also das zu tun, was der grafische
H5P-Editor (Lumi, Moodle, WordPress, apps.zum.de …) nicht kann: hunderte
Elemente auf einmal prüfen, Metadaten vervollständigen, Layout
vereinheitlichen, kaputte Pakete reparieren, ganze Dateien ohne Editor bauen.

Sie ist **projektneutral**: keine Annahmen über Fach, Schulform,
Ordnerstruktur oder Design. Konkrete Dateinamen, Pfade, Farbwerte und
Designvorgaben bestimmt die aufrufende Projekt-Skill.

## Was ist eine .h5p-Datei?

Ein ZIP-Archiv mit fester Struktur:

```
meine-datei.h5p
├── h5p.json                  Buch-Metadaten: title, mainLibrary,
│                             preloadedDependencies (Bibliotheksliste)
├── content/
│   ├── content.json          DER gesamte Inhalt — alle Folien, Texte,
│   │                         Aufgaben, Medienverweise, Positionen
│   ├── images/  audios/  videos/   die eingebetteten Mediendateien
└── H5P.InteractiveBook-1.11/ ein Ordner je mitgelieferter Bibliothek
    H5P.CoursePresentation-1.26/   (Name-Major.Minor)
    H5P.Blanks-1.14/ …
```

Die Versionsnummern oben sind Beispiele für das Namensmuster, keine
Sollwerte. Welche Version gilt, wird immer aus der Datei ausgelesen.

Alles Inhaltliche steckt in `content/content.json`. Es ist ein tief
verschachteltes JSON — Claude arbeitet darin **immer mit einem rekursiven
Struktur-Walk** (Dicts und Listen), nie mit blindem Suchen-und-Ersetzen im
Rohtext. Beispiel-Walk und fertige Helfer: `scripts/h5p_pack.py`.

## Ablauf einer Bearbeitung

1. **Sicherheitskopie.** Die Originaldatei bleibt unangetastet; gearbeitet
   wird auf einer Kopie. Es gibt keine Undo-Funktion.
2. **Entpacken** mit `h5p_pack.unpack()` in ein leeres Arbeitsverzeichnis.
3. **Überblick verschaffen** mit `scripts/h5p_check.py --inspect` —
   Kapitel, Folien, Elemente, Medien, Bibliotheken auf einen Blick.
   Danach erst inhaltlich lesen. Achtung: manche Inhalte verstecken sich
   (Interaktionen in einem `H5P.InteractiveVideo`, siehe
   `technik.md`).
4. **Bearbeiten** — je nach Vorhaben die passende Referenz lesen, nur die:

| Vorhaben | Referenz |
|---|---|
| Packen, Bibliotheken, Fehlersuche, kaputte Archive, Umlaut-Pfade | `technik.md` |
| Folienaufbau, Koordinaten, Titel, Hintergründe, Layout-Konsistenz, Kein-Scrollen-Regel, Tabellen, Quiz-Hintergründe | `layout.md` |
| Bilder, Audio, Video, mehrsprachige Untertitel, Lizenzen, Alt-Texte, Vorlese-Audio | `medien.md` |
| Aufgabenqualität, Blanks-Synonyme, Drag-Feedback, Versionierung | `inhalt-und-aufgaben.md` |
| Eine neue Datei ohne Editor bauen | `basispakete.md` |
| Verzweigte Lernpfade (Branching Scenario) | `verzweigung.md` |
| Vor der Auslieferung prüfen | `checkliste.md` |

5. **Abschluss-Selbstcheck** (`checkliste.md`, unterstützt durch
   `scripts/h5p_check.py --all`) — **Pflicht, bevor eine Datei als fertig
   gemeldet wird.** Bei langen Bearbeitungen gehen einzelne Schritte
   erfahrungsgemäß verloren; „ich hab dran gedacht" reicht nicht, jeder
   Punkt wird aktiv gegen die fertige Datei geprüft.
6. **Packen** mit `h5p_pack.pack()` — niemals mit rohem `zip -r`
   (Erklärung in `technik.md`). Danach die **final ausgelieferte
   Datei** noch einmal verifizieren, nicht nur eine Zwischenversion.

## Die sechs Fehler, die am häufigsten passieren

Diese Liste ist aus über hundert realen Bearbeitungen destilliert. Wer sie
kennt, spart sich die meisten Fehlschläge:

1. **Mit `zip -r` gepackt.** Das Archiv enthält dann Verzeichnis-Einträge,
   und der H5P-Server lehnt den Upload ab („File 'content/' not allowed").
   → immer `h5p_pack.pack()`, das entspricht `zip -r -X -D`.
2. **Bibliotheksversionen passen nicht zusammen.** Der Editor hebt beim
   Speichern Versionen an; wird danach ein älterer Stand teilweise
   zurückkopiert, zeigt eine `library`-Referenz auf eine Version, die im
   Paket gar nicht liegt. Upload-Fehler: „Bibliothek H5P.X a.b ist
   ungültig, sollte c.d sein." → `check_library_versions.py` vor jedem
   Packen.
3. **Medien ohne Autor/Quelle/Lizenz.** Viele H5P-Server verweigern den
   Upload oder zeigen „Fehlt" an. Neu eingefügte Medien bekommen im
   Editor-Workflow oft gar keine Metadaten. → `medien.md`.
4. **Der Editor hat beim Speichern etwas gelöscht.** Bekanntes Verhalten
   (mehrfach reproduziert): ein ganzes Kapitel wird leer, oder
   `metadata.source` verschwindet bei frisch eingefügten Bildern. → nach
   **jeder** Bearbeitung durch einen Menschen im Editor gegenprüfen,
   `technik.md`, Abschnitt „Editor-Fallstricke".
5. **Auf einem alten Arbeitsverzeichnis weitergebaut.** Jede neue Variante
   wird aus der zuletzt gültigen fertigen Datei frisch entpackt — sonst
   wandern Reste einer anderen Variante mit ins Paket (fällt oft nur an der
   Dateigröße auf).
6. **CC0 im falschen Lizenzfeld.** `"CC0 1.0"` ist nur unter
   `metadata.license` gültig. Im älteren `copyright`-Objekt einer Datei
   (`params.file`, `sources[]`, `files[]`) heißt CC0 immer
   `{"license": "PD", "version": "CC0 1.0"}`. Sonst meldet der Server
   je Datei „Ungültig ausgewählte Option bei Auswahl" — aber nur bei der
   ersten Anzeige nach dem Hochladen; danach ist der Wert still verworfen.
   Keine Meldung beweist also nichts. → `medien.md`, „Zwei
   Copyright-Felder"; `h5p_check.py --all` prüft es.

## Grundhaltung

- **Nicht raten.** Bibliotheksversionen, Koordinaten, Lizenzen und Quellen
  werden aus der Datei ausgelesen, nicht aus dem Gedächtnis oder aus einer
  anderen Datei übernommen. Werte, die in einer Datei stimmen, können in
  der nächsten anders sein.
- **Autofix vs. Rückfrage — Form ja, Inhalt nein.**
  Ohne Rückfrage korrigiert werden: Rechtschreibung und Grammatik,
  unsichtbare Sonderzeichen, LaTeX→Unicode, kaputte oder fehlende
  Metadaten, Bildtitel und Alternativtexte.
  Vorgelegt statt geändert werden: Fachtexte, Aufgabenstellungen,
  didaktische Umformulierungen, gelöschte Elemente — und jeder sichtbare
  Text, zu dem eine Vorlese-Aufnahme existiert, weil die Aufnahme sonst
  nicht mehr zum Text passt. Original und Vorschlag nebeneinander zeigen.
- **Sichtprüfung einplanen.** Claude sieht kein gerendertes H5P. Vor dem
  Packen hilft ein einfaches Mock-up-Rendering (PIL: Hintergrund, Bilder an
  ihren Prozentkoordinaten, Textelemente als beschriftete Rahmen), um
  Überlappungen zu finden (mit `scripts/mockup_render.py` zugleich der
  Scroll-Check) — danach lässt der Mensch die Datei einmal im
  Editor gegenlesen. Eine Fertigmeldung von Claude ist keine Freigabe.
- **Änderungen sichtbar machen.** Was automatisch korrigiert wurde, wird
  kurz aufgelistet — sonst kann niemand fachlich gegenprüfen.

## Skripte

Liegen im Unterordner `scripts/` des Werkzeug-Ordners, reines Python 3 ohne
Fremdbibliotheken (nur `zip`/`unzip` als Systemwerkzeug; Ausnahme
`mockup_render.py`). Sie werden in den
Arbeitsordner kopiert und importiert:

- **`h5p_pack.py`** — `unpack()`, `pack()`, `verify()`, plus Helfer für den
  Struktur-Walk: `replace_text()`, `strip_invisible()`,
  `latex_to_unicode()`, `library_versions()`, `find_media()`,
  `find_orphan_media()`, `find_incomplete_media_metadata()`,
  `replace_source_exact()`.
- **`check_library_versions.py`** — `find_mismatches()` (Binnen-Konsistenz
  einer Datei), `find_outdated()` (Aktualität über einen ganzen Ordner),
  `fix_content_json_version()`.
- **`mockup_render.py`** — Mock-up-Render und Überlaufprüfung je Folie
  (Playwright/Chromium nötig).
- **`h5p_check.py`** — Kommandozeilen-Werkzeug: `--inspect` (Struktur-
  Überblick), `--media` (Medien-Inventar mit Metadaten-Libücken), `--all`
  (kompletter Abschluss-Selbstcheck gegen eine fertige Datei, inkl.
  ungültiger `copyright.license`-Werte).