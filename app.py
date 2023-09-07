import connector
import time
from azure.iot.device import IoTHubModuleClient, Message
# import logging

# # Configure the logger
# logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Example log messages
# logging.debug('This is a debug message')


CONNECTION_STRING = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=edgeDevive-opcua;SharedAccessKey=jiDsujbUvP2MySzcHAg+eDYEKf97zrh+YTqM6sGjkQU="


def create_client():
    # Instantiate client
    try:
        client = IoTHubModuleClient.create_from_connection_string(
            CONNECTION_STRING)
    except Exception as e:
        print("Error occured:", e)

    def twin_patch_handler(twin_patch):
        print("Twin patch received:")
        print(twin_patch)

    try:
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except:
        client.shutdown()
    try:
        twin = client.get_twin()
        # print(twin)
    except Exception as e:
        print(e)

    connector.setConnection(twin, client, Message)

    # return client

# def callnextcode():
#     twin={
#         "server_ip" : "3.86.56.32",
#         "server_port" : 2109
#     }
#     connector.setConnection(twin)


if __name__ == "__main__":
    # callnextcode()
    create_client()
