# 📁 Structure complète du projet FaceSynth

## Vue d'ensemble de la structure

```
faceSynth-website/
│
├── 📄 Configuration & Build
│   ├── package.json                    # Dépendances npm et scripts
│   ├── tsconfig.json                   # Configuration TypeScript
│   ├── next.config.js                  # Configuration Next.js
│   ├── tailwind.config.ts              # Configuration Tailwind CSS
│   ├── postcss.config.js               # Configuration PostCSS
│   ├── .editorconfig                   # Configuration éditeur
│   ├── .gitignore                      # Fichiers ignorés Git
│   ├── vercel.json                     # Configuration Vercel deployment
│   ├── Dockerfile                      # Configuration Docker
│   └── .env.example                    # Template variables d'environnement
│
├── 📚 Documentation
│   ├── README.md                       # Guide général du projet
│   ├── DEVELOPMENT.md                  # Guide de développement
│   ├── ARCHITECTURE.md                 # Architecture détaillée
│   ├── LAUNCH_CHECKLIST.md            # Checklist pré-lancement
│   └── STRUCTURE.md                    # Ce fichier
│
├── 🎨 App Directory (Next.js 14 App Router)
│   ├── layout.tsx                      # Root layout (metadata, imports CSS)
│   ├── globals.css                     # Styles globaux + Tailwind
│   ├── page.tsx                        # Page d'accueil (agrège toutes les sections)
│   │
│   ├── 🔧 components/
│   │   │
│   │   ├── 📦 common/ (Composants utilitaires réutilisables)
│   │   │   ├── Button.tsx              # Bouton avec variantes (primary/secondary/outline)
│   │   │   ├── Card.tsx                # Conteneur de contenu avec hover optionnel
│   │   │   └── SectionWrapper.tsx      # Wrapper de section avec animations
│   │   │
│   │   ├── 📄 Sections principales
│   │   │   ├── HeroSection.tsx         # Hero avec grille visuelle + CTA
│   │   │   ├── ProblemSolutionSection.tsx    # Problèmes vs solutions
│   │   │   ├── BenefitsSection.tsx     # 6 bénéfices clés
│   │   │   ├── PackContentSection.tsx  # Détail du contenu + annotations
│   │   │   ├── VariationsSection.tsx   # Contrôle des distributions
│   │   │   ├── UseCasesSection.tsx     # 6 cas d'usage
│   │   │   ├── PricingSection.tsx      # 3 plans de pricing
│   │   │   ├── ComplianceSection.tsx   # RGPD / Éthique / Garanties
│   │   │   └── FAQSection.tsx          # 8 Q&A avec accordéon
│   │   │
│   │   ├── LeadCaptureForm.tsx         # Modal de capture de leads
│   │   └── Footer.tsx                  # Pied de page avec liens
│   │
│   ├── 📚 hooks/ (Custom React hooks)
│   │   └── useScrollAnimation.ts       # Hook pour animations au scroll
│   │
│   ├── 🎯 constants/ (Constantes et données)
│   │   └── site.ts                     # Config produit, textes, liens
│   │
│   ├── 🔤 types/ (TypeScript types/interfaces)
│   │   └── index.ts                    # Types réutilisables (PricingPlan, Feature, etc.)
│   │
│   └── 📁 api/ (API routes - optionnel)
│       └── leads.ts (à créer)          # Endpoint pour soumettre les leads
│
├── 🌐 public/ (Assets statiques)
│   ├── favicon.ico                     # Favicon du site
│   ├── robots.txt                      # Règles pour les crawlers
│   ├── sitemap.xml                     # Sitemap XML pour SEO
│   ├── manifest.json                   # PWA manifest
│   ├── icon-192.png                    # PWA icon 192×192 (placeholder)
│   ├── icon-512.png                    # PWA icon 512×512 (placeholder)
│   ├── icon-192-maskable.png           # PWA maskable icon 192 (placeholder)
│   ├── icon-512-maskable.png           # PWA maskable icon 512 (placeholder)
│   ├── screenshot-wide.png             # PWA screenshot wide (placeholder)
│   └── screenshot-narrow.png           # PWA screenshot narrow (placeholder)
│
└── 🔄 Node modules & Cache (auto-généré)
    ├── node_modules/                   # Dépendances npm
    ├── .next/                          # Build cache Next.js
    └── .env.local                      # Variables d'environnement locales (gitignored)
```

## 📋 Description détaillée des fichiers clés

