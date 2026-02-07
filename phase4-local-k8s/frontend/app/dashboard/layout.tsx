'use client';

import ChatBotWrapper from '@/components/chatbot/ChatBotWrapper';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-6 sm:py-8">
        {children}
      </main>
      <ChatBotWrapper />
    </div>
  );
}