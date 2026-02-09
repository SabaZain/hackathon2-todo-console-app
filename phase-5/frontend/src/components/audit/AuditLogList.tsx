'use client';

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api.service';

interface AuditLog {
  id: string;
  timestamp: string;
  userId: string;
  taskId: string | null;
  operationType: 'CREATE' | 'UPDATE' | 'DELETE' | 'COMPLETE' | 'RESTORE';
  beforeState: any;
  afterState: any;
  correlationId: string;
  metadata: any;
  task?: {
    id: string;
    title: string;
    status: string;
  };
}

interface AuditLogListProps {
  taskId?: string;
}

export default function AuditLogList({ taskId }: AuditLogListProps) {
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    operationType: '',
    startDate: '',
    endDate: '',
  });

  useEffect(() => {
    loadAuditLogs();
  }, [taskId, filters]);

  const loadAuditLogs = async () => {
    try {
      setLoading(true);
      setError(null);

      const queryParams = new URLSearchParams();
      if (taskId) queryParams.append('taskId', taskId);
      if (filters.operationType) queryParams.append('operationType', filters.operationType);
      if (filters.startDate) queryParams.append('startDate', filters.startDate);
      if (filters.endDate) queryParams.append('endDate', filters.endDate);

      const endpoint = taskId
        ? `/audit/task/${taskId}`
        : `/audit?${queryParams.toString()}`;

      const response = await apiService.get(endpoint);
      setAuditLogs(response.data || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load audit logs');
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    });
  };

  const getOperationIcon = (operationType: string) => {
    const icons: Record<string, string> = {
      CREATE: '➕',
      UPDATE: '✏️',
      DELETE: '🗑️',
      COMPLETE: '✅',
      RESTORE: '♻️',
    };
    return icons[operationType] || '📝';
  };

  const getOperationColor = (operationType: string) => {
    const colors: Record<string, string> = {
      CREATE: 'bg-green-100 text-green-800',
      UPDATE: 'bg-blue-100 text-blue-800',
      DELETE: 'bg-red-100 text-red-800',
      COMPLETE: 'bg-purple-100 text-purple-800',
      RESTORE: 'bg-yellow-100 text-yellow-800',
    };
    return colors[operationType] || 'bg-gray-100 text-gray-800';
  };

  const getOperationDescription = (log: AuditLog) => {
    const taskTitle = log.task?.title || 'Unknown Task';

    switch (log.operationType) {
      case 'CREATE':
        return `Created task "${taskTitle}"`;
      case 'UPDATE':
        return `Updated task "${taskTitle}"`;
      case 'DELETE':
        return `Deleted task "${taskTitle}"`;
      case 'COMPLETE':
        return `Completed task "${taskTitle}"`;
      case 'RESTORE':
        return `Restored task "${taskTitle}"`;
      default:
        return `Performed ${log.operationType} on "${taskTitle}"`;
    }
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
          onClick={loadAuditLogs}
          className="ml-4 text-sm underline hover:no-underline"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      {!taskId && (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Operation Type
              </label>
              <select
                value={filters.operationType}
                onChange={(e) =>
                  setFilters({ ...filters, operationType: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">All Operations</option>
                <option value="CREATE">Create</option>
                <option value="UPDATE">Update</option>
                <option value="DELETE">Delete</option>
                <option value="COMPLETE">Complete</option>
                <option value="RESTORE">Restore</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Start Date
              </label>
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) =>
                  setFilters({ ...filters, startDate: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                End Date
              </label>
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) =>
                  setFilters({ ...filters, endDate: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </div>
      )}

      {/* Audit Log Timeline */}
      {auditLogs.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">No audit logs found</p>
          <p className="text-sm mt-1">Activity history will appear here</p>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="divide-y divide-gray-200">
            {auditLogs.map((log) => (
              <div key={log.id} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start space-x-3">
                  {/* Icon */}
                  <div className="flex-shrink-0">
                    <span className="text-2xl">{getOperationIcon(log.operationType)}</span>
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getOperationColor(
                          log.operationType
                        )}`}
                      >
                        {log.operationType}
                      </span>
                      <span className="text-sm text-gray-500">
                        {formatTimestamp(log.timestamp)}
                      </span>
                    </div>

                    <p className="text-sm text-gray-900 mb-2">
                      {getOperationDescription(log)}
                    </p>

                    {/* Show changes for UPDATE operations */}
                    {log.operationType === 'UPDATE' && log.beforeState && log.afterState && (
                      <div className="mt-2 text-xs">
                        <details className="cursor-pointer">
                          <summary className="text-indigo-600 hover:text-indigo-800">
                            View changes
                          </summary>
                          <div className="mt-2 p-2 bg-gray-50 rounded border border-gray-200">
                            <div className="grid grid-cols-2 gap-2">
                              <div>
                                <p className="font-medium text-gray-700 mb-1">Before:</p>
                                <pre className="text-xs overflow-auto">
                                  {JSON.stringify(log.beforeState, null, 2)}
                                </pre>
                              </div>
                              <div>
                                <p className="font-medium text-gray-700 mb-1">After:</p>
                                <pre className="text-xs overflow-auto">
                                  {JSON.stringify(log.afterState, null, 2)}
                                </pre>
                              </div>
                            </div>
                          </div>
                        </details>
                      </div>
                    )}

                    {/* Correlation ID */}
                    <p className="text-xs text-gray-400 mt-1">
                      ID: {log.correlationId.slice(0, 8)}...
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
