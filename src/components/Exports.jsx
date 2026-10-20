import { exportsCopy } from '../content'
import { renderTitle } from '../lib/compose'
import { logoClaude, logoCursor, logoCursorAi, logoLovable, logoOpenai, logoVscode } from '../lib/icons'

const Logo = ({ svg, label }) => <span role="img" aria-label={label} style={{ display: 'flex' }} dangerouslySetInnerHTML={{ __html: svg }} />

export default function Exports() {
  return (
    <section className="exports">
      <div className="container">
        <div className="exports__wrapper">
          <h2 className="exports__title display-2 reveal">{renderTitle(exportsCopy.title)}</h2>
          <div className="exports__cards">
            <div className="exports__card reveal">
              <div className="exports__media">
                <img src="/assets/css-export-DPacxBL7.jpg" alt="CSS custom properties exported from a generated type ramp" width="707" height="553" />
              </div>
              <div className="exports__text">
                <h3 className="exports__card-title heading-1">CSS</h3>
                <p className="exports__card-text body-1">{exportsCopy.css}</p>
                <div className="exports__card-logos">
                  <Logo svg={logoCursor} label="Cursor" />
                  <Logo svg={logoVscode} label="VS Code" />
                </div>
              </div>
            </div>
            <div className="exports__card exports__card--reverse reveal" id="ai-prompt" style={{ '--reveal-delay': '100ms' }}>
              <div className="exports__text">
                <h3 className="exports__card-title heading-1">
                  AI Prompt <span className="tag caption-1">NEW</span>
                </h3>
                <p className="exports__card-text body-1">{exportsCopy.ai}</p>
                <div className="exports__card-logos">
                  <Logo svg={logoClaude} label="Claude" />
                  <Logo svg={logoCursorAi} label="Cursor" />
                  <Logo svg={logoOpenai} label="OpenAI" />
                  <Logo svg={logoLovable} label="Lovable" />
                </div>
              </div>
              <div className="exports__media">
                <img src="/assets/ai-prompt-B1wIQtkI.jpg" alt="Structured typography brief generated for AI coding assistants" width="707" height="553" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
