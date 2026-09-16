---
name: 1-webext-robustheit
description: "Eine Erweiterung robust gegen eine fremde, selbst nicht kontrollierte Weboberfläche machen (Moodle & Co.): Versionsdisziplin, Portabilität, robuste Selektorwahl, Submit-Reload-Muster, MV3-Laufzeitkonventionen, KI-Form-vs-Prompt-Regel, Kontextverlust nach dem Neuladen. IMMER verwenden bei „Selektor funktioniert nicht\", „Extension context invalidated\", „Seite lädt neu\", „Manifest V3\", „Versionsnummer der Erweiterung\", „content.js\", „robuste Erweiterung\" — auch ohne Skill-Namen."
---

# Browsererweiterungen robust gegen fremde Weboberflächen

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — reine Technik, frei weiterzugeben

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.

> **Verwandte Skill.** Wie das Projekt selbst angelegt, für Chrome/Firefox/Edge gebaut und als
> ZIP verpackt wird, steht in `1-browser-wxt`. Diese Skill hier gilt unverändert, ob die
> Erweiterung von Hand oder mit WXT gebaut wird — sie beschreibt, was im Content Script selbst
> robust gemacht wird.

> **Quelle.** Der Kern dieser Skill (Versionsdisziplin, Selektor-Rangfolge, Kontextverlust)
> stammt aus eigener Praxis mit den Moodle-Erweiterungen. Am 16.09.2026 gegen den fremden
> GitHub-Skill [`xenitV1/claude-code-maestro`](https://github.com/xenitV1/claude-code-maestro/blob/main/skills/browser-extension/SKILL.md)
> (**MIT-Lizenz**) abgeglichen — von dort übernommen: die Icon-Größenliste in Abschnitt 4 und
> die Erinnerung an `web_accessible_resources`. Diese Skill selbst bleibt unter eigener
> CC-BY-4.0-Lizenz.

> **Begleitdateien-Übersicht**
>
> | Vorhaben | Referenz |
> |---|---|
> | Ein Knopf löst ein Formular aus, die Seite lädt neu | `server-submits.md` |
> | Die Erweiterung erzeugt einen Prompt für ein KI-Werkzeug | `ki-prompts.md` |
> | Konkrete Selektoren und URLs in Moodle | `moodle-selektoren.md` |
> | Manifest vor der Fertigmeldung prüfen, Panel-Layout | `pruefen-und-panel.md` |

Diese Skill beschreibt, wie eine Erweiterung gebaut wird, die auf einer
Weboberfläche arbeitet, die man selbst nicht kontrolliert. Der schwierige
Teil daran ist nicht das Manifest, sondern die Frage, woran man sich im
fremden HTML festhält, ohne beim nächsten Update abzureißen. Ob das Gerüst
drumherum von Hand oder mit WXT gebaut ist (`1-browser-wxt`), ändert daran
nichts.

## 1 · Versionsdisziplin

**Die kanonische Quelle der Versionsnummer ist das, was der Browser tatsächlich lädt.**
Bei einer von Hand gebauten Erweiterung ist das `manifest.json`; bei einer mit WXT gebauten
ist das `wxt.config.ts` (Feld `manifest.version`) bzw. `package.json` — nie eine README oder
Projektdoku. Weichen sie ab, wird die README nachgezogen, nie umgekehrt.

**Immer drei Stellen: `x.y.z`.** Auch dann, wenn die letzte Stelle 0 ist —
`2.7` wird als `2.7.0` geschrieben. Eine einheitliche Form macht auf einen
Blick vergleichbar, welche Fassung neuer ist, und ein zweistelliger
Ausreißer fällt sonst durch jede Sortierung. Chrome erlaubt bis zu vier
Zahlen; drei sind das Maß.

Was welche Stelle bedeutet:

| Stelle | Wofür | Beispiel |
|---|---|---|
| **x** — vorne | Echte neue Fassung: großer Umbau, geänderter Arbeitsablauf, neues Bedienkonzept | Grader 2.30 → 3.0.0 |
| **y** — Mitte | Die Erweiterung kann etwas, was sie vorher nicht konnte | 1.4.2 → 1.5.0 |
| **z** — hinten | Laufende Anpassungen: Fehlerbehebung, Feinschliff, Text, Symbol, Doku | 1.5.6 → 1.5.7 |

Die ganz große Zahl wird also selten und bewusst vergeben; alles, was im
Alltag anfällt, läuft hinten mit.

**Die mittlere Stelle streng nehmen.** Sie steigt nur, wenn die Erweiterung
etwas Neues **kann** — nicht, wenn ein bestehender Ablauf besser, schöner
oder verständlicher wird. Ein neuer Reiter, ein neues Feld im JSON, ein
zweiter Arbeitsweg: ja. Eine bessere Fehlermeldung, ein umformulierter
Prompt, eine Fortschrittsanzeige, ein neues Layout: nein, das gehört nach
hinten. Im Zweifel die hintere Stelle — sie kostet nichts, während eine zu
schnell gedrehte Mitte den Abstand zwischen den Erweiterungen unlesbar
macht.

**Die Nummer gehört zum Veröffentlichen, nicht zu jeder Änderung.** Alles,
was zwischen zwei Commits entsteht, ist ein Zwischenstand und teilt sich
**eine** neue Nummer. Drei Verbesserungen an einem Vormittag, danach ein
Commit — das ist ein Schritt, nicht drei. Genau so ist der Coach an einem
Morgen von 1.1.1 auf 1.4.0 gesprungen, wo 1.2.1 richtig gewesen wäre: jede
Sitzung wurde wie ein eigenes Release behandelt.

Das gilt für die **mittlere** Stelle. Die hintere darf beim Entwickeln
mitlaufen: Wer eine Fassung zum Testen in den Chrome-Ordner kopiert (oder,
mit WXT, per `wxt`/`wxt -b firefox` startet), muss nach „↺ neu laden" an
der Nummer sehen können, dass sie aktiv ist.

**Eine veröffentlichte Nummer wird nie zurückgenommen.** Ist sie committet
und gepusht, bleibt sie stehen, auch wenn sie zu groß gewählt war. Eine
*niedrigere* Nummer sieht nach dem Neuladen aus wie die alte Fassung —
genau die Unsicherheit, die die Versionsanzeige beseitigen soll. Lieber den
schiefen Sprung stehen lassen und ab da sauber weiterzählen.

**Bei jeder Codeänderung die Version hochzählen.** Nach dem Neuladen unter
`chrome://extensions/` ist die Nummer der einzige Beleg, dass wirklich die
neue Fassung läuft. Eine vergessene Erhöhung kostet eine halbe Stunde
Fehlersuche an der falschen Stelle.

**Die Nummer gehört sichtbar in die Oberfläche** — in die Kopfzeile des
Panels, gelesen aus dem Manifest (siehe Abschnitt 4). Dann beantwortet die
Erweiterung die Frage „ist das schon die neue Fassung?" selbst, ohne Umweg
über `chrome://extensions/`.

**Die Version steht an vier Stellen** und muss überall gleich sein:
Manifest-Quelle (`manifest.json` bzw. `wxt.config.ts`), README-Kopf, README-Fuß,
Kommentarkopf der `content.js`/`content.ts`. Der Änderungsabschnitt der README bekommt
zusätzlich einen Eintrag. Liegen mehrere Erweiterungen in einem Repo, gehört die
Übersichtstabelle des Haupt-README dazu.

**Bei einem Release die Versionstabelle für ALLE Erweiterungen des Repos
gegen die Manifeste prüfen**, nicht nur für die gerade geänderte. Wer eine
Erweiterung zwischendurch weiterentwickelt und die Tabelle vergisst, merkt
es nie — die Abweichung ist still und fällt erst auf, wenn jemand die
falsche Fassung herunterlädt. Belegt: zwei von fünf Zeilen standen zwei
bzw. drei Fassungen zurück. Ein Dreizeiler, der jedes `manifest.json` liest
und mit der Tabelle vergleicht, findet das in Sekunden.

**Ordnername ohne Versionsnummer.** Chrome lädt entpackte Erweiterungen
fest aus dem Pfad. Steht die Version im Ordnernamen, muss bei jedem Update
die Erweiterung neu hinzugefügt statt nur neu geladen werden.

**Vor Doku-Änderungen die Originaldateien lesen**, nicht aus dem Gedächtnis
oder aus älteren Zusammenfassungen arbeiten.

**Backup vor größeren Umbauten** — die alte Fassung **außerhalb** des
Erweiterungsordners ablegen. Innerhalb würde sie mit weitergegeben.

## 2 · Portabilität: die Erweiterung läuft überall

Eine Erweiterung, die nur auf der eigenen Installation läuft, kann man
niemandem geben. Vier Regeln machen den Unterschied.

**Kein fester Host im Manifest bzw. in `matches`.**

```json
"matches": ["https://schule.example.org/mod/quiz/*"]   // falsch
"matches": ["*://*/*mod/quiz/report.php*"]             // richtig
```

Das führende `*` vor dem Pfad ist wichtig: viele Installationen liegen in
einem Unterverzeichnis, nicht auf der Domainwurzel.

**Keine URL ab der Domainwurzel bauen.** `location.origin` verliert das
Unterverzeichnis. Stattdessen die Anwendungswurzel aus `location.pathname`
ableiten, indem das erste bekannte Pfadsegment gesucht wird, und relative
Links mit `new URL(href, location.href)` auflösen.

**Ein breites Muster braucht eine Gegenprobe im Code.** Wer auf `*://*/*`
lauscht, landet auf jeder Website. Das Content Script prüft deshalb vor dem
Einbau, ob die Seite wirklich die erwartete Anwendung ist — an einem
Merkmal, das dort sicher vorhanden ist.

**Sprachabhängige Texte nur als zweite Ebene.** Sichtbarer Text ist der
letzte Anker, nicht der erste, und dann immer als Liste mehrerer Sprachen
mit einem Rückfall auf „nimm den einzigen Knopf, der passt".

## 3 · Selektoren robust wählen

**Nie an Utility-Klassen eines CSS-Frameworks hängen.**
`fieldset.w-100.m-0.p-0.border-0` bricht bei jedem Theme-Update. Solche
Selektoren sind die häufigste Ursache stiller Ausfälle.

Rangfolge, von stabil nach brüchig:

1. **Feldnamen** (`input[name$="-mark"]`) — von der Anwendung stabil und
   sprachunabhängig vergeben.
2. **IDs**, die aus dem Formularnamen entstehen.
3. **Formular-Aktion** als Teilzeichenkette (`form[action*="/grade/edit/"]`)
   — überlebt auch Unterverzeichnis-Installationen.
4. **Sichtbarer Text** in Legenden oder Labels — sprachabhängig, immer
   mehrsprachig führen.
5. **CSS-Klassen** nur als letzte Rückfallebene.

Beim Umstieg die alte Erkennung als Rückfallebene behalten, nicht ersatzlos
streichen.

**Ein Formular, das die Seite per JavaScript nachbaut, ist nicht da, wenn
man zu früh fragt.** Manche Oberflächen rendern ihre Felder erst nach
`document_idle`. Ein Selektor, der „nicht funktioniert", ist dann in
Wahrheit richtig und nur zu früh aufgerufen — belegt an einem Feld, das
mehrfach vergeblich gesucht wurde, obwohl der Selektor stimmte. Deshalb auf
das Element warten (kurzer Poll mit Zeitgrenze, etwa 20 Sekunden) statt
einmal abzufragen und aufzugeben.

## 4 · Laufzeitkonventionen (Manifest V3)

- **Icons in 16/32/48/128 px**, sonst zeigt der Browser das graue Puzzleteil —
  bei einer Weitergabe wirkt das unfertig. Aus einer quadratischen Vorlage
  ab 512 px die vier Größen rechnen. (Mit WXT: einfach unter `public/`
  ablegen, siehe `1-browser-wxt`.)
- Hat die Erweiterung einen Werkzeugleisten-Knopf, gehört dieselbe
  Icon-Liste zusätzlich unter `action.default_icon`.
- **`web_accessible_resources`** braucht nur, wer ein Icon **in die Seite**
  lädt (`chrome.runtime.getURL(...)`/`browser.runtime.getURL(...)`). Der Pfad muss exakt zur
  `icons/`-Struktur passen. **Sein `matches`-Feld ist strenger als das der
  Content Scripts** — dort sind nur bestimmte Musterformen erlaubt; die
  genaue Falle und der Weg, sie vor der Fertigmeldung zu erkennen, stehen
  in `pruefen-und-panel.md`.
- **`chrome.storage.local`/`browser.storage.local` braucht `"permissions": ["storage"]`.** Fehlt
  das, scheitert der Zugriff **stumm** — kein Fehler, keine Meldung.
- **Content Scripts kommen nicht an das JavaScript der Seite heran.** Für
  den Zugriff auf Objekte im Seitenkontext:
  `chrome.scripting.executeScript` mit `world: 'MAIN'` über den Service
  Worker.
- **Die angezeigte Version aus dem Manifest lesen**
  (`chrome.runtime.getManifest().version`), nie fest eintragen — dann zeigt
  die Oberfläche immer die Fassung, die wirklich läuft. Der Aufruf gehört
  abgesichert (`chrome.runtime.getManifest ? … : ''`), damit die Kopfzeile
  auch dann steht, wenn der Kontext einmal fehlt.
- **Mehrere eigene Erweiterungen auf derselben Seite** grenzt man über
  URL-Parameter voneinander ab, nicht über Inhalte der Seite. Schließen
  sich die Bedingungen gegenseitig aus — jede Erweiterung steigt aus, wenn
  der Parameter der anderen gesetzt ist —, dürfen alle dieselbe
  Panel-Position benutzen; erst wenn zwei gleichzeitig erscheinen können,
  braucht es versetzte, unterschiedlich gefärbte Knöpfe. Die
  Ausstiegsprüfungen gehören spiegelbildlich in **beide** Erweiterungen —
  eine einseitige Prüfung lässt die andere weiter überall erscheinen.
- **Möglichst enge `matches`.** Ein `https://*/*` löst beim Installieren
  die Warnung „alle Daten auf allen Websites lesen und ändern" aus. Das
  schreckt jeden ab, dem man die Erweiterung geben will.

## 5 · Wo die Form hingehört: Plugin statt Prompt

Erzeugt die Erweiterung Texte, die ein Sprachmodell füllt, gilt: **die KI
liefert den Inhalt, die Form baut das Plugin.** Überschriften, Fettung,
Unterstreichung, Absätze, Reihenfolge, feste Zusatzzeilen — all das setzt
kein Prompt zuverlässig durch; es kommt viermal richtig und beim fünften
Mal als Fließtext. Die KI bekommt deshalb **Felder** vorgegeben und füllt
nur sie; das Plugin setzt daraus das fertige HTML zusammen und lässt leere
Felder weg. Der Prompt sagt ausdrücklich, dass in die Felder weder
Formatierungszeichen noch Zeilenumbrüche gehören.

Was die Erweiterung ohnehin weiß, lässt sie die KI gar nicht erst
schreiben: Steht die Musterlösung schon in den ausgelesenen Daten, setzt
sie das Plugin selbst ein — das kostet keine Token, kann nicht abweichen
und ist wörtlich das, was hinterlegt wurde. Mehr dazu in `ki-prompts.md`.

**Hängt die Erweiterung feste Zusatzzeilen an, muss sie erkennen, ob der
Inhalt Klartext oder Auszeichnungssprache ist.** Ein Hinweis, der als
Klartext an HTML gehängt wird, klebt in der Ansicht an den letzten Satz;
umgekehrt steht HTML in einem Klartextfeld als sichtbarer Quelltext. Also
am Inhalt prüfen (`/<(p|br|div|strong|em)\b/i`) und den Zusatz in
derselben Form anhängen.

## 6 · Kontextverlust nach dem Neuladen der Erweiterung

**„Extension context invalidated" ist kein Codefehler.** Wird eine
Erweiterung neu geladen oder neu installiert, während eine passende Seite
offen ist, läuft dort das **alte** Content Script weiter — aber ohne
Verbindung zur Erweiterung. Jeder `chrome.*`/`browser.*`-Aufruf wirft dann diesen
Fehler, und der Benutzer sieht eine Meldung, mit der niemand etwas anfangen
kann. Abhilfe ist immer dieselbe: die Seite neu laden. Das gilt beim
WXT-Dev-Server (`1-browser-wxt`) genauso wie bei der von Hand entpackten
Erweiterung.

Das soll die Erweiterung selbst sagen, nicht der Support:

```js
function kontextGueltig() {
  try { return !!(chrome && chrome.runtime && chrome.runtime.id); }
  catch (e) { return false; }
}
```

- Beim Aufbau der Oberfläche **und** vor jeder Aktion, die `chrome.*`
  benutzt, einmal prüfen und im Klartext sagen, was zu tun ist.
- Alle Storage-Aufrufe in `try/catch` kapseln und bei totem Kontext leer
  zurückgeben, statt die Aktion mit einem Ausnahmefehler abzubrechen.
- Beim Abfangen auch auf `message port closed` und
  `receiving end does not exist` prüfen — dieselbe Ursache, andere
  Formulierung.

Wer viel entwickelt, läuft ständig hinein, weil Neuladen und Testen sich
abwechseln. Ohne diesen Abfang sucht man den Fehler im eigenen Code.

## 7 · Abschluss-Checkliste

- [ ] `node --check` über jede JavaScript-Datei (bzw. `tsc --noEmit` bei TypeScript/WXT)
- [ ] Manifest-Quelle (`manifest.json` bzw. `wxt.config.ts`) gültig — bei WXT über
      `web-ext lint`, sonst per `--pack-extension`, siehe `pruefen-und-panel.md`
- [ ] Version dreistellig (`x.y.z`), Stelle passend zur Größe der Änderung
      gewählt, an allen vier Stellen gleich
- [ ] Mittlere Stelle nur gedreht, wenn die Erweiterung etwas Neues kann —
      und höchstens einmal je Veröffentlichung
- [ ] Versionstabelle des Haupt-README gegen **jedes** Manifest geprüft
- [ ] Jede im Manifest genannte Datei existiert wirklich
- [ ] Kein fester Host, keine URL ab der Domainwurzel
- [ ] Selektoren gegen die aktuelle Oberfläche geprüft, bei nachgeladenen
      Formularen mit Warteschleife statt Einmalabfrage
- [ ] Toter Erweiterungskontext wird abgefangen und im Klartext gemeldet
- [ ] Logik an einem echten Fall durchgespielt, nicht nur gelesen
- [ ] Lizenzdatei vorhanden, keine personenbezogenen Daten im Repo
