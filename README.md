# Werkzeuge fuer Lehrkraefte — Skills fuer Claude

Skills rund um **H5P**, **Moodle** und **Chrome-Erweiterungen**, entstanden
im Chemieunterricht und in der Fortbildung am LI Hamburg.
Autor: Arne Spielhoff. Fassung 1.3.0, Stand 20.09.2026.

## Was ist das hier?

Du brauchst dafuer **Claude**, einen KI-Assistenten von Anthropic. Man
arbeitet entweder im Chat auf **claude.ai** mit ihm, oder in einer
Arbeitsumgebung namens **Cowork** bzw. **Claude Code** (fuer
Programmierumgebungen) — dort kann Claude zusaetzlich eigene Dateien lesen,
schreiben und Programme ausfuehren, nicht nur chatten.

Eine **Skill** ist eine Anleitung, die Claude **vor** einer bestimmten
Aufgabe liest, bevor es loslegt. Ohne Skill improvisiert Claude — mit einer
passenden Skill haelt es sich an einen festen, erprobten Ablauf: welcher
Bewertungsmassstab gilt, welches Dateiformat am Ende herauskommen muss,
welche Fallstricke es gibt. Die Skills in diesem Repo sind genau solche
Anleitungen, aus echtem Unterrichtseinsatz entstanden.

Ein **Plugin** ist ein fertiges Paket aus einer oder mehreren solchen
Skills (plus allem, was dazugehoert: Beispieldateien, kleine
Hilfsprogramme), das sich mit zwei kurzen Chat-Befehlen installieren laesst
— siehe unten. Nichts muss von Hand irgendwo hineinkopiert werden.

## Fuer wen ist das?

Fuer Lehrkraefte, die mit Claude arbeiten (Desktop-App, Claude Code oder
claude.ai) und eine dieser vier Aufgaben regelmaessig haben: interaktive
H5P-Uebungen bauen, Moodle-Testfragen erstellen, PDF-Abgaben lesen und
rueckmelden, oder selbst kleine Browser-Erweiterungen fuer eine
Lernplattform bauen. Fachlich sind die Skills bewusst **nicht auf Chemie
beschraenkt** — die Bewertungs- und Feedbackregeln gelten fachunabhaengig
fuer jedes Fach.

Es gibt zwei Wege, das zu installieren, je nachdem womit du arbeitest.

## Weg 1 — Claude-Desktop-App oder Claude Code (empfohlen)

Eine Installation, alle Begleitdateien und Skripte sind dabei. Du tippst
diese zwei Zeilen einfach als Chat-Nachricht an Claude:

    /plugin marketplace add arfhh/lehrkraft-werkzeuge
    /plugin install h5p-basics@lehrkraft-werkzeuge

Die erste Zeile sagt Claude, wo es nach Paketen suchen soll (dieses
GitHub-Repo). Die zweite installiert eines davon. Statt `h5p-basics` geht
auch `moodle-basics`, `browser-basics` oder `abgaben-basics` — oder alle
vier nacheinander. Danach einmal `/reload-plugins` tippen, damit Claude die
neuen Skills auch wirklich einliest.

## Weg 2 — Claude im Browser (claude.ai)

Auf claude.ai lassen sich keine Plugins installieren. Dort geht es nur
manuell: unter **Releases** dieses Repos das passende ZIP herunterladen,
entpacken, den Ordner ins eigene Projekt legen und die Skills aus dem
Unterordner `Skill/` im eigenen Konto als Skill anlegen (Name plus
Dateiinhalt hineinkopieren). Die genaue Anleitung liegt als `LIESMICH.md`
in jedem ZIP.

## Die vier Buendel — was sie konkret koennen

