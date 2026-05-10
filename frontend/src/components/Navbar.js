/**
 * Navigation Bar Component
 * Displays app navigation with user info and logout
 */

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-lg border-b-2 border-primary-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Navigation Links */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link to="/dashboard" className="flex items-center">
                <svg
                  className="h-8 w-8 text-primary-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </Link>
            </div>
            <div className="hidden md:block ml-10">
              <div className="flex items-baseline space-x-4">
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  to="/test"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Test Query
                </Link>
                {user?.role === 'admin' && (
                  <Link
                    to="/logs"
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    Logs
                  </Link>
                )}
              </div>
            </div>
          </div>

          {/* User Info and Logout */}
          <div className="flex items-center space-x-4">
            <div className="text-sm">
              <div className="text-gray-700 font-medium">{user?.username}</div>
              <div className="text-gray-500 text-xs capitalize">{user?.role}</div>
            </div>
            <button
              onClick={handleLogout}
              className="bg-danger-600 hover:bg-danger-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
