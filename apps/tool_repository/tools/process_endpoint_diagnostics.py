"""
file_name = process_endpoint_diagnostics.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to commit endpoint diagnostics and process
             endpoint diagnostic get requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from typing import Dict, List, Optional, Union

from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_endpoint_diagnostics,
    commit_endpoint_diagnostics,
    diagnostics_type_list_to_diagnostic_dict_list,
)
from repository.models.endpoint_diagnostics_model import (
    EndpointDiagnostics,
)
from repository.endpoint_diagnostics import (
    EndpointDiagnosticsRepository,
)
from apps.tool_repository.tools.event_utils import string_to_date


def process_commit_diagnostics(
    diagnostic_id: Optional[int], endpoint_info: Dict[str, str]
) -> int:
    """
    Commits endpoint diagnostics to the database.

    This function takes optional diagnostic ID and endpoint info as input.
    If a diagnostic ID is not provided, the function creates a new diagnostic entry.
    If a diagnostic ID is provided, the function updates the existing diagnostic entry with the
    corresponding response and error.
    The diagnostic info is passed in a dictionary containing an endpoint name, request data,
    response data, and error data.

    Args:
        diagnostic_id: An optional integer representing the diagnostic ID to be updated.
        endpoint_info: A dictionary containing diagnostic information for the endpoint.

    Returns:
        The diagnostic_id of the request and endpoint.
    """

    if diagnostic_id is None:
        return setup_endpoint_diagnostics(
            endpoint=endpoint_info["Endpoint"], request=endpoint_info["Request"]
        )

    commit_endpoint_diagnostics(
        diagnostic_id=diagnostic_id,
        response=endpoint_info["Response"],
        error=endpoint_info["Error"],
    )

    return diagnostic_id


def process_get_diagnostics(
    diagnostic_filter_form: Dict[str, str]
) -> List[Dict[str, Union[str, int, float]]]:
    """
    Processes a request to retrieve endpoint diagnostics.

    This function takes a dictionary representing filter data from a request and uses the data
    to retrieve endpoint diagnostics from the EndpointDiagnosticsRepository.
    The filter can be used to query diagnostics by date range or endpoint name.

    Args:
        diagnostic_filter_form: A dictionary representing the filter data from a request.
        The optional fields are "Endpoint", "EndpointCounter", "DateFrom", and "DateTo".

    Returns:
        A list of dictionaries representing the retrieved endpoint diagnostics.
        Each dictionary contains the fields "DiagnosticId", "Endpoint", "Request", "Response",
        "Error", and "Datetime".
    """

    diagnostic_filter_form["DateFrom"] = string_to_date(
        diagnostic_filter_form["DateFrom"]
    )
    diagnostic_filter_form["DateTo"] = string_to_date(diagnostic_filter_form["DateTo"])

    endpoint_diagnostics: List[
        EndpointDiagnostics
    ] = EndpointDiagnosticsRepository().get(filters=diagnostic_filter_form)

    return diagnostics_type_list_to_diagnostic_dict_list(
        diagnostic_list=endpoint_diagnostics,
        endpoint_counter=diagnostic_filter_form.get("EndpointCounter"),
    )
