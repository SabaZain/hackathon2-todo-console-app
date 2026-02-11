'use client';

import { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('auth_token');

    // Public routes that don't require authentication
    const publicRoutes = ['/', '/login', '/register'];
    const isPublicRoute = publicRoutes.includes(pathname);

    // If not authenticated and trying to access protected route, redirect to login
    if (!token && !isPublicRoute) {
      router.push('/login');
    }
  }, [pathname, router]);

  return <>{children}</>;
}
