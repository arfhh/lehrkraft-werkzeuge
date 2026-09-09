"""
h5p_check.py — Ueberblick und Abschluss-Selbstcheck fuer eine .h5p-Datei.

Arbeitet direkt auf der gepackten Datei (entpackt sich intern nach /tmp)
oder auf einem bereits entpackten Arbeitsverzeichnis.

    python3 h5p_check.py --inspect DATEI.h5p    Struktur: Kapitel, Folien,
                                                Elemente, Bibliotheken
    python3 h5p_check.py --media   DATEI.h5p    Medien-Inventar mit
                                                Metadaten-Luecken
    python3 h5p_check.py --all     DATEI.h5p    kompletter Selbstcheck

Exit-Code 1, wenn --all Probleme findet — so laesst es sich in einem
Skript verketten.

Die Punkte, die Urteilsvermoegen brauchen (passt der Bildtitel zum Bild?
sind die Alt-Texte aussagekraeftig? sitzen die Titel einheitlich?), kann
kein Skript abnehmen — dafuer die Checkliste in
references/checkliste.md durchgehen.
"""
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from h5p_pack import (  # noqa: E402
    count_invisible, dir_entries, file_list, find_empty_chapters, find_latex,
    find_incomplete_media_metadata, find_media, find_missing_alt,
    find_orphan_media, iter_slides, library_versions, root_entries,
)
from check_library_versions import find_mismatches  # noqa: E402


def _open(pfad):
    """Gibt (arbeitsverzeichnis, tempdir_oder_None) zurueck."""
    p = Path(pfad)
    if p.is_dir():
        return p, None
    tmp = tempfile.mkdtemp(prefix="h5pcheck-")
    with zipfile.ZipFile(p) as zf:
        zf.extractall(tmp)
    return Path(tmp), tmp


def _content(work):
    return json.loads((work / "content" / "content.json").read_text("utf-8"))


# --------------------------------------------------------------------------


