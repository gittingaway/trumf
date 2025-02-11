import json
import os
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image
from supabase import create_client

load_dotenv()

SUPABASE_API_URL = os.getenv("SUPABASE_API_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = "logos"

if not SUPABASE_API_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError(
        "Please set the SUPABASE_API_URL and SUPABASE_SERVICE_ROLE_KEY environment variables."
    )

supabase = create_client(SUPABASE_API_URL, SUPABASE_SERVICE_ROLE_KEY)


def load_dummy_data():
    with open("./dummy_data.json", "r") as file:
        data = json.load(file).get("merchants")
    return data


def download_image(url):
    """
    Downloads an image from a given URL and saves it to the specified path.

    :param url: str - The URL of the image to download.
    :param save_path: str - The local file path to save the image.
    """
    remove_domain = url.split("/")[-1]
    save_path = "./images/" + remove_domain
    save_path = save_path.replace("png", "webp")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        image = Image.open(BytesIO(response.content))

        image.save(save_path, "WEBP", quality=100)

        print(f"Image downloaded successfully: {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")


def upload_image(file_path):
    """
    Uploads an image to a Supabase storage bucket.

    :param file_path: str - The local file path of the image to upload.
    """
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, "rb") as file:
            response = supabase.storage.from_(BUCKET_NAME).upload(
                file=file,
                path=file_name,
                file_options={"CacheControl": "3600", "upsert": "true"},
            )
        print(f"Image uploaded successfully")
        return file_name
    except Exception as e:
        print(f"Error uploading image: {e}")
        raise e


def get_image_url(file_name):
    return supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)


# Example usage


def main():
    data = load_dummy_data()
    path = download_image(data[0].get("image_url"))
    file_name = upload_image(path)
    public_url = get_image_url(file_name)
    print(public_url)
    # for merchant in data:
    #    download_image(merchant.get("image_url"))


if __name__ == "__main__":
    main()
