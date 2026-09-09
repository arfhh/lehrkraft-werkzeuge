# Layout: Folienaufbau und Konsistenz

Dieser Teil betrifft vor allem `H5P.CoursePresentation` — den Content-Typ,
in dem Elemente frei auf einer Folie positioniert werden — und damit auch
`H5P.InteractiveBook`, dessen Kapitel meist Course Presentations enthalten.

## Das Koordinatensystem

Jedes Element auf einer Folie hat `x`, `y`, `width`, `height` — **alles in
Prozent der Foliengröße**, nicht in Pixeln:

```json
{
  "x": 1.57, "y": 3.10, "width": 94.0, "height": 10.8,
  "action": {
    "library": "H5P.AdvancedText 1.1",
    "params": { "text": "<p>…</p>" },
    "metadata": { "contentType": "Text", "license": "U", "title": "…" }
  }
}
```

Aufbau der Struktur:

```
content.json
└── chapters[]                     (nur bei H5P.InteractiveBook)
    └── params.content[]           (H5P.Column)
        └── content.params.presentation.slides[]
            └── elements[]         die frei positionierten Elemente
```

Die **Reihenfolge in `elements[]` ist die z-Ordnung**: das erste Element
liegt hinten, das letzte vorn. Ein vollflächiges Hintergrundbild gehört
deshalb an den Anfang der Liste.

Bei einer eigenständigen Course Presentation ohne Buch entfällt die
Kapitel-Ebene: `content.json` → `presentation.slides[]`.

## Folien-Hintergründe als Bildelement

Ein verbreitetes, robustes Muster für ein einheitliches Aussehen: jede
Inhalts-Folie bekommt als **unterstes** Element ein `H5P.Image` in voller
Foliengröße (`x=0, y=0, width≈100, height=100`) mit `decorative: true` und
einem festen `metadata.title` wie `"Hintergrund"`. Die eigentlichen
Inhalte liegen darüber.

Vorteile: das Design steckt in ein paar austauschbaren PNGs statt in
hunderten Einzeleinstellungen, und ein Skript kann jederzeit prüfen, ob
eine Folie dem Standard folgt.

Dabei drei Fallen:

- **Hintergrundbilder brauchen dieselben vollständigen Metadaten wie jedes
  andere Bild** (Autor, Quelle, Lizenz — siehe `medien.md`). Sie werden
  reihenweise vergessen, weil sie „nur Deko" sind; der Server prüft das
  trotzdem. Realer Fund: alle sechs Hintergründe eines Buchs hatten gar
  kein `metadata`-Objekt.
- **Die Prüfung „hat diese Folie schon einen Hintergrund?" muss das ganze
  `elements[]`-Array durchsuchen, nicht nur `elements[0]`.** Ein
  Diagnoseskript, das nur den ersten Eintrag prüfte, meldete reihenweise
  falsche Treffer, weil der Hintergrund je nach Bearbeitungshistorie an
  anderer Stelle im Array stand. Richtig: nach einem Element mit
  `decorative == true` **und** dem vereinbarten `metadata.title` suchen —
  die Position im Array ist dafür egal.
- **Fehlt der Hintergrund ganz**, ist das ein eigener Fund und nicht nur
  eine Positionsfrage. Ältere Folien haben oft Text direkt auf Weiß.

Vollbild-Video-Folien und Titel-/Cover-Folien bekommen bewusst keinen
solchen Hintergrund — er wäre unsichtbar bzw. stört das Cover-Design.

### Kasten-Ränder eines Hintergrundbilds ermitteln

Wenn das Hintergrundbild sichtbare Kästen zeichnet, in die der Text passen
soll, lassen sich deren Ränder per Pixel-Scan bestimmen, statt sie zu
schätzen: mit PIL eine horizontale bzw. vertikale Linie durch die Bildmitte
scannen und die Übergänge zur Rahmenfarbe suchen. Ergebnis in Prozent
umrechnen (`x_prozent = x_pixel / bildbreite * 100`) und die Breite
vorhandener Textelemente dagegen prüfen.

**Reicht ein Text über den Kastenrand hinaus: nicht die Schrift
verkleinern, sondern den Kasten verbreitern.**

## Layout-Konsistenz-Check

