export interface BluetoothDevice {
  id: string;
  name: string | null;
}

export const checkBluetoothAvailability = (): { available: boolean; error?: string } => {
  if (!navigator.bluetooth) {
    return {
      available: false,
      error: "Bluetooth is not supported in this browser. Please use a modern browser that supports Web Bluetooth API."
    };
  }

  return { available: true };
};

export const scanForDevices = async (): Promise<BluetoothDevice[]> => {
  const availabilityCheck = checkBluetoothAvailability();
  if (!availabilityCheck.available) {
    throw new Error(availabilityCheck.error);
  }

  try {
    const device = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: ['heart_rate', 'battery_service']
    });

    return [{
      id: device.id,
      name: device.name
    }];
  } catch (error) {
    if (error instanceof Error) {
      // Handle specific Bluetooth errors
      if (error.message.includes('User cancelled')) {
        throw new Error('Bluetooth scan was cancelled. Please try again.');
      } else if (error.message.includes('globally disabled')) {
        throw new Error('Bluetooth is disabled in your browser settings. Please enable it and try again.');
      } else if (error.message.includes('adapter not available')) {
        throw new Error('No Bluetooth adapter found. Please check if your device supports Bluetooth.');
      }
    }
    throw error;
  }
};