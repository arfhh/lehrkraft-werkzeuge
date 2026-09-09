# Erweiterungen, die KI-Prompts erzeugen

Begleitdatei zu `1-chrome-mv3`.


Grader, Reviewer und Coach greifen selbst nie auf eine KI zu. Sie **erzeugen einen
Prompt**, den die Lehrkraft in einen beliebigen KI-Chat einfügt, und **lesen die
Antwort als JSON wieder ein**. Das ist die Bedingung dafür, dass sie bei Kollegen ohne
eigene Einrichtung funktionieren.

**Der Prompt muss selbsttragend sein.** Alles, was zur Beurteilung nötig ist, gehört
hinein: Bewertungsmaßstab mit ausformulierten Kriterien und Beispielen, Rechenweg für
die Punkte, exaktes Ausgabeformat. Ein Modell, das nur „vergib 90 %" liest, ohne zu
wissen wofür, liefert von Durchlauf zu Durchlauf andere Werte.

**Die KI beurteilt, das Programm rechnet.** Die KI liefert Prozentwerte oder
Einstufungen; Punkte und Feldnamen erzeugt die Erweiterung.

**Aufbau, der sich bewährt hat:**

1. Begrüßung + Lizenzhinweis — nur im ersten Batch
2. Ausgangslage: was die Daten sind und warum sie so aussehen
3. Bewertungsmaßstab, verbindlich, mit Ankerbeispielen je Stufe
4. Rechenweg
5. Schritt 1: Tabelle zur Prüfung ausgeben, **dann anhalten und fragen**
6. Schritt 2: erst nach Bestätigung das JSON
7. Die Daten selbst, hinter einem Platzhalter wie `[DATENBLOCK]`

**Batch-Regel:** Werden die Daten auf mehrere Prompts aufgeteilt, trägt **Batch 1** die
Stop-Regeln und die Modus-/Rückfragen, **Batch 2 und folgende nur Fortsetzungslogik**.
Werden beide gemischt, gewinnt die zuletzt genannte Anweisung — das war schon ein Bug.

**Prompt-Override:** Die Erweiterungen lassen den Prompt überschreiben. Beim Speichern
der Grundeinstellungen muss der Override **zurückgesetzt** werden, sonst bleiben
veraltete Parameterwerte darin eingebettet.

**Zwei Kopierknöpfe anbieten:** den fertigen Prompt samt Daten (für alle) und die
Rohdaten allein (für einen Chat, der die Regeln schon über ein eigenes Skill kennt).
Der eigene Arbeitsablauf hängt in der Regel am zweiten Knopf — der darf nie wegfallen.

**Prompt-Länge anzeigen.** Bei vielen Funden wird der Prompt schnell zu lang für einen
Chat. Die Zeichenzahl unter den Knöpfen einzublenden ist billig und erspart Rätselraten.

**Eine Warnung ohne Handlungsmöglichkeit ist wertlos.** Jede Prüfung im Panel muss
sagen, wer oder was betroffen ist und was man tun kann — mit Link zum Versuch und,
wo möglich, einem Knopf, der die fertige Nachforderung in die Zwischenablage legt.

---

## Lehren aus den Blindvergleichen
- **Übereinstimmung zweier Modelle ist kein Qualitätsmaß.** Als der Prompt die hinterlegten
  Einstufungen mitgab, sank die Übereinstimmung (15/31 → 7/19), weil ein Modell sich verankerte
  und das andere nicht. Maßstab ist die Verankerung an der hinterlegten Liste, nicht der Konsens.
  Gegenprobe: mit Erwartungshorizont in der Frage kamen zwei Modelle auf **76 von 78** gleiche
  Bewertungen — der Aufwand gehört einmalig in den Horizont, nicht in jede Bewertung.
- **Falsches Gerät = 0 %.** Ausnahme: steht die Verwechslung unter den bekannten Varianten mit
  einem Wert, gilt dieser.
