'use client';

import Link from 'next/link';
import Button from '@/components/ui/Button';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="z-10 w-full max-w-2xl items-center justify-between font-mono text-sm flex flex-col items-center text-center">
        <div className="bg-slate-900 rounded-xl shadow-lg p-6 w-full">
          <h1 className="text-3xl sm:text-4xl font-bold mb-4 text-white text-center">Welcome to the Todo App</h1>
          <p className="text-lg mb-8 text-gray-200 max-w-xl text-center">
            A simple and intuitive task management application to help you stay organized and productive.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <Button label="Go to Dashboard" type="primary" onClick={() => {}} />
            </Link>
            <Link href="/signin">
              <Button label="Sign In" type="secondary" onClick={() => {}} />
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}