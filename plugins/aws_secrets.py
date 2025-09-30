from pathlib import Path
from json import loads
import os
import boto3
from botocore.exceptions import ClientError


def pytest_configure():
    """Loads all secrets from AWS Secrets to environment variables"""
    # pylint: disable=protected-access
    # If an ..env file exists then the variables will be loaded from it and not from AWS Secrets
    if not Path("..env").exists():
        # AWS Secrets configuration of where the secrets are stored
        region = "eu-west-1"
        secret_id = "wnec-backend-tests"

        try:
            # Initiate session (raises an exception if the credentials are not set)
            session = boto3.session.Session()

            # Initiate client (raises an exception if the region is not valid)
            client = session.client("secretsmanager", region_name=region)

            # Get request response (raises exception if ID is not found)
            aws_response = client.get_secret_value(SecretId=secret_id)

            # Prevents weird boto3 warning (https://github.com/boto/boto3/issues/454)
            client._endpoint.http_session._manager.clear()

            # Converts text response to a dictionary
            secrets = loads(aws_response["SecretString"])

            # Save secret values as environment variables
            for key, value in secrets.items():
                os.environ[key] = value

            # Empty status means success
            status = ""
        except ClientError as error:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
            if error.response["Error"]["Code"] == "ResourceNotFoundException":
                status = f'The requested secret "{secret_id}" was not found on region {region}'
            elif error.response["Error"]["Code"] == "InvalidRequestException":
                status = f"The request was invalid: {error}"
            elif error.response["Error"]["Code"] == "UnrecognizedClientException":
                status = f"Invalid AWS access key ID or secret key: {error}"
            elif error.response["Error"]["Code"] == "InvalidParameterException":
                status = f"The request had invalid parameters: {error}"

            os.environ["AWS_SECRETS_STATUS"] = status
        except Exception:
            # Stop further test from failing due to the lack of valid variables
            status = "Unknown Exception"

        # Saves reference for other tests (mainly conftest.py)
        os.environ["AWS_SECRETS_STATUS"] = status
