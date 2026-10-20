import { useEffect } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import HowItWorks from './components/HowItWorks'
import FigmaOrg from './components/FigmaOrg'
import Breakpoint from './components/Breakpoint'
import Presets from './components/Presets'
import Exports from './components/Exports'
import Pricing from './components/Pricing'
import Faq from './components/Faq'
import Newsletter from './components/Newsletter'
import Footer from './components/Footer'
import FloatingCta from './components/FloatingCta'
import TypeInspector from './components/TypeInspector'
import { destroySmoothScroll, initSmoothScroll } from './lib/scroll'
import { initReveal } from './lib/reveal'
import { initParallax } from './lib/parallax'
import { initScrollCompose } from './lib/compose'

export default function App() {
  // Section-level behaviours live in each component's effects (they run first, in tree order).
  // Page-level motion runs here, after them: Lenis -> reveal -> parallax -> scroll-compose.
  useEffect(() => {
    const lenis = initSmoothScroll()
    const cleanups = [initReveal(), initParallax(lenis), initScrollCompose()]
    return () => {
      cleanups.forEach((fn) => fn && fn())
      destroySmoothScroll()
    }
  }, [])

  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <HowItWorks />
        <FigmaOrg />
        <Breakpoint />
        <Presets />
        <Exports />
        <Pricing />
        <Faq />
        <Newsletter />
      </main>
      <Footer />
      <FloatingCta />
      <TypeInspector />
    </>
  )
}
