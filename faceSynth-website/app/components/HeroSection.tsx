'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from './common/Button';
import { LeadCaptureForm } from './LeadCaptureForm';

/**
 * Section Hero - Présentation principale du produit FaceSynth
 * Inclut un titre accrocheur, sous-titre, CTA principaux et visuel hero
 */
export const HeroSection: React.FC = () => {
  const [showForm, setShowForm] = useState(false);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2, delayChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
  };

  return (
    <section className="hero-gradient relative overflow-hidden pt-20 pb-20 sm:pt-32 sm:pb-32">
      {/* Decorative background elements */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary-indigo/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary-blue/5 rounded-full blur-3xl"></div>

      <div className="container-main relative z-10">
        <motion.div
          className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Contenu texte */}
          <motion.div variants={itemVariants} className="space-y-6">
            <motion.h1
              className="text-h1 text-neutral-text leading-tight"
              variants={itemVariants}
            >
              Entraînez vos modèles IA avec confiance,{' '}
              <span className="text-primary-blue">sans données personnelles</span>
            </motion.h1>

            <motion.p
              className="text-lg text-neutral-subtext leading-relaxed max-w-xl"
              variants={itemVariants}
            >
              FaceSynth fournit des milliers de visages synthétiques réalistes, entièrement 
              annotés et 100% conformes RGPD. Entraînez vos modèles de vision par ordinateur 
              rapidement, sans risques juridiques ni obstacles éthiques.
            </motion.p>

            {/* Points clés rapides */}
            <motion.div className="space-y-3 pt-4" variants={itemVariants}>
              {[
                '✓ Aucune donnée personnelle réelle',
                '✓ Annotations riches (pose, regard, expression, etc.)',
                '✓ Livraison immédiate en haute résolution',
              ].map((point, idx) => (
                <div key={idx} className="flex items-start gap-3">
                  <span className="text-primary-blue font-bold text-lg"></span>
                  <span className="text-neutral-text">{point}</span>
                </div>
              ))}
            </motion.div>

            {/* CTA principaux */}
            <motion.div
              className="flex flex-col sm:flex-row gap-4 pt-8"
              variants={itemVariants}
            >
              <Button
                variant="primary"
                size="lg"
                onClick={() => setShowForm(true)}
              >
                Obtenir un sample pack
              </Button>
              <Button
                variant="outline"
                size="lg"
                onClick={() => {
                  // Scroll vers la section de contact ou ouvre un formulaire
                  document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Demander une démo
              </Button>
            </motion.div>
          </motion.div>

          {/* Visuel hero - Grille de visages synthétiques */}
          <motion.div
            variants={itemVariants}
            className="relative h-96 sm:h-full flex items-center justify-center"
          >
            <div className="relative w-full h-full max-w-md">
              {/* Grille placeholder pour les visages synthétiques */}
              <div className="grid grid-cols-3 gap-3 w-full h-full">
                {[...Array(9)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="bg-gradient-to-br from-primary-blue/10 to-primary-indigo/10 rounded-lg border border-primary-blue/20 flex items-center justify-center relative overflow-hidden group"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.1, duration: 0.5 }}
                    whileHover={{ scale: 1.05, boxShadow: '0 0 20px rgba(37, 99, 235, 0.3)' }}
                  >
                    {/* Simulation d'annotations (landmarks, bounding box) */}
                    <div className="absolute inset-1 border border-primary-blue/30 rounded"></div>
                    <div className="w-8 h-8 bg-gradient-to-r from-primary-blue to-primary-indigo rounded-full opacity-50 group-hover:opacity-100 transition-opacity"></div>
                    <div className="absolute top-1 right-1 text-xs text-primary-blue opacity-0 group-hover:opacity-100 transition-opacity">
                      {`#${i + 1}`}
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Overlay avec texte explicatif */}
              <div className="absolute -bottom-8 left-0 right-0 text-center text-small text-neutral-subtext">
                <p className="font-semibold">Visages 100% synthétiques avec annotations</p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Modal de capture de lead */}
      {showForm && (
        <LeadCaptureForm onClose={() => setShowForm(false)} />
      )}
    </section>
  );
};
