import React from 'react';
import { Brain, AlertTriangle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { getLatestEmotions } from '../lib/db';



// export async function getLatestAlerts() {
async function getLatestAlerts() {
  const response = await fetch('http://localhost:5000/api/alerts'); // Updated URL
  if (!response.ok) {
    throw new Error('Failed to fetch alerts');
  }
  return response.json();
}

export function Dashboard() {
  const { data: emotions } = useQuery({
    queryKey: ['emotions'],
    queryFn: getLatestEmotions,
  });

  const { data: alerts } = useQuery({
    queryKey: ['alerts'],
    queryFn: getLatestAlerts,
  });

  const latestEmotion = emotions?.[0];


  return (
    <div className="space-y-6 p-6 bg-gray-100 min-h-screen">
      {/* Current State Section */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-800">Current State</h2>
          <Brain className="h-6 w-6 text-blue-500" />
        </div>

        {latestEmotion ? (
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">Emotion</p>
              <p className="text-lg font-medium text-blue-700">{latestEmotion.emotion}</p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">Steps</p>
              <p className="text-lg font-medium text-green-700">{latestEmotion.steps}</p>
            </div>
          </div>
        ) : (
          <p className="mt-4 text-sm text-gray-500">No emotion data available.</p>
        )}
      </div>

      {/* Recent Alerts Section */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-800">Recent Alerts</h2>
          <AlertTriangle className="h-6 w-6 text-yellow-500" />
        </div>

        <div className="mt-4 space-y-4">
          {alerts?.length > 0 ? (
            alerts.slice(0, 3).map((alert) => (
              <div key={alert.id} className="bg-red-50 p-4 rounded-lg flex justify-between items-start">
                <div>
                  <p className="font-medium text-red-700">{alert.message}</p>
                  <p className="text-xs text-gray-500">{new Date(alert.timestamp).toLocaleString()}</p>
                </div>
                <span className={`text-xs font-semibold px-2 py-1 rounded-md ${alert.status === 'Sent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}>
                  {alert.status}
                </span>
              </div>
            ))
          ) : (
            <p className="text-sm text-gray-500">No alerts found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
