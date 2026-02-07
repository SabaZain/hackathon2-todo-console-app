'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check for authentication token on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    // Clear the authentication token from localStorage
    localStorage.removeItem('token');
    // Update state to reflect logout
    setIsAuthenticated(false);
    // Redirect to home page after logout
    window.location.href = '/';
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex justify-between h-20 items-center">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-blue-600 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Todo App
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-1 sm:space-x-4">
            <Link href="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 hover:bg-gray-50">
              Dashboard
            </Link>
            {/* Show Logout button if user is authenticated, otherwise show Sign In/Sign Up */}
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors duration-200 shadow-sm"
              >
                Logout
              </button>
            ) : (
              <>
                <Link href="/signin" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 hover:bg-gray-50">
                  Sign In
                </Link>
                <Link href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors duration-200 shadow-sm">
                  Sign Up
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-lg text-gray-700 hover:text-blue-600 focus:outline-none hover:bg-gray-100 transition-colors duration-200"
            >
              <svg
                className="h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={isMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white shadow-inner">
            <Link href="/dashboard" className="text-gray-700 hover:text-blue-600 block px-3 py-3 rounded-lg text-base font-medium hover:bg-gray-50 transition-colors duration-200">
              Dashboard
            </Link>
            {/* Show Logout button in mobile menu if user is authenticated */}
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white block px-3 py-3 rounded-lg text-base font-medium hover:bg-red-700 transition-colors duration-200 w-full text-center"
              >
                Logout
              </button>
            ) : (
              <>
                <Link href="/signin" className="text-gray-700 hover:text-blue-600 block px-3 py-3 rounded-lg text-base font-medium hover:bg-gray-50 transition-colors duration-200">
                  Sign In
                </Link>
                <Link href="/signup" className="bg-blue-600 text-white block px-3 py-3 rounded-lg text-base font-medium hover:bg-blue-700 transition-colors duration-200 w-full text-center">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;