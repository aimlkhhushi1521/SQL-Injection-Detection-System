/**
 * Query Tester Component
 * Real-time SQL injection detection with security comparison demo
 */

import React, { useState } from 'react';
import { api } from '../services/api';

function QueryTester({ user }) {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTestQuery = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a SQL query to test');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await api.testQuery(query, user?.id);
      
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.message || 'Query testing failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResult(null);
    setError('');
  };

  // Example queries for testing
  const safeExamples = [
    "SELECT * FROM users WHERE id = 1",
    "SELECT name, email FROM customers WHERE active = 1",
    "INSERT INTO orders (user_id, product_id) VALUES (5, 10)",
  ];

  const attackExamples = [
    "' OR 1=1 --",
    "' UNION SELECT username, password FROM users --",
    "'; DROP TABLE users --",
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">SQL Query Tester</h1>
        <p className="text-gray-600 mt-2">Test SQL queries for injection vulnerabilities in real-time</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Query Input Section */}
        <div className="space-y-6">
          {/* Input Form */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Test Your Query</h2>
            <form onSubmit={handleTestQuery}>
              <div className="mb-4">
                <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                  SQL Query
                </label>
                <textarea
                  id="query"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 font-mono text-sm"
                  placeholder="Enter SQL query to test..."
                />
              </div>

              {error && (
                <div className="mb-4 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    'Test Query'
                  )}
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Clear
                </button>
              </div>
            </form>
          </div>

          {/* Result Display */}
          {result && (
            <div className={`rounded-lg shadow-md p-6 border-l-4 ${
              result.is_attack 
                ? 'bg-danger-50 border-danger-500' 
                : 'bg-success-50 border-success-500'
            }`}>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  {result.is_attack ? (
                    <svg className="h-8 w-8 text-danger-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  ) : (
                    <svg className="h-8 w-8 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                </div>
                <div className="ml-4 flex-1">
                  <h3 className={`text-lg font-semibold ${
                    result.is_attack ? 'text-danger-900' : 'text-success-900'
                  }`}>
                    {result.is_attack ? 'SQL Injection Detected!' : 'Query Appears Safe'}
                  </h3>
                  
                  <div className="mt-4 space-y-2">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-700">Detection Method:</span>
                        <p className="text-gray-900 capitalize">{result.method}</p>
                      </div>
                      <div>
                        <span className="font-medium text-gray-700">Confidence:</span>
                        <p className="text-gray-900">{(result.confidence * 100).toFixed(1)}%</p>
                      </div>
                      {result.attack_type && (
                        <div>
                          <span className="font-medium text-gray-700">Attack Type:</span>
                          <p className="text-gray-900">{result.attack_type}</p>
                        </div>
                      )}
                      {result.severity && (
                        <div>
                          <span className="font-medium text-gray-700">Severity:</span>
                          <span className={`ml-2 px-3 py-1 rounded-full text-xs font-semibold ${
                            result.severity === 'High' ? 'bg-danger-100 text-danger-700' :
                            result.severity === 'Medium' ? 'bg-warning-100 text-warning-700' :
                            'bg-blue-100 text-blue-700'
                          }`}>
                            {result.severity}
                          </span>
                        </div>
                      )}
                    </div>
                    
                    <div className="mt-4 p-3 bg-white rounded-lg border border-gray-200">
                      <span className="font-medium text-gray-700 text-sm">Recommendation:</span>
                      <p className="text-gray-900 text-sm mt-1">{result.recommendation}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Example Queries */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Example Queries</h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-success-700 mb-2">✓ Safe Queries (Click to test)</p>
                <div className="space-y-2">
                  {safeExamples.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(example)}
                      className="w-full text-left text-xs font-mono bg-success-50 hover:bg-success-100 text-success-900 px-3 py-2 rounded border border-success-200 transition-colors"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-danger-700 mb-2">✗ Attack Queries (Click to test)</p>
                <div className="space-y-2">
                  {attackExamples.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(example)}
                      className="w-full text-left text-xs font-mono bg-danger-50 hover:bg-danger-100 text-danger-900 px-3 py-2 rounded border border-danger-200 transition-colors"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Security Comparison Demo */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Security Best Practices</h2>
            
            {/* Vulnerable Query Example */}
            <div className="mb-6">
              <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
                <div className="flex items-center mb-2">
                  <svg className="h-5 w-5 text-danger-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <h3 className="font-semibold text-danger-900">VULNERABLE (Don't Do This)</h3>
                </div>
                <pre className="text-xs font-mono text-danger-800 bg-white p-3 rounded mt-2 overflow-x-auto">
{`# Python - VULNERABLE to SQL Injection
user_input = request.form['username']
query = "SELECT * FROM users WHERE username = '" + user_input + "'"
cursor.execute(query)`}
                </pre>
                <p className="text-xs text-danger-700 mt-2">
                  <strong>Risk:</strong> User input is directly concatenated into the query, allowing attackers to inject malicious SQL code.
                </p>
              </div>
            </div>

            {/* Secure Query Example */}
            <div className="mb-6">
              <div className="bg-success-50 border border-success-200 rounded-lg p-4">
                <div className="flex items-center mb-2">
                  <svg className="h-5 w-5 text-success-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <h3 className="font-semibold text-success-900">SECURE (Use Parameterized Queries)</h3>
                </div>
                <pre className="text-xs font-mono text-success-800 bg-white p-3 rounded mt-2 overflow-x-auto">
{`# Python - SECURE with Parameterized Query
user_input = request.form['username']
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (user_input,))`}
                </pre>
                <p className="text-xs text-success-700 mt-2">
                  <strong>Safe:</strong> User input is treated as data, not executable code. The database driver handles escaping automatically.
                </p>
              </div>
            </div>

            {/* Key Security Tips */}
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
              <h3 className="font-semibold text-primary-900 mb-3 flex items-center">
                <svg className="h-5 w-5 text-primary-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Security Tips
              </h3>
              <ul className="space-y-2 text-sm text-primary-800">
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Always use parameterized queries (prepared statements)</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Validate and sanitize all user inputs</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Use stored procedures where possible</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Implement least privilege database access</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Enable Web Application Firewall (WAF)</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Regularly update and patch database software</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Monitor and log all database queries</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Common Attack Types */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Common SQL Injection Types</h3>
            <div className="space-y-3">
              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="font-medium text-gray-900 text-sm">Tautology Attack</p>
                <code className="text-xs text-gray-600">' OR 1=1 --</code>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="font-medium text-gray-900 text-sm">UNION-based Attack</p>
                <code className="text-xs text-gray-600">' UNION SELECT username, password FROM users --</code>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="font-medium text-gray-900 text-sm">Stacked Queries</p>
                <code className="text-xs text-gray-600">{`'; DROP TABLE users --`}</code>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <p className="font-medium text-gray-900 text-sm">Time-based Attack</p>
                <code className="text-xs text-gray-600">{`'; WAITFOR DELAY '0:0:5' --`}</code>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default QueryTester;
