// Placeholder copy for the clone. Written fresh for a fictional typographic-scale
// Figma plugin; lengths match CLONE_SPEC.md char/word/line counts so layout and
// scroll-compose timing stay identical.
//
// Title markup mini-syntax (parsed by src/lib/compose.jsx):
//   "|"      -> <br class="title-break">
//   "[...]"  -> brand-coloured span

export const FIGMA_URL = 'https://www.figma.com/community/plugin/1615417453541684477/typewave'

export const hero = {
  title: 'Craft a balanced|type scale|[without any math.]',
  subtitle:
    'Typewave reads a single base size and drafts a responsive type ramp, with Figma frames, text styles, variables and handoff exports included, so font sizing never stalls the work.',
}

export const howItWorks = {
  title: 'Manual ramps take hours.|Ours arrive [before your coffee cools!]',
  cards: [
    {
      badge: '1',
      badgeBg: 'var(--color-brand)',
      video: '/assets/def1--g7RFuQa.mp4',
      title: 'Split text into up to five distinct roles',
      text: 'Assign each typeface in your document to a dedicated role, whether display, headline, paragraph or caption, and every role keeps its individual rhythm and spacing throughout.',
    },
    {
      badge: '2',
      badgeBg: 'var(--color-badge-2)',
      video: '/assets/def2-0T0-0aPX.mp4',
      title: 'Shape the ramp for each product',
      text: 'Begin with a ready-made starting point tuned for marketing websites, then drag the base size, ratio and step count until the ramp feels right. Every adjustment previews instantly, so you can compare alternatives before committing.',
    },
    {
      badge: '3',
      badgeBg: 'var(--color-badge-3)',
      video: '/assets/loop3-CWAyqkgp.mp4',
      title: 'Generate a complete typographic system in Figma',
      text: 'One click lays out the preview frames, writes the text styles, sets up the variables and gets the code and prompt exports ready for you, all named in a way that your whole team can read at a glance.',
    },
  ],
}

export const figmaOrg = {
  title: 'Every layer filed,|[named and categorised]',
  cards: [
    {
      img: '/assets/frame-Cg0zK82j.png',
      alt: 'Labelled preview frames laid out for each step of a generated type ramp',
      title: 'Frames',
      text: 'Each step of the ramp receives its own labelled preview frame, so you can inspect sizes, line heights and spacing in context before sharing the file with your teammates.',
    },
    {
      img: '/assets/styles-DpEOnP78.png',
      alt: 'Figma text styles panel grouped by role and breakpoint',
      title: 'Styles',
      text: 'A matching text style is generated for every level of the ramp, grouped by role and breakpoint so designers can choose the right one from the panel without guessing.',
    },
    {
      img: '/assets/variable-fdRUIB1a.png',
      alt: 'Figma variables table holding font sizes and line heights per mode',
      title: 'Variables',
      text: 'Font sizes, line heights and letter spacing are stored as variables, so you can bind them to your components and switch modes whenever the layout shifts.',
    },
  ],
}

export const breakpoint = {
  title: 'All devices covered|[with zero extra work.]',
  caption:
    'Large headings shrink the most on narrow screens, while body text and captions barely move, because small sizes already sit close to the limit of comfortable reading. The plugin follows that curve for you and scales each step by its own amount per breakpoint. Choose any desktop size in the panel beside this note to see how tablet and mobile will follow along instantly.',
  // Device mockup copy (rebuilt in HTML/CSS instead of the original Lottie)
  mock: {
    headline: ['Type that adapts', 'to any screen'], // 2 lines, hard break (as in the original comp)
    paragraph:
      'Set every size once on desktop and let the ramp settle itself on tablets and phones, keeping headings bold, body copy calm and spacing consistent on any device.',
    button: 'Browse styles',
  },
}

export const presets = {
  title: 'Store your setups|reuse them across files|[in any project.]',
}

export const exportsCopy = {
  title: 'Design and engineering|finally [share one language.]',
  css: 'Every size, line height and spacing value in your ramp can be exported as a tidy block of CSS custom properties, grouped by breakpoint and ready to paste into any stylesheet. Developers get the exact numbers you approved in Figma, with readable names that map onto your text styles, so nothing slips at handoff.',
  ai: 'Coding assistants work better when they understand your typography. The AI Prompt export packs every role, size, weight and breakpoint into a short, structured brief that you can drop into Claude, Cursor, ChatGPT or Lovable. The model then knows which style belongs to a page title, which one suits a caption and how each should respond on smaller screens, so the components it writes follow your system from the first draft instead of inventing values.',
}

