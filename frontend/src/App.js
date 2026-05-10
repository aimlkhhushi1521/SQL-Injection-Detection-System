/**
 * Main Application Component
 * Handles routing and authentication state management
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import QueryTester from './components/QueryTester';
import LogsViewer from './components/LogsViewer';

function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing authentication on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
    
    setLoading(false);
  }, []);

  // Login handler
  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {isAuthenticated && <Navbar user={user} onLogout={handleLogout} />}
        
        <Routes>
          {/* Public routes */}
          <Route 
            path="/login" 
            element={
              isAuthenticated ? 
                <Navigate to="/dashboard" /> : 
                <Login onLogin={handleLogin} />
            } 
          />
          <Route 
            path="/register" 
            element={
              isAuthenticated ? 
                <Navigate to="/dashboard" /> : 
                <Register />
            } 
          />
          
          {/* Protected routes */}
          <Route 
            path="/dashboard" 
            element={
              isAuthenticated ? 
                <Dashboard user={user} /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/test" 
            element={
              isAuthenticated ? 
                <QueryTester user={user} /> : 
                <Navigate to="/login" />
            } 
          />
          <Route 
            path="/logs" 
            element={
              isAuthenticated ? 
                <LogsViewer user={user} /> : 
                <Navigate to="/login" />
            } 
          />
          
          {/* Default redirect */}
          <Route 
            path="/" 
            element={
              isAuthenticated ? 
                <Navigate to="/dashboard" /> : 
                <Navigate to="/login" />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
