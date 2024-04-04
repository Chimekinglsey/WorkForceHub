import boto3
import json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name='us-east-1'):

    if not secret_name or not region_name:
        return None

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret
