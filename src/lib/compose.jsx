import { Fragment } from 'react'
import { clamp01, onScrollFrame, prefersReducedMotion } from './scroll'

// Title mini-syntax: "|" -> <br class="title-break">, "[...]" -> brand span.
// With compose=true every non-space run becomes span.compose-word and every
// char span.compose-char (M4), rendered by React so nothing mutates the DOM.
function renderText(text, compose, keyBase) {
  if (!compose) return text
  return text.split(/(\s+)/).map((part, i) => {
    if (part === '') return null
    if (/^\s+$/.test(part)) return ' '
    return (
      <span className="compose-word" key={`${keyBase}-${i}`}>
        {Array.from(part).map((ch, j) => (
          <span className="compose-char" key={j}>
            {ch}
          </span>
        ))}
      </span>
    )
  })
}

export function renderTitle(src, { brandClass = 'text-brand', compose = true } = {}) {
  const out = []
  const lines = src.split('|')
  lines.forEach((line, li) => {
    if (li > 0) {
      // keep a space before the break so words don't fuse when .title-break is hidden (<=767)
      out.push(' ', <br className="title-break" key={`br-${li}`} />)
    }
    const re = /\[([^\]]*)\]/g
    let last = 0
    let m
    let seg = 0
    while ((m = re.exec(line))) {
      if (m.index > last) out.push(<Fragment key={`t-${li}-${seg++}`}>{renderText(line.slice(last, m.index), compose, `${li}-${seg}`)}</Fragment>)
      out.push(
        <span className={brandClass} key={`b-${li}-${seg++}`}>
          {renderText(m[1], compose, `${li}-b${seg}`)}
        </span>
      )
      last = re.lastIndex
    }
    if (last < line.length) out.push(<Fragment key={`t-${li}-${seg++}`}>{renderText(line.slice(last), compose, `${li}-${seg}`)}</Fragment>)
  })
  return out
}

export const plainTitle = (src) => src.replace(/\|/g, ' ').replace(/[[\]]/g, '')

// M4: scroll-composed characters. start=0.9vh, end=0.45vh,
// E=clamp01((start-top)/(start-end)); char i of n: d=(i/n)*(1-0.35), opacity=clamp01((E-d)/0.35).
export function initScrollCompose() {
  if (prefersReducedMotion()) return () => {}
  const SPAN = 0.35
  const headings = Array.from(
    document.querySelectorAll('h1.display-1, h2.display-1, h1.display-2, h2.display-2')
  )
    .filter((h) => !h.classList.contains('footer__title'))
    .map((el) => ({ el, chars: Array.from(el.querySelectorAll('.compose-char')), last: -1 }))

  const update = () => {
    const vh = window.innerHeight
    const start = 0.9 * vh
    const end = 0.45 * vh
    headings.forEach((h) => {
      const top = h.el.getBoundingClientRect().top
      const E = clamp01((start - top) / (start - end))
      if (E === h.last) return
      h.last = E
      const n = h.chars.length
      h.chars.forEach((c, i) => {
        const d = (i / n) * (1 - SPAN)
        c.style.opacity = clamp01((E - d) / SPAN)
      })
    })
  }
  update()
  return onScrollFrame(update)
}
