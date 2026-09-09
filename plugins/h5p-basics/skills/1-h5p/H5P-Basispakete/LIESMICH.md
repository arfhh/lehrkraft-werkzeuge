# H5P-Basispakete (Werkzeugkasten)

Schlanke `.h5p`-Pakete, die die vollständigen H5P-Programmbibliotheken
(JavaScript/CSS) enthalten, aber nur einen generischen Platzhalter-Inhalt.
Damit lässt sich eine fertige `.h5p`-Datei bauen, ohne den ZUM-Editor zu
öffnen: entpacken, `content/content.json` durch den eigenen Inhalt ersetzen,
neu packen.

Dieser Ordner ist projektunabhängig. Er wird von mehreren KI-Projekten
genutzt und ist das Original — Arbeitskopien anderswo werden von hier
erneuert, nicht umgekehrt.

## Herkunft und Lizenz

Die Pakete stammen aus dem Toolkit der Barcamp-Session „KI und ZUM-Apps",
OERcamp 2026, Bildungszentrum Erkner, 28.–30.08.2026.

**Lizenz: CC BY 4.0.** Bei Weitergabe sind zu nennen:

- ZUM Deutsch Lernen (alle Pakete)
- Ralf Klötzke (`ZUM_H5P_Basis_BranchingScenario.h5p`)

Die enthaltenen H5P-Bibliotheken sind überwiegend MIT-lizenziert; Ausnahmen
sind MaterialDesignIcons (GPL3) und TextUtilities (Public Domain).

## Inventar

| Datei | Hauptbibliothek |
|---|---|
| ZUM_H5P_Basis_BranchingScenario.h5p | H5P.BranchingScenario 1.8 (+ BranchingQuestion 1.0) |
| ZUM_H5P_Basis_CoursePresentation.h5p | H5P.CoursePresentation 1.25 |
| ZUM_H5P_Basis_DialogCards.h5p | H5P.Dialogcards 1.9 |
| ZUM_H5P_Basis_ImageHotspots.h5p | H5P.ImageHotspots 1.10 |
| ZUM_H5P_Basis_ImageHotspotsZUM.h5p | H5P.ImageHotspotsZUM 1.9 |
| ZUM_H5P_Basis_InteractiveVideo.h5p | H5P.InteractiveVideo 1.26 |
| ZUM_H5P_Basis_Matching.h5p | H5P.Matching 1.0 |
| ZUM_H5P_Basis_SortParagraphs.h5p | H5P.SortParagraphs 0.11 |
| ZUM_H5P_Basis_Summary.h5p | H5P.Summary 1.10 |
| ZUM_H5P_Basis_Verstaendnischeck.h5p | H5P.QuestionSet 1.20 — enthält Blanks 1.14, DragQuestion 1.14, DragText 1.10, Essay 1.5, MarkTheWords 1.11, MultiChoice 1.16, MultiMediaChoice 0.3, TrueFalse 1.8 |

**Interactive Book fehlt.** Es muss aus einem frischen ZUM-Apps-Export nach
„Anleitung B" der Toolkit-Anleitung selbst aufbereitet werden.

## Zwei Fallstricke

**Nie zwei Basispakete zusammenkopieren.** Die Bibliotheksversionen
widersprechen sich teilweise: MultiChoice 1.14 gegen 1.16, Question 1.4 gegen
1.5, TrueFalse 1.6 gegen 1.8.

**Beim Packen keine Verzeichniseinträge ins ZIP**, sonst lehnt ZUM-Apps die
Datei mit „File 'content/' not allowed" ab:

```
zip -r -X -D Mein_Inhalt.h5p . -x '*.DS_Store'
```

Alle zehn Pakete wurden am 01.09.2026 geprüft: unbeschädigt, keine
Verzeichniseinträge, `content/content.json` vorhanden.
