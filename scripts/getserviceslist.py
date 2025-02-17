import asyncio
from bleak import BleakClient

# # Replace with your smartwatch's MAC address
# MAC_ADDRESS_FIRE_BOLTT = "F9:BA:ED:5F:3D:19"
# MAC_ADDRESS_NOISE = "D6:3A:0C:20:1B:6A"
# MAC_ADDRESS_FASTRACK = "F4:61:A8:0F:1D:05"
# MAC_ADDRESS_NINJA = "F7:63:6A:6C:12:35"
MAC_ADDRESS_NINJA_WHITE = "FB:D8:57:5B:04:32"


async def list_services(MAC_ADDRESS):
    """
    Connect to the smartwatch and list all services and characteristics.
    """
    async with BleakClient(MAC_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        print(f"Mac Address : {MAC_ADDRESS}")

        for service in client.services:
            
            print(f"  [Service] {service.uuid}")
            print()

            for characteristic in service.characteristics:
                properties = characteristic.properties
                print(f"  [Characteristic] {characteristic.uuid} - {properties}")
                
            print()
            print('-' * 80)

# Entry point
if __name__ == "__main__":
    asyncio.run(list_services(MAC_ADDRESS_NINJA_WHITE))
