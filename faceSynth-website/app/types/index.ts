/**
 * Types TypeScript réutilisables pour l'application FaceSynth
 */

export interface PricingPlan {
  name: string;
  description: string;
  price: string;
  images: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export interface Feature {
  title: string;
  description: string;
  icon: string;
}

export interface UseCase {
  title: string;
  description: string;
  icon: string;
}

export interface FAQItem {
  question: string;
  answer: string;
}

export interface LeadData {
  email: string;
  company?: string;
  message?: string;
  timestamp?: Date;
}

export interface SectionProps {
  id?: string;
  className?: string;
}

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}
