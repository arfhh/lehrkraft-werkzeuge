---
name: 1-browser-wxt
description: "WXT-basierte Cross-Browser-Erweiterungen (Chrome/Firefox/Edge) aufsetzen, bauen und als ZIP verpacken: Projektgerüst, gemeinsame Codebasis, browserspezifische Kapselung, Manifest im Code statt Handarbeit, lokales Testen je Browser, web-ext lint. IMMER verwenden bei „WXT\", „neue Erweiterung anlegen\", „Firefox-Version bauen\", „Cross-Browser\", „wxt.config.ts\", „alle Browser bauen\", „Erweiterung als ZIP\" — auch ohne Skill-Namen."
---

> **Begleitdateien.** Die unten genannten Dateien liegen im Ordner dieser
> Skill selbst — Referenztexte direkt daneben, Skripte in `scripts/`.


# Browser-Erweiterungen bauen mit WXT (Chrome/Firefox/Edge)

© 2026 A. Spielhoff — lizenziert unter CC BY 4.0

**Benötigt:** — (keine)
**Ebene:** 1 — reine Technik, frei weiterzugeben

> **Begleitdatei.** Konkrete `wxt.config.ts`-Vorlage und Befehls-Spickzettel liegen nicht in
> dieser Skill, sondern im **Werkzeug-Ordner** `1-browser-wxt/wxt-befehle-und-config.md`. Wo
> dieser Ordner liegt, sagt die Projekt-Anweisung.

> **Verwandte Skill.** Sobald die Erweiterung mit einer fremden, serverseitig gerenderten
> Oberfläche arbeitet (Moodle & Co.) — Selektor-Strategie, Submit-Reload-Muster, Kontextverlust
> nach dem Neuladen — steht das in `1-webext-robustheit`. Diese Skill hier baut nur das Gerüst;
> was im Content Script robust gegen die fremde Seite gemacht wird, steht dort.

