# Lizenz und KI-Kennzeichnung

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

Keine Rechtsberatung — eine Einordnung für die übliche Veröffentlichung
von Lernmaterial.

## Zwei Lizenzen, nicht eine

Bei jedem TTS-System getrennt prüfen:

1. **Lizenz des Programms** (Code) — bestimmt, wie man die Software nutzt.
2. **Lizenz des Modells** (Gewichte) — bestimmt oft auch, was mit den
   **erzeugten Audios** geschehen darf.

Wer erzeugte Audios unter **CC BY** freigibt, erlaubt allen die
kommerzielle Weiternutzung. Das geht nur, wenn die Modell-Lizenz die
Ausgaben nicht auf nicht-kommerzielle Zwecke beschränkt.

| Modell | Lizenz Gewichte | Audios unter CC BY? |
|---|---|---|
| Chatterbox Multilingual | MIT | ja |
| XTTS v2 (Coqui) | CPML, ausdrücklich auch für Ausgaben nicht-kommerziell; kein Lizenzgeber mehr erreichbar | nein |
| Voxtral TTS (Mistral), Fish Audio u. a. | CC BY-NC bzw. eigene NC-Lizenz | unklar bis nein — höchstens CC BY-NC |
| Kokoro | Apache 2.0 | ja, aber ohne Stimmklonen |

Nicht-kommerzielle Modelle eignen sich zum Ausprobieren und für Material,
das selbst unter CC BY-NC erscheint.

## Rechte an der Stimme

Die Stimme gehört zu den Persönlichkeitsrechten. Eigene Stimme: frei
verwendbar. Fremde Stimme: nur mit ausdrücklicher Zustimmung, die die
geplante Veröffentlichung abdeckt. Mitgelieferte Standardstimmen fallen
unter die Modell-Lizenz.

## Kennzeichnung

Hörende sollen wissen, dass eine KI spricht — auch bei der eigenen Stimme.

- **Im Material**, sichtbar neben dem Audio: „Dieser Text wird von einer
  KI-Stimme vorgelesen.“ Bei geklonter Stimme: „… von einer KI-Version
  meiner Stimme vorgelesen.“
- **In der Datei:** `text_zu_mp3.py` schreibt Titel, Autor, Lizenz und den
  KI-Hinweis in die MP3-Metadaten (ID3).
- **Unhörbar:** Chatterbox setzt in jede Ausgabe ein PerTh-Wasserzeichen,
  das MP3-Kompression und Schnitt übersteht. Es ist ein Zusatz, keine
  Kennzeichnung für Menschen.

## Lizenzangabe für die Audiodatei

```
Audio: <Titel>, <Autor>, CC BY 4.0 — gesprochen mit KI (Chatterbox, Resemble AI, MIT)
```

Steht der vorgelesene Text unter einer fremden Lizenz (z. B. CC BY-SA),
übernimmt das Audio diese Lizenz als Bearbeitung; dann gilt die
Lizenz des Textes, nicht automatisch CC BY.

## Demo-Sprachproben von Resemble AI

Die Demo-Oberfläche im GitHub-Projekt (`multilingual_app.py`, `LANGUAGE_CONFIG`)
verweist auf je eine Sprachprobe pro Sprache (z. B. `de_f1.flac`). Sie lassen
sich als Klon-Referenz nutzen, tragen aber **keine Lizenzangabe** — anders als
Code und Gewichte (MIT). Darum nur zum Ausprobieren; für Veröffentlichungen
die eigene Stimme oder eine Stimme mit ausdrücklicher Zustimmung verwenden.
