/**
 * Diagnostic script to identify chatbot authentication issues
 */

console.log("=== Chatbot Authentication Diagnostics ===");

function diagnoseAuth() {
    console.log("\n1. Checking for authentication tokens in localStorage:");

    const possibleTokens = [
        'token',
        'access_token',
        'jwt',
        'auth_token',
        'bearer_token'
    ];

    let foundToken = null;
    let tokenKey = null;

    for (const key of possibleTokens) {
        const token = localStorage.getItem(key);
        if (token) {
            console.log(`   ✓ Found token in localStorage[${key}]: ${token.substring(0, 20)}...`);
            foundToken = token;
            tokenKey = key;
            break;
        } else {
            console.log(`   ✗ No token in localStorage[${key}]`);
        }
    }

    if (!foundToken) {
        console.log("   ⚠ No authentication token found in localStorage");
        console.log("   This could explain why the chatbot isn't working");
        return;
    }

    console.log("\n2. Attempting to decode JWT token:");

    try {
        const parts = foundToken.split('.');
        if (parts.length !== 3) {
            console.log("   ✗ Invalid JWT format - token doesn't have 3 parts");
            return;
        }

        // Decode the payload (second part)
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
        console.log("   ✓ Successfully decoded JWT payload:");
        console.log("   ", JSON.stringify(payload, null, 2));

        // Check for user ID in various possible fields
        const possibleUserIdFields = ['user_id', 'userId', 'sub', 'id', 'user'];
        let userId = null;

        for (const field of possibleUserIdFields) {
            if (payload[field]) {
                userId = payload[field];
                console.log(`   ✓ Found user ID in field '${field}': ${userId}`);
                break;
            }
        }

        if (!userId) {
            console.log("   ✗ No user ID found in JWT payload!");
            console.log("   Possible fields checked:", possibleUserIdFields);
            console.log("   Available fields:", Object.keys(payload));
            return;
        }

        // Test the API endpoint
        console.log("\n3. Testing API endpoint with extracted info:");
        console.log(`   Will try to call: /api/${userId}/chat`);

        // Store user ID in the format expected by the legacy system
        localStorage.setItem('todo_user_id', userId.toString());
        console.log(`   ✓ Stored user ID in localStorage['todo_user_id']: ${userId}`);

        // Test API connectivity
        testApiConnectivity(userId, foundToken);

    } catch (error) {
        console.error("   ✗ Error decoding JWT:", error.message);
    }
}

function testApiConnectivity(userId, token) {
    console.log("\n4. Testing API connectivity:");

    const testData = {
        message: "Test message to verify API connectivity"
    };

    fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(testData)
    })
    .then(response => {
        console.log(`   Response status: ${response.status}`);

        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    })
    .then(data => {
        console.log("   ✓ API call successful!");
        console.log("   Response:", JSON.stringify(data, null, 2));

        if (data.response_text || data.response) {
            console.log("   ✓ Chatbot responded correctly to test message");
        } else {
            console.log("   ⚠ Chatbot response format may be unexpected");
        }
    })
    .catch(error => {
        console.error("   ✗ API call failed:", error.message);
        console.log("   This indicates a connectivity or authentication issue");
    });
}

// Run diagnostics when page loads
if (typeof window !== 'undefined') {
    // Wait a bit for page to load
    setTimeout(diagnoseAuth, 1000);
} else {
    console.log("This script should run in a browser environment");
}

console.log("Check the console for diagnostic results...");