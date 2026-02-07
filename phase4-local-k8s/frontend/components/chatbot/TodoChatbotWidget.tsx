'use client';

import { useEffect } from 'react';

declare global {
  interface Window {
    TodoAPIClient: any;
    TodoChatIcon: any;
    TodoChatInterface: any;
    TodoChatIntegration: any;
    TodoMessageSender: any;
    TodoStateManager: any;
  }
}

const TodoChatbotWidget = () => {
  useEffect(() => {
    // JWT decoding function to extract user ID from token
    function getUserIdFromToken(token: string) {
      try {
        // Split the token to get the payload part
        const parts = token.split('.');
        if (parts.length !== 3) {
          console.error('Invalid JWT token format');
          return null;
        }

        // Decode the payload (second part)
        // Replace URL-safe base64 characters and pad if necessary
        const base64Payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64Payload).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        const payload = JSON.parse(jsonPayload);

        // Extract user_id from the payload
        return payload.user_id ? payload.user_id.toString() : null;
      } catch (error) {
        console.error('Error decoding JWT token:', error);
        return null;
      }
    }

    const loadChatbot = async () => {
      // Create container for the chatbot if it doesn't exist
      let container = document.getElementById('todo-chat-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'todo-chat-container';
        document.body.appendChild(container);
      }

      // Load the chatbot CSS
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = '/todo-chatbot/chat-widget-styles.css';
      document.head.appendChild(link);

      // Load the chatbot scripts sequentially
      const scripts = [
        '/todo-chatbot/api-client.js',
        '/todo-chatbot/chat-icon.js',
        '/todo-chatbot/chat-interface.js',
        '/todo-chatbot/message-display.js',
        '/todo-chatbot/message-sender.js',
        '/todo-chatbot/response-handler.js',
        '/todo-chatbot/state-manager.js',
        '/todo-chatbot/typing-indicator.js',
        '/todo-chatbot/ui-controller.js',
        '/todo-chatbot/integration.js'
      ];

      for (const src of scripts) {
        const script = document.createElement('script');
        script.src = src;
        script.async = false; // Ensure scripts load in order
        document.head.appendChild(script);

        // Wait for script to load before continuing
        await new Promise((resolve) => {
          script.onload = resolve;
          script.onerror = resolve; // Continue even if there's an error
        });
      }

      // Configure the API client after scripts are loaded
      if (window.TodoAPIClient) {
        window.TodoAPIClient.baseURL = 'http://127.0.0.1:8000/api';

        // Get auth token from Next.js auth context if available
        const token = localStorage.getItem('token');
        if (token) {
          window.TodoAPIClient.setAuthToken(token);

          // Extract user ID from JWT token and set it in localStorage for the chatbot
          const userId = getUserIdFromToken(token);
          if (userId) {
            localStorage.setItem('todo_user_id', userId);

            // Update the APIClient's method to get user ID
            if (window.TodoAPIClient) {
              (window.TodoAPIClient as any).getCurrentUserId = function() {
                return localStorage.getItem('todo_user_id') || 'anonymous';
              };
            }

            // Update the message sender's method as well
            if (window.TodoMessageSender) {
              (window.TodoMessageSender as any).prototype.getCurrentUserId = function() {
                return localStorage.getItem('todo_user_id') || 'anonymous';
              };
            }

            // Update the state manager if available
            if (window.TodoStateManager) {
              (window.TodoStateManager as any).setCurrentUser(userId);
            }
          }
        }
      }
    };

    // Only load the chatbot on the client-side
    if (typeof window !== 'undefined') {
      loadChatbot();
    }

    // Cleanup function
    return () => {
      // Remove the container when component unmounts
      const container = document.getElementById('todo-chat-container');
      if (container && container.parentNode) {
        container.parentNode.removeChild(container);
      }

      // Remove the CSS link
      const link = document.querySelector('link[href="/todo-chatbot/chat-widget-styles.css"]');
      if (link && link.parentNode) {
        link.parentNode.removeChild(link);
      }

      // Clean up any global variables set by the chatbot scripts
      if (typeof window !== 'undefined') {
        delete (window as any).TodoAPIClient;
        delete (window as any).TodoChatIcon;
        delete (window as any).TodoChatInterface;
        delete (window as any).TodoChatIntegration;
        delete (window as any).TodoMessageSender;
        delete (window as any).TodoStateManager;
      }
    };
  }, []);

  return null; // This component doesn't render anything itself
};

export default TodoChatbotWidget;