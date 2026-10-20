import { useEffect, useRef } from 'react'
import FigmaButton from './FigmaButton'
import { hero } from '../content'
import { renderTitle } from '../lib/compose'
import { clamp01, isDesktop, onScrollFrame } from '../lib/scroll'

export default function Hero() {
  const sectionRef = useRef(null)
  const containerRef = useRef(null)
  const scaleRef = useRef(null)
  const videoRef = useRef(null)

  // M6: hero video scale-up 0.8 -> 1 with a 6% peek above the fold (desktop only).
  useEffect(() => {
    const section = sectionRef.current
    const container = containerRef.current
    const wrap = scaleRef.current
    let o = 1
    let active = false

    const measure = () => {
      active = isDesktop()
      if (!active) {
        wrap.style.top = ''
        wrap.style.transform = ''
        section.style.minHeight = ''
        return
      }
      const vh = window.innerHeight
      const H = wrap.offsetHeight
      const top = vh - 0.06 * vh - (H * (1 - 0.8)) / 2
      wrap.style.top = `${top}px`
      const containerDocTop = container.getBoundingClientRect().top + window.scrollY
      const heroTop = section.getBoundingClientRect().top + window.scrollY
      // scaled (0.8) rect: top = top + 0.1H, height = 0.8H
      o = containerDocTop + top + 0.1 * H - (vh - 0.8 * H) / 2
      const pad = parseFloat(getComputedStyle(section).paddingBottom) || 0
      const videoCenterDocY = containerDocTop + top + H / 2
      section.style.minHeight = `${Math.max(vh, videoCenterDocY + H / 2 - heroTop + pad)}px`
      update()
    }
    const update = () => {
      if (!active) return
      const s = 0.8 + 0.2 * clamp01(window.scrollY / o)
      wrap.style.transform = `scale(${s})`
    }

    measure()
    const offScroll = onScrollFrame(update, { resize: false })
    window.addEventListener('resize', measure)
    return () => {
      offScroll()
      window.removeEventListener('resize', measure)
    }
  }, [])

  // M7: play once per viewport entry while scrolling down and centre <= vh; reset when fully out.
  useEffect(() => {
    const v = videoRef.current
    v.autoplay = false
    v.loop = false
    v.pause()
    const prime = v.play()
    if (prime && prime.then) prime.then(() => v.pause()).catch(() => {})

    let lastY = window.scrollY
    let armed = true
    const update = () => {
      const y = window.scrollY
      const down = y > lastY
      lastY = y
      const vh = window.innerHeight
      const r = v.getBoundingClientRect()
      if (r.bottom <= 0 || r.top >= vh) {
        if (!armed) {
          v.pause()
          v.currentTime = 0
          armed = true
        }
        return
      }
      if (armed && down && r.top + r.height / 2 <= vh) {
        armed = false
        v.playbackRate = 1
        v.currentTime = 0
        const p = v.play()
        if (p && p.catch) p.catch(() => {})
      }
    }
    return onScrollFrame(update, { resize: false })
  }, [])

  return (
    <section className="hero" ref={sectionRef}>
      <div className="container" ref={containerRef}>
        <div className="hero__wrapper" data-parallax="-0.02">
          <div className="hero__content" data-parallax="-0.08">
            <h1 className="hero__title display-1 reveal" style={{ '--reveal-delay': '0ms' }}>
              {renderTitle(hero.title, { brandClass: 'hero__title--brand' })}
            </h1>
            <p className="hero__subtitle subtitle-1 reveal" style={{ '--reveal-delay': '150ms' }}>
              {hero.subtitle}
            </p>
            <div className="hero__cta reveal" style={{ '--reveal-delay': '300ms' }}>
              <FigmaButton />
            </div>
          </div>
          <div className="hero__video-scale" ref={scaleRef}>
            <video
              ref={videoRef}
              className="hero__image reveal"
              style={{ '--reveal-delay': '450ms' }}
              src="/assets/intro-DrshnI3i.mp4"
              muted
              playsInline
              preload="auto"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
