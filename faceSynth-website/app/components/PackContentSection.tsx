'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';
import { Card } from './common/Card';

/**
 * Section Contenu du pack
 * Détail des images, résolutions, formats et métadonnées
 */
export const PackContentSection: React.FC = () => {
  const specs = [
    { label: 'Images synthétiques', value: '10 000+', icon: '🖼️' },
    { label: 'Résolution standard', value: '1024×1024 px', icon: '📐' },
    { label: 'Formats', value: 'PNG, JPEG', icon: '📦' },
    { label: 'Métadonnées', value: 'JSON/CSV', icon: '📋' },
  ];

  const annotations = [
    '✓ Pose tête (yaw, pitch, roll)',
    '✓ Direction du regard (gaze angle)',
    '✓ Identité synthétique unique',
    '✓ Type d\'éclairage appliqué',
    '✓ Expression faciale',
    '✓ Segmentation visage/arrière-plan',
    '✓ Seed de génération (reproductibilité)',
    '✓ Landmarks 2D/3D',
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
          Ce que vous obtenez
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          Un dataset complet et prêt à l'emploi, avec annotations riches pour l'entraînement de vos modèles
        </motion.p>

        {/* Specs principales */}
        <motion.div
          className="grid grid-cols-2 sm:grid-cols-4 gap-6 mb-16"
          variants={containerVariants}
        >
          {specs.map((spec, idx) => (
            <motion.div key={idx} variants={itemVariants}>
              <Card className="text-center">
                <div className="text-4xl mb-3">{spec.icon}</div>
                <p className="text-small text-neutral-subtext mb-2">{spec.label}</p>
                <p className="text-h3 font-bold text-primary-blue">{spec.value}</p>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Annotations détaillées */}
        <motion.div className="grid grid-cols-1 lg:grid-cols-2 gap-12" variants={containerVariants}>
          <motion.div variants={itemVariants}>
            <h3 className="text-h3 mb-6 text-neutral-text">Annotations incluses</h3>
            <div className="space-y-4">
              {annotations.map((annotation, idx) => (
                <motion.div
                  key={idx}
                  className="flex items-start gap-3 p-3 rounded-lg bg-neutral-bg/50 hover:bg-primary-blue/5 transition-colors"
                  whileHover={{ x: 10 }}
                >
                  <span className="text-primary-blue font-bold text-lg flex-shrink-0">→</span>
                  <span className="text-neutral-text">{annotation}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Info format livraison */}
          <motion.div variants={itemVariants}>
            <h3 className="text-h3 mb-6 text-neutral-text">Format de livraison</h3>
            <Card className="space-y-4">
              <div>
                <h4 className="font-semibold text-neutral-text mb-2">Accès et téléchargement</h4>
                <p className="text-neutral-subtext">
                  Lien de téléchargement sécurisé avec authentification. Stockage illimité pendant 30 jours.
                </p>
              </div>
              <div className="border-t border-neutral-border pt-4">
                <h4 className="font-semibold text-neutral-text mb-2">Documentation</h4>
                <p className="text-neutral-subtext">
                  PDF complet + fiches techniques RGPD, éthique et légales.
                </p>
              </div>
              <div className="border-t border-neutral-border pt-4">
                <h4 className="font-semibold text-neutral-text mb-2">Support</h4>
                <p className="text-neutral-subtext">
                  Email de support inclus pour toute question d'intégration.
                </p>
              </div>
            </Card>
          </motion.div>
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
