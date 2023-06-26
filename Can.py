/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (2.0.3) or chardet (5.1.0) doesn't match a supported version!
  warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported "
Traceback (most recent call last):
  File "test5.py", line 62, in <module>
    main(debug=True)
  File "test5.py", line 53, in main
    send_can_message(bus, telemetry)
  File "test5.py", line 6, in send_can_message
    candump=convert_telemetry_to_candump(telemetry)
  File "test5.py", line 13, in convert_telemetry_to_candump
    temperature = telemetry["reported"]["temperature"]   # Scale and convert to integer
KeyError: 'reported'
