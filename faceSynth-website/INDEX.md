# 📑 FaceSynth Landing Page - Index & Guide de navigation

Bienvenue ! Voici comment naviguer dans la documentation et le code du projet FaceSynth.

---

## 🚀 Par où commencer ?

### 🟢 Je veux lancer le site immédiatement
→ **[QUICKSTART.md](./QUICKSTART.md)**
- Installation en 5 min
- Deployment (Vercel ou Docker)
- Customisation basique

### 🟡 Je veux comprendre l'architecture
→ **[ARCHITECTURE.md](./ARCHITECTURE.md)**
- Vue d'ensemble structure
- Flux d'interaction
- Stack technique détaillée

### 🟠 Je veux développer / customiser
→ **[DEVELOPMENT.md](./DEVELOPMENT.md)**
- Ajouter une section
- Intégrations (API, i18n)
- Debugging & testing

### 🔴 Je veux tous les détails
→ **[README.md](./README.md)** puis **[STRUCTURE.md](./STRUCTURE.md)**

---

## 📚 Index des documents

### Documentation Générale
| Doc | Description | Lisez si... |
|-----|-------------|------------|
| **[QUICKSTART.md](./QUICKSTART.md)** | Setup rapide | Vous commencez (5 min) |
| **[README.md](./README.md)** | Guide principal | Vous voulez l'overview |
| **[DEVELOPMENT.md](./DEVELOPMENT.md)** | Dev guide | Vous allez modifier le code |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Architecture | Vous voulez comprendre en détail |
| **[STRUCTURE.md](./STRUCTURE.md)** | Structure fichiers | Vous cherchez un fichier spécifique |
| **[LAUNCH_CHECKLIST.md](./LAUNCH_CHECKLIST.md)** | Checklist lancement | Vous préparez le déploiement |
| **[FILES_INVENTORY.md](./FILES_INVENTORY.md)** | Liste complète | Vous voulez savoir ce qui existe |
| **[INDEX.md](./INDEX.md)** | Ce fichier | Vous vous repérez 😊 |

### Fichiers de Configuration
| Fichier | Rôle | À modifier ? |
|---------|------|------------|
| `package.json` | Dépendances npm | Rarement |
| `tsconfig.json` | TypeScript | Rarement |
| `tailwind.config.ts` | **Tailwind (couleurs, fonts)** | **OUI, pour design** |
| `next.config.js` | Next.js | Rarement |
| `postcss.config.js` | PostCSS | Rarement |
| `.env.example` / `.env.local` | **Env variables** | **OUI, pour production** |

---

## 🗂️ Structure du Projet

```
faceSynth-website/
│
├── 📖 DOCS (vous êtes ici)
│   ├── QUICKSTART.md ..................... Démarrage rapide
│   ├── README.md ......................... Vue générale
│   ├── DEVELOPMENT.md ................... Développement
│   ├── ARCHITECTURE.md .................. Architecture détaillée
│   ├── STRUCTURE.md ..................... Structure fichiers
│   ├── LAUNCH_CHECKLIST.md .............. Checklist lancement
│   ├── FILES_INVENTORY.md ............... Inventory complet
│   └── INDEX.md (ce fichier) ............ Navigation
│
├── 🔧 CONFIG
│   ├── package.json ..................... Dépendances
│   ├── tsconfig.json .................... TypeScript
│   ├── tailwind.config.ts ............... Styles (CUSTOMISER ICI)
│   ├── next.config.js ................... Next.js
│   ├── postcss.config.js ................ PostCSS
│   ├── .editorconfig .................... Format code
│   ├── .eslintrc.json ................... Linting
│   ├── .npmrc ........................... npm config
│   ├── Dockerfile ....................... Docker build
│   ├── vercel.json ...................... Vercel config
│   ├── .env.example ..................... Env template (COPIER EN .env.local)
│   └── .gitignore ....................... Git ignore rules
│
├── 🎨 APP CODE
│   └── app/
│       ├── layout.tsx ................... Root layout + metadata
│       ├── globals.css .................. Styles globaux
│       ├── page.tsx ..................... Homepage
│       │
│       ├── components/
│       │   ├── common/
│       │   │   ├── Button.tsx ........... Component bouton
│       │   │   ├── Card.tsx ............ Component carte
│       │   │   └── SectionWrapper.tsx ... Component section
│       │   │
│       │   ├── HeroSection.tsx
│       │   ├── ProblemSolutionSection.tsx
│       │   ├── BenefitsSection.tsx
│       │   ├── PackContentSection.tsx
│       │   ├── VariationsSection.tsx
│       │   ├── UseCasesSection.tsx
│       │   ├── PricingSection.tsx
│       │   ├── ComplianceSection.tsx
│       │   ├── FAQSection.tsx
│       │   ├── Footer.tsx
│       │   └── LeadCaptureForm.tsx
│       │
│       ├── hooks/
│       │   └── useScrollAnimation.ts .... Custom hooks
│       │
│       ├── types/
│       │   └── index.ts ................ TypeScript types
│       │
│       └── constants/
│           └── site.ts ................. Config + textes
│
├── 🌐 PUBLIC (Assets)
│   ├── favicon.ico ..................... Site icon
│   ├── robots.txt ...................... SEO crawlers
│   ├── sitemap.xml ..................... SEO sitemap
│   ├── manifest.json ................... PWA config
│   └── icon-*.png ...................... PWA icons
│
└── node_modules/ & .next/ .............. Auto-généré (npm install, npm build)
```

