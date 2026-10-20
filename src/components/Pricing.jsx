import { pricing } from '../content'
import { renderTitle } from '../lib/compose'
import { checkIcon } from '../lib/icons'

export default function Pricing() {
  return (
    <section className="pricing" id="pricing">
      <div className="container">
        <div className="pricing__wrapper">
          <h2 className="pricing__title display-2 reveal">
            {renderTitle(pricing.title, { brandClass: 'pricing__title--brand' })}
          </h2>
          <div className="pricing__grid">
            {pricing.plans.map((plan) => (
              <div
                key={plan.name}
                className={`pricing-plan${plan.featured ? ' pricing-plan--featured' : ''} reveal`}
                style={{ '--reveal-delay': `${plan.delay}ms` }}
              >
                <div className="pricing-plan__content">
                  <div className="pricing-plan__top">
                    <div className="pricing-plan__header">
                      <p className="pricing-plan__name heading-2">{plan.name}</p>
                      <p className="pricing-plan__subtitle heading-2">{plan.subtitle}</p>
                    </div>
                    <p className="pricing-plan__license body-2">{plan.license}</p>
                  </div>
                  <div className="pricing-plan__price display-3">{plan.price}</div>
                </div>
                <div className="pricing-plan__seam">
                  <div className="pricing-plan__seam-notch" />
                </div>
                <div className="pricing-plan__cta">
                  <a
                    className={`btn btn--${plan.variant} btn--sm button-2`}
                    href={plan.href}
                    {...(plan.mailto ? {} : { target: '_blank', rel: 'noopener noreferrer' })}
                  >
                    {plan.cta}
                  </a>
                </div>
              </div>
            ))}
          </div>
          <div className="pricing-includes reveal">
            <h3 className="pricing-includes__title heading-2">{pricing.includesTitle}</h3>
            <div className="pricing-includes__columns">
              {pricing.includes.map((list, li) => (
                <ul className="pricing-includes__list" key={li}>
                  {list.map((item) => {
                    const text = typeof item === 'string' ? item : item.text
                    return (
                      <li className="pricing-includes__item" key={text}>
                        <span className="pricing-includes__check" dangerouslySetInnerHTML={{ __html: checkIcon }} />
                        <span className="pricing-includes__text body-1">{text}</span>
                        {item.tag && <span className="tag caption-1">{item.tag}</span>}
                      </li>
                    )
                  })}
                </ul>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
