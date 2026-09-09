---
name: 1-moodle-xml
description: "Das Dateiformat Moodle-XML für den Import von Fragen in die Fragensammlung eines Moodle-LMS: Dateigerüst, Kategorie-Pseudofrage, XML-Vorlagen aller Fragetypen (multichoice, truefalse, shortanswer, numerical, matching, essay, description, calculated, cloze), der vollständige Cloze-Formenkanon (SA, SAC, NUM, MC, MCS, MR, MRS, MRH, MRHS, MCV, MCVS, MCH, MCHS) mit Grundsyntax und Escaping-Regeln, die kritischen fraction-Bewertungsregeln samt zulässiger Prozentwerte, und der Umbau nativer Fragetypen in Cloze. Rein technisch und projektneutral — sie sagt nicht, WELCHE Fragen gestellt und WIE Schreibvarianten bewertet werden; das geben die Didaktik- und Projekt-Skills vor. IMMER verwenden bei \"Moodle-XML\", \"Cloze\", \"Lückentext\", \"fraction\", \"questiontext\", \"Fragen importieren\", \"Fragensammlung als XML\", \"Importfehler in Moodle\" — auch ohne Skill-Namen."
---

# Moodle-XML

© 2026 A. Spielhoff — lizenziert unter CC BY-SA 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — reines Dateiformat, frei weiterzugeben

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.

## Herkunft und Lizenz

Diese Skill beruht auf zwei Prompts:

- „Moodle_XML_MegaPrompt_v3.0" von bildungssprit.de (CC BY-SA 4.0) —
  allgemeine Fragetypen
- „Moodle Lückentext Cloze" von A. Spielhoff (CC BY-SA 4.0), auf dem
  obigen aufbauend — Cloze-Formenkanon

Wegen der Share-Alike-Klausel dieser Vorlagen steht diese Skill unter
**CC BY-SA 4.0**, abweichend von den übrigen Skills.

**Pflicht:** Wird eine fertige XML-Datei ausgegeben oder geschrieben, steht
am Dateianfang dieser Kommentar:

```xml
<!-- Erstellt mit dem Moodle-Tests-Skill, basierend auf
     Moodle_XML_MegaPrompt_v3.0 (bildungssprit.de, CC BY-SA 4.0) und
     dem Cloze-Formenkanon von A. Spielhoff (CC BY-SA 4.0) -->
```

## Was Moodle-XML ist

Ein Austauschformat für Fragen. Eine Datei enthält beliebig viele Fragen in
einem `<quiz>`-Element; jede Frage ist ein `<question type="…">`-Block. Der
Import-Weg ist in jedem Moodle identisch: *Fragensammlung → Import →
Dateiformat „Moodle-XML" → Datei hochladen → Import starten*.

**Der Import legt immer neue Fragen an.** Er gleicht nicht gegen bestehende
ab — weder über `<name>` noch über `<idnumber>`. Ein zweiter Import einer
korrigierten Datei erzeugt Duplikate statt Aktualisierungen. Für Änderungen
an bereits importierten Fragen ist deshalb ein anderer Weg nötig; welcher,
bestimmt die aufrufende Skill.

Der Fragetext (`<questiontext>`) nimmt beliebiges HTML samt Inline-CSS auf.
Moodles Editor kann beim Speichern HTML filtern — Layout nach dem ersten
Speichern einmal gegenprüfen.

Nicht über XML abbildbar: `calculatedmulti` sowie Drag-and-drop- und
bildmarkierungs-Spezialtypen. Diese direkt in der Moodle-Oberfläche anlegen.

## Allgemeine XML-Regeln (für ALLE Fragetypen)

1. Erste Zeile: `<?xml version="1.0" encoding="UTF-8"?>`.
2. Alle Fragen stehen innerhalb von `<quiz> … </quiz>`.
3. **UTF-8 ohne BOM.**
4. HTML-Inhalte in `<questiontext>`, `<generalfeedback>`,
   `<correctfeedback>`, `<partiallycorrectfeedback>`, `<incorrectfeedback>`
   und `<feedback>` stehen in `<![CDATA[…]]>`.
5. Textfelder mit HTML-Inhalt bekommen `format="html"`.
6. Bei numerischen und formelbasierten Antworten **kein** `format`-Attribut
   am `<answer>`-Tag.
