from itertools import chain
import requests


def flatten_list(list_to_flatten):
    return list(chain.from_iterable(list_to_flatten))


def validate_build_volume(build_volume):

    if not build_volume:
        raise ValueError("No build volume has been provided")

    axis = build_volume.split('x')

    if len(axis) != 3:
        return False

    try:
        for dimension in axis:
            int(dimension)
    except ValueError:
        return False

    return True


def issue_command_to_printer(printer_ip, printer_port, endpoint, api_key, json, custom_headers=None):

    return requests.post(
        url="http://{ip}:{port}{endpoint}".format(
            ip=printer_ip,
            port=printer_port,
            endpoint=endpoint
        ),
        headers=custom_headers or {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        },
        json=json
    )