Ein Buch wirkt fertig oder unfertig vor allem daran, ob Titel und Inhalte
auf allen Folien an derselben Stelle sitzen. Abweichungen von ein, zwei
Prozentpunkten fallen einzeln nicht auf, summieren sich aber. Dieser Check
gehört in **jede** Bearbeitung, nicht nur wenn etwas auffällt:

1. **Referenzfolie suchen.** Eine Folie, deren Titel-Position sauber sitzt
   (im Zweifel die zuletzt neu gebaute), und deren `x/y/width/height` als
   Referenz für alle Folien **desselben Hintergrund-/Folientyps** nehmen.
   Verschiedene Folientypen haben eigene, jeweils in sich einheitliche
   Werte — nie die Werte des einen Typs pauschal auf einen anderen
   übertragen.
2. **Alle Folien desselben Typs auf die Referenzwerte normalisieren**, auch
   ohne sichtbare Auffälligkeit. *Ausnahme:* eine geschlossene Gruppe
   gleichartiger Folien mit eigener, untereinander konsistenter Position
   kann ein bewusstes Sub-Template sein — vor dem Normalisieren nachfragen.
3. **Kein Element darf über die Kasten-Ränder des Hintergrunds hinausragen**
   oder in einen Titelbalken hineinragen. Beim Verkleinern eines zu großen
   Bildes **immer das Seitenverhältnis beibehalten**:
   ```
   neue_breite_% = neue_höhe_% × (bild_px_breite / bild_px_höhe)
                              × (folien_px_höhe / folien_px_breite)
   ```
   Breite und Höhe unabhängig zu schätzen verzerrt das Bild — ein Fehler,
   der beim schnellen Anpassen immer wieder passiert.
4. **Nach alten Layout-Resten suchen**, die nicht mehr zum aktuellen Design
   passen. Zwei wiederkehrende Muster:
   - **Verwaiste `H5P.Shape`-Rechtecke**, die farblich einem Balken des
     Hintergrundbilds ähneln — Reste aus einer Zeit, als das Design noch
     aus Shapes gebaut war. Shape und Hintergrundbild ergeben zusammen
     einen doppelten, verwaschenen Balken. Löschen, Titel danach auf die
     Referenzposition setzen.
   - **Alte, groß eingebundene `H5P.Audio`-Elemente mit
     `playerMode: "full"`** (voller Player mit Zeitleiste, meist unten auf
     der Folie), wo das aktuelle Design kleine `minimalistic`-Buttons
     vorsieht. Ersatzlos löschen, nicht auf `minimalistic` umstellen.
     *Ausnahme:* ein erkennbar eigenständiger Audioinhalt (ein Podcast, ein
     Interview — eigener inhaltlicher Titel, kein Vorlesetext) bleibt
     unangetastet. Unterscheidungsmerkmal: ein Layout-Rest liest denselben
     Text vor, der als kleiner Button woanders schon existiert.
   - Nach jedem Löschen eines Elements prüfen, ob die zugehörige
     Mediendatei dadurch verwaist ist (`find_orphan_media()`).
5. **Visuell gegenprüfen, bevor gepackt wird.** Ohne echten H5P-Renderer
   hilft ein Mock-up mit PIL: Hintergrund einfügen, Bilder an ihren
   Prozentkoordinaten platzieren, Text- und Widget-Elemente als
   beschriftete Rahmen zeichnen. Das findet Überlappungen und Überstände
   vor dem Packen statt danach im Feedback.

## Titel-Elemente

Der Folientitel ist meist ein `H5P.AdvancedText` am oberen Rand. Ein
einheitliches HTML-Muster erspart viel Nacharbeit, zum Beispiel:

```html
<p><span style="font-size:1.5em"><strong>Titeltext</strong></span></p>
```

Zwei Details, die regelmäßig Ärger machen:

- **Alte `<hr />`-Reste im Titel-HTML.** Frühere Titelformen hatten oft
  `</p>\n\n<hr>\n<p>&nbsp;</p>` angehängt — das erscheint als sichtbare
  horizontale Linie unter der Überschrift. Beim Anfassen **jedes**
  Titel-Elements aktiv nach `<hr` suchen und entfernen, auch wenn nur die
  Position geändert wird und nicht der Text.
- **Titel-Erkennung ist nicht trivial.** Auf derselben Folie können
  mehrere Textblöcke dasselbe Muster (`<strong>` + große Schrift) nutzen —
  etwa ein Aufgabentext oder ein Download-Link. Beim automatischen Erkennen
  zusätzlich nach der `y`-Position filtern: der echte Titel sitzt am
  weitesten oben (typischerweise `y < 10`). Sonst wird der falsche Block
  umformatiert — in einem realen Durchlauf führte das zu einer
  Elementposition von 223 % Folienbreite, weit außerhalb der Folie.

