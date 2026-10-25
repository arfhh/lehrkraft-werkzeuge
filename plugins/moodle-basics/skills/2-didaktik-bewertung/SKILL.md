---
name: "2-didaktik-bewertung"
description: "Bewertungs- und Feedbackregeln für digitale Lernaufgaben, fachunabhängig (Skala, AFB, Feedbacktexte, Anonymität, Duplikate)."
---

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.


# Bewerten und Rückmelden

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 2 — Didaktik, fachunabhängig, frei an Lehrkräfte weiterzugeben

Diese Skill hält fest, nach welchen Maßstäben bewertet und wie
zurückgemeldet wird. Sie ist unabhängig von Fach, Schulform und
Lernplattform. Welche Datei- oder Fragenformate daraus entstehen,
bestimmen die Technik-Skills; welche Aufgaben und Themen bewertet werden,
bestimmt die aufrufende Projekt-Skill.

**Begleitdateien** (im gleichnamigen Werkzeug-Ordner):

| Datei | Lesen, wenn … |
|---|---|
| `fehlervarianten.md` | Lücken angelegt oder Fehlervarianten ergänzt werden |
| `feedback-und-note.md` | Rückmeldungen formuliert oder Noten berechnet werden |

## 1 · Die 6-Stufen-Skala für Kurzantworten

Bei automatisch ausgewerteten Kurzantworten entscheidet die Schreibweise
über die Punktzahl. Ohne festen Maßstab wird das von Aufgabe zu Aufgabe
anders gehandhabt und ist für die Lernenden nicht nachvollziehbar.
**Immer diese sechs Stufen, nicht frei improvisieren:**

| Stufe | % | Kriterium |
|---|---|---|
| 1 | 100 | Korrekt geschrieben, oder ein echtes akzeptiertes Synonym; ebenso ein Platzhaltermuster, das nur korrekte Wortformen und Endungsvarianten abdeckt |
| 2 | 90 | Wort korrekt, nur Groß-/Kleinschreibung falsch — nur relevant, wenn die Auswertung überhaupt zwischen Groß- und Kleinschreibung unterscheidet; sonst entfällt die Stufe |
| 3 | 75 | Ein einzelner klarer Tippfehler (ein Buchstabe vertauscht, doppelt oder fehlend), Wort eindeutig erkennbar |
| 4 | 50 | Mehrere Tippfehler oder eine stärkere Verschreibung, Wort noch mit Mühe erkennbar |
| 5 | 25 | Nur Wortstamm oder Wortanfang erkennbar, starke Verkürzung, oder ein breiter Platzhaltertreffer |
| 6 | 0.01 | Falsches Wort oder Rateversuch ohne erkennbaren Bezug — **bewusst nicht 0 %** |

**Warum 0.01 statt 0.** In der Auswertungstabelle der Lernplattform bleibt
so sichtbar, dass dieser Fehler bereits bekannt und geprüft ist. Eine echte
Neuentdeckung erscheint dagegen als 0 % ohne Treffer. Der Unterschied ist
das Werkzeug, mit dem sich nach jedem Durchgang genau die noch unbekannten
Schreibweisen herausfischen lassen.

Alle Antwortvarianten eines Feldes werden **absteigend nach Prozentwert
sortiert** (100 → 0.01). Prozentwerte mit Dezimalpunkt schreiben, nicht mit
Komma.

**Echte Wortverwechslungen** — ein anderer, tatsächlich existierender
Begriff — landen auf 0.01 %. Ausnahme: die Lehrkraft bestätigt
ausdrücklich, dass beides gelten soll, etwa weil zwei Gegenstände auf einem
Foto nicht eindeutig zu unterscheiden sind. Dann 100 %. **Im Zweifel
nachfragen**, bevor eine augenscheinlich falsche Antwort auf 0.01 % statt
100 % gesetzt wird.

**Wo die Skala NICHT gilt: bei Zahlen.** Numerische Lücken werden nicht
gegen die Rechtschreibskala geprüft — Teilpunkte für einen Rechenfehler
sind etwas anderes als Toleranz gegenüber einem Tippfehler. Dasselbe gilt
für **negative Prozentwerte bei Mehrfachauswahl**: ein Minuswert ist dort
der reguläre Mechanismus gegen Ankreuzen auf Verdacht und kein Fehler, den
die Skala einzustufen hätte.

## 2 · Neue Fehlervarianten ableiten

Damit die Skala greift, müssen plausible Falschschreibungen vorher
eingetragen sein — Richtwert **etwa zehn pro Lücke**. Die neun
Fehlerkategorien (häufigste: Getrennt-/Zusammenschreibung, Doppelung,
Auslassung), ihre Zuordnung zur Skala (eine Kategorie 75, zwei 50,
Stamm/Platzhalter 25), die Zusatzmuster für 100 % (Artikel-/Vollform,
verwandte Wortform) und die Synonym-Regel: Begleitdatei
`fehlervarianten.md`. **Beim Anlegen oder Überarbeiten von Lücken immer
lesen.**

