'use client';

import { useState, useEffect } from 'react';
import { taskAPI } from '@/lib/api';
import TaskItem from '@/components/task/TaskItem';
import TaskModal from '@/components/task/TaskModal';
import Button from '@/components/ui/Button';
import { Task } from '@/types';

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const fetchedTasks = await taskAPI.getTasks();
      setTasks(fetchedTasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskSaved = () => {
    setShowModal(false);
    setEditingTask(null);
    fetchTasks(); // Refresh the task list
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowModal(true);
  };

  const handleDeleteTask = async (taskId: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.deleteTask(taskId);
        fetchTasks(); // Refresh the task list
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      // Use the toggle completion API endpoint
      const result = await taskAPI.toggleTaskCompletion(task.id);
      fetchTasks(); // Refresh the task list
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    if (filter === 'pending') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // fallback for in-progress if needed
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading tasks...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <Button
            label="+ New Task"
            type="primary"
            onClick={() => {
              setEditingTask(null);
              setShowModal(true);
            }}
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex flex-wrap gap-2">
          {(['all', 'pending', 'completed'] as const).map((status) => (
            <button
              key={status}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 ${
                filter === status
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              onClick={() => setFilter(status)}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks</h3>
          <p className="text-gray-500 mb-4">
            {filter === 'all'
              ? 'Get started by creating a new task.'
              : `No ${filter} tasks found.`}
          </p>
          <Button
            label="Create your first task"
            type="primary"
            onClick={() => setShowModal(true)}
          />
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={handleEditTask}
              onDelete={handleDeleteTask}
              onToggleComplete={handleToggleComplete}
            />
          ))}
        </div>
      )}

      {showModal && (
        <TaskModal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false);
            setEditingTask(null);
          }}
          onSave={handleTaskSaved}
          taskData={editingTask || undefined}
        />
      )}
    </div>
  );
};

export default DashboardPage;