'use client';

import Link from 'next/link';
import { useEffect } from 'react';

export default function NotFound() {
  // Optional: Log the error or send to analytics
  useEffect(() => {
    console.error('404: Page not found');
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <div>
          <h2 className="mt-6 text-4xl font-extrabold text-gray-900">
            404 - Page Not Found
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Sorry, the page you are looking for doesn't exist or has been moved.
          </p>
        </div>

        <div className="mt-8 space-y-4">
          <div className="text-sm text-gray-500 mb-6">
            <p>Error Code: 404 NOT_FOUND</p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/">
              <span className="w-full flex justify-center">
                <button
                  className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Go to Home
                </button>
              </span>
            </Link>

            <Link href="/dashboard">
              <span className="w-full flex justify-center">
                <button
                  className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                >
                  Go to Dashboard
                </button>
              </span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}