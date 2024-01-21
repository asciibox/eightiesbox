gsutil iam ch allUsers:objectViewer gs://[YOUR-BUCKET-NAME]
gsutil cors set cors-config.json gs://[YOUR-BUCKET-NAME]
gsutil cors get gs://[YOUR-BUCKET-NAME]



from google.cloud import storage
import os
import uuid
from datetime import datetime
import re
import mimetypes

def processUploadedFile(data, context):
    """
    Triggered by a change to a Cloud Storage object in the 'incoming' bucket.
    Args:
         data (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file_path = data['name']  # Full path including directories and file
    
    # Determine if the file is a part of the timeline
    is_timeline = file_path.startswith("timeline/")

    incoming_bucket_name = data['bucket']

    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    incoming_bucket = storage_client.bucket(incoming_bucket_name)
    blob = incoming_bucket.blob(file_path)

    # Define the "processed" bucket
    processed_bucket_name = "eightiesbox_uploaded"
    processed_bucket = storage_client.bucket(processed_bucket_name)

    # Get today's date in the format DD-MM-YYYY
    today = datetime.today().strftime('%d-%m-%Y')

    # Check if there's a directory for the current day in the "processed" bucket
    daily_directory = None
    blobs = processed_bucket.list_blobs(prefix=today)
    for b in blobs:
        if b.name.startswith(today) and '/' in b.name:
            daily_directory = b.name.split('/')[0]
            break

    # If no directory for today was found, create one with a new UUID
    if not daily_directory:
        daily_uuid = str(uuid.uuid4())
        daily_directory = f"{today}_{daily_uuid}"

    # Define the pattern for the timestamp in the filename
    timestamp_pattern = re.compile(r'_(\d{13})(?=\.)') 

    # Extract the base directory name and the original filename
    base_directory_name = os.path.dirname(file_path).split('/')[-1]
    original_filename = os.path.basename(file_path)

    
    
    # Search for the timestamp in the original filename
    timestamp_match = timestamp_pattern.search(original_filename)
    if timestamp_match:
        # Extract the timestamp
        timestamp = timestamp_match.group(0)
        timestamp = timestamp[1:]
        # Remove the timestamp from the original filename
        clean_filename = timestamp_pattern.sub('', original_filename)

        # New regex pattern to extract the category string
        category_pattern = re.compile(r'^[a-fA-F0-9]{24}-(.{20})')
        category_match = category_pattern.search(clean_filename)

        # Initialize an empty category string
        category_string = 'default_no_category'

        if category_match:
            # Extract the category string
            category_string = category_match.group(1)
            # Remove the category string from the clean_filename
            clean_filename = category_pattern.sub('', clean_filename)
            clean_filename = clean_filename[1:]
        else:
            print(f"Category not found in {clean_filename}")

        # Extract the file extension
        file_extension = os.path.splitext(clean_filename)[1]  # This will give you '.png' from your example

        # Ensure we only get the first 20 characters of the filename without the extension
        filename_prefix = os.path.splitext(clean_filename[:20])[0]

        print(f"File path: {file_path}, Is Timeline: {is_timeline}")  # Debug log

        if is_timeline:
            # Split the file_path to extract the user_id_str and original_filename
            parts = file_path.split('/')
            # Ensure that there are enough parts in the path
            if len(parts) >= 3:
                user_id_str = parts[1]
                original_filename = parts[-1]  # Get the last part as the filename

                # Constructing the new file path
                new_file_path = f"timeline/{user_id_str}/{original_filename}"
                print(f"New file path for timeline: {new_file_path}, User ID: {user_id_str}")  # Debug log
            else:
                print("Error: file_path does not contain enough parts to extract user_id_str and original_filename")
        else:
            # Construct the new file path
            new_file_path = f"{daily_directory}/{category_string}/{base_directory_name}/{timestamp}_{filename_prefix}{file_extension}/{clean_filename}"
            
    else:
        # If no timestamp is found, we keep the original structure
        print("No timestamp found, keeping old structure")
        new_file_path = f"{daily_directory}/{base_directory_name}/{original_filename}"


    new_blob = processed_bucket.copy_blob(blob, processed_bucket, new_file_path)

    # Check if the copy was successful before deleting
    if new_blob:
        print("NEW BLOCK == True")
        if is_timeline:
            print("IS_TIMELINE == TRUE")
            new_blob = processed_bucket.blob(new_file_path)
            new_blob.metadata = {'Content-Disposition': 'inline'}
            mime_type, _ = mimetypes.guess_type(new_file_path)
            new_blob.content_type = mime_type if mime_type else 'application/octet-stream'
            new_blob.patch()
        else:
            print("IS_TIMELINE == FALSE")
        # Delete the original file from the "incoming" bucket
        blob.delete()
        print(f"File {file_path} processed and moved to {new_file_path} in the 'processed' bucket.")
    else:
        print(f"Failed to copy {file_path} to {new_file_path}.")
