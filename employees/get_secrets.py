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

    secret = json.loas(get_secret_value_response['SecretString'])
    return secret


    # def get_secret(secret_name, region_name='us-east-1'):
#     if not secret_name or not region_name:
#         return None

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     # Retrieve the secret value
#     try:
#         response = client.get_secret_value(SecretId=secret_name)
#     except client.exceptions.ResourceNotFoundException:
#         print("The requested secret was not found")
#         return None
#     except client.exceptions.InvalidRequestException:
#         print("The request was invalid")
#         return None
#     except client.exceptions.ClientError as e:
#         print(f"Error retrieving secret: {e}")
#         return None

#     # Parse and return the secret value
#     if 'SecretString' in response:
#         secret = json.loads(response['SecretString'])
#         return secret
#     else:
#         print("Secret value not found")
#         return None
# import boto3
# from botocore.exceptions import ClientError