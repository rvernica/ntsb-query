Filter group 1: Event date is on or after "01/01/2020" and Event date is on or before "01/01/2025" and Investigation mode is "Aviation" and City is "San Jose" and State is "California"
```
curl --location 'https://data.ntsb.gov/carol-main-public/api/Query/Main' \
--data '{
    "ResultSetSize": 50,
    "ResultSetOffset": 0,
    "QueryGroups": [
        {
            "QueryRules": [
                {
                    "RuleType": "Simple",
                    "Values": [
                        "Aviation"
                    ],
                    "Columns": [
                        "Event.Mode"
                    ],
                    "Operator": "is",
                    "overrideColumn": "",
                    "selectedOption": {
                        "FieldName": "Mode",
                        "DisplayText": "Investigation mode",
                        "Columns": [
                            "Event.Mode"
                        ],
                        "Selectable": true,
                        "InputType": "Text",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": true
                    }
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "2020-01-01"
                    ],
                    "Columns": [
                        "Event.EventDate"
                    ],
                    "Operator": "is on or after",
                    "selectedOption": {
                        "FieldName": "EventDate",
                        "DisplayText": "Event date",
                        "Columns": [
                            "Event.EventDate"
                        ],
                        "Selectable": true,
                        "InputType": "Date",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": true
                    },
                    "overrideColumn": ""
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "2025-01-01"
                    ],
                    "Columns": [
                        "Event.EventDate"
                    ],
                    "Operator": "is on or before",
                    "selectedOption": {
                        "FieldName": "EventDate",
                        "DisplayText": "Event date",
                        "Columns": [
                            "Event.EventDate"
                        ],
                        "Selectable": true,
                        "InputType": "Date",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": true
                    },
                    "overrideColumn": ""
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "CA"
                    ],
                    "Columns": [
                        "Event.State"
                    ],
                    "Operator": "is",
                    "selectedOption": {
                        "FieldName": "State",
                        "DisplayText": "State",
                        "Columns": [
                            "Event.State"
                        ],
                        "Selectable": true,
                        "InputType": "Dropdown",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": true
                    },
                    "overrideColumn": ""
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "San Jose"
                    ],
                    "Columns": [
                        "Event.City"
                    ],
                    "Operator": "is",
                    "selectedOption": {
                        "FieldName": "City",
                        "DisplayText": "City",
                        "Columns": [
                            "Event.City"
                        ],
                        "Selectable": true,
                        "InputType": "Text",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": true
                    },
                    "overrideColumn": ""
                }
            ],
            "AndOr": "and",
            "inLastSearch": false,
            "editedSinceLastSearch": false
        }
    ],
    "AndOr": "and",
    "SortColumn": null,
    "SortDescending": true,
    "TargetCollection": "cases",
    "SessionId": 185475
}'
```
Response:
```
{
    "Results": [
        {
            "Fields": [
                {
                    "FieldName": "NtsbNo",
                    "ExportName": "NtsbNo",
                    "Values": [
                        "WPR23LA116"
                    ]
                },
                {
                    "FieldName": "CompletionStatus",
                    "ExportName": null,
                    "Values": [
                        "Completed"
                    ]
                },
                {
                    "FieldName": "EventType",
                    "ExportName": "EventType",
                    "Values": [
                        "Accident"
                    ]
                },
                {
                    "FieldName": "Mkey",
                    "ExportName": "Mkey",
                    "Values": [
                        "106827"
                    ]
                },
                {
                    "FieldName": "IsStudy",
                    "ExportName": null,
                    "Values": [
                        "false"
                    ]
                },
                {
                    "FieldName": "EventDate",
                    "ExportName": "EventDate",
                    "Values": [
                        "2023-02-20T16:25:00Z"
                    ]
                },
                {
                    "FieldName": "City",
                    "ExportName": "City",
                    "Values": [
                        "San Jose"
                    ]
                },
                {
                    "FieldName": "State",
                    "ExportName": "State",
                    "Values": [
                        "California"
                    ]
                },
                {
                    "FieldName": "Country",
                    "ExportName": "Country",
                    "Values": [
                        "United States"
                    ]
                },
                {
                    "FieldName": "ReportNo",
                    "ExportName": "ReportNo",
                    "Values": []
                },
                {
                    "FieldName": "N#",
                    "ExportName": null,
                    "Values": [
                        "N9267P"
                    ]
                },
                {
                    "FieldName": "VehicleMake",
                    "ExportName": null,
                    "Values": [
                        "Piper"
                    ]
                },
                {
                    "FieldName": "VehicleModel",
                    "ExportName": null,
                    "Values": [
                        "PA-24-260"
                    ]
                },
                {
                    "FieldName": "HighestInjuryLevel",
                    "ExportName": null,
                    "Values": [
                        "None"
                    ]
                },
                {
                    "FieldName": "InjuryOngroundCount",
                    "ExportName": null,
                    "Values": []
                },
                {
                    "FieldName": "InjuryOnboardCount",
                    "ExportName": null,
                    "Values": [
                        "0"
                    ]
                },
                {
                    "FieldName": "HasSafetyRec",
                    "ExportName": "HasSafetyRec",
                    "Values": [
                        "false"
                    ]
                },
                {
                    "FieldName": "Mode",
                    "ExportName": "Mode",
                    "Values": [
                        "Aviation"
                    ]
                },
                {
                    "FieldName": "ReportNumber",
                    "ExportName": null,
                    "Values": []
                },
                {
                    "FieldName": "ReportType",
                    "ExportName": "ReportType",
                    "Values": [
                        "DirectorBrief"
                    ]
                },
                {
                    "FieldName": "DocketPublishDate",
                    "ExportName": null,
                    "Values": [
                        "2024-06-20T17:00:00Z"
                    ]
                },
                {
                    "FieldName": "OriginalPublishedDate",
                    "ExportName": null,
                    "Values": [
                        "2024-06-20T04:00:00Z"
                    ]
                },
                {
                    "FieldName": "ReportDate",
                    "ExportName": null,
                    "Values": [
                        "2023-03-13T22:24:37.44Z"
                    ]
                },
                {
                    "FieldName": "MostRecentReportType",
                    "ExportName": null,
                    "Values": [
                        "Final"
                    ]
                },
                {
                    "FieldName": "EV_ID",
                    "ExportName": null,
                    "Values": []
                },
                {
                    "FieldName": "RepGenFlag",
                    "ExportName": null,
                    "Values": []
                }
            ],
            "EntryId": "68428d99c0451aad599bfa5d"
        }
    ],
    "Columns": [
        "NtsbNo",
        "CompletionStatus",
        "EventType",
        "Mkey",
        "IsStudy",
        "EventDate",
        "City",
        "State",
        "Country",
        "ReportNo",
        "N#",
        "VehicleMake",
        "VehicleModel",
        "HighestInjuryLevel",
        "InjuryOngroundCount",
        "InjuryOnboardCount",
        "HasSafetyRec",
        "Mode",
        "ReportNumber",
        "ReportType",
        "DocketPublishDate",
        "OriginalPublishedDate",
        "ReportDate",
        "MostRecentReportType",
        "EV_ID",
        "RepGenFlag"
    ],
    "ResultListCount": 5,
    "MaxResultCountReached": false
}
```