/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (2.0.3) or chardet (5.1.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
Traceback (most recent call last):
  File "test5.py", line 64, in <module>
    main(debug=True)
  File "test5.py", line 55, in main
    send_can_message(bus, telemetry)
  File "test5.py", line 6, in send_can_message
    candump=convert_telemetry_to_candump(telemetry)
  File "test5.py", line 16, in convert_telemetry_to_candump
    candump = f"001 #{temperature:02X}{humidity:02X}"  # Assuming sensor_id is constant as '001'
ValueError: Unknown format code 'X' for object of type 'float'