---

## 🎯 Tasks courants & où aller

### "Je veux changer les couleurs"
1. Ouvrir `tailwind.config.ts`
2. Modifier la section `colors`
3. Restart dev server
→ Doc complète: [DEVELOPMENT.md - Customization](./DEVELOPMENT.md)

### "Je veux ajouter une section"
1. Créer `app/components/MySection.tsx`
2. Importer dans `app/page.tsx`
3. L'ajouter au JSX
→ Doc complète: [DEVELOPMENT.md - Add Section](./DEVELOPMENT.md)

### "Je veux déployer"
1. Lire [LAUNCH_CHECKLIST.md](./LAUNCH_CHECKLIST.md)
2. Ou lancer `vercel deploy` (Vercel)
3. Ou `docker build && docker run` (Docker)
→ Doc complète: [QUICKSTART.md - Deploy](./QUICKSTART.md)

### "Je veux comprendre comment ça marche"
→ [ARCHITECTURE.md](./ARCHITECTURE.md)

### "Je veux voir tous les fichiers créés"
→ [FILES_INVENTORY.md](./FILES_INVENTORY.md)

### "J'ai un problème"
1. Vérifier [QUICKSTART.md - Troubleshooting](./QUICKSTART.md)
2. Lire les comments dans le code
3. Consulter [DEVELOPMENT.md - Debugging](./DEVELOPMENT.md)

---

## 🎓 Apprentissage par niveau

### Débutant - "Je veux juste lancer le site"
1. [QUICKSTART.md](./QUICKSTART.md) - 5 min
2. `npm install && npm run dev`
3. C'est prêt !

### Intermédiaire - "Je veux le customiser"
1. [QUICKSTART.md](./QUICKSTART.md) - Setup
2. [STRUCTURE.md](./STRUCTURE.md) - Où sont les fichiers
3. [DEVELOPMENT.md](./DEVELOPMENT.md) - Comment modifier
4. Commencer avec `tailwind.config.ts` (couleurs) et `app/constants/site.ts` (textes)

### Avancé - "Je veux développer dessus"
1. [README.md](./README.md) - Vue générale
2. [ARCHITECTURE.md](./ARCHITECTURE.md) - Architecture
3. [DEVELOPMENT.md](./DEVELOPMENT.md) - Patterns & conventions
4. Explorer `app/components/` pour les exemples

### Expert - "Je dois tout refactor"
1. [ARCHITECTURE.md](./ARCHITECTURE.md) - Vue d'ensemble
2. [STRUCTURE.md](./STRUCTURE.md) - Structure complète
3. Code des composants
4. Modifier selon vos besoins

---

## 🚀 Checklist de démarrage

```bash
# 1. Clone/navigate
cd faceSynth-website

# 2. Install
npm install

# 3. Setup env
cp .env.example .env.local

# 4. Dev
npm run dev

# 5. Ouvrir
open http://localhost:3000

# 6. Customiser
# → Éditer tailwind.config.ts (couleurs)
# → Éditer app/constants/site.ts (textes)

# 7. Build
npm run build
npm start

# 8. Deploy
vercel deploy
```

---

## 📞 Support & Ressources

### Documentation
- **Next.js** : https://nextjs.org/docs
- **Tailwind CSS** : https://tailwindcss.com
- **Framer Motion** : https://www.framer.com/motion/
- **TypeScript** : https://www.typescriptlang.org/

### Fichiers Clés
- Couleurs/Design : `tailwind.config.ts`
- Textes/Config : `app/constants/site.ts`
- Pages : `app/page.tsx` et `app/components/`
- Styles : `app/globals.css`

### Problèmes ?
1. Consulter [DEVELOPMENT.md - Debugging](./DEVELOPMENT.md)
2. Vérifier les comments dans le code
3. Google search + Stack Overflow

---

## 📊 Vue d'ensemble rapide

| Aspect | Tech | Où |
|--------|------|-----|
| Framework | Next.js 14 App Router | `next.config.js` |
| Language | TypeScript | `tsconfig.json` |
| Styling | Tailwind CSS | `tailwind.config.ts` |
| Animations | Framer Motion | `app/components/` |
| Types | TypeScript interfaces | `app/types/index.ts` |
| Constants | Config centralisée | `app/constants/site.ts` |
| Hosting | Vercel (recommandé) | `vercel.json` |

---

## ✨ Prochaines étapes recommandées

### Immédiatement
- [ ] `npm install`
- [ ] `npm run dev`
- [ ] Tester sur http://localhost:3000

### Avant deployment
- [ ] Lire [LAUNCH_CHECKLIST.md](./LAUNCH_CHECKLIST.md)
- [ ] Customiser couleurs/textes
- [ ] Tester sur tous les devices
- [ ] Build + test prod: `npm run build && npm start`

### Après deployment
- [ ] Configurer monitoring
- [ ] Configurer analytics
- [ ] Tester les leads capture
- [ ] Itérer basé sur feedback

---

**Bon travail ! Vous avez tout ce qu'il faut pour réussir. 🎉**

Pour les questions : consultez la documentation appropriée ou explorez le code (il est bien commenté).
