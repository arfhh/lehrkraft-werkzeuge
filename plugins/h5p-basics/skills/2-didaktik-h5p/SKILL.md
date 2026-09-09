---
name: 2-didaktik-h5p
description: "Fachlich-didaktische Beurteilung interaktiver Lerneinheiten (H5P): die Gesamtschau, bei der eine Lerneinheit als Ganzes im Zusammenhang des Lehrplans und der Nachbarthemen geprüft wird statt Folie für Folie — mit Vorschlägen für einfachere Fachtexte, ergänzende Folien, zusätzliche interaktive Übungen und bessere Bilder; die Qualitätskriterien für interaktive Aufgaben (Lückentexte, Zuordnungen, Auswahlaufgaben, freie Schreibaufgaben) und ihr Feedback; die didaktischen Entwurfsmuster für verzweigte Lernpfade. Beschreibt WAS inhaltlich gut ist, nicht wie es technisch gebaut wird — dafür ist die H5P-Technik-Skill zuständig. IMMER verwenden bei „didaktisch prüfen\", „Gesamtschau\", „inhaltliche Qualität\", „Text vereinfachen\", „neue Übung vorschlagen\", „Aufgabenqualität\", „Feedback bei falschen Antworten\", „Lernpfad gestalten\" — auch ohne Skill-Namen."
---

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.


# Interaktive Lerneinheiten didaktisch beurteilen

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** `1-h5p`
**Ebene:** 2 — Didaktik, frei an Lehrkräfte weiterzugeben

Diese Skill beschreibt, woran sich die inhaltliche Qualität einer
interaktiven Lerneinheit bemisst und was verbessert werden darf. Wie eine
Änderung technisch in die Datei kommt, steht in `1-h5p`. Welches Fach,
welcher Lehrplan und welche Materialreihe gemeint sind, sagt die aufrufende
Projekt-Skill.

## 1 · Die Gesamtschau

Über die Fehlersuche hinaus wird jede Lerneinheit einmal **als Ganzes**
angesehen — in der Rolle einer Fachlehrkraft der Zielstufe, nicht als
Korrektor. Der Auftrag lautet: mitautorschaftlich denken, nicht nur
absichern.

**Wann:** ganz am Anfang der Bearbeitung, **bevor** Vorlesetexte
geschrieben oder Aufnahmen gemacht werden. Die gesprochenen Texte müssen
sich auf den fertigen Folientext beziehen, nicht umgekehrt — sonst ist
jede spätere Textänderung eine neue Aufnahme.

**Was dabei einbezogen wird:**

- **Der Lehrplan**, aus dem Thema und Einordnung der Einheit stammen.
- **Die Nachbareinheiten** desselben Themenblocks, die vorangehende und
  die nachfolgende. Die Einheiten bauen aufeinander auf: jede soll gezielt
  etwas Neues vermitteln, ohne bereits Gelerntes unnötig zu wiederholen
  und ohne eine Lücke zur nächsten Stufe zu lassen.
- **Die komplette Einheit selbst** — Fachinhalte, interaktive Übungen,
  angehängte Arbeitsblätter, Lösungskontrolle — im Zusammenhang, nicht
  isoliert Folie für Folie.

**Was vorgeschlagen werden darf:**

- **Fachtexte vereinfachen.** Jeden Fachtext aktiv darauf prüfen, ob er
  klarer und knapper ginge — auch wenn der Inhalt bereits richtig ist.
  Fachlich korrekt, aber so einfach formuliert, dass sich auch schwächere
  Lernende den Inhalt selbständig erarbeiten können. Häufiger Fall: eine
  Formulierung ist zugleich umständlich **und** fachlich leicht ungenau;
  dann beides zusammen richten.
- **Fehlende Inhalte ergänzen** — eine Zusammenfassung, eine
  Zwischenerklärung, wo eine Verständnislücke auffällt.
- **Zusätzliche interaktive Übungen.** Hier ausdrücklich kreativ sein und
  nutzen, was das Format hergibt, statt sich auf die bisher verwendeten
  Aufgabentypen zu beschränken. Vor dem Vorschlagen eines noch nicht
  verwendeten Typs technisch gegenprüfen, ob die nötige Bibliothek in der
  Zieldatei überhaupt mitgeliefert ist (`1-h5p`, `references/technik.md`)
  — sonst ist der Vorschlag nicht umsetzbar.
- **Bilder didaktisch verbessern.** Vorhandene Vektorgrafiken dürfen bei
  einer guten Idee direkt angepasst werden. Für genuin neue Illustrationen
  wird ein Bildprompt geliefert statt selbst gezeichnet.
