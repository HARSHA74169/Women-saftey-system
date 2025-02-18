import asyncio
import logging
from typing import List, Optional
from bleak import BleakScanner, BleakError

class BLEDeviceScanner:
    def __init__(self, scan_time: float = 5.0, max_retries: int = 3):
        """
        Initialize the BLE scanner.
        
        Args:
            scan_time: Duration of each scan in seconds.
            max_retries: Maximum number of scan retries if no devices are found.
        """
        self.scan_time = scan_time
        self.max_retries = max_retries
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.devices = {}

    def _device_found_callback(self, device, advertisement_data):
        """Callback function triggered when a device is found during scanning."""
        self.devices[device.address] = {
            "name": device.name or "Unknown",
            "address": device.address,
            "rssi": advertisement_data.rssi,
        }

    async def scan_devices(self, name_filter: Optional[str] = None) -> List[dict]:
        """
        Scan for BLE devices with retries.
        
        Args:
            name_filter: Optional string to filter devices by name.
        
        Returns:
            List of discovered BLE devices.
        """
        retry_count = 0

        while retry_count < self.max_retries:
            try:
                self.logger.info(f"Starting BLE scan (Attempt {retry_count + 1}/{self.max_retries})")

                # Reset the list of found devices
                self.devices = {}

                # Initialize scanner and register callback
                scanner = BleakScanner(detection_callback=self._device_found_callback)

                # Start scanning
                await scanner.start()
                await asyncio.sleep(self.scan_time)
                await scanner.stop()

                # Get discovered devices
                devices_list = list(self.devices.values())

                # Filter devices by name if a filter is provided
                if name_filter:
                    devices_list = [device for device in devices_list if name_filter.lower() in device["name"].lower()]

                if devices_list:
                    self.logger.info(f"✅ Found {len(devices_list)} device(s)")
                    return devices_list
                
                self.logger.warning("⚠️ No devices found, retrying...")
                retry_count += 1
                await asyncio.sleep(2)  # Wait before retrying
                    
            except BleakError as e:
                self.logger.error(f"🔴 BLE scanning error: {e}")
                retry_count += 1
                await asyncio.sleep(2)
            except Exception as e:
                self.logger.error(f"🚨 Unexpected error: {e}")
                retry_count += 1
                await asyncio.sleep(2)

        return []  # Return empty list if no devices were found

async def main():
    scanner = BLEDeviceScanner(scan_time=10.0, max_retries=3)
    
    try:
        # Scan for all devices
        devices = await scanner.scan_devices()
        
        print("\n🔍 Discovered Devices:")
        print("-" * 50)
        if devices:
            for device in devices:
                print(f"📡 Name: {device['name']}")
                print(f"🔗 Address: {device['address']}")
                print(f"📶 RSSI: {device['rssi']} dBm")
                print("-" * 50)
        else:
            print("❌ No devices found. Ensure Bluetooth is enabled.")
            
    except Exception as e:
        print(f"🚨 An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
