"""
file_name = process_help_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to handle help requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=line-too-long
from typing import Optional

commands = {
    "createEvent": {
        "Description": "Creates an event based on parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "eventForm": {
                "ReccuranceId": "an optional field, integer type",
                "Name": "a required feild, string type",
                "StartDate": "a required field, date type",
                "EndDate": "a required field, date type",
                "Type": "a required field, string type",
                "Location": "a required field, string type",
                "Description": "an optional field, string type",
                "RecurranceType": "an optional field, string type. Options: daily, weekly, monthly, yearly or some form of sun/m/t/w/th/f/sat",
            },
        },
    },
    "getEvent": {
        "Description": "Gets event based on a series of parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "defaultForm": {
                "defaultOption": "a required field, stirng type. Options: today, week, month"
            },
            "filterForm": {
                "EventIds": "an optional field, list of integers",
                "RecurranceIds": "an optional field, list of integers",
                "Name": "an optional field, string type",
                "NameExact": "an optional field, bool type",
                "StartDate": "an optional field, date type",
                "EndDate": "an optional field, date type",
                "DateFrom": "an optional field,  date type",
                "DateTo": "an optional field, date type",
                "Type": "an optional field, string type",
                "Description": "an optional field, string type",
            },
        },
        "AdditionalInformation": "DdefaultForm and filterForm are optional. Defaults to get all events.",
    },
    "updateEvent": {
        "Description": "Updates an event[s] based on a series of parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "filterForm": {
                "EventId": "a required field (either eventId or recurranceId), an integer type",
                "RecurranceId": "a required field (either eventId or recurranceId), an integer type",
                "updateDictionary": {
                    "Name": "an optional field, string type",
                    "StartDate": "an optional field, date type",
                    "EndDate": "an optional field,, date type",
                    "Type": "an optional field, string type",
                    "Description": "an optional field, string type",
                },
            },
        },
    },
    "deleteEvent": {
        "Description": "Deletes an event[s] based on a series of parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "deleteForm": {
                "EventIds": "an optional field, list of integers",
                "RecurranceIds": "an optional field, list of integers",
                "Name": "an optional field, string type",
                "NameExact": "an optional field, bool type",
                "StartDate": "an optional field, date type",
                "EndDate": "an optional field, date type",
                "DateFrom": "an optional field,  date type",
                "DateTo": "an optional field, date type",
                "Type": "an optional field, string type",
                "Description": "an optional field, string type",
            },
        },
    },
    "getCurrentWeather": {
        "Description": "Gets today's weather",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
        },
    },
    "getGmailEmails": {
        "Description": "Gets gmail email snippets based on a series of paremeters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "authorizationFlle": {
                "token": "",
                "refresh_token": "",
                "token_uri": "",
                "client_id": "",
                "client_secret": "",
                "scopes": ["", ""],
                "expiry": "",
            },
            "labelFilters": "an optional parameter, a list of strings",
            "maxResults": "an optional parameter, integer type",
        },
    },
    "getTranslation": {
        "Description": "Translates a piece of text based on a series of parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "translationForm": {
                "text": "a required parameter, string type",
                "source": "an optional parameter, string type",
                "target": "an optional parameter, string type",
            },
        },
    },
}


def get_command(command: Optional[str]) -> dict:
    """
    Returns information about a command.

    This function takes a string `command` and returns a dictionary containing information about the specified command.
    If `command` is not provided or is not a recognized command, the function returns an empty dictionary.

    Args:
        command: A string representing the command to retrieve information about.

    Returns:
        A dictionary containing information about the specified command.
    """

    if command:
        if command in commands:
            return commands[command]
        return {}

    return commands
