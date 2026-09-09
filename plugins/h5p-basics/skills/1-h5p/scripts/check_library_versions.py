"""
check_library_versions.py — Bibliotheksversionen in H5P-Paketen pruefen.

HINTERGRUND
-----------
Jedes H5P-Paket bringt seine Bibliotheken selbst mit (Ordner
`H5P.Column-1.18/`). In content.json und h5p.json steht daneben, welche
Version der Inhalt erwartet (`"library": "H5P.Column 1.18"`).

H5P-Editoren heben Versionen beim Speichern gern an (z. B. H5P.Column
1.16 -> 1.18). Wird danach ein aelterer Zwischenstand teilweise
zurueckkopiert — etwa beim Wiederherstellen nach dem bekannten
"Editor leert ein Kapitel"-Fehler —, bleiben einzelne library-Referenzen
auf der alten Version stehen, obwohl das Paket nur noch den neuen Ordner
enthaelt. Lokal funktioniert das oft weiter; Moodle und andere Server
lehnen den Upload ab:

    Bibliothek H5P.Column 1.16 ist ungueltig, sollte 1.18 sein
    Content contains H5P.Xyz a.b, but it should be H5P.Xyz c.d

NUTZUNG
    python3 check_library_versions.py DATEI.h5p [DATEI2.h5p ...]
    python3 check_library_versions.py --outdated ORDNER

ALS MODUL
    from check_library_versions import find_mismatches, find_outdated

ZWEI VERSCHIEDENE PRUEFUNGEN — BEIDE WERDEN GEBRAUCHT
* find_mismatches()  BINNEN-Konsistenz INNERHALB einer Datei: passen die
  library-Referenzen zu den mitgelieferten Bibliotheksordnern?
* find_outdated()    Aktualitaet UEBER MEHRERE Dateien: ist eine Datei
  zwar in sich stimmig, aber gegenueber dem Rest einer Sammlung
  insgesamt veraltet? (Realer Fund: ein Buch komplett auf
  H5P.InteractiveBook 1.7 statt der sonst genutzten 1.11 — intern voellig
  konsistent, deshalb von find_mismatches() grundsaetzlich nicht
  gefunden.)

HINWEIS ZUR FEHLERSUCHE
Ein Bibliotheksordner OHNE aktive Verwendung (weder in
h5p.json/preloadedDependencies noch als library-Referenz in content.json)
kann nie die Ursache eines Validierungsfehlers sein. Zuerst pruefen, ob
die gemeldete Bibliothek ueberhaupt referenziert wird.
"""
import json
import pathlib
import re
import sys
import zipfile

LIB_FOLDER_RE = re.compile(r"^(H5P\.\w+)-(\d+)\.(\d+)$")
LIB_REF_RE = re.compile(r"\"library\"\s*:\s*\"(H5P\.\w+)\s+(\d+\.\d+)\"")


def find_mismatches(h5p_path):
    """Liste von (fundort, bibliothek, gefundene_version, erwartete_version).

    Leere Liste = keine Mismatches. Prueft alle JSON-Dateien im Archiv
    plus h5p.json/preloadedDependencies.
    """
    z = zipfile.ZipFile(h5p_path)
    names = z.namelist()

    bundled = {}
    for n in names:
        m = LIB_FOLDER_RE.match(n.split("/")[0])
        if m:
            bundled[m.group(1)] = f"{m.group(2)}.{m.group(3)}"

    mismatches = []
    for n in names:
        if n.endswith(".json"):
            try:
                data = z.read(n).decode("utf-8", errors="ignore")
            except Exception:
                continue
            for m in LIB_REF_RE.finditer(data):
                lib, ver = m.group(1), m.group(2)
                if lib in bundled and bundled[lib] != ver:
                    mismatches.append((n, lib, ver, bundled[lib]))

    try:
        h5pjson = json.loads(z.read("h5p.json"))
        for dep in h5pjson.get("preloadedDependencies", []):
            lib = dep.get("machineName")
            ver = f"{dep.get('majorVersion')}.{dep.get('minorVersion')}"
            if lib in bundled and bundled[lib] != ver:
                mismatches.append(
                    ("h5p.json/preloadedDependencies", lib, ver, bundled[lib]))
    except Exception:
        pass

    return mismatches


