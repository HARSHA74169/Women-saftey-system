import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import * as XLSX from 'xlsx';

// Function to fetch sensor data from the Flask API
async function getSensorData() {
  const response = await fetch('http://localhost:5000/history'); // Update with your backend URL
  if (!response.ok) {
    throw new Error('Failed to fetch sensor data');
  }
  return response.json();
}

export function History() {
  const { data: sensorData, error, isLoading } = useQuery({
    queryKey: ['sensorData'],
    queryFn: getSensorData,
  });

  const [filters, setFilters] = useState({
    startTime: '',
    endTime: '',
    minHeartRate: '',
    maxHeartRate: '',
  });

  const [exportFormat, setExportFormat] = useState('xlsx');

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const filteredData = sensorData?.filter((entry: any) => {
    const entryTime = new Date(entry.timestamp).getTime();
    const startTime = filters.startTime ? new Date(filters.startTime).getTime() : null;
    const endTime = filters.endTime ? new Date(filters.endTime).getTime() : null;
    const minHeartRate = filters.minHeartRate ? parseInt(filters.minHeartRate, 10) : null;
    const maxHeartRate = filters.maxHeartRate ? parseInt(filters.maxHeartRate, 10) : null;

    return (
      (!startTime || entryTime >= startTime) &&
      (!endTime || entryTime <= endTime) &&
      (!minHeartRate || entry.heart_rate >= minHeartRate) &&
      (!maxHeartRate || entry.heart_rate <= maxHeartRate)
    );
  });

  const exportData = () => {
    if (!filteredData?.length) return;

    const formattedData = filteredData.map(entry => ({
      Time: new Date(entry.timestamp).toLocaleString(),
      'Heart Rate': entry.heart_rate,
      Steps: entry.step_count ?? 'N/A',
      'Battery Level': entry.battery_level ?? 'N/A',
      'Device ID': entry.device_id ?? 'N/A'
    }));

    if (exportFormat === 'xlsx') {
      // Export as Excel
      const worksheet = XLSX.utils.json_to_sheet(formattedData);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, "Sensor Data");
      XLSX.writeFile(workbook, `sensor_data_${new Date().toISOString().split('T')[0]}.xlsx`);
    } else {
      // Export as CSV
      const headers = ['Time', 'Heart Rate', 'Steps', 'Battery Level', 'Device ID'];
      const csvData = formattedData.map(row =>
        headers.map(header => row[header as keyof typeof row]).join(',')
      );

      const csvContent = [
        headers.join(','),
        ...csvData
      ].join('\n');

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `sensor_data_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading sensor data</p>;

  return (
    <>
      <div className="bg-white rounded-xl shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Sensor History</h2>
          <div className="mt-4">
            <label>
              Start Time:
              <input
                type="datetime-local"
                name="startTime"
                value={filters.startTime}
                onChange={handleFilterChange}
                className="ml-2 p-1 border rounded"
              />
            </label>
            <label className="ml-4">
              End Time:
              <input
                type="datetime-local"
                name="endTime"
                value={filters.endTime}
                onChange={handleFilterChange}
                className="ml-2 p-1 border rounded"
              />
            </label>
            <label className="ml-4">
              Min Heart Rate:
              <input
                type="number"
                name="minHeartRate"
                value={filters.minHeartRate}
                onChange={handleFilterChange}
                className="ml-2 p-1 border rounded"
              />
            </label>
            <label className="ml-4">
              Max Heart Rate:
              <input
                type="number"
                name="maxHeartRate"
                value={filters.maxHeartRate}
                onChange={handleFilterChange}
                className="ml-2 p-1 border rounded"
              />
            </label>
          </div>
          <div className="mt-4 flex items-center gap-2">
            <select
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value)}
              className="p-2 border rounded"
            >
              <option value="xlsx">Excel (.xlsx)</option>
              <option value="csv">CSV (.csv)</option>
            </select>
            <button
              onClick={exportData}
              disabled={!filteredData?.length}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
            >
              Export Data
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Heart Rate</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Steps</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Emotion</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Battery Level</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device ID</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredData?.map((entry: any) => (
                <tr key={entry.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(entry.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {entry.heart_rate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {entry.step_count ?? 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {entry.emotion ?? 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {entry.battery_level ?? 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {entry.device_id ?? 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
    </>
  );
}