- Groß-/Kleinschreibung als **Pflichtschritt vor der Skala** — sonst wird sie übersprungen.
- **Formvorgaben setzt kein Prompt durch.** 0-%-Einträge, nach Frage statt nach Versuch
  gruppiertes Feedback, aufzählende Feedbacktexte — das im Plugin abfangen, nicht im Prompt
  verschärfen.

## Drei Fehlerquellen bei KI-Prompts
1. **Fehlender Kontext.** „Verstaut" ist in „Alle Geräte müssen [[L1]] werden" falsch, in „an
   ihren Platz [[L2]] werden" richtig. Den Satz **direkt neben die zu beurteilende Angabe**
   legen, nicht nur weiter oben im Datenblock.
2. **Selbst gekürzte Liste.** Ein Modell kürzte sechs hinterlegte 100-%-Antworten auf eine und
   beurteilte gegen die Abkürzung — dieselbe Antwort bekam in zwei Durchläufen 100 % und 0 %.
   Die Ausgabe so verlangen, dass die vollständige Referenzliste sichtbar wird.
3. **Verneinte Sätze.** Bei „…werden NICHT in die Vorratsgefäße [[L1]]" hielt das Modell die
   hinterlegte Lösung für die falsche Handlung. Pflichtabschnitt **vor** den Kriterien: Satz
   lesen · gegen ALLE hinterlegten Antworten prüfen · **das Wort bewerten, nicht die Handlung**,
   mit Verneinungsbeispiel.

**Merke:** Mehr Kontext ist nicht automatisch besser — jede Erweiterung eröffnet neue Wege,
falsch zu schließen. Nach so einer Änderung denselben Datensatz erneut durchlaufen lassen und
gegen den vorherigen Lauf **diffen**, statt nur den ursprünglichen Fall zu prüfen.

---

# C · Moodle-Fakten und Prüfverfahren

## Erwartungshorizonte erzeugen lassen: drei Stellen, die schiefgehen (04.09.2026)

Am ersten Praxislauf des Grader-Generators beobachtet — das Modell hielt sich an Format
und Ablauf, lieferte inhaltlich aber dreimal das Falsche:

**1 · Beispielantworten geraten zu Musterlösungen.** Auf „formuliere so, wie Lernende
tatsächlich schreiben" kam: *„Von links nach rechts werden die Atome kleiner, weil die
Kernladung zunimmt und die Elektronen stärker angezogen werden."* Das ist Lehrersprache.
Wer so antwortet, liegt ohnehin bei voller Punktzahl — der Eintrag hilft beim Bewerten
nicht. Gebraucht werden die rauen Fassungen („der Kern zieht doller"), denn die
entscheiden über die mittleren Stufen. **Abhilfe:** ein Negativbeispiel in den Prompt,
eine Mindestzahl verlangen, und nach Wortvarianten fragen (Ring/Bahn/Ebene statt Schale).

**2 · Stufen hängen an Gummiwörtern.** „überwiegend richtig", „etwas unvollständig",
„deutliche Lücken" — daran kann sich kein Modell verankern; genau das erzeugt die
Streuung aus dem Blindvergleich. Dazu entstehen Lücken: Eine Antwort, die beide Trends
beschreibt und einen erklärt, passte gleichzeitig auf zwei Stufen. **Abhilfe:** zählbare
Bedingungen verlangen (Trends, Aspekte, Teilaussagen) und am Ende prüfen lassen, dass
jede denkbare Antwort genau EINER Stufe zuzuordnen ist.

**3 · „Reicht nicht" wird mit „ist falsch" verwechselt.** Eine sachlich falsche Aussage
landete unter „reicht nicht" statt bei Stufe 0. Ein Bewertungsmodell liest sie dann als
fast richtig. **Abhilfe:** im Prompt trennen — „reicht nicht" ist richtig, aber zu wenig;
Falsches gehört zu Stufe 0 und unter „häufiger Fehler".

Der Ablauf selbst (erst lesbare Übersicht, eine Frage auf einmal, JSON erst nach
Bestätigung) wurde eingehalten. Formatvorgaben setzt ein Prompt also durchaus durch —
inhaltliche Qualitätsvorgaben brauchen dagegen Negativbeispiele und Zählbarkeit.
