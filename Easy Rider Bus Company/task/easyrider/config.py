import re

FIELD_PATTERNS = {
    "stop_name": re.compile(r'^[A-Z][a-z]+(?: [A-Z][a-z]+)* (Road|Avenue|Boulevard|Street)$'),
    "stop_type": re.compile(r'^[SOF]?$'),
    "arrival_time": re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$')
}

FIELD_SPECIFICATIONS = {
    "bus_id": {"type": int, "format": None, "required": True},
    "stop_id": {"type": int, "format": None, "required": True},
    "stop_name": {"type": str, "format": FIELD_PATTERNS["stop_name"], "required": True},
    "next_stop": {"type": int, "format": None, "required": True},
    "stop_type": {"type": str, "format": FIELD_PATTERNS["stop_type"], "required": False},
    "arrival_time": {"type": str, "format": FIELD_PATTERNS["arrival_time"], "required": True}
}

CORRECT_BUS_LINES = {
    128: {
        "stops": 8,
        "S": "Fifth Avenue",
        "F": "Prospekt Avenue",
        "stop_names": [
            "Fifth Avenue", "Abbey Road", "Santa Monica Boulevard", "Elm Street",
            "Beale Street", "Sesame Street", "Bourbon Street", "Prospekt Avenue"
        ],
        "color": "red"
    },
    256: {
        "stops": 9,
        "S": "Pilotow Street",
        "F": "Michigan Avenue",
        "stop_names": [
            "Pilotow Street", "Startowa Street", "Elm Street", "Lombard Street",
            "Sesame Street", "Orchard Road", "Sunset Boulevard", "Khao San Road",
            "Michigan Avenue"
        ],
        "color": "green"
    },
    512: {
        "stops": 8,
        "S": "Arlington Road",
        "F": "Prospekt Avenue",
        "stop_names": [
            "Arlington Road", "Parizska Street", "Elm Street", "Niebajka Avenue",
            "Jakis Street", "Sunset Boulevard", "Jakas Avenue", "Prospekt Avenue"
        ],
        "color": "blue"
    }
}