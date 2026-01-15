// API client for frontend-backend integration

import { Task, User, TaskFormData, UserFormData, SigninFormData } from '@/types';

// Base API URL - will be configured based on environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8001';

// Helper function to add auth token to headers
// NOTE: Authentication is temporarily bypassed for local development
// Headers will not include Authorization since backend bypasses JWT validation
const getAuthHeaders = () => {
  return {
    'Content-Type': 'application/json',
  };
};

// Helper function to handle API responses
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Authentication API (stubs for now until backend auth is implemented)
export const authAPI = {
  signin: async (credentials: SigninFormData): Promise<{ token: string; user: User }> => {
    console.log('Signin attempt with:', credentials);

    // For now, simulate successful login with a mock token
    // In the future, this would connect to the backend auth endpoint
    const mockToken = 'mock-jwt-token-for-testing';
    const mockUser: User = {
      id: 'user-1',
      name: 'Test User',
      email: credentials.email
    };

    // Store token in localStorage
    localStorage.setItem('token', mockToken);

    return { token: mockToken, user: mockUser };
  },

  signup: async (userData: UserFormData): Promise<{ user: User }> => {
    console.log('Signup attempt with:', userData);

    // For now, simulate successful registration with a mock user
    // In the future, this would connect to the backend auth endpoint
    const mockUser: User = {
      id: 'user-' + Date.now(),
      name: userData.name,
      email: userData.email
    };

    return { user: mockUser };
  },

  signout: async (): Promise<void> => {
    // Remove token from localStorage
    localStorage.removeItem('token');
  }
};

// Task API
export const taskAPI = {
  getTasks: async (): Promise<Task[]> => {
    console.log('Fetching tasks from backend');

    const headers = getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/tasks`, {
      method: 'GET',
      headers,
    });

    const tasks = await handleResponse(response);

    // Map backend task properties to frontend Task interface
    return tasks.map((task: any) => ({
      id: task.id,
      title: task.title,
      description: task.description,
      completed: task.completed,
      owner_id: task.owner_id,
      created_at: task.created_at
    }));
  },

  createTask: async (taskData: TaskFormData): Promise<Task> => {
    console.log('Creating task:', taskData);

    const headers = getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/tasks`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed || false, // Default to false if not provided
      }),
    });

    const newTask = await handleResponse(response);

    // Map backend response to frontend Task interface
    return {
      id: newTask.id,
      title: newTask.title,
      description: newTask.description,
      completed: newTask.completed,
      owner_id: newTask.owner_id,
      created_at: newTask.created_at
    };
  },

  updateTask: async (id: number, taskData: TaskFormData): Promise<Task> => {
    console.log('Updating task:', id, taskData);

    const headers = getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description,
        completed: taskData.completed,
      }),
    });

    const updatedTask = await handleResponse(response);

    // Map backend response to frontend Task interface
    return {
      id: updatedTask.id,
      title: updatedTask.title,
      description: updatedTask.description,
      completed: updatedTask.completed,
      owner_id: updatedTask.owner_id,
      created_at: updatedTask.created_at
    };
  },

  deleteTask: async (id: number): Promise<void> => {
    console.log('Deleting task:', id);

    const headers = getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Delete failed' }));
      throw new Error(errorData.detail || 'Delete failed');
    }

    return response.json(); // Returns the success message
  },

  toggleTaskCompletion: async (id: number): Promise<{ task_id: number; completed: boolean }> => {
    console.log('Toggling task completion:', id);

    const headers = getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/api/tasks/${id}/complete`, {
      method: 'PATCH',
      headers,
    });

    return handleResponse(response);
  }
};

// DEV NOTE: This bypass is for hackathon demo & local testing
// JWT auth will be restored later for production