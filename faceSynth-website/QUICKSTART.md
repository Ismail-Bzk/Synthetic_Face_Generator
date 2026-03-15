# 🚀 Quick Start - FaceSynth Landing Page

Prêt à lancer le site ? Voici le minimum pour démarrer.

## ⚡ Installation (5 minutes)

```bash
# 1. Aller au dossier du projet
cd faceSynth-website

# 2. Installer les dépendances
npm install

# 3. Copier env example
cp .env.example .env.local

# 4. Lancer le dev server
npm run dev

# 5. Ouvrir http://localhost:3000 ✓
```

## 🎨 Customisation rapide

### Changer les couleurs
📁 `tailwind.config.ts` → Modifiez `colors` :
```ts
'primary-blue': '#YOUR_COLOR',
'primary-indigo': '#YOUR_SECONDARY',
```

### Changer le texte principal
📁 `app/constants/site.ts` → Modifiez `SITE_CONFIG` et `HERO_COPY`

### Ajouter votre logo
📁 `public/` → Mettez votre `favicon.ico` (32×32) et icons PWA

### Changer la description SEO
📁 `app/layout.tsx` → Modifiez `metadata`

## 📝 Contenu à personnaliser

**Sections à traduire / adapter :**

| Fichier | Section |
|---------|---------|
| `app/components/HeroSection.tsx` | Titre, sous-titre, CTA |
| `app/constants/site.ts` | Config produit |
| `app/components/Footer.tsx` | Liens, contact |
| Tous les `.tsx` | Descriptions, textes |

## 🚀 Déploiement (2 options)

### Option 1 : Vercel (Facile ⭐⭐⭐)
```bash
npm install -g vercel
vercel
# Suivre les prompts, c'est automatique !
```

### Option 2 : Docker
```bash
docker build -t facesynth .
docker run -p 3000:3000 facesynth
# http://localhost:3000
```

## ✅ Avant de déployer

```bash
# 1. Build final
npm run build

# 2. Vérifier les erreurs
npm run lint

# 3. Test production local
npm start

# 4. Vérifier la responsivité (Dev Tools → F12)
```

## 📚 Documentation

| Document | Pour |
|----------|------|
| `README.md` | Vue générale + installation |
| `DEVELOPMENT.md` | Customisation et extension |
| `ARCHITECTURE.md` | Comment ça marche |
| `LAUNCH_CHECKLIST.md` | Avant/après lancement |

## 🆘 Problèmes courants

### ❌ `npm install` échoue
```bash
# Supprimer cache
rm -rf node_modules package-lock.json
npm install
```

### ❌ `npm run dev` erreur TypeScript
```bash
# Vérifier les versions dans package.json
npm install
```

### ❌ Styles Tailwind ne s'appliquent pas
- Vérifier `app/globals.css` a les directives `@tailwind`
- Vérifier `tailwind.config.ts` a le bon `content` path

### ❌ Images ne s'affichent pas
- Vérifier le chemin dans `public/`
- Utiliser `<img>` ou `<Image>` de Next.js

## 💡 Tips

- **Animations smooth ?** C'est framer-motion, tous les composants les ont
- **Responsive ok ?** Testé sur mobile/tablet/desktop
- **SEO optimisé ?** Metadata + sitemap + robots.txt déjà inclus
- **Formulaire leads ?** Prêt, à connecter à votre backend

## 🔧 Customisation avancée

Pour des changements plus complexes :
→ Voir `DEVELOPMENT.md`

Pour l'architecture en détail :
→ Voir `ARCHITECTURE.md`

Pour la liste complète des fichiers :
→ Voir `FILES_INVENTORY.md`

---

**Vous êtes prêt ! 🎉**

**Questions ?** Consultez la documentation complète ou les comments dans le code.
