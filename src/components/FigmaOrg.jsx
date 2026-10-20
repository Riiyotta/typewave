import { figmaOrg } from '../content'
import { renderTitle } from '../lib/compose'

const DELAYS = ['0ms', '100ms', '200ms']

export default function FigmaOrg() {
  return (
    <section className="figma-org">
      <div className="container">
        <h2 className="figma-org__title display-2 reveal">{renderTitle(figmaOrg.title)}</h2>
      </div>
      {/* intentionally outside .container (own padding / max-width; carousel at <=1024) */}
      <div className="figma-org__cards">
        {figmaOrg.cards.map((card, i) => (
          <div className="figma-card reveal" style={{ '--reveal-delay': DELAYS[i] }} key={card.title}>
            <div className="figma-card__media">
              <img src={card.img} alt={card.alt} width="800" height="600" />
            </div>
            <h3 className="figma-card__title heading-1">{card.title}</h3>
            <p className="figma-card__text body-1">{card.text}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
