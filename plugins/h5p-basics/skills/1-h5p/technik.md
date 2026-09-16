# Technik: Packen, Bibliotheken, Fehlersuche

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' technik.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | 1. Entpacken und Packen | 33–34 |
> | Die eiserne Regel: nie mit `zip -r` packen | 35–68 |
> | Was `verify()` prüft | 69–78 |
> | Dateinamen im Paket: nur ASCII | 79–104 |
> | Root-Ebene des Archivs prüfen | 105–126 |
> | Arbeitsverzeichnisse nicht wiederverwenden | 127–144 |
> | Packen auf gemounteten/synchronisierten Laufwerken | 145–162 |
> | 2. Bibliotheksversionen | 163–164 |
> | Warum das ständig schiefgeht | 165–179 |
> | Zwei verschiedene Prüfungen — beide werden gebraucht | 180–208 |
> | Große Versionssprünge: erst Risiko einschätzen | 209–222 |
> | 3. Editor-Fallstricke (Lumi, Moodle, WordPress) | 223–229 |
> | Ein ganzes Kapitel wird beim Speichern geleert | 230–279 |
> | `metadata.source` verschwindet bei frisch eingefügten Bildern | 280–290 |
> | Kryptische Lumi-Fehler beim Öffnen | 291–297 |
> | 4. Defekte Einträge im Archiv | 298–320 |
> | 5. Versteckte Inhalte finden | 321–335 |
> | 6. Textkorrekturen über die JSON-Struktur | 336–362 |
> | 7. Verwaiste Mediendateien | 363–377 |
> | 8. Pfade mit Umlauten (macOS) | 378–401 |
<!-- /INDEX -->

## 1. Entpacken und Packen

### Die eiserne Regel: nie mit `zip -r` packen

`zip -r` legt für jeden Ordner einen eigenen 0-Byte-Eintrag im Archiv an
(`content/`, `H5P.Blanks-1.14/`). Der H5P-Server-Validator prüft **jeden**
Zip-Eintrag gegen eine Dateiendungs-Whitelist; ein Verzeichnis-Eintrag hat
keine Endung. Ergebnis: `File "content/" not allowed` — der komplette
Upload schlägt fehl, obwohl die Datei sich lokal in Lumi einwandfrei öffnen
lässt. Das ist der mit Abstand häufigste Grund für „lokal geht's, auf dem
Server nicht".

Richtig ist `zip -rXq -D` (`-D` = keine Verzeichnis-Einträge, `-X` = keine
Extra-Attribute) — genau das macht `h5p_pack.pack()`, inklusive
anschließender Verifikation. Schlägt die Verifikation fehl, löscht `pack()`
die Ausgabedatei wieder: es entsteht nie eine halb-kaputte Datei.

```python
import sys; sys.path.insert(0, "scripts")
from h5p_pack import unpack, pack, verify, load_content, save_content

work = unpack("original.h5p", "/tmp/arbeit")
content = load_content(work)
# ... bearbeiten ...
save_content(work, content)
pack(work, "/tmp/neu.h5p", reference="original.h5p")
```

`reference=` vergleicht die Dateiliste mit dem Original: fehlende Dateien
sind immer ein Fehler, zusätzliche sind erlaubt (`allow_new_files=True`).
**`reference=None` verwenden**, wenn bewusst Dateien entfernt oder ersetzt
wurden — sonst meldet `verify()` diese als „fehlend". Das gilt insbesondere
nach jeder Bearbeitung durch einen Menschen im Editor: Editoren benennen
Bilder um, vergeben neue `subContentId`s und heben Bibliotheksversionen an.
Das sind harmlose Abweichungen, keine Datenverluste.

### Was `verify()` prüft

1. **ZIP-Integrität** (`testzip()`) — einzelne Einträge können strukturell
   defekt sein, ohne dass der Editor es merkt (siehe unten).
2. **Keine Verzeichnis-Einträge** — die Kernregel oben.
3. **Keine Nicht-ASCII-Dateinamen im Paket** — siehe unten.
4. **Pflichtdateien** `h5p.json` und `content/content.json` vorhanden.
5. **JSON lesbar.**
6. **Vergleich mit der Referenzdatei**, falls angegeben.

### Dateinamen im Paket: nur ASCII

Dateinamen **innerhalb** des H5P-Pakets dürfen keine Umlaute, `&` oder
andere Nicht-ASCII-Zeichen enthalten. Ein Bild namens `loesung-aufräumen.png`
lässt manche Player (u. a. Lumi) mit einem kryptischen `ENOENT`-Fehler
scheitern, weil die Kodierung des Zip-Eintragsnamens nicht zuverlässig zum
in `content.json` referenzierten Pfad passt. Werden Dateinamen aus Texten
abgeleitet (z. B. aus Aufgaben-Labels), vorher transliterieren:

