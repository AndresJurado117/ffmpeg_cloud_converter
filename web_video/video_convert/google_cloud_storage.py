from google.cloud import storage
import os
from datetime import datetime, timedelta

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-storage.json"


# define function that creates the bucket
def create_bucket(bucket_name, storage_class="STANDARD", location="us-central1"):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = storage_class

    bucket = storage_client.create_bucket(bucket, location=location)
    # for dual-location buckets add data_locations=[region_1, region_2]

    return f"Bucket {bucket.name} successfully created."


# define function that uploads a file from the bucket
def upload_cs_file(bucket_name, source_file_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    return True


# define function that downloads a file from the bucket
def download_cs_file(bucket_name, file_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True


# define function that list files in the bucket
def list_cs_files(bucket_name):
    storage_client = storage.Client()

    file_list = storage_client.list_blobs(bucket_name)
    file_list = [file.name for file in file_list]

    return file_list


# define function that generates the public URL, default expiration is set to 24 hours
def get_cs_file_url(bucket_name, file_name, expire_in=datetime.today() + timedelta(1)):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url


# Source: https://medium.com/google-cloud/automating-google-cloud-storage-management-with-python-92ba64ec8ea8
