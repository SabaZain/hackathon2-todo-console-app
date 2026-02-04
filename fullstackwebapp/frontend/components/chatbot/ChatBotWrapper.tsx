'use client';

import { useState, useEffect } from 'react';
import ChatBot from './ChatBot';

const ChatBotWrapper = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Function to get user ID from JWT token
    const getUserIdFromToken = (token) => {
      try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;

        const base64Payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64Payload)
            .split('')
            .map(function(c) {
              return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join('')
        );

        const payload = JSON.parse(jsonPayload);

        // Try multiple possible user ID field names that might be used in the JWT
        const possibleUserIdFields = ['user_id', 'userId', 'sub', 'id', 'user'];

        for (const field of possibleUserIdFields) {
          if (payload[field] !== undefined && payload[field] !== null) {
            return payload[field]?.toString();
          }
        }

        console.warn("No user ID found in JWT payload. Available fields:", Object.keys(payload));
        return null;
      } catch (error) {
        console.error('Error decoding JWT token:', error);
        return null;
      }
    };

    const checkAuth = () => {
      // Check for JWT token using multiple possible keys
      let foundToken = localStorage.getItem('token') ||
                      localStorage.getItem('access_token') ||
                      localStorage.getItem('jwt') ||
                      localStorage.getItem('auth_token');

      if (foundToken) {
        const extractedUserId = getUserIdFromToken(foundToken);

        if (extractedUserId) {
          setIsAuthenticated(true);
          setUserId(extractedUserId);
          setToken(foundToken);

          // Store the user ID in localStorage for consistency with legacy system
          localStorage.setItem('todo_user_id', extractedUserId);

          console.log("Chatbot authenticated, user ID:", extractedUserId);
        } else {
          console.log("No valid user ID found in token");
          setIsAuthenticated(false);
          setUserId(null);
          setToken(null);
        }
      } else {
        console.log("No authentication token found in localStorage");
        setIsAuthenticated(false);
        setUserId(null);
        setToken(null);
      }
    };

    // Check authentication immediately
    checkAuth();

    // Add listener for storage changes (e.g., when user logs in/out from another tab)
    const handleStorageChange = (e) => {
      // Only react to changes in token-related items
      if (e.key && (e.key.includes('token') || e.key.includes('auth'))) {
        setTimeout(checkAuth, 100); // Small delay to ensure localStorage is updated
      }
    };

    window.addEventListener('storage', handleStorageChange);

    // Also listen for a custom event that might be fired after login
    const handleAuthChange = () => {
      setTimeout(checkAuth, 100);
    };

    window.addEventListener('authChanged', handleAuthChange);

    // Listen for custom events that might be dispatched after login
    window.addEventListener('loginSuccess', handleAuthChange);
    window.addEventListener('logoutSuccess', handleAuthChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChanged', handleAuthChange);
      window.removeEventListener('loginSuccess', handleAuthChange);
      window.removeEventListener('logoutSuccess', handleAuthChange);
    };
  }, []);

  if (!isAuthenticated || !userId || !token) {
    // Don't show the chatbot if user is not authenticated
    return null;
  }

  return <ChatBot userId={userId} token={token} />;
};

export default ChatBotWrapper;