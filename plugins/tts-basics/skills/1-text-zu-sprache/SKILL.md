---
name: 1-text-zu-sprache
description: "Texte lokal und offline in natürlich klingende Sprachaufnahmen (MP3) umwandeln mit dem frei lizenzierten Modell Chatterbox Multilingual (MIT), wahlweise in einer mitgelieferten oder der eigenen, geklonten Stimme: Installation auf macOS (Apple Silicon, ohne Admin/Homebrew), Linux und Windows, Doppelklick-Starter mit Weboberfläche, Deinstallation, Aufnahme der Sprachprobe, Regeln für Sprechtexte (Zahlen, Abkürzungen, Einheiten, Pausen), das Skript text_zu_mp3.py mit Satzaufteilung, Lautheitsangleichung und Lizenz-Metadaten, die Lizenzlage der Audios (warum NC-Modelle für CC BY ausscheiden), KI-Kennzeichnung und Fehlerbehebung. Rein technisch: fachliche Ausspracheregeln (z. B. Formeln) liefert eine Fach-Skill; NICHT für das Einbauen der Audiodatei in H5P, dafür `1-h5p`. IMMER verwenden bei „Text zu Sprache“, „TTS“, „vorlesen lassen“, „Audio erzeugen“, „Sprechtext“, „Stimme klonen“, „Chatterbox“, „Vorlese-Audio erzeugen“, „MP3 aus Text“ — auch ohne Skill-Namen."
---

# Lokale Sprachausgabe mit Chatterbox

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — Technik, frei weitergebbar

## Wegweiser

| Datei | Wann lesen |
|---|---|
| `installation.md` | Einrichtung auf einem neuen Rechner, Update auf neue Modellversion |
| `sprachprobe.md` | Eigene Stimme klonen: Referenzaufnahme planen und aufbereiten |
| `sprechtext-regeln.md` | Jeder Rohtext, der vertont werden soll |
| `lizenz-und-kennzeichnung.md` | Vor dem Veröffentlichen; bei Fragen zu anderen TTS-Modellen |
| `fehlerbehebung.md` | Fehlermeldung, Abbruch, seltsame Laute, falsche Sprache |
| `scripts/installieren_macos.sh` | Einrichtung auf einem Mac mit Apple Silicon, ohne Admin/Homebrew/git |
| `scripts/starter_bauen.sh` | macOS: zwei Doppelklick-Starter (Oberfläche, Ordner vertonen) |
| `scripts/oberflaeche.py` | Lokale Weboberfläche (Gradio) für Nutzer ohne Terminal |
| `scripts/deinstallieren_macos.sh` | Alles wieder entfernen, mit Rückfrage |
| `scripts/text_zu_mp3.py` | Erzeugt aus Textdatei(en) fertige MP3s |
| `README.md` | Für Menschen: Überblick zum Nachbauen (z. B. auf GitHub) |

## Das Modell in Kürze

- **Chatterbox Multilingual** von Resemble AI, Lizenz **MIT** für Code und
  Gewichte. Die erzeugten Audios unterliegen keiner Einschränkung und
  dürfen z. B. unter CC BY veröffentlicht werden.
- 23 Sprachen, darunter Deutsch (`de`), Englisch, Französisch, Spanisch,
  Italienisch, Niederländisch, Polnisch, Türkisch, Russisch.
- **Modellversionen:** `v2` steckt im PyPI-Paket, `v3` (bessere Qualität)
  nur im Quellcode auf GitHub. Darum wird aus GitHub installiert und im
  Skript `--modell v3` gesetzt (Standard). Fehlt v3, fällt das Skript mit
  Warnung auf v2 zurück.
- Läuft vollständig offline nach dem ersten Download der Gewichte
  (wenige GB). Kein Konto, kein Token nötig.
- Jede Ausgabe trägt ein **unhörbares Wasserzeichen** (PerTh), das MP3-
  Kompression übersteht. Es ersetzt die sichtbare Kennzeichnung nicht.

