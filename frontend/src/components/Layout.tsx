import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Activity, BarChart2, Bluetooth } from 'lucide-react';

export function Layout() {
  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <main className="flex-1 container mx-auto px-4 py-8 overflow-auto">
        <Outlet />
      </main>
      
      <nav className="bg-white border-t border-gray-200">
        <div className="container mx-auto px-4">
          <div className="flex justify-around py-4">
            <Link to="/" className="flex flex-col items-center text-gray-600 hover:text-blue-600">
              <Activity className="h-6 w-6" />
              <span className="text-xs mt-1">Dashboard</span>
            </Link>
            <Link to="/history" className="flex flex-col items-center text-gray-600 hover:text-blue-600">
              <BarChart2 className="h-6 w-6" />
              <span className="text-xs mt-1">History</span>
            </Link>
            <Link to="/bluetooth" className="flex flex-col items-center text-gray-600 hover:text-blue-600">
              <Bluetooth className="h-6 w-6" />
              <span className="text-xs mt-1">Devices</span>
            </Link>
          </div>
        </div>
      </nav>
    </div>
  );
}