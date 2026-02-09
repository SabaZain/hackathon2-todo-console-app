'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">Phase 5 Todo Application</h1>
        <p className="text-lg mb-8">
          Event-Driven Architecture with Kafka, Dapr, and Kubernetes
        </p>

        <div className="mb-8 text-center">
          <div className="flex justify-center space-x-4">
            <Link
              href="/tasks"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Go to Tasks
              <svg
                className="ml-2 h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </Link>
            <Link
              href="/audit"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              View Audit Trail
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">🔄 Recurring Tasks</h2>
            <p className="text-gray-600">
              Create tasks that repeat automatically on your schedule
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">⏰ Reminders</h2>
            <p className="text-gray-600">
              Get notified via push, email, or in-app notifications
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">🔍 Search & Filter</h2>
            <p className="text-gray-600">
              Find tasks quickly with powerful search and filtering
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">📊 Audit Trail</h2>
            <p className="text-gray-600">
              Complete history of all task operations
            </p>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Status: ✅ All 6 User Stories Complete | Phase 5 Implementation
          </p>
        </div>
      </div>
    </main>
  );
}