7. Die Kategorie wird als Pseudofrage am Dateianfang gesetzt.
8. Keine ungeschützten `<`, `>`, `&` außerhalb von CDATA.
9. Nur wohlgeformtes XML erzeugen; vor dem Ausliefern prüfen.
10. Immer `<name>` für den Fragetitel, nie `<n>` — häufige Fehlerquelle.
11. Keine unsichtbaren Sonderzeichen (z. B. Soft-Hyphen `\xad`) in
    Antworttexten oder Kategorienamen. Sie verhindern exakte Treffer, obwohl
    der Text beim Lesen normal aussieht.

## KRITISCHE Bewertungsregeln (fraction)

**Häufigster Importfehler:** Moodle meldet „Eine der Antworten sollte mit
100% bewertet werden", wenn die fraction-Werte nicht stimmen.

- **Regel 1 — Einzelantwort** (`<single>true</single>`): genau **eine**
  Antwort `fraction="100"`, alle anderen `fraction="0"`.
- **Regel 2 — Mehrfachantwort** (`<single>false</single>`): Summe aller
  **positiven** fraction-Werte muss exakt **100** ergeben. Falsche Antworten
  negativ. Zulässig sind nur diese Moodle-Werte (und ihre Negative):
  `100, 90, 80, 75, 70, 66.666, 60, 50, 40, 33.333, 30, 25, 20, 16.666,
  14.2857, 12.5, 11.111, 10, 5, 0`.
- **Regel 3 — Wahr/Falsch:** genau eine Antwort `fraction="100"`, die andere
  `fraction="0"`.
- **Regel 4 — Kurzantwort:** mindestens eine Antwort `fraction="100"`.
- **Regel 5 — Numerisch/Berechnet:** Hauptantwort `fraction="100"`.
- **Regel 6 — Essay:** `fraction="0"` (korrekt so, da manuell bewertet).
- **Regel 7 — Zuordnung:** **keine** fraction-Attribute, Moodle bewertet
  automatisch.
- **Regel 8 — Dezimaltrennzeichen immer Punkt, nie Komma:** gilt für alle
  fraction-Attribute und für alle Prozentwerte der Cloze-Syntax (`%0.01%`,
  `33.333`). Ein Komma erkennt der Cloze-Parser nicht als Zahl — die
  Markierung wird wirkungslos, und der Text „%0,01%" kann wörtlich Teil der
  gespeicherten Antwort werden.

**Schnellreferenz Mehrfachantwort:**

| Richtige Antworten | fraction richtig | fraction falsch |
|---|---|---|
| 1 von 4 | 100 | 0 |
| 2 von 4 | 50 | -50 |
| 3 von 4 | 33.333 | -33.333 |
| 2 von 5 | 50 | -50 |
| 3 von 5 | 33.333 | -33.333 |
| 4 von 5 | 25 | -25 |

**Vor jeder XML-Ausgabe prüfen:** Hat jede Frage außer Essay und Zuordnung
mindestens eine Antwort mit `fraction="100"`, bzw. summieren sich die
positiven Werte bei Mehrfachantwort exakt auf 100? Steht in keinem
Zahlenwert ein Komma?

## Wegweiser

| Wenn … | dann lies … |
|---|---|
| eine Frage in einem nativen Fragetyp gebaut oder korrigiert wird (MC, Wahr/Falsch, Kurzantwort, Numerisch, Zuordnung, Essay, Beschreibung, Berechnet), oder die Kategorie-Pseudofrage, `tags` oder `hint` gebraucht werden | `fragetypen.md` |
| eine Cloze-Frage gebaut wird, ein Kürzel des Formenkanons nachzuschlagen ist, Sonderzeichen escaped werden müssen oder das Dateigerüst einer Cloze-Datei gebraucht wird | `cloze.md` |
| eine vorhandene `multichoice`-, `numerical`- oder `matching`-Frage in Cloze überführt werden soll | `umbau.md` |

## Genauigkeit

Cloze-Syntax und fraction-Bewertung sind strikt. `~`, `=`, `#`, `%`, `:`,
`{`, `}`, Leerzeichen in Prozentwerten und die Großschreibung der
Typ-Kürzel (`SHORTANSWER_C`, nicht `Shortanswer_c`) dürfen nicht variiert
oder „verbessert" werden. Im Zweifel die Vorlagen aus den Referenzdateien
wortwörtlich als Gerüst nehmen und nur die Inhalte austauschen.
