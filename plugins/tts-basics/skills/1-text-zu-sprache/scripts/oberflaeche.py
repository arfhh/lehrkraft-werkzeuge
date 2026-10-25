#!/usr/bin/env python3
"""oberflaeche.py – lokale Weboberfläche (Gradio) für Chatterbox Multilingual.

© 2026 A. Spielhoff – lizenziert unter CC BY 4.0
Chatterbox: Resemble AI, MIT-Lizenz.

Start:  python oberflaeche.py [--stimmen ORDNER] [--ausgang ORDNER]
Öffnet http://127.0.0.1:7860 im Browser. Läuft nur lokal, nichts geht ins Netz.
"""
import argparse
import re
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import torch
import gradio as gr

import text_zu_mp3 as tzm

STANDARD = "Standardstimme"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stimmen", type=Path, default=Path.cwd() / "Stimmen",
                   help="Ordner mit WAV-Sprachproben")
    p.add_argument("--ausgang", type=Path, default=Path.cwd() / "Ausgang",
                   help="Ordner für gespeicherte MP3s")
    p.add_argument("--modell", default="v3", choices=["v2", "v3"])
    p.add_argument("--port", type=int, default=7860)
    args = p.parse_args()
    args.stimmen.mkdir(parents=True, exist_ok=True)
    args.ausgang.mkdir(parents=True, exist_ok=True)

    tzm.FFMPEG = tzm.ffmpeg_pfad() or ""
    if not tzm.FFMPEG:
        raise SystemExit("ffmpeg fehlt – pip install imageio-ffmpeg")

    geraet = tzm.geraet_waehlen("auto")
    print(f"Lade Chatterbox Multilingual {args.modell} auf '{geraet}' …")
    modell = tzm.modell_laden(geraet, args.modell)
    standard_conds = modell.conds  # prepare_conditionals ersetzt das Objekt, ändert es nicht
    zustand = {"stimme": STANDARD}

    def stimmen_liste():
        return [STANDARD] + sorted(f.name for f in args.stimmen.glob("*.wav"))

    def erzeugen(text, stimme, ausdruck, cfg, temperatur, seed, autor, name):
        text = (text or "").strip()
        if not text:
            raise gr.Error("Bitte einen Text eingeben.")
        if stimme != zustand["stimme"] or stimme != STANDARD:
            if stimme == STANDARD:
                modell.conds = standard_conds
            else:
                modell.prepare_conditionals(str(args.stimmen / stimme), exaggeration=ausdruck)
            zustand["stimme"] = stimme
        a = SimpleNamespace(sprache="de", ausdruck=ausdruck, cfg=cfg,
                            temperatur=temperatur, pause=0.35, autor=autor,
                            lizenz="CC BY 4.0", bitrate="96k", modell=args.modell)
        torch.manual_seed(int(seed))
        wav = tzm.vertonen(modell, text, a)
        stamm = re.sub(r"[^\wäöüÄÖÜß -]", "", (name or "").strip()) or \
            datetime.now().strftime("Audio_%Y-%m-%d_%H-%M-%S")
        ziel = args.ausgang / f"{stamm}.mp3"
        tzm.als_mp3(wav, modell.sr, ziel, stamm.replace("_", " "), a)
        return str(ziel), f"Gespeichert: {ziel}"

    with gr.Blocks(title="Chatterbox – Text zu Sprache") as app:
        gr.Markdown("## Chatterbox – Text zu Sprache (lokal)\n"
                    "Text eingeben, Stimme wählen, **Erzeugen**. Die MP3 landet im "
                    f"Ordner `{args.ausgang}`. Eigene Stimmen: WAV-Datei in `{args.stimmen}` legen.")
        text = gr.Textbox(label="Sprechtext", lines=10,
                          placeholder="Zahlen, Abkürzungen und Einheiten ausschreiben …")
        with gr.Row():
            stimme = gr.Dropdown(stimmen_liste(), value=STANDARD, label="Stimme")
            neu = gr.Button("Stimmenliste neu laden", size="sm")
            name = gr.Textbox(label="Dateiname (ohne .mp3, optional)")
        with gr.Row():
            ausdruck = gr.Slider(0.2, 1.0, 0.65, step=0.05, label="Ausdruck (0.3 ruhig – 0.7 lebhaft)")
            cfg = gr.Slider(0.0, 1.0, 0.5, step=0.05, label="CFG (niedriger = langsamer)")
        with gr.Accordion("Weitere Einstellungen", open=False):
            temperatur = gr.Slider(0.3, 1.2, 0.95, step=0.05, label="Temperatur")
            seed = gr.Number(42, label="Seed (andere Zahl = andere Sprechvariante)", precision=0)
            autor = gr.Textbox(label="Autor (MP3-Metadaten)")
        los = gr.Button("Erzeugen", variant="primary")
        audio = gr.Audio(label="Ergebnis", type="filepath")
        info = gr.Markdown()
        neu.click(lambda: gr.Dropdown(choices=stimmen_liste()), outputs=stimme)
        los.click(erzeugen, [text, stimme, ausdruck, cfg, temperatur, seed, autor, name],
                  [audio, info])

    app.launch(server_name="127.0.0.1", server_port=args.port, inbrowser=True,
               allowed_paths=[str(args.ausgang.resolve())], show_error=True)


if __name__ == "__main__":
    main()
