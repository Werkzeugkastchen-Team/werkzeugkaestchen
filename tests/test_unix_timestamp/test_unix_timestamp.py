import pytest
from tools.unix_timestamp.unix_timestamp_tool import UnixTimestampTool


def test_unix_timestamp_initialization():
    """Test if the tool initializes correctly"""
    tool = UnixTimestampTool()
    assert tool.name == "Unix\-Timestamp Konverter"
    assert "timestamp" in tool.input_params
    assert "timezone" in tool.input_params
    assert "conversion_type" in tool.input_params
    assert "date" in tool.input_params
    assert "time" in tool.input_params

# Tests for timestamp to date conversion


def test_valid_timestamp_conversion():
    """Test valid timestamp conversion"""
    tool = UnixTimestampTool()

    # Test with a known timestamp (January 1, 2022 00:00:00 UTC)
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "1640995200",
        "timezone": "UTC"
    })

    assert result == True
    assert "01.01.2022" in tool.output
    assert "00:00:00" in tool.output
    assert "UTC" in tool.output


def test_timezone_conversion():
    """Test timezone conversion"""
    tool = UnixTimestampTool()

    # Test with a known timestamp and different timezone
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "1640995200",
        "timezone": "America/New_York"
    })

    assert result == True
    assert "31.12.2021" in tool.output  # New York is 5 hours behind UTC
    assert "19:00:00" in tool.output
    assert "America/New_York" in tool.output


def test_empty_timestamp():
    """Test handling of empty timestamp"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "",
        "timezone": "UTC"
    })

    assert result == False
    assert "Bitte geben Sie einen Unix\-Timestamp ein\." in tool.error_message


def test_invalid_timestamp():
    """Test handling of invalid timestamp"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "abc",
        "timezone": "UTC"
    })

    assert result == False
    assert "Der eingegebene Wert ist kein gültiger Unix\-Timestamp\. Bitte geben Sie eine ganze Zahl ein\." in tool.error_message


def test_negative_timestamp():
    """Test handling of negative timestamp"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "-1",
        "timezone": "UTC"
    })

    assert result == False
    assert "Negative Timestamps werden nicht unterstützt" in tool.error_message


def test_invalid_timezone():
    """Test handling of invalid timezone"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "timestamp_to_date",
        "timestamp": "1640995200",
        "timezone": "Invalid/Zone"
    })

    assert result == False
    assert "Unbekannte Zeitzone" in tool.error_message

# Tests for date to timestamp conversion


def test_valid_date_to_timestamp():
    """Test valid date to timestamp conversion"""
    tool = UnixTimestampTool()

    # Test with a known date (January 1, 2022 00:00:00 UTC)
    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "01.01.2022",
        "time": "00:00:00",
        "timezone": "UTC"
    })

    assert result == True
    assert "1640995200" in tool.output


def test_date_to_timestamp_timezone_handling():
    """Test timezone handling for date to timestamp conversion"""
    tool = UnixTimestampTool()

    # Test with a known date in New York timezone
    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "31.12.2021",
        "time": "19:00:00",
        "timezone": "America/New_York"
    })

    assert result == True
    assert "1640995200" in tool.output  # Should be the same timestamp


def test_date_without_time():
    """Test date conversion without specifying time"""
    tool = UnixTimestampTool()

    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "01.01.2022",
        "timezone": "UTC"
    })

    assert result == True
    assert "1640995200" in tool.output  # 00:00:00 UTC


def test_empty_date():
    """Test handling of empty date"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "",
        "timezone": "UTC"
    })

    assert result == False
    assert "Bitte geben Sie ein Datum ein" in tool.error_message


def test_invalid_date_format():
    """Test handling of invalid date format"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "2022-01-01",  # Wrong format, should be DD.MM.YYYY
        "timezone": "UTC"
    })

    assert result == False
    assert "Ungültiges Datumsformat" in tool.error_message


def test_invalid_time_format():
    """Test handling of invalid time format"""
    tool = UnixTimestampTool()
    result = tool.execute_tool({
        "conversion_type": "date_to_timestamp",
        "date": "01.01.2022",
        "time": "25:70:99",  # Invalid time
        "timezone": "UTC"
    })

    assert result == False
    assert "Ungültige Uhrzeit" in tool.error_message
