def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            value = int(value)
        elif isinstance(value, float):
            value = int(value * 100)
        elif isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    continue  # Skip this key-value pair if conversion is not possible

        value = max(min(value, 255), 0)
        candump += f"{key}_{value}_"

    return candump.rstrip("_")
