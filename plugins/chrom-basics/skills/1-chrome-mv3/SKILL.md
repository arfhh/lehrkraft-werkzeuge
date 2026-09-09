---
name: 1-chrome-mv3
description: "Chrome-Erweiterungen nach Manifest V3 bauen und warten, die auf einer fremden Weboberfläche arbeiten: Versionsdisziplin und wo die Versionsnummer überall stehen muss, die vier Portabilitätsregeln (kein fester Host im Manifest, keine URL ab der Domainwurzel, Gegenprobe im Code bei breitem Muster, sprachabhängige Texte nur als Rückfallebene), die Rangfolge bei der Wahl robuster Selektoren, die Manifest-V3-Konventionen für Icons, Berechtigungen, Zugriff auf Seiten-JavaScript und enge matches, sowie eine Abschluss-Checkliste. Mit Begleitdateien für das Muster bei seitenneuladenden Submits, für Erweiterungen die KI-Prompts erzeugen, und für verifizierte Moodle-Selektoren. Rein technisch — welche konkreten Erweiterungen gepflegt und wie sie weitergegeben werden, steht in der Projekt-Skill. IMMER verwenden bei „Chrome-Erweiterung\", „manifest.json\", „content.js\", „Manifest V3\", „Content Script\", „Selektor funktioniert nicht\", „neue Version der Erweiterung\" — auch ohne Skill-Namen."
---

# Chrome-Erweiterungen nach Manifest V3

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — reine Technik, frei weiterzugeben

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.

Diese Skill beschreibt, wie eine Erweiterung gebaut wird, die auf einer
Weboberfläche arbeitet, die man selbst nicht kontrolliert. Der schwierige
Teil daran ist nicht das Manifest, sondern die Frage, woran man sich im
fremden HTML festhält, ohne beim nächsten Update abzureißen.

| Vorhaben | Referenz |
|---|---|
| Ein Knopf löst ein Formular aus, die Seite lädt neu | `server-submits.md` |
| Die Erweiterung erzeugt einen Prompt für ein KI-Werkzeug | `ki-prompts.md` |
| Konkrete Selektoren und URLs in Moodle | `moodle-selektoren.md` |

## 1 · Versionsdisziplin

**`manifest.json` ist die kanonische Quelle der Versionsnummer.** Nicht die
README, nicht eine Projektdoku. Weichen sie ab, wird die README nachgezogen
— nie umgekehrt.

**Bei jeder Codeänderung die Version hochzählen.** Nach dem Neuladen unter
`chrome://extensions/` ist die Nummer der einzige Beleg, dass wirklich die
neue Fassung läuft. Eine vergessene Erhöhung kostet eine halbe Stunde
Fehlersuche an der falschen Stelle.

**Nebensachen bekommen eine Patch-Stelle** (1.5 → 1.5.1): Symbolwechsel,
Doku, Umbenennungen. So bleiben geplante Funktionsnummern frei. Chrome
erlaubt bis zu vier Zahlen. Eine echte Funktionsänderung bekommt die
nächste Minor-Nummer.

**Die Version steht an vier Stellen** und muss überall gleich sein:
`manifest.json`, README-Kopf, README-Fuß, Kommentarkopf der `content.js`.
Der Änderungsabschnitt der README bekommt zusätzlich einen Eintrag.

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

**Kein fester Host im Manifest.**

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

## 4 · Manifest-V3-Konventionen

- **Icons in 16/32/48/128 px**, sonst zeigt Chrome das graue Puzzleteil —
  bei einer Weitergabe wirkt das unfertig. Aus einer quadratischen Vorlage
  ab 512 px die vier Größen rechnen.
- Hat die Erweiterung einen Werkzeugleisten-Knopf, gehört dieselbe
  Icon-Liste zusätzlich unter `action.default_icon`.
- **`web_accessible_resources`** braucht nur, wer ein Icon **in die Seite**
  lädt (`chrome.runtime.getURL(...)`). Der Pfad muss exakt zur
  `icons/`-Struktur passen.
- **`chrome.storage.local` braucht `"permissions": ["storage"]`.** Fehlt
  das, scheitert der Zugriff **stumm** — kein Fehler, keine Meldung.
- **Content Scripts kommen nicht an das JavaScript der Seite heran.** Für
  den Zugriff auf Objekte im Seitenkontext:
  `chrome.scripting.executeScript` mit `world: 'MAIN'` über den Service
  Worker.
- **Die angezeigte Version aus dem Manifest lesen**
  (`chrome.runtime.getManifest().version`), nie fest eintragen — dann zeigt
  die Oberfläche immer die Fassung, die wirklich läuft.
- **Mehrere eigene Erweiterungen auf derselben Seite** grenzt man über
  URL-Parameter voneinander ab, nicht über Inhalte der Seite, und über
  unterschiedlich platzierte, unterschiedlich gefärbte Knöpfe.
- **Möglichst enge `matches`.** Ein `https://*/*` löst beim Installieren
  die Warnung „alle Daten auf allen Websites lesen und ändern" aus. Das
  schreckt jeden ab, dem man die Erweiterung geben will.

## 5 · Abschluss-Checkliste

- [ ] `node --check` über jede JavaScript-Datei
- [ ] `manifest.json` als JSON geparst, nicht nur angesehen
- [ ] Version an allen vier Stellen gleich
- [ ] Jede im Manifest genannte Datei existiert wirklich
- [ ] Kein fester Host, keine URL ab der Domainwurzel
- [ ] Selektoren gegen die aktuelle Oberfläche geprüft
- [ ] Logik an einem echten Fall durchgespielt, nicht nur gelesen
- [ ] Lizenzdatei vorhanden, keine personenbezogenen Daten im Repo
