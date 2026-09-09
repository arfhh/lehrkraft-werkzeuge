# XML-Vorlagen der nativen Fragetypen

Referenz zu `1-moodle-xml`. Die allgemeinen XML-Regeln und die
fraction-Bewertungsregeln stehen in der SKILL.md; Cloze steht in
`cloze.md`.

Die Vorlagen sind wortwörtlich als Gerüst zu übernehmen — nur die Inhalte
werden ausgetauscht.

## Übersicht

| Fragetyp | XML-type | Beschreibung |
|---|---|---|
| Multiple Choice (Einzelantwort) | `multichoice` | eine richtige Antwort |
| Multiple Choice (Mehrfachantwort) | `multichoice` | mehrere richtige Antworten |
| Wahr/Falsch | `truefalse` | Aussage wahr oder falsch |
| Kurzantwort | `shortanswer` | Freitext mit hinterlegten Varianten |
| Zuordnung | `matching` | Begriffe ↔ Aussagen zuordnen |
| Numerische Antwort | `numerical` | Zahlenwert mit Fehlerbereich, optional Einheiten |
| Essay/Freitext | `essay` | offene Antwort, manuell bewertet |
| Beschreibung | `description` | Infotext ohne Antwortmöglichkeit |
| Lückentext | `cloze` | eingebettete Antworten im Text, siehe `cloze.md` |
| Berechnete Frage | `calculated` | formelbasiert mit Variablen und Datensätzen |
| Einfach berechnet | `calculatedsimple` | vereinfachte berechnete Frage |

Nicht über XML abbildbar: `calculatedmulti` sowie Drag-and-drop- und
bildmarkierungs-Spezialtypen.

## Kategorie-Pseudofrage

Steht als erster `<question>`-Block der Datei und legt fest, in welche
Kategorie der Fragensammlung alle folgenden Fragen importiert werden.
Unterkategorien werden mit `/` getrennt.

```xml
<question type="category">
  <category>
    <text>$course$/Kategoriename</text>
  </category>
</question>
```

## Multiple Choice — Einzelantwort

```xml
<question type="multichoice">
  <name><text>Fragetitel</text></name>
  <questiontext format="html">
    <text><![CDATA[<p>Fragetext hier</p>]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[<p>Allgemeines Feedback</p>]]></text>
  </generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <single>true</single>
  <shuffleanswers>true</shuffleanswers>
  <answernumbering>abc</answernumbering>
  <showstandardinstruction>0</showstandardinstruction>
  <correctfeedback format="html">
    <text><![CDATA[<p>Richtig!</p>]]></text>
  </correctfeedback>
  <partiallycorrectfeedback format="html">
    <text><![CDATA[<p>Teilweise richtig.</p>]]></text>
  </partiallycorrectfeedback>
  <incorrectfeedback format="html">
    <text><![CDATA[<p>Leider falsch.</p>]]></text>
  </incorrectfeedback>
  <shownumcorrect/>
  <answer fraction="100" format="html">
    <text><![CDATA[<p>Richtige Antwort</p>]]></text>
    <feedback format="html"><text><![CDATA[<p>Korrekt, weil…</p>]]></text></feedback>
  </answer>
  <answer fraction="0" format="html">
    <text><![CDATA[<p>Falsche Antwort 1</p>]]></text>
    <feedback format="html"><text><![CDATA[<p>Falsch, weil…</p>]]></text></feedback>
  </answer>
  <answer fraction="0" format="html">
    <text><![CDATA[<p>Falsche Antwort 2</p>]]></text>
    <feedback format="html"><text><![CDATA[<p>Falsch, weil…</p>]]></text></feedback>
  </answer>
  <answer fraction="0" format="html">
    <text><![CDATA[<p>Falsche Antwort 3</p>]]></text>
    <feedback format="html"><text><![CDATA[<p>Falsch, weil…</p>]]></text></feedback>
  </answer>
</question>
```

## Multiple Choice — Mehrfachantwort

Aufbau wie Einzelantwort, aber `<single>false</single>`, und die Antworten
nutzen positive und negative fraction-Werte nach Regel 2 der SKILL.md
(z. B. zwei richtige à `fraction="50"`, falsche à `fraction="-50"`). Die
Summe der positiven Werte muss exakt 100 ergeben.

## Wahr/Falsch

```xml
<question type="truefalse">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Aussage hier</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Erklärung</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>1.0000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <answer fraction="100" format="moodle_auto_format">
    <text>true</text>
    <feedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></feedback>
  </answer>
  <answer fraction="0" format="moodle_auto_format">
    <text>false</text>
    <feedback format="html"><text><![CDATA[<p>Falsch, weil…</p>]]></text></feedback>
  </answer>
</question>
```

## Kurzantwort

