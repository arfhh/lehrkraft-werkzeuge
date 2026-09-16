# Verifizierte Moodle-Selektoren und URLs

Begleitdatei zu `1-chrome-mv3`. Alle Angaben sind an einer laufenden
Moodle-Installation geprüft. Pfade stehen relativ zur Moodle-Wurzel, damit
sie auch bei einer Installation in einem Unterverzeichnis stimmen.


Alles hier wurde live geprüft. Nicht neu erraten — und wenn etwas nicht mehr stimmt,
hier korrigieren. Pfadangaben sind **relativ zur Moodle-Wurzel** zu lesen.

<!-- INDEX -->
> **Abschnitte.** Diese Datei muss nicht ganz gelesen werden — nur den
> gebrauchten Abschnitt: `sed -n '<von>,<bis>p' moodle-selektoren.md`.
> Nach inhaltlichen Aenderungen `python3 index_bauen.py` laufen lassen,
> sonst stimmen die Zeilen nicht mehr.
>
> | Abschnitt | Zeilen |
> |---|---|
> | Notenstufen-Seite | 32–41 |
> | Bewertungsseite (Manuelle Bewertung) | 42–55 |
> | Richtige Antworten holen | 56–68 |
> | Kursname | 69–75 |
> | DOM der Bewertungsseite bei Essay-Fragen | 76–88 |
> | Draft-Dateibereich: „File does not exist" | 89–101 |
> | Speichern erzeugt eine neue Fragen-ID | 102–113 |
> | Schon nachbewertet erkennt man nur arithmetisch | 114–129 |
> | Das Bearbeiten-Formular einer Frage (live geprüft 04.09.2026) | 130–173 |
> | Präzisierung zu draftfile-Bildern (04.09.2026) | 174–182 |
> | Schreiben ins Fragenformular: zwei Fallen, live belegt 04.09.2026 | 183–204 |
<!-- /INDEX -->

### Notenstufen-Seite

- Übersicht: `…/grade/edit/letter/index.php?id=<kursid>`
  Bearbeiten: dieselbe URL **+ `&edit=1`**
