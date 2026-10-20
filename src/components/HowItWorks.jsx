import { useEffect, useRef } from 'react'
import { howItWorks } from '../content'
import { renderTitle } from '../lib/compose'
import { clamp01, isDesktop, onScrollFrame } from '../lib/scroll'

export default function HowItWorks() {
  const cardsRef = useRef(null)

  // M8: sticky stacking cards (desktop) / M8b: autoplay all card videos (<=1024).
  useEffect(() => {
    const cards = Array.from(cardsRef.current.querySelectorAll('.card'))
    const videos = cards.map((c) => c.querySelector('video'))
    const started = cards.map(() => false)
    let r = 0
    let desktop = isDesktop()

    const playVideo = (i) => {
      if (started[i]) return
      started[i] = true
      const p = videos[i].play()
      if (p && p.catch) p.catch(() => {})
    }

    const measure = () => {
      desktop = isDesktop()
      if (!desktop) {
        cards.forEach((c) => {
          c.style.top = ''
          c.style.transform = ''
        })
        videos.forEach((_, i) => playVideo(i))
        return
      }
      r = (window.innerHeight - cards[0].offsetHeight) / 2
      cards.forEach((c) => (c.style.top = `${r}px`))
      update()
    }

    const update = () => {
      if (!desktop) return
      const vh = window.innerHeight
      const span = vh - r
      cards.forEach((card, i) => {
        const rect = card.getBoundingClientRect()
        const p = 0.75 + 0.25 * clamp01((vh - rect.top) / span)
        let s = 1
        const next = cards[i + 1]
        if (next) s = 1 - 0.25 * clamp01((vh - next.getBoundingClientRect().top) / span)
        const scale = Math.min(p, s)
        card.style.transform = `scale(${scale})`
        if (scale >= 0.98) playVideo(i)
      })
    }

    const onLoad = () => measure()
    if (document.readyState === 'complete') measure()
    else window.addEventListener('load', onLoad)
    // card height depends on video intrinsic size (height:auto), so re-measure when metadata arrives
    videos.forEach((v) => v.addEventListener('loadedmetadata', measure))
    measure()
    const offScroll = onScrollFrame(update, { resize: false })
    window.addEventListener('resize', measure)
    return () => {
      offScroll()
      window.removeEventListener('resize', measure)
      window.removeEventListener('load', onLoad)
      videos.forEach((v) => v.removeEventListener('loadedmetadata', measure))
    }
  }, [])

  return (
    <section className="how-it-works" id="how-it-works">
      <div className="container">
        <div className="how-it-works__wrapper">
          <div className="how-it-works__header" data-parallax="-0.04">
            <h2 className="how-it-works__title display-2 reveal" style={{ '--reveal-delay': '150ms' }}>
              {renderTitle(howItWorks.title)}
            </h2>
          </div>
          <div className="how-it-works__cards" ref={cardsRef}>
            {howItWorks.cards.map((card) => (
              <div className="card" key={card.badge}>
                <div className="card__body">
                  <div className="card__top">
                    <div className="badge button-2" style={{ '--badge-bg': card.badgeBg }}>
                      {card.badge}
                    </div>
                    <h3 className="card__title heading-1">{card.title}</h3>
                  </div>
                  <p className="card__text body-1">{card.text}</p>
                </div>
                <div className="card__media">
                  <video className="card__image" src={card.video} loop muted playsInline preload="metadata" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
