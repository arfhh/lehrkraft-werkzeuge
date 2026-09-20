# Fortschrittsmaßstab und Reihenfolge

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0
Begleitdatei zu `2-didaktik-abgaben`.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' fortschritt.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | Warum überhaupt ein Maßstab | 23–35 |
> | Der Maßstab: das obere Drittel bis Zweifünftel | 36–57 |
> | Was daraus folgt | 58–106 |
> | Die Reihenfolge-Regel | 107–130 |
> | Reihenfolge vor Median | 131–136 |
> | Wo der Hinweis steht | 137–142 |
> | Was nicht passiert | 143–150 |
<!-- /INDEX -->

## Warum überhaupt ein Maßstab

Eine Aufgabenserie läuft über Wochen. Zu jedem Zeitpunkt sind manche
Lernende bei Blatt 1, andere bei Blatt 5. Ohne Maßstab passiert eins von
zwei Dingen, und beide sind falsch:

- Die Rückmeldung orientiert sich an der schnellsten Person. Dann bekommt
  jemand mit einem abgegebenen Blatt vier Blätter vorgehalten, obwohl er
  völlig im Rahmen liegt. Das entmutigt ohne Grund.
- Es gibt gar keine Rückmeldung zum Stand. Dann merken gerade die, die noch
  nichts abgegeben haben, nichts davon — sie bekommen ja auch kein
  inhaltliches Feedback, weil es nichts zu beurteilen gibt.

## Der Maßstab: das obere Drittel bis Zweifünftel

**Erwartungsstand = Median der Anzahl abgegebener Blätter unter den besten
40 Prozent der Lerngruppe.**

Gerechnet wird so: alle Mitglieder der Gruppe absteigend nach Anzahl
abgegebener Blätter sortieren, die Personen ohne jede Abgabe ausdrücklich
mitzählen; die obersten 40 Prozent nehmen (aufgerundet, mindestens eine
Person); von diesen den Median bilden.

Warum nicht der Median der ganzen Gruppe: Er beschreibt zwar, wo die Gruppe
steht, kippt aber ins Bedeutungslose, sobald viele noch gar nichts abgegeben
haben — dann liegt er bei null oder eins, und niemand bekommt mehr eine
Rückmeldung zum Stand, gerade wenn sie am nötigsten wäre. Belegt an einem
echten Durchgang: Median der Gruppe 1, Median der besten 40 Prozent 3.

Warum nicht der Spitzenwert: Der beschreibt eine einzelne Person. Die besten
40 Prozent sind eine Gruppe, über die sich ehrlich sagen lässt, viele hätten
das schon geschafft.

Aufrunden des Ergebnisses findet nicht statt.

## Was daraus folgt

**Unter dem Erwartungsstand** — und das schließt die Personen ohne jede
Abgabe ein. Genannt wird, was bis zum Erwartungsstand fehlt, nicht was bis
zum Klassenbesten fehlt.

⚠️ **Bezugsgröße ist ausschließlich die laufende Aufgabenserie/das laufende
Thema.** Der Erwartungsstand wird bei jedem Durchgang neu berechnet, aus den
Blättern des aktuell laufenden Themas allein. Ein früheres, bereits
abgeschlossenes Thema zählt nicht mit, auch wenn es im selben Kommentarfeld
weiterlebt (Präzedenzfall 19.09.2026: ein abgeschlossenes Thema wurde
versehentlich zum laufenden addiert und ergab einen falschen, zu hohen
Erwartungsstand). Nie die Zahl aus der Vorrunde weiterschleppen.

**Die Formulierung hängt von der Rückstandsgröße ab, nicht davon, ob der
Hinweis schon einmal kam.** Rückstand = Erwartungsstand − eigene Anzahl
abgegebener Blätter (im laufenden Thema). Drei Stufen:

**Rückstand 1** — rein informativ, keine Aufforderung:

