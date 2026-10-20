import Lenis from 'lenis'

// ---- shared math / media helpers ----
export const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v)
export const DESKTOP_MQ = '(min-width: 1025px)'
export const isDesktop = () => window.matchMedia(DESKTOP_MQ).matches
export const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

// rAF-throttled scroll + resize subscription. Returns an unsubscribe fn.
export function onScrollFrame(cb, { resize = true } = {}) {
  let ticking = false
  const handler = () => {
    if (ticking) return
    ticking = true
    requestAnimationFrame(() => {
      ticking = false
      cb()
    })
  }
  window.addEventListener('scroll', handler, { passive: true })
  if (resize) window.addEventListener('resize', handler)
  return () => {
    window.removeEventListener('scroll', handler)
    if (resize) window.removeEventListener('resize', handler)
  }
}

// ---- M1: Lenis smooth scroll (desktop only, decided once at load) ----
let instance = null
let rafId = 0

const shim = {
  isShim: true,
  get scroll() {
    return window.scrollY
  },
  scrollTo(target, { offset = 0 } = {}) {
    const el = typeof target === 'string' ? document.querySelector(target) : target
    if (!el) return
    window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY + offset, behavior: 'smooth' })
  },
  on() {},
  off() {},
  stop() {},
  start() {},
}

export function initSmoothScroll() {
  if (instance) return instance
  if (window.matchMedia('(max-width: 1024px)').matches) {
    instance = shim
    return instance
  }
  const lenis = new Lenis({
    duration: 1.4,
    easing: (t) => 1 - Math.pow(1 - t, 5),
    smoothWheel: true,
  })
  const raf = (t) => {
    lenis.raf(t)
    rafId = requestAnimationFrame(raf)
  }
  rafId = requestAnimationFrame(raf)
  instance = lenis
  return instance
}

export function destroySmoothScroll() {
  if (instance && !instance.isShim) {
    cancelAnimationFrame(rafId)
    instance.destroy()
  }
  instance = null
}

export const getLenis = () => instance || shim

// Nav / floating-CTA scroll target helper: lenis.scrollTo(selector, { offset: -80 })
export function scrollToSelector(selector) {
  getLenis().scrollTo(selector, { offset: -80 })
}
