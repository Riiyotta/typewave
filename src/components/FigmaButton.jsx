import { FIGMA_URL } from '../content'
import { figmaIcon } from '../lib/icons'

// a.btn.btn--primary.btn--sm.button-2 (Figma icon + "Try it now") -> Figma community URL
export default function FigmaButton({ className = '' }) {
  return (
    <a
      className={`btn btn--primary btn--sm button-2 ${className}`.trim()}
      href={FIGMA_URL}
      target="_blank"
      rel="noopener noreferrer"
    >
      <span className="btn__icon" dangerouslySetInnerHTML={{ __html: figmaIcon }} />
      <span className="btn__label">Try it now</span>
    </a>
  )
}
