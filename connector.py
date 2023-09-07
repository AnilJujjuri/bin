from pyModbusTCP.client import ModbusClient
import time
from azure.iot.device import IoTHubModuleClient


def send_to_iothub(data):

    try:
        CONNECTION_STRING = "HostName=EDGTneerTrainingPractice.azure-devices.net;DeviceId=edgeDevive-opcua;SharedAccessKey=jiDsujbUvP2MySzcHAg+eDYEKf97zrh+YTqM6sGjkQU="
        module_client = IoTHubModuleClient.create_from_connection_string(
            CONNECTION_STRING)
        module_client.connect()
        module_client.patch_twin_reported_properties(data)
        module_client.disconnect()
        print(f"Successfully sent data to IoT Hub--->  {data}")
    except Exception as e:
        print("Error sending data to IoT Hub:", str(e))


def collect(twin, edgeClient, Message):
    # twin2={
    #         'desired': {
    #             '$version': 1,
    #             'SERVER_IP':"3.86.56.32",
    #             'SERVER_PORT':2109
    #         },
    #         'reported': {
    #             'properties': {
    #                 'temperature': 32,
    #                 'pressure': 64
    #             },
    #             '$version': 2326
    #         }
    # }
    # print(twin)
    SERVER_IP = "3.86.56.32"
    SERVER_PORT = 2109

    client = ModbusClient(host=SERVER_IP, port=SERVER_PORT)

    if not client.is_open:
        if not client.open():
            print(f"Unable to connect to {SERVER_IP}:{SERVER_PORT}")
            exit(1)
    try:
        while True:
            # Read temperature and pressure values from the server
            data = client.read_holding_registers(0, 4)

            if data:
                energy = data[0]
                voltage = data[1]
                current = data[2]
                power = data[3]

                data_to_send = {
                    "energy": energy,
                    "voltage": voltage,
                    "current": current,
                    "power": power
                }
                send_to_iothub(data_to_send)
                # print(f"Temperature: {temperature}°C")
                # print(f"Pressure: {pressure} hPa")
                print(data_to_send)
                time.sleep(2)
            else:
                print("Failed to read data from the server")

    except KeyboardInterrupt:
        print("Closing Modbus client...")
        client.close()


def setConnection(twinObj, edgeClient, Message):
    print(twinObj)
    myedgeclient = edgeClient
    myMessage = Message

    global twin
    twin = twinObj

    if twin:
        twin = twinObj
        time.sleep(1)
        print("Starting data acquisition task")

        collect(twin, myedgeclient, myMessage)
    else:
        twin = twinObj
    print("Updated twin")
    # print(twinObj)
    # print(twin)

    # SERVER_IP = "3.86.56.32"
    # SERVER_PORT = 2109

    # print(SERVER_IP)
    # print(SERVER_PORT)
