import math


def parse_reading(text):
    """Parse 'temperature/humidity' (e.g. '35.5/80').

    Returns (temperature: float, humidity: int) or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    try:
        temp = float(parts[0])
        humidity = int(parts[1])
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(temp):
        return None
    if not 0 <= humidity <= 100:
        return None
    return temp, humidity


def wind_category(speed_text):
    """Return 'warning', 'advisory' or 'none' for a wind speed in km/h.

    Returns None if the input is not a valid non-negative whole number.
    """
    if not isinstance(speed_text, (str, int)) or isinstance(speed_text, bool):
        return None
    try:
        speed = int(speed_text)
    except (ValueError, OverflowError):
        return None
    if speed < 0:
        return None
    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    """Return max - min of comma-separated rainfall readings (mm).

    Returns None if the input is empty, malformed, negative or not finite.
    """
    if not isinstance(readings_csv, str):
        return None
    try:
        readings = [float(r) for r in readings_csv.split(',')]
    except (ValueError, OverflowError):
        return None
    if not readings:
        return None
    if any(not math.isfinite(r) or r < 0 for r in readings):
        return None
    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result if result is not None else "Invalid input")

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result if result is not None else "Invalid input")

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
