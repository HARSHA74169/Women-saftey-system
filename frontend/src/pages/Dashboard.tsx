import React from 'react';
import { Brain, AlertTriangle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { getLatestEmotions, getLatestAlerts } from '../lib/db';

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
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Current State</h2>
          <Brain className="h-6 w-6 text-blue-500" />
        </div>
        
        {latestEmotion && (
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-500">Emotion</p>
              <p className="text-lg font-medium">{latestEmotion.emotion}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-500">Steps</p>
              <p className="text-lg font-medium">{latestEmotion.steps}</p>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Recent Alerts</h2>
          <AlertTriangle className="h-6 w-6 text-yellow-500" />
        </div>
        
        <div className="mt-4 space-y-4">
          {alerts?.slice(0, 3).map((alert) => (
            <div key={alert.id} className="bg-gray-50 p-4 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-medium">{alert.type}</p>
                  <p className="text-sm text-gray-500">{alert.message}</p>
                </div>
                <span className="text-xs text-gray-400">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}