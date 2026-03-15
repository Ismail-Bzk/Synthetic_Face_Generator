import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'FaceSynth – RGPD Synthetic Face Pack',
  description: 'Dataset de visages synthétiques 100% RGPD pour entraîner vos modèles de computer vision sans données personnelles.',
  keywords: 'synthetic faces, computer vision, RGPD, dataset, IA, machine learning',
  authors: [{ name: 'FaceSynth Team' }],
  viewport: 'width=device-width, initial-scale=1',
  openGraph: {
    title: 'FaceSynth – RGPD Synthetic Face Pack',
    description: 'Dataset de visages synthétiques 100% RGPD pour entraîner vos modèles de computer vision.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <head>
        <meta name="theme-color" content="#2563eb" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
