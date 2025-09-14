#!/bin/sh

echo 'Start MinIO init'
until mc alias set minio "$AWS_S3_ENDPOINT_URL" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY"; do
  echo 'Waiting for MinIO to be ready...'
  sleep 2
done

mc mb minio/"$AWS_STORAGE_BUCKET_NAME" --ignore-existing || echo 'Bucket may already exist'

for folder in test doctors patients clinic; do
  echo -n "" | mc pipe minio/"$AWS_STORAGE_BUCKET_NAME"/"$folder"/.keep || echo "Folder $folder setup failed"
  mc anonymous set download minio/"$AWS_STORAGE_BUCKET_NAME"/"$folder"/ || echo "Folder $folder policy setup failed"
done

echo "Bucket $AWS_STORAGE_BUCKET_NAME and folders test, doctors, patients, clinic initialized"