| Buendel | Skills | Wofuer |
|---|---|---|
| `h5p-basics` | `1-h5p`, `2-didaktik-h5p` | H5P-Dateien auf Dateiebene bauen, pruefen und reparieren, plus die didaktische Beurteilung interaktiver Lerneinheiten. |
| `moodle-basics` | `1-moodle-xml`, `2-didaktik-bewertung` | Moodle-Fragen als XML erzeugen und importieren, mit Cloze-Formenkanon und Bewertungsmassstab. |
| `browser-basics` | `1-webext-robustheit`, `1-browser-wxt` | Browser-Erweiterungen bauen, die auf einer fremden Weboberflaeche wie Moodle arbeiten -- robuste Laufzeit-Technik plus WXT-Aufbau fuer Chrome, Firefox und Edge aus einer Codebasis. |
| `abgaben-basics` | `1-pdf-abgaben`, `2-didaktik-abgaben`, `2-didaktik-bewertung` | PDF-Datei-Abgaben tokensparsam auslesen (Vordruck-Abzug, Duplikaterkennung, Kontaktbogen fuer Handschrift) und ueber Wochen laufende Aufgabenserien fachunabhaengig bewerten und rueckmelden. |

Konkret heisst das:

- **`h5p-basics`** — Claude kann fertige interaktive H5P-Uebungen
  (Lueckentexte, Zuordnungen, verzweigte Lernpfade, Karteikarten …) direkt
  als Datei bauen, kaputte reparieren oder inhaltlich verbessern, ohne dass
  du den H5P-Editor von Hand bedienst.
- **`moodle-basics`** — Claude kann Testfragen fuer dein Moodle fertig als
  importierbare Datei schreiben, inklusive Luecken, die viele
  Schreibweisen und Tippfehler automatisch richtig einordnen, nach einem
  einheitlichen, durchdachten Bewertungsmassstab.
- **`browser-basics`** — fuer alle, die selbst kleine
  Browser-Erweiterungen fuer Moodle oder eine andere Lernplattform bauen
  wollen: Claude kennt damit den technischen Aufbau und die typischen
  Fallstricke, wie sie auch in den sechs Erweiterungen unten stecken.
- **`abgaben-basics`** — Claude kann eingereichte PDF-Arbeitshefte lesen
  (auch ausgefuellte Formularfelder und handschriftliche Zeichnungen),
  dabei sparsam mit Rechenaufwand umgehen, Duplikate erkennen, und ueber
  Wochen laufende Aufgabenserien fair und nachvollziehbar zurueckmelden.

## Und was sind die Chrome-Erweiterungen?

Skills geben Claude nur **Fachwissen** — sie holen selbst keine Daten aus
Moodle. Dafuer gibt es zusaetzlich sechs kleine **Browser-Erweiterungen**
(kleine Zusatzprogramme, die man im Browser installiert, nicht auf dem
Computer). Einmal installiert, erscheint auf bestimmten Moodle-Seiten
(z. B. der Bewerten-Uebersicht eines Tests) ein zusaetzlicher Knopf oder
ein kleines Panel. Klickst du ihn an, liest die Erweiterung die Seite aus
und baut daraus einen fertigen Text (einen "Prompt"), den du in einen
Claude-Chat einfuegst. Claude beantwortet ihn, du kopierst die Antwort
zurueck in die Erweiterung — sie traegt Note und Feedback dann in Moodles
eigene Felder ein, aber **abgeschickt wird immer von Hand** mit Moodles
eigenem Speichern-Knopf. Nichts wird ungesehen uebernommen, und keine
Erweiterung schickt Daten an einen fremden Server oder braucht einen
API-Schluessel.

Alle sechs liegen mit eigener, ausfuehrlicher Installationsanleitung (fuer
Chrome, Firefox und Edge, Schritt fuer Schritt) in einem eigenen Repo:
<https://github.com/arfhh/moodle-erweiterungen> — Bewerten
(Klausuren), Nachbewerten (Kurztests), Coaching (kurze Freitextantworten),
Datei-Abgaben bewerten (PDF-Arbeitshefte), Cloze-Autofill (Fragensammlung
pflegen) und Notenstufen-Autofill.

## Lizenz

`h5p-basics`, `browser-basics` und `abgaben-basics`: **CC BY 4.0** — nutzen,
aendern und weitergeben mit Namensnennung.
`moodle-basics`: **CC BY-SA 4.0** — zusaetzlich Weitergabe unter gleichen
Bedingungen, weil Teile auf Vorarbeiten unter dieser Lizenz beruhen.
