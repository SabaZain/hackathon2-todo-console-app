'use client';

import { useState } from 'react';
import { ReminderChannel } from '@/types';

interface ReminderFormProps {
  taskId: string;
  onSubmit: (reminderData: ReminderFormData) => Promise<void>;
  onCancel: () => void;
  initialData?: ReminderFormData;
}

export interface ReminderFormData {
  reminderTime: string;
  channels: ReminderChannel[];
}

export default function ReminderForm({
  taskId: _taskId,
  onSubmit,
  onCancel,
  initialData,
}: ReminderFormProps) {
  const [reminderTime, setReminderTime] = useState(
    initialData?.reminderTime || ''
  );
  const [channels, setChannels] = useState<ReminderChannel[]>(
    initialData?.channels || [ReminderChannel.IN_APP]
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChannelToggle = (channel: ReminderChannel) => {
    setChannels((prev) =>
      prev.includes(channel)
        ? prev.filter((c) => c !== channel)
        : [...prev, channel]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!reminderTime) {
      setError('Please select a reminder time');
      return;
    }

    if (channels.length === 0) {
      setError('Please select at least one notification channel');
      return;
    }

    const reminderDate = new Date(reminderTime);
    if (reminderDate <= new Date()) {
      setError('Reminder time must be in the future');
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit({
        reminderTime,
        channels,
      });
    } catch (err: any) {
      setError(err.message || 'Failed to create reminder');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="reminderTime"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Reminder Time
        </label>
        <input
          type="datetime-local"
          id="reminderTime"
          value={reminderTime}
          onChange={(e) => setReminderTime(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
          required
        />
        <p className="mt-1 text-xs text-gray-500">
          Set when you want to be reminded about this task
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Notification Channels
        </label>
        <div className="space-y-2">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={channels.includes(ReminderChannel.IN_APP)}
              onChange={() => handleChannelToggle(ReminderChannel.IN_APP)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              In-App Notification
            </span>
          </label>

          <label className="flex items-center">
            <input
              type="checkbox"
              checked={channels.includes(ReminderChannel.EMAIL)}
              onChange={() => handleChannelToggle(ReminderChannel.EMAIL)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">Email</span>
          </label>

          <label className="flex items-center">
            <input
              type="checkbox"
              checked={channels.includes(ReminderChannel.PUSH)}
              onChange={() => handleChannelToggle(ReminderChannel.PUSH)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">
              Push Notification
            </span>
          </label>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Creating...' : 'Create Reminder'}
        </button>
      </div>
    </form>
  );
}
