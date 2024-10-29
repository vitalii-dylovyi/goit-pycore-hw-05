import sys
from datetime import datetime
from typing import Optional
from functools import reduce


def parse_log_line(line: str) -> Optional[dict]:
    """
    Parse a single log line into components.
    Returns None if the line format is invalid.
    """
    try:
        # Using more robust splitting and validation
        parts = line.strip().split(" ", 3)
        if len(parts) < 4:
            raise ValueError("Invalid log line format")

        # Validate date format
        datetime.strptime(f"{parts[0]} {parts[1]}", "%Y-%m-%d %H:%M:%S")

        # Validate log level
        level = parts[2]
        if level not in ["INFO", "DEBUG", "ERROR", "WARNING"]:
            raise ValueError(f"Invalid log level: {level}")

        return {
            "date": f"{parts[0]} {parts[1]}",
            "level": level,
            "message": parts[3].strip(),
        }
    except (IndexError, ValueError) as e:
        print(f"Warning: Skipping invalid log line: {line.strip()} ({str(e)})")
        return None


def load_logs(file_path: str) -> list:
    """
    Load and parse logs from file.
    """
    try:
        with open(file_path, "r") as file:
            # Using functional approach with filter and list comprehension
            logs = list(filter(None, map(parse_log_line, file)))

            if not logs:
                print("Warning: No valid log entries found in file")

            return logs

    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except PermissionError:
        print(f"Error: Permission denied accessing {file_path}")
        return []
    except Exception as e:
        print(f"Error: Unexpected error reading file: {str(e)}")
        return []


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Filter logs by level.
    """
    return list(filter(lambda log: log["level"].upper() == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Count logs by level.
    """
    return reduce(
        lambda acc, log: {**acc, log["level"]: acc.get(log["level"], 0) + 1}, logs, {}
    )


def display_log_counts(counts: dict):
    """
    Display log counts in a formatted table.
    """
    if not counts:
        print("No logs to display")
        return

    print("\nLog Level Statistics:")
    print("-" * 30)
    print(f"{'Level':<14} | {'Count':<8}")
    print("-" * 30)

    # Sort levels for consistent display
    for level in sorted(counts.keys()):
        print(f"{level:<14} | {counts[level]:<8}")


def display_filtered_logs(logs: list, level: str):
    """
    Display filtered logs in a formatted way.
    """
    if not logs:
        print(f"\nNo logs found for level '{level}'")
        return

    print(f"\nDetailed logs for level '{level}':")
    print("-" * 50)

    # Using list comprehension for formatting
    formatted_logs = [
        f"{log['date']} - {log['message']}"
        for log in sorted(logs, key=lambda x: x["date"])
    ]
    print("\n".join(formatted_logs))


def main():
    """
    Main function handling command line arguments and program flow.
    """
    if len(sys.argv) < 2:
        print("Usage: python task_3.py <path_to_logfile> [log_level]")
        return

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if not logs:
        return

    # Calculate and display statistics
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Handle optional level filter
    if len(sys.argv) > 2:
        level = sys.argv[2].upper()
        if level not in ["INFO", "DEBUG", "ERROR", "WARNING"]:
            print(f"Error: Invalid log level '{level}'")
            print("Valid levels: INFO, DEBUG, ERROR, WARNING")
            return

        filtered_logs = filter_logs_by_level(logs, level)
        display_filtered_logs(filtered_logs, level)


if __name__ == "__main__":
    main()
