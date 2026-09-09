# Manifest pruefen, Panel-Layout

Begleitdatei zu `1-chrome-mv3`.

## Manifest vor der Fertigmeldung mit Chrome prüfen
`json.load()` prüft nur, ob die Datei JSON ist — nicht, ob Chrome sie annimmt. Genau diese Lücke
hat drei kaputte Fassungen bis auf GitHub durchgelassen.

```bash
CH=/opt/pw-browsers/chromium-*/chrome-linux/chrome
$CH --no-sandbox --pack-extension=/pfad/zur/erweiterung
# CRX entstanden -> gueltig;  kein CRX -> stderr nennt das Feld, wie im Chrome-Dialog
```

⚠️ **Die konkrete Falle:** In `web_accessible_resources[].matches` erlaubt Chrome **nur Muster
mit dem Pfad `/*`** — also `https://*/*`, **nicht** `*://*/*mod/quiz/report.php*`. Der Abschnitt
sagt nur, welche Herkunft eine Ressource laden darf; gefiltert wird über
`content_scripts.matches`. Dort ist das führende `*` im Pfad genau richtig — nicht verwechseln.

## Panel-Layout
**Eingabefelder stehen UNTER ihrer Beschriftung, nie daneben, und füllen die Panelbreite.** Ein
`<textarea>` ist von Haus aus inline und stellt sich neben den Beschriftungstext; bei 400 px
Panelbreite bleibt ein Stummel von drei Wörtern. Sammelregel in der CSS-Datei
(`display:block; width:100%; box-sizing:border-box`) statt Einzelregeln — für `<input>` fehlt sie
noch. Verwandt: Fortschritt und Protokoll gehören **über** die Knöpfe, sonst laufen sie außerhalb
des Sichtfelds ab und die Erweiterung wirkt tot.

## innerText taugt nicht zum Zerlegen von HTML (04.09.2026)

Wer fremdes HTML einliest — eine Schülerabgabe, ein Feldinhalt — legt es üblicherweise in
ein `document.createElement('div')`. **Dieses Element hängt nicht im Dokument, und dann
liefert `innerText` genau dasselbe wie `textContent`: ohne Zeilenumbrüche.** Erst ein
gerendertes Element setzt zwischen Blöcken ein `\n`.

Das erzeugt einen **längenabhängigen** Fehler, der lange unentdeckt bleibt: Ein Parser, der
„erste Zeile = Überschrift" über `text.split('\n')[0]` bestimmt, hält bei kurzem Inhalt den
ganzen Block für die Überschrift und verliert den Text darunter — bei langem Inhalt greift
dagegen eine Längenprüfung und alles wirkt richtig.

**Regel: nie über Zeilenumbrüche zerlegen, sondern über die Struktur.** Rekursiv absteigen;
ein Element mit Block-Kindern (`DIV P H1-6 UL OL LI TABLE TBODY TR TD TH BLOCKQUOTE SECTION
ARTICLE PRE`) ist ein Behälter, nur ein Blatt-Block kann Überschrift oder Textabsatz sein.
Zum Vergleichen `textContent` mit `.replace(/\s+/g,' ').trim()` verwenden.

Wird doch Text mit Absätzen gebraucht, die Blockenden vorher selbst zu Umbrüchen machen:

```js
d.innerHTML = html.replace(/<br\s*\/?>/gi, '\n')
                  .replace(/<\/(p|div|h[1-6]|li|tr|blockquote)>/gi, '</$1>\n');
return d.textContent.replace(/\n{3,}/g, '\n\n').trim();
```

## Versionsnummern: führende Nullen verschwinden (04.09.2026)

Chrome liest die Teile einer `version` als **ganze Zahlen**, nicht als Text. Das hat zwei
Folgen, die sich widersprechen können:

- Zweistellig weiterzählen funktioniert über 9 hinaus: **2.30 ist größer als 2.9**, weil 30
  größer als 9 ist. Kein Problem.
- Eine **führende Null verschwindet**: `3.01` und `3.1` sind für Chrome **dieselbe
  Version**. Wer nach 3.0 eine Kleinigkeit als „3.01" veröffentlicht, springt in Wahrheit
  auf 3.1 — und die nächste echte 3.1 ist dann keine Erhöhung mehr. `3.02` wäre 3.2 und
  damit größer als 3.1, obwohl es „nach 3.01" aussieht.

Chrome nimmt alle diese Schreibweisen an (mit `--pack-extension` geprüft) — sie bedeuten
nur nicht, was sie suggerieren. Deshalb: **nie eine führende Null.** Wer Platz für
Korrekturfassungen braucht, hängt eine dritte Stelle an (`3.0.1`, kleiner als `3.1`).
