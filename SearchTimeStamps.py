
import json
from datetime import datetime


mapping = {'NOBODY': 0, 'LOOKING_DOWN': 1, 'SMOKING': 2, 'CALLING': 3, 'LDW': 5, 'EYE_CLOSED': 4, 'LDW_R': 5, 'LDW_L': 5, 'FCW': 6, 'camera cover!': 0, 'infrared block!': 0}

#  Invert the mapping dictionary
inverted_mapping = {v: k for k, v in mapping.items()}

def search_and_aggregate(data, start_datetime, end_datetime, target_id=None):
    result = {}

    start_datetime = datetime.strptime(start_datetime, "%Y%m%d%H%M%S")
    end_datetime = datetime.strptime(end_datetime, "%Y%m%d%H%M%S")

    for entry in data:
        entry_datetime = datetime.strptime(entry["timestamp"], "%Y%m%d%H%M%S")

        # Check if the entry is within the specified date and time range
        if start_datetime <= entry_datetime <= end_datetime:
            # Check if the entry matches the target ID if specified
            if target_id is None or entry["id"] == target_id:
                entry_type = entry["type"]
                result[entry_type] = result.get(entry_type, 0) + 1

    return result


if __name__ == '__main__':
    with open("./Datafiles/Timestamps_data_Dec23.json", "r") as json_file:
        data_str = json_file.read()
    data = json.loads(data_str)

    start_datetime = "20211109100000"  # Enter the start datetime in YYYYMMDDHHMMSS format
    end_datetime = "20221109120000"    # Enter the end datetime in YYYYMMDDHHMMSS format
    target_id = "1006"                  # Enter the target ID (or set to None for all IDs)

    result = search_and_aggregate(data, start_datetime, end_datetime, target_id)

    print(f"Aggregated Result: {result}")
    for entry_type, count in result.items():
        type_str = inverted_mapping[entry_type]
        print(f"Type {type_str}: {count} occurrences")


