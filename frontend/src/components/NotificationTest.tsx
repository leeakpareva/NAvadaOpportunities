import React, { useState } from 'react';
import { testNotifications } from '../lib/api';
import type { NotificationTestResponse } from '../types/files';

export const NotificationTest: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<NotificationTestResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTestNotifications = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await testNotifications();
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to test notifications');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Test Notifications</h2>
      
      <button
        onClick={handleTestNotifications}
        disabled={loading}
        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
          loading ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
        } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
      >
        {loading ? 'Testing...' : 'Test Notifications'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Test Results:</h3>
          <div className="space-y-2">
            <p>
              Job Notifications:{' '}
              <span className="font-mono">
                {result.results.job_notifications.success}/{result.results.job_notifications.total}
              </span>{' '}
              successful
            </p>
            <p>
              PR Notifications:{' '}
              <span className="font-mono">
                {result.results.pr_notifications.filter(Boolean).length}/
                {result.results.pr_notifications.length}
              </span>{' '}
              successful
            </p>
            <p className="text-sm text-gray-600">{result.message}</p>
          </div>
        </div>
      )}
    </div>
  );
};
