from minimalmodbus import ModbusTcpServer

def run_modbus_server():
    server_ip = "0.0.0.0"  # Listen on all available interfaces
    server_port = 5020

    try:
        modbus_server = ModbusTcpServer(server_ip, server_port)
        modbus_server.serve_forever()
    except KeyboardInterrupt:
        modbus_server.close()

if __name__ == "__main__":
    run_modbus_server()
