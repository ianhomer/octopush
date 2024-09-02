import argparse
import requests
import sys
import pandas
from datetime import datetime
import os

parser = argparse.ArgumentParser(description="octopush")
parser.add_argument("--mpan", help="Specify MPAN")
parser.add_argument(
    "--get-meter-point", help="Get meter point", action="store_true"
)
parser.add_argument("--list-products", help="List products", action="store_true")

OCTOPUS_MPAN_NAME = "OCTOPUS_MPAN"


def main():
    args = parser.parse_args()
    do(args)


def do(args):
    if args.list_products:
        list_products()
    elif args.get_meter_point:
        get_meter_point(args)
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


def get_meter_point(args):
    try:
        mpan = args.mpan or os.environ[OCTOPUS_MPAN_NAME]
    except KeyError:
        print(
            "Please set mpan with argument --mpan "
            + f"or environment variable {OCTOPUS_MPAN_NAME}\n"
        )
        raise Exception("mpan not specified")
    url = f"https://api.octopus.energy/v1/electricity-meter-points/{mpan}/"
    response = requests.get(url=url)
    json = response.json()
    print(json)


main()