## 3 · Anforderungsbereiche

Jede Aufgabe wird einem Anforderungsbereich zugeordnet:

| AFB | Bezeichnung | Was verlangt wird |
|---|---|---|
| I | Reproduktion | Wiedergeben, benennen, beschreiben |
| II | Anwendung und Analyse | Übertragen, ordnen, erklären, auswerten |
| III | Bewertung und Transfer | Beurteilen, begründen, auf Neues übertragen |

Zwei Regeln dazu:

- Wird ein bestehender Aufgabentext übernommen, ist eine **römische Zahl in
  Klammern** hinter der Aufgabe der übliche AFB-Marker.
- In einem Aufgabenpool, aus dem zufällig gezogen wird, müssen **alle
  Aufgaben denselben AFB** haben — sonst hängt die Note vom Losglück ab.
  Dasselbe gilt für Schwierigkeit und Aufgabentyp.

## 4 · Aufgaben formulieren

- **Jede Aufgabe beginnt mit einem Operator** („Nenne", „Erkläre",
  „Beurteile"), hervorgehoben. Aus Fragen werden Anweisungen: nicht „Was
  ist …?", sondern „Erkläre, was … ist."
- Bei freien Schreibaufgaben den Hinweis **„in eigenen Worten"** ergänzen,
  damit nicht abgeschrieben wird. Formulierung von Aufgabe zu Aufgabe
  variieren, sonst wird sie überlesen.
- Eine Aufgabe hat **eine** eindeutige Lösung. Lässt sich das nicht
  herstellen, ist es keine automatisch auswertbare Aufgabe.
- **Eine Ein-Wort-Antwort ist keine Freitextaufgabe.** Wo genau ein Begriff
  erwartet wird, gehört eine automatisch ausgewertete Lückenform hin — die
  kann das besser und gerechter. Eine Freitextaufgabe verlangt mindestens
  zwei bis drei Sätze; erst dann ist es sinnvoll, neben dem Inhalt auch die
  sprachliche Form zu bewerten.

## 5 · Feedback an Schülerinnen und Schüler

Kernregeln:

- **Kurzantworten:** Lösungswort nennen ist erwünscht, sonst kurz halten;
  ein Satz nur bei Verwechslungsgefahr oder Denkfehler.
- **Sprachfehler** wörtlich zitieren und richtig danebenstellen, höchstens
  zwei bis drei Vorschläge. Fehlerfreie Antwort: **kein** Kommentar.
- **Längere Arbeiten:** Ansprache „Du", nie ein Name; reiner Klartext ohne
  Markdown/LaTeX/Tabellen, Fachzeichen als Unicode; keine Aufforderung zum
  Nachreichen nach Fristende.
- **Fachlicher Abzug braucht immer eine Erklärung.** Ist eine Aufgabe nicht
  zu 100 % richtig, steht im Feedback kurz, was fachlich falsch ist und wie
  es richtig heißt. Sonst sehen die Lernenden nur einen Abzug und können sich
  nicht verbessern. Nicht bearbeitete Teile brauchen keine Erklärung, das ist
  den Lernenden sofort klar. Fachliche Fehler dagegen erkennen sie nicht
  immer, deshalb dort die richtige Antwort nennen.

Beispieltexte, Unterrichts-Schreibweisen und das Zusammensetzen eines
einzigen Kommentarfeldes: Begleitdatei `feedback-und-note.md`.

## 6 · Bewertungsstufen und Note

Längere Arbeiten: **voll / halb / fehlend** statt Punkten. Pflicht- vs.
Wahlaufgaben, Prozentgrenzen (legt die Projekt-Skill fest) und
**Sprachbewertung nur als Abzug vom Inhalt, nie als zweiter Topf**:
Details in `feedback-und-note.md` — vor jeder Notenberechnung lesen.

## 7 · Anonymisiert bewerten

Wo Schülerarbeiten maschinell verarbeitet werden, gilt:

- Bewertet wird **ausschließlich über Kürzel-IDs**. Klarnamen erreichen die
  Bewertung nicht.
- Die Zuordnungsdatei zwischen Kürzel und Klarnamen wird **nie gelesen und
  nie verändert**. Sie ist Sache der Lehrkraft.
- Kommt in einer Abgabe trotzdem ein Klarname vor, wird er ignoriert und
  nicht in Rückmeldungen übernommen.

## 8 · Duplikate im Graubereich

Bei Verdacht auf abgeschriebene Arbeiten wird **bewusst konservativ**
entschieden:

- „technisch kopiert" — dieselbe Datei geteilt → bestätigen
- „selbst sehr ähnlich geschrieben" → nicht bestätigen
- Im Zweifel nicht bestätigen.

Kleine natürliche Abweichungen sind das Erkennungsmerkmal **eigenständiger
Arbeit**, kein Grund zur Vorsicht. Ein Duplikatsverdacht wird der Lehrkraft
gemeldet, nicht selbst zur Note verarbeitet.