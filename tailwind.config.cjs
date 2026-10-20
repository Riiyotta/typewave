/** @type {import('tailwindcss').Config} */
// Tokens reference the CSS custom properties declared in src/index.css (:root),
// so the values live in exactly one place.
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  // The original site ships its own minimal reset (*{margin:0;padding:0;box-sizing:border-box})
  // and relies on UA defaults otherwise; Tailwind's preflight would change line-heights
  // (html{line-height:1.5}) and form-control fonts, so it is disabled.
  corePlugins: { preflight: false, container: false },
  theme: {
    screens: {
      // desktop-first, matching the original max-width queries
      desktop: { min: '1025px' },
      tablet: { max: '1024px' },
      mobile: { max: '767px' },
    },
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: 'var(--color-surface)',
        text: 'var(--color-text)',
        muted: 'var(--color-text-muted)',
        brand: 'var(--color-brand)',
        accent: 'var(--color-accent)',
        danger: 'var(--color-danger)',
        chrome: 'var(--color-chrome)',
        'badge-2': 'var(--color-badge-2)',
        'badge-3': 'var(--color-badge-3)',
        'preset-pink': 'var(--color-preset-pink)',
      },
      fontFamily: {
        primary: 'var(--font-primary)',
        secondary: 'var(--font-secondary)',
      },
      borderRadius: {
        xs: 'var(--radius-xs)',
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        full: 'var(--radius-full)',
      },
      maxWidth: { container: 'var(--grid-container-max)' },
      spacing: {
        navbar: 'var(--navbar-height)',
        'navbar-mobile': 'var(--navbar-height-mobile)',
        section: 'var(--section-padding)',
      },
      transitionTimingFunction: {
        standard: 'var(--ease-standard)',
        decel: 'var(--ease-decel)',
      },
    },
  },
  plugins: [],
}
