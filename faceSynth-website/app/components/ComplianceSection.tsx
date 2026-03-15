'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';

/**
 * Section RGPD, Éthique & Garantie
 * Rassurez fortement sur les aspects de conformité
 */
export const ComplianceSection: React.FC = () => {
  const guarantees = [
    {
      title: 'Aucune donnée personnelle réelle',
      description: 'Les visages sont 100% synthétiques. Pas de scraping, pas de personnes réelles.',
      icon: '✨',
    },
    {
      title: 'Conforme RGPD par nature',
      description: 'Sans données personnelles, pas de consentement requis, pas d\'obligations d\'opt-out.',
      icon: '⚖️',
    },
    {
      title: 'Génération procédurale transparente',
      description: 'Créé avec Blender. Seed unique pour chaque visage. Reproductibilité totale.',
      icon: '🔧',
    },
    {
      title: 'Explicabilité et audit',
      description: 'Documentations RGPD/éthique incluses. Transparence complète sur la génération.',
      icon: '📋',
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
          RGPD, Éthique & Garantie
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          FaceSynth est conçu pour les équipes sensibles à la conformité et l'éthique des données.
        </motion.p>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16"
          variants={containerVariants}
        >
          {guarantees.map((guarantee, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <Card
                className="bg-gradient-to-br from-primary-blue/5 to-transparent border-l-4 border-primary-blue"
                hover
              >
                <div className="text-5xl mb-4">{guarantee.icon}</div>
                <h3 className="text-h3 mb-3 text-neutral-text">{guarantee.title}</h3>
                <p className="text-neutral-subtext leading-relaxed">{guarantee.description}</p>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Points importants pour les DPO / Compliance */}
        <motion.div variants={itemVariants}>
          <Card className="bg-primary-blue/10 border-primary-blue/30">
            <h3 className="text-h3 mb-6 text-primary-blue">Pour votre équipe conformité & DPO</h3>
            <ul className="space-y-4">
              {[
                'Pas de DPIA (Data Protection Impact Assessment) requise',
                'Pas de consentement utilisateur à gérer',
                'Pas de demande de droit à l\'oubli ou d\'opposition',
                'Certificat de conformité RGPD fourni',
                'Fiche méthodologique d\'anonymat fournie',
                'Garantie légale contre les recours liés aux données personnelles',
              ].map((point, idx) => (
                <motion.li
                  key={idx}
                  className="flex items-start gap-3"
                  initial={{ opacity: 0, x: -10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                >
                  <span className="text-primary-blue font-bold text-lg">✓</span>
                  <span className="text-neutral-text">{point}</span>
                </motion.li>
              ))}
            </ul>
          </Card>
        </motion.div>

        {/* Appel à l'action */}
        <motion.div
          variants={itemVariants}
          className="mt-12 p-8 bg-gradient-to-r from-primary-indigo/10 to-primary-blue/10 rounded-2xl border border-primary-blue/20 text-center"
        >
          <h3 className="text-h3 mb-3 text-neutral-text">Vous avez des questions de conformité ?</h3>
          <p className="text-neutral-subtext mb-4">
            Notre équipe est disponible pour discuter en détail des implications RGPD et éthiques.
          </p>
          <p className="text-primary-blue font-semibold">
            contact@facesynth.io ou +33 (0) 1 XX XX XX XX
          </p>
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
