# Installation von Chatterbox Multilingual

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

## Voraussetzungen

- **Rechner:** 16 GB Arbeitsspeicher empfohlen, etwa 8 GB freier Platz.
  Grafikkarte nicht nötig, beschleunigt aber deutlich (Apple Silicon über
  MPS, NVIDIA über CUDA).
- **Python 3.11.** Das Paket pinnt `torch==2.6.0`; mit Python 3.12+ treten
  Probleme beim Wasserzeichen-Modul auf, 3.13+ zieht andere Pakete nach.
  3.11 ist der sichere Weg.
- **ffmpeg** für die MP3-Erzeugung, **git** für die Installation aus GitHub.
- Internet nur beim Einrichten und beim ersten Start (Download der
  Gewichte von Hugging Face). Danach offline.

## Installationsort wählen

- **Frei wählbar**, Standard `~/chatterbox-tts`. Den Ordner als Argument an
  das Installationsskript geben.
- **Nicht in einen Cloud-synchronisierten Ordner** (iCloud Drive, Dropbox,
  OneDrive …): die Umgebung hat zehntausende kleine Dateien und rund 1 GB.
- **Leerzeichen im Pfad** sind erlaubt, dann aber jeden Pfad in
  Anführungszeichen setzen. Die Skripte tun das durchgängig.

## macOS (Apple Silicon)

Automatisch, **ohne Admin-Rechte, ohne Homebrew, ohne git/Xcode-Werkzeuge**:

```bash
bash scripts/installieren_macos.sh "/Pfad/zum/Installationsordner"
```

Das Skript macht von Hand Folgendes:

```bash
curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh   # uv nach ~/.local/bin
cd "/Pfad/zum/Installationsordner"
~/.local/bin/uv venv --python 3.11 .venv          # Python 3.11 kommt von uv
echo "resemble-perth @ https://github.com/resemble-ai/Perth/archive/<commit>.zip" > overrides.txt
~/.local/bin/uv pip install --python .venv/bin/python --override overrides.txt \
  "chatterbox-tts @ https://github.com/resemble-ai/chatterbox/archive/refs/heads/master.zip" \
  imageio-ffmpeg gradio
# ffmpeg aus imageio-ffmpeg nach .venv/bin/ffmpeg verlinken; Skripte hineinkopieren
```

Warum so: Chatterbox und sein Wasserzeichen-Modul werden sonst per `git`
installiert, und `git` fehlt auf einem frischen Mac (der Aufruf öffnet nur
den Xcode-Installationsdialog). Als ZIP geht es ohne. ffmpeg kommt als
pip-Paket statt über Homebrew; `text_zu_mp3.py` findet es auch ohne PATH.

Wer Homebrew schon hat, kann alternativ `brew install python@3.11 ffmpeg`
und `pip install "git+https://github.com/resemble-ai/chatterbox.git"` nutzen.

### Starter zum Doppelklicken (macOS)

```bash
bash scripts/starter_bauen.sh "/Pfad/zum/Installationsordner" "/Pfad/zum/Ablageordner"
```

Legt im Ablageordner an:

| Eintrag | Zweck |
|---|---|
| `Chatterbox Oberfläche.app` | Startet die lokale Weboberfläche (`oberflaeche.py`) im Browser: Text eingeben, Stimme wählen, Regler, anhören, MP3 landet in `Ausgang/`. Erneut öffnen → läuft bereits: im Browser öffnen oder beenden. |
| `Chatterbox Ordner vertonen.app` | Vertont alle `.txt` aus `Eingang/` nach `Ausgang/`, fragt vorher nach der Stimme. |
| `Eingang/`, `Ausgang/`, `Stimmen/` | Texte, fertige MP3s, WAV-Sprachproben (`sprachprobe.md`) |

Die Starter laufen offline (`HF_HUB_OFFLINE=1`), Protokolle liegen als
`oberflaeche.log` bzw. `ordner_vertonen.log` im Installationsordner. Der
Ablageordner darf synchronisiert sein. Beim ersten Öffnen fragt macOS evtl.
nach einer Bestätigung (Rechtsklick → Öffnen).

## Linux (Debian/Ubuntu)

```bash
sudo apt install python3.11 python3.11-venv ffmpeg git
python3.11 -m venv ~/chatterbox-tts/.venv
source ~/chatterbox-tts/.venv/bin/activate
pip install --upgrade pip
pip install "git+https://github.com/resemble-ai/chatterbox.git"
```

Ist Python 3.11 nicht im Paketsystem: `uv` (https://docs.astral.sh/uv/)
installieren und `uv venv --python 3.11` verwenden.

## Windows

1. Python 3.11 von python.org installieren (Haken bei „Add to PATH“).
2. ffmpeg und git installieren, z. B. `winget install Gyan.FFmpeg Git.Git`.
3. In der Eingabeaufforderung:

```bat
py -3.11 -m venv %USERPROFILE%\chatterbox-tts\.venv
%USERPROFILE%\chatterbox-tts\.venv\Scripts\activate
pip install --upgrade pip
pip install "git+https://github.com/resemble-ai/chatterbox.git"
```

Mit NVIDIA-Karte vorher die CUDA-Fassung von torch 2.6 nach Anleitung auf
pytorch.org installieren, sonst rechnet die CPU.

## Erster Start

```bash
cd ~/chatterbox-tts && source .venv/bin/activate
echo "Hallo, das ist ein Test." > probe.txt
python text_zu_mp3.py probe.txt
```

Der erste Start lädt die Gewichte (Ordner `~/.cache/huggingface`). Danach
dauert das Laden des Modells nur noch Sekunden.

## Aktualisieren

```bash
source ~/chatterbox-tts/.venv/bin/activate
pip install --upgrade --force-reinstall --no-deps "git+https://github.com/resemble-ai/chatterbox.git"
```

Neue Modellversion (z. B. `v4`) prüfen: Datei `src/chatterbox/mtl_tts.py`
im GitHub-Projekt, Abschnitt `MULTILINGUAL_T3_MODELS`. Taucht dort ein neuer
Schlüssel auf, im Skript bei `--modell` unter `choices` ergänzen.

## Speicherorte und Größen

| Ort | Inhalt | Größe |
|---|---|---|
| Installationsordner | `.venv`, Skripte, Protokolle | ca. 1,1 GB |
| `~/.cache/huggingface/hub` | Modellgewichte | ca. 3 GB |
| `~/.pkuseg` | Wortzerlegung für Chinesisch (lädt beim ersten Start mit) | ca. 90 MB |
| `~/.local/bin/uv`, `~/.local/share/uv` | uv und seine Python-Fassung (nur macOS-Skript) | ca. 100 MB |

## Deinstallation

```bash
bash scripts/deinstallieren_macos.sh "/Pfad/zum/Installationsordner" ["/Pfad/zum/Ablageordner"]
```

Zeigt alles mit Größe an und löscht erst nach Rückfrage: Installationsordner,
Chatterbox-Gewichte, `~/.pkuseg`, die beiden Starter (Eingang/Ausgang/Stimmen
bleiben). uv nur auf zweite Rückfrage. Andere Systeme: dieselben Ordner von
Hand löschen.