```python
import re, unicodedata
def ascii_stem(text):
    t = text.lower()
    for a, b in [("ä","ae"),("ö","oe"),("ü","ue"),("ß","ss")]:
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "datei"
```

Dieselbe Funktion liegt fertig als `ascii_stem()` in `h5p_pack.py`;
`verify()` prüft die Regel zusätzlich automatisch, sodass ein Paket mit
Nicht-ASCII-Dateinamen gar nicht erst entsteht.

Für **Ordner außerhalb** des Pakets gilt das nicht — dort ist die Falle
eine andere (siehe „Pfade mit Umlauten" unten).

### Root-Ebene des Archivs prüfen

Ein normales H5P-Zip hat auf Wurzelebene **nur** `h5p.json` — alles andere
außer den Bibliotheksordnern ist ein Fund. Manche Pakete bringen zusätzlich
eine `mimetype`-Datei mit; sie wird toleriert, aber **von `pack()` nicht
erzeugt**: fehlt sie im Arbeitsverzeichnis, fehlt sie auch im fertigen
Paket, und das ist kein Fehler. Typischer Unfall: beim Kopieren des
Arbeitsverzeichnisses landen eine Rest-`.h5p` aus einem früheren Entpacken
und ein Debug-Bild mit im Paket, weil sie im Arbeitsverzeichnis lagen und
nicht in `content/` — die „verwaiste Medien"-Prüfung erfasst sie deshalb
nicht.

```python
import zipfile
root = [n for n in zipfile.ZipFile(pfad).namelist() if "/" not in n]
assert "h5p.json" in root, root
assert set(root) <= {"h5p.json", "mimetype"}, root   # mimetype: geduldet
```

Eigene Mockups und Vorschaubilder deshalb **immer in einem separaten
Ordner** erzeugen, nie im H5P-Arbeitsverzeichnis.

### Arbeitsverzeichnisse nicht wiederverwenden

Jede neue Variante einer Datei wird **frisch aus der zuletzt gültigen
fertigen Datei entpackt** — nie in einem Arbeitsverzeichnis weitergebaut,
das schon für eine andere Variante benutzt wurde.

Realer Fehler: Für eine Variante mit eingebetteten Videos und eine ohne
wurde dasselbe Verzeichnis benutzt. Die eigentlich videofreie Datei war am
Ende 92 MB statt 12 MB groß — sie enthielt die Videos mit, obwohl der Name
das Gegenteil versprach. `verify()` findet das nicht (es prüft Integrität,
nicht „zu viel Inhalt"). **Deshalb: Dateigröße nach dem Packen grob
gegenprüfen.** Eine Variante ohne Videos muss deutlich kleiner sein als
die mit.

Dasselbe gilt für jede spätere Nachbesserung: frisch von der aktuell
gültigen Datei entpacken, nicht ein altes Verzeichnis von vorgestern
wiederbeleben.

### Packen auf gemounteten/synchronisierten Laufwerken

Auf FUSE-Mounts, Netzlaufwerken und manchen Cloud-Sync-Ordnern scheitert
`zip` mit `zip I/O error: Operation not permitted` bzw. `Could not create
output file` (Exit-Code 15) — zip schreibt über eine Temp-Datei plus
Rename, was solche Mounts nicht zuverlässig unterstützen. Anschließend
schlägt sogar das Aufräumen der 0-Byte-Restdatei fehl.

**Lösung:** das entpackte Arbeitsverzeichnis nach `/tmp` (echtes lokales
Dateisystem) kopieren, dort packen, die fertige `.h5p` danach zurück-
kopieren. Reines Kopieren funktioniert auf solchen Mounts problemlos — nur
das Packen selbst nicht. Nach dem Zurückkopieren `testzip()` und Dateigröße
**auf der finalen Datei** noch einmal prüfen.

Wenn auf demselben Mount auch `rm`/`mv` blockiert sind: verwaiste Dateien
beim Kopieren nach `/tmp` einfach **nicht mitkopieren**, statt zu versuchen,
sie im Original zu löschen.

## 2. Bibliotheksversionen

### Warum das ständig schiefgeht

Jedes H5P-Paket bringt seine Bibliotheken selbst mit (`H5P.Column-1.18/`).
In `content.json` und `h5p.json` steht daneben, welche Version der Inhalt
erwartet (`"library": "H5P.Column 1.18"`). Editoren heben Versionen beim
Speichern gern an. Wird danach ein älterer Stand teilweise zurückkopiert
(z. B. bei einer Wiederherstellung), zeigt eine Referenz auf eine Version,
die nicht mehr im Paket liegt. **Lokal funktioniert das oft weiter**, beim
Upload auf einen H5P-Server (Moodle, WordPress, ZUM-Apps …) kommt dann:

> Bibliothek H5P.Column 1.16 ist ungültig, sollte 1.18 sein

Bibliotheksversionen deshalb **nie fest verdrahten**, immer mit
`library_versions(work_dir)` aus dem Paket selbst auslesen.

### Zwei verschiedene Prüfungen — beide werden gebraucht

Die Versionsprüfung ist ein **fester Schritt vor jedem finalen Packen**,
keine Maßnahme im Verdachtsfall: der Fehler entsteht stumm und zeigt sich
erst beim Upload.

```bash
python3 scripts/check_library_versions.py DATEI.h5p        # Binnen-Konsistenz
python3 scripts/check_library_versions.py --outdated ORDNER # projektweite Aktualität
```

- **`find_mismatches(datei)`** — passen alle `library`-Referenzen (in allen
  JSONs plus `h5p.json/preloadedDependencies`) zu den mitgelieferten
  Bibliotheksordnern? Findet die klassische Upload-Fehlermeldung.
- **`find_outdated(ordner)`** — ist eine Datei zwar *in sich* stimmig, aber
  gegenüber dem Rest einer Sammlung insgesamt veraltet? Realer Fund: ein
  Buch lag komplett auf `H5P.InteractiveBook 1.7` statt der sonst überall
  genutzten `1.11`, intern völlig konsistent — `find_mismatches()` findet
  das grundsätzlich nicht.

Bei Treffern mit `fix_content_json_version(work_dir, lib, alt, neu)`
reparieren, dann **mit `reference=None`** neu packen (die Referenzprüfung
würde den Fix sonst als Abweichung werten).

**Ein Bibliotheksordner ohne aktive Verwendung** (weder in
`preloadedDependencies` noch als `library`-Referenz) kann nie die Ursache
eines Validierungsfehlers sein. Bei der Fehlersuche zuerst prüfen, ob die
gemeldete Bibliothek überhaupt referenziert wird.

### Große Versionssprünge: erst Risiko einschätzen

Ein Sprung um eine Minor-Version ist per Ordnertausch + Referenz-Update
gefahrlos. Bei größeren Sprüngen (z. B. 1.7 → 1.11) vorher prüfen:

1. `semantics.json` und `library.json` beider Versionen per Text-Diff
   vergleichen.
2. Sind die Unterschiede kosmetisch (Default-Werte, Options-Strings) →
   gefahrlos übernehmen.
3. Gibt es echte Schema-Änderungen (neue Pflichtfelder ohne Default) →
   **nicht selbst migrieren**. Stattdessen die Datei einmal im H5P-Editor
   öffnen und speichern lassen: der Editor migriert Content-Parameter
   automatisch und korrekt.

## 3. Editor-Fallstricke (Lumi, Moodle, WordPress)

Nach **jeder** Bearbeitung durch einen Menschen im grafischen Editor gilt
die Datei als „möglicherweise beschädigt", auch wenn sie sich einwandfrei
öffnen lässt und der Mensch sagt, alles sei super. Zwei reproduzierte
Fehlerbilder:

### Ein ganzes Kapitel wird beim Speichern geleert

Beobachtet in Lumi bei `H5P.InteractiveBook`: der Mensch ändert an einer
völlig anderen Stelle etwas (eine Drag-Aufgabe, eine Audio-Position) und
speichert — danach ist ein Kapitel (typischerweise das letzte,
`chapters[-1]`) ein leeres `{}`/`[]`. Zusätzlich verschwinden **alle** von
diesem Kapitel referenzierten Bilder aus `content/images/`: der Editor
räumt beim Speichern unreferenzierte Assets weg, und ein leer
gespeichertes Kapitel macht seine Bilder unreferenziert. Mehrfach
bestätigt, teils zweimal an derselben Datei.

**Pflichtablauf nach jeder Editor-Bearbeitung:**

1. **Zuerst die ZIP-Integrität prüfen** (`testzip()`), noch vor allem
   anderen. Ein Editor kann beim Speichern einzelne Medieneinträge
   strukturell zerschreiben (`zlib error -3`, `BadZipFile`, falsche
   Header-Offsets), ohne irgendetwas zu melden — beobachtet wurden 22 von
   48 Einträgen in einem einzigen Speichervorgang, darunter sämtliche
   Hintergründe. `content.json` und `h5p.json` blieben dabei lesbar, die
   Datei ließ sich normal öffnen. Ohne diesen Test fällt der Schaden erst
   beim Hochladen auf, dann aber mit allen seither gemachten Änderungen
   darin.

   **Was in diesem Fall funktioniert hat, ist nicht das Reparieren des
   Archivs und nicht das Entfernen der defekten Elemente**, sondern: die
   letzte selbst gepackte, nachweislich intakte Fassung als Quelle nehmen
   und die Editor-Runde verwerfen. Das setzt den Nachweis voraus, dass im
   Editor inhaltlich nichts geändert wurde — Text- und Geometrievergleich
   alt gegen neu über alle `text`/`alt`/`title`-Strings (HTML-bereinigt)
   und alle `x`/`y`/`width`/`height`. Bleibt nur Editor-Rauschen übrig
   (`changes: []`, `extraTitle`, `authors: []`, `<br>` → `<br />`,
   CSS-Semikolons), ist die alte Fassung der bessere Ausgangspunkt.
   Ergibt der Vergleich echte inhaltliche Unterschiede, ist das Verwerfen
   keine Option — dann mit dem Nutzer klären.
2. Alle Kapitel auf Leere prüfen, bevor irgendetwas anderes
   geschieht.
3. Bei Leere: aus dem letzten bekannt-guten Zwischenstand wiederherstellen
   — Kapitel-JSON **und** alle davon referenzierten Mediendateien.
4. **Bibliotheksversion des wiederhergestellten Kapitels gegenprüfen**
   (`chapters[N]["library"]`) — der alte Stand bringt die alte
   Versionsnummer mit, das Paket enthält aber schon die neue. Genau daraus
   entsteht der Upload-Fehler aus Abschnitt 2.
5. Erst danach packen, mit `reference=None`.

Meldet der Editor direkt nach so einer Wiederherstellung „Der ausgewählte
Inhaltstyp 'H5P.X a.b' ist auf dieser Seite nicht installiert", ist das
meist ein Editor-Cache-Rest und verschwindet mit der wiederhergestellten
Datei — trotzdem zuerst Schritt 3 prüfen, weil dieselbe Meldung auch aus
einer echten Versionsabweichung kommen kann.

### `metadata.source` verschwindet bei frisch eingefügten Bildern

Davon unabhängig: nach einer normalen Speicherung fehlte bei 5 von 6 neu
eingefügten `H5P.Image`-Elementen das Feld `metadata.source` komplett,
während `metadata.authors` erhalten blieb. Betroffen waren nur die in
derselben Sitzung neu eingefügten Bilder, nicht die älteren.

→ Nach jeder Editor-Bearbeitung **alle** Medienelemente auf leere
`authors`/`source` scannen (`find_incomplete_media_metadata()`), nicht nur
die selbst eingefügten.

### Kryptische Lumi-Fehler beim Öffnen

`ENOENT: ... .education.lumi.lumi.XXXXXX` mit gleichbleibendem
Zufalls-Suffix über mehrere Öffnungsversuche hinweg ist meist **kein**
kaputtes Paket, sondern ein Lumi-seitiger Cache-/Temp-Zustand. Erst Lumi
neu starten, bevor an der Datei gesucht wird.

## 4. Defekte Einträge im Archiv

Einzelne Zip-Einträge können strukturell defekt sein, ohne dass ein Player
das merkt. Realer Fall: zwei MP3-Einträge, die `testzip()` als kaputt
meldete; bei einem warf `zf.read()` `BadZipFile: File name in directory
'...' and header '...' differ` (die Verzeichnis-Referenz zeigte auf einen
falschen Byte-Offset, mitten in einen PNG-Eintrag hinein). Die Rohdaten
waren im Archiv nirgends mehr vorhanden — nicht reparierbar. Die Datei ließ
sich in Lumi trotzdem öffnen und wirkte funktionsfähig.

**Konsequenz:** „Es hat sich geöffnet und sah gut aus" ist kein
Qualitätsnachweis. Bei jedem Repack `testzip()` auf der **final
ausgelieferten** Datei ausführen, nicht nur auf einer Zwischenversion:

```bash
python3 -c "import zipfile;print(zipfile.ZipFile('DATEI.h5p').testzip())"
# Ergebnis muss None sein
```

Bei einem Fund nicht versuchen, den Eintrag aus demselben Archiv zu
retten — stattdessen das zugehörige Element aus `content.json` entfernen,
sauber packen und den Inhalt danach neu ergänzen.

## 5. Versteckte Inhalte finden

Ein `--inspect`-Überblick, der nur die Elemente pro Folie auflistet, zeigt
nicht alles:

- **`H5P.InteractiveVideo`** trägt seine zeitleisten-gebundenen Aufgaben
  unter `action.params.interactiveVideo.assets.interactions` — eine
  Elementliste zeigt dort oft nur „keine Quellen". Diese Interaktionen
  enthalten echte Aufgabentexte mit eigenen Rechtschreib-, Fach- und
  LaTeX-Fehlern und müssen wie eine normale Folie geprüft werden.
- **Bibliotheksinterne Unterinhalte** (`H5P.Column` in einem Kapitel, ein
  Quiz in einem Accordion) liegen beliebig tief verschachtelt. Deshalb
  arbeitet jede Prüfung als rekursiver Struktur-Walk, nicht über feste
  Pfade.

## 6. Textkorrekturen über die JSON-Struktur

Alle Helfer in `h5p_pack.py` laufen rekursiv über die **geparste**
Struktur, nicht über den Rohtext, und geben die Trefferzahl zurück:

- **`strip_invisible(obj)`** — entfernt weiches Trennzeichen,
  Zero-Width-Zeichen, Wortverbinder und ähnliche Copy-Paste-Reste.
  Autofix, nie nachfragen. Wichtig: auf den geparsten Strings arbeiten —
  im Rohtext der Datei stehen sie nur als `­`-Escape.
- **`latex_to_unicode(obj)`** — ersetzt LaTeX-Notation durch Unicode:
  `\(x_{1}^{2}\)` → `x₁²`, `\(\frac{km}{h}\)` → `km/h`. Grund: reines
  Unicode rendert in H5P stabiler als eingebettetes LaTeX/MathType. Nur
  Ziffern, `+`, `-`, `(`, `)` werden hoch-/tiefgestellt — andere Zeichen
  bleiben als LaTeX stehen und müssen von Hand geprüft werden. Einmal pro
  Durchgang über die komplette `content.json` laufen lassen und die
  Treffer gegenprüfen.
- **`replace_text(obj, alt, neu)`** — für gezielte Korrekturen. Deckt auch
  Strings ab, die direkt als Listenelement stehen (bei `H5P.Blanks` liegen
  Aufgabentexte oft so vor, nicht als Dict-Wert).
- **`replace_source_exact(obj, varianten, neu)`** — ersetzt Quellen-URLs
  **nur bei exaktem Treffer** am Schlüssel `source`. Siehe
  `medien.md`, Abschnitt „Quellen umstellen", warum ein naiver
  String-Replace hier Inhalte zerstört.

Rechtschreibprüfung nicht nur auf `content.json` anwenden: auch `h5p.json`
(`title`, `extraTitle`) enthält sichtbaren Text und wird gern übersehen.

## 7. Verwaiste Mediendateien

Nach dem Löschen eines Elements — oder eines ganzen Kapitels — bleiben die
zugehörigen Mediendateien im Arbeitsverzeichnis liegen und wandern
unnötigerweise mit ins Paket. Vor dem Packen prüfen:

```python
from h5p_pack import find_orphan_media
verwaist = find_orphan_media(work_dir)   # Liste relativer Pfade
```

Die Prüfung testet für jede Datei in `content/images|audios|videos`, ob ihr
Pfad noch irgendwo im JSON vorkommt. Verwaiste Dateien vor dem Packen
entfernen (bzw. beim Kopieren nach `/tmp` weglassen).

## 8. Pfade mit Umlauten (macOS)

macOS speichert Dateinamen NFD-zerlegt (`ö` = `o` + kombinierendes
Diaerese-Zeichen), getippte Strings sind NFC. Ein fest getippter Pfad mit
Umlaut kann deshalb einen unsichtbaren Doppelgänger-Ordner anlegen, statt
den echten zu treffen — betrifft jeden Ordnernamen mit Umlaut.

```python
import unicodedata, pathlib
def resolve(pfad):
    """Findet den real existierenden Pfad unabhängig von NFC/NFD."""
    p = pathlib.Path(pfad)
    if p.exists():
        return p
    ziel = unicodedata.normalize("NFC", p.name)
    for kandidat in p.parent.iterdir():
        if unicodedata.normalize("NFC", kandidat.name) == ziel:
            return kandidat
    return p
```

Dieselbe Funktion liegt als `resolve_path()` in `h5p_pack.py`. (Anderes
Problem als die ASCII-Regel für Dateinamen *im* Paket — gleiche
Fehlerklasse.)
