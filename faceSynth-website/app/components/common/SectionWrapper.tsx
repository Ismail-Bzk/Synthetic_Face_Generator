'use client';

import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface SectionWrapperProps {
  children: React.ReactNode;
  id?: string;
  className?: string;
  bgColor?: 'light' | 'white';
}

/**
 * Wrapper de section avec animation framer-motion
 * Permet une animation fade-in + slide-up au scroll
 */
export const SectionWrapper: React.FC<SectionWrapperProps> = ({
  children,
  id,
  className,
  bgColor = 'light',
}) => {
  const bgStyles = {
    light: 'bg-neutral-bg',
    white: 'bg-neutral-card',
  };

  return (
    <motion.section
      id={id}
      className={clsx(
        'section-padding',
        bgStyles[bgColor],
        className
      )}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      viewport={{ once: true, margin: '-100px' }}
    >
      <div className="container-main">
        {children}
      </div>
    </motion.section>
  );
};
