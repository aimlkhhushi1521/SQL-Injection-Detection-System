/**
 * Dashboard Component
 * Displays statistics, charts, and recent attack logs
 */

import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, LineElement, PointElement } from 'chart.js';
import { Pie } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, LineElement, PointElement);

function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await api.getDashboardStats();
      if (response.data.success) {
        setStats(response.data.stats);
      }
    } catch (err) {
      setError('Failed to load dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      </div>
    );
  }

  // Prepare severity pie chart data
  const severityData = {
    labels: ['High', 'Medium', 'Low'],
    datasets: [
      {
        data: [
          stats?.severity?.high || 0,
          stats?.severity?.medium || 0,
          stats?.severity?.low || 0,
        ],
        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6'],
        borderColor: ['#dc2626', '#d97706', '#2563eb'],
        borderWidth: 2,
      },
    ],
  };

  const severityOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'Attack Severity Distribution',
        font: {
          size: 16,
        },
      },
    },
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Monitor SQL injection detection statistics</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Total Queries */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-primary-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Queries</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.total_queries || 0}</p>
            </div>
            <div className="bg-primary-100 p-3 rounded-full">
              <svg className="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Attacks Detected */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-danger-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Attacks Detected</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.total_attacks || 0}</p>
            </div>
            <div className="bg-danger-100 p-3 rounded-full">
              <svg className="h-8 w-8 text-danger-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Safe Queries */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-success-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Safe Queries</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats?.safe_queries || 0}</p>
            </div>
            <div className="bg-success-100 p-3 rounded-full">
              <svg className="h-8 w-8 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Attack Rate */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-warning-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Attack Rate</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.total_queries > 0 
                  ? ((stats?.total_attacks / stats?.total_queries) * 100).toFixed(1) 
                  : 0}%
              </p>
            </div>
            <div className="bg-warning-100 p-3 rounded-full">
              <svg className="h-8 w-8 text-warning-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Charts and Recent Attacks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Severity Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <Pie data={severityData} options={severityOptions} />
        </div>

        {/* Attack Types */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Attack Types</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {stats?.attack_types?.length > 0 ? (
              stats.attack_types.map((attack, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-700 font-medium">{attack.attack_type}</span>
                  <span className="bg-danger-100 text-danger-700 px-3 py-1 rounded-full text-xs font-semibold">
                    {attack.count}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No attacks detected yet</p>
            )}
          </div>
        </div>
      </div>

      {/* Recent Attacks Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Attacks</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Query</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Attack Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats?.recent_attacks?.length > 0 ? (
                stats.recent_attacks.map((attack) => (
                  <tr key={attack.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {attack.query.substring(0, 50)}{attack.query.length > 50 ? '...' : ''}
                      </code>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {attack.attack_type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        attack.severity === 'High' ? 'bg-danger-100 text-danger-700' :
                        attack.severity === 'Medium' ? 'bg-warning-100 text-warning-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {attack.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(attack.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                    No recent attacks
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
