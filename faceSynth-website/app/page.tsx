'use client';

import React from 'react';
import { HeroSection } from './components/HeroSection';
import { ProblemSolutionSection } from './components/ProblemSolutionSection';
import { BenefitsSection } from './components/BenefitsSection';
import { PackContentSection } from './components/PackContentSection';
import { VariationsSection } from './components/VariationsSection';
import { UseCasesSection } from './components/UseCasesSection';
import { PricingSection } from './components/PricingSection';
import { ComplianceSection } from './components/ComplianceSection';
import { FAQSection } from './components/FAQSection';
import { Footer } from './components/Footer';

/**
 * Page d'accueil principale de FaceSynth
 * Agrège toutes les sections dans un flow cohérent et attrayant
 */
export default function Home() {
  return (
    <main className="bg-neutral-bg">
      {/* Hero Section - Impact immédiat */}
      <HeroSection />

      {/* Problem / Solution - Contextualization */}
      <ProblemSolutionSection />

      {/* Bénéfices clés - Valeur proposition */}
      <BenefitsSection />

      {/* Contenu du pack - Détail technique */}
      <PackContentSection />

      {/* Variations & contrôle - Flexibilité */}
      <VariationsSection />

      {/* Cas d'usage - Inspiration */}
      <UseCasesSection />

      {/* Pricing - Conversion */}
      <PricingSection />

      {/* RGPD/Compliance - Confiance */}
      <ComplianceSection />

      {/* FAQ - Doutes résidus */}
      <FAQSection />

      {/* Footer - Navigation générale */}
      <Footer />
    </main>
  );
}
