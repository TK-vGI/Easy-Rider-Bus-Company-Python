from typing import List, Dict, Optional
from datetime import datetime
from config import FIELD_SPECIFICATIONS, CORRECT_BUS_LINES
import re


def validate_required_field(value: Optional[str], required: bool) -> bool:
    """Check if a required field is valid (not empty or None)."""
    return not (required and (value is None or value == ""))


def validate_type(value: Optional[str], expected_type: type) -> bool:
    """Check if a value matches the expected type."""
    return value is None or isinstance(value, expected_type)


def validate_format(value: Optional[str], pattern: Optional[re.Pattern]) -> bool:
    """Check if a value matches the specified regex pattern."""
    return pattern is None or (isinstance(value, str) and bool(re.match(pattern, value)))


def validate_time_chronology(bus_lines: Dict[int, List[Dict]]) -> Dict[str, int]:
    """Validate that arrival times are in ascending order for each bus line."""
    errors = {"arrival_time": 0}
    for bus_id, stops in bus_lines.items():
        previous_time = datetime.strptime("00:00", "%H:%M")
        for stop in stops:
            time_str = stop.get("arrival_time")
            try:
                current_time = datetime.strptime(str(time_str), "%H:%M")
                if current_time <= previous_time:
                    errors["arrival_time"] += 1
                    break
                previous_time = current_time
            except (ValueError, TypeError):
                continue  # Format errors are counted elsewhere
    return errors


def validate_bus_line_stops(bus_lines: Dict[int, List[Dict]]) -> Dict[str, int]:
    """Validate stop counts and names against CORRECT_BUS_LINES."""
    errors = {"bus_id": 0, "stop_name": 0}
    for bus_id, stops in bus_lines.items():
        if bus_id not in CORRECT_BUS_LINES:
            errors["bus_id"] += 1
            continue
        expected = CORRECT_BUS_LINES[bus_id]
        # Check stop count
        if len(stops) != expected["stops"]:
            errors["bus_id"] += 1
            continue
        # Check stop names
        actual_stops = [stop["stop_name"] for stop in stops]
        if actual_stops != expected["stop_names"]:
            errors["stop_name"] += 1
        # Check start and finish stops
        start_stop = next((stop["stop_name"] for stop in stops if stop.get("stop_type") == "S"), None)
        finish_stop = next((stop["stop_name"] for stop in stops if stop.get("stop_type") == "F"), None)
        if start_stop != expected["S"] or finish_stop != expected["F"]:
            errors["stop_name"] += 1
    return errors


def aggregate_errors(data: List[Dict]) -> Dict[str, int]:
    """Aggregate errors for field validation and time chronology.

    Args:
        data: List of stop dictionaries.

    Returns:
        Dictionary with error counts for each field.
    """
    errors = {field: 0 for field in FIELD_SPECIFICATIONS}
    bus_lines = {line["bus_id"]: [] for line in data if isinstance(line.get("bus_id"), int)}

    for line in data:
        for field, specs in FIELD_SPECIFICATIONS.items():
            value = line.get(field)
            if not validate_required_field(value, specs["required"]):
                errors[field] += 1
                continue
            if not validate_type(value, specs["type"]):
                errors[field] += 1
                continue
            if not validate_format(value, specs["format"]):
                errors[field] += 1
        if isinstance(line.get("bus_id"), int):
            bus_lines[line["bus_id"]].append(line)

    # Merge time chronology errors
    time_errors = validate_time_chronology(bus_lines)
    errors.update(time_errors)

    # # Merge bus line stop validation errors
    # stop_errors = validate_bus_line_stops(bus_lines)
    # for field, count in stop_errors.items():
    #     errors[field] += count

    return errors