- **Verbesserungen am angehängten Arbeitsblatt.** Diese bleiben bewusst
  schlank: ein Teil der Lernkontrolle findet bereits interaktiv statt,
  das Blatt wird nicht künstlich aufgebläht.

**Wie vorgeschlagen wird:** im Gespräch, Folie für Folie, zunächst knapp.
Eine ausführliche Gegenüberstellung von Original und Vorschlag nur auf
Nachfrage zu einem einzelnen Punkt.

**Formulierungsvorschläge werden direkt in eine Entwurfsdatei eingebaut**,
nicht einzeln im Chat abgenickt. Die Entwurfsdatei ist die Freigabestation:
dort sieht die Lehrkraft die Änderung im Layout und im Zusammenhang und
kann in einem Durchgang reagieren, statt Text und Layout getrennt zweimal
zu beurteilen. Der Entwurf wird **neben** der noch gültigen Fassung
gespeichert, nie darüber.

Macht eine Änderung eine bereits vorhandene Vorleseaufnahme ungültig, wird
das transparent aufgelistet — welche Folie eine neue Aufnahme braucht —
aber **nach** dem Einbau in den Entwurf, nicht als Vorbedingung dafür.

**Ausnahme.** Sicherheitsunterweisungen werden von der Gesamtschau
ausgenommen: dort keine inhaltlich-didaktische Neugestaltung, nur die
üblichen Prüfungen auf Sprache, Layout und Metadaten. Der Grund ist, dass
diese Texte oft rechtlich oder schulintern abgestimmt sind. Andere
Prüfungen — etwa auf einheitliche Personendarstellung — gelten dort
weiterhin.

## 2 · Qualität interaktiver Aufgaben

**Lückentexte.** Alternative richtige Schreibweisen und naheliegende
Synonyme müssen zugelassen sein, sonst bestraft die Aufgabe Wortwahl statt
Wissen. Ergänzte Alternativen werden sichtbar aufgelistet, damit die
Lehrkraft fachlich gegenprüfen kann. Keine Synonyme bei Zahlen, Formeln
und Symbolen — dort ist genau eine Schreibweise richtig.

**Zuordnungsaufgaben.** Gezieltes Feedback nur für die **drei bis fünf
typischen Fehlvorstellungen**, nicht flächendeckend für jede mögliche
Fehlzuordnung. Ein Rückmeldetext, der bei jedem Fehler erscheint, wird
nicht gelesen. Kein Feedback auf richtige Zuordnungen — das unterbricht
den Arbeitsfluss ohne Nutzen.

**Auswahlaufgaben.** Die falschen Antworten müssen plausible
Fehlvorstellungen abbilden, nicht offensichtlicher Unsinn sein. Die
richtige Antwort darf nicht an der Formulierung erkennbar sein — etwa
weil sie als einzige lang und vorsichtig formuliert ist.

**Freie Schreibaufgaben.** Den Hinweis „in eigenen Worten" ergänzen, damit
nicht abgeschrieben wird, und die Formulierung von Aufgabe zu Aufgabe
variieren. Erkennungsmerkmal für eine freie Schreibaufgabe ist ein
großzügig bemessenes Eingabefeld.

**Rückmeldetexte** erklären, statt nur „richtig" oder „falsch" zu melden.
Eine Rückmeldung, die den Denkfehler benennt, ist der eigentliche
Lernmoment der Aufgabe.

## 3 · Verzweigte Lernpfade gestalten

Ein verzweigter Lernpfad ist didaktisch etwas anderes als eine Folge von
Aufgaben: die Lernenden treffen Entscheidungen und erleben deren Folgen.
Damit das trägt:

- **Zwei Fragen je Ebene.** Erst die Entscheidungsfrage, dann eine
  Begründungsfrage zur getroffenen Wahl. Ohne die zweite Frage wird
  geraten statt gedacht.
- **Sprechende Knotentitel.** Ein Titel wie „Ebene 2, Weg A, falsch" hilft
  beim Bauen und Prüfen; „Frage 7" hilft niemandem.
- **Sichtbare Fortschrittsmarker** in den Titeln, damit die Lernenden
  wissen, wo sie stehen — ein verzweigter Pfad nimmt ihnen sonst die
  Orientierung, die eine Seitenzahl sonst gibt.
- **Gestaffelte Rücksprünge.** Ein Fehler wirft nicht an den Anfang
  zurück, sondern eine Ebene. Zurück auf null ist Bestrafung, nicht
  Wiederholung.
- **Keine Kreuzungen.** Wege laufen nach unten und treffen sich höchstens
  an klar benannten Sammelpunkten. Ein Netz statt eines Baums ist weder
  planbar noch prüfbar.
- **Jede Rückmeldung wird ausformuliert**, auch die auf den falschen
  Wegen. Gerade dort findet das Lernen statt.
