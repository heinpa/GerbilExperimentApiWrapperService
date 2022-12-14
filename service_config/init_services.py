import requests
import json
from os import environ
import sys

mode_message = 'Please specify mode "register" or "update" or "delete"'

# run configuration not provided
if len(sys.argv) != 2:
    print(mode_message)
    sys.exit(-1)
# invalid run configuration provided
elif sys.argv[1] not in ['register', 'update', 'delete']:
    print(mode_message)
    sys.exit(-2)

mode = sys.argv[1]

# load service configuration
with open(environ['CONFIG_FILE']) as f:
    initialization_configuration = json.load(f)

# load microservice updater configuration
host = environ['UPDATER_HOST']
api_key = environ['API_KEY']

# for each service configuration
for i, service in enumerate(initialization_configuration['services']):
    service['API-KEY'] = api_key

    # read all related files and add them to the payload
    if 'files' in service:
        for file in service['files']:
            with open(f'{environ["SETUP_PATH"]}/{service["files"][file]}') as f:
                service['files'][file] = f.read()

    # register new service
    if mode == 'register':
        response = requests.post(f'{host}/service', json=service, headers={'Content-Type': 'application/json'},
                                 verify=False)

        # registration successful
        if response.ok:
            print(f'service {i} registered successfully.', response.text)

            # store service_id for later updates or deletions
            if 'ids' not in initialization_configuration:
                initialization_configuration['ids'] = {}

            initialization_configuration['ids'][str(i)] = response.json()['id']
        # registration failed
        else:
            print(f'registration of service {i} failed:', response.text)
    # update service
    elif mode == 'update':
        if 'ids' in initialization_configuration:
            # send update request
            response = requests.post(f'{host}/service/{initialization_configuration["ids"][str(i)]}',
                                     json=service, headers={'Content-Type': 'application/json'}, verify=False)

            # update initiated successfully
            if response.ok:
                print(f'service {i} update initiated successfully.', response.text)
            # update initiation failed
            else:
                print(f'service {i} update failed.', response.text)
    # delete service
    elif mode == 'delete':
        if 'ids' in initialization_configuration:
            # send delete request
            response = requests.delete(f'{host}/service/{initialization_configuration["ids"][str(i)]}',
                                       json=service, headers={'Content-Type': 'application/json'}, verify=False)

            # deletion successful
            if response.ok:
                print(f'service {i} deleted.', response.text)

                # delete id from configuration
                initialization_configuration['ids'].pop(str(i))
            else:
                print(f'service {i} deletion failed!', response.text)

