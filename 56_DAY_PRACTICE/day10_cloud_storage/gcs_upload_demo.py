"""
Step 5: Upload file to Google Cloud Storage
Run: python3 gcs_upload_demo.py
"""

from google.cloud import storage
import os

# Configuration
PROJECT_ID = "e2e-etl-project"
BUCKET_NAME = "krishna-genai-storage-1234"
FILE_TO_UPLOAD = os.path.join(os.path.dirname(__file__), "vertex_ai_demo.py")
DESTINATION_BLOB_NAME = "uploaded_demo.py"

def upload_to_gcs():
    print(f"Uploading: {FILE_TO_UPLOAD}")

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(DESTINATION_BLOB_NAME)
    blob.upload_from_filename(FILE_TO_UPLOAD)

    print(f"✅ Uploaded to gs://{BUCKET_NAME}/{DESTINATION_BLOB_NAME}")

if __name__ == "__main__":
    upload_to_gcs()
