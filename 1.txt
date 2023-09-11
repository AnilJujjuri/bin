import connector
import time
from azure.iot.device import IoTHubModuleClient, Message

CONNECTION_STRING = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=edgeDevive-opcua;SharedAccessKey=jiDsujbUvP2MySzcHAg+eDYEKf97zrh+YTqM6sGjkQU="

def create_client_with_retry(max_retries=3, retry_delay=5):
    retries = 0
    client = None

    while retries < max_retries:
        try:
            client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
            break  # Connection successful, exit the loop
        except Exception as e:
            print("Error occurred:", e)
            retries += 1
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    if client:
        def twin_patch_handler(twin_patch):
            print("Twin patch received:")
            print(twin_patch)

        try:
            client.on_twin_desired_properties_patch_received = twin_patch_handler
        except:
            client.shutdown()
        try:
            twin = client.get_twin()
            connector.setConnection(twin, client, Message)
        except Exception as e:
            print(e)
    else:
        print(f"Failed to create the client after {max_retries} retries.")

if __name__ == "__main__":
    create_client_with_retry()
