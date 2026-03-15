'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';

/**
 * Section Bénéfices clés
 */
export const BenefitsSection: React.FC = () => {
  const benefits = [
    {
      title: 'Conformité RGPD garantie',
      description: 'Aucune donnée personnelle réelle. Pas de consentement requis. Transparence totale.',
      icon: '🔒',
    },
    {
      title: 'Distribution contrôlée',
      description: 'Genre, âge, ethnies synthétiques : définissez exactement la diversité dont vous avez besoin.',
      icon: '⚖️',
    },
    {
      title: 'Annotations riches',
      description: 'Pose, regard, expression, segmentation, landmarks, seed. Tout pour former vos modèles.',
      icon: '🏷️',
    },
    {
      title: 'Réduction des coûts',
      description: 'Pas de collecte, pas d\'IRB, pas d\'obstacles administratifs. ROI immédiat.',
      icon: '💰',
    },
    {
      title: 'Reproductibilité 100%',
      description: 'Généré procéduralement. Exact et répétable à volonté avec les mêmes seeds.',
      icon: '🔄',
    },
    {
      title: 'Flexibilité extrême',
      description: 'Besoin de 10k ou 200k images ? De variations spécifiques ? Adaptation rapide.',
      icon: '🎯',
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  };

  return (
    <SectionWrapper bgColor="light">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-100px' }}
        variants={containerVariants}
      >
        <motion.h2 className="text-h2 text-center mb-4" variants={itemVariants}>
          Bénéfices clés
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          Pourquoi FaceSynth est le meilleur choix pour vos équipes computer vision
        </motion.p>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          variants={containerVariants}
        >
          {benefits.map((benefit, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <Card hover>
                <div className="text-5xl mb-4">{benefit.icon}</div>
                <h3 className="text-h3 mb-3 text-neutral-text">{benefit.title}</h3>
                <p className="text-neutral-subtext leading-relaxed">{benefit.description}</p>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