### Configuration
| Fichier | Rôle | Customization |
|---------|------|---------------|
| `package.json` | Dépendances et scripts | Versions, nouvelles dépendances |
| `tsconfig.json` | TypeScript config | Strict mode, paths |
| `tailwind.config.ts` | Couleurs, tailles, animations | Palette, breakpoints |
| `next.config.js` | Next.js config | Image optimization, middleware |
| `postcss.config.js` | CSS processing | Plugins additionnels |

### Composants par rôle

#### Common (Réutilisables)
- `Button.tsx` : Réduit la duplication pour tous les boutons
- `Card.tsx` : Conteneur cohérent pour le contenu
- `SectionWrapper.tsx` : Animatinos + containers répétitives

#### Sections (Métier)
- `HeroSection` : Impact premier écran
- `ProblemSolutionSection` : Contexte
- `BenefitsSection` : Proposition de valeur
- `PackContentSection` : Détails techniques
- `VariationsSection` : Flexibilité produit
- `UseCasesSection` : Inspiration
- `PricingSection` : Conversion
- `ComplianceSection` : Confiance
- `FAQSection` : Objections
- `Footer` : Navigation générale
- `LeadCaptureForm` : Capture de leads

### Styles & Theming

```
globals.css
├── @tailwind base (styles base HTML)
├── @tailwind components (classes custom)
└── @tailwind utilities (classes Tailwind)
   └── Custom @layer pour .container-main, .section-padding, .glow-*

tailwind.config.ts
├── colors (primary-blue, primary-indigo, neutral-*)
├── fontSize (h1, h2, h3, body, small)
├── animations (fade-in, slide-up)
└── backgroundImage (gradient-hero)
```

### Assets Statiques (public/)

**SEO & Crawling**
- `robots.txt` : Règles pour les bots
- `sitemap.xml` : Index des pages

**PWA & Manifest**
- `manifest.json` : Configuration PWA installable
- `icon-*.png` : Icons pour PWA

**Favicon**
- `favicon.ico` : Icône navigateur

## 🔧 Comment ajouter une nouvelle section

1. Créer `app/components/NewSection.tsx`
   ```tsx
   'use client';
   import { SectionWrapper } from './common/SectionWrapper';
   
   export const NewSection: React.FC = () => {
     return (
       <SectionWrapper bgColor="white">
         <h2 className="text-h2">Mon titre</h2>
         {/* Content */}
       </SectionWrapper>
     );
   };
   ```

2. Importer dans `app/page.tsx`
   ```tsx
   import { NewSection } from './components/NewSection';
   ```

3. Ajouter dans le JSX principal
   ```tsx
   export default function Home() {
     return (
       <main>
         {/* autres sections */}
         <NewSection />
       </main>
     );
   }
   ```

## 📦 Installation & Setup

```bash
# 1. Clone
git clone <repo-url>
cd faceSynth-website

# 2. Install
npm install

# 3. Setup env
cp .env.example .env.local
# Modifier .env.local avec vos valeurs

# 4. Dev
npm run dev
# http://localhost:3000

# 5. Build
npm run build
npm start

# 6. Deploy
vercel deploy
```

## 🎨 Conventions & Patterns

### Naming
- Components : PascalCase (`HeroSection.tsx`)
- Files : Same as export + `.tsx`
- Hooks : Prefix `use` (`useScrollAnimation.ts`)
- Constants : UPPER_SNAKE_CASE (`SITE_CONFIG`)

### Styling
- Utiliser Tailwind classes autant que possible
- Custom CSS seulement dans `globals.css` si nécessaire
- Colors du palette : `text-primary-blue`, `bg-neutral-bg`

### Components
- Toujours ajouter `'use client'` pour les composants interactifs
- Props typées avec TypeScript interface
- Render functions pure (pas d'effets de bord)

### Animations
- Framer Motion pour les entrées/sorties
- `whileInView` pour scroll-trigger
- `transition` toujours défini

## 📊 Performance Targets

| Métrique | Target |
|----------|--------|
| Lighthouse Performance | >90 |
| FCP (First Contentful Paint) | <2s |
| LCP (Largest Contentful Paint) | <2.5s |
| CLS (Cumulative Layout Shift) | <0.1 |
| Bundle Size (gzipped) | <500KB |

## 🚀 Déploiement

### Vercel (Recommandé)
- Zero config
- Auto-deploys on push
- Serverless functions for API

### Docker
```bash
docker build -t facesynth .
docker run -p 3000:3000 facesynth
```

### Netlify
- Configure build: `npm run build`
- Publish: `.next`

## 📧 Support & Contact

Pour toute question sur la structure ou les patterns :
- Consultez `DEVELOPMENT.md`
- Consultez `ARCHITECTURE.md`
- Vérifiez les comments inline dans les composants

---

**Projet maintenu avec ❤️ pour la communauté AI/CV**
