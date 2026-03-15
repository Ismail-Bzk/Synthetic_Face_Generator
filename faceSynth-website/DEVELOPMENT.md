# Guide de Développement - FaceSynth Landing Page

## 🚀 Démarrage rapide

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev

# Ouvrir http://localhost:3000
```

## 📋 Structure des composants

Tous les composants sont dans `app/components/` :

### Composants utilitaires (`common/`)
- `Button.tsx` : Bouton réutilisable avec variantes
- `Card.tsx` : Conteneur de contenu avec hover optionnel
- `SectionWrapper.tsx` : Wrapper de section avec animations framer-motion

### Sections principales
- `HeroSection.tsx` : Hero avec grille visuelle
- `ProblemSolutionSection.tsx` : Problèmes et solutions
- `BenefitsSection.tsx` : 6 bénéfices clés
- `PackContentSection.tsx` : Détail du contenu et annotations
- `VariationsSection.tsx` : Contrôle des distributions
- `UseCasesSection.tsx` : 6 cas d'usage
- `PricingSection.tsx` : 3 plans de pricing
- `ComplianceSection.tsx` : RGPD et garanties
- `FAQSection.tsx` : 8 questions/réponses
- `Footer.tsx` : Pied de page
- `LeadCaptureForm.tsx` : Modal de capture de leads

## 🎨 Personnalisation du design

### Couleurs
Modifiez `tailwind.config.ts` :
```ts
colors: {
  'primary-blue': '#2563eb',      // Changez cette couleur
  'primary-indigo': '#6366f1',    // Et celle-ci
  // ... autres couleurs
}
```

### Typographie
```ts
fontSize: {
  'h1': '3rem',  // Modifiez les tailles
  'h2': '2.25rem',
  'body': '1rem',
}
```

### Animations
Dans n'importe quel composant avec `motion` :
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}  // État initial
  whileInView={{ opacity: 1, y: 0 }}  // État au scroll
  transition={{ duration: 0.6 }}  // Durée
>
  Content
</motion.div>
```

## 📝 Ajouter une nouvelle section

1. Créer le composant dans `app/components/YourSection.tsx`
2. Importer dans `app/page.tsx`
3. Ajouter la section dans le JSX

Exemple :
```tsx
// app/components/MySection.tsx
'use client';
import { SectionWrapper } from './common/SectionWrapper';

export const MySection: React.FC = () => {
  return (
    <SectionWrapper bgColor="white">
      <h2 className="text-h2">Mon titre</h2>
      <p>Mon contenu</p>
    </SectionWrapper>
  );
};
```

Puis dans `app/page.tsx` :
```tsx
import { MySection } from './components/MySection';

export default function Home() {
  return (
    <main>
      {/* ... autres sections */}
      <MySection />
    </main>
  );
}
```

## 🔧 Configuration avancée

### Variables d'environnement
Créer `.env.local` :
```
NEXT_PUBLIC_API_URL=https://api.facesynth.io
NEXT_PUBLIC_CONTACT_EMAIL=contact@facesynth.io
```

Utiliser :
```tsx
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Intégration API

Exemple pour envoyer le formulaire vers un backend :
```tsx
// app/components/LeadCaptureForm.tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  const response = await fetch('/api/leads', {
    method: 'POST',
    body: JSON.stringify({ email, company, message }),
  });
  
  if (response.ok) {
    setSubmitted(true);
  }
};
```

### I18n (Internationalisation)

Pour supporter plusieurs langues, utiliser [`next-intl`](https://next-intl-docs.vercel.app/) :

```bash
npm install next-intl
```

Structurer les traductions :
```
/app/i18n/
├── fr.json
├── en.json
└── es.json
```

## 🧪 Testing

### Linting et formatage
```bash
# Vérifier les erreurs TypeScript
npm run lint

# Formatter le code
npm run format  # (à configurer avec Prettier)
```

### Build production
```bash
npm run build
npm start
```

## 🚢 Déploiement

### Vercel (recommandé)
```bash
# Installer Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Docker
```bash
docker build -t facesynth .
docker run -p 3000:3000 facesynth
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

## 🐛 Debugging

### Console du navigateur
```tsx
// Utiliser console.log dans les composants
const MyComponent = () => {
  useEffect(() => {
    console.log('Component mounted');
  }, []);
  
  return <div>...</div>;
};
```

### React DevTools
Installer l'extension React DevTools pour inspecter les props et state.

### Performance
```bash
# Vérifier le score Lighthouse
npm run build
npm start
# Ouvrir DevTools → Lighthouse → Analyze page load
```

## 📚 Ressources

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [TypeScript](https://www.typescriptlang.org/docs/)

## 🤝 Contribution

1. Créer une branche : `git checkout -b feature/ma-feature`
2. Commit : `git commit -m "Add ma-feature"`
3. Push : `git push origin feature/ma-feature`
4. PR sur main

---

**Bon code ! 🎉**
