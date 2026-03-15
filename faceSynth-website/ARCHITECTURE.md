# Architecture FaceSynth Landing Page

## 🏗️ Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│                    FaceSynth Landing Page               │
│                   (Next.js 14 App Router)               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │          app/layout.tsx (Root Layout)           │  │
│  │        - Metadata (SEO, OG, etc.)               │  │
│  │        - Imports globals.css & Tailwind        │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │         app/page.tsx (Home Page)                │  │
│  │      - Compose toutes les sections             │  │
│  │      - Use Client pour interactivité           │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Sections (Composants)               │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ HeroSection (Stateless + useState)        │ │  │
│  │  ├─ Motion animations (framer-motion)        │ │  │
│  │  ├─ LeadCaptureForm (Modal)                 │ │  │
│  │  └─ Grille visuelle interactive             │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ ProblemSolutionSection                    │ │  │
│  │  ├─ Cards avec hover effects                │ │  │
│  │  └─ Motion stagger animations              │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ BenefitsSection (6 cartes)                │ │  │
│  │  ├─ Icons + texte                           │ │  │
│  │  └─ Responsive grid                         │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ PackContentSection (Spécifications)      │ │  │
│  │  ├─ 4 specs principales (grille)            │ │  │
│  │  ├─ Annotations (checklist)                 │ │  │
│  │  └─ Format de livraison (infos)            │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ VariationsSection (Contrôle)             │ │  │
│  │  ├─ 8 dimensions de variation               │ │  │
│  │  └─ Message de confiance                    │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ UseCasesSection (6 cas d'usage)          │ │  │
│  │  ├─ Cards avec icônes                       │ │  │
│  │  └─ Descriptions courtes                    │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ PricingSection (3 plans)                  │ │  │
│  │  ├─ Starter / Pro / Enterprise              │ │  │
│  │  ├─ Plan highlighted (scale-up)            │ │  │
│  │  └─ CTA avec scroll vers contact            │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ ComplianceSection (RGPD / Éthique)       │ │  │
│  │  ├─ 4 garanties principales                 │ │  │
│  │  ├─ Points pour DPO/Compliance              │ │  │
│  │  └─ Call-to-action contact                 │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ FAQSection (Accordéon)                   │ │  │
│  │  ├─ 8 Q&A avec expand/collapse             │ │  │
│  │  └─ Animations smooth                       │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ Footer (Navigation + Liens)              │ │  │
│  │  ├─ Brand + Social links                    │ │  │
│  │  ├─ Sections (Product, Support, Legal)    │ │  │
│  │  └─ Copyright                               │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ LeadCaptureForm (Modal)                  │ │  │
│  │  ├─ Email + Company + Message               │ │  │
│  │  ├─ Validation côté client                 │ │  │
│  │  └─ Submit simulation                       │ │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Composants Utilitaires (Common)            │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ Button (Primary/Secondary/Outline)       │ │  │
│  │  ├─ Props: variant, size, onClick, disabled  │ │  │
│  │  └─ Tailwind + hover effects               │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ Card (Conteneur flexible)                │ │  │
│  │  ├─ Props: children, className, hover      │ │  │
│  │  └─ Bordures + padding + shadows           │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ SectionWrapper (Wrapper animé)          │ │  │
│  │  ├─ Framer Motion: fade-in + slide-up     │ │  │
│  │  ├─ whileInView pour scroll-trigger        │ │  │
│  │  └─ container-main + padding               │ │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Styles Globaux & Tailwind              │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ globals.css                               │ │  │
│  │  ├─ @tailwind directives                    │ │  │
│  │  ├─ Base styles (body, h1, h2, etc.)       │ │  │
│  │  ├─ Component classes (.section-padding)  │ │  │
│  │  └─ Custom animations (@keyframes)         │ │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │ tailwind.config.ts                       │ │  │
│  │  ├─ Couleurs personnalisées                │ │  │
│  │  ├─ Tailles de texte (h1, h2, h3, etc.)  │ │  │
│  │  ├─ Animations (fade-in, slide-up)        │ │  │
│  │  └─ Gradients (gradient-hero)             │ │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

## 📦 Dépendances principales

| Package | Version | Rôle |
|---------|---------|------|
| `next` | 14.x | Framework SSR / App Router |
| `react` | 18.x | UI library |
| `typescript` | 5.x | Type safety |
| `tailwindcss` | 3.x | Utility-first CSS |
| `framer-motion` | 10.x | Animations fluides |
| `clsx` | 2.x | Fusion de classes CSS |
| `postcss` | 8.x | CSS processing |
| `autoprefixer` | 10.x | Vendor prefixes |

## 🎯 Principes de design

### 1. **Hiérarchie d'information**
- Hero : Impact + CTA immédiat
- Problem/Solution : Contexte
- Benefits : Proposition de valeur
- Pack Content : Détails techniques
- Variations : Flexibilité/Contrôle
- Use Cases : Inspiration/Validation
- Pricing : Conversion
- Compliance : Confiance/Sécurité
- FAQ : Objections
- Footer : Navigation générale

### 2. **Animations & Transitions**
- Fade-in + slide-up au scroll avec framer-motion
- Hover effects légers sur boutons/cartes
- Modal smooth pour lead capture
- Accordéon smooth pour FAQ

### 3. **Responsive & Accessibility**
- Mobile-first approach
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
- Sémantique HTML correcte
- ARIA labels où nécessaire
- Contraste de couleurs approprié

### 4. **Performance**
- Code splitting automatique (Next.js)
- CSS-in-JS minimal (Tailwind)
- Images optimisées (next/image si applicable)
- Lazy loading des sections au scroll

## 🔄 Flux d'interaction

### Lead Capture
```
Utilisateur clique CTA principal
       ↓
Modal LeadCaptureForm s'ouvre
       ↓
Utilisateur remplit email (obligatoire)
       ↓
Validation côté client
       ↓
Submit → API (placeholder)
       ↓
Success message
       ↓
Modal ferme après 1.5s
```

### Scroll Trigger Animations
```
Page loads
       ↓
chaque SectionWrapper écoute whileInView
       ↓
Utilisateur scroll vers section
       ↓
Component apparaît en viewport
       ↓
Animation fade-in + slide-up déclenche
```

## 🛠️ Stack technique détaillé

### Build & Development
- **Next.js 14** : App Router (SSR/SSG)
- **TypeScript** : Full type safety
- **Tailwind CSS** : Utility-first styling
- **PostCSS** : CSS preprocessing
- **Framer Motion** : Animation library

### Code Quality
- **ESLint** : Linting (via Next.js)
- **TypeScript strict mode** : Type checking strict
- **EditorConfig** : Cohérence style de code

### Deployment
- **Vercel** : Hosting recommandé
- **Docker** : Alternative containerized
- **Environment variables** : `.env.local`

## 📊 Performance Budget

- Lighthouse Performance: >90
- First Contentful Paint (FCP): <2s
- Largest Contentful Paint (LCP): <2.5s
- Cumulative Layout Shift (CLS): <0.1

---

**Architecture pensée pour l'extensibilité, la performance et la maintenabilité.**
