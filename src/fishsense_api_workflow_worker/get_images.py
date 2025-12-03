from fishsense_api_sdk.clients.image_client import ImageClient
from fishsense_api_sdk.models.image import Image
import asyncio

async def main():
    # Initialize the ImageClient
    image_client = ImageClient(base_url="http://fishsense-api:8000", timeout=30)

    try:
        # Query the images endpoint

        dive_id = None  # Set to a specific ID (e.g., 1) to fetch images for that dive
        image_id = None  # Set to a specific ID (e.g., 1) to fetch a single image
        response = await image_client.get(dive_id=dive_id, image_id=image_id)  # Change to None to fetch all images

        # Handle single Image object
        if isinstance(response, Image):
            print("Image ID: ", response.id)
            print("Path: ", response.path)
            print("Taken datetime: ", response.taken_datetime)
            print("Checksum: ", response.checksum)
            print("Is canonical: ", response.is_canonical)
            print("Dive ID: ", response.dive_id)
            print("Camera ID: ", response.camera_id)

        # Handle list of Image objects
        elif isinstance(response, list):
            for image in response:
                print("Image ID: ", image.id)
                print("Path: ", image.path)
                print("Taken datetime: ", image.taken_datetime)
                print("Checksum: ", image.checksum)
                print("Is canonical: ", image.is_canonical)
                print("Dive ID: ", image.dive_id)
                print("Camera ID: ", image.camera_id)
                print("-----")

        else:
            print("Unexpected response type:", type(response))

    except Exception as e:
        print("Error:", e)

asyncio.run(main())