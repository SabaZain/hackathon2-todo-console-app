// Data types for the application

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: number;
  created_at: string; // ISO date string from backend
}

// Frontend-specific type for task form handling
export interface TaskFormData {
  title: string;
  description?: string;
  completed: boolean;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface UserFormData {
  name: string;
  email: string;
  password: string;
}

export interface SigninFormData {
  email: string;
  password: string;
}