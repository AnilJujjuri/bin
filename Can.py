File "/home/Machine1/can_connector/can_connector/rec.py", line 32, in <module>
    main()
  File "/home/Machine1/can_connector/can_connector/rec.py", line 29, in main
    receive_can_messages(bus)
  File "/home/Machine1/can_connector/can_connector/rec.py", line 18, in receive_can_messages
    direction = 'Rx' if message.is_received else 'Tx'
AttributeError: 'Message' object has no attribute 'is_received'
SocketcanBus was not properly shut down
