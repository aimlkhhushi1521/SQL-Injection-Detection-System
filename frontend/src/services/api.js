/**
 * API Service Layer
 * Centralized API calls to the Flask backend
 */

import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * API service object with all backend endpoints
 */
export const api = {
  /**
   * Authenticate user
   * @param {Object} credentials - {username, password}
   * @returns {Promise} Response with token and user data
   */
  login: (credentials) => apiClient.post('/login', credentials),

  /**
   * Register new user
   * @param {Object} userData - {username, password}
   * @returns {Promise} Response with user ID
   */
  register: (userData) => apiClient.post('/register', userData),

  /**
   * Test SQL query for injection
   * @param {string} query - SQL query to test
   * @param {number} userId - User ID (optional)
   * @returns {Promise} Detection result
   */
  testQuery: (query, userId = null) => {
    const data = { query };
    if (userId) {
      data.user_id = userId;
    }
    return apiClient.post('/test-query', data);
  },

  /**
   * Get detection logs
   * @param {number} limit - Number of logs to retrieve
   * @param {string} role - User role (admin/user)
   * @returns {Promise} Array of log entries
   */
  getLogs: (limit = 100, role = 'user') => 
    apiClient.get('/logs', { params: { limit, role } }),

  /**
   * Get dashboard statistics
   * @returns {Promise} Dashboard stats object
   */
  getDashboardStats: () => apiClient.get('/dashboard-stats'),

  /**
   * Logout user
   * @returns {Promise} Logout confirmation
   */
  logout: () => apiClient.post('/logout'),

  /**
   * Health check
   * @returns {Promise} Server status
   */
  healthCheck: () => apiClient.get('/health'),
};

export default api;
