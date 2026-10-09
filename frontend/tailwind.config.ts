import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        canvas: '#0a0a0a',
        'canvas-soft': '#1a1c20',
        'canvas-card': '#191919',
        hairline: '#212327',
        ink: '#ffffff',
        'ink-hover': '#fafaf7',
        body: '#dadbdf',
        'body-mid': '#7d8187',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        mono: ['var(--font-geist-mono)', 'monospace'],
      },
      letterSpacing: {
        'tighter-2': '-0.04em',
        'tight-1': '-0.02em',
        'wide-1': '0.1em',
      },
    },
  },
  plugins: [],
}
export default config
