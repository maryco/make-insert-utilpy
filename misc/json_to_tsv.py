import pandas as pd
import sys

"""
> pipenv run python ./json_to_tsv.py my.json
"""


def main():
    if (len(sys.argv) != 2):
        sys.exit(f"Required input json file.")

    json_file = f"{sys.argv[1]}"
    try:
        with open(json_file, "r") as fp:
            df = pd.read_json(json_file, encoding="utf-8")
    except FileNotFoundError as e:
        sys.exit(f"File not found ({json_file}).")

    df.to_csv(f"../dist/{json_file}.tsv", sep="\t")


if __name__ == "__main__":
    main()
