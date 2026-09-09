# Medien: Metadaten, Barrierefreiheit, Audio, Video

## 1. Metadaten — der häufigste Grund für abgelehnte Uploads

Jedes Medienelement (`H5P.Image`, `H5P.Audio`, `H5P.Video`,
`H5P.InteractiveVideo`, auch dekorative Hintergrundbilder) trägt ein
`metadata`-Objekt:

```json
"metadata": {
  "contentType": "Image",
  "license": "CC0 1.0",
  "title": "Schaubild zum Ablauf",
  "authors": [{"name": "Vorname Nachname", "role": "Author"}],
  "source": "https://…",
  "changes": []
}
```

**`authors` und `source` dürfen nie leer oder fehlend sein.** Viele
H5P-Server (Moodle, apps.zum.de) zeigen sonst „Fehlt" an oder verweigern
den Upload. Der Fehler fällt typischerweise erst nach dem Hochladen auf —
also lange nachdem die Datei als fertig galt.

Neu eingefügte Medien bekommen im normalen Editor-Workflow oft gar keine
Metadaten. Deshalb nach jedem Medien-Einbau und vor jeder Auslieferung
scannen:

```python
from h5p_pack import find_incomplete_media_metadata
luecken = find_incomplete_media_metadata(content)   # [(library, title), …]
```

Der Scan muss **alle** Medientypen abdecken, nicht nur den, an dem gerade
gearbeitet wurde. Realer Fund: ein Projekt prüfte jahrelang nur
`H5P.Audio` — beim ersten Lauf über `H5P.Image` fanden sich in einer
einzigen Datei 14 unvollständige Bild-Metadaten.

### Zwei Copyright-Felder, nur eines zählt

- **`metadata.license` / `metadata.authors` / `metadata.source`** — das
  maßgebliche, vom aktuellen Editor gepflegte Objekt.
- **`params.file.copyright` bzw. `params.files[].copyright`** — ein
  älteres, vom Editor mitgeführtes Feld. Ein `copyright.license: "U"` ist
  dort der **normale Standardzustand** und kein Fund: bei einer
  Vollprüfung hatten alle 79 Bilder und 5 Audios einer vollständig
  korrekten Datei dieses `"U"`. Nicht als „fehlende Metadaten" melden und
  nicht auf Verdacht überschreiben.

**Aber Vorsicht bei einem dritten, älteren Format:** manche Widgets — etwa
`H5P.DragQuestion`-Hintergründe — tragen ihr Copyright weder im einen noch
im anderen, sondern in einem eigenen Objekt unter
`question.settings.background.copyright` mit den Schlüsseln
`license`/`title`/`author`/`version`/`source` (Einzahl `author`!). Dort ist
`source` sehr wohl ein vollwertiges Feld und muss bei Quellen-Korrekturen
mit erfasst werden.

### Lizenz „U" nicht blind auf CC0 setzen

`"license": "U"` heißt „unbekannt" und ist **kein Freibrief für CC0**.
Vor jeder Änderung die tatsächliche Herkunft prüfen:

- Gibt es im selben H5P ein Bild mit erkennbar identischer Herkunft
  (gleiche Bildserie, gleicher Zeichenstil), dessen Lizenz schon eindeutig
  gesetzt ist? Dann diese übernehmen.
- Sieht das Medium nach fremder Quelle aus (Foto, Screenshot einer fremden
  Seite, Scan aus einem Buch, Cover-Art)? Dann **nicht raten** — nachfragen,
  woher es stammt.
- Nur wenn beides eindeutig auf Eigenerstellung hindeutet oder der Mensch
  es bestätigt, auf die passende freie Lizenz setzen — dann konsistent an
  beiden Stellen (`metadata.license` und `copyright.license`).

Hat ein Medium bereits eine **echte, bewusst gesetzte** Lizenz (z. B.
`CC BY-SA` bei einem Wikimedia-Bild), diese niemals überschreiben. Höchstens
ein inkonsistentes `copyright.license: "U"` an den bereits korrekten
`metadata.license`-Wert angleichen.

