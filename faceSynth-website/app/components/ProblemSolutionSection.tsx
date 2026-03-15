'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';

/**
 * Section Problème / Solution
 * Présente les défis actuels et comment FaceSynth les résout
 */
export const ProblemSolutionSection: React.FC = () => {
  const problems = [
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

  const solutions = [
    {
      title: '100% synthétique',
      description: 'Aucune donnée personnelle réelle. Conforme RGPD par nature.',
      icon: '✨',
    },
    {
      title: 'Contrôle total',
      description: 'Définissez la distribution démographique, les variations et les annotations.',
      icon: '🎛️',
    },
    {
      title: 'Reproductibilité',
      description: 'Généré procéduralement avec seed. Exact et répétable à 100%.',
      icon: '🔄',
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
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  };

  return (
    <SectionWrapper bgColor="white">
      <div className="space-y-16">
        {/* Problèmes */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={containerVariants}
        >
          <motion.h2 className="text-h2 text-center mb-12" variants={itemVariants}>
            Les défis actuels de la data vision
          </motion.h2>

          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
            variants={containerVariants}
          >
            {problems.map((problem, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <Card hover>
                  <div className="text-4xl mb-4">{problem.icon}</div>
                  <h3 className="text-h3 mb-3 text-neutral-text">{problem.title}</h3>
                  <p className="text-neutral-subtext">{problem.description}</p>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Séparateur visuel */}
        <div className="flex items-center justify-center gap-4">
          <div className="flex-grow h-px bg-neutral-border"></div>
          <span className="text-2xl text-primary-blue">↓</span>
          <div className="flex-grow h-px bg-neutral-border"></div>
        </div>

        {/* Solutions */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={containerVariants}
        >
          <motion.h2 className="text-h2 text-center mb-12" variants={itemVariants}>
            La solution : FaceSynth
          </motion.h2>

          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
            variants={containerVariants}
          >
            {solutions.map((solution, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <Card hover className="bg-gradient-to-br from-primary-blue/5 to-primary-indigo/5 border-primary-blue/20">
                  <div className="text-4xl mb-4">{solution.icon}</div>
                  <h3 className="text-h3 mb-3 text-primary-blue">{solution.title}</h3>
                  <p className="text-neutral-text">{solution.description}</p>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </SectionWrapper>
  );
};
