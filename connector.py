from pyModbusTCP.client import ModbusClient
import time
from azure.iot.device import IoTHubModuleClient
from opcua import Client, Node, ua
data_variables = ["temperature", "pressure"]
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
    def dict_format(keys, values):
        return dict(zip(keys, values))

    start_time = time.time()
    while True:
        try:
            if time.time() - start_time > 180:
                # ipc_client.close()
                print("Exiting after 3 minutes.")
                break

            url = "opc.tcp://3.86.56.32:2109/opcua/"
            client = Client(url)
            client.connect()

            data_list = []
            namespace = "mynamespace"
            idx = client.get_namespace_index(namespace)

            for i in range(len(data_variables)):
                myvar = client.nodes.root.get_child(
                    ["0:Objects", "{}:vPLC".format(idx), "{}:{}".format(idx, data_variables[i])])
                val = myvar.get_value()
                data_list.append(val)
            myData = dict_format(data_variables, data_list)
            # myData = json.dumps(myData).encode('utf-8')
            #print(type(myData))
            #print(myData)
            send_to_iothub(myData)

            # resp = ipc_client.publish_to_iot_core(topic_name=topic, qos=qos, payload=myData)
            # print(f"payload sent-----: {resp}")

            client.disconnect()
            time.sleep(0.10)

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
