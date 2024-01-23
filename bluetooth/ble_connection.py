import asyncio
from bleak import BleakClient


async def discover_characteristics(device_name_or_address, service_uuid):
    client = BleakClient(device_name_or_address)
    try:
        await client.connect()
        print(f"Connected to {device_name_or_address}")

        # Discover services and their characteristics
        services = await client.get_services()
        for service in services:
            if service.uuid == service_uuid:
                print(f"Service found: {service}")
                characteristics = service.characteristics
                print(f"Characteristics for Service {service_uuid}:")
                for characteristic in characteristics:
                    print(characteristic)
                break
        else:
            print(f"Service {service_uuid} not found on {device_name_or_address}")

    except Exception as e:
        print(f"Failed to connect to {device_name_or_address}: {e}")
    finally:
        await client.disconnect()


async def main():
    device_name_or_address = "Your_Device_Name_Or_Address"  # Replace with the name or address of the device you want
    # to connect to
    service_uuid = "0000180F-0000-1000-8000-00805F9B34FB"  # Replace with the UUID of the service you want to explore
    print(f"Scanning characteristics for Service {service_uuid} on {device_name_or_address}...")
    await discover_characteristics(device_name_or_address, service_uuid)


# Run the main function to start discovering characteristics for the specified service of the device
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

"""
NeuroState-AB0B - Address: E8:EB:1B:51:AB:0B

00001800-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Access Profile
0000180a-0000-1000-8000-00805f9b34fb (Handle: 16): Device Information
49535343-fe7d-4ae5-8fa9-9fafd205e455 (Handle: 48): Unknown

readC = list?.firstWhere((element) =>
          element.uuid.toString() == "49535343-1e4d-4bd9-ba61-23c647249616");
      writeC = list?.firstWhere((element) =>
          element.uuid.toString() == "49535343-8841-43f4-a8d4-ecbe34729bb3")

"""
