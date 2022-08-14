"""
Upload bank statement to firefly

Usage:
  upload_csv.py <filepath> --source-name=<source-name>

Options:
  --source-name=<source-name>     Name of the source account in firefly-iii for transactions
"""

from configparser import ConfigParser

from docopt import docopt
from finance.client import FireflyClient, put_transaction
from finance.data import parse_hdfc_format
from tqdm import tqdm

if __name__ == "__main__":
    args = docopt(__doc__)
    config = ConfigParser()

    # HACK: Using hardcoded path for config used by firefly-cli
    config.read("/home/lepisma/.config/firefly-cli/firefly-cli.ini")
    client = FireflyClient(config["API"]["url"], config["API"]["api_token"], args["--source-name"])

    ts = parse_hdfc_format(args["<filepath>"])

    for t in tqdm(ts):
        put_transaction(client, t)