## Ablauf je Vertonung

1. **Rohtext → Sprechtext.** Nach `sprechtext-regeln.md` umschreiben:
   alles so, wie es gesprochen wird. Fachgebundene Regeln (Formeln,
   Fachsymbole) kommen aus der zuständigen Fach-Skill, falls vorhanden.
   Ergebnis dem Nutzer zum Gegenlesen zeigen, bevor vertont wird.
2. **Textdatei anlegen.** Eine `.txt` je Audiodatei, UTF-8. Der Dateiname
   wird zum MP3-Namen. Absätze durch Leerzeile trennen; jeder Absatz
   bekommt eine etwas längere Pause.
3. **Skript starten** (im eingerichteten Ordner):

   ```bash
   .venv/bin/python text_zu_mp3.py meintext.txt
   .venv/bin/python text_zu_mp3.py texte/ --stimme meine_stimme.wav --autor "Name"
   ```

   Ohne `--stimme` spricht die mitgelieferte Standardstimme. Ein Ordner
   als Eingabe vertont alle `.txt` darin.
4. **Anhören.** Jede Datei einmal vollständig. Typische Fehler: verschluckte
   Wörter, falsche Betonung, Wiederholungen. Betroffenen Satz umformulieren
   oder mit anderem `--seed` neu erzeugen.
5. **Kennzeichnen und lizenzieren.** Siehe `lizenz-und-kennzeichnung.md`.
   Das Skript schreibt Titel, Autor, Lizenz und KI-Hinweis in die MP3-
   Metadaten.

## Wichtige Schalter von `text_zu_mp3.py`

| Schalter | Standard | Wirkung |
|---|---|---|
| `--sprache` | `de` | Sprachcode, muss zur Textsprache passen |
| `--stimme` | — | WAV-Referenz der zu klonenden Stimme |
| `--modell` | `v3` | `v2` als Rückfall |
| `--ausdruck` | `0.65` | 0.3 ruhig-sachlich, 0.7 lebhaft; ab 0.8 mehr Aussetzer |
| `--cfg` | `0.5` | niedriger = langsamer, bedächtiger; `0` gegen fremden Akzent |
| `--temperatur` | `0.95` | niedriger = gleichmäßiger, aber hölzerner |
| `--seed` | `42` | anderer Wert = andere Sprechvariante |
| `--geraet` | `auto` | `mps`, `cuda` oder `cpu` erzwingen |
| `--autor`, `--lizenz` | —, `CC BY 4.0` | landen in den MP3-Metadaten |

Die Standardwerte (Ausdruck 0.65, CFG 0.5, Temperatur 0.95, Pause 0.35)
sind im Hörvergleich für Fachtexte am natürlichsten. Zu niedrige Werte
(Ausdruck/CFG 0.35, Temperatur 0.7) klingen hölzern. Für ruhigere
Arbeitsanweisungen: `--ausdruck 0.45 --cfg 0.4`.

## Was Claude dabei tut

- **Im Chat** (ohne Zugriff auf den Rechner): Sprechtext aufbereiten,
  `.txt`-Dateien bereitstellen, den passenden Befehl nennen. Vertont wird
  auf dem Rechner des Nutzers.
- **Mit Zugriff auf den Rechner** (z. B. Agent-Umgebung): zusätzlich das
  Skript ausführen und die MP3s ablegen. Vor dem ersten Lauf prüfen, ob die
  Einrichtung nach `installation.md` vorhanden ist. Ausführen in einer
  echten Shell des Rechners (nicht in einer Linux-VM), Python direkt aus
  `.venv/bin/python` aufrufen, Pfade immer in Anführungszeichen.
- **Für Nutzer ohne Terminal**: Starter bauen (`installation.md`).
- Nur die Stimme der Person klonen, die das selbst wünscht, oder einer
  Person mit ausdrücklicher Zustimmung. Bei fremden Stimmen ohne
  erkennbare Zustimmung nicht mitwirken.
