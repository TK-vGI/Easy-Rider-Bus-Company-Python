from typing import List, Dict, Tuple, Optional


def count_bus_stops(data: List[Dict]) -> Dict[int, int]:
    """Count the number of stops per bus line.

    Args:
        data: List of stop dictionaries.

    Returns:
        Dictionary mapping bus_id to stop count.
    """
    return {
        line["bus_id"]: sum(1 for l in data if l["bus_id"] == line["bus_id"] and isinstance(line["bus_id"], int))
        for line in data if isinstance(line["bus_id"], int)
    }


def get_stop_types_by_line(data: List[Dict]) -> Dict[int, Dict[str, List[str]]]:
    """Organize stops by bus line and type (start or finish).

    Args:
        data: List of stop dictionaries.

    Returns:
        Dictionary mapping bus_id to start (S) and finish (F) stop lists.
    """
    stop_types = {}
    for line in data:
        bus_id = line.get("bus_id")
        stop_name = line.get("stop_name")
        stop_type = line.get("stop_type", "")
        if isinstance(bus_id, int) and isinstance(stop_name, str):
            stop_types.setdefault(bus_id, {"S": [], "F": []})
            if stop_type in ("S", "F"):
                stop_types[bus_id][stop_type].append(stop_name)
    return stop_types


def validate_bus_lines(stop_types: Dict[int, Dict[str, List[str]]]) -> Tuple[bool, Optional[int]]:
    """Check if each bus line has exactly one start and one finish stop.

    Args:
        stop_types: Dictionary of bus lines with start and finish stops.

    Returns:
        Tuple of (is_valid, bad_bus_id). If invalid, bad_bus_id is the first invalid bus.
    """
    for bus_id, stops in stop_types.items():
        if len(stops["S"]) != 1 or len(stops["F"]) != 1:
            return False, bus_id
    return True, None


def find_transfer_stops(data: List[Dict]) -> List[str]:
    """Identify stops served by multiple bus lines.

    Args:
        data: List of stop dictionaries.

    Returns:
        Sorted list of transfer stop names.
    """
    stop_to_buses = {}
    for line in data:
        stop_name = line.get("stop_name")
        bus_id = line.get("bus_id")
        if isinstance(bus_id, int) and isinstance(stop_name, str):
            stop_to_buses.setdefault(stop_name, set()).add(bus_id)
    return sorted([stop for stop, buses in stop_to_buses.items() if len(buses) > 1])


def get_unique_stops_by_type(stop_types: Dict[int, Dict[str, List[str]]]) -> Tuple[List[str], List[str]]:
    """Extract unique start and finish stops across all bus lines.

    Args:
        stop_types: Dictionary of bus lines with start and finish stops.

    Returns:
        Tuple of (sorted start stops, sorted finish stops).
    """
    start_stops = set()
    finish_stops = set()
    for stops in stop_types.values():
        start_stops.update(stops["S"])
        finish_stops.update(stops["F"])
    return sorted(start_stops), sorted(finish_stops)


def check_on_demand_stops(data: List[Dict], stop_types: Dict[int, Dict[str, List[str]]],
                          transfer_stops: List[str]) -> List[str]:
    """Identify on-demand stops that are not start, finish, or transfer stops.

    Args:
        data: List of stop dictionaries.
        stop_types: Dictionary of bus lines with start and finish stops.
        transfer_stops: List of transfer stop names.

    Returns:
        Sorted list of valid on-demand stop names.
    """
    critical_stops = set(transfer_stops)
    for stops in stop_types.values():
        critical_stops.update(stops["S"])
        critical_stops.update(stops["F"])
    return sorted([
        line["stop_name"] for line in data
        if line.get("stop_type") == "O" and line.get("stop_name") not in critical_stops
    ])