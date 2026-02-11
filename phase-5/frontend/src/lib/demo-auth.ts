/**
 * Demo authentication helper for development
 * This sets up a demo token in localStorage for testing
 */

export const setupDemoAuth = () => {
  if (typeof window !== 'undefined') {
    // Set demo token for development
    localStorage.setItem('auth_token', 'demo-token');
  }
};

export const clearDemoAuth = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
};

export const isDemoAuthSetup = (): boolean => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token') === 'demo-token';
  }
  return false;
};
