# Sprachprobe für die eigene Stimme

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

Chatterbox klont ohne Training: aus der Sprachprobe wird bei jedem Start
ein Stimmprofil berechnet. Die Qualität der Probe bestimmt die Qualität
jeder späteren Aufnahme.

## Aufnahme

- **Länge:** 10 bis 20 Sekunden zusammenhängende Sprache. Kürzer klingt
  unähnlich, länger bringt kaum Gewinn.
- **Sprache:** dieselbe wie die späteren Texte. Für englische Texte eine
  eigene englische Probe aufnehmen; sonst schleicht sich ein Akzent ein
  (Notlösung: `--cfg 0`).
- **Sprechweise:** so, wie die Texte klingen sollen — ruhig erklärend für
  Sachtexte. Die Probe überträgt Tempo und Stimmung mit.
- **Inhalt:** ganze Sätze mit Fragen und Aussagen, keine Liste einzelner
  Wörter. Beispiel:

  > Heute schauen wir uns an, wie das funktioniert. Zuerst lest ihr den
  > Text in Ruhe durch. Habt ihr eine Frage? Dann notiert sie am Rand.
  > Danach vergleicht ihr eure Ergebnisse zu zweit.

- **Umgebung:** kleiner, möblierter Raum, Fenster zu, kein Lüfter. Headset-
  oder USB-Mikrofon, etwa eine Handbreit vor dem Mund. Laptop-Mikrofon
  geht, klingt aber hallig.

## Aufbereitung (z. B. mit Audacity)

1. Anfang und Ende auf etwa 0,2 s Stille kürzen, Versprecher herausschneiden.
2. Rauschen entfernen (Effekt „Rauschverminderung“, Profil aus einer
   stillen Stelle), sparsam einsetzen.
3. Normalisieren auf etwa −1 dB Spitze.
4. Exportieren als **WAV, Mono, 24 000 oder 44 100 Hz, 16 Bit**.

Mehrere Proben lohnen sich: kurze Testsätze mit jeder vertonen und die
beste behalten.

## Sprecherstimmen aus LibriVox-Hörbüchern

Wer die eigene Stimme nicht nutzen will, findet bei **LibriVox**
(librivox.org) Tausende Hörbücher, die Freiwillige einlesen und als
**gemeinfrei (Public Domain)** freigeben. Ein kurzer Ausschnitt daraus
eignet sich als Sprachprobe.

### 1. Aufnahme finden

1. Auf librivox.org suchen, Filter **Sprache: Deutsch**.
2. Am besten ein **Solo**-Projekt wählen (ein Buch, eine Stimme). Bei
   Sammelprojekten steht der Name je Kapitel in der Kapitelliste.
3. Eine Probe anhören: ruhig, deutlich, ohne Hall und Rauschen, Tempo
   wie bei einem Sachtext. Lebhaft gespielte Romanstellen und Dialoge mit
   verstellten Stimmen sind ungeeignet.
4. Ein Kapitel als MP3 laden. Bessere Qualität (128 kbit/s statt 64)
   gibt es über den Link **Internet Archive** auf derselben Seite.

### 2. Ausschnitt schneiden

Chatterbox wertet nur die **ersten 10 Sekunden** einer Probe aus. Am
Kapitelanfang steht die LibriVox-Ansage („Dies ist eine LibriVox-Aufnahme
…“), deshalb erst ab etwa Minute 1 schneiden. Das ffmpeg aus der
Installation liegt im Installationsordner unter `.venv/bin/ffmpeg`:

```bash
cd ~/chatterbox-tts
.venv/bin/ffmpeg -ss 60 -t 12 -i "kapitel_01.mp3" -ac 1 -ar 24000 -sample_fmt s16 \
  "/Pfad/zum/Ablageordner/Stimmen/LibriVox_Vorname_Nachname_w.wav"
```

- `-ss 60` = Startpunkt in Sekunden, `-t 12` = Länge. Beginnt die Stelle
  mitten im Satz oder mit Atmer, den Startpunkt um ein paar Sekunden
  verschieben.
- Namensschema `LibriVox_<Vorname>_<Nachname>_<w|m>.wav`, so bleibt die
  Herkunft am Dateinamen erkennbar.
- Abgelegt im Ordner `Stimmen/` erscheint die Stimme in beiden
  Doppelklick-Starten.

### 3. Prüfen

Einen Testsatz mit der neuen Stimme vertonen und anhören. Klingt sie
dumpf, hallig oder mit fremdem Akzent, eine andere Stelle desselben
Kapitels schneiden. Zwei bis drei Ausschnitte vergleichen lohnt sich.

### Rechtliches

- Die **Aufnahme** ist gemeinfrei: ausschneiden und weiterverarbeiten ist
  erlaubt, auch für Material unter CC BY.
- Die **Stimme** selbst ist davon nicht erfasst. Das Recht an der eigenen
  Stimme ist ein Persönlichkeitsrecht, und ob die Gemeinfrei-Erklärung
  das Klonen abdeckt, ist nicht geklärt. Darum: die Sprecherin oder den
  Sprecher nicht als Urheber der neuen Audios ausgeben, die Audios
  deutlich als KI-Stimme kennzeichnen (`lizenz-und-kennzeichnung.md`),
  in den Metadaten die Quelle nennen (z. B. „Stimmvorlage: LibriVox,
  gemeinfrei“) und die Stimme auf Bitte der Person sofort entfernen.
- Die Demo-Stimmen (`Demo_*.wav`) aus der Resemble-Oberfläche haben keine
  Lizenz: nur zum Ausprobieren, nicht für Veröffentlichungen.

## Zustimmung

Nur die eigene Stimme oder die einer Person mit ausdrücklicher, am besten
schriftlicher Zustimmung. Die Sprachprobe ist personenbezogen: nicht
veröffentlichen, nicht in geteilte Ordner legen.
