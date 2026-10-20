import { memo, useEffect, useRef, useState } from 'react'
import { breakpoint } from '../content'

// HTML/CSS rebuild of the 1280x728 "Breakpoint" Lottie (50 frames, 0–49): a device
// frame that morphs desktop browser -> tablet -> phone. Geometry is taken from the
// composition's layer data (composition px); layers switch on the same in/out frames.
const COMP_W = 1280
const LAST = 49

// [fromFrame, value...] tables; a row applies while fromFrame <= f (until the next row)
const HEADLINE = [
  [0, { size: 72, top: 242.5, width: 751.7 }],
  [27, { size: 56, top: 225.5, width: 503.3 }],
  [33, { size: 56, top: 217.4, width: 503.3 }],
  [41, { size: 40, top: 242.5, width: 503.3 }],
]
const PARAGRAPH = [
  [0, { top: 416.5, width: 564.0 }],
  [21, { top: 416.5, width: 543.9 }],
  [25, { top: 416.5, width: 527.1 }],
  [27, { top: 366.9, width: 466.7 }],
  [29, { top: 366.9, width: 440.3 }],
  [31, { top: 366.9, width: 417.3 }],
  [33, { top: 360.4, width: 397.6 }],
  [35, { top: 360.4, width: 384.6 }],
  [37, { top: 360.4, width: 362.6 }],
  [41, { top: 351.5, width: 362.6 }],
  [47, { top: 351.5, width: 329.7 }],
]
const BUTTON_Y = [
  [0, 538.7],
  [27, 487.7],
  [33, 498.6],
  [41, 490.6],
]
const pick = (table, f) => {
  let v = table[0][1]
  for (const [from, val] of table) if (f >= from) v = val
  return v
}

function BreakpointMock({ frame }) {
  const boxRef = useRef(null)
  const [scale, setScale] = useState(1)

  useEffect(() => {
    const box = boxRef.current
    const ro = new ResizeObserver(() => setScale(box.clientWidth / COMP_W))
    ro.observe(box)
    return () => ro.disconnect()
  }, [])

  const f = Math.min(Math.max(frame, 0), LAST)
  const deviceW = 1271.3 - (1271.3 - 399.3) * (f / LAST) // linear keyframes 0 -> 49
  const browser = f < 27
  const tablet = f >= 27 && f < 41
  const phone = f >= 41
  const t27 = Math.min(f, 27) / 27
  const barW = 1269.343 * (1 - 0.38 * t27) // chrome divider scaleX 100% -> 62% over 0–27
  const dotDx = 228.101 * t27 // traffic-light dots follow the left edge
  const head = pick(HEADLINE, f)
  const para = pick(PARAGRAPH, f)
  const btnY = pick(BUTTON_Y, f)

  return (
    <div className="bp-mock" ref={boxRef} aria-hidden="true">
      <div className="bp-mock__stage" style={{ transform: `scale(${scale})` }}>
        <div className="bp-mock__device" style={{ width: `${deviceW + 2}px` }} />
        {browser && (
          <>
            <div className="bp-mock__bar" style={{ left: '640px', width: `${barW}px` }} />
            {[42.101, 63.768, 85.435].map((x) => (
              <span
                key={x}
                className="bp-mock__dot"
                style={{ left: `${x + dotDx}px`, top: '26.779px', width: '14px', height: '14px' }}
              />
            ))}
          </>
        )}
        {tablet && (
          <span className="bp-mock__dot" style={{ left: '640px', top: '682.748px', width: '26.821px', height: '26.821px' }} />
        )}
        {phone && (
          <span className="bp-mock__dot" style={{ left: '640px', top: '34.269px', width: '20.551px', height: '20.551px' }} />
        )}
        <p
          className="bp-mock__headline"
          style={{ top: `${head.top}px`, width: `${head.width}px`, fontSize: `${head.size}px`, lineHeight: `${head.size}px` }}
        >
          {breakpoint.mock.headline[0]}
          <br />
          {breakpoint.mock.headline[1]}
        </p>
        <p className="bp-mock__paragraph" style={{ top: `${para.top}px`, width: `${para.width}px` }}>
          {breakpoint.mock.paragraph}
        </p>
        <span className="bp-mock__button" style={{ top: `${btnY}px` }}>
          {breakpoint.mock.button}
        </span>
      </div>
    </div>
  )
}

export default memo(BreakpointMock)