- Der „Bearbeiten"-Knopf sitzt in einem **GET**-Formular ohne `target` → derselbe Tab.
- `input[name="gradeentryadd"]` („X Feld(er) zum Formular hinzufügen") ist ein
  **`type="submit"`** → jeder Klick lädt die Seite neu. Standard sind **3 Felder** pro Klick.
- Feldnamen: **`gradeletter[N]` / `gradeboundary[N]`** — nicht `letter[N]`.
- Override-Checkbox: `#id_override`. Legenden: „Note 1", „Note 2", …

### Bewertungsseite (Manuelle Bewertung)

- URL: `mod/quiz/report.php?id=<cmid>&mode=grading&slot=…&qid=…&grade=<filter>&includeauto=1&qperpage=100`
- **`grade=autograded`** nur fürs reine Auslesen. **`grade=all`** fürs Eintragen, fürs
  Gegenprüfen und wenn Feedback-Kandidaten gesammelt werden — ein manuell bewerteter
  Versuch verlässt `autograded` sofort.
- Punktefeld `input[name$="-mark"]`, daneben `-maxmark`, Kommentar `textarea[name$="-comment"]`.
- **Punkte im deutschen Format mit Komma** (`0,75`), sonst nimmt Moodle den Wert nicht an.
- Cloze-Lücken: `input[name$="_answer"]`, Lückennummer aus `sub(\d+)_`, Status über die
  Klassen `correct` / `partiallycorrect` / `incorrect`.
- Versuchsschlüssel `qubaid` aus `div.que` id `question-<qubaid>-<slot>`.
- **Es gibt hier KEINEN `.rightanswer`-Block** und keine `.feedback`/`.outcome`-Elemente.
  Die richtige Antwort steht nirgends auf der Seite. Nicht erneut danach suchen.

### Richtige Antworten holen

`GET <MOODLE_ROOT>/question/bank/editquestion/question.php?id=<qid>&cmid=<cmid>` liefert
das Bearbeiten-Formular mit `textarea[name="questiontext[text]"]` — darin der
vollständige Cloze-Quelltext samt aller Varianten und Prozentwerte. Reiner Lesezugriff.

Nicht brauchbar: `/question/question.php` (500) und
`/question/bank/previewquestion/preview.php` (200, aber ohne Quelltext-Textarea).

Setzt das Recht voraus, Fragen zu bearbeiten. Fehlt es, kommt eine Weiterleitung
(z. B. auf `enrol/index.php`) mit Status 200, aber ohne die Textarea — **immer auf die
Textarea prüfen, nicht auf den Status**, und einen Rückfallpfad vorsehen.

### Kursname

Aus dem Link mit `/course/view.php` holen. Die Brotkrümel-Navigation liefert sonst
die Sprachauswahl („English (en)").

---

## DOM der Bewertungsseite bei Essay-Fragen
- `graderinfo` steht als `div.graderinfo` **im DOM der Bewertungsseite** — kein Umweg über
  `question.php` nötig (anders als beim Cloze-Quelltext).
- Schülerantwort: `textarea.qtype_essay_response`, **readonly und ohne `name`** — nur lesen.
- Die gezogene Aufgabenstellung steht bei jedem Versuch in `.qtext`.
- Essay-Fragen sind nie autobewertet: Auslesefilter ist `grade=needsgrading`, `grade=all` fürs
  Eintragen und Gegenprüfen.
- Der Kommentar wird von TinyMCE überlagert; das `textarea[name$="-comment"]` bleibt im DOM und
  im Formular. Nichts über den sichtbaren Editor versuchen.
- Panel-Positionen, damit sich die Erweiterungen nicht überlagern: Grader `top 80px` blau ·
  Reviewer `top 150px` petrol · Coach `top 220px` violett `#7c3aed`. (Coach und Grader können
  auch beide auf 80 px, sie erscheinen nie zusammen.)

## Draft-Dateibereich: „File does not exist"
Moodle legt bei **jedem** GET des Bearbeiten-Formulars einen neuen Draft-Dateibereich an
(`questiontext[itemid]`) und schreibt dessen Nummer in die `draftfile.php`-URLs der Bilder. Ein
anderswo vorbereiteter Fragetext trägt eine alte Nummer → beim Speichern **HTTP 404 „Unbekannter
Fehler mit lokalen Dateien"**.

Deshalb: Funktionen, die eine Frage schreiben, bekommen die **Änderung** übergeben, nicht den
fertigen Text. Sie laden das Formular, lesen `questiontext[text]` daraus, wenden die Änderung auf
**diesen** Text an und senden sofort. Gilt für jede Erweiterung, die Fragetexte schreibt.

Zweite Lehre aus demselben Fall: **einen HTTP-Fehlerstatus nie als Erfolg durchwinken.** Erst
`r.ok` prüfen, dann alles Weitere.

## Speichern erzeugt eine neue Fragen-ID
Moodle 4.x/5.x legt beim Speichern über das Bearbeiten-Formular eine **neue Fragenversion mit
neuer `id`** an. Die alte id bleibt gültig und liefert weiterhin den **alten** Stand — eine
Gegenprobe an der alten id meldet fälschlich „nicht gespeichert".

- Die neue id steht im `lastchanged`-Parameter der Weiterleitung. Rückfall: den Fragenamen in der
  zurückgelieferten Fragensammlung suchen (`[data-itemtype="questionname"]` → `data-itemid`).
- **Eine einmal erzeugte Patch-Liste ist nach dem Lauf verbraucht** — vor einem zweiten Durchgang
  eine frische erzeugen.
- Nützliche Nebenwirkung: die alte Version bleibt erhalten und rückholbar, und Zufallsfragen
  ziehen automatisch die neueste — laufende Tests brauchen nichts.

## Schon nachbewertet erkennt man nur arithmetisch
Der Zustandstext taugt **nicht**: bei nachbewerteten Versuchen steht dort schlicht „Richtig" bzw.
„Teilweise richtig", das Kommentarfeld ist leer, es gibt keine `.history`-Tabelle. Auch CSS-Klassen
und der Badge „v2 (neueste)" (= Fragenversion) helfen nicht.

Was funktioniert:

```
Obergrenze = (max / Anzahl Lücken) × Anzahl der Lücken, die NICHT incorrect sind
ist > Obergrenze + 0.005  →  von Hand nachbewertet
```

Setzt gleiche Lückengewichte voraus (geprüft: alle Lücken Gewicht 1). Das Gewicht steht im
Cloze-Quelltext als Zahl vor dem ersten Doppelpunkt. Bei ungleichen Gewichten müssten Erkennung
und Punkteformel auf die Einzelgewichte umgestellt werden.

## Das Bearbeiten-Formular einer Frage (live geprüft 04.09.2026)

Seite: `question/bank/editquestion/question.php?id=…&qtype=essay&cmid=…`
(Titel „Freitextfrage bearbeiten"). **Nicht** `question/edit.php` — das ist die
Fragenlisten-Seite.

- **Zwei Formulare auf der Seite**, nur das zweite trägt `graderinfo[text]`.
  `document.forms[0]` ist der Bearbeitungsmodus-Schalter im Seitenkopf. Verlässlich ist
  ausschließlich: das Formular, das `[name="graderinfo[text]"]` enthält. Die `id` des
  Fragenformulars folgt **nicht** dem Muster `mform<N>` — nicht darauf bauen.
- **Fünf FIELDSETs mit `name`** im Formular. Die Regel „aus `form.elements` nur INPUT,
  SELECT und TEXTAREA übernehmen" ist hier keine Vorsichtsmaßnahme, sondern nötig.
- Submit-Knöpfe: `updatebutton` („Speichern und weiter bearbeiten"), `submitbutton`
  („Änderungen speichern"), `cancel`. `submitbutton` nehmen, `cancel` niemals mitschicken.

| Feld | Element | id |
|---|---|---|
| `graderinfo[text]` | TEXTAREA | `id_graderinfo` |
| `graderinfo[format]` | hidden | `menugraderinfoformat` |
| `graderinfo[itemid]` | hidden | — |
| `responsetemplate[text]` | TEXTAREA | `id_responsetemplate` |
| `responsetemplate[format]` | hidden | `menuresponsetemplateformat` |
| `questiontext[text]` | TEXTAREA | `id_questiontext` |
| `name`, `defaultmark` | INPUT text | `id_name`, `id_defaultmark` |
| `responseformat`, `responsefieldlines` | SELECT | `id_responseformat`, `id_responsefieldlines` |

⚠️ **`responsetemplate[itemid]` gibt es nicht.** Die Antwortvorlage hat keinen
Draft-Dateibereich — dort können also keine Bilder liegen, und die Draft-Falle
(„File does not exist") betrifft dieses Feld nicht. `graderinfo` und `questiontext` haben
je einen.

⚠️ **TinyMCE liegt über den Textareas** (vier Editoren auf der Seite). Eine Erweiterung im
isolierten World kann die sichtbaren Felder deshalb nicht befüllen: Ein gesetzter
`textarea.value` wird beim Absenden von TinyMCEs eigenem Inhalt überschrieben. Der Weg über
`fetch` des Formulars + eigenes Absenden umgeht das vollständig und braucht keine
`scripting`-Berechtigung. Danach die offene Seite neu laden, sonst überschreibt ein
späteres Speichern von Hand das Geschriebene wieder.

**HTML übersteht das Speichern.** Eine Antwortvorlage aus verschachtelten `<div>` mit
Inline-Styles kommt unverändert zurück: Rahmen, Hintergrund, `border-radius`, kursive
`<span>` und `<p style="margin:0">` bleiben erhalten. Moodle normalisiert nur die
Schreibweise (`margin:0` → `margin: 0`) — beim Prüfen also tolerant suchen, nicht auf die
exakte Zeichenfolge testen.

### Präzisierung zu draftfile-Bildern (04.09.2026)

Der ursprüngliche Befund („Draft-URLs sind temporär und liefern später ein kaputtes
Bildsymbol") gilt **nur beim Wiederverwenden in einer ANDEREN Frage**. In der Frage, in der
sie entstanden sind, halten `draftfile.php`-Bilder im Fragetext dauerhaft — praktisch
belegt an Bestandsfragen, die seit Monaten laufen. Also: nicht von sich aus zum Austausch
drängen; erst wenn eine Icon-URL in eine andere Frage kopiert werden soll, den
`pluginfile.php`-Weg nehmen.

### Schreiben ins Fragenformular: zwei Fallen, live belegt 04.09.2026

**1 · `submitbutton`, niemals `updatebutton`.** Das Formular hat drei Absende-Knöpfe in
dieser Reihenfolge: `updatebutton` („Speichern und weiter bearbeiten"), `submitbutton`
(„Änderungen speichern"), `cancel`. Wer einfach „den ersten, der nicht cancel heißt" nimmt,
erwischt `updatebutton` — und **damit speichert Moodle nicht**. Es kommt HTTP 200, keine
Fehlermeldung, das Formular wird unverändert zurückgegeben; erst die Gegenprobe zeigt, dass
nichts angekommen ist. Mit `submitbutton` leitet Moodle auf die Fragenliste weiter und hat
gespeichert.

**2 · Nach dem Speichern liefert die alte URL den alten Stand.** Moodle legt eine neue
Fragenversion mit neuer `id` an (siehe „Speichern erzeugt eine neue Fragen-ID"). Eine
Gegenprobe an der URL, von der man gekommen ist, meldet deshalb **immer** „nicht
angekommen", obwohl alles gespeichert wurde. Die neue id steht im `lastchanged` der
Weiterleitung; Rückfall ist der Fragename in der zurückgelieferten Fragensammlung
(`[data-itemtype="questionname"][data-value="…"]` → `data-itemid`). Danach die offene Seite
**auf die neue id umleiten**, nicht neu laden — sonst arbeitet man am toten Stand weiter.

**Und die Gegenprobe muss streng genug sein.** Nur die ersten zwanzig Zeichen zu vergleichen
reicht nicht: Wenn der alte Inhalt genauso anfängt wie der neue — bei einer Antwortvorlage
mit fester Kopfzeile der Normalfall —, meldet sie Erfolg, obwohl nichts geschrieben wurde.
Länge **und** eine Passage aus der Mitte mitprüfen.
