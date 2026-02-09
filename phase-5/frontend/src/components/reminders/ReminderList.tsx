'use client';

import { useState, useEffect } from 'react';
import { Reminder, ReminderStatus } from '@/types';
import { apiService } from '@/services/api.service';

interface ReminderListProps {
  taskId: string;
  onEdit?: (reminder: Reminder) => void;
  onDelete?: (reminderId: string) => void;
}

export default function ReminderList({
  taskId,
  onEdit,
  onDelete,
}: ReminderListProps) {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReminders();
  }, [taskId]);

  const loadReminders = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.get(`/tasks/${taskId}/reminders`);
      setReminders(response.data.data || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load reminders');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (reminderId: string) => {
    if (!confirm('Are you sure you want to delete this reminder?')) {
      return;
    }

    try {
      await apiService.delete(`/reminders/${reminderId}`);
      setReminders((prev) => prev.filter((r) => r.id !== reminderId));
      if (onDelete) {
        onDelete(reminderId);
      }
    } catch (err: any) {
      alert(err.message || 'Failed to delete reminder');
    }
  };

  const formatDateTime = (dateString: string) => {
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

  const getStatusBadge = (status: ReminderStatus) => {
    const styles = {
      PENDING: 'bg-yellow-100 text-yellow-800',
      SENT: 'bg-green-100 text-green-800',
      FAILED: 'bg-red-100 text-red-800',
    };

    return (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          styles[status] || 'bg-gray-100 text-gray-800'
        }`}
      >
        {status}
      </span>
    );
  };

  const getChannelIcons = (channels: string[]) => {
    const icons: Record<string, string> = {
      EMAIL: '📧',
      PUSH: '🔔',
      IN_APP: '💬',
    };

    return channels.map((channel) => (
      <span key={channel} className="text-lg" title={channel}>
        {icons[channel] || '❓'}
      </span>
    ));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  if (reminders.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No reminders set for this task</p>
        <p className="text-sm mt-1">Add a reminder to get notified</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {reminders.map((reminder) => (
        <div
          key={reminder.id}
          className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-sm font-medium text-gray-900">
                  {formatDateTime(reminder.reminderTime)}
                </span>
                {getStatusBadge(reminder.status)}
              </div>

              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <span>Channels:</span>
                <div className="flex space-x-1">
                  {getChannelIcons(reminder.channels)}
                </div>
              </div>

              {reminder.sentAt && (
                <div className="text-xs text-gray-500 mt-1">
                  Sent: {formatDateTime(reminder.sentAt)}
                </div>
              )}
            </div>

            <div className="flex space-x-2 ml-4">
              {reminder.status === 'PENDING' && onEdit && (
                <button
                  onClick={() => onEdit(reminder)}
                  className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                  title="Edit reminder"
                >
                  Edit
                </button>
              )}
              <button
                onClick={() => handleDelete(reminder.id)}
                className="text-red-600 hover:text-red-800 text-sm font-medium"
                title="Delete reminder"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
