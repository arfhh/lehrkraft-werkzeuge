# Werkzeuge fuer Lehrkraefte — Skills fuer Claude

Skills rund um **H5P**, **Moodle**, **Browser-Erweiterungen** und **Sprachausgabe**, entstanden
im Chemieunterricht und in der Fortbildung am LI Hamburg.
Autor: Arne Spielhoff. Fassung 1.2.0, Stand 25.10.2026.

Es gibt zwei Wege, je nachdem womit du arbeitest.

## Weg 1 — Claude-Desktop-App oder Claude Code (empfohlen)

Eine Installation, alle Begleitdateien und Skripte sind dabei.

    /plugin marketplace add arfhh/lehrkraft-werkzeuge
    /plugin install h5p-basics@lehrkraft-werkzeuge

Statt `h5p-basics` geht auch `moodle-basics`, `browser-basics` oder `tts-basics`.
Danach einmal `/reload-plugins`.

## Weg 2 — Claude im Browser (claude.ai)

Unter **Releases** das passende ZIP herunterladen, entpacken, den Ordner ins
eigene Projekt legen und die Skills aus dem Unterordner `Skill/` im Konto
anlegen. Die Anleitung liegt als `LIESMICH.md` im ZIP.

## Die Buendel

| Buendel | Skills | Wofuer | ZIP |
|---|---|---|---|
| `h5p-basics` | `1-h5p`, `2-didaktik-h5p` | H5P-Dateien auf Dateiebene bauen, pruefen und reparieren, plus die didaktische Beurteilung interaktiver Lerneinheiten. | [H5P-Basics.zip](https://github.com/arfhh/lehrkraft-werkzeuge/releases/latest/download/H5P-Basics.zip) |
| `moodle-basics` | `1-moodle-xml`, `2-didaktik-bewertung` | Moodle-Fragen als XML erzeugen und importieren, mit Cloze-Formenkanon und Bewertungsmassstab. | [Moodle-Basics.zip](https://github.com/arfhh/lehrkraft-werkzeuge/releases/latest/download/Moodle-Basics.zip) |
| `browser-basics` | `1-webext-robustheit`, `1-browser-wxt` | Browser-Erweiterungen bauen, die auf einer fremden Weboberflaeche wie Moodle arbeiten -- robuste Laufzeit-Technik plus WXT-Aufbau fuer Chrome, Firefox und Edge aus einer Codebasis. | [Browser-Basics.zip](https://github.com/arfhh/lehrkraft-werkzeuge/releases/latest/download/Browser-Basics.zip) |
| `tts-basics` | `1-text-zu-sprache` | Texte lokal und offline vertonen (MP3) mit Chatterbox -- Installation, Doppelklick-Starter, eigene oder LibriVox-Stimme, Sprechtext-Regeln, Lizenz und KI-Kennzeichnung. | [TTS-Basics.zip](https://github.com/arfhh/lehrkraft-werkzeuge/releases/latest/download/TTS-Basics.zip) |

## Text zu Sprache (`tts-basics`) einrichten

Die Skill bereitet Texte zum Vorlesen auf; vertont wird mit dem frei
lizenzierten Modell **Chatterbox Multilingual** (MIT) auf dem eigenen
Rechner, offline und kostenlos. Das muss einmal installiert werden:

Am einfachsten: Claude in der Desktop-App bitten, Chatterbox einzurichten —
die Skill kennt den Ablauf. Von Hand geht es so (die Skripte liegen im
Plugin unter `scripts/`, im ZIP unter `py-scripts/`):

1. **Mac mit Apple Silicon** (ohne Admin-Rechte, Homebrew oder git):
   `bash scripts/installieren_macos.sh ~/chatterbox-tts`.
   Der erste Start laedt die Modellgewichte (ca. 3 GB), danach offline.
2. **Ohne Terminal weiterarbeiten:**
   `bash scripts/starter_bauen.sh ~/chatterbox-tts ~/Chatterbox` legt zwei
   Programme zum Doppelklicken an (Weboberflaeche, „Ordner vertonen")
   sowie die Ordner `Eingang/`, `Ausgang/` und `Stimmen/`.
3. **Linux, Windows, Speicherorte, Deinstallation:**
   [`installation.md`](plugins/tts-basics/skills/1-text-zu-sprache/installation.md).

Voraussetzungen: 16 GB Arbeitsspeicher empfohlen, ca. 8 GB frei, Python
3.11 (das Mac-Skript bringt es selbst mit). Installationsordner nicht in
iCloud/Dropbox legen.

**Stimmen.** Ohne Angabe spricht eine Standardstimme. Eigene Stimme: 10–20 s
Sprachprobe als WAV in `Stimmen/` legen. Sprecherstimmen aus gemeinfreien
**LibriVox-Hoerbuechern** gewinnen: Aufnahme suchen, 12 s ab Minute 1
ausschneiden, als WAV in `Stimmen/` legen — Schritt fuer Schritt mit
ffmpeg-Befehl und Hinweisen zum Stimmrecht in
[`sprachprobe.md`](plugins/tts-basics/skills/1-text-zu-sprache/sprachprobe.md).

## Fertige Erweiterungen zum Anschauen

Die Moodle-Erweiterungen, die mit `browser-basics` gebaut und gepflegt
werden, liegen in einem eigenen Repo:
<https://github.com/arfhh/moodle-erweiterungen>

## Lizenz

`h5p-basics`, `browser-basics` und `tts-basics`: **CC BY 4.0** — nutzen, aendern und
weitergeben mit Namensnennung.
`moodle-basics`: **CC BY-SA 4.0** — zusaetzlich Weitergabe unter gleichen
Bedingungen, weil Teile auf Vorarbeiten unter dieser Lizenz beruhen.