> **Quelle.** Diese Skill entstand am 16.09.2026 aus zwei fremden GitHub-Skills, beide unter
> **MIT-Lizenz**: [`yamadashy/repomix`](https://github.com/yamadashy/repomix/blob/main/browser/.claude/skills/browser-extension-developer/SKILL.md)
> lieferte die reale WXT-Projektstruktur und die Befehle in Abschnitt 1, 5, 6, 7; von
> [`xenitV1/claude-code-maestro`](https://github.com/xenitV1/claude-code-maestro/blob/main/skills/browser-extension/SKILL.md)
> stammen allgemeine MV3-Konventionen (Icons, Berechtigungen), die hier zusätzlich mit WXT
> abgeglichen wurden — dieser Skill nutzt selbst kein WXT. Beide Quellen erlauben Nutzung und
> Bearbeitung mit Namensnennung im Quelltext der Lizenz; diese Skill selbst bleibt unter eigener
> CC-BY-4.0-Lizenz.

WXT ist ein Build-Framework für Browser-Erweiterungen: eine Codebasis, ein Befehl je Browser.
Es erspart das Hand-Manifest, kapselt Chrome/Firefox/Edge-Unterschiede und macht aus einem
Ordner mit `entrypoints/` fertige, installierbare ZIPs für jeden Zielbrowser.

## 1 · Projekt anlegen

```bash
npx wxt@latest init meine-erweiterung
cd meine-erweiterung && npm install
```

Ergebnis-Struktur:

```
meine-erweiterung/
├── entrypoints/       # background.ts, content.ts, popup/ … — je Datei ein Manifest-Eintrag
├── public/            # Icons, _locales/, alles was 1:1 mitkopiert wird
├── wxt.config.ts      # die einzige Konfigurationsdatei
└── .output/           # Build-Ergebnis, je Browser ein Unterordner (chrome-mv3, firefox-mv2 …)
```

Kein `manifest.json` von Hand pflegen — es wird bei jedem Build aus `wxt.config.ts` plus den
Entrypoints erzeugt. Wer eine bestehende Hand-MV3-Erweiterung migriert: `manifest.json`-Felder
wandern nach `wxt.config.ts` (Abschnitt 2), `content.js` wird zu `entrypoints/content.ts`
(Abschnitt 3) — die Selektor- und Robustheitsregeln selbst bleiben unverändert, siehe
`1-webext-robustheit`.

## 2 · Manifest und Berechtigungen im Code

```ts
// wxt.config.ts
import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'Meine Erweiterung',
    version: '1.0.0',
    permissions: ['storage', 'scripting'],
    host_permissions: ['*://*/*mod/quiz/report.php*'],
    browser_specific_settings: {
      gecko: { id: 'meine-erweiterung@example.org', strict_min_version: '109.0' },
    },
  },
});
```

- **Berechtigungen und `host_permissions` immer von Hand eintragen** — WXT ergänzt von sich aus
  nur `tabs`/`scripting` im Dev-Modus und `sidePanel`, wenn ein Side-Panel-Entrypoint existiert.
  Least-Privilege gilt weiter: enge `matches`/`host_permissions`, sonst löst die
  Installationswarnung „alle Daten auf allen Websites" aus.
- **Icons werden aus `public/` automatisch erkannt** (`icon-16.png`, `icon-16x16.png`,
  `icon/48.png` …) — kein Eintrag im Manifest nötig. Firefox erkennt zusätzlich
  `icon-light-*.png`/`icon-dark-*.png` für Theme-Varianten.
- **`web_accessible_resources` im MV3-Format schreiben**, WXT wandelt es für Firefox-MV2
  automatisch um.
- **`browser_specific_settings.gecko.id`** ist für die Firefox-Signierung/-Verteilung
  Pflicht, sonst lehnt Mozilla die Einreichung ab.

## 3 · Content Scripts und Hintergrund deklarativ

Statt `content_scripts` im Manifest aufzuzählen, bekommt jede Entrypoint-Datei ihre `matches`
selbst mit:

```ts
// entrypoints/content.ts
export default defineContentScript({
  matches: ['*://*/*mod/quiz/report.php*'],
  main() {
    // wie bisher: robuste Selektoren, Warteschleife, Kontextverlust-Prüfung — siehe 1-webext-robustheit
  },
});
```

```ts
// entrypoints/background.ts
export default defineBackground(() => {
  // Service-Worker-Logik
});
```

Der Dateiname im `entrypoints/`-Ordner bestimmt den Manifest-Eintrag automatisch — ein Ordner
pro Popup/Side-Panel (`entrypoints/popup/index.html`) reicht für eine eigene HTML-Oberfläche.

## 4 · Browserspezifische Unterschiede kapseln

- **`browser.*` statt `chrome.*` verwenden** — WXT liefert automatisch den
  `webextension-polyfill` (`wxt/browser`), sodass derselbe Aufruf auf Chrome, Firefox und Edge
  funktioniert. `chrome.*` läuft zwar auch unter Chrome/Edge, aber nicht unter Firefox ohne
  Polyfill.
- **Verzweigung nur wo nötig:** `import.meta.env.FIREFOX` (boolescher Browser-Check) und
  `import.meta.env.MANIFEST_VERSION` (2 oder 3) stehen zur Build-Zeit zur Verfügung — damit
  lässt sich eine Ausnahme lokal begrenzen, statt den ganzen Code zu verzweigen.
- **Standard-Manifestversion unterscheidet sich:** WXT baut **Firefox standardmäßig als MV2**,
  alle anderen Browser (Chrome, Edge) als MV3. Wer Firefox ausdrücklich auch mit MV3 bauen will
  (Firefox unterstützt das inzwischen), erzwingt das über die Build-Option `manifestVersion: 3`
  — sonst landen zwei strukturell verschiedene Manifeste in `.output/`, was beim Debuggen
  überrascht, wenn man nur den Chrome-Ordner kennt.

## 5 · Lokal testen

```bash
npx wxt              # Dev-Modus, öffnet Chrome, Datei-Überwachung + Hot-Reload
npx wxt -b firefox   # Dev-Modus, öffnet Firefox
npx wxt -b edge      # Dev-Modus für Edge (chromium-basiert, wie Chrome)
```

Hot-Reload ersetzt bei UI-Dateien (Popup, Side-Panel) das manuelle Neuladen. **Bei einem
Content Script, das auf einer fremden, bereits offenen Seite hängt (Moodle & Co.), reicht das
nicht** — die offene Seite muss trotzdem einmal neu geladen werden, sonst läuft dort weiter das
alte Script ohne Verbindung zur Erweiterung (`Extension context invalidated`, Details in
`1-webext-robustheit`).

## 6 · Alle Browser-Versionen bauen

```bash
npx wxt build -b chrome
npx wxt build -b firefox
npx wxt build -b edge
```

Als ein Durchlauf im `package.json` bündeln:

```json
"scripts": {
  "build:chrome": "wxt build -b chrome",
  "build:firefox": "wxt build -b firefox",
  "build:edge": "wxt build -b edge",
  "build-all": "npm run build:chrome && npm run build:firefox && npm run build:edge"
}
```

Ergebnis landet browsergetrennt unter `.output/chrome-mv3/`, `.output/firefox-mv2/`,
`.output/edge-mv3/`.

## 7 · Fertige ZIP-Dateien erzeugen

```bash
npx wxt zip -b chrome
npx wxt zip -b firefox
npx wxt zip -b edge
```

WXT benennt die ZIP automatisch nach Name und Version aus `wxt.config.ts`
(`<name>-<version>-chrome.zip` usw.) — die Versionsdisziplin aus `1-webext-robustheit`
(dreistellig, mittlere Stelle nur bei echtem Funktionszuwachs, nie eine veröffentlichte Nummer
zurücknehmen) gilt unverändert; die Quelle der Versionsnummer ist jetzt `wxt.config.ts` statt
eines Hand-Manifests. Firefox verlangt für `about:addons`-Installation zusätzlich eine
Signierung durch Mozilla (`web-ext sign`) oder Entwicklermodus — für den privaten/schulischen
Gebrauch reicht meist „Temporäre Erweiterung laden" bzw. die unsignierte ZIP im
Entwicklermodus.

## 8 · Manifest und Berechtigungen prüfen

Nicht eigene Audit-Skripte pflegen — der Mozilla-Standard deckt Chrome, Firefox und Edge ab:

```bash
npx web-ext lint --source-dir=.output/chrome-mv3
npx web-ext lint --source-dir=.output/firefox-mv2
```

`web-ext lint` meldet ungültige Manifestfelder, zu weite Berechtigungen, fehlende Icons und
MV2/MV3-spezifische Fallstricke — vor jeder Weitergabe laufen lassen, nicht nur `JSON.parse()`
auf das generierte Manifest anwenden (das prüft nur Syntax, nicht Gültigkeit).

## 9 · Abschluss-Checkliste

- [ ] `wxt.config.ts` enthält `permissions`/`host_permissions` eng gefasst (Least Privilege)
- [ ] `browser_specific_settings.gecko.id` gesetzt, wenn Firefox zu den Zielen gehört
- [ ] Alle drei Browser gebaut (`build-all`) und **einmal tatsächlich entpackt geladen**, nicht
      nur kompiliert
- [ ] `web-ext lint` für jeden `.output/<browser>`-Ordner ohne Fehler
- [ ] ZIPs mit `wxt zip -b <browser>` erzeugt, Versionsnummer stimmt mit `wxt.config.ts` überein
- [ ] Content Scripts nutzen `browser.*` (Polyfill), nicht hart `chrome.*`, wenn Firefox Ziel ist
- [ ] Selektor-/Robustheitsregeln aus `1-webext-robustheit` angewendet, nicht nur das Gerüst
      übernommen
