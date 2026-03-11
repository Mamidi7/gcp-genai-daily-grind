import os
from google.cloud import storage

# 1. Wear the Service Account Mask
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sa-key.json"

# 2. Connect to the Bucket
client = storage.Client()
bucket_name = "krishna-genai-storage-1234" # Your exact bucket name
bucket = client.bucket(bucket_name)

# 3. Create a new file in the cloud
blob = bucket.blob("hello_from_mac.txt")
blob.upload_from_string("Namaskaram GCP! Krishna is here.")

print(f"File uploaded successfully to {bucket_name}!")