> Viele deiner Mitschülerinnen und Mitschüler haben schon drei Aufgaben
> bearbeitet. Bei dir fehlt dafür noch 1.1-02.

**Rückstand 2** — ein Hinweis zum Aufholen, noch kein Arbeitsauftrag:

> Viele deiner Mitschülerinnen und Mitschüler haben schon drei Aufgaben
> bearbeitet. Du hängst mit 1.1-01 und 1.1-02 hinterher — hol das zeitnah
> auf, damit dir der Anschluss nicht verloren geht.

**Rückstand über 2** — ein Arbeitsauftrag:

> Viele deiner Mitschülerinnen und Mitschüler haben schon vier Aufgaben
> bearbeitet. Bearbeite die fehlenden Aufgaben 1.1-01, 1.1-02 und 1.1-03 als
> Hausaufgabe.

Genannt werden dabei genau so viele der nächsten fehlenden Blätter, wie der
Rückstand groß ist — nicht alle insgesamt fehlenden, falls es mehr sind, und
nicht weniger.

Ein Speicher, der je Person und Thema festhält, ob und wann der Hinweis
zuletzt kam, ist für den Ton **nicht mehr nötig** — er ergibt sich allein
aus der aktuellen Rückstandsgröße. Ein Datum darf trotzdem dokumentiert
werden (letzter Stand des Hinweises), hat aber keinen Einfluss mehr auf die
Formulierung.

**Auf oder über dem Erwartungsstand.** Zum Stand wird nichts gesagt. Wer
im Rahmen liegt, braucht dazu keine Rückmeldung, und wer vorne liegt, schon
gar nicht.

## Die Reihenfolge-Regel

Ob eine Aufgabenserie in fester Reihenfolge zu bearbeiten ist, sagt die
Projekt-Skill. Gilt sie, folgt daraus eine eigene, schärfere Rückmeldung.

Wer Blatt 4 abgegeben hat, muss 1 bis 3 bearbeitet haben — das ist die
Voraussetzung dafür, dass 4 überhaupt sinnvoll bearbeitbar war. Fehlt ein
kleineres Blatt unterhalb des eigenen höchsten, ist das kein
Rückstand, sondern eine **Lücke**.

Bei einer Lücke gilt:

- Sie wird ausdrücklich benannt, mit Nummer.
- Hier darf und soll zum Nacharbeiten aufgefordert werden. Das ist die
  Ausnahme von der Regel, im laufenden Zwischenfeedback nicht zum
  Nachreichen aufzufordern — denn hier fehlt eine Voraussetzung, nicht
  nur ein Stück Arbeit.
- Der Ton bleibt sachlich: was fehlt, dass es zum Weiterarbeiten gebraucht
  wird, und dass es nachgeholt werden soll. Keine Ermahnung, keine Wertung
  der Person.

Beispiel: „Von 1.1-01 und 1.1-02 liegt nichts vor, obwohl du 1.1-03 schon
bearbeitet hast. Die beiden bauen aufeinander auf — hol sie bitte nach."

## Reihenfolge vor Median

Beides kann zugleich zutreffen. Dann steht die Lücke vorn und der
Rückstand entfällt: Wer eine Lücke hat, hat ohnehin schon die klarere
Ansage bekommen; zwei Hinweise zum selben Thema verwässern sich.

## Wo der Hinweis steht

Am Ende des Kommentarfeldes, nach dem inhaltlichen Feedback zu den
abgegebenen Blättern, als eigener kurzer Absatz. Bei Personen ohne jede
Abgabe ist er der einzige Inhalt.

## Was nicht passiert

- Keine Nennung anderer Lernender, auch nicht anonymisiert, auch nicht als
  Vergleich („die meisten sind schon bei …"). Der Maßstab wird benutzt, er
  wird nicht mitgeteilt.
- Keine Zahlenangabe zum eigenen Rang oder zur Position in der Gruppe.
- Keine Aussage darüber, was das für die spätere Note bedeutet. Das ist
  Sache des Abschlussfeedbacks.
