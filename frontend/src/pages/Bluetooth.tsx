import React, { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { scanForDevices, type BluetoothDevice } from '../lib/bluetooth';

export function Bluetooth() {
  const [scanning, setScanning] = useState(false);
  const [devices, setDevices] = useState<BluetoothDevice[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    try {
      setScanning(true);
      setError(null);
      const foundDevices = await scanForDevices();
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
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Bluetooth Devices</h2>
          <button
            onClick={handleScan}
            disabled={scanning}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
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
          <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <div className="mt-6 space-y-4">
          {devices.map((device) => (
            <div
              key={device.id}
              className="flex items-center justify-between bg-gray-50 p-4 rounded-lg"
            >
              <div>
                <p className="font-medium">{device.name || 'Unnamed Device'}</p>
                <p className="text-sm text-gray-500">{device.id}</p>
              </div>
              <button
                className="px-3 py-1 text-sm text-blue-600 hover:text-blue-700 focus:outline-none"
              >
                Connect
              </button>
            </div>
          ))}

          {devices.length === 0 && !scanning && (
            <p className="text-center text-gray-500 py-8">
              No devices found. Click "Scan for Devices" to start searching.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}