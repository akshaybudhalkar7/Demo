import boto3
import pandas as pd
import io

def compare_excels(bucket_name, file1_key, file2_key):
    s3 = boto3.client('s3')

    # Load the first Excel file from S3
    file1_obj = s3.get_object(Bucket=bucket_name, Key=file1_key)
    file1_df = pd.read_excel(io.BytesIO(file1_obj['Body'].read()))

    # Load the second Excel file from S3
    file2_obj = s3.get_object(Bucket=bucket_name, Key=file2_key)
    file2_df = pd.read_excel(io.BytesIO(file2_obj['Body'].read()))

    # Example comparison: Check if dataframes are equal
    comparison_result = file1_df.equals(file2_df)

    # Return the comparison result as a string
    return 'Files are identical' if comparison_result else 'Files are different'

def lambda_handler(event, context):
    # Extract bucket name and file keys from the event object
    bucket_name = event['bucket_name']
    file1_key = event['file1_key']
    file2_key = event['file2_key']

    # Perform comparison
    result = compare_excels(bucket_name, file1_key, file2_key)

    # Return result
    return {
        'statusCode': 200,
        'body': result
    }
