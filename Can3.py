Traceback (most recent call last):
  File "/home/azure/test11.py", line 63, in <module>
    main(debug=True)
  File "/home/azure/test11.py", line 53, in main
    handle_device_twin_update(twin, bus)
  File "/home/azure/test11.py", line 37, in handle_device_twin_update
    candump = convert_telemetry_to_candump(sensor_id, telemetry_data)
  File "/home/azure/test11.py", line 22, in convert_telemetry_to_candump
    value = max(min(value, 255), 0)
TypeError: '<' not supported between instances of 'int' and 'str'
