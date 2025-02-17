export interface BluetoothDevice {
  id: string;
  name: string | null;
}

export const scanForDevices = async (): Promise<BluetoothDevice[]> => {
  try {
    const devices: BluetoothDevice[] = [];
    
    if (!navigator.bluetooth) {
      throw new Error('Bluetooth not supported');
    }

    const device = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
    });

    if (device) {
      devices.push({
        id: device.id,
        name: device.name,
      });
    }

    return devices;
  } catch (error) {
    console.error('Bluetooth scan error:', error);
    throw error;
  }
};