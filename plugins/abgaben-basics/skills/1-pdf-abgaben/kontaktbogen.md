# Handschrift und Zeichnungen: der Kontaktbogen

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0
Begleitdatei zu `1-pdf-abgaben`.

Handschriftlich bearbeitete Abgaben lassen sich nur als Bild beurteilen, und
Bilder sind teuer: eine Seite kostet rund 1900 Token. Fünfzehn Abgaben einzeln
anzusehen kostet knapp 30 000. Das muss nicht sein — der gedruckte Vordruck
macht den Löwenanteil des Bildes aus, und er ist bei allen gleich.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' kontaktbogen.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | Vier Stufen | 28–41 |
> | Messwerte | 42–52 |
> | Der Nebengewinn: Dubletten bei Handschrift | 53–63 |
> | Der Tintenanteil entscheidet nicht, er sortiert nur vor | 64–71 |
> | Grenze | 72–79 |
> | Skript | 80–92 |
> | Geplant: das Blatt-Profil (Arne, 12.09.2026) | 93–125 |
<!-- /INDEX -->

## Vier Stufen

1. **Tintenanteil prüfen.** Bearbeitet oder nicht? Kostet nichts.
2. **Vordruck abziehen.** Der gedruckte Bogen lässt sich als Medianbild über
   alle Abgaben berechnen — ein Leerexemplar wird nicht gebraucht. Übrig
   bleibt nur die Handschrift, schwarz auf weiß.
3. **Auf den Antwortbereich zuschneiden.** Automatisch: alles, worin sich
   mindestens zwei Abgaben vom Vordruck unterscheiden.
4. **Kontaktbogen.** Alle Abgaben desselben Formulars nebeneinander in EIN
   beschriftetes Bild.

Einzeln und in voller Auflösung wird nur dort nachgesehen, wo der Kontaktbogen
etwas offenlässt — zwei bis drei Abgaben statt fünfzehn.

## Messwerte

| Weg | Token |
|---|---|
| 15 Seiten einzeln als Bild | ~28 500 |
| ein Kontaktbogen (etwa 1290×1650) | **~2 800** |
| plus eine Nachprüfung von drei Abgaben in voller Auflösung | +1 300 |

Faktor 7 bis 10 — und **besser lesbar** als das Einzelblatt, weil der gedruckte
Vordruck die Handschrift nicht mehr überlagert.

## Der Nebengewinn: Dubletten bei Handschrift

Für handschriftliche Antworten gibt es keine Textprüfung. Der Kontaktbogen ist
das einzige Verfahren, das hier überhaupt etwas findet: Zwei Abgaben mit
derselben ungewöhnlichen Lösung fallen beim Nebeneinander sofort auf.

Beleg aus einem echten Satz: zwei Abgaben mit identischer, von allen anderen
abweichender Reihenfolge — in deutlich unterschiedlicher Handschrift. Also
zusammengearbeitet, nicht dieselbe Datei geteilt; nach der üblichen Regel kein
bestätigtes Duplikat, aber ein Fund, den sonst niemand gemacht hätte.

## Der Tintenanteil entscheidet nicht, er sortiert nur vor

Eine blass gezeichnete Abgabe kann denselben Tintenanteil haben wie ein leeres
Formular. Belegt: 2,41 Prozent gegen 2,13 Prozent beim Leerexemplar — die
Abgabe war bearbeitet, nur sehr schwach. Der Wert darf deshalb nie allein über
„nicht bearbeitet" entscheiden. Angesehen wird trotzdem; durch den
Kontaktbogen ist das billig genug.

## Grenze

Das trägt, solange alle dasselbe Formular bearbeiten und die Antworten kurz
sind: Zahlen, Zuordnungen, Skizzen. Bei handschriftlichem Fließtext reicht die
Auflösung im Raster nicht — dort einzeln ansehen, aber weiterhin mit
abgezogenem Vordruck und zugeschnitten, lange Kante etwa 1000 Pixel. Das spart
immer noch gut die Hälfte.

## Skript

`scripts/kontaktbogen.py` im gleichnamigen Werkzeug-Ordner.

```
python3 kontaktbogen.py <wurzel> "<dateimuster>" -o bogen.png
        [--bereich x0,x1,y0,y1] [--spalten 3] [--dpi 100] [--breite 430]
```

Ohne `--bereich` wird der Antwortbereich selbst bestimmt. Braucht
`poppler-utils`, `numpy` und `Pillow` — läuft deshalb nicht in jeder Umgebung;
`abgaben_lesen.py` kommt dagegen ohne Python-Pakete aus.

## Geplant: das Blatt-Profil (Arne, 12.09.2026)

Der Kontaktbogen selbst ist klassengebunden — er besteht aus Schülerarbeit.
Alles, was zu seiner Herstellung gebraucht wird, hängt dagegen **nur am
Arbeitsblatt** und ist in jeder Klasse desselben Jahrgangs identisch:

| Wert | heute | mit Profil |
|---|---|---|
| Vordruckbild | je Klasse aus dem Median | einmal gespeichert |
| Zuschnittbereich | je Klasse neu, fällt unterschiedlich aus | fest, klassenübergreifend vergleichbar |
| Tintenanteil des leeren Formulars | braucht eine leere Abgabe in dieser Klasse | fest hinterlegt |
| Vordruckzeilen für den Textabzug | je Klasse aus den Abgaben | einmal gespeichert |
| Kurzantwort ja/nein | je Klasse gemessen | einmal entschieden |

Ablage bei der Lösung des Blattes in `Lösungen/`, zugeordnet über den
beschreibenden Namensteil (dieselbe Regel wie für Lösungen selbst).

**Drei Gewinne über das Token-Sparen hinaus:**
1. Funktioniert auch bei weniger als drei Abgaben desselben Blattes — der
   Medianweg kann das nicht.
2. Gleicher Zuschnitt in allen Klassen, dadurch überhaupt erst vergleichbar.
3. Grundwert für den Tintenanteil steht fest, statt eine nachweislich leere
   Abgabe in der jeweiligen Klasse zu brauchen.

Liegt das **leere Formular** in `Lösungen/`, ersetzt es den Medianweg ganz:
dann ist der echte Vordruck die Quelle statt einer Schätzung daraus.

**Einschränkung:** Der gespeicherte Zuschnitt ist Startwert, nicht Gesetz.
Schreibt eine Klasse über den Rand, wird er für diesen Lauf geweitet. Vor der
Übernahme prüfen, ob alle Antworten im Bereich liegen.

**Umsetzung:** beim ersten handschriftlichen Blatt (z. B. Schalenmodell
zeichnen) an echten Daten bauen, nicht auf Vorrat.
