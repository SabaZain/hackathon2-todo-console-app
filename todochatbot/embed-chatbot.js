/**
 * Script to embed Todo Chatbot into Next.js application
 *
 * This script should be added to the main layout of the Next.js app
 * to integrate the chatbot without breaking existing functionality.
 */

// Function to inject the chatbot components into the Next.js app
function injectTodoChatbot() {
    // Create a container for the chatbot components
    const chatContainer = document.createElement('div');
    chatContainer.id = 'todo-chat-container';
    document.body.appendChild(chatContainer);

    // Add the CSS styles for the chatbot
    const styleLink = document.createElement('link');
    styleLink.rel = 'stylesheet';
    styleLink.href = '/todochatbot/chat-widget-styles.css';
    document.head.appendChild(styleLink);

    // Dynamically load the chatbot JavaScript components
    const scripts = [
        '/todochatbot/api-client.js',
        '/todochatbot/chat-icon.js',
        '/todochatbot/chat-interface.js',
        '/todochatbot/message-display.js',
        '/todochatbot/message-sender.js',
        '/todochatbot/response-handler.js',
        '/todochatbot/state-manager.js',
        '/todochatbot/typing-indicator.js',
        '/todochatbot/ui-controller.js',
        '/todochatbot/integration.js'
    ];

    scripts.forEach(scriptPath => {
        const script = document.createElement('script');
        script.src = scriptPath;
        script.async = false; // Ensure scripts load in order
        document.head.appendChild(script);
    });

    // Configure the API client to point to the correct backend
    document.addEventListener('DOMContentLoaded', function() {
        if (window.TodoAPIClient) {
            // Point to the chatbot backend running on port 8000
            window.TodoAPIClient.baseURL = 'http://127.0.0.1:8000/api';

            // Get auth token from existing Todo app context
            const authToken = getExistingAuthToken(); // Try to get from existing Todo app
            if (authToken) {
                window.TodoAPIClient.setAuthToken(authToken);
                console.log("JWT token set from existing Todo app context");
            } else {
                console.warn("No JWT token found from existing Todo app context - chatbot may have limited functionality");
            }
        }
    });

    // Function to get auth token from existing Todo app
    function getExistingAuthToken() {
        // Try multiple methods to get the auth token from existing Todo app
        let token = null;

        // Method 1: From localStorage (common in Todo apps)
        token = localStorage.getItem('auth_token') ||
                localStorage.getItem('jwt_token') ||
                localStorage.getItem('access_token');

        // Method 2: From global variable set by Todo app
        if (!token && window.todoApp && window.todoApp.authToken) {
            token = window.todoApp.authToken;
        }

        // Method 3: From window object
        if (!token && window.authToken) {
            token = window.authToken;
        }

        // Method 4: From sessionStorage
        if (!token) {
            token = sessionStorage.getItem('auth_token') ||
                    sessionStorage.getItem('jwt_token');
        }

        return token;
    }
}

// Wait for the page to load before injecting the chatbot
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectTodoChatbot);
} else {
    // DOM is already loaded, run immediately
    injectTodoChatbot();
}

// For Next.js compatibility, also listen for route changes
if (typeof window !== 'undefined') {
    // This part handles Next.js dynamic route changes
    const handleRouteChange = () => {
        // Ensure the container exists after route changes
        if (!document.getElementById('todo-chat-container')) {
            const chatContainer = document.createElement('div');
            chatContainer.id = 'todo-chat-container';
            document.body.appendChild(chatContainer);
        }
    };

    // If using Next.js router events
    if (typeof window !== 'undefined' && window.next) {
        // Next.js router listener would go here
    }
}