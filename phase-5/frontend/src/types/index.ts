// Task types
export enum TaskStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
}

export enum TaskPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  tags: string[];
  dueDate?: string;
  completedAt?: string;
  isRecurring: boolean;
  recurrencePatternId?: string;
  parentTaskId?: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
  recurrencePattern?: RecurrencePattern;
  reminders?: Reminder[];
}

// Recurrence types
export enum RecurrenceFrequency {
  DAILY = 'DAILY',
  WEEKLY = 'WEEKLY',
  MONTHLY = 'MONTHLY',
  YEARLY = 'YEARLY',
  CUSTOM = 'CUSTOM',
}

export interface RecurrencePattern {
  id: string;
  frequency: RecurrenceFrequency;
  interval: number;
  dayOfWeek?: number;
  dayOfMonth?: number;
  endDate?: string;
  occurrencesCount?: number;
  createdAt: string;
  updatedAt: string;
}

// Reminder types
export enum ReminderChannel {
  PUSH = 'PUSH',
  EMAIL = 'EMAIL',
  IN_APP = 'IN_APP',
}

export enum ReminderStatus {
  PENDING = 'PENDING',
  SENT = 'SENT',
  FAILED = 'FAILED',
}

export interface Reminder {
  id: string;
  taskId: string;
  reminderTime: string;
  channels: ReminderChannel[];
  status: ReminderStatus;
  sentAt?: string;
  createdAt: string;
  updatedAt: string;
  task?: Task;
}

// Notification types
export interface Notification {
  id: string;
  userId: string;
  type: 'reminder' | 'task_update' | 'system';
  title: string;
  message: string;
  taskId?: string;
  reminderId?: string;
  createdAt: string;
  read: boolean;
}

// User types
export interface User {
  id: string;
  email: string;
  name: string;
  timezone: string;
  notificationPreferences: {
    push: boolean;
    email: boolean;
    inApp: boolean;
  };
  createdAt: string;
  updatedAt: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  count?: number;
}

// Filter types
export interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  tags?: string[];
  search?: string;
  dueDateFrom?: string;
  dueDateTo?: string;
}
