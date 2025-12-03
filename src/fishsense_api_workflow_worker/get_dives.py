from fishsense_api_sdk.clients.dive_client import DiveClient
from fishsense_api_sdk.models.dive import Dive
import asyncio

async def main():
    # Initialize the DiveClient
    dive_client = DiveClient(base_url="http://fishsense-api:8000", timeout=30)

    try:
        # Query the dives endpoint (change dive_id to None to fetch all dives)
        dive_id = None  # Set to a specific ID (e.g., 1) to fetch a single dive
        dives = await dive_client.get(dive_id=dive_id)

        # Handle single Dive object
        if isinstance(dives, Dive):
            print("Dive ID: ", dives.id)
            print("Name: ", dives.name)
            print("Path: ", dives.path)
            print("DateTime: ", dives.dive_datetime)
            print("Priority: ", dives.priority)
            print("Flip Dive Slate: ", dives.flip_dive_slate)
            print("Camera ID: ", dives.camera_id)
            print("Dive Slate ID: ", dives.dive_slate_id)
            print("-----")

        # Handle list of Dive objects
        elif isinstance(dives, list):
            for dive in dives:
                print("Dive ID: ", dive.id)
                print("Name: ", dive.name)
                print("Path: ", dive.path)
                print("DateTime: ", dive.dive_datetime)
                print("Priority: ", dive.priority)
                print("Flip Dive Slate: ", dive.flip_dive_slate)
                print("Camera ID: ", dive.camera_id)
                print("Dive Slate ID: ", dive.dive_slate_id)
                print("-----")

        else:
            print("Unexpected response type:", type(dives))

    except Exception as e:
        print("Error:", e)

asyncio.run(main())