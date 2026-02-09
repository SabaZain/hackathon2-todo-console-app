'use client';

import { useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface TaskUpdateEvent {
  eventType: string;
  taskId: string;
  payload: any;
  timestamp: string;
}

interface UseWebSocketOptions {
  userId: string;
  token: string;
  onTaskUpdate?: (event: TaskUpdateEvent) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Error) => void;
}

export function useWebSocket({
  userId,
  token,
  onTaskUpdate,
  onConnect,
  onDisconnect,
  onError,
}: UseWebSocketOptions) {
  const socketRef = useRef<Socket | null>(null);
  const isConnectedRef = useRef(false);

  useEffect(() => {
    // Create socket connection
    const socket = io(process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:3001', {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    socketRef.current = socket;

    // Handle connection
    socket.on('connect', () => {
      console.log('WebSocket connected:', socket.id);

      // Authenticate
      socket.emit('authenticate', { userId, token });
    });

    // Handle authentication success
    socket.on('authenticated', (data: { success: boolean }) => {
      if (data.success) {
        console.log('WebSocket authenticated');
        isConnectedRef.current = true;
        if (onConnect) {
          onConnect();
        }
      }
    });

    // Handle task updates
    socket.on('task:update', (event: TaskUpdateEvent) => {
      console.log('Task update received:', event);
      if (onTaskUpdate) {
        onTaskUpdate(event);
      }
    });

    // Handle disconnection
    socket.on('disconnect', (reason: string) => {
      console.log('WebSocket disconnected:', reason);
      isConnectedRef.current = false;
      if (onDisconnect) {
        onDisconnect();
      }
    });

    // Handle errors
    socket.on('connect_error', (error: Error) => {
      console.error('WebSocket connection error:', error);
      if (onError) {
        onError(error);
      }
    });

    // Cleanup on unmount
    return () => {
      if (socket) {
        socket.disconnect();
      }
    };
  }, [userId, token, onTaskUpdate, onConnect, onDisconnect, onError]);

  // Subscribe to specific task
  const subscribeToTask = useCallback((taskId: string) => {
    if (socketRef.current && isConnectedRef.current) {
      socketRef.current.emit('subscribe:task', taskId);
      console.log('Subscribed to task:', taskId);
    }
  }, []);

  // Unsubscribe from specific task
  const unsubscribeFromTask = useCallback((taskId: string) => {
    if (socketRef.current && isConnectedRef.current) {
      socketRef.current.emit('unsubscribe:task', taskId);
      console.log('Unsubscribed from task:', taskId);
    }
  }, []);

  return {
    isConnected: isConnectedRef.current,
    subscribeToTask,
    unsubscribeFromTask,
  };
}
