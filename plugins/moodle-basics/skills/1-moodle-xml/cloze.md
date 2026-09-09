# Cloze — der vollständige Formenkanon

Begleitdatei zu `1-moodle-xml`. Cloze ist der Fragetyp, mit dem sich
mehrere Eingabefelder verschiedener Art in EINEN zusammenhängenden Text
setzen lassen. Die Syntax ist streng: ein fehlendes Zeichen und Moodle
lehnt den Import ab oder zeigt den Rohcode an.

Der Bewertungsmaßstab für Teilpunkte bei Tippfehlern kommt von außen —
diese Datei beschreibt nur, WIE Prozentwerte notiert werden, nicht WELCHE
vergeben werden. Alle Antwortvarianten eines Feldes werden absteigend nach
Prozentwert sortiert; Prozentwerte immer mit Dezimalpunkt, nie mit Komma.


Cloze-Fragen sind leistungsfähig, aber **eine kleine Programmiersprache mit strikter Syntax** – Satzzeichen (`~`, `=`, `#`, `%`, `:`, `{`, `}`) dürfen nicht variiert oder „verbessert" werden. Übernimm die Muster unten exakt, ändere nur die Inhalte. **Kommt eines dieser Zeichen (oder `\`) als tatsächlicher Inhalt in einem Antworttext vor** (z. B. `{` und `}` in einer LaTeX-Formel wie `\(\frac{1}{6 \cdot 10^{23}}\)`), MUSS es escaped werden, sonst verwechselt Moodles Cloze-Parser den Inhalt mit der Feld-Syntax: erst `\` → `\\`, dann `{` → `\{`, `}` → `\}`, `~` → `\~`, `=` → `\=`, `#` → `\#` (Reihenfolge beachten, sonst werden neu eingefügte Backslashes selbst nochmal escaped).

