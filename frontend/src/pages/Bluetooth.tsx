import React, { useState } from 'react';
import { Loader2, Bluetooth as BluetoothIcon, AlertCircle } from 'lucide-react';
import { scanForDevices, checkBluetoothAvailability, type BluetoothDevice } from '../lib/bluetooth';

export function Bluetooth() {
  const [scanning, setScanning] = useState(false);
  const [devices, setDevices] = useState<BluetoothDevice[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    try {
      setScanning(true);
      setError(null);

      const response = await fetch('http://localhost:5000/scan'); // Fetch from Flask API
      if (!response.ok) throw new Error('Failed to scan devices');

      const foundDevices = await response.json();
      setDevices(foundDevices);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to scan for devices');
    } finally {
      setScanning(false);
    }
  };


  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <BluetoothIcon className="h-6 w-6 text-blue-500" />
            <h2 className="text-xl font-semibold">Bluetooth Devices</h2>
          </div>
          <button
            onClick={handleScan}
            disabled={scanning}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {scanning ? (
              <>
                <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" />
                Scanning...
              </>
            ) : (
              'Scan for Devices'
            )}
          </button>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-400 mt-0.5" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-4">
          {devices.map((device) => (
            <div
              key={device.id}
              className="flex items-center justify-between bg-gray-50 p-4 rounded-lg border border-gray-200"
            >
              <div>
                <p className="font-medium text-gray-900">{device.name || 'Unnamed Device'}</p>
                <p className="text-sm text-gray-500 mt-1">{device.id}</p>
              </div>
              <button
                className="px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 focus:outline-none focus:underline"
              >
                Connect
              </button>
            </div>
          ))}

          {devices.length === 0 && !scanning && !error && (
            <div className="text-center py-8">
              <BluetoothIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-500">
                No devices found. Click "Scan for Devices" to start searching.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}