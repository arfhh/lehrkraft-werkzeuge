"""H5P-Dateien sicher entpacken, bearbeiten und packen.

WARUM DIESES SKRIPT EXISTIERT
-----------------------------
`zip -r` legt für jeden Ordner einen eigenen 0-Byte-Eintrag im Archiv an
(z. B. "content/", "H5P.Blanks-1.14/"). Der H5P-Server-Validator prüft
jeden Zip-Eintrag gegen eine Dateiendungs-Whitelist; ein Verzeichnis-
Eintrag hat keine Endung -> Fehler `File "content/" not allowed` und der
komplette Upload schlägt fehl. Lokal (z. B. in Lumi) lässt sich so eine
Datei trotzdem einwandfrei öffnen — der Fehler fällt erst beim Hochladen
auf.

Deshalb packt dieses Skript ausschließlich mit `zip -rXq -D` und VERWEIGERT
das Schreiben, wenn die Verifikation fehlschlägt. Es entsteht nie eine
halb-kaputte Ausgabedatei.

BENUTZUNG ALS SKRIPT
    python3 h5p_pack.py unpack "alt.h5p" arbeitsordner/
    python3 h5p_pack.py pack arbeitsordner/ "neu.h5p" --reference "alt.h5p"
    python3 h5p_pack.py verify "neu.h5p" --reference "alt.h5p"

BENUTZUNG ALS MODUL
    from h5p_pack import unpack, pack, verify, load_content, save_content

Getestet mit Python 3.9+; benötigt nur die Standardbibliothek und das
Kommandozeilenwerkzeug `zip`.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

MEDIA_LIBS = ("H5P.Image", "H5P.Audio", "H5P.Video", "H5P.InteractiveVideo")
MEDIA_DIRS = ("images", "audios", "videos", "files")


class H5PPackError(RuntimeError):
    pass


# --------------------------------------------------------------------------
# Entpacken / Packen
# --------------------------------------------------------------------------


def unpack(h5p_path, dest_dir, clean: bool = True) -> Path:
    """Entpackt eine .h5p-Datei nach dest_dir und gibt den Pfad zurück."""
    h5p_path, dest = Path(h5p_path), Path(dest_dir)
    if clean and dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(h5p_path) as zf:
        zf.extractall(dest)
    return dest


def pack(src_dir, out_path, reference=None, allow_new_files: bool = True) -> Path:
    """Packt src_dir zu einer .h5p und verifiziert das Ergebnis.

    reference: die Originaldatei. Ist sie angegeben, wird die Dateiliste
    verglichen — fehlende Dateien sind immer ein Fehler, zusätzliche nur
    dann erlaubt, wenn allow_new_files=True.

    reference=None verwenden, wenn bewusst Dateien entfernt/ersetzt wurden
    oder wenn die Datei zwischendurch in einem H5P-Editor gespeichert
    wurde (Editoren benennen Medien um und heben Bibliotheksversionen an —
    harmlose Abweichungen, die der Vergleich sonst als Fehler meldet).

    Bei jedem Problem wird die erzeugte Datei wieder gelöscht und eine
    H5PPackError geworfen.

    Hinweis: auf FUSE-Mounts, Netzlaufwerken und manchen Cloud-Sync-Ordnern
    scheitert `zip` mit "Operation not permitted". Dann das Arbeits-
    verzeichnis nach /tmp kopieren, dort packen und die fertige Datei
    zurückkopieren.
    """
    src, out = Path(src_dir), Path(out_path)
    if not (src / "h5p.json").is_file():
        raise H5PPackError(f"{src} sieht nicht nach einem entpackten H5P aus "
                           "(h5p.json fehlt)")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    # -D unterdrückt Verzeichnis-Einträge, -X lässt Extra-Attribute weg.
    res = subprocess.run(
        ["zip", "-rXq", "-D", str(out.resolve()), "."],
        cwd=src, capture_output=True, text=True,
    )
    if res.returncode != 0:
        if out.exists():
            out.unlink()
        raise H5PPackError(
            f"zip fehlgeschlagen (Exit {res.returncode}): {res.stderr.strip()}\n"
            "Bei 'Operation not permitted': Arbeitsverzeichnis nach /tmp "
            "kopieren und dort packen."
        )

    try:
        verify(out, reference=reference, allow_new_files=allow_new_files)
    except H5PPackError:
        try:
            out.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return out


# --------------------------------------------------------------------------
# Verifikation
# --------------------------------------------------------------------------


def file_list(h5p_path) -> list:
    """Sortierte Liste aller echten Dateien (ohne Verzeichnis-Einträge)."""
    with zipfile.ZipFile(h5p_path) as zf:
        return sorted(i.filename for i in zf.infolist() if not i.is_dir())


def dir_entries(h5p_path) -> list:
    """Alle Verzeichnis-Einträge — muss für ein gültiges H5P leer sein."""
    with zipfile.ZipFile(h5p_path) as zf:
        return sorted(i.filename for i in zf.infolist() if i.is_dir())


def root_entries(h5p_path) -> list:
    """Dateien auf der Wurzelebene des Archivs.

    Ein normales H5P hat dort nur h5p.json (und ggf. mimetype). Alles
    andere ist versehentlich mitgepackter Müll — typischerweise eine
    Rest-.h5p oder ein Debug-Bild aus dem Arbeitsverzeichnis.
    """
    return sorted(n for n in file_list(h5p_path) if "/" not in n)


def verify(h5p_path, reference=None, allow_new_files: bool = True,
           verbose: bool = True) -> dict:
    """Prüft eine .h5p auf Upload-Tauglichkeit. Wirft bei Problemen."""
    h5p_path = Path(h5p_path)
    report = {"file": str(h5p_path)}
    problems = []

    # 1) ZIP-Integrität. Einzelne Einträge können defekt sein, ohne dass
    #    ein Player das merkt.
    with zipfile.ZipFile(h5p_path) as zf:
        bad = zf.testzip()
    if bad:
        problems.append(f"defekter Eintrag im Archiv: {bad}")

    # 2) keine Verzeichnis-Einträge (die Kernregel)
    dirs = dir_entries(h5p_path)
    report["dir_entries"] = len(dirs)
    if dirs:
        problems.append(
            f"{len(dirs)} Verzeichnis-Eintraege im ZIP (z. B. {dirs[:3]}) — "
            "der H5P-Server lehnt den Upload ab. Mit `zip -rXq -D` packen."
        )

    # 3) keine Nicht-ASCII-Dateinamen
    files = file_list(h5p_path)
    non_ascii = [f for f in files if not f.isascii()]
    report["non_ascii_files"] = non_ascii
    if non_ascii:
        problems.append(
            f"{len(non_ascii)} Datei(en) mit Nicht-ASCII-Namen im ZIP (z. B. "
            f"{non_ascii[:3]}) — manche Player scheitern daran mit einem "
            "kryptischen ENOENT-Fehler, weil die Kodierung des Zip-"
            "Eintragsnamens nicht zuverlaessig zum in content.json "
            "referenzierten Pfad passt."
        )

    # 4) Pflichtdateien
    report["n_files"] = len(files)
    for must in ("h5p.json", "content/content.json"):
        if must not in files:
            problems.append(f"Pflichtdatei fehlt: {must}")

    # 5) Wurzelebene sauber
    extra_root = [n for n in root_entries(h5p_path)
                  if n not in ("h5p.json", "mimetype")]
    report["extra_root_files"] = extra_root
    if extra_root:
        problems.append(
            f"unerwartete Datei(en) auf der Wurzelebene: {extra_root[:5]} — "
            "vermutlich Reste im Arbeitsverzeichnis, die mitgepackt wurden."
        )

    # 6) JSON lesbar
    if not problems:
        with zipfile.ZipFile(h5p_path) as zf:
            for name in ("h5p.json", "content/content.json"):
                try:
                    json.loads(zf.read(name).decode("utf-8"))
                except Exception as exc:  # noqa: BLE001
                    problems.append(f"{name} ist kein gueltiges JSON: {exc}")

    # 7) Vergleich mit dem Original
    if reference is not None:
        ref_files = set(file_list(reference))
        now = set(files)
        missing = sorted(ref_files - now)
        added = sorted(now - ref_files)
        report["missing"] = missing
        report["added"] = added
        if missing:
            problems.append(
                f"{len(missing)} Datei(en) fehlen gegenueber dem Original: "
                f"{missing[:5]}"
            )
        if added and not allow_new_files:
            problems.append(f"unerwartete neue Dateien: {added[:5]}")

    if problems:
        raise H5PPackError(
            "H5P-Verifikation fehlgeschlagen fuer " + str(h5p_path) + ":\n  - "
            + "\n  - ".join(problems)
        )

    if verbose:
        size_mb = Path(h5p_path).stat().st_size / 1024 / 1024
        print(f"OK  {h5p_path.name}")
        print(f"    {report['n_files']} Dateien, {size_mb:.1f} MB, "
              "0 Verzeichnis-Eintraege, Integritaet fehlerfrei")
        if reference is not None and report.get("added"):
            print(f"    zusaetzlich gegenueber Original: "
                  f"{len(report['added'])} neue Datei(en)")
    return report


# --------------------------------------------------------------------------
# Zugriff auf die Inhalte
# --------------------------------------------------------------------------


def load_content(work_dir) -> dict:
    return json.loads((Path(work_dir) / "content" / "content.json").read_text("utf-8"))


def save_content(work_dir, data) -> None:
    path = Path(work_dir) / "content" / "content.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def load_h5p_json(work_dir) -> dict:
    return json.loads((Path(work_dir) / "h5p.json").read_text("utf-8"))


def save_h5p_json(work_dir, data) -> None:
    path = Path(work_dir) / "h5p.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------
# Struktur-Walk: Textkorrekturen
# --------------------------------------------------------------------------


def _walk_strings(obj, fn):
    """Ruft fn(text) -> (neuer_text, treffer) fuer jeden String auf.

    Wichtig: Aufgabentexte liegen bei manchen Content-Typen (H5P.Blanks)
    direkt als String-Element einer Liste, nicht nur als Dict-Wert —
    beide Faelle werden abgedeckt.
    """
    total = 0
    if isinstance(obj, dict):
        for key, val in obj.items():
            if isinstance(val, str):
                new, n = fn(val)
                if n:
                    obj[key] = new
                    total += n
            else:
                total += _walk_strings(val, fn)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            if isinstance(val, str):
                new, n = fn(val)
                if n:
                    obj[i] = new
                    total += n
            else:
                total += _walk_strings(val, fn)
    return total


def replace_text(obj, old: str, new: str) -> int:
    """Ersetzt old durch new in ALLEN Strings einer JSON-Struktur.

    Gibt die Trefferzahl zurueck. Arbeitet in-place.
    """
    return _walk_strings(obj, lambda t: (t.replace(old, new), t.count(old)))


INVISIBLE_CHARS = [
    "\u00ad",  # weiches Trennzeichen
    "\u2060",  # Wortverbinder
    "\u200b",  # Zero Width Space
    "\u200c",  # Zero Width Non-Joiner
    "\u200d",  # Zero Width Joiner
    "\ufeff",  # BOM / Zero Width No-Break Space
]


def strip_invisible(obj) -> int:
    """Entfernt unsichtbare Sonderzeichen (Autofix, nie nachfragen).

    Typische Copy-Paste-Reste. Achtung: auf der GEPARSTEN Struktur
    arbeiten, nicht auf dem Rohtext der Datei (dort stehen sie nur als
    \\u00ad-Escape).
    """
    return sum(replace_text(obj, ch, "") for ch in INVISIBLE_CHARS)


def count_invisible(obj) -> int:
    """Wie strip_invisible(), aber ohne zu aendern (nur zaehlen)."""
    found = 0

    def scan(o):
        nonlocal found
        if isinstance(o, dict):
            values = o.values()
        elif isinstance(o, list):
            values = o
        else:
            return
        for v in values:
            if isinstance(v, str):
                found += sum(v.count(ch) for ch in INVISIBLE_CHARS)
            else:
                scan(v)

    scan(obj)
    return found


_SUB = str.maketrans("0123456789+-()", "₀₁₂₃₄₅₆₇₈₉₊₋₍₎")
_SUP = str.maketrans("0123456789+-()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾")
_FRAC_RE = re.compile(r"\\frac\{([^{}]*)\}\{([^{}]*)\}")
_SUB_RE = re.compile(r"_\{([^{}]*)\}")
_SUP_RE = re.compile(r"\^\{([^{}]*)\}")
_DELIM_RE = re.compile(r"\\[()]")
LATEX_HINT_RE = re.compile(r"\\\(|\\frac|_\{|\^\{")


def latex_to_unicode(obj) -> int:
    """Ersetzt LaTeX-Notation durch Unicode-Zeichen.

    `\\(H_{3}O^{+}\\)` wird zu `H₃O⁺`, `\\(\\frac{g}{mol}\\)` zu `g/mol`.
    Grund: reine Unicode-Darstellung rendert in H5P stabiler als
    eingebettetes LaTeX/MathType.

    Nur Ziffern, +, -, ( und ) werden hoch-/tiefgestellt — bei anderen
    Zeichen (Buchstaben-Exponenten o. ae.) bleibt der LaTeX-Ausdruck
    stehen und muss von Hand geprueft werden. Gibt die Trefferzahl
    zurueck.
    """

    def convert(text):
        count = 0

        def frac_sub(m):
            nonlocal count
            count += 1
            return f"{m.group(1)}/{m.group(2)}"

        new = _FRAC_RE.sub(frac_sub, text)

        def sub_sub(m):
            nonlocal count
            inner = m.group(1)
            if not all(c in "0123456789+-()" for c in inner):
                return m.group(0)
            count += 1
            return inner.translate(_SUB)

        new = _SUB_RE.sub(sub_sub, new)

        def sup_sub(m):
            nonlocal count
            inner = m.group(1)
            if not all(c in "0123456789+-()" for c in inner):
                return m.group(0)
            count += 1
            return inner.translate(_SUP)

        new = _SUP_RE.sub(sup_sub, new)
        new, n = _DELIM_RE.subn("", new)
        count += n
        return new, count

    return _walk_strings(obj, convert)


def find_latex(obj) -> list:
    """Findet Strings, in denen noch LaTeX-Notation steckt."""
    hits = []

    def scan(o):
        if isinstance(o, dict):
            values = o.values()
        elif isinstance(o, list):
            values = o
        else:
            return
        for v in values:
            if isinstance(v, str):
                if LATEX_HINT_RE.search(v):
                    hits.append(v[:120])
            else:
                scan(v)

    scan(obj)
    return hits


def replace_source_exact(obj, varianten, neu: str) -> int:
    """Ersetzt Quellen-URLs NUR bei exaktem Treffer am Schluessel `source`.

    varianten: Liste bekannter Schreibweisen der alten Quelle
    (http/https, mit/ohne www., mit/ohne Trailing-Slash).

    NIE einen String-Replace ueber den kompletten JSON-Rohtext laufen
    lassen: dieselbe Zeichenkette ist oft Praefix echter Inhaltslinks
    (".../uploads/material.pdf"), die dabei zerstoert wuerden.

    Erfasst jedes Dict mit einem `source`-Schluessel, unabhaengig von
    `library` — Quellen stecken auch in Widget-eigenen copyright-Objekten
    und in Kapitel-Metadaten, nicht nur in H5P.Image.
    """
    varianten = set(varianten)
    count = 0

    def scan(o):
        nonlocal count
        if isinstance(o, dict):
            src = o.get("source")
            if isinstance(src, str) and src.strip() in varianten:
                o["source"] = neu
                count += 1
            for v in o.values():
                scan(v)
        elif isinstance(o, list):
            for v in o:
                scan(v)

    scan(obj)
    return count


def url_varianten(domain: str) -> list:
    """Baut alle ueblichen Schreibweisen einer Domain als Quellenangabe.

    url_varianten("beispiel.de") -> http/https x mit/ohne www. x
    mit/ohne Trailing-Slash = 8 Varianten.
    """
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    ohne_www = domain[4:] if domain.startswith("www.") else domain
    out = []
    for schema in ("http://", "https://"):
        for host in (ohne_www, "www." + ohne_www):
            out.append(schema + host)
            out.append(schema + host + "/")
    return out


# --------------------------------------------------------------------------
# Medien
# --------------------------------------------------------------------------


def find_media(content) -> list:
    """Alle Medienelemente als Liste von Dicts.

    Rueckgabe je Element: {library, title, license, authors, source,
    paths}. Laeuft rekursiv, erfasst also auch tief verschachtelte
    Unterinhalte.
    """
    out = []

    def paths_of(params):
        found = []
        for key in ("file", "files", "sources"):
            val = params.get(key)
            if isinstance(val, dict) and val.get("path"):
                found.append(val["path"])
            elif isinstance(val, list):
                found += [v["path"] for v in val
                          if isinstance(v, dict) and v.get("path")]
        iv = params.get("interactiveVideo")
        if isinstance(iv, dict):
            files = (iv.get("video") or {}).get("files") or []
            found += [f["path"] for f in files
                      if isinstance(f, dict) and f.get("path")]
        return found

    def scan(o):
        if isinstance(o, dict):
            lib = o.get("library")
            if isinstance(lib, str) and lib.startswith(MEDIA_LIBS):
                meta = o.get("metadata") or {}
                params = o.get("params") or {}
                out.append({
                    "library": lib,
                    "title": meta.get("title"),
                    "license": meta.get("license"),
                    "authors": meta.get("authors") or [],
                    "source": meta.get("source"),
                    "alt": params.get("alt"),
                    "decorative": params.get("decorative"),
                    "paths": paths_of(params),
                })
            for v in o.values():
                scan(v)
        elif isinstance(o, list):
            for v in o:
                scan(v)

    scan(content)
    return out


def find_incomplete_media_metadata(content) -> list:
    """Medienelemente ohne Autor oder ohne Quelle.

    Der haeufigste Grund fuer abgelehnte Uploads bzw. "Fehlt"-Anzeigen auf
    dem Server. Gilt fuer ALLE Medientypen, auch fuer dekorative
    Hintergrundbilder.

    Rueckgabe: Liste von (library, title, fehlende_felder).
    """
    out = []
    for m in find_media(content):
        fehlt = []
        if not m["authors"]:
            fehlt.append("authors")
        if not m["source"]:
            fehlt.append("source")
        if fehlt:
            out.append((m["library"], m["title"], fehlt))
    return out


def find_missing_alt(content) -> list:
    """Bilder ohne brauchbaren Alternativtext (und nicht als deko markiert).

    Ein Alt-Text von unter ~3 Zeichen oder identisch mit einem generischen
    Titel ist praktisch nutzlos fuer Screenreader.
    """
    out = []
    for m in find_media(content):
        if not m["library"].startswith("H5P.Image"):
            continue
        if m.get("decorative"):
            continue
        alt = (m.get("alt") or "").strip()
        if len(alt) < 3:
            out.append((m["title"], alt))
    return out


def find_orphan_media(work_dir) -> list:
    """Mediendateien, auf die im JSON niemand mehr verweist.

    Entstehen beim Loeschen eines Elements oder eines ganzen Kapitels und
    wandern sonst unnoetig mit ins Paket. Vor dem Packen entfernen.
    """
    work = Path(work_dir)
    blob = ""
    for jsonfile in list(work.glob("*.json")) + list((work / "content").rglob("*.json")):
        try:
            blob += jsonfile.read_text("utf-8", errors="ignore")
        except OSError:
            continue
    orphans = []
    for sub in MEDIA_DIRS:
        folder = work / "content" / sub
        if not folder.is_dir():
            continue
        for f in sorted(folder.iterdir()):
            if f.is_file() and f.name not in blob:
                orphans.append(str(f.relative_to(work)))
    return orphans


def image_source_majority(content):
    """Haeufigster `source`-Wert aus den H5P.Image-Metadaten.

    Nuetzlich, um die projektuebliche Quelle einer Datei zu ermitteln,
    bevor fehlende Quellen ergaenzt werden. Nur H5P.Image zaehlt —
    Aufgaben-Widgets haben oft eigene source-Felder mit Weblinks, die
    nichts mit Medien-Copyright zu tun haben.
    """
    from collections import Counter
    found = Counter()
    for m in find_media(content):
        if m["library"].startswith("H5P.Image") and m["source"]:
            found[m["source"]] += 1
    return found.most_common(1)[0][0] if found else None


# --------------------------------------------------------------------------
# Struktur
# --------------------------------------------------------------------------


def library_versions(work_dir) -> dict:
    """Die im Paket TATSAECHLICH enthaltenen Bibliotheksversionen.

    Die Versionen unterscheiden sich von Datei zu Datei. Niemals fest
    verdrahten — sonst verweist der Inhalt auf eine Bibliothek, die im
    Paket gar nicht liegt (Upload-Fehler "Bibliothek H5P.X a.b ist
    ungueltig, sollte c.d sein").
    """
    out = {}
    for entry in Path(work_dir).iterdir():
        if entry.is_dir() and "-" in entry.name:
            machine, _, version = entry.name.rpartition("-")
            if machine.startswith("H5P.") and version[:1].isdigit():
                prev = out.get(machine)
                key = tuple(int(x) for x in version.split(".") if x.isdigit())
                if prev is None or key > tuple(
                    int(x) for x in prev.split(".") if x.isdigit()
                ):
                    out[machine] = version
    return out


def iter_slides(content):
    """Liefert (kapitel_titel, folien_index, folie) fuer alle Folien.

    Funktioniert sowohl fuer H5P.InteractiveBook (Kapitel -> Column ->
    CoursePresentation) als auch fuer eine eigenstaendige
    CoursePresentation.
    """
    def slides_of(obj, kapitel):
        if isinstance(obj, dict):
            pres = obj.get("presentation")
            if isinstance(pres, dict) and isinstance(pres.get("slides"), list):
                for i, slide in enumerate(pres["slides"]):
                    yield (kapitel, i, slide)
                return
            for v in obj.values():
                yield from slides_of(v, kapitel)
        elif isinstance(obj, list):
            for v in obj:
                yield from slides_of(v, kapitel)

    chapters = content.get("chapters")
    if isinstance(chapters, list):
        for ch in chapters:
            titel = ((ch.get("metadata") or {}).get("title")
                     or (ch.get("params") or {}).get("title") or "?")
            yield from slides_of(ch, titel)
    else:
        yield from slides_of(content, "")


def find_empty_chapters(content) -> list:
    """Kapitel ohne Inhalt.

    Bekanntes Editor-Verhalten: beim Speichern wird ein komplettes Kapitel
    (oft das letzte) zu einem leeren Objekt, inklusive Verlust der davon
    referenzierten Bilder. Nach JEDER Bearbeitung durch einen Menschen im
    Editor pruefen.
    """
    out = []
    chapters = content.get("chapters")
    if not isinstance(chapters, list):
        return out
    for i, ch in enumerate(chapters):
        titel = ((ch.get("metadata") or {}).get("title") or "?")
        inhalt = (ch.get("params") or {}).get("content")
        if not inhalt:
            out.append((i, titel))
    return out


def ascii_stem(text: str) -> str:
    """Macht aus beliebigem Text einen ASCII-sicheren Dateinamen-Stamm.

    Dateinamen INNERHALB eines H5P-Pakets duerfen keine Nicht-ASCII-Zeichen
    enthalten (siehe verify(), Punkt 3).
    """
    t = text.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "datei"


def resolve_path(pfad):
    """Findet einen real existierenden Pfad unabhaengig von NFC/NFD.

    macOS speichert Dateinamen NFD-zerlegt, getippte Strings sind NFC —
    ein fest getippter Pfad mit Umlaut kann sonst einen unsichtbaren
    Doppelgaenger-Ordner anlegen statt den echten zu treffen.
    """
    p = Path(pfad)
    if p.exists():
        return p
    if not p.parent.exists():
        return p
    ziel = unicodedata.normalize("NFC", p.name)
    for kandidat in p.parent.iterdir():
        if unicodedata.normalize("NFC", kandidat.name) == ziel:
            return kandidat
    return p


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    ref = None
    if "--reference" in argv:
        ref = argv[argv.index("--reference") + 1]
    args = [a for a in argv[2:] if not a.startswith("--")]
    if ref and ref in args:
        args.remove(ref)

    try:
        if cmd == "unpack":
            print(unpack(args[0], args[1]))
        elif cmd == "pack":
            print(pack(args[0], args[1], reference=ref))
        elif cmd == "verify":
            verify(args[0], reference=ref)
        else:
            print(__doc__)
            return 1
    except (H5PPackError, IndexError) as exc:
        print("FEHLER:", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
