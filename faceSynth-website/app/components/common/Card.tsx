'use client';

import React from 'react';
import clsx from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hover?: boolean;
}

/**
 * Composant Card réutilisable pour les sections de contenu
 */
export const Card: React.FC<CardProps> = ({
  className,
  children,
  hover = false,
  ...props
}) => {
  return (
    <div
      className={clsx(
        'bg-neutral-card border border-neutral-border rounded-xl p-6 sm:p-8',
        hover && 'transition-all duration-300 hover:shadow-lg hover:border-primary-blue/30',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
