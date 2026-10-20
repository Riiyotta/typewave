import { useEffect, useRef, useState } from 'react'
import { EMAIL, faq } from '../content'
import { renderTitle } from '../lib/compose'
import { chevronIcon } from '../lib/icons'
import { isDesktop } from '../lib/scroll'

// FAQPage JSON-LD generated from the placeholder copy (spec §0 head/meta)
const faqJsonLd = JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faq.items.map((it) => ({
    '@type': 'Question',
    name: it.q,
    acceptedAnswer: {
      '@type': 'Answer',
      text: it.a ? it.a.join(' ') : `${it.linkParagraph[0]}${EMAIL}${it.linkParagraph[1]}`,
    },
  })),
})

export default function Faq() {
  const [openIndex, setOpenIndex] = useState(-1)
  const sectionRef = useRef(null)

  // Desktop: a document click outside .faq closes all items.
  useEffect(() => {
    const onDocClick = (e) => {
      if (!isDesktop()) return
      if (sectionRef.current && !sectionRef.current.contains(e.target)) setOpenIndex(-1)
    }
    document.addEventListener('click', onDocClick)
    return () => document.removeEventListener('click', onDocClick)
  }, [])

  return (
    <section className="faq" id="faq" ref={sectionRef}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: faqJsonLd }} />
      <div className="container">
        <div className="faq__inner">
          <div className="faq__lead">
            <h2 className="faq__title display-2 reveal">
              {renderTitle(faq.title, { brandClass: 'faq__title--brand' })}
            </h2>
            <a className="faq__email body-1 reveal" style={{ '--reveal-delay': '150ms' }} href={`mailto:${EMAIL}`}>
              {EMAIL}
            </a>
          </div>
          <div className="faq__list reveal">
            {faq.items.map((item, i) => {
              const open = openIndex === i
              const qid = `faq-q-${i}`
              const aid = `faq-a-${i}`
              return (
                <div className={`faq__item${open ? ' is-open' : ''}`} key={qid}>
                  <button
                    type="button"
                    id={qid}
                    className="faq__question subtitle-1"
                    aria-expanded={open}
                    aria-controls={aid}
                    onClick={() => setOpenIndex(open ? -1 : i)}
                  >
                    <span className="faq__question-text">{item.q}</span>
                    <span className="faq__chevron" dangerouslySetInnerHTML={{ __html: chevronIcon }} />
                  </button>
                  <div className="faq__answer" id={aid} role="region" aria-labelledby={qid} aria-hidden={!open}>
                    <div className="faq__answer-inner">
                      {item.a &&
                        item.a.map((p, j) => (
                          <p className="faq__answer-text body-1" key={j} style={j > 0 ? { marginTop: '16px' } : undefined}>
                            {p}
                          </p>
                        ))}
                      {item.image && <img className="faq__answer-image" src={item.image.src} alt={item.image.alt} width="869" height="650" />}
                      {item.linkParagraph && (
                        <p className="faq__answer-text body-1">
                          {item.linkParagraph[0]}
                          <a className="faq__answer-link" href={`mailto:${EMAIL}`}>
                            {EMAIL}
                          </a>
                          {item.linkParagraph[1]}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
