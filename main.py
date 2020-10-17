import os, csv, json
from settings import *

if __name__ == "__main__":
    with open("out.csv", "w") as out_csv:
        wr = csv.writer(out_csv)
        wr.writerow(FIRST_ROW)

        for entry in os.scandir("./"):
            if ".json" in entry.name:
                with open(entry.name) as json_file:
                    data = json.load(json_file)
                print(data)

                payload = gen_payload(data)
                print(payload)
                break
