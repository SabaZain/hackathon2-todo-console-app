'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Global error:', error);
  }, [error]);

  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8 text-center">
            <div>
              <h2 className="mt-6 text-4xl font-extrabold text-gray-900">
                Something went wrong
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                An unexpected error occurred. Please try again.
              </p>
              {process.env.NODE_ENV === 'development' && (
                <div className="mt-4 p-4 bg-gray-100 text-left text-sm text-red-700 rounded-md">
                  <pre>{error.message}</pre>
                  {error.digest && <div>Digest: {error.digest}</div>}
                </div>
              )}
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => reset()}
                className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Try again
              </button>

              <Link href="/">
                <button className="px-6 py-3 border border-transparent text-base font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
                  Go to Home
                </button>
              </Link>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}