Cloze eignet sich besonders für **Zufallsfragen**: Alle Fragen einer Kategorie werden in Moodle als zufälliger Fragenpool genutzt (siehe „Zufallsfragen" am Ende). Empfehlung: mind. 15–20 Fragen pro Kategorie, damit Abschreiben erschwert wird. In einem Zufallspool brauchen alle Fragen denselben Anforderungsbereich, denselben Typ und dieselbe Schwierigkeit — sonst hängt die Note vom Losglück ab.

### Format-Übersicht (Kürzel)

**Kurzantwort:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| SA | SHORTANSWER | Groß-/Kleinschreibung ignoriert |
| SAC | SHORTANSWER_C | Groß-/Kleinschreibung beachtet |

**Numerisch:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| NUM | NUMERICAL | Numerische Eingabe (optional Toleranz) |

**Dropdown:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| MC | MULTICHOICE | Dropdown, unsortiert |
| MCS | MULTICHOICE_S | Dropdown, gemischt/shuffled |

**Checkboxen vertikal:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| MR | MULTIRESPONSE | vertikal, unsortiert |
| MRS | MULTIRESPONSE_S | vertikal, gemischt |

**Checkboxen horizontal:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| MRH | MULTIRESPONSE_H | horizontal, unsortiert |
| MRHS | MULTIRESPONSE_HS | horizontal, gemischt |

**Radiobuttons vertikal:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| MCV | MULTICHOICE_V | vertikal, unsortiert |
| MCVS | MULTICHOICE_VS | vertikal, gemischt |

**Radiobuttons horizontal:**

| Kürzel | Typ | Beschreibung |
|---|---|---|
| MCH | MULTICHOICE_H | horizontal, unsortiert |
| MCHS | MULTICHOICE_HS | horizontal, gemischt |

„S" = Shuffled = Antworten werden bei jedem Teststart neu gemischt. **Für Zufallsfragen immer die S-Variante verwenden.**

### Grundsyntax

`{Punkte:TYP:Optionen}` — `=` markiert die richtige Antwort (100%), `~` trennt Optionen, `%XX%` setzt einen expliziten Prozentwert, `#` leitet Feedback zur Option ein. **Prozentwerte immer mit Punkt, nie mit Komma** (siehe „KRITISCHE Bewertungsregeln", Regel 8).

### Kurzantwort im Text (SA / SAC)

`SHORTANSWER` (kurz `SA`) vergleicht **ohne** Rücksicht auf Groß- und
Kleinschreibung, `SHORTANSWER_C` (`SAC`) **mit**. Daraus folgt:

- `SA` bei allgemeinen Begriffen und Vokabeln.
- `SAC`, wenn die Schreibweise fachlich zählt — etwa bei Formeln oder
  Kürzeln, bei denen Großbuchstaben Bedeutung tragen.
- **Einmal pro Datei oder Kategorie festlegen und durchhalten.**
- Bei `SA` **niemals** eigene Einträge für abweichende Groß- und
  Kleinschreibung anlegen: sie sind wirkungslos, weil `SA` ohnehin nicht
  unterscheidet. Nur bei `SAC` sinnvoll.

Zwei Aufgabenformate:

- **Zuordnung:** `Begriff = {1:SHORTANSWER:~=Antwort~%80%Variante}`
- **Textzusammenhang:** `Der {1:SHORTANSWER:~=Löwe~%75%Löwee} ist der
  König der Savanne.`

Ein Feld mit gestaffelten Varianten (hier `SAC`, weil die Großschreibung
zählen soll). Welcher Prozentwert wofür vergeben wird, entscheidet der
Bewertungsmaßstab, nicht diese Datei:

```
{1:SHORTANSWER_C:
  ~=Becherglas
  ~%90%becherglas
  ~%75%Becherglaz~%75%Becherglaas~%75%Bechergals
  ~%50%Becher Gläser
  ~%25%Becherg*~%25%Becher
  ~%0.01%Messbecher}
```

Der Stern `*` ist ein Platzhalter für beliebige Zeichen und trifft breit —
solche Einträge gehören auf eine niedrige Stufe, sonst schlucken sie
Antworten, die eigentlich mehr wert wären.

**Mehrere Lücken in einem Satz** sind erlaubt:

```
Der {1:SHORTANSWER:~=Löwe~%75%Löwee} ist der König der Savanne und
lebt in {1:SHORTANSWER:~=Afrika~%75%Affrika}.
```

### Multiple-Choice-Familie im Text (MC/MCS/MR/MRS/MRH/MRHS/MCV/MCVS/MCH/MCHS)

**Auswahl des Untertyps nach Optionslänge:** kurze Optionen (1–3 Wörter) → horizontal (H-Varianten); lange Optionen (4+ Wörter) → vertikal; mehrere richtige Antworten → MR-Familie; Lückentext im Satz → MC/MCS (Dropdown).

**Radiobuttons/Dropdown (genau eine richtige Antwort) – Bewertungslogik:**
- Kein Punktabzug (Standard): falsche Antworten `~%0%`
  ```
  {1:MCVS:=RichtigeAntwort~%0%Falsch1~%0%Falsch2~%0%Falsch3~%0%Falsch4}
  ```
- Punktabzug (z. B. 50%): falsche Antworten `~%-50%`, und im Fragetext nach einer Leerzeile unter der Lücke der Hinweis „Es gibt Punktabzug bei falscher Auswahl." ergänzen. Bei anderem Prozentwert entsprechend `~%-XX%`.

**Checkboxen (mehrere richtige Antworten möglich) – Bewertungsformel:** 100 ÷ Anzahl richtiger Antworten = % je richtiger Antwort. Falsche Antworten `~%-50%`.

| Richtige von 5 | % je richtiger Antwort |
|---|---|
| 1 | 100 (`~=`) |
| 2 | 50 |
| 3 | 33.33 |
| 4 | 25 |
| 5 | 20 |

Beispiele:
```
1 von 5: {1:MRS:~=Richtig1~%-50%Falsch1~%-50%Falsch2~%-50%Falsch3~%-50%Falsch4}
2 von 5: {1:MRS:~%50%Richtig1~%50%Richtig2~%-50%Falsch1~%-50%Falsch2~%-50%Falsch3}
3 von 5: {1:MRS:~%33.33%Richtig1~%33.33%Richtig2~%33.33%Richtig3~%-50%Falsch1~%-50%Falsch2}
4 von 5: {1:MRS:~%25%Richtig1~%25%Richtig2~%25%Richtig3~%25%Richtig4~%-50%Falsch1}
5 von 5: {1:MRS:~%20%Richtig1~%20%Richtig2~%20%Richtig3~%20%Richtig4~%20%Richtig5}
```

Wenn die Anzahl richtiger Antworten je Frage variieren soll: **vorher** einen Verteilungsplan festlegen und zur Bestätigung zeigen (z. B. F1→1, F2→3, F3→2 richtige), damit nicht zufällig immer dieselbe Anzahl verwendet wird (auch nicht zweimal hintereinander).

**Feedback pro Option** wird mit `#` angehängt: `=Antwort#Feedbacktext`.

XML-Beispiele:
```xml
<!-- MCVS: 1 richtige Antwort, kein Punktabzug -->
<question type="cloze">
  <name><text>MC_Thema_Begriff_001</text></name>
  <questiontext format="html">
    <text><![CDATA[Die gesetzgebende Gewalt in Deutschland wird ausgeübt durch
      {1:MCVS:=den Bundestag#Richtig!
             ~%0%die Bundesregierung#Falsch – Exekutive.
             ~%0%das Bundesverfassungsgericht#Falsch – Judikative.
             ~%0%den Bundespräsidenten#Falsch.
             ~%0%den Bundesrat#Teilweise falsch.}.
    ]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[Der Bundestag ist die gesetzgebende Gewalt in Deutschland.]]></text>
  </generalfeedback>
</question>

<!-- MRS: 2 richtige Antworten, gemischt -->
<question type="cloze">
  <name><text>MC_Thema_Begriff_002</text></name>
  <questiontext format="html">
    <text><![CDATA[Welche Organe gehören zur Legislative in Deutschland?
      {1:MRS:~%50%den Bundestag#Richtig!
            ~%50%den Bundesrat#Richtig!
            ~%-50%die Bundesregierung#Falsch – Exekutive.
            ~%-50%das Bundesverfassungsgericht#Falsch – Judikative.
            ~%-50%den Bundespräsidenten#Falsch.}.
    ]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[Die Legislative besteht aus Bundestag und Bundesrat.]]></text>
  </generalfeedback>
</question>

<!-- MCS: 1 richtige Antwort, 100% Punktabzug -->
<question type="cloze">
  <name><text>MC_Werkstoffe_Reaktionsprodukt_001</text></name>
  <questiontext format="html">
    <text><![CDATA[Welches ist das Produkt der Reaktion von CaO mit H₂O?
      {1:MCS:=Ca(OH)₂#Richtig!
            ~%-100%CaCO₃#Falsch.
            ~%-100%H₂O#Falsch.
            ~%-100%CaCl₂#Falsch.
            ~%-100%Mg#Falsch.}

    Hinweis: Es gibt Punktabzug bei falscher Auswahl.
    ]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[CaO + H₂O ergibt Ca(OH)₂ (gelöschter Kalk).]]></text>
  </generalfeedback>
</question>
```

### Numerisch im Text (NUM)

Wann sinnvoll: Naturwissenschaften (Siedepunkt, pH-Wert), Mathematik (Berechnungsergebnisse), Messwerte/Normwerte, Schätzfragen.

**Achtung:** Moodle nutzt in der XML-Syntax den **Punkt** als Dezimaltrennzeichen, nicht das Komma.

Syntax: `{1:NUMERICAL:~=Wert:Toleranz}`

| Aufgabentyp | Toleranz-Faustregel |
|---|---|
| Faktenwissen (z. B. Siedepunkt) | 0 (exakt) |
| Messwerte/Normwerte | ca. 5% des Wertes |
| Berechnungsaufgaben | 0,5 |
| Schätzfragen | 5–10% des Wertes |

Beispiele:
```
{1:NUMERICAL:~=100:0}     → exakt 100
{1:NUMERICAL:~=37:0.5}    → 37 ± 0,5
{1:NUMERICAL:~=9.81:0.1}  → 9,81 ± 0,1
```

```xml
<question type="cloze">
  <name><text>NUM_Werkstoffe_Siedepunkt_001</text></name>
  <questiontext format="html">
    <text><![CDATA[Wasser siedet bei Normaldruck bei {1:NUMERICAL:~=100:0} °C.]]></text>
  </questiontext>
  <generalfeedback format="html">
    <text><![CDATA[Der Siedepunkt von Wasser liegt bei Normaldruck exakt bei 100°C.]]></text>
  </generalfeedback>
</question>
```

### Cloze-Namensschema

`[Typ]_[Thema]_[Inhalt]_[Nr]`, z. B. `SA_Tiere_Löwe_001`, `SAC_Labor_Becherglas_001`, `MC_Fotosynthese_Reaktionsgleichung_001`, `NUM_Werkstoffe_Siedepunkt_001`.

### Vollständiges Cloze-Datei-Gerüst

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>

  <!-- Erstellt mit dem Moodle-Tests-Skill, basierend auf
       Moodle_XML_MegaPrompt_v3.0 (bildungssprit.de, CC BY-SA 4.0) und
       dem Cloze-Formenkanon von A. Spielhoff (CC BY-SA 4.0) -->

  <question type="category">
    <category><text>$course$/[Thema]</text></category>
  </question>

  <question type="cloze">
    <name><text>[Typ]_[Thema]_[Inhalt]_001</text></name>
    <questiontext format="html">
      <text><![CDATA[Aufgabenstellung: [Frage mit eingebetteter Lücke]]]></text>
    </questiontext>
    <generalfeedback format="html"><text></text></generalfeedback>
  </question>

  <!-- weitere <question type="cloze">-Blöcke -->

</quiz>
```

Die einfache Cloze-Frage (ohne generalfeedback/Zusatzfelder nötig) braucht nicht `defaultgrade`/`penalty` explizit gesetzt – Moodle berechnet die Punktzahl bei Cloze aus der Anzahl der Lücken. Bei mehreren Lücken in einer Frage: `{1:...}`, `{2:...}` usw. für unabhängige Bepunktung je Lücke.

---