```xml
<question type="shortanswer">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Fragetext</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Erklärung</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <usecase>0</usecase>
  <answer fraction="100" format="moodle_auto_format">
    <text>Korrekte Antwort</text>
    <feedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></feedback>
  </answer>
  <answer fraction="100" format="moodle_auto_format">
    <text>Alternative Schreibweise</text>
    <feedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></feedback>
  </answer>
  <answer fraction="0" format="moodle_auto_format">
    <text>*</text>
    <feedback format="html"><text><![CDATA[<p>Leider falsch. Die korrekte Antwort ist: …</p>]]></text></feedback>
  </answer>
</question>
```

`<usecase>0</usecase>` = Groß-/Kleinschreibung wird ignoriert (Standard),
`<usecase>1</usecase>` = wird beachtet. `*` ist die Auffangantwort für alles
Übrige. Teiltreffer werden über zusätzliche Antworten mit kleineren
fraction-Werten abgebildet; welcher Wert für welche Abweichung gilt, gibt
der Bewertungsmaßstab der aufrufenden Skill vor.

## Numerische Antwort

```xml
<question type="numerical">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Fragetext</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Erklärung</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <answer fraction="100">
    <text>42</text>
    <feedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></feedback>
    <tolerance>0.5</tolerance>
  </answer>
  <units>
    <unit><multiplier>1</multiplier><unit_name>kg</unit_name></unit>
    <unit><multiplier>1000</multiplier><unit_name>g</unit_name></unit>
  </units>
  <unitgradingtype>0</unitgradingtype>
  <unitpenalty>0.1000000</unitpenalty>
  <showunits>3</showunits>
  <unitsleft>0</unitsleft>
</question>
```

`<tolerance>` ist der akzeptierte Bereich um den Zahlenwert. Eine absolute
Toleranz wie `0.5` ist die verständlichste Form. Dezimaltrennzeichen ist
immer der Punkt.

## Zuordnung (Matching)

Mindestens drei, besser vier oder mehr Paare. Ein `<subquestion>` mit leerem
`<text>` liefert einen Distraktor, der in der Auswahlliste erscheint, aber
zu keinem Begriff gehört. Keine fraction-Attribute — Moodle bewertet
automatisch.

```xml
<question type="matching">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Ordne die Begriffe richtig zu:</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Erklärung</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <shuffleanswers>true</shuffleanswers>
  <correctfeedback format="html"><text><![CDATA[<p>Alles richtig!</p>]]></text></correctfeedback>
  <partiallycorrectfeedback format="html"><text><![CDATA[<p>Teilweise richtig.</p>]]></text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text><![CDATA[<p>Leider falsch.</p>]]></text></incorrectfeedback>
  <shownumcorrect/>
  <subquestion format="html">
    <text><![CDATA[<p>Begriff 1</p>]]></text>
    <answer><text>Zuordnung 1</text></answer>
  </subquestion>
  <subquestion format="html">
    <text><![CDATA[<p>Begriff 2</p>]]></text>
    <answer><text>Zuordnung 2</text></answer>
  </subquestion>
  <subquestion format="html">
    <text><![CDATA[<p></p>]]></text>
    <answer><text>Distraktor-Zuordnung</text></answer>
  </subquestion>
</question>
```

## Essay/Freitext

```xml
<question type="essay">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Fragetext</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Erwarteter Inhalt / Musterlösung</p>]]></text></generalfeedback>
  <defaultgrade>5.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <responseformat>editor</responseformat>
  <responserequired>1</responserequired>
  <responsefieldlines>15</responsefieldlines>
  <minwordlimit></minwordlimit>
  <maxwordlimit></maxwordlimit>
  <attachments>0</attachments>
  <attachmentsrequired>0</attachmentsrequired>
  <maxbytes>0</maxbytes>
  <filetypeslist></filetypeslist>
  <graderinfo format="html"><text><![CDATA[<p>Bewertungshinweis für die Lehrkraft</p>]]></text></graderinfo>
  <responsetemplate format="html"><text><![CDATA[<p>Vorlage für die Antwort (optional)</p>]]></text></responsetemplate>
  <answer fraction="0"><text></text></answer>
</question>
```

`responseformat` ist **nicht** `html`, sondern einer von `editor`,
`editorfilepicker`, `plain`, `monospaced`, `noinline`. Die
`responsetemplate` erscheint als vorbelegter Text im Antwortfeld.

## Beschreibung

```xml
<question type="description">
  <name><text>Einleitungstext</text></name>
  <questiontext format="html"><text><![CDATA[<p>Infotext ohne Antwortmöglichkeit.</p>]]></text></questiontext>
  <generalfeedback format="html"><text></text></generalfeedback>
  <defaultgrade>0.0000000</defaultgrade>
  <penalty>0.0000000</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
</question>
```

## Berechnete Frage (`calculated`)

