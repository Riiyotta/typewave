// M2: fade-up reveal. IntersectionObserver threshold 0.15, once.
// On init and on resize, anything already overlapping the viewport is revealed immediately.
export function initReveal() {
  const els = Array.from(document.querySelectorAll('.reveal'))
  const show = (el) => {
    el.classList.add('is-visible')
    io.unobserve(el)
  }
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && show(e.target)),
    { threshold: 0.15 }
  )
  const revealInViewport = () => {
    const vh = window.innerHeight
    els.forEach((el) => {
      if (el.classList.contains('is-visible')) return
      const r = el.getBoundingClientRect()
      if (r.bottom > 0 && r.top < vh) show(el)
    })
  }
  els.forEach((el) => io.observe(el))
  revealInViewport()
  window.addEventListener('resize', revealInViewport)
  return () => {
    io.disconnect()
    window.removeEventListener('resize', revealInViewport)
  }
}
