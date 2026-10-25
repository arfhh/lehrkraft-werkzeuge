#!/usr/bin/env bash
# Einrichtung von Chatterbox Multilingual auf macOS (Apple Silicon) – ohne Admin-Rechte,
# ohne Homebrew, ohne git/Xcode-Werkzeuge.
# © 2026 A. Spielhoff – lizenziert unter CC BY 4.0
# Aufruf:  bash installieren_macos.sh  [Zielordner, Standard: ~/chatterbox-tts]
# Zielordner nicht in einen Cloud-synchronisierten Ordner legen (iCloud, Dropbox …).
set -euo pipefail

ZIEL="${1:-$HOME/chatterbox-tts}"
HIER="$(cd "$(dirname "$0")" && pwd)"
UV="$HOME/.local/bin/uv"
CHATTERBOX="https://github.com/resemble-ai/chatterbox/archive/refs/heads/master.zip"
# Chatterbox verlangt das Wasserzeichen-Modul per git – hier als ZIP umgebogen
PERTH="https://github.com/resemble-ai/Perth/archive/ff1c8ac55a976971245cdd53c18d6131ca00d993.zip"

[[ "$(uname -m)" == "arm64" ]] || { echo "Dieses Skript ist für Apple Silicon (M1 bis M5)."; exit 1; }

echo "1/5  uv (Python-Verwaltung, landet in ~/.local/bin) …"
if [[ ! -x "$UV" ]]; then
  curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh
fi

echo "2/5  Ordner und Python-3.11-Umgebung in $ZIEL …"
mkdir -p "$ZIEL"
cd "$ZIEL"
"$UV" venv --python 3.11 .venv

echo "3/5  Chatterbox (mit Modell v3), ffmpeg und Oberfläche – ca. 1 GB …"
echo "resemble-perth @ $PERTH" > overrides.txt
"$UV" pip install --python .venv/bin/python --override overrides.txt \
  "chatterbox-tts @ $CHATTERBOX" imageio-ffmpeg gradio
FF="$(.venv/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
ln -sf "$FF" .venv/bin/ffmpeg

echo "4/5  Skripte kopieren …"
cp "$HIER/text_zu_mp3.py" "$HIER/oberflaeche.py" "$ZIEL/"

echo "5/5  Probelauf (lädt beim ersten Mal die Modellgewichte, ca. 3 GB) …"
echo "Hallo. Dies ist ein kurzer Test der lokalen Sprachausgabe." > probe.txt
.venv/bin/python text_zu_mp3.py probe.txt --autor "Test" \
  || { echo "Probelauf abgebrochen – bei Zeitüberschreitung einfach erneut starten:"; \
       echo "  cd \"$ZIEL\" && .venv/bin/python text_zu_mp3.py probe.txt"; exit 1; }

echo
echo "Fertig. probe.mp3 liegt in $ZIEL."
echo "Starter zum Doppelklicken bauen:"
echo "  bash \"$HIER/starter_bauen.sh\" \"$ZIEL\" \"<Ablageordner>\""
echo "Direkt im Terminal:"
echo "  cd \"$ZIEL\" && .venv/bin/python text_zu_mp3.py meintext.txt"
