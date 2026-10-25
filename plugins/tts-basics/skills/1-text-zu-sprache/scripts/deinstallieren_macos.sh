#!/usr/bin/env bash
# Entfernt Chatterbox wieder vollständig (macOS).
# © 2026 A. Spielhoff – lizenziert unter CC BY 4.0
# Aufruf:  bash deinstallieren_macos.sh  INSTALLATIONSORDNER  [ABLAGEORDNER der Starter]
set -euo pipefail
INST="${1:?Installationsordner fehlt}"; ABL="${2:-}"
frage() { read -r -p "$1 [j/N] " a; [[ "$a" =~ ^[jJyY]$ ]]; }
groesse() { du -sh "$1" 2>/dev/null | cut -f1; }

echo "Wird entfernt:"
echo "  $INST  ($(groesse "$INST"))"
for d in "$HOME"/.cache/huggingface/hub/models--ResembleAI--chatterbox*; do
  [[ -e "$d" ]] && echo "  $d  ($(groesse "$d"))"
done
[[ -d "$HOME/.pkuseg" ]] && echo "  $HOME/.pkuseg  ($(groesse "$HOME/.pkuseg"))"
[[ -n "$ABL" ]] && echo "  Starter-Apps in $ABL (Eingang/Ausgang/Stimmen bleiben)"
frage "Fortfahren?" || { echo "Abgebrochen."; exit 0; }

rm -rf "$INST" "$HOME"/.cache/huggingface/hub/models--ResembleAI--chatterbox* "$HOME/.pkuseg"
if [[ -n "$ABL" ]]; then rm -rf "$ABL/Chatterbox Oberfläche.app" "$ABL/Chatterbox Ordner vertonen.app"; fi
# Hugging Face legt Gewichte als Blobs ab; verwaiste Blobs ohne Verweis aufräumen
HUB="$HOME/.cache/huggingface/hub"
if [[ -d "$HUB" ]] && ! ls -d "$HUB"/models--* >/dev/null 2>&1; then rm -rf "$HUB"; fi

if command -v uv >/dev/null || [[ -x "$HOME/.local/bin/uv" ]]; then
  if frage "Auch uv und dessen Python-Fassungen entfernen (nur wenn sonst nicht genutzt)?"; then
    rm -rf "$HOME/.local/bin/uv" "$HOME/.local/bin/uvx" "$HOME/.local/share/uv" "$HOME/.cache/uv"
  fi
fi
echo "Fertig."