def inspect(pfad):
    work, tmp = _open(pfad)
    try:
        content = _content(work)
        h5p = json.loads((work / "h5p.json").read_text("utf-8"))

        print(f"== {Path(pfad).name}")
        print(f"Titel:         {h5p.get('title')}")
        print(f"Hauptbibliothek: {h5p.get('mainLibrary')}")
        print()

        print("-- Bibliotheken im Paket")
        for lib, ver in sorted(library_versions(work).items()):
            print(f"   {lib:<34} {ver}")
        print()

        print("-- Folien")
        aktuelles_kapitel = None
        for kapitel, idx, slide in iter_slides(content):
            if kapitel != aktuelles_kapitel:
                print(f"\n   Kapitel: {kapitel}")
                aktuelles_kapitel = kapitel
            elemente = slide.get("elements") or []
            kurz = []
            for el in elemente:
                lib = ((el.get("action") or {}).get("library") or "?").split()[0]
                kurz.append(lib.replace("H5P.", ""))
            print(f"     Folie {idx:>2}: {len(elemente):>2} Elemente  "
                  f"{', '.join(kurz) if kurz else '(leer)'}")

        leer = find_empty_chapters(content)
        if leer:
            print("\n   !! LEERE KAPITEL:", leer)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def media(pfad):
    work, tmp = _open(pfad)
    try:
        content = _content(work)
        alle = find_media(content)
        print(f"== Medien in {Path(pfad).name}: {len(alle)}")
        for m in alle:
            fehlt = []
            if not m["authors"]:
                fehlt.append("authors")
            if not m["source"]:
                fehlt.append("source")
            marker = "  << FEHLT: " + ", ".join(fehlt) if fehlt else ""
            print(f"   {m['library'].split()[0]:<26} "
                  f"{(m['title'] or '(ohne Titel)')[:42]:<44}"
                  f"{m['license'] or '-':<10}{marker}")
        print()
        ohne_alt = find_missing_alt(content)
        if ohne_alt:
            print(f"-- {len(ohne_alt)} Bild(er) ohne brauchbaren Alternativtext:")
            for titel, alt in ohne_alt:
                print(f"   {(titel or '(ohne Titel)')[:50]:<52} alt={alt!r}")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def check_all(pfad):
    work, tmp = _open(pfad)
    ist_zip = tmp is not None
    probleme, hinweise = [], []
    try:
        content = _content(work)

        # --- automatisch pruefbar
        unvollstaendig = find_incomplete_media_metadata(content)
        if unvollstaendig:
            probleme.append(
                f"{len(unvollstaendig)} Medienelement(e) ohne authors/source "
                f"(z. B. {unvollstaendig[0][1]!r} -> {unvollstaendig[0][2]})")

        leer = find_empty_chapters(content)
        if leer:
            probleme.append(f"leere Kapitel: {leer}")

        latex = find_latex(content)
        if latex:
            probleme.append(f"{len(latex)} LaTeX-Rest(e), z. B. {latex[0][:60]!r}")

        unsichtbar = count_invisible(content)
        if unsichtbar:
            probleme.append(f"{unsichtbar} unsichtbare Sonderzeichen")

        verwaist = find_orphan_media(work)
        if verwaist:
            probleme.append(f"{len(verwaist)} verwaiste Mediendatei(en): "
                            f"{verwaist[:3]}")

        ohne_alt = find_missing_alt(content)
        if ohne_alt:
            hinweise.append(f"{len(ohne_alt)} Bild(er) ohne brauchbaren "
                            "Alternativtext (nicht als deko markiert)")

        if ist_zip:
            mism = find_mismatches(pfad)
            if mism:
                probleme.append(f"Bibliotheksversions-Mismatch: {mism[:3]}")
            dirs = dir_entries(pfad)
            if dirs:
                probleme.append(
                    f"{len(dirs)} Verzeichnis-Eintraege im ZIP — der Server "
                    "lehnt den Upload ab (mit `zip -rXq -D` packen)")
            nicht_ascii = [f for f in file_list(pfad) if not f.isascii()]
            if nicht_ascii:
                probleme.append(f"Nicht-ASCII-Dateinamen: {nicht_ascii[:3]}")
            extra = [n for n in root_entries(pfad)
                     if n not in ("h5p.json", "mimetype")]
            if extra:
                probleme.append(f"Fremddateien auf der Wurzelebene: {extra[:5]}")
            with zipfile.ZipFile(pfad) as zf:
                bad = zf.testzip()
            if bad:
                probleme.append(f"defekter Zip-Eintrag: {bad}")
            groesse = Path(pfad).stat().st_size / 1024 / 1024
            hinweise.append(f"Dateigroesse {groesse:.1f} MB — plausibel fuer "
                            "diese Variante?")
        else:
            hinweise.append("entpacktes Verzeichnis geprueft — Zip-Checks "
                            "(Integritaet, Verzeichnis-Eintraege, Dateinamen) "
                            "erst nach dem Packen moeglich")

        # --- Ausgabe
        print(f"== Selbstcheck {Path(pfad).name}")
        if probleme:
            print(f"\n{len(probleme)} PROBLEM(E):")
            for p in probleme:
                print("   !!", p)
        else:
            print("\nKeine automatisch pruefbaren Probleme gefunden.")

        if hinweise:
            print("\nHinweise:")
            for h in hinweise:
                print("   -", h)

        print("\nNoch von Hand zu pruefen (references/checkliste.md):")
        for punkt in (
            "Bildtitel und Alt-Texte passen zum tatsaechlichen Bildinhalt",
            "Quellenangaben aktuell, echte Inhaltslinks unveraendert",
            "Synonyme bei jeder H5P.Blanks-Luecke ergaenzt",
            "Layout-Konsistenz ueber alle Folien, keine alten Layout-Reste",
            "versteckte Inhalte geprueft (InteractiveVideo-Interaktionen)",
            "Dateiname UND Cover-Versionstext auf das aktuelle Datum gebracht",
            "Rechtschreibung auch in h5p.json (title, extraTitle)",
            "Sichtpruefung: Mock-up angesehen oder im Editor gegengelesen",
        ):
            print("   [ ]", punkt)

        return 1 if probleme else 0
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    modus, pfad = argv[1], argv[2]
    if modus == "--inspect":
        inspect(pfad)
        return 0
    if modus == "--media":
        media(pfad)
        return 0
    if modus == "--all":
        return check_all(pfad)
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