Variablen stehen in geschweiften Klammern im Fragetext und in der
Antwortformel; `{={a}+{b}}` rechnet im Feedback. Keine Datensätze mit
Division durch Null oder unsinnigen Werten erzeugen. Die
`dataset_definitions` müssen für jede Variable gleich viele
`dataset_item`-Einträge enthalten.

```xml
<question type="calculated">
  <name><text>Fragetitel</text></name>
  <questiontext format="html"><text><![CDATA[<p>Was ist {a} + {b}?</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Die Summe von {a} und {b} ist {={a}+{b}}.</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <idnumber></idnumber>
  <synchronize>0</synchronize>
  <single>0</single>
  <answernumbering>abc</answernumbering>
  <shuffleanswers>0</shuffleanswers>
  <correctfeedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></correctfeedback>
  <partiallycorrectfeedback format="html"><text><![CDATA[<p>Teilweise richtig.</p>]]></text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text><![CDATA[<p>Falsch.</p>]]></text></incorrectfeedback>
  <answer fraction="100">
    <text>{a}+{b}</text>
    <tolerance>0.01</tolerance>
    <tolerancetype>1</tolerancetype>
    <correctanswerformat>1</correctanswerformat>
    <correctanswerlength>2</correctanswerlength>
    <feedback format="html"><text><![CDATA[<p>Richtig!</p>]]></text></feedback>
  </answer>
  <dataset_definitions>
    <dataset_definition>
      <status><text>private</text></status>
      <n><text>a</text></n>
      <type>calculated</type>
      <distribution><text>uniform</text></distribution>
      <minimum><text>1</text></minimum>
      <maximum><text>100</text></maximum>
      <decimals><text>0</text></decimals>
      <itemcount>10</itemcount>
      <number_of_items>10</number_of_items>
      <dataset_items>
        <dataset_item><number>1</number><value>23</value></dataset_item>
        <dataset_item><number>2</number><value>47</value></dataset_item>
        <dataset_item><number>3</number><value>12</value></dataset_item>
        <dataset_item><number>4</number><value>89</value></dataset_item>
        <dataset_item><number>5</number><value>34</value></dataset_item>
        <dataset_item><number>6</number><value>56</value></dataset_item>
        <dataset_item><number>7</number><value>71</value></dataset_item>
        <dataset_item><number>8</number><value>8</value></dataset_item>
        <dataset_item><number>9</number><value>95</value></dataset_item>
        <dataset_item><number>10</number><value>63</value></dataset_item>
      </dataset_items>
    </dataset_definition>
    <dataset_definition>
      <status><text>private</text></status>
      <n><text>b</text></n>
      <type>calculated</type>
      <distribution><text>uniform</text></distribution>
      <minimum><text>1</text></minimum>
      <maximum><text>100</text></maximum>
      <decimals><text>0</text></decimals>
      <itemcount>10</itemcount>
      <number_of_items>10</number_of_items>
      <dataset_items>
        <dataset_item><number>1</number><value>15</value></dataset_item>
        <dataset_item><number>2</number><value>38</value></dataset_item>
        <dataset_item><number>3</number><value>77</value></dataset_item>
        <dataset_item><number>4</number><value>4</value></dataset_item>
        <dataset_item><number>5</number><value>52</value></dataset_item>
        <dataset_item><number>6</number><value>29</value></dataset_item>
        <dataset_item><number>7</number><value>61</value></dataset_item>
        <dataset_item><number>8</number><value>43</value></dataset_item>
        <dataset_item><number>9</number><value>16</value></dataset_item>
        <dataset_item><number>10</number><value>88</value></dataset_item>
      </dataset_items>
    </dataset_definition>
  </dataset_definitions>
</question>
```

`calculatedsimple` ist identisch aufgebaut, nur mit
`<type>calculatedsimple</type>` in den `dataset_definitions` und meist
kleineren Wertebereichen. Standardvorschlag: `calculatedsimple` statt
`calculated`, sofern keine über mehrere Fragen geteilten Datensätze nötig
sind.

## Optionale Zusatzelemente

Tags — stehen innerhalb eines `<question>`-Blocks:

```xml
<tags>
  <tag><text>Schlagwort1</text></tag>
  <tag><text>Schlagwort2</text></tag>
</tags>
```

Hints — wirken nur in adaptiven Testmodi, in der Reihenfolge der Fehlversuche:

```xml
<hint format="html">
  <text><![CDATA[<p>Erster Hinweis – nach dem ersten Fehlversuch</p>]]></text>
  <shownumcorrect/>
  <clearwrong/>
</hint>
<hint format="html">
  <text><![CDATA[<p>Zweiter Hinweis</p>]]></text>
</hint>
```

`<shownumcorrect/>` zeigt nach dem Fehlversuch die Anzahl richtiger
Teilantworten, `<clearwrong/>` löscht die falschen Eingaben.
