import { newsletter } from '../content'
import { renderTitle } from '../lib/compose'

export default function Newsletter() {
  return (
    <section className="newsletter">
      <div className="container">
        <div className="newsletter__inner">
          <div className="newsletter__content reveal">
            <h2 className="newsletter__title display-2">
              {renderTitle(newsletter.title, { brandClass: 'newsletter__title--brand' })}
            </h2>
          </div>
          <form
            className="newsletter__form reveal"
            style={{ '--reveal-delay': '150ms' }}
            action="https://typewave.lemonsqueezy.com/email-subscribe/external"
            method="post"
            target="_blank"
          >
            <div className="newsletter__field">
              <input
                className="newsletter__input display-2"
                type="email"
                name="email"
                placeholder={newsletter.placeholder}
                aria-label="Email address"
              />
              <button type="submit" className="newsletter__submit" aria-label="Subscribe">
                <span className="display-2">→</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  )
}
