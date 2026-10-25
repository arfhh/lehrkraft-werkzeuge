#!/usr/bin/env bash
# Baut zwei Starter-Programme (Doppelklick, kein Terminal nötig) für Chatterbox auf macOS.
# © 2026 A. Spielhoff – lizenziert unter CC BY 4.0
# Aufruf:  bash starter_bauen.sh  INSTALLATIONSORDNER  ABLAGEORDNER
#   INSTALLATIONSORDNER: dort liegen .venv, text_zu_mp3.py, oberflaeche.py
#   ABLAGEORDNER: bekommt die beiden Apps und die Unterordner Eingang/, Ausgang/, Stimmen/
set -euo pipefail
INST="${1:?Installationsordner fehlt}"; ABL="${2:?Ablageordner fehlt}"
[[ -x "$INST/.venv/bin/python" ]] || { echo "Keine Installation in $INST gefunden."; exit 1; }
mkdir -p "$ABL/Eingang" "$ABL/Ausgang" "$ABL/Stimmen"
TMP="$(mktemp -d)"

# AppleScript-Zeichenkette sicher maskieren
as_str() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }
I="$(as_str "$INST")"; A="$(as_str "$ABL")"

cat > "$TMP/oberflaeche.applescript" <<AS
property inst : "$I"
property abl : "$A"
set laeuft to (do shell script "lsof -ti tcp:7860 -sTCP:LISTEN || true")
if laeuft is not "" then
	set w to button returned of (display dialog "Die Chatterbox-Oberfläche läuft bereits." buttons {"Beenden", "Im Browser öffnen"} default button 2 with title "Chatterbox")
	if w is "Beenden" then
		do shell script "kill " & laeuft
		display notification "Oberfläche beendet." with title "Chatterbox"
	else
		open location "http://127.0.0.1:7860"
	end if
else
	do shell script "cd " & quoted form of inst & " && HF_HUB_OFFLINE=1 PATH=" & quoted form of (inst & "/.venv/bin") & ":\$PATH nohup .venv/bin/python oberflaeche.py --stimmen " & quoted form of (abl & "/Stimmen") & " --ausgang " & quoted form of (abl & "/Ausgang") & " > oberflaeche.log 2>&1 &"
	display notification "Modell wird geladen – der Browser öffnet sich gleich. Zum Beenden das Programm erneut öffnen." with title "Chatterbox"
end if
AS

cat > "$TMP/ordner.applescript" <<AS
property inst : "$I"
property abl : "$A"
set wavs to paragraphs of (do shell script "cd " & quoted form of (abl & "/Stimmen") & " && ls *.wav 2>/dev/null || true")
set liste to {"Standardstimme"}
repeat with w in wavs
	if w as text is not "" then set end of liste to (w as text)
end repeat
set n to (do shell script "ls " & quoted form of (abl & "/Eingang") & " | grep -c '\\\\.txt\$' || true")
if n is "0" then
	display dialog "Im Ordner Eingang liegen keine .txt-Dateien." buttons {"OK"} with title "Chatterbox"
	return
end if
set wahl to choose from list liste with prompt (n & " Textdatei(en) in Eingang. Welche Stimme?") default items {"Standardstimme"} with title "Chatterbox"
if wahl is false then return
set stimme to ""
if item 1 of wahl is not "Standardstimme" then set stimme to " --stimme " & quoted form of (abl & "/Stimmen/" & item 1 of wahl)
display notification "Vertonung läuft …" with title "Chatterbox"
try
	do shell script "cd " & quoted form of inst & " && HF_HUB_OFFLINE=1 PATH=" & quoted form of (inst & "/.venv/bin") & ":\$PATH .venv/bin/python text_zu_mp3.py " & quoted form of (abl & "/Eingang") & " --ausgabe " & quoted form of (abl & "/Ausgang") & stimme & " > ordner_vertonen.log 2>&1"
	display notification "Fertig." with title "Chatterbox"
	do shell script "open " & quoted form of (abl & "/Ausgang")
on error
	display dialog "Fehler – Details in " & inst & "/ordner_vertonen.log" buttons {"OK"} with title "Chatterbox" with icon stop
end try
AS

osacompile -o "$ABL/Chatterbox Oberfläche.app" "$TMP/oberflaeche.applescript"
osacompile -o "$ABL/Chatterbox Ordner vertonen.app" "$TMP/ordner.applescript"
rm -rf "$TMP"
echo "Starter liegen in $ABL"
