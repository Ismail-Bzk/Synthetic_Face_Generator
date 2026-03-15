'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SectionWrapper } from './common/SectionWrapper';

interface FAQItem {
  question: string;
  answer: string;
}

/**
 * Section FAQ
 */
export const FAQSection: React.FC = () => {
  const faqs: FAQItem[] = [
    {
      question: 'Est-ce que ces visages sont vraiment 100% synthétiques ?',
      answer:
        'Oui, absolument. Chaque visage est généré procéduralement via Blender avec des paramètres aléatoires et seed. Aucune donnée personnelle réelle n\'est utilisée, collectée ou stockée.',
    },
    {
      question: 'Comment puis-je prouver la conformité RGPD à mon DPO ?',
      answer:
        'Chaque pack FaceSynth inclut une fiche méthodologique d\'anonymat et un certificat RGPD. Nous fournissons aussi un document légal détaillant l\'absence totale de données personnelles.',
    },
    {
      question: 'Puis-je demander un dataset entièrement custom ?',
      answer:
        'Bien sûr ! Contactez notre équipe pour un devis Enterprise. Nous pouvons générer des datasets avec des variations spécifiques à votre domaine (ex. âges, ethnies synthétiques, accessoires particuliers).',
    },
    {
      question: 'Quelle est la qualité visuelle des visages synthétiques ?',
      answer:
        'Les visages FaceSynth sont très réalistes et détaillés, adaptés pour l\'entraînement de modèles modernes de computer vision. Ils incluent des variations d\'éclairage, de pose et d\'expression.',
    },
    {
      question: 'Puis-je combiner FaceSynth avec mes propres données réelles ?',
      answer:
        'Oui ! Une approche courante est le "synthetic pretraining" : vous utilisez FaceSynth pour pré-entraîner votre modèle, puis le fine-tuner sur vos vraies données. Cela améliore souvent la robustesse.',
    },
    {
      question: 'Comment est structurée la livraison ? Combien de temps ?',
      answer:
        'Après confirmation de la commande, vous recevez un lien de téléchargement sécurisé dans les 24h. Les images sont organisées en dossiers avec un fichier CSV/JSON de métadonnées. Stockage disponible 30 jours.',
    },
    {
      question: 'Existe-t-il une garantie en cas de problème ?',
      answer:
        'Oui, FaceSynth garantit la conformité RGPD et l\'absence totale de données personnelles réelles. Si vous découvrez une violation, nous vous remboursons intégralement et fournissons une assistance légale.',
    },
    {
      question: 'Quel support technique est inclus ?',
      answer:
        'Le support email est inclus pour les plans Pro et Enterprise. Pour Starter, accès aux docs et FAQ. Réponse garantie sous 24h pour les questions techniques d\'intégration.',
    },
  ];

  const [expanded, setExpanded] = useState<number | null>(0);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.08, delayChildren: 0 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
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
          Questions fréquentes
        </motion.h2>
        <motion.p
          className="text-lg text-center text-neutral-subtext max-w-2xl mx-auto mb-16"
          variants={itemVariants}
        >
          Trouvez réponse à vos questions les plus courantes sur FaceSynth
        </motion.p>

        <motion.div
          className="max-w-3xl mx-auto space-y-4"
          variants={containerVariants}
        >
          {faqs.map((faq, idx) => (
            <motion.div
              key={idx}
              variants={itemVariants}
              className="bg-neutral-card border border-neutral-border rounded-lg overflow-hidden"
            >
              <button
                onClick={() => setExpanded(expanded === idx ? null : idx)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-neutral-bg/50 transition-colors"
              >
                <span className="text-left text-lg font-semibold text-neutral-text">
                  {faq.question}
                </span>
                <motion.span
                  className="text-primary-blue text-2xl font-bold flex-shrink-0 ml-4"
                  animate={{ rotate: expanded === idx ? 45 : 0 }}
                  transition={{ duration: 0.3 }}
                >
                  +
                </motion.span>
              </button>

              <AnimatePresence>
                {expanded === idx && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="border-t border-neutral-border"
                  >
                    <p className="px-6 py-4 text-neutral-subtext leading-relaxed">
                      {faq.answer}
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </SectionWrapper>
  );
};
