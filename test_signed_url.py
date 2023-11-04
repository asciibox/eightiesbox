from google.cloud import storage
import datetime

def generate_signed_url(bucket_name, blob_name, download_as_filename):
    """Generates a signed URL for a blob."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Replace slashes with underscores in the filename
    safe_filename = download_as_filename.replace('/', '_')

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),  # URL valid for 15 minutes
        method="GET",
        response_disposition=f'attachment; filename="{safe_filename}"',  # Set the content disposition
    )

    return url

# Usage
bucket_name = "eightiesbox_uploaded"
blob_name = "04-11-2023_97abd50f-a301-4eca-925d-92ec1ab13052/6532e74cc68b1f0e982b69e3/1699098793714_DALL·E 2023-04-22 00.png/DALL·E 2023-04-22 00.22.56.png"
desired_download_filename = "DALLE_2023-04-22.png"
url = generate_signed_url(bucket_name, blob_name, desired_download_filename)
print("Generated signed URL:", url)