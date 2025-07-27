from typing import Dict, List, Optional
from config import FIELD_SPECIFICATIONS
from analyzer import get_unique_stops_by_type


def format_output(errors: Dict[str, int], bus_lines: Dict[int, int], stop_types: Dict[int, Dict[str, List[str]]],
                  transfers: List[str], valid: bool, bad_bus: Optional[int], on_demand_stops: List[str]) -> None:
    """Format and print the validation and analysis results.

    Args:
        errors: Dictionary of error counts per field.
        bus_lines: Dictionary of bus_id to stop count.
        stop_types: Dictionary of bus lines with start and finish stops.
        transfers: List of transfer stop names.
        valid: Whether all bus lines have valid start/finish stops.
        bad_bus: ID of the first invalid bus line, if any.
        on_demand_stops: List of valid on-demand stop names.
    """
    total_errors = sum(errors.values())
    print(f"Type and required field validation: {total_errors} errors")
    for field in FIELD_SPECIFICATIONS:
        print(f"{field}: {errors[field]}")
    print("\nLine names and number of stops:")
    for bus_id, count in sorted(bus_lines.items()):
        print(f"bus_id: {bus_id}, stops: {count}")
    if not valid:
        print(f"There is no start or end stop for the line: {bad_bus}")
    else:
        start_stops, finish_stops = get_unique_stops_by_type(stop_types)
        print(f"\nStart stops: {len(start_stops)} {start_stops}")
        print(f"Transfer stops: {len(transfers)} {transfers}")
        print(f"Finish stops: {len(finish_stops)} {finish_stops}")
    print(f"On demand stops: {len(on_demand_stops)} {on_demand_stops}")