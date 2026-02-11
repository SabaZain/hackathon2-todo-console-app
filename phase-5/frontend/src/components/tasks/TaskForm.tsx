'use client';

import { useState } from 'react';
import { Task, TaskPriority, RecurrenceFrequency } from '@/types';

interface TaskFormProps {
  onSubmit: (taskData: TaskFormData) => Promise<void>;
  onCancel: () => void;
  initialData?: Task;
  mode?: 'create' | 'edit';
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority: TaskPriority;
  tags: string[];
  dueDate?: string;
  isRecurring?: boolean;
  recurrencePattern?: {
    frequency: RecurrenceFrequency;
    interval: number;
    dayOfWeek?: number;
    dayOfMonth?: number;
    endDate?: string;
    occurrencesCount?: number;
  };
}

export default function TaskForm({
  onSubmit,
  onCancel,
  initialData,
  mode = 'create',
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [priority, setPriority] = useState<TaskPriority>(
    initialData?.priority || TaskPriority.MEDIUM
  );
  const [tags, setTags] = useState<string[]>(initialData?.tags || []);
  const [tagInput, setTagInput] = useState('');
  const [dueDate, setDueDate] = useState(
    initialData?.dueDate
      ? new Date(initialData.dueDate).toISOString().slice(0, 16)
      : ''
  );
  const [isRecurring, setIsRecurring] = useState(initialData?.isRecurring || false);

  // Recurrence pattern state
  const [frequency, setFrequency] = useState<RecurrenceFrequency>(
    initialData?.recurrencePattern?.frequency || RecurrenceFrequency.DAILY
  );
  const [interval, setInterval] = useState(
    initialData?.recurrencePattern?.interval || 1
  );
  const [dayOfWeek, setDayOfWeek] = useState<number | undefined>(
    initialData?.recurrencePattern?.dayOfWeek
  );
  const [dayOfMonth, setDayOfMonth] = useState<number | undefined>(
    initialData?.recurrencePattern?.dayOfMonth
  );
  const [endDate, setEndDate] = useState(
    initialData?.recurrencePattern?.endDate
      ? new Date(initialData.recurrencePattern.endDate).toISOString().slice(0, 10)
      : ''
  );
  const [occurrencesCount, setOccurrencesCount] = useState<number | undefined>(
    initialData?.recurrencePattern?.occurrencesCount
  );
  const [endType, setEndType] = useState<'never' | 'date' | 'count'>(
    initialData?.recurrencePattern?.endDate
      ? 'date'
      : initialData?.recurrencePattern?.occurrencesCount
      ? 'count'
      : 'never'
  );

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      setTags([...tags, trimmedTag]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (isRecurring && interval < 1) {
      setError('Interval must be at least 1');
      return;
    }

    if (isRecurring && frequency === RecurrenceFrequency.WEEKLY && dayOfWeek === undefined) {
      setError('Please select a day of the week for weekly recurrence');
      return;
    }

    if (isRecurring && frequency === RecurrenceFrequency.MONTHLY && dayOfMonth === undefined) {
      setError('Please select a day of the month for monthly recurrence');
      return;
    }

    setIsSubmitting(true);

    try {
      const taskData: TaskFormData = {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        tags,
        dueDate: dueDate || undefined,
      };

      if (isRecurring) {
        taskData.isRecurring = true;
        taskData.recurrencePattern = {
          frequency,
          interval,
          dayOfWeek: frequency === RecurrenceFrequency.WEEKLY ? dayOfWeek : undefined,
          dayOfMonth: frequency === RecurrenceFrequency.MONTHLY ? dayOfMonth : undefined,
          endDate: endType === 'date' && endDate ? endDate : undefined,
          occurrencesCount: endType === 'count' ? occurrencesCount : undefined,
        };
      }

      await onSubmit(taskData);
    } catch (err: any) {
      setError(err.message || 'Failed to save task');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getFrequencyLabel = () => {
    const labels: Record<RecurrenceFrequency, string> = {
      DAILY: 'day(s)',
      WEEKLY: 'week(s)',
      MONTHLY: 'month(s)',
      YEARLY: 'year(s)',
      CUSTOM: 'custom',
    };
    return labels[frequency];
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Title */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
          placeholder="Enter task title"
          required
        />
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
          placeholder="Enter task description"
        />
      </div>

      {/* Priority */}
      <div>
        <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
          Priority
        </label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value as TaskPriority)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
        >
          <option value={TaskPriority.LOW}>Low</option>
          <option value={TaskPriority.MEDIUM}>Medium</option>
          <option value={TaskPriority.HIGH}>High</option>
        </select>
      </div>

      {/* Tags */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
        <div className="flex space-x-2 mb-2">
          <input
            type="text"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleAddTag();
              }
            }}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            placeholder="Add a tag"
          />
          <button
            type="button"
            onClick={handleAddTag}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Add
          </button>
        </div>
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {tags.map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-indigo-100 text-indigo-800"
              >
                #{tag}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(tag)}
                  className="ml-2 text-indigo-600 hover:text-indigo-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Due Date */}
      <div>
        <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-1">
          Due Date
        </label>
        <input
          type="datetime-local"
          id="dueDate"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
        />
      </div>

      {/* Recurring Task Toggle */}
      <div className="border-t border-gray-200 pt-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={isRecurring}
            onChange={(e) => setIsRecurring(e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <span className="ml-2 text-sm font-medium text-gray-700">
            Make this a recurring task
          </span>
        </label>
      </div>

      {/* Recurrence Pattern */}
      {isRecurring && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 space-y-4">
          <h3 className="text-sm font-semibold text-gray-900">Recurrence Pattern</h3>

          {/* Frequency */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Repeat every
            </label>
            <div className="flex space-x-2">
              <input
                type="number"
                min="1"
                value={interval}
                onChange={(e) => setInterval(parseInt(e.target.value) || 1)}
                className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
              />
              <select
                value={frequency}
                onChange={(e) => setFrequency(e.target.value as RecurrenceFrequency)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
              >
                <option value={RecurrenceFrequency.DAILY}>Day(s)</option>
                <option value={RecurrenceFrequency.WEEKLY}>Week(s)</option>
                <option value={RecurrenceFrequency.MONTHLY}>Month(s)</option>
                <option value={RecurrenceFrequency.YEARLY}>Year(s)</option>
              </select>
            </div>
          </div>

          {/* Day of Week (for weekly) */}
          {frequency === RecurrenceFrequency.WEEKLY && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                On day
              </label>
              <select
                value={dayOfWeek ?? ''}
                onChange={(e) => setDayOfWeek(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                required
              >
                <option value="">Select a day</option>
                <option value="0">Sunday</option>
                <option value="1">Monday</option>
                <option value="2">Tuesday</option>
                <option value="3">Wednesday</option>
                <option value="4">Thursday</option>
                <option value="5">Friday</option>
                <option value="6">Saturday</option>
              </select>
            </div>
          )}

          {/* Day of Month (for monthly) */}
          {frequency === RecurrenceFrequency.MONTHLY && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                On day of month
              </label>
              <input
                type="number"
                min="1"
                max="31"
                value={dayOfMonth ?? ''}
                onChange={(e) => setDayOfMonth(parseInt(e.target.value) || undefined)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                placeholder="1-31"
                required
              />
            </div>
          )}

          {/* End Condition */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ends
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={endType === 'never'}
                  onChange={() => setEndType('never')}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">Never</span>
              </label>

              <label className="flex items-center">
                <input
                  type="radio"
                  checked={endType === 'date'}
                  onChange={() => setEndType('date')}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">On date</span>
              </label>
              {endType === 'date' && (
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="ml-6 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                />
              )}

              <label className="flex items-center">
                <input
                  type="radio"
                  checked={endType === 'count'}
                  onChange={() => setEndType('count')}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">After</span>
              </label>
              {endType === 'count' && (
                <div className="ml-6 flex items-center space-x-2">
                  <input
                    type="number"
                    min="1"
                    value={occurrencesCount ?? ''}
                    onChange={(e) => setOccurrencesCount(parseInt(e.target.value) || undefined)}
                    className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                  />
                  <span className="text-sm text-gray-700">occurrences</span>
                </div>
              )}
            </div>
          </div>

          {/* Preview */}
          <div className="bg-white border border-indigo-300 rounded p-3">
            <p className="text-xs font-medium text-gray-700 mb-1">Preview:</p>
            <p className="text-sm text-gray-900">
              Repeats every {interval} {getFrequencyLabel()}
              {frequency === RecurrenceFrequency.WEEKLY && dayOfWeek !== undefined && (
                <> on {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayOfWeek]}</>
              )}
              {frequency === RecurrenceFrequency.MONTHLY && dayOfMonth && (
                <> on day {dayOfMonth}</>
              )}
              {endType === 'date' && endDate && <>, until {new Date(endDate).toLocaleDateString()}</>}
              {endType === 'count' && occurrencesCount && <>, for {occurrencesCount} times</>}
              {endType === 'never' && <>, indefinitely</>}
            </p>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
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
          {isSubmitting ? 'Saving...' : mode === 'edit' ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}
