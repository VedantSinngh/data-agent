import type { Metadata } from 'next'
import { Inter, Roboto_Mono } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const geistMono = Roboto_Mono({ subsets: ['latin'], variable: '--font-geist-mono' })

export const metadata: Metadata = {
  title: 'DataTrust Agent',
  description: 'AI-powered data-quality investigation and remediation assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${geistMono.variable}`}>
      <body className="bg-canvas text-body font-sans antialiased">
        <nav className="border-b border-hairline bg-canvas/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
            <div className="text-ink font-sans text-lg tracking-tight-1">DataTrust</div>
            <div className="flex gap-4">
              <button className="btn-outline">Investigate</button>
            </div>
          </div>
        </nav>
        <main className="max-w-[1200px] mx-auto p-6 md:p-16">
          {children}
        </main>
      </body>
    </html>
  )
}
