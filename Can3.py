
def convert_telemetry_to_candump(sensor_id, telemetry_data):
    candump = f"{sensor_id}_"

    for key, value in telemetry_data.items():
        if isinstance(value, int):
            value = int(value)  # Convert to integer
        elif isinstance(value, float):
            value = int(value * 100)  # Scale float values and convert to integer

        # Limit value to valid byte range
        value = max(min(value, 255), 0)

        candump += f"{key}_{value}_"  # Append key-value pair to the candump string

    return candump.rstrip("_")  # Remove the trailing underscore
