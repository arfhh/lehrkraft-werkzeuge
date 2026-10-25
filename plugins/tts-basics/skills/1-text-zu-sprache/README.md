# 1-text-zu-sprache — Texte lokal vertonen, auch mit der eigenen Stimme

Eine Skill für Claude und zugleich eine Anleitung für Menschen: Texte werden
**auf dem eigenen Rechner** in natürlich klingende MP3-Dateien umgewandelt —
mit einer mitgelieferten Stimme oder der **eigenen, geklonten Stimme**. Kein
Online-Dienst, keine Kosten, und die Audios dürfen frei (z. B. unter
CC BY) veröffentlicht werden.

Typischer Einsatz: Vorlese-Audios zu Arbeitsanweisungen, Sachtexten und
interaktiven Lerneinheiten (z. B. H5P), damit Lernende Texte hören statt
nur lesen können.

## Warum Chatterbox?

| | Chatterbox Multilingual | XTTS v2 |
|---|---|---|
| Lizenz der Gewichte | **MIT** | CPML (nicht-kommerziell, auch für Audios) |
| Audios unter CC BY veröffentlichen | ja | nein |
| Weiterentwicklung | aktiv (Resemble AI) | eingestellt |
| Deutsch, Stimmklonen | ja | ja |
| Apple Silicon | ja (MPS) | praktisch nur CPU |

Details: [`lizenz-und-kennzeichnung.md`](lizenz-und-kennzeichnung.md).

## Schnellstart (macOS mit Apple Silicon)

```bash
bash scripts/installieren_macos.sh            # ohne Admin, Homebrew oder git
cd ~/chatterbox-tts
.venv/bin/python text_zu_mp3.py meintext.txt
.venv/bin/python text_zu_mp3.py meintext.txt --stimme meine_stimme.wav --autor "Vorname Nachname"
```

Ohne Terminal weiterarbeiten: `bash scripts/starter_bauen.sh ~/chatterbox-tts ~/Chatterbox`
legt zwei Programme zum Doppelklicken an (Weboberfläche und „Ordner vertonen“).
Entfernen: `bash scripts/deinstallieren_macos.sh ~/chatterbox-tts ~/Chatterbox`.

Linux und Windows: [`installation.md`](installation.md).

## Inhalt

| Datei | Inhalt |
|---|---|
| `SKILL.md` | Anweisungen für Claude (Ablauf, Schalter) |
| `installation.md` | Einrichtung auf macOS, Linux, Windows; Starter; Speicherorte; Deinstallation |
| `sprachprobe.md` | Die eigene Stimme gut aufnehmen und aufbereiten; Sprecherstimmen aus LibriVox-Hörbüchern gewinnen |
| `sprechtext-regeln.md` | Texte vorlesefertig machen, mit Prompt für jede KI |
| `lizenz-und-kennzeichnung.md` | Lizenzlage, Stimmrechte, KI-Kennzeichnung |
| `fehlerbehebung.md` | Häufige Fehler und Lösungen |
| `scripts/text_zu_mp3.py` | Vertont eine Textdatei oder einen ganzen Ordner |
| `scripts/installieren_macos.sh` | Einrichtung auf dem Mac in einem Schritt |
| `scripts/oberflaeche.py` | Lokale Weboberfläche im Browser |
| `scripts/starter_bauen.sh` | Doppelklick-Starter für macOS |
| `scripts/deinstallieren_macos.sh` | Alles wieder entfernen |

## Als Skill in Claude nutzen

Ordner `1-text-zu-sprache` als ZIP in Claude unter *Einstellungen → Skills* hochladen.
Claude bereitet dann Sprechtexte auf und nennt die passenden Befehle; in einer
Umgebung mit Rechnerzugriff führt es das Skript auch selbst aus.

## Verantwortung

Nur die eigene Stimme klonen oder die einer Person mit ausdrücklicher
Zustimmung. Hörende darauf hinweisen, dass eine KI spricht.

## Lizenz

Skill, Anleitungen und Skripte: © 2026 A. Spielhoff, **CC BY 4.0**.
Chatterbox: © Resemble AI, MIT-Lizenz — https://github.com/resemble-ai/chatterbox
