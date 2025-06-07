"""
Provides tools for querying the NTSB CAROL (Case Analysis and Reporting Online) database.

This module defines the data model for search parameters (`NTSBSearchModel`) and
the main tool class (`NTSBSearchTool`) for interacting with the NTSB API.
"""

import datetime
import json
from typing import Any, Dict, Generator, List, Optional, Type

import httpx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# Define the input schema for the tool
class NTSBSearchModel(BaseModel):
    """
    Input model for the NTSB Search Tool.

    Defines the available search criteria for querying the NTSB database.
    """

    start_date: Optional[str] = Field(
        None, description="Start date for search (MM/DD/YYYY). e.g., '01/01/2020'"
    )
    end_date: Optional[str] = Field(
        None, description="End date for search (MM/DD/YYYY). e.g., '12/31/2023'"
    )
    city: Optional[str] = Field(None, description="City of the event. e.g., 'Dallas'")
    state: Optional[str] = Field(
        None, description="State of the event (full name). e.g., 'California'"
    )
    narrative_keywords: Optional[str] = Field(
        None,
        description=(
            "Comma-separated keywords to search in narratives. Each keyword is "
            "searched across Preliminary, Factual, and Analysis narratives (OR logic). "
            "Multiple distinct keywords are combined with AND logic. "
            "e.g., 'engine failure,fire'"
        ),
    )
    aircraft_make: Optional[str] = Field(
        None, description="Aircraft manufacturer. e.g., 'Boeing'"
    )
    aircraft_model: Optional[str] = Field(
        None, description="Aircraft model. e.g., '737'"
    )
    max_results: int = Field(
        default=10,
        description=(
            "Maximum number of results to return. Default is 10. "
            "The API might cap results (e.g., at 50)."
        ),
    )


