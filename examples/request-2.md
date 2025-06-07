
Find results that match ALL of the following groups of rules:
Filter group 1: Investigation mode is "Aviation" and Event date is on or after "01/01/2020" and Event date is on or before "01/01/2025"
Filter group 2: Preliminary narrative contains "gear" or Factual narrative contains "gear" or Analysis narrative contains "gear"
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
                        "FieldName": "Mocurl --location 'https://data.ntsb.gov/carol-main-public/api/Query/Main' \
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
                }
            ],
            "AndOr": "and",
            "inLastSearch": false,
            "editedSinceLastSearch": false
        },
        {
            "QueryRules": [
                {
                    "RuleType": "Simple",
                    "Values": [
                        "gear"
                    ],
                    "Columns": [
                        "Narrative.Prelim"
                    ],
                    "Operator": "contains",
                    "selectedOption": {
                        "FieldName": "AviationPrelim",
                        "DisplayText": "Preliminary narrative",
                        "Columns": [
                            "Narrative.Prelim"
                        ],
                        "Selectable": true,
                        "InputType": "Text",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": false
                    },
                    "overrideColumn": ""
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "gear"
                    ],
                    "Columns": [
                        "Narrative.Factual"
                    ],
                    "Operator": "contains",
                    "selectedOption": {
                        "FieldName": "AviationFactual",
                        "DisplayText": "Factual narrative",
                        "Columns": [
                            "Narrative.Factual"
                        ],
                        "Selectable": true,
                        "InputType": "Text",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": false
                    },
                    "overrideColumn": ""
                },
                {
                    "RuleType": "Simple",
                    "Values": [
                        "gear"
                    ],
                    "Columns": [
                        "Narrative.Analysis"
                    ],
                    "Operator": "contains",
                    "selectedOption": {
                        "FieldName": "AviationAnalysis",
                        "DisplayText": "Analysis narrative",
                        "Columns": [
                            "Narrative.Analysis"
                        ],
                        "Selectable": true,
                        "InputType": "Text",
                        "RuleType": 0,
                        "Options": null,
                        "TargetCollection": "cases",
                        "UnderDevelopment": false
                    },
                    "overrideColumn": ""
                }
            ],
            "AndOr": "or",
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
                        "ERA25LA088"
                    ]
                },
                {
                    "FieldName": "CompletionStatus",
                    "ExportName": null,
                    "Values": [
                        "In work"
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
                        "199500"
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
                        "2025-01-01T03:20:00Z"
                    ]
                },
                {
                    "FieldName": "City",
                    "ExportName": "City",
                    "Values": [
                        "Naples"
                    ]
                },
                {
                    "FieldName": "State",
                    "ExportName": "State",
                    "Values": [
                        "Florida"
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
                        "N8163F"
                    ]
                },
                {
                    "FieldName": "VehicleMake",
                    "ExportName": null,
                    "Values": [
                        "Beech"
                    ]
                },
                {
                    "FieldName": "VehicleModel",
                    "ExportName": null,
                    "Values": [
                        "A36"
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
                    "Values": [
                        "0"
                    ]
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
                    "Values": []
                },
                {
                    "FieldName": "OriginalPublishedDate",
                    "ExportName": null,
                    "Values": []
                },
                {
                    "FieldName": "ReportDate",
                    "ExportName": null,
                    "Values": [
                        "2025-02-08T00:06:36.796Z"
                    ]
                },
                {
                    "FieldName": "MostRecentReportType",
                    "ExportName": null,
                    "Values": [
                        "Prelim"
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
            "EntryId": "68428d9cc0451aad599c0681"
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
    "ResultListCount": 1881,
    "MaxResultCountReached": true
}
```