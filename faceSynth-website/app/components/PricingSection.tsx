'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';
import { Button } from './common/Button';

/**
 * Section Pricing et licences
 */
export const PricingSection: React.FC = () => {
  const plans = [
    {
      name: 'Starter',
      description: 'Idéal pour débuter et tester',
      price: '1 500 – 3 000 €',
      images: '10 000 images',
      features: [
        '10 000 visages synthétiques',
        'Résolution 1024×1024',
        'Annotations complètes',
        'Format PNG/JPEG',
        'Documentation',
        'Licence non-commerciale ou académique',
      ],
      cta: 'Commencer',
      highlighted: false,
    },
    {
      name: 'Pro',
      description: 'Pour les projets en production',
      price: '5 000 – 12 000 €',
      images: '50k – 200k images',
      features: [
        '50 000 à 200 000 visages',
        'Résolutions multiples',
        'Annotations riches complètes',
        'Métadonnées JSON/CSV',
        'Support email prioritaire',
        'Licence commerciale',
        'Variations personnalisées',
      ],
      cta: 'Obtenir un devis',
      highlighted: true,
    },
    {
      name: 'Enterprise',
      description: 'Solutions sur mesure',
      price: 'Devis personnalisé',
      images: 'Configurations illimitées',
      features: [
        'Datasets custom de toute taille',
        'Variations spécifiques à votre domaine',
        'Résolutions et formats adaptés',
        'Support dédié',
        'Garanties SLA',
        'Options de déploiement privé',
        'Contrats de licences négociables',
      ],
      cta: 'Parler à un expert',
      highlighted: false,
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15, delayChildren: 0 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  };

  return (
    <SectionWrapper bgColor="light" id="pricing">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-100px' }}
        variants={containerVariants}
      >
        <motion.h2 className="text-h2 text-center mb-4" variants={itemVariants}>
          Prix et licences
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          Tarification flexible adaptée à vos besoins. Les prix ci-dessous sont des ordres de grandeur.
        </motion.p>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
          variants={containerVariants}
        >
          {plans.map((plan, idx) => (
            <motion.div
              key={idx}
              variants={itemVariants}
              className={plan.highlighted ? 'md:scale-105' : ''}
            >
              <Card
                className={`h-full flex flex-col ${
                  plan.highlighted
                    ? 'ring-2 ring-primary-blue shadow-xl'
                    : ''
                }`}
              >
                {plan.highlighted && (
                  <div className="bg-primary-blue text-white text-xs font-bold px-3 py-1 rounded-full w-fit mb-4">
                    Plus populaire
                  </div>
                )}

                <h3 className="text-h3 font-bold text-neutral-text mb-2">
                  {plan.name}
                </h3>
                <p className="text-neutral-subtext text-sm mb-4">{plan.description}</p>

                <div className="mb-6">
                  <div className="text-4xl font-bold text-primary-blue mb-1">
                    {plan.price}
                  </div>
                  <p className="text-small text-neutral-subtext">{plan.images}</p>
                </div>

                <ul className="space-y-3 mb-8 flex-grow">
                  {plan.features.map((feature, fidx) => (
                    <li key={fidx} className="flex items-start gap-3">
                      <span className="text-primary-blue font-bold">✓</span>
                      <span className="text-neutral-text text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Button
                  variant={plan.highlighted ? 'primary' : 'outline'}
                  size="lg"
                  className="w-full"
                  onClick={() => {
                    document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
                  }}
                >
                  {plan.cta}
                </Button>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Note de confiance */}
        <motion.div
          variants={itemVariants}
          className="mt-16 p-6 bg-neutral-card border border-neutral-border rounded-xl text-center"
        >
          <p className="text-neutral-text">
            <span className="font-semibold text-primary-blue">Garantie FaceSynth :</span> Pas de personnes réelles, pas de scraping, 
            génération procédurale transparente. Certificat RGPD et documents légaux inclus.
          </p>
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
