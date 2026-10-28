"""Tests targeting high line coverage for weather_alert.py.
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
def test_wind_alert_line_coverage(speed, expected):
    assert wind_alert(speed) == expected


@pytest.mark.parametrize(
    ("rainfall", "saturated", "expected"),
    [
        (0, False, "none"),
        (9.9, True, "none"),
        (10, False, "advisory"),
        (10, True, "watch"),
        (49.9, False, "advisory"),
        (49.9, True, "watch"),
        (50, False, "watch"),
        (50, True, "warning"),
        (75, False, "watch"),
        (75, True, "warning"),
    ],
)
def test_rain_alert_line_coverage(rainfall, saturated, expected):
    assert rain_alert(rainfall, saturated) == expected


@pytest.mark.parametrize(
    ("temperature", "humidity", "expected"),
    [
        (20, 40, "none"),
        (34.9, 40, "none"),
        (35, 40, "advisory"),
        (39.9, 40, "advisory"),
        (40, 40, "watch"),
        (44.9, 40, "watch"),
        (45, 40, "warning"),
        (30, 90, "advisory"),
        (40, 90, "warning"),
        (43, 70, "warning"),
    ],
)
def test_heat_alert_line_coverage(temperature, humidity, expected):
    assert heat_alert(temperature, humidity) == expected


def test_overall_alert_empty_and_severity_order():
    assert overall_alert([]) == "none"
    assert overall_alert(["none"]) == "none"
    assert overall_alert(["advisory"]) == "advisory"
    assert overall_alert(["watch"]) == "watch"
    assert overall_alert(["warning"]) == "warning"


def test_overall_alert_keeps_worst_alert():
    assert overall_alert(["watch", "advisory", "warning", "none"]) == "warning"
    assert overall_alert(["warning", "watch", "advisory"]) == "warning"


def test_overall_alert_rejects_unknown_alert():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["none", "storm"])
