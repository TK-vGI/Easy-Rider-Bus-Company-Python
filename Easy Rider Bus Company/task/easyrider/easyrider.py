import re
import json

# path_to_html = "./Unlost in time/task.html"

pattern_stop_name = re.compile(r'^([A-Z][a-z]+(?: [A-Z][a-z]+)*) (Road|Avenue|Boulevard|Street)$')
pattern_stop_type = re.compile(r'[SOF]?$')
pattern_a_time = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')

correct_data_types = {
    "bus_id": {"type": int, "format": False, "required": True},
    "stop_id": {"type": int, "format": False, "required": True},
    "stop_name": {"type": str, "format": pattern_stop_name, "required": True},
    "next_stop": {"type": int, "format": False, "required": True},
    "stop_type": {"type": str, "format": pattern_stop_type, "required": False},
    "a_time": {"type": str, "format": pattern_a_time, "required": True}
}

correct_bus_lines = {
    "red":{"bus_id": 128,"stops": 4, "stop_names": ["Prospekt Avenue", "Bourbon Street", "Sunset Boulevard", "Sesame Street"]},
    "green": {"bus_id": 256, "stops": 4, "stop_names": ["Pilotow Street", "Elm Street", "Fifth Avenue", "Sesame Street"]},
    "blue":{"bus_id": 512,"stops": 2, "stop_names": ["Bourbon Street", "Sunset Boulevard"]},
}


def output(err: dict, bus_lines: dict) -> None:
    total_err = sum([value for value in err.values()])
    print(f"Type and field validation: {total_err} errors")
    print(f"bus_id: {err['bus_id']}")
    print(f"stop_id: {err['stop_id']}")
    print(f"stop_name: {err['stop_name']}")
    print(f"next_stop: {err['next_stop']}")
    print(f"stop_type: {err['stop_type']}")
    print(f"a_time: {err['a_time']}")
    print()
    print("Line names and number of stops:")
    for bus, stops in bus_lines.items():
        print(f"bus_id: {bus} stops: {stops}")

def is_required_field_valid(value, required):
    return not (required and value == "")

def is_type_valid(value, expected_type):
    return isinstance(value, expected_type)

def is_format_valid(value, format_pattern):
    return format_pattern is False or re.match(format_pattern, str(value))

def aggregate_errors(data: dict) -> dict[str, int]:
    error_list = {key: 0 for key in correct_data_types}

    for line in data:
        for field, specs in correct_data_types.items():
            value = line.get(field)
            required = specs["required"]
            expected_type = specs["type"]
            format_pattern = specs["format"]

            # Check for required fields
            if not is_required_field_valid(value, required):
                error_list[field] += 1
                continue

            # Check for correct type
            if value is not None and not is_type_valid(value, expected_type):
                error_list[field] += 1
                continue

            # Check format if pattern exist
            if value is not None and not is_format_valid(value, format_pattern):
                error_list[field] += 1

    return error_list


def count_bus_stops(data: list[dict]) -> dict[int, int]:
    stop_counts = {}

    for entry in data:
        bus_id = entry.get("bus_id")

        # Only count valid bus_id entries
        if isinstance(bus_id, int):
            stop_counts[bus_id] = stop_counts.get(bus_id, 0) + 1

    return stop_counts


def load_data():
    return json.loads(input())


def main():
    # # Open and read the JSON file
    # with open('test_file_3.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)

    data = load_data()

    result_errors = aggregate_errors(data)
    bus_lines = count_bus_stops(data)

    # Output result
    output(result_errors, bus_lines)


if __name__ == "__main__":
    main()