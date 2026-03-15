# FaceSynth Landing Page

Landing page moderna e interattiva per **FaceSynth – RGPD Synthetic Face Pack**.

## 📋 Descrizione

Un sito web moderno costruito con **Next.js 14**, **TypeScript**, **Tailwind CSS** e **framer-motion**. Presenta il prodotto FaceSynth (dataset di volti sintetici 100% RGPD) a team di computer vision, AI, e R&D.

## 🎯 Funzionalità

- ✨ **Hero Section** con visuale interattiva di volti sintetici
- 📊 **Sections strutturate**: Problema/Soluzione, Benefici, Contenuto Pack, Variazioni, Casi d'uso, Pricing, Compliance, FAQ
- 🎨 **Design moderno**: Palette blu/indigo, design responsive mobile-first
- 🎬 **Animazioni smooth**: Fade-in e slide-up al scroll con framer-motion
- 📝 **Form capture leads**: Modal con validazione email
- ♿ **Accessibilità**: HTML semantico, buona gerarchia visiva
- 📱 **Responsive**: Ottimizzato per mobile, tablet, desktop

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Linguaggio**: TypeScript
- **Styling**: Tailwind CSS
- **Animazioni**: framer-motion
- **Utilities**: clsx

## 📦 Installazione

```bash
# Clonare il repository
git clone <repo-url>
cd faceSynth-website

# Installare dipendenze
npm install

# Avviare dev server
npm run dev

# Build per produzione
npm run build
npm start
```

Il sito sarà disponibile a `http://localhost:3000`.

## 📁 Struttura del Progetto

```
faceSynth-website/
├── app/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx           # Button component riutilizzabile
│   │   │   ├── Card.tsx             # Card component
│   │   │   └── SectionWrapper.tsx   # Wrapper con animazioni
│   │   ├── HeroSection.tsx
│   │   ├── ProblemSolutionSection.tsx
│   │   ├── BenefitsSection.tsx
│   │   ├── PackContentSection.tsx
│   │   ├── VariationsSection.tsx
│   │   ├── UseCasesSection.tsx
│   │   ├── PricingSection.tsx
│   │   ├── ComplianceSection.tsx
│   │   ├── FAQSection.tsx
│   │   ├── LeadCaptureForm.tsx      # Modal form
│   │   └── Footer.tsx
│   ├── layout.tsx                  # Root layout
│   ├── globals.css                 # Stili globali
│   └── page.tsx                    # Homepage
├── public/                         # Assets statici
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── next.config.js
```

## 🎨 Design & Colori

- **Sfondo principale**: Bianco/grigio molto chiaro (`#f9fafb`)
- **Accenti primari**: Blu (`#2563eb`)
- **Accenti secondari**: Blu-violetto (`#6366f1`)
- **Testo**: Grigio scuro (`#1f2937`)
- **Testo secondario**: Grigio medio (`#6b7280`)

## 🔧 Configurazione

### Tailwind CSS
Personalizzare i colori e le varianti in `tailwind.config.ts`.

### Framer Motion
Le animazioni sono integrate nei componenti di sezione tramite `<motion.*>`. Modifica `initial`, `animate`, `transition` per personalizzare.

## 📝 Contenuto

Tutto il contenuto è in **francese**. Per tradurre:

1. Creare una struttura i18n (es. con `next-intl`)
2. Estrarre stringhe in file JSON
3. Integrare la libreria di traduzione

## 🚀 Deployment

### Vercel (consigliato)
```bash
vercel deploy
```

### Docker
```bash
docker build -t facesynth-landing .
docker run -p 3000:3000 facesynth-landing
```

### Altre piattaforme
Compatible con Netlify, AWS Amplify, etc. Segui le loro guide di deployment Next.js.

## 🔐 Variabili d'ambiente

Creare un file `.env.local`:
```
NEXT_PUBLIC_API_URL=https://api.facesynth.io
```

## 📊 Performance

- Lighthouse score target: >90 (Performance, Accessibility, Best Practices, SEO)
- Immagini ottimizzate con `next/image`
- Code splitting automatico con Next.js
- CSS-in-JS minimized

## 🤝 Contribuzioni

Per contribuire:
1. Fork il repo
2. Crea un branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m 'Add feature'`
4. Push: `git push origin feature/my-feature`
5. Apri una Pull Request

## 📄 License

MIT License – Vedi il file `LICENSE`.

## 📧 Support

Per domande o feedback:
- Email: contact@facesynth.io
- LinkedIn: [FaceSynth](https://linkedin.com)
- Twitter: [@FaceSynth](https://twitter.com)

---

**Made with ❤️ for the AI/CV community.**
