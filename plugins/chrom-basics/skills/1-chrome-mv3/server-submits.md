# Das Muster für Submits, die die Seite neu laden

Begleitdatei zu `1-chrome-mv3`.


Der häufigste Fehler in diesen Erweiterungen: Ein Klick auf ein Moodle-Bedienelement
sieht wie ein harmloser JS-Knopf aus, ist aber ein `type="submit"` und lädt die Seite
neu. Der laufende Ablauf bricht mitten drin ab, ohne Fehlermeldung — es sieht so aus,
als hätte der Klick nichts bewirkt.

**Erkennen:** Vor jedem programmatischen Klick prüfen, ob das Element `type="submit"`
in einem `<form>` ist. Wenn ja, ist die Seite danach weg.

**Lösen:** Zustand vor dem Klick in `localStorage` retten, und die frisch geladene
Seite den Ablauf fortsetzen lassen.

```js
const PENDING_KEY = 'meinAblaufPending';
const PENDING_TTL_MS = 30000;      // gegen veraltete Reste
const MAX_RUNDEN = 12;             // gegen Endlosschleifen

function setPending(runde) {
  localStorage.setItem(PENDING_KEY, JSON.stringify({ t: Date.now(), runde }));
}
function readPending() {
  const raw = localStorage.getItem(PENDING_KEY);
  if (!raw) return null;
  try {
    const o = JSON.parse(raw);
    if (!o || typeof o.runde !== 'number' || Date.now() - o.t > PENDING_TTL_MS) {
      localStorage.removeItem(PENDING_KEY); return null;
    }
    return o;
  } catch (e) { localStorage.removeItem(PENDING_KEY); return null; }
}

async function run(runde = 0) {
  if (nochNichtFertig() && runde < MAX_RUNDEN) {
    setPending(runde + 1);          // VOR dem Klick, jedes Mal neu
    submitKnopf.click();
    return;                          // Seite lädt neu, init() übernimmt
  }
  eigentlicheArbeit();
}

function init() {
  const p = readPending();
  if (p) { clearPending(); setTimeout(() => run(p.runde), 300); }
}
```

`localStorage`, nicht `sessionStorage` — überlebt auch den Fall, dass Moodle wider
Erwarten einen neuen Tab öffnet.

**Zwei Fallen dabei:**

- Das Flag **vor jedem** Klick neu setzen, nicht nur einmal am Anfang. Wird es beim
  ersten Durchlauf verbraucht, bleibt der zweite ohne Signal liegen.
- Kurzschluss-Auswertung beachten: `if (istZielseite() && verbrauchePending())` ruft
  `verbrauchePending()` nicht auf, wenn die erste Bedingung falsch ist — das Flag
  bleibt dann liegen und stört später.

---

