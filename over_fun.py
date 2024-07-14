from botocore.exceptions import ClientError
import boto3
from boto3.dynamodb.conditions import Attr
import random,secrets,string
from random import choices
session = boto3.session.Session(profile_name='Ankit')
def generate_presigned_url(bucket_name, object_key, expiration_time):
    s3_client = boto3.client('s3')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_time
        )
        return presigned_url
    except ClientError as e:
        print("Error generating pre-signed URL:", e)
        return None
def item_picker(items, quantities, num_to_pick):
    return choices(items, weights=quantities, k=num_to_pick)
def item_picker_avoider(items, quantities, num_to_pick, elements_to_avoid):
    filtered_items = [item for item in items if item not in elements_to_avoid]
    filtered_quantities = [quantities[idx] for idx, item in enumerate(items) if item not in elements_to_avoid]
    if not filtered_items:
        return []
    chosen_items = choices(filtered_items, weights=filtered_quantities, k=num_to_pick)
    return chosen_items
def generate_secret_code(length=12):
    alphabet = string.ascii_letters + string.digits  # You can include more characters if needed
    secret_code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_code
def list_folders_in_bucket(bucket_name, prefix=''):
    s3 = session.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    folders = []
    if 'CommonPrefixes' in response:
        for folder in response['CommonPrefixes']:
            folder_name = folder['Prefix'].rstrip('/').split('/')[-1]  # Extract last part of folder path
            folders.append(folder_name)

    return folders
def list_objects_in_bucket(bucket_name, prefix=''):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    objects = []
    if 'Contents' in response:
        for obj in response['Contents']:
            object_name = obj['Key'].split('/')[-1]
            objects.append(object_name)

    return objects