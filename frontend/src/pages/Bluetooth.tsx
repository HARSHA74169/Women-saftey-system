import React, { useState, useCallback } from 'react';
import { Loader2, AlertCircle, Watch } from 'lucide-react';

interface SmartWatchDevice {
  id: string;
  name: string;
  rssi: number;
  discoveredAt?: number;
}

export function Bluetooth() {
  const [scanning, setScanning] = useState(false);
  const [connecting, setConnecting] = useState<string | null>(null);
  const [devices, setDevices] = useState<SmartWatchDevice[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [connectedDevice, setConnectedDevice] = useState<SmartWatchDevice | null>(null);

  const handleScan = useCallback(async () => {
    try {
      setScanning(true);
      setError(null);

      const response = await fetch('http://localhost:5000/scan');
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to scan devices');
      }

      const foundDevices = await response.json();
      setDevices(foundDevices);

      if (foundDevices.length === 0) {
        setError('No smartwatches found nearby. Please ensure devices are in range and discoverable.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to scan for smartwatches');
      setDevices([]);
    } finally {
      setScanning(false);
    }
  }, []);

  const handleConnect = useCallback(async (device: SmartWatchDevice) => {
    try {
      setConnecting(device.id);
      setError(null);

      const response = await fetch(`http://localhost:5000/connect/${device.id}`, {
        method: 'POST',
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to connect to device');
      }

      setConnectedDevice(device);
      // Keep other devices visible but disable their connect buttons
      setDevices(prevDevices =>
        prevDevices.map(d => ({
          ...d,
          disabled: d.id !== device.id
        }))
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to device');
    } finally {
      setConnecting(null);
    }
  }, []);

  const getRssiStrength = (rssi: number) => {
    if (rssi >= -60) return 'Excellent';
    if (rssi >= -70) return 'Good';
    if (rssi >= -80) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="space-y-6">
      {/* Rest of your existing JSX remains the same */}
      {/* Update the device list rendering to include signal strength */}
      <div className="space-y-4">
        {devices.map((device) => (
          <div
            key={device.id}
            className="flex items-center justify-between bg-gray-50 p-4 rounded-lg border border-gray-200"
          >
            <div>
              <p className="font-medium text-gray-900">{device.name || 'Unnamed Watch'}</p>
              <p className="text-sm text-gray-500 mt-1">
                Signal Strength: {getRssiStrength(device.rssi)} ({device.rssi} dBm)
              </p>
              <p className="text-sm text-gray-500">{device.id}</p>
            </div>
            <button
              onClick={() => handleConnect(device)}
              disabled={connecting === device.id || (!!connectedDevice && connectedDevice.id !== device.id)}
              className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 hover:text-blue-700 focus:outline-none focus:underline disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {connecting === device.id ? (
                <>
                  <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" />
                  Connecting...
                </>
              ) : connectedDevice?.id === device.id ? (
                <span className="text-green-600">Connected</span>
              ) : (
                'Connect'
              )}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}