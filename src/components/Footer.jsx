import FigmaButton from './FigmaButton'
import { footer } from '../content'
import { renderTitle } from '../lib/compose'
import { footerLogo } from '../lib/icons'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__container">
        <div className="footer__hero reveal">
          <div className="footer__logo" dangerouslySetInnerHTML={{ __html: footerLogo }} />
          {/* excluded from scroll-compose (M4) */}
          <h1 className="footer__title display-3">
            {renderTitle(footer.title, { brandClass: 'footer__title--brand', compose: false })}
          </h1>
          <div className="footer__cta">
            <FigmaButton />
          </div>
        </div>
        <div className="footer__bottom reveal" style={{ '--reveal-delay': '150ms' }}>
          <p className="footer__copy caption-1">© 2026 Blendmodes</p>
          <nav className="footer__legal">
            <a className="footer__legal-link caption-1" href="https://www.lemonsqueezy.com/privacy" target="_blank" rel="noopener noreferrer">
              Privacy policy
            </a>
            <a className="footer__legal-link caption-1" href="https://www.lemonsqueezy.com/buyer-terms" target="_blank" rel="noopener noreferrer">
              Terms &amp; conditions
            </a>
          </nav>
        </div>
      </div>
    </footer>
  )
}
