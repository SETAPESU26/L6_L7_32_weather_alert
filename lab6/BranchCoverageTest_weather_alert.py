import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# ---- starter tests ----
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

# ---- wind_alert: every decision True and False ----
def test_wind_warning():
    assert wind_alert(100) == "warning"

def test_wind_warning_boundary():
    assert wind_alert(89) == "warning"

def test_wind_watch():
    assert wind_alert(70) == "watch"

def test_wind_watch_boundary():
    assert wind_alert(62) == "watch"

def test_wind_advisory():
    assert wind_alert(45) == "advisory"

def test_wind_advisory_boundary():
    assert wind_alert(39) == "advisory"

def test_wind_just_below_advisory():
    assert wind_alert(38) == "none"

# ---- rain_alert: both inner and outer branches ----
def test_rain_heavy_saturated():
    assert rain_alert(60, True) == "warning"

def test_rain_heavy_dry_soil():
    assert rain_alert(60, False) == "watch"

def test_rain_moderate_saturated():
    assert rain_alert(20, True) == "watch"

def test_rain_moderate_dry_soil():
    assert rain_alert(20, False) == "advisory"

def test_rain_light():
    assert rain_alert(5, False) == "none"

def test_rain_boundaries():
    assert rain_alert(50, False) == "watch"
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(9.9, True) == "none"

# ---- heat_alert: humidity branch True/False + every threshold ----
def test_heat_low_humidity_warning():
    assert heat_alert(46, 20) == "warning"

def test_heat_low_humidity_watch():
    assert heat_alert(41, 20) == "watch"

def test_heat_low_humidity_advisory():
    assert heat_alert(36, 20) == "advisory"

def test_heat_low_humidity_none():
    assert heat_alert(20, 20) == "none"

def test_heat_humidity_exactly_40_adds_nothing():
    assert heat_alert(35, 40) == "advisory"

def test_heat_humid_warning():
    assert heat_alert(44, 90) == "warning"      # 44 + 5.0 = 49

def test_heat_humid_watch():
    assert heat_alert(39, 60) == "watch"        # 39 + 2.0 = 41

def test_heat_humid_advisory():
    assert heat_alert(30, 100) == "advisory"    # 30 + 6.0 = 36

def test_heat_humid_none():
    assert heat_alert(20, 90) == "none"         # 20 + 5.0 = 25

# ---- overall_alert: loop, update/no-update, error ----
def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_later_alert_not_worse():
    assert overall_alert(["warning", "advisory"]) == "warning"

def test_overall_all_none():
    assert overall_alert(["none", "none"]) == "none"

def test_overall_single():
    assert overall_alert(["watch"]) == "watch"

def test_overall_unknown_alert():
    with pytest.raises(ValueError):
        overall_alert(["warning", "tornado"])
