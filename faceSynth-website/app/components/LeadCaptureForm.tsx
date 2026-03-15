'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from './common/Button';

interface LeadCaptureFormProps {
  onClose: () => void;
}

/**
 * Composant formulaire de capture de leads
 * Apparaît en modal lors du clic sur les CTA principaux
 */
export const LeadCaptureForm: React.FC<LeadCaptureFormProps> = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Simulation d'envoi de formulaire (à remplacer par API réelle)
    try {
      // await fetch('/api/leads', { ... })
      console.log('Form submitted:', { email, company, message });
      
      // Simule un délai réseau
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setSubmitted(true);
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setLoading(false);
    }
  };

  const isValidEmail = (email: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <motion.div
        className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        transition={{ duration: 0.3 }}
      >
        {!submitted ? (
          <>
            <h2 className="text-h3 font-bold text-neutral-text mb-2">
              Obtenir un sample pack
            </h2>
            <p className="text-neutral-subtext mb-6">
              Remplissez le formulaire ci-dessous et nous vous enverrons un dataset de sample dans les 24h.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email */}
              <div>
                <label className="block text-sm font-semibold text-neutral-text mb-2">
                  Email professionnel *
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="vous@entreprise.com"
                  required
                  className="w-full px-4 py-2 border border-neutral-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue"
                />
              </div>

              {/* Entreprise / Organisme */}
              <div>
                <label className="block text-sm font-semibold text-neutral-text mb-2">
                  Entreprise / Organisme (optionnel)
                </label>
                <input
                  type="text"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="Ex: Acme AI Labs"
                  className="w-full px-4 py-2 border border-neutral-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue"
                />
              </div>

              {/* Message optionnel */}
              <div>
                <label className="block text-sm font-semibold text-neutral-text mb-2">
                  Votre cas d\'usage (optionnel)
                </label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Ex: Detection de visages pour surveillance, Eye-tracking, etc."
                  rows={3}
                  className="w-full px-4 py-2 border border-neutral-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue resize-none"
                />
              </div>

              {/* Boutons */}
              <div className="flex gap-3 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  className="flex-1"
                  onClick={onClose}
                  disabled={loading}
                >
                  Annuler
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  className="flex-1"
                  disabled={!isValidEmail(email) || loading}
                >
                  {loading ? 'Envoi...' : 'Envoyer'}
                </Button>
              </div>
            </form>
          </>
        ) : (
          <motion.div
            className="text-center py-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="text-5xl mb-4">✓</div>
            <h3 className="text-h3 font-bold text-primary-blue mb-2">
              Demande reçue !
            </h3>
            <p className="text-neutral-subtext">
              Nous vous enverrons un sample pack à {email} dans les 24h.
            </p>
          </motion.div>
        )}

        {/* Bouton fermeture */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-neutral-subtext hover:text-neutral-text"
        >
          ✕
        </button>
      </motion.div>
    </div>
  );
};
