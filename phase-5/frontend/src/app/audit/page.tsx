'use client';

import { useState, useEffect } from 'react';
import AuditLogList from '@/components/audit/AuditLogList';
import { apiService } from '@/services/api.service';

interface AuditStats {
  totalOperations: number;
  recentActivity: number;
  operationCounts: Array<{
    operationType: string;
    count: number;
  }>;
  mostActiveTasks: Array<{
    taskId: string | null;
    count: number;
    task?: {
      id: string;
      title: string;
      status: string;
    };
  }>;
}

export default function AuditPage() {
  const [stats, setStats] = useState<AuditStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoadingStats(true);
      const response = await apiService.get('/audit/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load audit stats:', error);
    } finally {
      setLoadingStats(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Audit Trail</h1>
          <p className="mt-1 text-sm text-gray-500">
            Complete history of all task operations
          </p>
        </div>

        {/* Statistics */}
        {!loadingStats && stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            {/* Total Operations */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <span className="text-3xl">📊</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Operations</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalOperations}</p>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <span className="text-3xl">📅</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Last 7 Days</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recentActivity}</p>
                </div>
              </div>
            </div>

            {/* Operation Breakdown */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 md:col-span-2">
              <p className="text-sm font-medium text-gray-500 mb-3">Operations by Type</p>
              <div className="space-y-2">
                {stats.operationCounts.map((item) => (
                  <div key={item.operationType} className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">{item.operationType}</span>
                    <span className="text-sm font-semibold text-gray-900">{item.count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Most Active Tasks */}
        {!loadingStats && stats && stats.mostActiveTasks.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Most Active Tasks</h2>
            <div className="space-y-3">
              {stats.mostActiveTasks.map((item, index) => (
                <div
                  key={item.taskId || index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-lg font-bold text-gray-400">#{index + 1}</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {item.task?.title || 'Unknown Task'}
                      </p>
                      <p className="text-xs text-gray-500">
                        Status: {item.task?.status || 'N/A'}
                      </p>
                    </div>
                  </div>
                  <span className="text-sm font-semibold text-indigo-600">
                    {item.count} operations
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Audit Log List */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Activity History</h2>
          <AuditLogList />
        </div>
      </div>
    </div>
  );
}
