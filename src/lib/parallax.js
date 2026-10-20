import { isDesktop } from './scroll'

// M5: [data-parallax] -> translateY(lenis.scroll * factor), only while the closest
// <section> intersects the viewport. Desktop only; transforms cleared at <=1024.
export function initParallax(lenis) {
  const els = Array.from(document.querySelectorAll('[data-parallax]')).map((el) => ({
    el,
    factor: parseFloat(el.dataset.parallax) || 0,
    section: el.closest('section'),
  }))
  const update = () => {
    if (!isDesktop() || lenis.isShim) {
      els.forEach(({ el }) => (el.style.transform = ''))
      return
    }
    const vh = window.innerHeight
    const y = lenis.scroll
    els.forEach(({ el, factor, section }) => {
      if (section) {
        const r = section.getBoundingClientRect()
        if (r.bottom < 0 || r.top > vh) return
      }
      el.style.transform = `translateY(${y * factor}px)`
    })
  }
  const unsub = lenis.on('scroll', update)
  window.addEventListener('resize', update)
  update()
  return () => {
    if (typeof unsub === 'function') unsub()
    window.removeEventListener('resize', update)
  }
}
