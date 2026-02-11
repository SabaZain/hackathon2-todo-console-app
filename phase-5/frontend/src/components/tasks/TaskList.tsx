'use client';

import { useState, useEffect } from 'react';
import { Task, TaskStatus, TaskPriority, TaskFilters } from '@/types';
import { apiService } from '@/services/api.service';

interface TaskListProps {
  onTaskClick?: (task: Task) => void;
  onTaskComplete?: (taskId: string) => void;
  onTaskEdit?: (task: Task) => void;
  onTaskDelete?: (taskId: string) => void;
}

export default function TaskList({
  onTaskClick,
  onTaskComplete,
  onTaskEdit,
  onTaskDelete,
}: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<TaskFilters>({});
  const [sortBy, setSortBy] = useState<'dueDate' | 'priority' | 'createdAt' | 'title'>('dueDate');

  useEffect(() => {
    loadTasks();
  }, [filters]);

  useEffect(() => {
    setTasks((prev) => sortTasks([...prev], sortBy));
  }, [sortBy]);

  const sortTasks = (tasksToSort: Task[], sortOption: string): Task[] => {
    const sorted = [...tasksToSort];

    switch (sortOption) {
      case 'dueDate':
        return sorted.sort((a, b) => {
          if (!a.dueDate && !b.dueDate) return 0;
          if (!a.dueDate) return 1;
          if (!b.dueDate) return -1;
          return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
        });

      case 'priority':
        const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
        return sorted.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

      case 'createdAt':
        return sorted.sort((a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        );

      case 'title':
        return sorted.sort((a, b) => a.title.localeCompare(b.title));

      default:
        return sorted;
    }
  };

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const queryParams = new URLSearchParams();
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.priority) queryParams.append('priority', filters.priority);
      if (filters.tags && filters.tags.length > 0) {
        queryParams.append('tags', filters.tags.join(','));
      }
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.dueDateFrom) queryParams.append('dueDateFrom', filters.dueDateFrom);
      if (filters.dueDateTo) queryParams.append('dueDateTo', filters.dueDateTo);

      const response = await apiService.get(
        `/tasks?${queryParams.toString()}`
      );
      const fetchedTasks = response.data || [];
      setTasks(sortTasks(fetchedTasks, sortBy));
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async (taskId: string) => {
    try {
      await apiService.post(`/tasks/${taskId}/complete`);
      await loadTasks(); // Reload to show updated status
      if (onTaskComplete) {
        onTaskComplete(taskId);
      }
    } catch (err: any) {
      alert(err.message || 'Failed to complete task');
    }
  };

  const handleDelete = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await apiService.delete(`/tasks/${taskId}`);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      if (onTaskDelete) {
        onTaskDelete(taskId);
      }
    } catch (err: any) {
      alert(err.message || 'Failed to delete task');
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getPriorityColor = (priority: TaskPriority) => {
    const colors = {
      HIGH: 'bg-red-100 text-red-800 border-red-200',
      MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      LOW: 'bg-green-100 text-green-800 border-green-200',
    };
    return colors[priority] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getStatusColor = (status: TaskStatus) => {
    const colors = {
      PENDING: 'bg-blue-100 text-blue-800',
      IN_PROGRESS: 'bg-purple-100 text-purple-800',
      COMPLETED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-gray-100 text-gray-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
        <button
          onClick={loadTasks}
          className="ml-4 text-sm underline hover:no-underline"
        >
          Retry
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg">No tasks found</p>
        <p className="text-sm mt-1">Create your first task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filter Controls */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filters.status || ''}
              onChange={(e) =>
                setFilters({ ...filters, status: e.target.value as TaskStatus || undefined })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            >
              <option value="">All</option>
              <option value="PENDING">Pending</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={filters.priority || ''}
              onChange={(e) =>
                setFilters({ ...filters, priority: e.target.value as TaskPriority || undefined })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            >
              <option value="">All</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            >
              <option value="dueDate">Due Date</option>
              <option value="priority">Priority</option>
              <option value="createdAt">Created Date</option>
              <option value="title">Title (A-Z)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              value={filters.search || ''}
              onChange={(e) =>
                setFilters({ ...filters, search: e.target.value || undefined })
              }
              placeholder="Search tasks..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
            />
          </div>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <h3
                    className="text-lg font-semibold text-gray-900 cursor-pointer hover:text-indigo-600"
                    onClick={() => onTaskClick && onTaskClick(task)}
                  >
                    {task.title}
                  </h3>
                  {task.isRecurring && (
                    <span
                      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800"
                      title="Recurring task"
                    >
                      🔄 Recurring
                    </span>
                  )}
                </div>

                {task.description && (
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {task.description}
                  </p>
                )}

                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                      task.status
                    )}`}
                  >
                    {task.status}
                  </span>

                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium border ${getPriorityColor(
                      task.priority
                    )}`}
                  >
                    {task.priority}
                  </span>

                  {task.dueDate && (
                    <span className="text-xs text-gray-500">
                      📅 Due: {formatDate(task.dueDate)}
                    </span>
                  )}
                </div>

                {task.tags && task.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {task.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-gray-100 text-gray-700"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                {task.status !== TaskStatus.COMPLETED && (
                  <button
                    onClick={() => handleComplete(task.id)}
                    className="px-3 py-1 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md"
                    title="Complete task"
                  >
                    ✓ Complete
                  </button>
                )}

                {onTaskEdit && (
                  <button
                    onClick={() => onTaskEdit(task)}
                    className="px-3 py-1 text-sm font-medium text-indigo-600 hover:text-indigo-800"
                    title="Edit task"
                  >
                    Edit
                  </button>
                )}

                <button
                  onClick={() => handleDelete(task.id)}
                  className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-800"
                  title="Delete task"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
