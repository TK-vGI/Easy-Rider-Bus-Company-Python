from typing import List, Dict, Optional
from data_loader import load_data
from validator import aggregate_errors
from analyzer import count_bus_stops, get_stop_types_by_line, validate_bus_lines, find_transfer_stops, \
    check_on_demand_stops
from output_formatter import format_output


def process_bus_data(data: List[Dict]) -> None:
    """Process bus route data and output validation results.

    Args:
        data: List of stop dictionaries.
    """
    errors = aggregate_errors(data)
    bus_lines = count_bus_stops(data)
    stop_types = get_stop_types_by_line(data)
    valid, bad_bus = validate_bus_lines(stop_types)
    transfers = find_transfer_stops(data)
    on_demand_stops = check_on_demand_stops(data, stop_types, transfers)
    format_output(errors, bus_lines, stop_types, transfers, valid, bad_bus, on_demand_stops)


def main(file_path: Optional[str] = "test_file_6.json") -> None:
    """Main function to orchestrate bus route validation.

    Args:
        file_path: Path to the JSON file, or None for standard input.
    """
    try:
        data = load_data(file_path)
        process_bus_data(data)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # main(file_path=None)  # Use stdin instead of file
    main() # Use JSON file
