export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">Phase 5 Todo Application</h1>
        <p className="text-lg mb-8">
          Event-Driven Architecture with Kafka, Dapr, and Kubernetes
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">🔄 Recurring Tasks</h2>
            <p className="text-gray-600">
              Create tasks that repeat automatically on your schedule
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">⏰ Reminders</h2>
            <p className="text-gray-600">
              Get notified via push, email, or in-app notifications
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">🔍 Search & Filter</h2>
            <p className="text-gray-600">
              Find tasks quickly with powerful search and filtering
            </p>
          </div>

          <div className="border border-gray-300 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">📊 Audit Trail</h2>
            <p className="text-gray-600">
              Complete history of all task operations
            </p>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            Status: 🚧 In Development | Phase 5 Implementation
          </p>
        </div>
      </div>
    </main>
  );
}
