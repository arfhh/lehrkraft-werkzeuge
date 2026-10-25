#!/usr/bin/env python3
"""text_zu_mp3.py – Textdateien lokal mit Chatterbox Multilingual vertonen.

© 2026 A. Spielhoff – lizenziert unter CC BY 4.0
Chatterbox: Resemble AI, MIT-Lizenz.

Beispiele:
  python text_zu_mp3.py text.txt
  python text_zu_mp3.py texte/ --stimme meine_stimme.wav --autor "Vorname Nachname"
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Nicht unterstützte Operationen auf Apple Silicon automatisch auf die CPU umleiten
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import torch  # noqa: E402
import torchaudio  # noqa: E402

MAX_ZEICHEN = 250  # längere Stücke führen eher zu verschluckten Wörtern


def geraet_waehlen(wunsch: str) -> str:
    if wunsch != "auto":
        return wunsch
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def modell_laden(geraet: str, version: str):
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS

    try:
        return ChatterboxMultilingualTTS.from_pretrained(device=geraet, t3_model=version)
    except TypeError:
        print(f"Hinweis: Installierte Chatterbox-Fassung kennt keine Modellwahl – "
              f"es läuft v2 statt {version}. Für v3 aus GitHub installieren (installation.md).")
        return ChatterboxMultilingualTTS.from_pretrained(device=geraet)


def in_stuecke(absatz: str) -> list[str]:
    """Absatz in Sätze teilen und Sätze zu Stücken bis MAX_ZEICHEN bündeln."""
    saetze = re.split(r"(?<=[.!?])\s+", absatz.strip())
    stuecke, aktuell = [], ""
    for satz in saetze:
        if not satz:
            continue
        # Überlange Einzelsätze an Kommas teilen
        teile = [satz] if len(satz) <= MAX_ZEICHEN else re.split(r"(?<=,)\s+", satz)
        for teil in teile:
            if aktuell and len(aktuell) + 1 + len(teil) > MAX_ZEICHEN:
                stuecke.append(aktuell)
                aktuell = teil
            else:
                aktuell = f"{aktuell} {teil}".strip()
    if aktuell:
        stuecke.append(aktuell)
    return stuecke


def stille(sekunden: float, sr: int) -> torch.Tensor:
    return torch.zeros(1, int(sekunden * sr))


def vertonen(modell, text: str, a) -> torch.Tensor:
    absaetze = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    teile = []
    for i, absatz in enumerate(absaetze):
        for stueck in in_stuecke(" ".join(absatz.split())):
            print(f"   · {stueck[:70]}{'…' if len(stueck) > 70 else ''}")
            wav = modell.generate(
                stueck,
                language_id=a.sprache,
                exaggeration=a.ausdruck,
                cfg_weight=a.cfg,
                temperature=a.temperatur,
            )
            teile.append(wav.detach().cpu().reshape(1, -1))
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()  # verhindert schleichendes Langsamerwerden bei langen Läufen
            teile.append(stille(a.pause, modell.sr))
        if i < len(absaetze) - 1:
            teile.append(stille(a.pause * 2, modell.sr))
    return torch.cat(teile, dim=1)


def als_mp3(wav: torch.Tensor, sr: int, ziel: Path, titel: str, a) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        roh = Path(tmp) / "roh.wav"
        torchaudio.save(str(roh), wav, sr)
        meta = {
            "title": titel,
            "artist": a.autor or "",
            "copyright": a.lizenz,
            "comment": f"Gesprochen von einer KI-Stimme (Chatterbox Multilingual {a.modell}). "
                       f"Lizenz: {a.lizenz}",
        }
        befehl = [FFMPEG, "-y", "-loglevel", "error", "-i", str(roh),
                  "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                  "-ac", "1", "-ar", "44100", "-codec:a", "libmp3lame", "-b:a", a.bitrate,
                  "-id3v2_version", "3"]
        for k, v in meta.items():
            if v:
                befehl += ["-metadata", f"{k}={v}"]
        subprocess.run(befehl + [str(ziel)], check=True)


def ffmpeg_pfad() -> str | None:
    """ffmpeg im PATH, sonst die Fassung aus dem pip-Paket imageio-ffmpeg."""
    gefunden = shutil.which("ffmpeg")
    if gefunden:
        return gefunden
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


FFMPEG = "ffmpeg"


def main() -> None:
    global FFMPEG
    p = argparse.ArgumentParser(description="Textdateien lokal mit Chatterbox vertonen.")
    p.add_argument("eingabe", type=Path, help=".txt-Datei oder Ordner mit .txt-Dateien")
    p.add_argument("--ausgabe", type=Path, help="Zielordner (Standard: neben der Eingabe)")
    p.add_argument("--stimme", type=Path, help="WAV-Sprachprobe der zu klonenden Stimme")
    p.add_argument("--sprache", default="de")
    p.add_argument("--modell", default="v3", choices=["v2", "v3"])
    p.add_argument("--geraet", default="auto", choices=["auto", "mps", "cuda", "cpu"])
    p.add_argument("--ausdruck", type=float, default=0.65)
    p.add_argument("--cfg", type=float, default=0.5)
    p.add_argument("--temperatur", type=float, default=0.95)
    p.add_argument("--pause", type=float, default=0.35, help="Sekunden zwischen Stücken")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--autor", default="")
    p.add_argument("--lizenz", default="CC BY 4.0")
    p.add_argument("--bitrate", default="96k")
    a = p.parse_args()

    FFMPEG = ffmpeg_pfad() or ""
    if not FFMPEG:
        sys.exit("ffmpeg fehlt – siehe installation.md (pip install imageio-ffmpeg genügt).")
    if not a.eingabe.exists():
        sys.exit(f"Nicht gefunden: {a.eingabe}")
    dateien = sorted(a.eingabe.glob("*.txt")) if a.eingabe.is_dir() else [a.eingabe]
    if not dateien:
        sys.exit("Keine .txt-Dateien gefunden.")
    zielordner = a.ausgabe or (a.eingabe if a.eingabe.is_dir() else a.eingabe.parent)
    zielordner.mkdir(parents=True, exist_ok=True)

    geraet = geraet_waehlen(a.geraet)
    print(f"Lade Chatterbox Multilingual {a.modell} auf '{geraet}' …")
    modell = modell_laden(geraet, a.modell)
    if a.stimme:
        if not a.stimme.exists():
            sys.exit(f"Sprachprobe nicht gefunden: {a.stimme}")
        modell.prepare_conditionals(str(a.stimme), exaggeration=a.ausdruck)

    for datei in dateien:
        text = datei.read_text(encoding="utf-8").strip()
        if not text:
            print(f"Übersprungen (leer): {datei.name}")
            continue
        print(f"▶ {datei.name}")
        torch.manual_seed(a.seed)
        wav = vertonen(modell, text, a)
        ziel = zielordner / f"{datei.stem}.mp3"
        als_mp3(wav, modell.sr, ziel, datei.stem.replace("_", " "), a)
        print(f"✔ {ziel}  ({wav.shape[1] / modell.sr:.1f} s)")


if __name__ == "__main__":
    main()
