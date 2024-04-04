from datetime import datetime

from ocui.oci.serialization import DATETIME_FORMAT_STRING


def parse_list_of_strings(string: str | list[str], separator=" ") -> list[str]:
    if string:
        if type(string) is list:
            return string
        else:
            return string.split(separator)
    else:
        return []


def parse_datetime(dtime: str) -> datetime:
    return datetime.strptime(dtime, DATETIME_FORMAT_STRING)
