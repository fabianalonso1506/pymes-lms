import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'PYMES LMS',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-gray-50 text-gray-800">
        {children}
      </body>
    </html>
  );
}