# Define the custom tool
class NTSBSearchTool(BaseTool):
    """
    A tool to query the NTSB (National Transportation Safety Board) CAROL API
    for accident and incident records.

    It allows searching based on various criteria such as date range, location,
    investigation mode, aircraft details, and narrative keywords.
    The tool handles session creation with the API and formats the query
    according to the API's requirements.
    """

    API_BASE: str = "https://data.ntsb.gov/carol-main-public/api"
    QUERY_URL: str = API_BASE + "/Query/Main"
    SESSION_URL: str = API_BASE + "/Session/CreateSession"

    STATE_ABBREVIATIONS: Dict[str, str] = {
        "alabama": "AL",
        "alaska": "AK",
        "arizona": "AZ",
        "arkansas": "AR",
        "california": "CA",
        "colorado": "CO",
        "connecticut": "CT",
        "delaware": "DE",
        "florida": "FL",
        "georgia": "GA",
        "hawaii": "HI",
        "idaho": "ID",
        "illinois": "IL",
        "indiana": "IN",
        "iowa": "IA",
        "kansas": "KS",
        "kentucky": "KY",
        "louisiana": "LA",
        "maine": "ME",
        "maryland": "MD",
        "massachusetts": "MA",
        "michigan": "MI",
        "minnesota": "MN",
        "mississippi": "MS",
        "missouri": "MO",
        "montana": "MT",
        "nebraska": "NE",
        "nevada": "NV",
        "new hampshire": "NH",
        "new jersey": "NJ",
        "new mexico": "NM",
        "new york": "NY",
        "north carolina": "NC",
        "north dakota": "ND",
        "ohio": "OH",
        "oklahoma": "OK",
        "oregon": "OR",
        "pennsylvania": "PA",
        "rhode island": "RI",
        "south carolina": "SC",
        "south dakota": "SD",
        "tennessee": "TN",
        "texas": "TX",
        "utah": "UT",
        "vermont": "VT",
        "virginia": "VA",
        "washington": "WA",
        "west virginia": "WV",
        "wisconsin": "WI",
        "wyoming": "WY",
        "district of columbia": "DC",
        "puerto rico": "PR",
    }
    SELECTED_OPTION_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "Event.Mode": {
            "FieldName": "Mode",
            "DisplayText": "Investigation mode",
            "InputType": "Text",
            "UnderDevelopment": True,
        },
        "Event.EventDate": {
            "FieldName": "EventDate",
            "DisplayText": "Event date",
            "InputType": "Date",
            "UnderDevelopment": True,
        },
        "Event.State": {
            "FieldName": "State",
            "DisplayText": "State",
            "InputType": "Dropdown",
            "UnderDevelopment": True,
        },
        "Event.City": {
            "FieldName": "City",
            "DisplayText": "City",
            "InputType": "Text",
            "UnderDevelopment": True,
        },
        "Narrative.Prelim": {
            "FieldName": "AviationPrelim",
            "DisplayText": "Preliminary narrative",
            "InputType": "Text",
            "UnderDevelopment": False,
        },
        "Narrative.Factual": {
            "FieldName": "AviationFactual",
            "DisplayText": "Factual narrative",
            "InputType": "Text",
            "UnderDevelopment": False,
        },
        "Narrative.Analysis": {
            "FieldName": "AviationAnalysis",
            "DisplayText": "Analysis narrative",
            "InputType": "Text",
            "UnderDevelopment": False,
        },
        "Event.VehicleMake": {
            "FieldName": "VehicleMake",
            "DisplayText": "Aircraft Make",
            "InputType": "Text",
            "UnderDevelopment": False,
        },
        "Event.VehicleModel": {
            "FieldName": "VehicleModel",
            "DisplayText": "Aircraft Model",
            "InputType": "Text",
            "UnderDevelopment": False,
        },
    }

    name: str = "NTSB Accident Search Tool"
    description: str = (
        "Queries the NTSB CAROL database for accident records. Searches by date "
        "range, location, investigation mode, aircraft details, and narrative "
        "keywords. Returns a summary of findings and a list of matching "
        "accident records in JSON format."
    )
    args_schema: Type[BaseModel] = NTSBSearchModel
    session_id: Optional[str] = None  # Instance variable for session ID

    def __init__(self, **kwargs: Any):
        """
        Initializes the NTSBSearchTool.

        Calls the parent BaseTool's initializer and then creates a session
        with the NTSB API.
        """
        super().__init__(**kwargs)  # Call BaseTool's __init__
        self._create_session()

    def _create_session(self):
        """
        Creates a new session with the NTSB CAROL API.

        Stores the session ID in `self.session_id`. If session creation fails,
        `self.session_id` will be None.
        """
        try:
            response = httpx.post(self.SESSION_URL, timeout=10)
            response.raise_for_status()
            self.session_id = response.text
            # Optional: for logging/debugging
            print(f"NTSB API Session created: {self.session_id}")
        except httpx.RequestError as e:
            self.session_id = None  # Ensure session_id is None on failure
            # Optional: for logging/debugging
            print(f"Error creating NTSB API session: {e}")
            # Depending on desired behavior, you might want to raise an exception here
            # or handle it more gracefully in _run.

    def _create_query_rule(
        self, columns_list: List[str], operator: str, rule_values: List[str]
    ) -> Dict[str, Any]:
        """
        Constructs a single query rule dictionary for the NTSB API.

        Args:
            columns_list: A list of column names (usually one) for the rule.
            operator: The operator for the rule (e.g., "is", "contains").
            rule_values: A list of values for the rule.

        Returns:
            A dictionary representing the query rule.
        """
        column_key = columns_list[0]
        template = self.SELECTED_OPTION_TEMPLATES.get(column_key)

        if not template:
            # This case should ideally be avoided by having all queryable fields in templates
            print(
                f"Warning: Using generic selectedOption for {column_key}. "
                "API compatibility not guaranteed."
            )
            selected_option_details = {
                "FieldName": column_key.split(".")[-1],
                "DisplayText": column_key.replace(".", " "),
                "InputType": "Text",
                "UnderDevelopment": False,
            }
        else:
            selected_option_details = template

        selected_option = {
            "FieldName": selected_option_details["FieldName"],
            "DisplayText": selected_option_details["DisplayText"],
            "Columns": columns_list,
            "Selectable": True,
            "InputType": selected_option_details["InputType"],
            "RuleType": 0,
            "Options": None,
            "TargetCollection": "cases",
            "UnderDevelopment": selected_option_details["UnderDevelopment"],
        }

        return {
            "RuleType": "Simple",
            "Values": rule_values,
            "Columns": columns_list,
            "Operator": operator,
            "overrideColumn": "",
            "selectedOption": selected_option,
        }

    def _narrative_groups(
        self, params: NTSBSearchModel
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Constructs query groups for narrative keywords.

        Each keyword in the narrative_keywords field forms its own OR-group.
        If multiple keywords are provided, they are combined with AND logic.

        Args:
            params: The search parameters model.

        Yields:
            group dictionaries for each keyword in the narrative_keywords field.
        """
        keywords = [
            kw.strip() for kw in str(params.narrative_keywords).split(",") if kw.strip()
        ]
        for keyword in keywords:  # Renamed 'keyword_item' to 'keyword'
            # Renamed 'narrative_keyword_rules' to 'narrative_rules'
            narrative_rules = [
                self._create_query_rule(["Narrative.Prelim"], "contains", [keyword]),
                self._create_query_rule(["Narrative.Factual"], "contains", [keyword]),
                self._create_query_rule(["Narrative.Analysis"], "contains", [keyword]),
            ]
            yield {
                "QueryRules": narrative_rules,
                "AndOr": "or",
                "inLastSearch": False,
                "editedSinceLastSearch": False,
            }

    def _build_query_groups(self, params: NTSBSearchModel) -> List[Dict[str, Any]]:
        """
        Constructs the list of query groups for the NTSB API query.

        Args:
            params: The search parameters model.

        Returns:
            A list of query group dictionaries.

        Raises:
            ValueError: If date formats are invalid or state name is invalid,
                        preventing query group construction.
        """
        query_groups: List[Dict[str, Any]] = []
        main_filter_rules: List[Dict[str, Any]] = [
            self._create_query_rule(["Event.Mode"], "is", ["Aviation"])
        ]

        # Date rules
        if params.start_date:
            try:
                dt_start = datetime.datetime.strptime(params.start_date, "%m/%d/%Y")
                main_filter_rules.append(
                    self._create_query_rule(
                        ["Event.EventDate"],
                        "is on or after",
                        [dt_start.strftime("%Y-%m-%d")],
                    )
                )
            except ValueError as exc:
                # Raise an exception instead of returning a string
                raise ValueError(
                    "Error: Invalid start_date format. Please use MM/DD/YYYY."
                ) from exc

        if params.end_date:
            try:
                dt_end = datetime.datetime.strptime(params.end_date, "%m/%d/%Y")
                main_filter_rules.append(
                    self._create_query_rule(
                        ["Event.EventDate"],
                        "is on or before",
                        [dt_end.strftime("%Y-%m-%d")],
                    )
                )
            except ValueError as exc:  # pylint: disable=raise-missing-from
                # Raise an exception instead of returning a string
                raise ValueError(
                    "Error: Invalid end_date format. Please use MM/DD/YYYY."
                ) from exc

        # Configuration for simple "is" filter rules
        simple_field_configs = [
            ("city", ["Event.City"]),
            ("aircraft_make", ["Event.VehicleMake"]),
            ("aircraft_model", ["Event.VehicleModel"]),
        ]

        for param_name, api_columns in simple_field_configs:
            value = getattr(params, param_name)
            if value:
                main_filter_rules.append(
                    self._create_query_rule(api_columns, "is", [str(value)])
                )

        # State rule (special handling for abbreviation)
        if params.state:
            state_value = str(params.state)
            state_abbr = self.STATE_ABBREVIATIONS.get(state_value.lower())
            if not state_abbr:
                # Raise an exception instead of returning a string
                raise ValueError(
                    f"Error: Invalid state name '{state_value}'. "
                    "Please use a full US state name."
                )
            main_filter_rules.append(
                self._create_query_rule(["Event.State"], "is", [state_abbr])
            )

        if main_filter_rules:
            query_groups.append(
                {
                    "QueryRules": main_filter_rules,
                    "AndOr": "and",
                    "inLastSearch": False,
                    "editedSinceLastSearch": False,
                }
            )

        # Narrative keywords rules (each keyword forms its own OR-group)
        if params.narrative_keywords:
            for group in self._narrative_groups(params):
                query_groups.append(group)

        return query_groups

    def _compose_output(self, response: httpx.Response) -> str:
        """
        Composes the output string from the API response.

        Args:
            response: The HTTP response object from the NTSB API.

        Returns:
            A formatted string containing the total count, displayed count,
            and a JSON representation of the results.
        """
        try:
            api_response_json = response.json()

            results_list = api_response_json.get("Results", [])
            count = api_response_json.get("ResultListCount", 0)

            if results_list:
                simplified_results = []
                for res in results_list:
                    record: Dict[str, Any] = {
                        "NTSBEntryId": res.get("EntryId")
                    }  # Renamed for clarity
                    for field in res.get("Fields", []):
                        if field.get("Values") and len(field["Values"]) > 0:
                            record[field["FieldName"]] = (
                                field["Values"][0]
                                if len(field["Values"]) == 1
                                else field["Values"]
                            )
                    simplified_results.append(record)
                output = (
                    f"Found {count} total results. Displaying "
                    f"{len(simplified_results)}: "
                    f"{json.dumps(simplified_results, indent=2)}"
                )
            else:
                output = f"No results found. (Total count reported by API: {count})"
        except json.JSONDecodeError:
            output = (
                "Error: Could not decode JSON response from API. "
                f"Response text: {response.text()}"
            )
        return output

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """
        Executes the NTSB query with the provided parameters.

        Args:
            *args: Variable length argument list (not used by this tool).
            **kwargs: Keyword arguments matching the fields in NTSBSearchModel.

        Returns:
            A string containing either the search results in JSON format or
            an error message.
        """
        if not self.session_id:
            return "Error: NTSB API session not established. Tool cannot function."

        # If all arguments are None or empty, we cannot form a query
        if not any(kwargs.values()):
            # This handles the case where no criteria were provided that result in query rules.
            return "Error: No valid search criteria provided to form a query."

        try:
            # Pydantic validation happens here on instantiation
            params = NTSBSearchModel(**kwargs)
            # _build_query_groups can now raise ValueError for specific
            # input issues
            query_groups = self._build_query_groups(params)
        except ValueError as e:
            # Catch validation errors from _build_query_groups (e.g., bad date/state)
            # or Pydantic validation errors if they were to occur here.
            return str(e)

        payload: Dict[str, Any] = {
            "ResultSetSize": (
                min(params.max_results, 50) if params.max_results > 0 else 10
            ),
            "ResultSetOffset": 0,
            "QueryGroups": query_groups,
            "AndOr": "and",  # How different QueryGroups are combined
            "SortColumn": "Event.EventDate",  # Default sort
            "SortDescending": True,
            "TargetCollection": "cases",
            "SessionId": self.session_id,  # Use the fetched session ID
        }

        try:
            response = httpx.post(self.QUERY_URL, json=payload, timeout=30)
            # Raises HTTPStatusError for bad responses (4XX or 5XX)
            response.raise_for_status()
            output = self._compose_output(response)
        except httpx.HTTPStatusError as e:
            output = (
                f"Error: API request failed with status {e.response.status_code}. "
                f"Response: {response.text}"
            )
        except httpx.RequestError as e:  # Catches DNS, Connection, Timeout errors
            output = f"Error: API request failed. {str(e)}"

        return output
