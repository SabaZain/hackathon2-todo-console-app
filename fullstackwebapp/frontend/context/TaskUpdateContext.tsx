'use client';

import React, { createContext, useContext, ReactNode, useEffect, useCallback } from 'react';

interface TaskUpdateContextType {
  triggerRefresh: () => void;
  subscribe: (callback: () => void) => () => void; // Returns unsubscribe function
}

const TaskUpdateContext = createContext<TaskUpdateContextType | undefined>(undefined);

export const TaskUpdateProvider = ({ children }: { children: ReactNode }) => {
  const subscribers = React.useRef<Set<() => void>>(new Set());

  const triggerRefresh = useCallback(() => {
    subscribers.current.forEach(callback => {
      try {
        callback();
      } catch (error) {
        console.error('Error in task update subscriber:', error);
      }
    });
  }, []);

  const subscribe = useCallback((callback: () => void) => {
    subscribers.current.add(callback);

    // Return unsubscribe function
    return () => {
      subscribers.current.delete(callback);
    };
  }, []);

  // Set up global event listener for task updates
  useEffect(() => {
    const handleGlobalTaskUpdate = () => {
      triggerRefresh();
    };

    window.addEventListener('taskUpdated', handleGlobalTaskUpdate);

    return () => {
      window.removeEventListener('taskUpdated', handleGlobalTaskUpdate);
    };
  }, [triggerRefresh]);

  return (
    <TaskUpdateContext.Provider value={{ triggerRefresh, subscribe }}>
      {children}
    </TaskUpdateContext.Provider>
  );
};

export const useTaskUpdate = () => {
  const context = useContext(TaskUpdateContext);
  if (context === undefined) {
    throw new Error('useTaskUpdate must be used within a TaskUpdateProvider');
  }
  return context;
};