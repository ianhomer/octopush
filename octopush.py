import argparse
import requests
import sys
import pandas
from datetime import datetime
import os

parser = argparse.ArgumentParser(description="octopush")
parser.add_argument("--mpan", help="Specify MPAN")
parser.add_argument("--serial-number", help="Specify meter serial number")
parser.add_argument("--get-meter-point", help="Get meter point", action="store_true")
parser.add_argument("--list-consumption", help="List consumption", action="store_true")
parser.add_argument("--list-products", help="List products", action="store_true")

OCTOPUS_MPAN_NAME = "OCTOPUS_MPAN"
OCTOPUS_SERIAL_NUMBER_NAME = "OCTOPUS_SERIAL_NUMBER"
OCTOPUS_API_KEY_NAME = "OCTOPUS_API_KEY"


def main():
    args = parser.parse_args()
    do(args)


def do(args):
    if args.list_products:
        list_products()
    elif args.get_meter_point:
        get_meter_point(args)
    elif args.list_consumption:
        list_consumption(args)
    else:
        parser.print_help()
        sys.exit(0)


def to_just_date(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
    return date.date()


def list_products():
    url = "https://api.octopus.energy/v1/products/?brand=OCTOPUS_ENERGY"
    response = requests.get(url=url)
    json = response.json()
    data = {
        "From": [to_just_date(x["available_from"]) for x in json["results"]],
        "Product": [x["display_name"] for x in json["results"]],
        "Is Green?": [x["is_green"] for x in json["results"]],
    }
    products = pandas.DataFrame(data).set_index("From").sort_index()
    print(products)


def get_mpan(args):
    try:
        return args.mpan or os.environ[OCTOPUS_MPAN_NAME]
    except KeyError:
        print(
            "Please set mpan with argument --mpan "
            + f"or environment variable {OCTOPUS_MPAN_NAME}\n"
        )
        raise Exception("mpan not specified")


def get_serial_number(args):
    try:
        return args.serial_number or os.environ[OCTOPUS_SERIAL_NUMBER_NAME]
    except KeyError:
        print(
            "Please set serial_number with argument --serial-number "
            + f"or environment variable {OCTOPUS_SERIAL_NUMBER_NAME}\n"
        )
        raise Exception("serial number not specified")


def get_api_key():
    try:
        return os.environ[OCTOPUS_API_KEY_NAME]
    except KeyError:
        print("Please set " + f"environment variable {OCTOPUS_API_KEY_NAME}\n")
        raise Exception("api key not specified")


def get_meter_point(args):
    mpan = get_mpan(args)
    url = f"https://api.octopus.energy/v1/electricity-meter-points/{mpan}/"
    response = requests.get(url=url)
    json = response.json()
    print(json)


def list_consumption(args):
    mpan = get_mpan(args)
    serial_number = get_serial_number(args)
    api_key = get_api_key()
    url = (
        "https://api.octopus.energy/v1/electricity-meter-points"
        + f"/{mpan}/meters/{serial_number}/consumption/"
    )
    response = requests.get(url=url, auth=(api_key, ""))
    json = response.json()
    interval_start = [x['interval_start'] for x in json['results']]
    consumption = [x['consumption'] for x in json['results']]
    usage = pandas.Series(consumption, index=interval_start).sort_index()
    print(usage)


main()
