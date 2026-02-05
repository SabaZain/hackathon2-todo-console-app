import '@/styles/globals.css'
import type { Metadata } from 'next'
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import ChatBotWrapper from '@/components/chatbot/ChatBotWrapper';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple todo application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <div className="flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-grow container mx-auto px-4 py-6 sm:py-8">
            {children}
          </main>
          <Footer />
          <ChatBotWrapper />
        </div>
      </body>
    </html>
  )
}