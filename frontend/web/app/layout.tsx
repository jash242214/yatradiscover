import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'YatraDiscover AI - AI-Powered Travel Planning',
  description: 'Personalized travel recommendations, smart itinerary management, and seamless booking integrations.',
  keywords: 'travel, AI, recommendations, itinerary, booking, vacation',
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#6366f1" />
      </head>
      <body>{children}</body>
    </html>
  );
}
