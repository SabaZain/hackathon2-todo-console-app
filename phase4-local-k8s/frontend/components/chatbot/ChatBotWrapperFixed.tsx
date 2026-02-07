'use client';

import { useState, useEffect } from 'react';
import ChatBot from './ChatBot';

const ChatBotWrapper = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      // Check for JWT token using multiple possible keys
      let foundToken = localStorage.getItem('token') ||
                      localStorage.getItem('access_token') ||
                      localStorage.getItem('jwt') ||
                      localStorage.getItem('auth_token');

      if (foundToken) {
        try {
          // Decode JWT to extract user ID
          const parts = foundToken.split('.');
          if (parts.length === 3) {
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
            let extractedUserId = null;

            for (const field of possibleUserIdFields) {
              if (payload[field]) {
                extractedUserId = payload[field]?.toString();
                break;
              }
            }

            if (extractedUserId) {
              setIsAuthenticated(true);
              setUserId(extractedUserId);
              setToken(foundToken);

              // Store the user ID in localStorage for consistency with legacy system
              localStorage.setItem('todo_user_id', extractedUserId);

              console.log("Chatbot authenticated, user ID:", extractedUserId);
            } else {
              console.warn("No user ID found in JWT payload. Available fields:", Object.keys(payload));
              setIsAuthenticated(false);
              setUserId(null);
              setToken(null);
            }
          } else {
            console.error("Invalid JWT token format");
            setIsAuthenticated(false);
            setUserId(null);
            setToken(null);
          }
        } catch (error) {
          console.error('Error decoding JWT token:', error);
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

    // Add listener for storage changes (e.g., when user logs out from another tab)
    const handleStorageChange = () => {
      checkAuth();
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  if (!isAuthenticated || !userId || !token) {
    // Don't show the chatbot if user is not authenticated
    return null;
  }

  return <ChatBot userId={userId} token={token} />;
};

export default ChatBotWrapper;