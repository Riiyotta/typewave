import { useEffect, useRef, useState } from 'react'
import FigmaButton from './FigmaButton'
import { navbarLogo } from '../lib/icons'
import { getLenis, scrollToSelector } from '../lib/scroll'

const NAV = [
  { label: 'How it works', target: '#how-it-works' },
  { label: 'AI Prompt', target: '#ai-prompt', tag: 'NEW' },
  { label: 'Pricing', target: '#pricing' },
  { label: 'FAQ', target: '#faq' },
]

function NavButtons({ onNavigate }) {
  return NAV.map((item) => (
    <button
      key={item.target}
      type="button"
      className="btn btn--ghost btn--sm button-2"
      data-scroll-to={item.target}
      onClick={() => onNavigate(item.target)}
    >
      <span className="btn__label">{item.label}</span>
      {item.tag && <span className="tag caption-1">{item.tag}</span>}
    </button>
  ))
}

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [hidden, setHidden] = useState(false)
  const openRef = useRef(false)
  openRef.current = open

  // M12: hide on scroll down (scrollY > lastY && scrollY > 80), rAF-throttled; skipped while menu open.
  useEffect(() => {
    let lastY = window.scrollY
    let ticking = false
    const onScroll = () => {
      if (ticking) return
      ticking = true
      requestAnimationFrame(() => {
        ticking = false
        const y = window.scrollY
        if (!openRef.current) {
          const hide = y > lastY && y > 80
          setHidden(hide)
        }
        lastY = y
      })
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // Mirror to html.navbar-hidden (drives FAQ sticky offset M13) and notify the floating CTA.
  useEffect(() => {
    document.documentElement.classList.toggle('navbar-hidden', hidden)
    window.dispatchEvent(new CustomEvent('navbar:visibility', { detail: { hidden } }))
  }, [hidden])

  // Mobile menu: stop/start Lenis; aria label handled in markup.
  useEffect(() => {
    const lenis = getLenis()
    if (open) lenis.stop()
    else lenis.start()
  }, [open])

  // Resizing to >=1025 closes the menu.
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1025px)')
    const onChange = () => mq.matches && setOpen(false)
    mq.addEventListener('change', onChange)
    return () => mq.removeEventListener('change', onChange)
  }, [])

  const navigate = (target) => {
    setOpen(false)
    // restart Lenis before scrolling so the scrollTo isn't swallowed by a stopped instance
    getLenis().start()
    scrollToSelector(target)
  }

  const cls = ['navbar', hidden && 'navbar--hidden', open && 'navbar--open'].filter(Boolean).join(' ')

  return (
    <header className={cls}>
      <div className="navbar__inner container">
        <a
          className="navbar__logo"
          href="/"
          aria-label="Typewave homepage"
          dangerouslySetInnerHTML={{ __html: navbarLogo }}
        />
        <nav className="navbar__nav">
          <NavButtons onNavigate={navigate} />
        </nav>
        <div className="navbar__cta">
          <FigmaButton />
        </div>
        <button
          type="button"
          className="navbar__hamburger"
          aria-label={open ? 'Close menu' : 'Open menu'}
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          <span className="navbar__hamburger-line navbar__hamburger-line--top" />
          <span className="navbar__hamburger-line navbar__hamburger-line--bot" />
        </button>
      </div>
      <div className="navbar__mobile-menu">
        <nav className="navbar__mobile-nav">
          <NavButtons onNavigate={navigate} />
        </nav>
        <div className="navbar__mobile-cta">
          <FigmaButton />
        </div>
      </div>
    </header>
  )
}
