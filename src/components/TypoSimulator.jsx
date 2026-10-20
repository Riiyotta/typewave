import { memo, useState } from 'react'

// Typo simulator (#typoSimulator) — formula ported exactly from CLONE_SPEC §7.
const TOKENS = [10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 80, 88, 96]
const calcRaw = (t, k) => (t <= 16 ? t : t * (1 - k * Math.sqrt((t - 16) / 80)))
const snap = (v) => TOKENS.reduce((best, t) => (Math.abs(t - v) < Math.abs(best - v) ? t : best), TOKENS[0])
const lh = (s) => (s >= 32 ? 1 : s >= 20 ? 1.4 : s >= 16 ? 1.5 : 1.333)

function TypoSimulator() {
  const [desktop, setDesktop] = useState(96)
  const rows = [
    { label: 'Desktop', size: desktop, select: true },
    { label: 'Tablet', size: snap(calcRaw(desktop, 0.25)) },
    { label: 'Mobile', size: snap(calcRaw(desktop, 0.6)) },
  ]
  return (
    <div className="typo-sim__grid">
      {rows.map((row) => (
        <div className="typo-sim__row" key={row.label}>
          <div className="typo-sim__label">{row.label}</div>
          <div className="typo-sim__value">
            {row.select ? (
              <select
                className="typo-sim__select"
                aria-label="Desktop font size"
                value={desktop}
                onChange={(e) => setDesktop(Number(e.target.value))}
              >
                {TOKENS.map((t) => (
                  <option key={t} value={t}>
                    {t}px
                  </option>
                ))}
              </select>
            ) : (
              <span className="typo-sim__token">{row.size}px</span>
            )}
            <div className="typo-sim__glyph" style={{ fontSize: `${row.size}px`, lineHeight: lh(row.size) }}>
              Ag
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default memo(TypoSimulator)