### Quellen umstellen — nur exakte Treffer ersetzen

Wenn Quellenangaben projektweit auf eine neue Adresse umgestellt werden
(z. B. weil Inhalte umgezogen sind), **nie einen String-Replace über den
kompletten JSON-Rohtext laufen lassen.** Dieselbe Zeichenkette ist oft
Präfix echter Inhaltslinks:

```
source:  "https://alte-domain.de"                        ← ersetzen
Textlink: "https://alte-domain.de/uploads/material.pdf"  ← NICHT anfassen
```

Richtig ist ein Struktur-Walk, der nur ersetzt, wenn der Dict-Schlüssel
exakt `source` heißt **und** der Wert exakt einer bekannten Variante
entspricht. Und Varianten gibt es viele: `http://` und `https://`, mit und
ohne `www.`, mit und ohne Trailing-Slash — schnell acht Schreibweisen.
`replace_source_exact()` in `h5p_pack.py` erledigt das.

**Die Suche muss das gesamte JSON durchlaufen, nicht nur `H5P.Image`-
Objekte.** Realer Fund: eine auf Bilder beschränkte Suche erwischte 2 von
7 Stellen; die restlichen steckten in `H5P.DragQuestion`-Hintergrund-
Copyrights, in Kapitel-eigenen `metadata`-Blöcken und im Top-Level-`source`
von `h5p.json`. Nach dem Fix per Textsuche verifizieren, dass die echten
Inhaltslinks unverändert geblieben sind.

Fehlt an einzelnen Bildern die Quelle ganz, hilft `image_source_majority()`
aus `h5p_pack.py`: es liefert den häufigsten `source`-Wert der
`H5P.Image`-Metadaten dieser Datei — meist die für das ganze Paket gültige
Quelle, die sich als Lückenfüller eintragen lässt. Gewertet werden nur
`H5P.Image`-Elemente, nicht die Weblink-Felder aus Aufgaben-Widgets.

Hat ein Medium bereits eine funktionierende, nachvollziehbare
Quellen-URL — dranlassen. Eine Quelle ist dazu da, dass jemand die
Herkunft nachprüfen kann. Ausnahme: offensichtliche Tippfehler in einer
Domain zählen nicht als funktionierende URL.

## 2. Alternativtexte und Barrierefreiheit

Bei jedem Durchgang **alle** `H5P.Image`-Elemente durchgehen und zwei Dinge
prüfen — das ist Autofix, keine Rückfrage nötig:

**Passt der Titel zum Bildinhalt?** Beim Bearbeiten wird oft ein
bestehendes Bildelement kopiert und nur die Bilddatei getauscht, nicht die
Metadaten. Ergebnis: Titel und Alt-Text beschreiben noch das alte Bild.
Realer Fund: ein Bild, das ein Balkendiagramm zeigte, war noch als
„Zeitstrahl" betitelt. Also das Bild **tatsächlich ansehen**, nicht
den vorhandenen Titel für bare Münze nehmen. (Bilddateien aus dem
entpackten `content/images/` lassen sich direkt mit dem Read-Tool
betrachten.)

**Beschreibt der Alternativtext das Bild für Blinde?** Alt-Texte sind
notorisch verwahrlost — leer, ein einzelnes Wort, oder identisch mit einem
generischen Titel wie „Bild".

- **Icons und Piktogramme**, deren Titel schon eindeutig ist (ein
  Warnsymbol, ein Werkzeugsymbol): ein Wort genügt.
- **Szenische Illustrationen, Diagramme, Grafiken mit eingebettetem Text,
  zusammengesetzte Bilder**: immer ein bis zwei vollständige Sätze, die
  sagen, was zu sehen ist. „Illustration: zwei Personen sortieren
  gemeinsam Karten auf einem Tisch." statt „Bild".
