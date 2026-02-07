// Simple task update tracker to coordinate between chatbot and dashboard

interface TaskUpdateListener {
  id: string;
  callback: () => void;
}

class TaskUpdater {
  private listeners: TaskUpdateListener[] = [];
  private lastUpdateTimestamp: number = 0;

  // Subscribe to task updates
  subscribe(id: string, callback: () => void): () => void {
    const listener: TaskUpdateListener = { id, callback };
    this.listeners.push(listener);

    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l.id !== id);
    };
  }

  // Notify all subscribers of a task update
  notify(): void {
    console.log('Task updater notifying all subscribers');
    this.lastUpdateTimestamp = Date.now();
    this.listeners.forEach(listener => {
      try {
        listener.callback();
      } catch (error) {
        console.error('Error in task update listener:', error);
      }
    });
  }

  // Get the timestamp of the last update
  getLastUpdateTimestamp(): number {
    return this.lastUpdateTimestamp;
  }
}

// Export a singleton instance
export const taskUpdater = new TaskUpdater();

// Convenience function to trigger a task refresh
export const triggerTaskRefresh = () => {
  taskUpdater.notify();
};