def bundled_libraries(h5p_path):
    """{bibliotheksname: "major.minor"} der im Paket enthaltenen Ordner."""
    bundled = {}
    with zipfile.ZipFile(h5p_path) as z:
        for n in z.namelist():
            m = LIB_FOLDER_RE.match(n.split("/")[0])
            if m:
                bundled[m.group(1)] = f"{m.group(2)}.{m.group(3)}"
    return bundled


def find_outdated(dirpath, pattern="*.h5p"):
    """Aktualitaets-Abgleich ueber alle .h5p eines Ordners.

    Sammelt je Datei die mitgelieferten Bibliotheksordner, bildet pro
    Bibliotheksname das Maximum ueber ALLE Dateien als "kanonische"
    Version und meldet jede Datei, die darunter liegt — auch wenn sie in
    sich voellig konsistent ist.

    Rueckgabe: Liste von (datei, bibliothek, version_dieser_datei,
    kanonische_version). Leere Liste = einheitlicher Stand.
    """
    files = sorted(pathlib.Path(dirpath).rglob(pattern))
    per_file = {}
    for f in files:
        try:
            per_file[f] = bundled_libraries(f)
        except (zipfile.BadZipFile, OSError):
            continue

    canonical = {}
    for libs in per_file.values():
        for lib, ver in libs.items():
            cur = canonical.get(lib)
            if cur is None or _vtuple(ver) > _vtuple(cur):
                canonical[lib] = ver

    outdated = []
    for f, libs in per_file.items():
        for lib, ver in sorted(libs.items()):
            if _vtuple(ver) < _vtuple(canonical[lib]):
                outdated.append((str(f), lib, ver, canonical[lib]))
    return outdated


def _vtuple(ver):
    major, _, minor = ver.partition(".")
    return (int(major), int(minor or 0))


def fix_content_json_version(extracted_dir, lib, old_ver, new_ver):
    """Hebt eine Versionsreferenz in einem entpackten Arbeitsverzeichnis an.

    Ersetzt alle Vorkommen von 'H5P.<lib> <old_ver>' durch
    'H5P.<lib> <new_ver>' in content/content.json und gibt die Anzahl
    zurueck. Danach mit pack(..., reference=None) neu packen — ein
    Referenzvergleich wuerde den Fix sonst als Abweichung werten.

    Bei GROSSEN Versionsspruengen (mehr als eine Minor-Version) vorher das
    Risiko einschaetzen: semantics.json/library.json beider Versionen
    diffen. Kosmetische Unterschiede sind unkritisch; bei echten
    Schema-Aenderungen (neue Pflichtfelder ohne Default) nicht selbst
    migrieren, sondern die Datei einmal im H5P-Editor oeffnen und
    speichern lassen — der migriert Content-Parameter korrekt.
    """
    path = pathlib.Path(extracted_dir) / "content" / "content.json"
    raw = path.read_text(encoding="utf-8")
    old = f"{lib} {old_ver}"
    new = f"{lib} {new_ver}"
    count = raw.count(old)
    if count:
        path.write_text(raw.replace(old, new), encoding="utf-8")
    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--outdated":
        if len(sys.argv) < 3:
            print("Nutzung: check_library_versions.py --outdated ORDNER")
            sys.exit(1)
        rows = find_outdated(sys.argv[2])
        if not rows:
            print(f"{sys.argv[2]}: alle Dateien auf einheitlichem "
                  "Bibliotheksstand")
            sys.exit(0)
        for datei, lib, ver, kanonisch in rows:
            print(f"VERALTET: {datei}: {lib} {ver} (kanonisch {kanonisch})")
        sys.exit(1)

    any_mismatch = False
    for path in sys.argv[1:]:
        mismatches = find_mismatches(path)
        if mismatches:
            any_mismatch = True
            print(f"{path}:")
            for m in mismatches:
                print("   MISMATCH:", m)
        else:
            print(f"{path}: OK")
    sys.exit(1 if any_mismatch else 0)
