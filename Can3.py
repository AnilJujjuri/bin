Traceback (most recent call last):
  File "c:\Users\40020507\Downloads\diagslave-3.4\win\new.py", line 61, in <module>
    run_modbus_server()
  File "c:\Users\40020507\Downloads\diagslave-3.4\win\new.py", line 55, in run_modbus_server
    slave.add_block("coil", WRITE_SINGLE_REGISTER, 0, 100)
  File "C:\Users\40020507\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\modbus_tk\modbus.py", line 764, in add_block
    raise InvalidModbusBlockError("Invalid block type {0}".format(block_type))
modbus_tk.exceptions.InvalidModbusBlockError: Invalid block type 6
