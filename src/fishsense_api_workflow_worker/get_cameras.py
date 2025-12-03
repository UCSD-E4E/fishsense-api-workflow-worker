from fishsense_api_sdk.clients.camera_client import CameraClient
from fishsense_api_sdk.models.camera import Camera
import asyncio

async def main():
    # Initialize the CameraClient
    camera_client = CameraClient(base_url="http://fishsense-api:8000", timeout=30)

    try:
        # Query the cameras endpoint (change camera_id to None to fetch all cameras)
        camera_id = None  # Set to a specific ID (e.g., 1) to fetch a single camera
        cameras = await camera_client.get(camera_id=camera_id)

        # Handle single Camera object
        if isinstance(cameras, Camera):
            print("Camera ID: ", cameras.id)
            print("Serial number: ", cameras.serial_number)
            print("Name: ", cameras.name)
            print("-----")

        # Handle list of Camera objects
        elif isinstance(cameras, list):
            for camera in cameras:
                print("Camera ID: ", camera.id)
                print("Serial number: ", camera.serial_number)
                print("Name: ", camera.name)
                print("-----")

        else:
            print("Unexpected response type:", type(cameras))

    except Exception as e:
        print("Error:", e)

asyncio.run(main())