# NTSB Accident Search Tool

## Description

The NTSB Accident Search Tool is a Python module designed to query the National Transportation Safety Board (NTSB) CAROL (Case Analysis and Reporting Online) API. It enables users to search for accident and incident records based on a variety of criteria, including date ranges, location, aircraft specifics, and narrative keywords.

This tool is implemented as a `BaseTool` subclass from the `crewai` library, making it suitable for integration into AI agent workflows, but it can also be used as a standalone client for the NTSB API. It handles API session creation and returns structured JSON data.

* https://data.ntsb.gov/carol-main-public/landing-page
* https://data.ntsb.gov/carol-main-public/query-builder

## Features

*   **Comprehensive Search Criteria:**
    *   Date range (start and end dates).
    *   Event location (city and state).
    *   Aircraft make and model.
    *   Keyword search within accident narratives (Preliminary, Factual, and Analysis sections).
*   **Flexible Output:** Control the maximum number of results returned.
*   **Session Management:** Automatically creates and uses NTSB API sessions.
*   **Structured Data:** Returns results in a clear JSON format.
*   **Input Validation:** Basic validation for search parameters like date formats and state names.
*   **CrewAI Compatible:** Designed as a `BaseTool` for easy use with CrewAI agents.

## Requirements

*   Python 3.13+
*   `httpx` - For making asynchronous HTTP requests to the NTSB API.
*   `crewai` - The base framework if used with AI agents.
*   `pydantic` - For data validation and modeling of search parameters.

## Installation

1.  Ensure Python 3.13+ is installed.
2.  After cloning or downloading the code, install the package with:
    ```bash
    pip install .
    ```

## Usage

The primary component is the `NTSBSearchTool` class found in `ntsb_query.query`.

### Standalone Usage Example

```python
from ntsb_query.query import NTSBSearchTool

# Initialize the tool (this will also create an NTSB API session)
ntsb_tool = NTSBSearchTool()

# --- Example 1: Search by location and date ---
print("--- Running Example 1 ---")
results_loc_date = ntsb_tool._run(
    start_date="01/01/2023",
    end_date="03/31/2023",
    city="Dallas",
    state="Texas",
    max_results=3
)
print(results_loc_date)
print("\n-------------------------\n")

# --- Example 2: Search by narrative keywords ---
print("--- Running Example 2 ---")
results_narrative = ntsb_tool._run(
    start_date="01/01/2022",
    end_date="12/31/2022",
    narrative_keywords="engine failure, runway", # Comma-separated, implies AND between "engine failure" and "runway"
    max_results=2
)
print(results_narrative)
print("\n-------------------------\n")

# --- Example 3: Search by aircraft make and model ---
print("--- Running Example 3 ---")
results_aircraft = ntsb_tool._run(
    aircraft_make="Cessna",
    aircraft_model="172",
    start_date="06/01/2023",
    end_date="06/30/2023",
    max_results=2
)
print(results_aircraft)
print("\n-------------------------\n")

# --- Example 4: Invalid input (e.g., bad date format) ---
print("--- Running Example 4 ---")
results_error = ntsb_tool._run(
    start_date="2023-01-01" # Incorrect format
)
print(results_error)
print("\n-------------------------\n")
```

### Input Parameters (`NTSBSearchModel`)

The `_run` method accepts keyword arguments that correspond to the fields in the `NTSBSearchModel`:

*   `start_date` (Optional[str]): Start date for the search period (format: MM/DD/YYYY). Example: `"01/01/2020"`.
*   `end_date` (Optional[str]): End date for the search period (format: MM/DD/YYYY). Example: `"12/31/2023"`.
*   `city` (Optional[str]): City where the event occurred. Example: `"Dallas"`.
*   `state` (Optional[str]): Full state name where the event occurred. Example: `"California"`.
*   `narrative_keywords` (Optional[str]): Comma-separated keywords to search within event narratives. Each distinct keyword phrase is searched across Preliminary, Factual, and Analysis narratives (using OR logic within the narrative types for a single keyword phrase). Multiple comma-separated keyword phrases are combined with AND logic (each phrase must be found). Example: `"engine failure, stall"`.
*   `aircraft_make` (Optional[str]): Manufacturer of the aircraft. Example: `"Boeing"`.
*   `aircraft_model` (Optional[str]): Model of the aircraft. Example: `"737"`.
*   `max_results` (int): Maximum number of results to display. Defaults to `10`. The NTSB API might cap the number of results per request (e.g., at 50).

### Output Format

The tool returns a string.
*   **On success with results:**
    ```
    Found {total_count} total results. Displaying {displayed_count}: [
      {
        "NTSBEntryId": "...", // Unique NTSB Entry ID
        "Mode": "Aviation",
        "EventDate": "YYYY-MM-DDTHH:MM:SS", // ISO format
        "City": "...",
        "State": "...", // Full state name
        "NtsbNo": "...", // NTSB Number
        // ... other relevant fields extracted from the API response
      },
      // ... more records
    ]
    ```
*   **On success with no results:**
    ```
    No results found. (Total count reported by API: {count})
    ```
*   **On error (e.g., input validation, API error):**
    ```
    Error: {description of the error}.
    ```
    Example: `Error: Invalid start_date format. Please use MM/DD/YYYY.` or `Error: API request failed with status 500. Response: ...`

## Testing

If tests are available (e.g., in a `tests` directory using `pytest`):

1.  Install `pytest`:
    ```bash
    pip install .[dev]
    ```
2.  Navigate to the project's root directory and run:
    ```bash
    pytest
    ```

## How it Works

The `NTSBSearchTool` performs the following steps:
1.  **Initialization (`__init__`):** Creates a session with the NTSB API by calling `_create_session`. The session ID is stored.
2.  **Execution (`_run`):**
    *   Validates input arguments using the `NTSBSearchModel`.
    *   Calls `_build_query_groups` to construct the query payload based on the provided parameters. This method handles the logic for date formatting, state abbreviation, and structuring rules for different criteria.
    *   Sends the formatted query to the NTSB API's `Query/Main` endpoint.
    *   Calls `_compose_output` to parse the API's JSON response and format it into the final output string.
    *   Handles potential errors from API requests or JSON parsing.

Internal helper methods:
*   `_create_query_rule`: Constructs individual rule objects for the API query.
*   `_narrative_groups`: Specifically builds query groups for `narrative_keywords`.
*   `_build_query_groups`: Aggregates all rules into the final query group structure.
*   `_compose_output`: Formats the raw API response into a user-friendly string.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Create a new Pull Request.

## License

[LICENSE](LICENSE)