## Elemente relativ zum Titel positionieren

Soll ein Element direkt neben dem Titeltext sitzen (typisch: ein kleiner
Audio-Button zum Vorlesen), hängt seine `x`-Position von der Titellänge ab.
Eine lineare Formel funktioniert gut:

```
x = basis + faktor × zeichenanzahl_des_titels
```

`basis` und `faktor` **werden an der konkreten Datei kalibriert**, nicht
aus einer anderen übernommen: zwei oder drei von Hand korrekt gesetzte
Buttons mit unterschiedlicher Titellänge auslesen und die Gerade daraus
bestimmen. An einer konkreten Datei kalibriert ergab sich
`x = 5,62 + 1,45 × n` (n = Zeichenanzahl des Titels) bei `width = 4,71` und
`height = 9,32` — an neun Buttons mit Titellängen zwischen 10 und 50
Zeichen bestätigt. Diese Zahlen hängen an Schriftgröße, Foliengröße und
Bibliotheksversion; **anderswo werden sie neu kalibriert**, nicht
übernommen.

Vier Regeln dazu:

- **Bei sehr langen Titeln überschätzt die lineare Formel** (der Titel
  bricht dann um). Dort mit reduziertem Wert schätzen und ausdrücklich zur
  Sichtkontrolle ankündigen.
- **Höhe und `y` müssen innerhalb einer Datei bei allen gleichartigen
  Buttons identisch sein.** Existieren schon von Hand korrigierte
  Elemente, deren Werte als verbindliche Referenz übernehmen — nicht raten
  und nicht aus einer anderen Datei kopieren.
- **Ändert sich ein Titel, muss der Button im selben Arbeitsschritt neu
  positioniert werden.** Dieser Zusammenhang wird notorisch vergessen:
  „nur ein Wort im Titel geändert" verschiebt die korrekte Button-Position
  um mehrere Prozentpunkte. Zweimal in Folge in einem realen Projekt
  passiert.
- **Titelnahe von inhaltlichen Elementen unterscheiden.** Ein Audio mitten
  im Fließtext (`y` deutlich größer) folgt dieser Logik nicht und bleibt
  unangetastet. Faustregel: `y < 5` → titelnah, `y >= 5` → inhaltlich.

## Interaktive Widgets nicht in der Breite verändern

`H5P.Blanks`, `H5P.MultiChoice`, `H5P.DragQuestion` und Verwandte **nicht**
in Breite oder Position anpassen, um sie in ein Spaltenlayout zu zwingen —
das riskiert Interaktivität und Auswertung. Passt die vorhandene Breite
nicht zu einem mehrspaltigen Hintergrund, lieber eine einteilige Variante
über die volle Breite nehmen, als eine Spaltenaufteilung zu erraten.

Inline-CSS (`margin`, `padding`) auf `<p>`-Elementen wird vom
AdvancedText-Editor beim Speichern verworfen — darauf lässt sich kein
Layout aufbauen.

## Mehrspaltige Bild-Text-Listen

Wenn eine Folie eine Liste aus „Beschriftung + Bild" zeigt (typisch für
Lösungs- oder Übersichtsfolien), hat sich bewährt:

- **Jede Zeile bekommt ihre eigene, unabhängig positionierte Textbox**,
  deren `y` exakt dem `y` des zugehörigen Bildes entspricht. Ein
  gemeinsamer Fließtextblock ist unbrauchbar: sein Zeilenumbruch macht die
  vertikale Position der einzelnen Zeilen unvorhersehbar.
- **Feste Boxbreite und feste x-Position** für alle Zeilen einer Spalte,
  Text linksbündig. Der naheliegende Weg — Boxbreite aus der Textlänge
  schätzen und jede Zeile einzeln zentrieren — wurde in einem realen
  Projekt über vier Korrekturrunden hinweg verworfen: die geschätzte
  Zeichenbreite stimmt nie für alle Labels, und das Ergebnis wirkt
  „getreppt" statt ruhig.
- **Nicht mehr als etwa sechs Zeilen pro Spalte**, danach eine zweite
  Spalte oder eine zweite Folie beginnen.
