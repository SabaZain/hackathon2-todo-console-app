'use client';

import { useState } from 'react';
import { Task, TaskStatus, TaskPriority } from '@/types';
import ReminderList from '@/components/reminders/ReminderList';
import ReminderForm, { ReminderFormData } from '@/components/reminders/ReminderForm';
import { apiService } from '@/services/api.service';

interface TaskDetailProps {
  task: Task;
  onClose: () => void;
  onEdit: () => void;
  onDelete: () => void;
  onRefresh: () => void;
}

export default function TaskDetail({
  task,
  onClose,
  onEdit,
  onDelete,
  onRefresh,
}: TaskDetailProps) {
  const [showReminderForm, setShowReminderForm] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);

  const handleComplete = async () => {
    if (!confirm('Mark this task as complete?')) {
      return;
    }

    setIsCompleting(true);
    try {
      await apiService.post(`/tasks/${task.id}/complete`);
      onRefresh();
    } catch (error: any) {
      alert(error.message || 'Failed to complete task');
    } finally {
      setIsCompleting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await apiService.delete(`/tasks/${task.id}`);
      onDelete();
    } catch (error: any) {
      alert(error.message || 'Failed to delete task');
    }
  };

  const handleCreateReminder = async (reminderData: ReminderFormData) => {
    try {
      await apiService.post('/reminders', {
        taskId: task.id,
        ...reminderData,
      });
      setShowReminderForm(false);
      onRefresh();
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to create reminder');
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not set';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
  };

  const getPriorityColor = (priority: TaskPriority) => {
    const colors = {
      HIGH: 'text-red-700 bg-red-100 border-red-200',
      MEDIUM: 'text-yellow-700 bg-yellow-100 border-yellow-200',
      LOW: 'text-green-700 bg-green-100 border-green-200',
    };
    return colors[priority] || 'text-gray-700 bg-gray-100 border-gray-200';
  };

  const getStatusColor = (status: TaskStatus) => {
    const colors = {
      PENDING: 'text-blue-700 bg-blue-100',
      IN_PROGRESS: 'text-purple-700 bg-purple-100',
      COMPLETED: 'text-green-700 bg-green-100',
      CANCELLED: 'text-gray-700 bg-gray-100',
    };
    return colors[status] || 'text-gray-700 bg-gray-100';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-start justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Task Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            title="Close"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="px-6 py-4 space-y-4">
        {/* Title */}
        <div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">{task.title}</h3>
          {task.isRecurring && (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              🔄 Recurring Task
            </span>
          )}
        </div>

        {/* Description */}
        {task.description && (
          <div>
            <p className="text-sm text-gray-600">{task.description}</p>
          </div>
        )}

        {/* Status and Priority */}
        <div className="flex flex-wrap gap-2">
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
              task.status
            )}`}
          >
            Status: {task.status}
          </span>
          <span
            className={`inline-flex items-center px-3 py-1 rounded text-xs font-medium border ${getPriorityColor(
              task.priority
            )}`}
          >
            Priority: {task.priority}
          </span>
        </div>

        {/* Due Date */}
        <div className="text-sm">
          <span className="font-medium text-gray-700">Due Date:</span>
          <span className="ml-2 text-gray-600">{formatDate(task.dueDate)}</span>
        </div>

        {/* Completed At */}
        {task.completedAt && (
          <div className="text-sm">
            <span className="font-medium text-gray-700">Completed:</span>
            <span className="ml-2 text-gray-600">{formatDate(task.completedAt)}</span>
          </div>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div>
            <span className="text-sm font-medium text-gray-700 block mb-2">Tags:</span>
            <div className="flex flex-wrap gap-1">
              {task.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Recurrence Pattern */}
        {task.isRecurring && task.recurrencePattern && (
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-3">
            <span className="text-sm font-medium text-gray-700 block mb-1">
              Recurrence Pattern:
            </span>
            <p className="text-sm text-gray-900">
              Every {task.recurrencePattern.interval}{' '}
              {task.recurrencePattern.frequency.toLowerCase()}
              {task.recurrencePattern.dayOfWeek !== undefined &&
                ` on ${
                  ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][
                    task.recurrencePattern.dayOfWeek
                  ]
                }`}
              {task.recurrencePattern.dayOfMonth !== undefined &&
                ` on day ${task.recurrencePattern.dayOfMonth}`}
            </p>
            {task.recurrencePattern.endDate && (
              <p className="text-xs text-gray-600 mt-1">
                Until: {formatDate(task.recurrencePattern.endDate)}
              </p>
            )}
            {task.recurrencePattern.occurrencesCount && (
              <p className="text-xs text-gray-600 mt-1">
                For {task.recurrencePattern.occurrencesCount} occurrences
              </p>
            )}
          </div>
        )}

        {/* Timestamps */}
        <div className="text-xs text-gray-500 space-y-1 pt-2 border-t border-gray-200">
          <div>Created: {formatDate(task.createdAt)}</div>
          <div>Updated: {formatDate(task.updatedAt)}</div>
        </div>

        {/* Reminders Section */}
        <div className="pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-900">Reminders</h4>
            {!showReminderForm && task.status !== TaskStatus.COMPLETED && (
              <button
                onClick={() => setShowReminderForm(true)}
                className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
              >
                + Add Reminder
              </button>
            )}
          </div>

          {showReminderForm ? (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <ReminderForm
                taskId={task.id}
                onSubmit={handleCreateReminder}
                onCancel={() => setShowReminderForm(false)}
              />
            </div>
          ) : (
            <ReminderList taskId={task.id} />
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="px-6 py-4 border-t border-gray-200 flex justify-between">
        <div className="space-x-2">
          {task.status !== TaskStatus.COMPLETED && (
            <button
              onClick={handleComplete}
              disabled={isCompleting}
              className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isCompleting ? 'Completing...' : '✓ Complete'}
            </button>
          )}
          <button
            onClick={onEdit}
            className="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-800"
          >
            Edit
          </button>
        </div>
        <button
          onClick={handleDelete}
          className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-800"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
