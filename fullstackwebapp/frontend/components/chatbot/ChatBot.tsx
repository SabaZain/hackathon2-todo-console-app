'use client';

import { useState, useRef, useEffect, KeyboardEvent } from 'react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface ToolCall {
  name?: string;
  arguments?: Record<string, any>;
}

interface ChatResponse {
  response?: string;
  message?: string;
  content?: string;
  response_text?: string;
  tool_calls?: ToolCall[];
  intent?: string;
}

interface ChatBotProps {
  userId: string;
  token: string;
}

const ChatBot = ({ userId, token }: ChatBotProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // DEBUG: Log outgoing request
    console.log('DEBUG: Sending message to backend:', {
      userId,
      token: token ? 'TOKEN_PRESENT' : 'TOKEN_MISSING',
      message: inputValue,
      endpoint: `${process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL || 'http://127.0.0.1:8000'}/api/${userId}/chat`
    });

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Determine the API base URL based on environment
      const API_BASE_URL = process.env.NODE_ENV === 'production'
        ? process.env.NEXT_PUBLIC_API_BASE_URL_PROD
        : process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL;

      // Fallback to localhost:8000 if environment variables are not set
      const baseUrl = API_BASE_URL || 'http://127.0.0.1:8000';

      // DEBUG: Log the actual request being made
      console.log('DEBUG: Making request to:', `${baseUrl}/api/${userId}/chat`);
      console.log('DEBUG: Request payload:', {
        message: inputValue,
        userId: userId,
        token: token ? 'PRESENT' : 'MISSING'
      });

      // Call the backend API - using the correct endpoint that matches the backend
      const response = await fetch(`${baseUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue,
        }),
      });

      // DEBUG: Log response status
      console.log('DEBUG: Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('DEBUG: API error response:', errorText);

        // Check if it's an authentication error
        if (response.status === 401 || response.status === 403) {
          console.error('DEBUG: Authentication error - token may be invalid or expired');
          throw new Error('Authentication failed. Please log in again.');
        }

        throw new Error(`API error: ${response.status} ${response.statusText}. Details: ${errorText}`);
      }

      const data: ChatResponse = await response.json();

      // DEBUG: Log the received response from backend for troubleshooting
      console.log('DEBUG: Received response from backend:', data);

      // DEBUG: Log the specific fields we're checking for response text
      console.log('DEBUG: Checking for response text in fields:', {
        response: data.response,
        message: data.message,
        content: data.content,
        response_text: data.response_text,
        typeof_data: typeof data
      });

      // Safely extract assistant text from any of the possible response fields
      // The backend may return response text in different fields
      const assistantText = data.response ||
                           data.message ||
                           data.content ||
                           data.response_text ||
                           (typeof data === 'string' ? data : 'No response generated');

      // DEBUG: Log which field was used for the response text
      console.log('DEBUG: Using response text from field:',
        data.response ? 'response' :
        data.message ? 'message' :
        data.content ? 'content' :
        data.response_text ? 'response_text' :
        'default fallback');

      const assistantMessage: Message = {
        id: Date.now().toString(),
        text: assistantText,
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if the response contains tool calls that indicate task operations
      // This is more reliable than text matching
      let hasTaskOperation = false;

      try {
        if (data.tool_calls && Array.isArray(data.tool_calls)) {
          hasTaskOperation = data.tool_calls.some((tool: { name?: string }) =>
            tool.name &&
            (tool.name.toLowerCase().includes('create_task') ||
             tool.name.toLowerCase().includes('update_task') ||
             tool.name.toLowerCase().includes('complete_task') ||
             tool.name.toLowerCase().includes('delete_task') ||
             tool.name.toLowerCase().includes('list_tasks'))
          );
        }
      } catch (e) {
        console.debug('Could not check tool calls:', e);
      }

      // Also check the intent if available
      const hasTaskIntent = data.intent &&
        (data.intent.toLowerCase().includes('create_task') ||
         data.intent.toLowerCase().includes('update_task') ||
         data.intent.toLowerCase().includes('complete_task') ||
         data.intent.toLowerCase().includes('delete_task') ||
         data.intent.toLowerCase().includes('list_tasks'));

      // Also check the response text as backup
      const lowerCaseText = assistantText.toLowerCase();
      const hasTaskText = lowerCaseText.includes('task') && (
        lowerCaseText.includes('created') ||
        lowerCaseText.includes('added') ||
        lowerCaseText.includes('updated') ||
        lowerCaseText.includes('deleted') ||
        lowerCaseText.includes('completed') ||
        lowerCaseText.includes('removed') ||
        lowerCaseText.includes('finished') ||
        lowerCaseText.includes('marked') ||
        lowerCaseText.includes('listed') ||
        lowerCaseText.includes('show')
      );

      // If any of these indicators are true, trigger a refresh
      if (hasTaskOperation || hasTaskIntent || hasTaskText) {
        console.log('Task operation detected, triggering refresh:', {
          hasTaskOperation,
          hasTaskIntent,
          hasTaskText,
          response: assistantText
        });

        // Use the new task updater to notify all subscribers
        // Dynamically import the module to avoid SSR issues
        try {
          (async () => {
            const { triggerTaskRefresh } = await import('@/lib/taskUpdater');
            triggerTaskRefresh();
          })();
        } catch (error) {
          console.warn('Could not load taskUpdater:', error);
        }

        // Also dispatch the original event for backward compatibility
        window.dispatchEvent(new CustomEvent('taskUpdated', {
          detail: {
            action: 'refresh',
            response: assistantText,
            hasTaskOperation,
            hasTaskIntent,
            hasTaskText,
            timestamp: Date.now()
          }
        }));
      }
    } catch (error) {
      // DEBUG: Log the full error
      console.error('DEBUG: Full error in handleSendMessage:', error);

      // Check if it's a network error or other type of error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error('DEBUG: Network error - unable to reach backend');
      }

      const errorMessage: Message = {
        id: Date.now().toString(),
        text: `Sorry, I encountered an error. Backend communication issue: ${error.message || 'Request failed'}`,
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Chatbot Icon Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 z-[9999]"
        aria-label="Open chat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>

      {/* Chat Modal */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-full max-w-md h-[500px] bg-white rounded-xl shadow-xl flex flex-col z-[9998] border border-gray-200">
          {/* Chat Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-xl flex justify-between items-center">
            <h3 className="font-semibold">AI Assistant</h3>
            <button
              onClick={toggleChat}
              className="text-white hover:text-gray-200 focus:outline-none"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <p>Start a conversation with the AI assistant</p>
              </div>
            ) : (
              <div className="space-y-3">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.sender === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-800'
                      }`}
                    >
                      <p>{message.text}</p>
                      <p
                        className={`text-xs mt-1 ${
                          message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-3 bg-white rounded-b-xl">
            <div className="flex items-center">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                disabled={isLoading}
                className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className={`bg-blue-600 text-white px-4 py-2 rounded-r-lg ${
                  isLoading || !inputValue.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatBot;