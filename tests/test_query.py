"""
Tests for the NTSBCarolAPITool, focusing on live API interactions and input validation.
"""

import datetime  # Required for date comparisons
import json
import time  # Potentially useful for rate limiting between tests

import pytest

# Assuming ntsbtool.py is in the same directory or accessible in PYTHONPATH
from ntsb_query import NTSBSearchTool


@pytest.fixture
def tool():
    """Provides an instance of the NTSBCarolAPITool for each test."""
    return NTSBSearchTool()


# Helper function to parse the tool's output string
def parse_tool_output(result_str: str):
    """
    Parses the tool's output string into total count, displayed count, and data.
    Returns (total_count, displayed_count, output_data) or raises ValueError.
    """
    if "No results found" in result_str:
        # Handle the case where the tool explicitly says no results were found
        # It might still report a total count from the API even if Results list is empty
        try:
            # Look for "Total count reported by API: X"
            count_part = result_str.split("Total count reported by API: ")[1].replace(
                ")", ""
            )
            total_count = int(count_part)
        except (IndexError, ValueError):
            # Fallback if the exact format changes or isn't present
            total_count = 0
        return total_count, 0, []

    if not result_str.startswith("Found ") or "Displaying " not in result_str:
        raise ValueError(f"Unexpected result string format: {result_str}")

    parts = result_str.split(" Displaying ")
    header_part = parts[0]  # "Found X total results."
    data_part_header = parts[1]  # "Y: [{...}]" or "Y: []"

    total_count = int(header_part.split(" ")[1])

    display_count_and_json = data_part_header.split(": ", 1)
    displayed_count = int(display_count_and_json[0])

    json_output_str = display_count_and_json[1]
    output_data = json.loads(json_output_str)

    return total_count, displayed_count, output_data


@pytest.mark.parametrize(
    "test_id, args",
    [
        (
            "request_1",
            {
                "start_date": "01/01/2023",
                "end_date": "12/31/2023",
                "investigation_mode": "Aviation",
                "city": "San Jose",
                "state": "California",
                "max_results": 5,
            },
        ),
        (
            "request_2",
            {
                "start_date": "01/01/2022",
                "end_date": "12/31/2022",
                "investigation_mode": "Aviation",
                "narrative_keywords": "gear failure",
                "max_results": 5,
            },
        ),
    ],
)
def test_various_criteria(tool, test_id, args):
    """Tests the tool with different sets of criteria, hitting the live API."""
    time.sleep(1)  # Be kind to the API
    result_str = tool.run(**args)
    print(f"\nAPI Response ({test_id} criteria): {result_str}")  # For debugging

    try:
        total_count, displayed_count, output_data = parse_tool_output(result_str)
    except (ValueError, json.JSONDecodeError) as e:
        pytest.fail(
            f"Failed to parse result string for {test_id}: {result_str}. Error: {e}"
        )

    assert displayed_count == len(output_data)
    assert len(output_data) <= args["max_results"]

    if len(output_data) > 0:
        first_record = output_data[0]

        if "city" in args:
            assert first_record.get("City") == args["city"]
        if "state" in args:
            # API returns full state name in response
            assert first_record.get("State") == args["state"]
        if "investigation_mode" in args:
            assert first_record.get("Mode") == args["investigation_mode"]

        assert "NTSBEntryId" in first_record
        assert "NtsbNo" in first_record
        assert "EventDate" in first_record

        event_date_str = first_record.get("EventDate", "").split("T")[0]
        query_start_date_obj = datetime.datetime.strptime(
            args["start_date"], "%m/%d/%Y"
        ).date()
        query_end_date_obj = datetime.datetime.strptime(
            args["end_date"], "%m/%d/%Y"
        ).date()

        if event_date_str:  # Ensure EventDate is present and valid
            try:
                event_date_obj = datetime.datetime.strptime(
                    event_date_str, "%Y-%m-%d"
                ).date()
                assert query_start_date_obj <= event_date_obj <= query_end_date_obj
            except ValueError:
                pytest.fail(
                    f"Could not parse event_date_str from record for {test_id}: {event_date_str}"
                )

        if "narrative_keywords" in args:
            # Note: Verifying narrative_keywords directly is hard as
            # narratives aren't in simplified output.  We rely on the
            # API filtering correctly.  This part remains a comment as
            # per original logic.
            pass

    else:
        print(
            f"Note: 0 displayed results for {test_id} "
            f"(API Total: {total_count}). This is acceptable."
        )


def test_default_max_results(tool):
    """Tests that the default max_results (10) is respected for displayed items."""
    args = {
        "state": "California",
        "start_date": "01/01/2023",  # Narrow recent range
        "end_date": "01/01/2025",
        # max_results is not specified, tool defaults to 10 for display
    }
    time.sleep(1)
    result_str = tool.run(**args)
    print(f"\nAPI Response (Default max_results): {result_str}")

    try:
        total_count, displayed_count, output_data = parse_tool_output(result_str)
    except (ValueError, json.JSONDecodeError) as e:
        pytest.fail(f"Failed to parse result string: {result_str}. Error: {e}")

    assert displayed_count == len(output_data)
    # Tool's NTSBSearchInput default for max_results is 10.
    # The tool requests this many (or min(this, 50)) from the API.
    assert len(output_data) <= 10

    if len(output_data) > 0:
        assert output_data[0].get("State") == args["state"]
    else:
        print(
            "Note: 0 displayed results for default_max_results test "
            f"(API Total: {total_count}). This is acceptable."
        )


# --- Input validation tests (do not require API calls) ---
def test_invalid_date_format(tool):
    """Tests error handling for invalid date formats."""
    result_start = tool.run(
        start_date="2020-01-01"
    )  # YYYY-MM-DD is wrong format for input
    assert result_start == "Error: Invalid start_date format. Please use MM/DD/YYYY."

    result_end = tool.run(end_date="2020/01/01")  # YYYY/MM/DD is wrong format for input
    assert result_end == "Error: Invalid end_date format. Please use MM/DD/YYYY."


def test_invalid_state_name(tool):
    """Tests error handling for invalid state names."""
    result = tool.run(state="NonExistentState")
    assert (
        result
        == "Error: Invalid state name 'NonExistentState'. Please use a full US state name."
    )


def test_no_criteria_error(tool):
    """Tests error handling when no search criteria are provided."""
    result = tool.run()  # No arguments
    assert result == "Error: No valid search criteria provided to form a query."
