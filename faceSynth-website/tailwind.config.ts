import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Palette personnalisée pour FaceSynth
        'primary-blue': '#2563eb',      // Bleu principal
        'primary-indigo': '#6366f1',    // Bleu-violet pour les accents
        'neutral-bg': '#f9fafb',        // Fond très clair
        'neutral-card': '#ffffff',      // Cartes blanches
        'neutral-border': '#e5e7eb',    // Bordures grises légères
        'neutral-text': '#1f2937',      // Texte sombre
        'neutral-subtext': '#6b7280',   // Texte secondaire
      },
      fontSize: {
        'h1': '3rem',
        'h2': '2.25rem',
        'h3': '1.875rem',
        'body': '1rem',
        'small': '0.875rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-in-out',
        'slide-up': 'slideUp 0.6s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backgroundImage: {
        'gradient-hero': 'linear-gradient(135deg, #f3f4f6 0%, #e0e7ff 100%)',
      },
    },
  },
  plugins: [],
};

export default config;
