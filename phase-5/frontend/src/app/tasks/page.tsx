'use client';

import { useState, useCallback } from 'react';
import TaskList from '@/components/tasks/TaskList';
import TaskForm, { TaskFormData } from '@/components/tasks/TaskForm';
import TaskDetail from '@/components/tasks/TaskDetail';
import { Task } from '@/types';
import { apiService } from '@/services/api.service';
import { useWebSocket } from '@/hooks/useWebSocket';

export default function TasksPage() {
  const [showForm, setShowForm] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [isConnected, setIsConnected] = useState(false);

  // WebSocket integration for real-time updates
  const handleTaskUpdate = useCallback((event: any) => {
    console.log('Real-time task update:', event);
    // Refresh the task list when any task is updated
    setRefreshKey((prev) => prev + 1);
  }, []);

  // Initialize WebSocket connection
  // TODO: Get actual userId and token from auth context
  const { subscribeToTask, unsubscribeFromTask } = useWebSocket({
    userId: 'demo-user', // Replace with actual user ID from auth
    token: 'demo-token', // Replace with actual JWT token from auth
    onTaskUpdate: handleTaskUpdate,
    onConnect: () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    },
    onDisconnect: () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    },
  });

  const handleCreateTask = async (taskData: TaskFormData) => {
    try {
      const endpoint = taskData.isRecurring ? '/tasks/recurring' : '/tasks';
      await apiService.post(endpoint, taskData);
      setShowForm(false);
      setRefreshKey((prev) => prev + 1); // Trigger refresh
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (taskData: TaskFormData) => {
    if (!editingTask) return;

    try {
      await apiService.put(`/tasks/${editingTask.id}`, taskData);
      setEditingTask(null);
      setRefreshKey((prev) => prev + 1); // Trigger refresh
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to update task');
    }
  };

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task);
  };

  const handleTaskEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(false);
    setSelectedTask(null);
  };

  const handleTaskComplete = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleTaskDelete = () => {
    setRefreshKey((prev) => prev + 1);
    setSelectedTask(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-3">
                <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
                {isConnected && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-1.5 animate-pulse"></span>
                    Live
                  </span>
                )}
              </div>
              <p className="mt-1 text-sm text-gray-500">
                Manage your tasks and recurring schedules
                {isConnected && ' • Real-time updates enabled'}
              </p>
            </div>
            <button
              onClick={() => {
                setShowForm(true);
                setEditingTask(null);
                setSelectedTask(null);
              }}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <svg
                className="h-5 w-5 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              New Task
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Task List */}
          <div className="lg:col-span-2">
            <TaskList
              key={refreshKey}
              onTaskClick={handleTaskClick}
              onTaskComplete={handleTaskComplete}
              onTaskEdit={handleTaskEdit}
              onTaskDelete={handleTaskDelete}
            />
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Create/Edit Form */}
            {(showForm || editingTask) && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  {editingTask ? 'Edit Task' : 'Create New Task'}
                </h2>
                <TaskForm
                  onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
                  onCancel={() => {
                    setShowForm(false);
                    setEditingTask(null);
                  }}
                  initialData={editingTask || undefined}
                  mode={editingTask ? 'edit' : 'create'}
                />
              </div>
            )}

            {/* Task Detail */}
            {selectedTask && !showForm && !editingTask && (
              <TaskDetail
                task={selectedTask}
                onClose={() => setSelectedTask(null)}
                onEdit={() => handleTaskEdit(selectedTask)}
                onDelete={() => {
                  handleTaskDelete();
                  setSelectedTask(null);
                }}
                onRefresh={() => setRefreshKey((prev) => prev + 1)}
              />
            )}

            {/* Empty State */}
            {!showForm && !editingTask && !selectedTask && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
                <div className="text-gray-400 mb-4">
                  <svg
                    className="mx-auto h-12 w-12"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                    />
                  </svg>
                </div>
                <p className="text-sm text-gray-500">
                  Select a task to view details or create a new task to get started
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
