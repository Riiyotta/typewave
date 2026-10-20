import { useEffect, useRef, useState } from 'react'
import { presets } from '../content'
import { renderTitle } from '../lib/compose'
import { presetFolder } from '../lib/icons'
import { clamp01, onScrollFrame, prefersReducedMotion } from '../lib/scroll'

// Folder colour cycle (spec §8): #E6F490, #0469FF, #DCBDC2, #FE8A3D, #E6E3DA — via tokens
const COLORS = [
  'var(--color-brand)',
  'var(--color-badge-3)',
  'var(--color-preset-pink)',
  'var(--color-badge-2)',
  'var(--color-text)',
]
const TIERS = {
  mobile: { count: 5, amp: 22 },
  tablet: { count: 8, amp: 50 },
  desktop: { count: 12, amp: 88 },
}
const getTier = () =>
  window.matchMedia('(max-width: 767px)').matches
    ? 'mobile'
    : window.matchMedia('(max-width: 1024px)').matches
      ? 'tablet'
      : 'desktop'

export default function Presets() {
  const [tier, setTier] = useState(getTier)
  const gridRef = useRef(null)

  useEffect(() => {
    const onResize = () => setTier(getTier())
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  // M11: single travelling sine bump, left -> right.
  useEffect(() => {
    if (prefersReducedMotion()) return
    const grid = gridRef.current
    const items = Array.from(grid.querySelectorAll('.presets__item'))
    const amp = TIERS[tier].amp
    const SPAN = 0.35
    const update = () => {
      const vh = window.innerHeight
      const top = grid.getBoundingClientRect().top
      const p = clamp01((0.8 * vh - top) / (0.8 * vh - 0.2 * vh))
      const d = items.length
      items.forEach((el, c) => {
        const m = (c / (d - 1)) * (1 - SPAN)
        const u = clamp01((p - m) / SPAN)
        el.style.transform = `translateY(${-Math.sin(u * Math.PI) * amp}px)`
      })
    }
    update()
    return onScrollFrame(update)
  }, [tier])

  const items = Array.from({ length: TIERS[tier].count }, (_, i) => i)

  return (
    <section className="presets">
      <div className="container">
        <h2 className="presets__title display-2 reveal">{renderTitle(presets.title)}</h2>
        <div className="presets__grid" data-tier={tier} ref={gridRef}>
          {items.map((i) => (
            <div className="presets__item" key={`${tier}-${i}`}>
              <div
                className="presets__folder"
                style={{ color: COLORS[i % COLORS.length] }}
                dangerouslySetInnerHTML={{ __html: presetFolder }}
              />
              <p className="presets__label body-1">Preset {i + 1}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
