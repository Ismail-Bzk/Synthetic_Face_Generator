'use client';

import React from 'react';
import { motion } from 'framer-motion';

/**
 * Composant Footer
 */
export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  const sections = [
    {
      title: 'Produit',
      links: [
        { label: 'Caractéristiques', href: '#' },
        { label: 'Pricing', href: '#pricing' },
        { label: 'Documentation', href: '#' },
        { label: 'FAQ', href: '#' },
      ],
    },
    {
      title: 'Support',
      links: [
        { label: 'Nous contacter', href: '#contact' },
        { label: 'Email support', href: 'mailto:support@facesynth.io' },
        { label: 'Status page', href: '#' },
        { label: 'Changelog', href: '#' },
      ],
    },
    {
      title: 'Légal',
      links: [
        { label: 'Mentions légales', href: '#' },
        { label: 'Politique de confidentialité', href: '#' },
        { label: 'Conditions d\'utilisation', href: '#' },
        { label: 'RGPD', href: '#' },
      ],
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
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.4 } },
  };

  return (
    <footer className="bg-neutral-text text-white">
      <div className="container-main pt-16 pb-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-50px' }}
          variants={containerVariants}
        >
          {/* Top section */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            {/* Brand */}
            <motion.div variants={itemVariants}>
              <h3 className="text-2xl font-bold mb-3">FaceSynth</h3>
              <p className="text-sm text-gray-300 mb-4">
                Dataset de visages synthétiques 100% RGPD pour l'IA et la computer vision.
              </p>
              <div className="flex gap-4">
                <a
                  href="https://linkedin.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                  title="LinkedIn"
                >
                  in
                </a>
                <a
                  href="https://twitter.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                  title="Twitter"
                >
                  X
                </a>
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                  title="GitHub"
                >
                  GH
                </a>
              </div>
            </motion.div>

            {/* Links */}
            {sections.map((section, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <h4 className="font-semibold mb-4 text-white">{section.title}</h4>
                <ul className="space-y-2">
                  {section.links.map((link, lidx) => (
                    <li key={lidx}>
                      <a
                        href={link.href}
                        className="text-sm text-gray-300 hover:text-white transition-colors"
                      >
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>

          {/* Divider */}
          <div className="border-t border-gray-700 my-8"></div>

          {/* Bottom section */}
          <motion.div
            className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-400"
            variants={itemVariants}
          >
            <p>
              © {currentYear} FaceSynth. All rights reserved. – Synthétique et fier de l'être.
            </p>
            <p>
              Fabriqué avec ❤️ pour la communauté AI/CV.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </footer>
  );
};
