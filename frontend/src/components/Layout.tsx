import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { Activity, BarChart2, Bluetooth } from 'lucide-react';
import { cn } from '../lib/utils';

export function Layout() {
  const location = useLocation();

  const getPageTitle = (pathname: string) => {
    switch (pathname) {
      case '/':
        return 'Dashboard';
      case '/history':
        return 'History';
      case '/bluetooth':
        return 'Bluetooth Devices';
      default:
        return 'Smartwatch Emotion Tracker';
    }
  };

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">{getPageTitle(location.pathname)}</h1>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 py-8 overflow-auto">
        <Outlet />
      </main>

      <nav className="bg-white border-t border-gray-200">
        <div className="container mx-auto px-4">
          <div className="flex justify-around py-4">
            <Link
              to="/"
              className={cn(
                "flex flex-col items-center transition-colors",
                isActive('/')
                  ? "text-blue-600"
                  : "text-gray-600 hover:text-blue-600"
              )}
            >
              <Activity className="h-6 w-6" />
              <span className="text-xs mt-1">Dashboard</span>
            </Link>
            <Link
              to="/history"
              className={cn(
                "flex flex-col items-center transition-colors",
                isActive('/history')
                  ? "text-blue-600"
                  : "text-gray-600 hover:text-blue-600"
              )}
            >
              <BarChart2 className="h-6 w-6" />
              <span className="text-xs mt-1">History</span>
            </Link>
            <Link
              to="/scan"
              className={cn(
                "flex flex-col items-center transition-colors",
                isActive('/bluetooth')
                  ? "text-blue-600"
                  : "text-gray-600 hover:text-blue-600"
              )}
            >
              <Bluetooth className="h-6 w-6" />
              <span className="text-xs mt-1">Devices</span>
            </Link>
          </div>
        </div>
      </nav>
    </div>
  );
}