- **`decorative: true` kritisch prüfen.** Bilder, die lernrelevanten Text
  oder Beschriftungen enthalten (ein beschriftetes Modell-Diagramm, ein
  Beispielkästchen mit Erklärtext), stehen oft fälschlich auf
  `decorative` — umstellen auf `false` und mit vollem Alt-Text versehen.
  Rein schmückende Icons ohne eigenen Informationsgehalt bleiben
  `decorative`.
- **Wird dasselbe Bild mehrfach verwendet**, bekommen alle Vorkommen
  denselben vollständigen Alt-Text, nicht nur das zuerst bearbeitete.

## 3. Vorlese-Audio (TTS)

Ein kleiner Audio-Button neben dem Folientitel, der den Folientext
vorliest, ist eine der wirksamsten Inklusionsmaßnahmen in einem
Selbstlern-H5P. Technisch ein `H5P.Audio`-Element:

```json
{
  "library": "H5P.Audio 1.5",
  "params": {
    "playerMode": "minimalistic",
    "fitToWrapper": true,
    "controls": true,
    "autoplay": false,
    "files": [{"path": "audios/files-a1b2c3d4.mp3", "mime": "audio/mpeg"}]
  },
  "metadata": { … vollständig, siehe oben … }
}
```

Positionierung: siehe `layout.md`, Abschnitt „Elemente relativ zum Titel
positionieren".

### Grundprinzip: Vorlese-Text = sichtbarer Folientext

Gesprochener und geschriebener Text sollen möglichst **wortgleich** sein,
nicht nur inhaltlich ähnlich. Grund: das Audio ist eine Lesehilfe — wer
mitliest, während vorgelesen wird, verliert bei freier Umformulierung
sofort den Faden.

Erlaubte Abweichungen sind nur solche, die die TTS überhaupt erst
sprechfähig machen. Alles andere (kürzen, umstellen, freier formulieren)
ist ausdrücklich nicht erlaubt.

### TTS-Aussprache: alles ausschreiben, was unklar ist

Genereller Grundsatz: **jedes Zeichen, jede Abkürzung, jedes Symbol im
Aufnahmetext, bei dem unklar ist, ob die TTS es korrekt vorliest, wird
ausgeschrieben oder phonetisch angepasst.** Bestätigte Fälle:

