import os
import configparser

print(os.getcwd())
# Path to the AWS credentials file
aws_credentials_file = os.path.expanduser('~/.aws/credentials')

# Path to the file containing new credentials
new_creds_file = '/Users/Shyju.Viswambaran/backend/my-python-utils/cred.txt'

new_creds = {}
with open(new_creds_file, 'r') as file:
    for line in file:
        if line.startswith('export '):
            key, value = line.strip().replace('export ', '').split('=', maxsplit=1)
            new_creds[key] = value

# Update the [default] section of the AWS credentials file
config = configparser.ConfigParser()
config.read(aws_credentials_file)

if 'default' not in config.sections():
    config.add_section('default')

config['default']['aws_access_key_id'] = new_creds.get('AWS_ACCESS_KEY_ID', '')
config['default']['aws_secret_access_key'] = new_creds.get('AWS_SECRET_ACCESS_KEY', '')
config['default']['aws_session_token'] = new_creds.get('AWS_SESSION_TOKEN', '')

# Write the updated configuration back to the file
with open(aws_credentials_file, 'w') as file:
    config.write(file)
