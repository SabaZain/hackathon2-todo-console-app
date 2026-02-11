'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-white to-gray-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 text-gray-900">
            TaskFlow
          </h1>
          <p className="text-xl mb-8 text-gray-600">
            Organize your tasks, boost your productivity
          </p>

          <div className="flex justify-center space-x-4">
            <Link
              href="/register"
              className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16">
          <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">🔄</div>
            <h2 className="text-xl font-semibold mb-2 text-gray-900">Recurring Tasks</h2>
            <p className="text-gray-600">
              Set up tasks that repeat automatically on your schedule
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">⏰</div>
            <h2 className="text-xl font-semibold mb-2 text-gray-900">Smart Reminders</h2>
            <p className="text-gray-600">
              Never miss a deadline with timely notifications
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">🔍</div>
            <h2 className="text-xl font-semibold mb-2 text-gray-900">Quick Search</h2>
            <p className="text-gray-600">
              Find any task instantly with powerful search and filters
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-3">📊</div>
            <h2 className="text-xl font-semibold mb-2 text-gray-900">Activity History</h2>
            <p className="text-gray-600">
              Track all changes and stay organized
            </p>
          </div>
        </div>

        <div className="mt-16 text-center">
          <p className="text-sm text-gray-500">
            Simple, powerful task management for everyone
          </p>
        </div>
      </div>
    </main>
  );
}
