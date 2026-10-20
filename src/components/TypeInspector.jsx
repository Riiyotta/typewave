import { useEffect, useRef } from 'react'

// M18: cursor badge naming the type-scale class under the pointer (pointer:fine only).
const TYPE_CLASSES = ['display-1', 'display-2', 'display-3', 'heading-1', 'heading-2', 'subtitle-1', 'body-1', 'body-2', 'button-1', 'button-2', 'caption-1']
const SELECTOR = TYPE_CLASSES.map((c) => `.${c}`).join(',')

const matchClass = (target) => {
  const el = target && target.closest ? target.closest(SELECTOR) : null
  if (!el) return null
  return TYPE_CLASSES.find((c) => el.classList.contains(c)) || null
}

export default function TypeInspector() {
  const ref = useRef(null)

  useEffect(() => {
    if (!window.matchMedia('(pointer: fine)').matches) return
    const badge = ref.current
    let lastX = -1
    let lastY = -1
    const show = (name, x, y) => {
      badge.textContent = name
      badge.style.left = `${x + 16}px`
      badge.style.top = `${y + 16}px`
      badge.classList.add('is-visible')
    }
    const hide = () => badge.classList.remove('is-visible')

    const onMove = (e) => {
      lastX = e.clientX
      lastY = e.clientY
      const name = matchClass(e.target)
      if (name) show(name, lastX, lastY)
      else hide()
    }
    const onScroll = () => {
      if (lastX < 0) return
      const name = matchClass(document.elementFromPoint(lastX, lastY))
      if (!name) hide()
    }
    document.addEventListener('mousemove', onMove, { passive: true })
    document.documentElement.addEventListener('mouseleave', hide)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      document.removeEventListener('mousemove', onMove)
      document.documentElement.removeEventListener('mouseleave', hide)
      window.removeEventListener('scroll', onScroll)
    }
  }, [])

  return <div className="type-inspector-badge" ref={ref} aria-hidden="true" />
}
