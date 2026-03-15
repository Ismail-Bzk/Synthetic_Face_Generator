/**
 * Constantes et données de configuration du site FaceSynth
 */

export const SITE_CONFIG = {
  name: 'FaceSynth',
  title: 'FaceSynth – RGPD Synthetic Face Pack',
  description: 'Dataset de visages synthétiques 100% RGPD pour entraîner vos modèles de computer vision sans données personnelles.',
  domain: 'facesynth.io',
  contactEmail: 'contact@facesynth.io',
  supportEmail: 'support@facesynth.io',
  phone: '+33 (0) 1 XX XX XX XX',
};

export const HERO_COPY = {
  mainTitle: 'Entraînez vos modèles IA avec confiance, sans données personnelles',
  subtitle: 'FaceSynth fournit des milliers de visages synthétiques réalistes, entièrement annotés et 100% conformes RGPD. Entraînez vos modèles de vision par ordinateur rapidement, sans risques juridiques ni obstacles éthiques.',
  ctas: [
    { label: 'Obtenir un sample pack', variant: 'primary' },
    { label: 'Demander une démo', variant: 'secondary' },
  ],
};

export const FEATURES_QUICK = [
  '✓ Aucune donnée personnelle réelle',
  '✓ Annotations riches (pose, regard, expression, etc.)',
  '✓ Livraison immédiate en haute résolution',
];

export const PROBLEMS = [
  {
    title: 'Collecte coûteuse et risquée',
    description: 'Accès limité aux données réelles, consentements à gérer, risques légaux importants.',
    icon: '⚠️',
  },
  {
    title: 'Contraintes réglementaires',
    description: 'CNIL, IRB, RGPD : des obstacles administratifs complexes et chronophages.',
    icon: '⚖️',
  },
  {
    title: 'Biais des datasets publics',
    description: 'Manque de diversité contrôlée, représentation non équitable, reproduction difficile.',
    icon: '📊',
  },
];

export const SOCIAL_LINKS = {
  linkedin: 'https://linkedin.com/company/facesynth',
  twitter: 'https://twitter.com/facesynth_ai',
  github: 'https://github.com/facesynth',
};

export const NAVIGATION_LINKS = [
  { label: 'Caractéristiques', href: '#features' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Docs', href: '#docs' },
  { label: 'Contact', href: '#contact' },
];
