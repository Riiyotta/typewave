import { useEffect, useRef, useState } from 'react'
import BreakpointMock from './BreakpointMock'
import TypoSimulator from './TypoSimulator'
import { breakpoint } from '../content'
import { renderTitle } from '../lib/compose'
import { clamp01, isDesktop, onScrollFrame } from '../lib/scroll'

const TOTAL_FRAMES = 50

export default function Breakpoint() {
  const sectionRef = useRef(null)
  const lottieRef = useRef(null)
  const capLeftRef = useRef(null)
  const capRightRef = useRef(null)
  const [frame, setFrame] = useState(0)

  // M9 / M9b scrub + M10 caption slide-up
  useEffect(() => {
    const section = sectionRef.current
    const lottie = lottieRef.current
    const caps = [capLeftRef.current, capRightRef.current]
    const toFrame = (progress) => clamp01((progress - 0.2) / 0.6) * (TOTAL_FRAMES - 1)

    const update = () => {
      const vh = window.innerHeight
      const y = window.scrollY
      let progress
      if (isDesktop()) {
        const sectionDocTop = section.getBoundingClientRect().top + y
        progress = clamp01((y - sectionDocTop) / (section.offsetHeight - vh))
        const ty = (1 - clamp01((progress - 0.5) / 0.5)) * vh * 0.6
        caps.forEach((c) => (c.style.transform = `translateY(${ty}px)`))
      } else {
        const lottieDocTop = lottie.getBoundingClientRect().top + y
        const A = lottieDocTop + lottie.clientHeight - vh
        const C = lottieDocTop
        progress = C === A ? 1 : clamp01((y - A) / (C - A))
        caps.forEach((c) => (c.style.transform = ''))
      }
      setFrame(toFrame(progress))
    }
    update()
    return onScrollFrame(update)
  }, [])

  return (
    <section
      className="breakpoint"
      ref={sectionRef}
      // calc(100vh + totalFrames*8px); overridden to auto at <=1024 by CSS
      style={{ height: `calc(100vh + ${TOTAL_FRAMES * 8}px)` }}
    >
      <div className="breakpoint__header container">
        <h2 className="breakpoint__title display-2 reveal">{renderTitle(breakpoint.title)}</h2>
      </div>
      <div className="breakpoint__sticky">
        <div className="container breakpoint__inner">
          <div className="breakpoint__lottie" ref={lottieRef}>
            <BreakpointMock frame={frame} />
          </div>
          <p className="breakpoint__caption-left body-1" ref={capLeftRef}>
            {breakpoint.caption}
          </p>
          <div className="breakpoint__caption" id="typoSimulator" ref={capRightRef}>
            <TypoSimulator />
          </div>
        </div>
      </div>
    </section>
  )
}
