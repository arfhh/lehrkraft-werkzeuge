# Inhalt und interaktive Aufgaben

## 1. Inhaltlich prüfen, nicht nur sprachlich

Ein H5P wird selten nur wegen Tippfehlern überarbeitet. Claude soll das
Material **fachlich und didaktisch** mitlesen und aktiv auf Schwächen
hinweisen — nicht erst auf Nachfrage:

- **Fachliche Ungenauigkeiten**, auch wenn der Satz grammatisch stimmt.
  Reales Beispiel: „Die waagerechten Spalten …" — waagerecht ist nie eine
  Spalte, der Text widerspricht sich selbst.
- **Copy-Paste-Reste.** Der häufigste stille Fehler: ein Folientitel oder
  Bildtitel, der noch zum Vorgängerelement gehört und nicht zum Inhalt der
  Folie. Titel gegen Inhalt prüfen, nicht für bare Münze nehmen.
- **Fehler in Grafiken.** Text, der in ein Bild eingebrannt ist, lässt sich
  nicht automatisch korrigieren — trotzdem melden, statt stillschweigend
  zu übergehen. Der Mensch entscheidet, ob die Grafik neu gebaut wird.
- **Links stichprobenartig prüfen.** Bei Zweifeln bitten, selbst
  draufzuklicken.

**Zu kompliziert formulierte Texte aktiv erkennen**, auch wenn inhaltlich
alles stimmt. Lernmaterial soll so einfach sein, dass sich auch schwächere
Lernende den Inhalt selbständig erarbeiten können. Also nicht nur auf
Fehler reagieren, sondern grundsätzlich mitdenken, ob eine Formulierung
knapper und klarer ginge.

**Form ja, Inhalt nein.** Ohne Rückfrage korrigiert werden: Rechtschreibung
und Grammatik, doppelte Leerzeichen, unsichtbare Sonderzeichen,
LaTeX→Unicode, kaputte oder fehlende Metadaten sowie Bildtitel und
Alternativtexte (siehe `medien.md`). Vorgelegt statt geändert werden:
Fachtexte, Aufgabenstellungen, didaktische Umformulierungen, gelöschte
Elemente — und jeder sichtbare Folientext, zu dem eine Vorlese-Aufnahme
existiert, weil die Aufnahme sonst nicht mehr zum Text passt. Bei diesen
Änderungen Original und Vorschlag nebeneinander zeigen und entscheiden
lassen.

Praktisch bewährt: Formulierungsvorschläge **direkt in eine Entwurfsdatei
einbauen** (unter eigenem Namen, neben der noch gültigen Version), statt
sie einzeln im Chat abnicken zu lassen. Der Mensch sieht die Änderung dann
gleich im Layout-Kontext und kann dort reagieren — das spart eine ganze
Runde. Der Entwurf ist die Freigabe-Station; erst danach folgen aufwendige
Schritte wie Audio-Aufnahmen.

## 2. `H5P.Blanks` — Synonyme ergänzen

Bei Lückentexten muss die eingetippte Antwort **exakt** treffen.
Abweichungen in Numerus, Wortwahl oder Formulierung werden sonst als falsch
gewertet — Lernende bekommen einen Fehler angezeigt, nur weil sie es anders
ausgedrückt haben. Das ist der häufigste Frustpunkt in H5P-Lückentexten.

Die Syntax steht direkt im Aufgabentext, nicht in einem eigenen JSON-Feld:

- Eine Lücke steht zwischen zwei `*`.
- Mehrere akzeptierte Antworten werden mit `/` getrennt.
- Ein Tipp (wird auf Wunsch eingeblendet, zählt **nicht** als Antwort)
  folgt nach einem `:` innerhalb derselben Lücke.

```
Vor dem Start muss die Anleitung
*gelesen/vollständig gelesen/durchgelesen/studiert* werden.

Das Ergebnis wird in einer
*Tabelle/Übersicht: hat Zeilen und Spalten* festgehalten.
```

Vorgehen bei jeder Blanks-Aufgabe: pro Lücke überlegen, was jemand
plausibel eintippen könnte (Synonyme, Singular/Plural, gängige
Umgangssprache), und ergänzen, **sofern es fachlich richtig ist**. Nicht
beliebig viele Alternativen anhängen — nur solche, die tatsächlich als
richtig durchgehen sollen.

Ausnahmen: rein numerische Lücken und eindeutige Eigennamen oder Symbole
brauchen keine Synonyme. Einen Tipp nur ergänzen, wenn die Lücke sonst
kaum zu erraten ist, nicht bei jeder.

Das ist Autofix-artig (direkt ergänzen), aber **sichtbar machen**: kurz
auflisten, was ergänzt wurde, damit jemand fachlich gegenprüfen kann.

## 3. `H5P.DragQuestion` — gezieltes Feedback bei typischen Fehlern

Bei Drag-and-Drop-Aufgaben lässt sich pro Ablagezone ein Hinweis
hinterlegen, der nach dem Überprüfen erscheint:

