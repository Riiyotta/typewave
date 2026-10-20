import { useEffect, useRef } from 'react'
import FigmaButton from './FigmaButton'
import { onScrollFrame, scrollToSelector } from '../lib/scroll'

// M15: visible only when hero video top <= 0, newsletter field top > vh, and navbar hidden.
export default function FloatingCta() {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    // enable the transition only after two frames so first paint doesn't animate
    let r2 = 0
    const r1 = requestAnimationFrame(() => {
      r2 = requestAnimationFrame(() => el.classList.add('is-ready'))
    })

    const update = () => {
      const video = document.querySelector('.hero__image')
      const field = document.querySelector('.newsletter__field')
      const navHidden = !!document.querySelector('.navbar--hidden')
      const visible =
        !!video &&
        !!field &&
        video.getBoundingClientRect().top <= 0 &&
        field.getBoundingClientRect().top > window.innerHeight &&
        navHidden
      el.classList.toggle('is-visible', visible)
    }
    const off = onScrollFrame(update)
    // the navbar class flips after its own rAF; re-check when it reports a change
    window.addEventListener('navbar:visibility', update)
    update()
    return () => {
      cancelAnimationFrame(r1)
      cancelAnimationFrame(r2)
      off()
      window.removeEventListener('navbar:visibility', update)
    }
  }, [])

  return (
    <div className="floating-cta" ref={ref}>
      <FigmaButton />
      <button type="button" className="btn btn--ghost button-2" data-scroll-to="#pricing" onClick={() => scrollToSelector('#pricing')}>
        <span className="btn__label">Pricing</span>
      </button>
    </div>
  )
}