| Problem | Im Aufnahmetext |
|---|---|
| Römische Ziffern werden komplett verschluckt („Teil I") | `I` → `eins`, `II` → `zwei` … |
| Nummerierung mit Punkt („2. Schritt") | `2.` → `zweitens` |
| Formelzeichen (`•`, Hoch-/Tiefstellung, `≈`) | „mal", „hoch", „ungefähr" ausschreiben |
| Fachbegriffe mit ungewöhnlicher Vokallänge | phonetisch anpassen, meist durch Verdopplung des Vokals (z. B. `Ton` → `Toon` für langes O) |
| Abkürzungen in Klammern ohne Sprechwert | im Aufnahmetext weglassen |

**Wichtige Unterscheidung:** Anpassungen, die die *Lesbarkeit auf der
Folie* nicht verschlechtern (Ziffer → Wort bei Aufzählungen), wandern in
den sichtbaren Folientext, damit beide synchron bleiben. Echte
wissenschaftliche Notation dagegen bleibt auf der Folie stehen — Lernende
sollen sie lesen lernen; das Ausschreiben ist eine rein technische Krücke
und nur im Aufnahmetext.

**Vorsicht bei automatisiertem Ersetzen phonetischer Fixes:** ein kurzes
Wort ist oft Teilstring eines längeren — `Ton` steckt in `Tonne`. Nur auf
Wortgrenzen ersetzen (`\bTon\b`), sonst entsteht „Toonne".

**Sonderfall — Folien, die sich nur durch eine Nummer im Titel
unterscheiden** („Übersicht I / II / III"): Ausschreiben hilft hier
*nicht*; die TTS lässt auch ausgeschriebene Zahlwörter in diesem Kontext
weg. Bewährte Lösung: für alle betroffenen Folien **dieselbe eine Aufnahme
ohne Nummer** verwenden. Der sichtbare Titel behält die Nummer.

### Ablauf einer Aufnahme-Runde

1. **Vorab-Check pro Folie** — nicht pauschal alles neu aufnehmen:
   - Gibt es überhaupt ein titelnahes `H5P.Audio`? Nein → neu aufnehmen.
   - Ja, mit echter Datei in `params.files[]`, und der Text hat sich seit
     der Aufnahme nur geringfügig geändert (ein Artikel, ein
     Grammatikfehler)? → **nicht** neu aufnehmen, allenfalls die
     Button-Position anpassen.
   - Nur bei inhaltlich substanziellen Textänderungen erneut aufnehmen.

   Realer Fehler: 5 von 11 Folien landeten in der Aufnahmeliste, weil nur
   die *Existenz* eines Audio-Elements geprüft wurde, nicht ob es schon
   eine Datei referenziert.
2. **Textdatei erzeugen** — ein Eintrag pro Folie, mit einer Kopfzeile, die
   als Dateiname taugt, und dem kompletten vorzulesenden Text darunter:
   ```
   Folie 4 (Kapitel "Einstieg")
   Wie kommt ein Werkstück in die richtige Form? Drei Wege führen dorthin …
   ---
   ```
   **Keine Doppelpunkte in der Kopfzeile** — sie wird direkt als Dateiname
   verwendet, und `:` ist auf macOS im Finder nicht speicherbar. Endet ein
   Folientitel selbst auf `:`, den vorher im H5P entfernen.
3. **Zuordnung gegenprüfen.** Die „Folie N" der Textdatei ist nicht
   zwangsläufig `slides[N]`: typischerweise ist `slides[0]` ein technisches
   Cover, also gilt ein Versatz von +1. Der Versatz kann aber je nach Datei
   anders sein (weitere Folien ohne Audio davor) — immer anhand der Titel
   gegenprüfen, nie blind übernehmen.
4. **Einbauen** mit vollständigen Metadaten (Autor der Aufnahme, dazu das
   verwendete TTS-Werkzeug als `Licensee` — Quelle und Lizenz wie bei
   jedem anderen Medium). Dateinamen ASCII-safe wählen.
5. **Gegenprüfen** mit `find_incomplete_media_metadata()`, dann packen.

Liefert das TTS-Werkzeug `.wav`, vor dem Einbau konvertieren, damit `mime`
konsistent `audio/mpeg` bleibt:

```bash
ffmpeg -i in.wav -codec:a libmp3lame -qscale:a 2 out.mp3
```

### Lückentexte vorlesen: Piepton-Splice

Soll das Audio eine `H5P.Blanks`-Aufgabe mitlesen, ohne die Lösungen zu
verraten: an jeder Lücke im Aufnahmetext das Wort **„Lücke"** einsetzen,
satzgrammatisch eingebettet („eins mal zehn hoch Lücke Meter"). Eine reine
Sprechpause taugt nicht — sie ist von einem Aussetzer nicht zu
unterscheiden. Ein echter Signalton lässt sich per TTS nicht erzeugen: TTS
synthetisiert nur Sprache, und Pausen-Tags gibt es in den gängigen APIs
nicht (anderslautende Blogposts widersprechen der offiziellen Doku).

Aus der einen durchgehenden Aufnahme lässt sich das Wort automatisch
herausschneiden und durch einen Piepton ersetzen:

1. **Piepton erzeugen** (kein Download, keine Lizenzfrage):
   ```bash
   ffmpeg -f lavfi -i "sine=frequency=880:duration=0.8" \
          -ar 44100 -ac 1 -codec:a libmp3lame -qscale:a 2 beep.mp3
   ```
2. **Wort-Zeitstempel ermitteln** mit `vosk` (`pip install vosk` — klein
   und schnell, im Gegensatz zu `openai-whisper`, das an typischen
   Kommando-Timeouts scheitert). Deutsches Modell
   `vosk-model-small-de-0.15` (~46 MB), Audio vorher auf 16 kHz mono
   konvertieren, `KaldiRecognizer(..., SetWords(True))` liefert `start`/
   `end` pro Wort. In abgeschotteten Umgebungen ist der Direktdownload von
   Modell-Hosting-Seiten oft gesperrt, während `pip` und `git` erreichbar
   bleiben — dann das Modell aus einem Git-Spiegel holen
   (`git clone --depth 1 --filter=blob:none`, danach gezielt
   `git checkout HEAD -- <datei>`), statt den ganzen Verlauf zu laden.
3. **Trefferzahl gegen die erwartete Lückenzahl prüfen** — bei Abweichung
   nicht weitermachen, sondern melden. (Praktisch: die Lückenzahl in die
   Kopfzeile der Textdatei schreiben, dann steht sie im Dateinamen.)
4. **Schneiden und zusammensetzen**: Segmente zwischen den Treffern mit
   `ffmpeg -ss … -to …` extrahieren (±0,03 s Padding um das Wort), dann
   Segmente und Piepton abwechselnd mit `ffmpeg -f concat` verbinden.

## 4. Video: lokal einbetten statt nur verlinken

Viele H5P verlinken Videos von YouTube (`mime: "video/YouTube"`, `path`
beginnt mit `https://youtu.be/…`). In vielen Netzen — Schulnetze vor allem
— ist das gesperrt. Die Lösung ist, die Videodatei zusätzlich lokal ins
Paket zu legen.

**Zwei unterschiedliche Strukturen, je nach Content-Typ:**

```python
# H5P.Video — einfaches Video ohne Zeitleisten-Interaktionen
el["action"]["params"]["sources"].insert(0, {
    "path": "videos/erklaervideo.mp4",
    "mime": "video/mp4",
    "copyright": {"license": "CC0 1.0"},
})

# H5P.InteractiveVideo — Quellen liegen TIEFER, nicht unter "sources"
el["action"]["params"]["interactiveVideo"]["video"]["files"].insert(0, {
    "path": "videos/erklaervideo.mp4",
    "mime": "video/mp4",
    "copyright": {"license": "CC0 1.0"},
})
```

- Die lokale Quelle **vorne** einfügen: die meisten Player bevorzugen sie,
  wenn sie sie unterstützen.
- **Den ursprünglichen Link nicht entfernen** — er bleibt als weitere
  Quelle stehen, damit die Datei auch außerhalb des Pakets nachvollziehbar
  ist und in Netzen ohne Sperre weiter funktioniert. Wird ein Link als
  kaputt gemeldet, beim Einbau **aktiv aktualisieren**, nicht stillschweigend
  den alten übernehmen.
- Bei `H5P.InteractiveVideo` die Felder `interactions`, `assets` und
  `startVideoAt` **nicht anfassen** — sie hängen an Zeitstempeln des
  Videos.
- Video-Elemente über einen Struktur-Walk suchen
  (`lib.startswith("H5P.Video")` bzw. `"H5P.InteractiveVideo"`), nicht
  über den Folienindex raten.
- Rohdatei nach `content/videos/` kopieren, Dateiname ASCII-safe.
- **Dateigröße:** eingebettete Videos vergrößern das Paket erheblich (aus
  12 MB werden schnell 90 MB). Das ist der Zweck der Übung, aber es lohnt
  sich, **zwei Dateien** anzubieten: eine schlanke ohne lokales Video und
  eine große mit. Beide getrennt bauen — jede aus einem **eigenen, frisch
  entpackten** Arbeitsverzeichnis (siehe `technik.md`).
- Wird nach dem Bau der Video-Variante noch ein Fehler in der Basisdatei
  behoben, muss die Video-Variante **neu gebaut** werden, nicht gepatcht.