export const pricing = {
  title: 'One fee, no [renewals.]',
  plans: [
    {
      name: 'Freelancer',
      subtitle: 'For individual creators',
      license: 'Single License',
      price: '€39,99',
      cta: 'Get Plan',
      variant: 'brand',
      href: 'https://typewave.lemonsqueezy.com/checkout/buy/f38b86ac-2475-4b2b-a7a8-67abd5d7cfec',
      featured: true,
      delay: 0,
    },
    {
      name: 'Studio',
      subtitle: 'Built for studios and crews',
      license: '5 Licenses',
      price: '€159,99',
      cta: 'Get Plan',
      variant: 'brand',
      href: 'https://typewave.lemonsqueezy.com/checkout/buy/65e62acf-90b0-4084-90e6-62ab198548a4',
      delay: 150,
    },
    {
      name: 'Enterprise',
      subtitle: 'Need more licenses?',
      license: 'Custom Licenses',
      price: "Let's talk",
      cta: 'Contact Us',
      variant: 'primary',
      href: 'mailto:hello@blendmodes.com?subject=Typewave%20Enterprise%20Licenses',
      mailto: true,
      delay: 300,
    },
  ],
  includesTitle: 'Everything included',
  includes: [
    ['Preset Library', 'Frame Generation', 'Text Style Output', 'Primitive & Semantic Variable Sets'],
    ['Fully Editable Tokens', 'Three Responsive Breakpoints Built In', 'CSS Variable Output', { text: 'AI Prompt Export', tag: 'NEW' }],
  ],
}

export const EMAIL = 'hello@blendmodes.com'

export const faq = {
  title: 'Questions|[& Answers]',
  items: [
    {
      q: 'What does Typewave actually produce?',
      a: [
        'Typewave builds a complete typographic system inside your file: preview frames for every step, text styles for each role and breakpoint, variables for sizes and line heights, plus CSS and AI Prompt exports. All of them read from one shared set of values.',
        'Change a value once and every output stays in sync, with nothing to update by hand.',
      ],
    },
    {
      q: 'How are tablet and mobile sizes derived?',
      a: [
        'You choose the desktop size for each level and the plugin works out tablet and mobile for you. Instead of shrinking every step by the same percentage, it applies a square-root curve, so large display sizes drop noticeably while body copy and captions stay almost untouched. Each result is then snapped to the nearest value in a fixed token list, which keeps the numbers clean and predictable. You can try the same logic in the small simulator in the breakpoint section above.',
      ],
    },
    {
      q: 'Can I reshape the set of text roles?',
      a: [
        'Yes. Every role can be renamed, reordered or removed, and you can adjust its size, weight, line height and letter spacing at any time. A single project supports up to five font families, so you can pair a display face with a text face and still keep monospace or accent fonts in their own clearly separated groups within the scale.',
      ],
    },
    {
      q: 'How much control do I have over design tokens?',
      a: [
        'Quite a lot. The settings panel lists every token the plugin uses, from the base size and ratio to the individual values assigned to each breakpoint. You can overwrite any of them by hand, lock the ones you want to keep, and regenerate the rest without losing your edits. Changes flow straight into all styles and variables.',
        'If your team already has naming conventions, you can also rename the token groups so they match the structure developers expect in code. The screenshot below shows the token editor with a customised setup.',
      ],
      image: {
        src: '/assets/token-Dmg8Y-M9.png',
        alt: 'Token editor in the plugin settings showing editable size and line-height values per role',
      },
    },
    {
      q: 'Where does the AI Prompt output help me?',
      a: [
        'The AI Prompt is a compact description of your typography written for coding assistants. Paste it into tools like Claude or Cursor and they will reuse your roles, sizes and breakpoints when they generate new interfaces, rather than guessing at values that drift away from the design.',
      ],
    },
    {
      q: 'Why is this a paid plugin?',
      a: [
        'Typewave is built and maintained by a small independent studio. A one-time licence pays for the hours spent fixing bugs, keeping up with Figma API changes and shipping new exports. It also means there are no ads, no tracking and no subscription reminders waiting in your inbox every single month.',
      ],
    },
    {
      q: 'Found a bug or want a feature?',
      // [before, link text = EMAIL, after]
      linkParagraph: [
        'Just send a note to ',
        ' with a description of the issue or the feature you have in mind. Screenshots really help a lot. We read every single message, reply as quickly as we can and use all of the feedback to decide what goes into the next update of the plugin.',
      ],
    },
  ],
}

export const newsletter = {
  title: 'Stay [current]',
  placeholder: 'your@email.com',
}

export const footer = {
  title: 'The [firm footing] for|every launch ahead.',
}