```
dropZones[i].tipsAndFeedback.feedbackOnIncorrect
```

Dieses Feld existiert seit jeher, wird aber fast nie genutzt — dabei ist es
der Unterschied zwischen „falsch" und „falsch, und zwar deshalb".

**Nicht flächendeckend befüllen.** Bei vielen falschen Zuordnungen
gleichzeitig entsteht sonst eine Textflut, die mehr verwirrt als hilft.
Stattdessen: pro Aufgabe überlegen, was die **drei bis fünf typischen
Fehler** sind, und nur an je einer repräsentativen Stelle einen Hinweis
setzen. Der Rest der Zonen bleibt bei der Standardmeldung.

**Kein `feedbackOnCorrect`** — bei richtigen Zuordnungen soll nichts
stehen.

Beispielhafte Fehlerarten, die einen Hinweis verdienen: eine
Reihenfolge-Regel missachtet; eine Obergrenze überschritten (Hinweis nur am
*ersten* überzähligen Platz); eine Größe verwechselt, die sich gar nicht
ändern kann; ein Sonderfall, der von der allgemeinen Regel abweicht und
einen eigenen Text braucht.

## 4. Freie Schreibaufgaben

Wo Lernende selbst einen Text schreiben sollen
(`H5P.FreeTextQuestion`, `H5P.OpenEndedQuestion`, `H5P.ExportableTextArea`
oder eine entsprechende Aufgabenformulierung), die Aufgabenstellung um den
Hinweis ergänzen, dass die Antwort **in eigenen Worten** verfasst werden
soll. Das verhindert reines Kopieren aus dem Material.

Erkennungsmerkmal ist nicht nur der Operator, sondern die **Größe des
Antwortfelds**: ein mehrzeiliges Feld für zusammenhängenden Text braucht
den Hinweis, ein kleines Feld für Kurzantworten oder Aufzählungen nicht.

Die Formulierung variieren, nicht immer dieselbe: „… in eigenen Worten.",
„Nutze dabei deine eigenen Worte.", „Formuliere deine Antwort in eigenen
Worten." — je nach Satzbau der Aufgabe.

## 5. Neue Aufgaben ergänzen

H5P kann weit mehr als Blanks, DragText, DragQuestion und MultiChoice —
lohnend ist, den Katalog auszuschöpfen. Zwei Orte kommen dafür in Frage:

- **eine neue Folie innerhalb der Course Presentation** — dort ist die
  Auswahl an Content-Typen begrenzt;
- **ein neues Kapitel im Interactive Book** — dort steht deutlich mehr zur
  Verfügung.

**Vor dem Vorschlagen eines neuen Content-Typs immer technisch
gegenprüfen**, ob die nötige Bibliothek im Zielpaket überhaupt enthalten
ist (`library_versions()`). Fehlt sie, muss sie aus einer anderen Datei
oder aus dem H5P Hub importiert werden — sonst erscheint beim Öffnen
„Der ausgewählte Inhaltstyp 'H5P.X' ist auf dieser Seite nicht
installiert".

## 6. Titel und Überschriften

Sprachliche Konventionen für Überschriften (etwa: immer mit bestimmtem
Artikel, keine Trailing-Doppelpunkte, einheitliche Groß-/Kleinschreibung)
lohnen sich — aber sie müssen **einmal festgelegt und dann konsequent
durchgezogen** werden, über alle Folientitel, Kapitel-/TOC-Titel
(`metadata.title` der Chapter) und den Buchtitel in `h5p.json` hinweg.

Zwei praktische Hinweise:

- **Trailing-Doppelpunkte in Folientiteln entfernen.** Titel werden gern
  als Abschnittsüberschrift oder Dateiname weiterverwendet, und `:` ist auf
  macOS im Dateinamen nicht zulässig.
- **Ändert sich ein Titel, verschieben sich relativ dazu positionierte
  Elemente** (Audio-Buttons, Icons). Titeländerung und Neupositionierung
  sind ein Arbeitsschritt, nicht zwei — siehe `layout.md`.

## 7. Versionierung sichtbar machen

Wer ein H5P mehrfach überarbeitet, braucht einen Weg zu erkennen, welche
Fassung vorliegt. Bewährt hat sich ein Duo:

- ein **Datum im Dateinamen** in einem festen Format;
- ein **Versionstext auf der Titel-/Cover-Folie** (ein
  `H5P.AdvancedText` mit z. B. `Version: 24.08.26`).

**Beide werden bei jeder Änderung aktualisiert — auch bei der kleinsten.**
Das ist die Regel, die am zuverlässigsten vergessen wird: ein
Bibliotheksversions-Fix, eine Metadaten-Korrektur, ein einzelner Tippfehler
gelten genauso als Bearbeitung wie ein voller Durchgang. Und es wird
regelmäßig nur *eine* der beiden Stellen aktualisiert. Deshalb: der Abgleich
beider Stellen gehört fest vor jeden `pack()`-Aufruf, der eine bestehende
Datei ersetzt (siehe `checkliste.md`).
