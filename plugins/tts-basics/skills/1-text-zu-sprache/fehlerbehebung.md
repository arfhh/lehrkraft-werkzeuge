# Fehlerbehebung

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

Allgemein: die vollständige Fehlermeldung samt Betriebssystem und
Python-Version an eine KI geben — das führt meist schnell zum Ziel.

## Installation

| Meldung / Symptom | Ursache und Lösung |
|---|---|
| `No matching distribution found for torch==2.6.0` | Falsche Python-Version. venv mit Python 3.11 neu anlegen. |
| Fehler beim Bauen von `pkuseg`, `numpy` o. ä. | Ebenfalls meist Python ≥ 3.12. Python 3.11 verwenden; unter macOS ggf. `xcode-select --install`. |
| `'NoneType' object is not callable` mit `Perth` | Wasserzeichen-Modul unter neuerem Python/ohne setuptools. `pip install setuptools` und Python 3.11. |
| `git: command not found` bzw. macOS öffnet den Xcode-Dialog | Ohne git installieren: Pakete als ZIP-URL statt `git+` (macOS-Skript tut das, `installation.md`). Dialog abbrechen. |
| `Failed to download and build resemble-perth … Git operation failed` | Abhängigkeit kommt per git. Mit `uv pip install --override` auf die ZIP-URL umbiegen (`installation.md`). |
| `brew: command not found` | Homebrew ist nicht nötig – das macOS-Skript nutzt uv. |
| `ffmpeg fehlt` | `pip install imageio-ffmpeg` in der Umgebung genügt. |
| `ConnectTimeout … github.com … spacy_ontonotes.zip` beim ersten Start | Kurzer Netz-Aussetzer beim Nachladen der Chinesisch-Wortzerlegung (5 s Zeitlimit). Einfach erneut starten. |
| Download der Gewichte bricht ab | Netz prüfen, erneut starten — bereits geladene Teile bleiben erhalten. |

## Laufzeit

| Symptom | Lösung |
|---|---|
| Starter-App tut nichts / Oberfläche öffnet sich nicht | Protokoll `oberflaeche.log` bzw. `ordner_vertonen.log` im Installationsordner lesen. Nach dem Verschieben des Installationsordners Starter neu bauen. |
| Oberfläche: `InvalidPathError … allowed_paths` | Ausgabeordner muss in `launch(allowed_paths=…)` stehen; aktuelle `oberflaeche.py` verwenden. |
| Ohne Internet: Fehler beim Laden von Hugging Face | `HF_HUB_OFFLINE=1` setzen (die Starter tun das). |
| `TypeError … t3_model` bzw. Hinweis „es läuft v2“ | PyPI-Fassung installiert. Aus GitHub neu installieren (`installation.md`, Aktualisieren). |
| Langer Lauf wird immer langsamer (Apple Silicon, z. B. von 15 auf 2 Schritte/s) | Grafikspeicher läuft voll bzw. Mac drosselt sich (Akku, Wärme). Netzteil anschließen, kühl aufstellen; das Skript leert den Grafikspeicher nach jedem Stück. Normal auf M-Chips: Rechenzeit etwa 2–2,5 × Audiodauer. |
| Halbe Genauigkeit (`float16`) auf `mps` | Bricht mit `MPSGraph … mps.add` ab – nicht verwenden. |
| Absturz oder `NotImplementedError` auf `mps` | `--geraet cpu`. Langsamer, aber stabil. Danach Chatterbox aktualisieren und `mps` erneut testen. |
| Sehr langsam | `--geraet` prüfen (Ausgabe „Lade … auf 'cpu'“?). Auf Apple Silicon sollte `mps` erscheinen. Andere speicherhungrige Programme schließen. |
| Englischer Akzent / falsche Sprache | `--sprache` prüfen; Sprachprobe in der Zielsprache verwenden oder `--cfg 0`. |
| Wörter verschluckt, Satzende abgeschnitten | Satz kürzen; Sätze mit Punkt beenden; anderen `--seed`. |
| Laute wiederholt, Stottern, Brummen | `--temperatur 0.6`, Satz umformulieren, anderen `--seed`. |
| Zu hektisch | `--cfg 0.3`, `--ausdruck 0.4`. |
| Zahl/Abkürzung falsch gesprochen | Im Sprechtext ausschreiben (`sprechtext-regeln.md`). |
| Stimme klingt nicht nach der Probe | Bessere Probe aufnehmen (`sprachprobe.md`): länger, rauschärmer, gleiche Sprache. |
| Großbuchstabenwort wird buchstabiert | Normal schreiben. |
| Erstes Wort fehlt | Text mit einem kurzen Einleitungswort beginnen oder Satz umstellen. |
