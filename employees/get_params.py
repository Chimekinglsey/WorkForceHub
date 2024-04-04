import boto3

def get_parameters(parameter_names):
    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameters(Names=parameter_names, WithDecryption=True)
    parameters = {param['Name']: param['Value'] for param in response['Parameters']}
    return parameters

def lambda_handler(event=None, context=None):
    parameter_names = [
        'ACCESS_KEY_ID',
        'ALLOWED_HOSTS',
        'EMAIL_HOST',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_HOST_USER',
        'EMAIL_SECRET_KEY',
        'S3_REGION_NAME',
        'SECRET_ACCESS_KEY',
        'STORAGE_BUCKET_NAME',
        'db_host',
        'db_name',
        'db_password',
        'db_port',
        'db_username'
    ]
    
    # Fetch parameters from Parameter Store
    parameters = get_parameters(parameter_names)

    # Prepare the dictionary with keys prepended with "AWS_" for uppercase keys
    formatted_parameters = {}
    for key, value in parameters.items():
        formatted_key = "AWS_" + key.upper() if key.isupper() else key
        formatted_parameters[formatted_key] = value

    return formatted_parameters
