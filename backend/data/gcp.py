import os
from django.conf import settings
from google.cloud import storage

project_id = 'managy-438606'
cloud_storage_key = os.path.join(settings.BASE_DIR, 'cloudstoragekey.json')
bucket_name = 'managy_bucket'

# uploadToGCP(`${testupload}`, 'admin_excel/', 'testbatchcreation.xlsx', 1)
def upload_to_gcp(filepath, storage_folder, file_name, public_access):
    # Set access control based on public_access parameter
    access = 'publicRead' if public_access == 1 else 'private'

    # Initialize a storage client
    client = storage.Client.from_service_account_json(cloud_storage_key, project=project_id)

    try:
        # Get the bucket
        bucket = client.bucket(bucket_name)

        # Construct the destination path
        storage_path = f"{storage_folder}/{file_name}"

        # Upload the file
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(filepath, content_type='application/plain')

        # Set the predefined ACL
        if public_access == 1:
            blob.make_public()  # Make the file publicly accessible

        # Return the media link
        return blob.public_url if public_access == 1 else None

    except Exception as error:
        print(error)
        raise Exception(f"An error occurred: {error}")
