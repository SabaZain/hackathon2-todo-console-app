'use client';

import { useState, useEffect } from 'react';
import { taskAPI } from '@/lib/api';
import { Task, TaskFormData } from '@/types';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: () => void;
  taskData?: Task;
}

const TaskModal = ({ isOpen, onClose, onSave, taskData }: TaskModalProps) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
    completed: false
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  // Populate form when taskData changes
  useEffect(() => {
    if (taskData) {
      setFormData({
        title: taskData.title,
        description: taskData.description || '',
        completed: taskData.completed
      });
    } else {
      setFormData({
        title: '',
        description: '',
        completed: false
      });
    }
  }, [taskData]);

  const handleChange = (field: keyof TaskFormData, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));

    // Clear error when user starts typing
    if (errors[field as keyof TaskFormData]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field as keyof TaskFormData];
        return newErrors;
      });
    }
  };

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) { // Backend validation is 200 chars
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    setIsLoading(true);

    try {
      if (taskData) {
        // Update existing task
        await taskAPI.updateTask(taskData.id, formData);
      } else {
        // Create new task
        await taskAPI.createTask(formData);
      }

      onSave();
    } catch (err) {
      console.error('Error saving task:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-95 animate-in fade-in-90 zoom-in-90">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-900">
              {taskData ? 'Edit Task' : 'Create New Task'}
            </h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors duration-200 p-1 rounded-full hover:bg-gray-100"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="space-y-5">
            <Input
              label="Title"
              placeholder="Task title"
              value={formData.title}
              onChange={(value) => handleChange('title', value)}
              error={errors.title}
              required
            />

            <Input
              label="Description"
              type="textarea"
              placeholder="Task description (optional)"
              value={formData.description || ''}
              onChange={(value) => handleChange('description', value)}
              error={errors.description}
            />

            <div className="flex items-center">
              <input
                type="checkbox"
                id="completed"
                checked={formData.completed}
                onChange={(e) => handleChange('completed', e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="completed" className="ml-2 block text-sm text-gray-700">
                Mark as completed
              </label>
            </div>
          </div>

          <div className="mt-8 flex justify-end space-x-3">
            <Button
              label="Cancel"
              type="secondary"
              onClick={onClose}
              disabled={isLoading}
            />
            <Button
              label={isLoading ? (taskData ? 'Updating...' : 'Creating...') : (taskData ? 'Update Task' : 'Create Task')}
              type="primary"
              onClick={handleSubmit}
              disabled={isLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskModal;