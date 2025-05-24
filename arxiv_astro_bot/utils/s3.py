import boto3

def resolve_s3_path(version):
    bot_name = version.split("_")[0]
    return f"lyricbots/{bot_name}/{version}/tf_model.h5"

def download_model_from_s3(bucket, subpath, local_path="tf_model.h5"):
    s3_key = f"{subpath}/tf_model.h5"
    print(f"Downloading s3://{bucket}/{s3_key} to {local_path}")
    s3.download_file(bucket, s3_key, local_path)
    return local_path
