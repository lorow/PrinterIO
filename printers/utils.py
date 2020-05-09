import requests


def validate_build_volume(build_volume, printer_type="CR"):

    if not build_volume:
        raise ValueError("No build volume has been provided")

    axis = build_volume.split("x")

    num_of_dimensions = {
        "CR": 3,
        "DL": 2,
        "RS": 3,
    }

    if printer_type not in num_of_dimensions:
        raise ValueError("Given printer type is not supported")

    if len(axis) != num_of_dimensions[printer_type]:
        return False

    try:
        for dimension in axis:
            int(dimension)
    except ValueError:
        return False

    return True


def issue_command_to_printer(
    printer_ip, printer_port, endpoint, api_key, json, custom_headers=None
):

    return requests.post(
        url="http://{ip}:{port}{endpoint}".format(
            ip=printer_ip, port=printer_port, endpoint=endpoint
        ),
        headers=custom_headers
        or {"X-Api-Key": api_key, "Content-Type": "application/json"},
        json=json,
    )
