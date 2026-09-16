# WXT: Befehle und Config-Vorlage

Begleitdatei zu `1-browser-wxt`.

## wxt.config.ts (Vorlage)

```ts
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
  // Firefox standardmaessig MV2 -- explizit MV3 erzwingen, falls gewuenscht:
  // manifestVersion: 3,
});
```

## package.json — Skript-Spickzettel

```json
{
  "scripts": {
    "dev": "wxt",
    "dev:firefox": "wxt -b firefox",
    "dev:edge": "wxt -b edge",
    "build:chrome": "wxt build -b chrome",
    "build:firefox": "wxt build -b firefox",
    "build:edge": "wxt build -b edge",
    "build-all": "npm run build:chrome && npm run build:firefox && npm run build:edge",
    "zip:chrome": "wxt zip -b chrome",
    "zip:firefox": "wxt zip -b firefox",
    "zip:edge": "wxt zip -b edge",
    "lint": "tsc --noEmit"
  }
}
```

## Manifest-Check je Browser

```bash
npx web-ext lint --source-dir=.output/chrome-mv3
npx web-ext lint --source-dir=.output/firefox-mv2
npx web-ext lint --source-dir=.output/edge-mv3
```

## Entrypoint-Skelette

```ts
// entrypoints/content.ts
export default defineContentScript({
  matches: ['*://*/*mod/quiz/report.php*'],
  main() {
    // Selektor-/Robustheitsregeln: siehe 1-chrome-mv3
  },
});
```

```ts
// entrypoints/background.ts
export default defineBackground(() => {
  // Service-Worker-Logik
});
```
