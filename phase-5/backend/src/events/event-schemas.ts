export const EventTypes = {
  // Task events
  TASK_CREATED: 'task.created',
  TASK_UPDATED: 'task.updated',
  TASK_DELETED: 'task.deleted',
  TASK_COMPLETED: 'task.completed',
  TASK_RESTORED: 'task.restored',

  // Reminder events
  REMINDER_SCHEDULED: 'reminder.scheduled',
  REMINDER_SENT: 'reminder.sent',
  REMINDER_FAILED: 'reminder.failed',

  // Audit events
  AUDIT_CREATE: 'audit.create',
  AUDIT_UPDATE: 'audit.update',
  AUDIT_DELETE: 'audit.delete',
  AUDIT_COMPLETE: 'audit.complete',
  AUDIT_RESTORE: 'audit.restore',
} as const;

export const Topics = {
  TASK_EVENTS: 'task-events',
  TASK_UPDATES: 'task-updates',
  REMINDERS: 'reminders',
  AUDIT_LOGS: 'audit-logs',
} as const;

export interface BaseEvent {
  eventId: string;
  eventType: string;
  timestamp: string;
  userId: string;
  correlationId: string;
  metadata: {
    sourceService: string;
    version: string;
  };
}

export interface TaskEvent extends BaseEvent {
  taskId: string;
  payload: {
    task: {
      id: string;
      title: string;
      description?: string;
      status: string;
      priority: string;
      tags: string[];
      dueDate?: string;
      isRecurring: boolean;
      recurrencePattern?: any;
      createdAt: string;
      updatedAt: string;
    };
  };
}

export interface TaskUpdateEvent extends BaseEvent {
  taskId: string;
  payload: {
    changes: Record<string, any>;
  };
}

export interface ReminderEvent extends BaseEvent {
  taskId: string;
  payload: {
    reminder: {
      id: string;
      taskId: string;
      reminderTime: string;
      channels: string[];
      status: string;
    };
  };
}

export interface AuditLogEvent extends BaseEvent {
  taskId?: string;
  payload: {
    operationType: string;
    beforeState: Record<string, any> | null;
    afterState: Record<string, any> | null;
  };
}

export type Event = TaskEvent | TaskUpdateEvent | ReminderEvent | AuditLogEvent;
