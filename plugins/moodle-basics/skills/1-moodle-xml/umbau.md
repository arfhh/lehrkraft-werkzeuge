# Native Fragetypen als Cloze umbauen

Begleitdatei zu `1-moodle-xml`.


**Grundregel.** Sobald eine Frage vom Typ `multichoice`, `numerical` oder
`matching` in ein eigenes HTML-Layout eingebettet werden soll, wird sie
**als Cloze neu aufgebaut** statt im nativen Typ zu bleiben.

Grund: Bei allen drei nativen Typen rendert Moodle die Eingabeelemente —
Checkboxen, Zahlenfeld, Zuordnungs-Auswahlfelder — selbst und **außerhalb**
des Fragetext-HTML. Sie stehen dann optisch losgelöst unter dem eigenen
Layout. Als Cloze liegen die Eingabeelemente technisch im selben
Fragetext-Feld und erscheinen dadurch innerhalb des Layouts.

Geht Cloze aus einem konkreten Grund nicht, bleibt der native Typ mit einem
Layout ohne eigenen Eingabe-Block der Rückfallweg.

### multichoice → Cloze MRS (bei mehreren richtigen Antworten) bzw. MCVS/MCHS (bei genau einer)

Bei mehreren richtigen Antworten immer **MRS** verwenden (nicht MC/MCS) — die Checkboxen sollen zufällig angeordnet sein, das „S" deckt das ab.

**Schritt für Schritt.** Die Schritte 3 und 4 sind die üblichen
Fehlerquellen — unbedingt einhalten:

1. Fragetyp umstellen: `<question type="multichoice">` → `<question type="cloze">`.
2. Multichoice-spezifische Elemente ENTFERNEN (gehören nicht zu Cloze, sonst Importfehler oder Datenmüll): `<answer>` (alle), `<shownumcorrect/>`, `<single>`, `<shuffleanswers>`, `<answernumbering>`, `<showstandardinstruction>`, `<correctfeedback>`, `<partiallycorrectfeedback>`, `<incorrectfeedback>`. Cloze-Fragen haben KEINE `<answer>`-Elemente auf Fragen-Ebene — die Antworten stecken ausschließlich im `{N:MRS:...}`-Feld im Fragetext. Übrig bleiben nur: `name`, `questiontext`, `generalfeedback`, `defaultgrade`, `penalty`, `hidden`, `idnumber`, `tags`.
3. **Gewichtung: die ursprünglichen `fraction`-Werte 1:1 als Prozent-Gewicht übernehmen**, IMMER mit `~%Zahl%`, NIE das bare `=`-Kürzel (das ist nur für „genau eine richtige Antwort = 100%" gedacht — bei MRS mit mehreren Richtigen summieren sich sonst mehrere `=100%` auf über 100% und Moodle bricht den Import mit „Eine der Antworten sollte mit 100% bewertet werden" ab). Beispiel: multichoice hatte `fraction="50"` und `fraction="-25"` → Cloze bekommt `~%50%` bzw. `~%-25%`.
4. **Sonderzeichen im Antworttext escapen** (wichtig bei LaTeX-Formeln wie `\(\frac{1}{6 \cdot 10^{23}}\)`, sonst verwechselt der Cloze-Parser die Formel-Klammern mit der Feld-Begrenzung): Reihenfolge wichtig, erst Backslash, dann Rest: `\` → `\\`, dann `{` → `\{`, `}` → `\}`, `~` → `\~`, `=` → `\=`, `#` → `\#`.
5. Cloze-Feld zusammensetzen: `{1:MRS:` + alle `~%Gewicht%Text`-Optionen aneinandergehängt + `}`.
6. **Kontrollrechnung vor dem Abschluss:** Summe aller POSITIVEN Gewichte muss exakt 100 ergeben (Toleranz: `33.33333` dreimal summiert auf `99.99999` ist okay, das ist Moodles Standardwert für Drittel). Stimmt die Summe nicht, ist ein Fehler passiert.
7. Cloze-Feld an der vorgesehenen Stelle in das Frage-HTML einsetzen.
8. XML vor dem Ausliefern auf Wohlgeformtheit prüfen.

Minimalbeispiel (2 richtige, 4 falsche, keine LaTeX-Formel):
```
{1:MRS:~%-25%Falsche Option A~%50%Richtige Option 1~%-25%Falsche Option B~%-25%Falsche Option C~%-25%Falsche Option D~%50%Richtige Option 2}
```

Bei genau einer richtigen Antwort (MCVS/MCHS): normale Grundsyntax aus dem Cloze-Kapitel unten verwenden (`=RichtigeAntwort~%0%Falsch1~...`).

### numerical → Cloze NM

Gleiches Rendering-Problem wie multichoice (Zahlen-Eingabebox liegt sonst außerhalb des Layouts). Als Cloze NM umbauen: `{1:NM:=Wert:Toleranz~%Gewicht%Wert2:Toleranz2~...}`. Die Einheit NICHT über Moodles natives Einheiten-Feature abbilden (funktioniert in Cloze nicht 1:1), sondern als statischen Text direkt hinter dem Cloze-Feld anhängen, z. B. `{1:NM:=18.02:0~%75%18:0} g`.

### matching → Cloze mit MC-Dropdown-Tabelle

Gleiches Rendering-Problem (Zuordnungs-UI liegt sonst außerhalb des Layouts). Als Tabelle im Eingabe-Block umbauen: eine Zeile pro Zuordnungspaar, linke Spalte = Begriff, rechte Spalte = `{Gewichtung:MC:~%0%Option1~%100%RichtigeOption~%0%Option3...}`-Dropdown mit allen Optionen. Gewichtung pro Feld = ursprüngliche `defaultgrade` ÷ Anzahl Paare (z. B. 3 Punkte ÷ 6 Paare = 0,5 je Feld), damit die Gesamtpunktzahl der Frage erhalten bleibt.

---

