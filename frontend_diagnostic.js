// Diagnostic script to check frontend chatbot communication
console.log("=== Frontend Chatbot Communication Diagnostic ===");

function runFrontendDiagnostic() {
    console.log("\n1. Checking authentication state...");

    // Check if token exists in localStorage
    const token = localStorage.getItem('token');
    console.log("   Token in localStorage:", token ? "YES" : "NO");

    if (token) {
        console.log("   Token preview:", token.substring(0, 30) + "...");

        // Decode JWT to check user ID
        try {
            const parts = token.split('.');
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
                console.log("   JWT Payload:", payload);

                const userId = payload.user_id || payload.userId || payload.sub || payload.id;
                console.log("   Extracted User ID:", userId);
            }
        } catch (e) {
            console.error("   Error decoding JWT:", e.message);
        }
    }

    console.log("\n2. Checking for todo_user_id in localStorage...");
    const todoUserId = localStorage.getItem('todo_user_id');
    console.log("   todo_user_id:", todoUserId);

    console.log("\n3. Checking if ChatBotWrapper should render...");
    const isAuthenticated = !!(token && (payload?.user_id || payload?.userId || payload?.sub || payload?.id));
    console.log("   Would ChatBotWrapper render:", isAuthenticated);

    console.log("\n4. Testing API endpoint accessibility...");

    if (token && todoUserId) {
        console.log("   Ready to make API call with:");
        console.log("   - User ID:", todoUserId);
        console.log("   - Token available: YES");

        // Test API call
        testApiCall(todoUserId, token);
    } else {
        console.log("   Cannot make API call - missing token or user ID");
        console.log("   This explains why chatbot isn't working!");
    }
}

async function testApiCall(userId, token) {
    console.log("\n5. Testing API call to backend...");

    const testMessage = "Test message from frontend diagnostic";

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/${userId}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ message: testMessage })
        });

        console.log("   Response status:", response.status);

        if (response.ok) {
            const data = await response.json();
            console.log("   Response data:", JSON.stringify(data, null, 2));

            if (data.response_text) {
                console.log("   ✅ API call successful - chatbot responded!");
            } else {
                console.log("   ⚠️  API call returned unexpected format");
            }
        } else {
            const errorText = await response.text();
            console.log("   ❌ API call failed:", errorText);
        }
    } catch (error) {
        console.log("   ❌ Network error:", error.message);
    }
}

// Run diagnostic
runFrontendDiagnostic();

console.log("\nCheck the console for diagnostic results...");