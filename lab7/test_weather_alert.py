from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

# Any kind of input at all: strings, None, numbers, bools, lists
ANYTHING = st.one_of(
    st.none(), st.text(), st.integers(), st.floats(),
    st.booleans(), st.lists(st.integers()),
)


# ---------- 1. "Must not crash" properties ----------
@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    try:
        parse_reading(s)
    except Exception as e:
        assert False, f"parse_reading crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    try:
        wind_category(s)
    except Exception as e:
        assert False, f"wind_category crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    try:
        rainfall_spread(s)
    except Exception as e:
        assert False, f"rainfall_spread crashed with: {e!r} on input {s!r}"


# ---------- 2. Same idea, with non-string types too ----------
@given(ANYTHING)
def test_all_functions_survive_any_type(x):
    for func in (parse_reading, wind_category, rainfall_spread):
        try:
            func(x)
        except Exception as e:
            assert False, f"{func.__name__} crashed with: {e!r} on input {x!r}"


# ---------- 3. Correctness properties on VALID input ----------
@given(st.floats(allow_nan=False, allow_infinity=False), st.integers(0, 100))
def test_parse_reading_valid_roundtrip(temp, humidity):
    assert parse_reading(f"{temp}/{humidity}") == (temp, humidity)


@given(st.integers(min_value=0, max_value=10**6))
def test_wind_category_valid_speeds(speed):
    result = wind_category(str(speed))
    if speed >= 89:
        assert result == "warning"
    elif speed >= 39:
        assert result == "advisory"
    else:
        assert result == "none"


@given(st.lists(st.floats(min_value=0, max_value=1e6), min_size=1, max_size=20))
def test_rainfall_spread_is_non_negative(values):
    csv = ",".join(str(v) for v in values)
    result = rainfall_spread(csv)
    assert result is not None
    assert result >= 0
    assert result == max(values) - min(values)


# ---------- 4. Invalid input must be rejected cleanly (None) ----------
def test_known_bad_inputs_return_none():
    assert parse_reading(None) is None
    assert parse_reading("") is None
    assert parse_reading("35") is None
    assert parse_reading("a/b") is None
    assert parse_reading("30/150") is None
    assert wind_category(None) is None
    assert wind_category("abc") is None
    assert wind_category("-5") is None
    assert rainfall_spread(None) is None
    assert rainfall_spread("") is None
    assert rainfall_spread("1,,3") is None
    assert rainfall_spread("nan,2") is None
