"""Tests targeting high line and branch coverage for weather_alert.py.
"""

import pytest

from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


@pytest.mark.parametrize(
    ("speed", "expected"),
    [
        (0, "none"),
        (38, "none"),
        (39, "advisory"),
        (61, "advisory"),
        (62, "watch"),
        (88, "watch"),
        (89, "warning"),
        (120, "warning"),
    ],
)
def test_wind_alert_all_threshold_branches(speed, expected):
    assert wind_alert(speed) == expected


@pytest.mark.parametrize(
    ("rainfall", "saturated", "expected"),
    [
        (0, False, "none"),
        (9.9, False, "none"),
        (10, False, "advisory"),
        (10, True, "watch"),
        (49.9, False, "advisory"),
        (49.9, True, "watch"),
        (50, False, "watch"),
        (50, True, "warning"),
    ],
)
def test_rain_alert_all_threshold_and_nested_branches(rainfall, saturated, expected):
    assert rain_alert(rainfall, saturated) == expected


@pytest.mark.parametrize(
    ("temperature", "humidity", "expected"),
    [
        (20, 40, "none"),
        (35, 40, "advisory"),
        (40, 40, "watch"),
        (45, 40, "warning"),
        (30, 90, "advisory"),
        (40, 90, "warning"),
        (43, 70, "warning"),
    ],
)
def test_heat_alert_threshold_and_humidity_branches(temperature, humidity, expected):
    assert heat_alert(temperature, humidity) == expected


def test_overall_alert_loop_and_severity_branches():
    assert overall_alert([]) == "none"  # loop does not execute
    assert overall_alert(["none"]) == "none"  # severity comparison false
    assert overall_alert(["advisory", "none"]) == "advisory"
    assert overall_alert(["watch", "advisory"]) == "watch"
    assert overall_alert(["warning", "watch"]) == "warning"


def test_overall_alert_rejects_unknown_alert():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])
