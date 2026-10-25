# Regeln für Sprechtexte

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

Das Modell liest, was dasteht. Alles, was nicht eindeutig als gesprochenes
Deutsch dasteht, wird geraten — oft falsch. Darum wird jeder Text vorher
so geschrieben, wie man ihn spricht. Fachgebundene Regeln (Formeln,
Fachsymbole, fachtypische Abkürzungen) gehören in eine Fach-Skill; hier
steht nur, was für jeden Text gilt.

## Ausschreiben

| Im Text | Im Sprechtext |
|---|---|
| z. B., d. h., usw., ca. | zum Beispiel, das heißt, und so weiter, circa |
| 25 °C, 3 kg, 15 min | fünfundzwanzig Grad Celsius, drei Kilogramm, fünfzehn Minuten |
| 1,5 | eins Komma fünf |
| 2026 (Jahr) | zweitausendsechsundzwanzig |
| 3. Aufgabe | dritte Aufgabe |
| 50 % | fünfzig Prozent |
| a), b) | Teil a, Teil b |
| → | daraus folgt / ergibt |
| Abb. 2 | Abbildung zwei |

- **Zahlen grundsätzlich als Wort.** Ziffern liest das Modell meist
  richtig, aber nicht immer — besonders nicht mit Einheit, Komma oder
  Bindestrich.
- **Einzelbuchstaben lautschriftlich**, wenn sie allein stehen: „aa“,
  „bee“, „zee“, „dee“, „ee“, „eff“, „gee“, „haa“, „iks“, „ypsilon“, „zett“.
- **Abkürzungen, die man buchstabiert,** mit Bindestrichen: „Ce-De“,
  „Pe-De-Eff“. Abkürzungen, die man als Wort spricht, unverändert.
- **Fremdwörter** mit ungewöhnlicher Aussprache testweise vertonen; notfalls
  lautnah schreiben.

## Entfernen oder umwandeln

- Klammern: Inhalt mit Kommas einbetten oder als eigenen Satz.
- Aufzählungszeichen, Nummern, Sternchen, Emojis, URLs: entfernen. Listen
  als Satz: „Ihr braucht drei Dinge: erstens …, zweitens …“
- Tabellen: nicht vorlesen lassen, sondern in Sätze übertragen.
- Fettdruck, Überschriftenzeichen: entfernen. Überschriften als kurzer
  eigener Absatz.

## Satzbau und Pausen

- **Kurze Sätze**, höchstens etwa 25 Wörter. Das Skript teilt Text in
  Stücke von höchstens 250 Zeichen; lange Sätze werden an Kommas
  getrennt, was hörbar ist.
- **Punkt** = Satzpause; **Komma** = kurze Pause; **Leerzeile** = längere
  Absatzpause.
- Doppelpunkt, Semikolon, Gedankenstrich und Auslassungspunkte werden vom
  Modell in Kommas umgewandelt — für eine deutliche Pause einen Punkt
  setzen.
- **Fragezeichen** heben die Satzmelodie; bei Aufgabenstellungen gezielt
  einsetzen.
- Wichtige Wörter nicht mit Großbuchstaben betonen — wird buchstabiert.

## Gegenlesen

Auch eine KI, die den Sprechtext erstellt, macht Fehler, vor allem bei
Zahlen und Fachausdrücken. Sprechtext lesen, fertige Audiodatei einmal
vollständig anhören.

## Vorbereiter-Prompt (für jede KI)

```
Überarbeite den folgenden Text so, dass ihn eine Text-to-Speech-KI fehlerfrei
vorlesen kann. Gib nur den fertigen Sprechtext aus, ohne Erklärungen.
Regeln: Zahlen, Einheiten, Prozent und Ordinalzahlen als Wort ausschreiben.
Abkürzungen auflösen. Einzelne Buchstaben lautschriftlich (aa, bee, iks).
Klammern, Aufzählungszeichen, Emojis, URLs und Formatierung entfernen; Listen
und Tabellen in vollständige Sätze übertragen. Sätze mit höchstens 25 Wörtern.
Doppelpunkt, Semikolon und Gedankenstrich durch Punkt oder Komma ersetzen.
Absätze durch eine Leerzeile trennen. Inhalt und Wortlaut sonst nicht ändern.
[Hier ggf. die Fachregeln aus der Fach-Skill einfügen.]

Text:
```
