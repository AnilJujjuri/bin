from modbus_tk import modbus_tcp
from modbus_tk.defines import READ_HOLDING_REGISTERS, WRITE_SINGLE_REGISTER
import logging

def run_modbus_server():
    server = modbus_tcp.TcpServer(address="0.0.0.0", port=5020)
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
    logger.setLevel(logging.INFO)

    try:
        logger.info("Modbus server is running...")
        server.start()
        slave = server.add_slave(1)
        slave.add_block("holding", READ_HOLDING_REGISTERS, 0, 100)
        slave.add_block("coil", WRITE_SINGLE_REGISTER, 0, 100)
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    run_modbus_server()
