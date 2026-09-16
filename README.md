# Werkzeuge fuer Lehrkraefte — Skills fuer Claude

Skills rund um **H5P**, **Moodle** und **Chrome-Erweiterungen**, entstanden
im Chemieunterricht und in der Fortbildung am LI Hamburg.
Autor: Arne Spielhoff. Fassung 1.1.0, Stand 16.09.2026.

Es gibt zwei Wege, je nachdem womit du arbeitest.

## Weg 1 — Claude-Desktop-App oder Claude Code (empfohlen)

Eine Installation, alle Begleitdateien und Skripte sind dabei.

    /plugin marketplace add arfhh/lehrkraft-werkzeuge
    /plugin install h5p-basics@lehrkraft-werkzeuge

Statt `h5p-basics` geht auch `moodle-basics` oder `browser-basics`.
Danach einmal `/reload-plugins`.

## Weg 2 — Claude im Browser (claude.ai)

Unter **Releases** das passende ZIP herunterladen, entpacken, den Ordner ins
eigene Projekt legen und die Skills aus dem Unterordner `Skill/` im Konto
anlegen. Die Anleitung liegt als `LIESMICH.md` im ZIP.

## Die drei Buendel

| Buendel | Skills | Wofuer |
|---|---|---|
| `h5p-basics` | `1-h5p`, `2-didaktik-h5p` | H5P-Dateien auf Dateiebene bauen, pruefen und reparieren, plus die didaktische Beurteilung interaktiver Lerneinheiten. |
| `moodle-basics` | `1-moodle-xml`, `2-didaktik-bewertung` | Moodle-Fragen als XML erzeugen und importieren, mit Cloze-Formenkanon und Bewertungsmassstab. |
| `browser-basics` | `1-webext-robustheit`, `1-browser-wxt` | Browser-Erweiterungen bauen, die auf einer fremden Weboberflaeche wie Moodle arbeiten -- robuste Laufzeit-Technik plus WXT-Aufbau fuer Chrome, Firefox und Edge aus einer Codebasis. |

## Fertige Erweiterungen zum Anschauen

Die fuenf Chrome-Erweiterungen fuer Moodle, die mit `browser-basics` gebaut
und gepflegt werden, liegen in einem eigenen Repo:
<https://github.com/arfhh/moodle-chrome-erweiterungen> — Bewerten,
Nachbewerten, Coaching, Cloze-Autofill und Notenstufen.

## Lizenz

`h5p-basics` und `browser-basics`: **CC BY 4.0** — nutzen, aendern und
weitergeben mit Namensnennung.
`moodle-basics`: **CC BY-SA 4.0** — zusaetzlich Weitergabe unter gleichen
Bedingungen, weil Teile auf Vorarbeiten unter dieser Lizenz beruhen.
