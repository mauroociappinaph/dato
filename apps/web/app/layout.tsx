import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'DATO',
  description: 'Política argentina verificada con datos reales',
};

export default function RootLayout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
