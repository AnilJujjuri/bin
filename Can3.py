def handle_device_twin_update(twin, bus):
    reported_properties = twin["reported"]

    for sensor_id, telemetry_data in reported_properties.items():
        if isinstance(telemetry_data, dict):
            can_id_parts = sensor_id.split("_")
            if len(can_id_parts) >= 2 and can_id_parts[1].isnumeric():
                can_id = can_id_parts[1]

                candump = convert_telemetry_to_candump(sensor_id, telemetry_data)

                can_data = []
                for byte in candump.split("_")[1:]:
                    if byte.isnumeric():
                        can_data.append(int(byte) % 256)
                    elif "." in byte:
                        float_value = float(byte)
                        float_bytes = struct.pack('!f', float_value)
                        float_int = struct.unpack('!I', float_bytes)[0]
                        can_data.append(float_int % 256)
                        can_data.append((float_int >> 8) % 256)
                        can_data.append((float_int >> 16) % 256)
                        can_data.append((float_int >> 24) % 256)

                send_can_message(bus, int(can_id), can_data)
