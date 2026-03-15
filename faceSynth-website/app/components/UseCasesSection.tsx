'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';

/**
 * Section Cas d'usage
 */
export const UseCasesSection: React.FC = () => {
  const useCases = [
    {
      title: 'Détection & reconnaissance faciale',
      description: 'Entraîner des modèles robustes sans crainte d\'intenter du biométrique ou d\'atteinte à la vie privée.',
      icon: '👤',
    },
    {
      title: 'Eye-tracking & gaze estimation',
      description: 'Milliers de visages avec directions de regard annotées pour perfectionner vos modèles d\'eye-tracking.',
      icon: '👁️',
    },
    {
      title: 'Biométrie privacy-preserving',
      description: 'Valider des algorithmes biométriques éthiques sans passer par des vraies données.',
      icon: '🔐',
    },
    {
      title: 'Robustesse à occlusion et lumière',
      description: 'Tester vos modèles face à des conditions difficiles : ombres, occlusions légères, éclairage extrême.',
      icon: '💡',
    },
    {
      title: 'Synthetic pretraining',
      description: 'Utiliser FaceSynth comme pré-entraînement avant fine-tuning sur vos données confidentielles.',
      icon: '🚀',
    },
    {
      title: 'Augmentation de données',
      description: 'Augmenter vos datasets réels existants avec des visages synthétiques variés et contrôlés.',
      icon: '📈',
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
    <SectionWrapper bgColor="white">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-100px' }}
        variants={containerVariants}
      >
        <motion.h2 className="text-h2 text-center mb-4" variants={itemVariants}>
          Cas d'usage
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          FaceSynth s'adapte à tous les besoins de vision par ordinateur et d'IA biométrique
        </motion.p>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          variants={containerVariants}
        >
          {useCases.map((useCase, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <Card hover>
                <div className="text-5xl mb-4">{useCase.icon}</div>
                <h3 className="text-h3 mb-3 text-neutral-text">{useCase.title}</h3>
                <p className="text-neutral-subtext leading-relaxed">{useCase.description}</p>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
