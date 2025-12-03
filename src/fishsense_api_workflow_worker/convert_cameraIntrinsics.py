from fishsense_api_sdk.clients.camera_client import CameraClient
from fishsense_api_sdk.models.camera_intrinsics import CameraIntrinsics
import asyncio

async def main():
    # Initialize the CameraClient
    client = CameraClient(base_url="http://fishsense-api:8000", timeout=30)

    try:
        # Manually query the camera intrinsics endpoint
        # Replace this with the actual endpoint for camera intrinsics
        response = await client.get_intrinsics(camera_id=1)  # Use the base client's HTTP method

        # Deserialize the response into _CameraIntrinsics
        # Convert to CameraIntrinsics
        camera_intrinsics = CameraIntrinsics._from_internal(response)

        # Use the CameraIntrinsics object
        print("Camera Matrix:\n", camera_intrinsics.camera_matrix)
        print("Distortion Coefficients:\n", camera_intrinsics.distortion_coefficients)
        print("Camera ID:", camera_intrinsics.camera_id)

    except Exception as e:
        print("Error:", e)

asyncio.run(main())