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


def gen_payload(data: str) -> list:
    payload = [
        date,
        case_number,
        county,
        precinct,
        disposition,
        data["DispositionDate"],
        data["DispositionAmount"],
        data["Prefix"],
        data["BaseCase"],
        data["Suffix"],
        data["Defendants"]["DefendantName"],
        data["Defendants"]["SSN"],
        data["Defendants"]["Dob"],
        data["Defendants"]["DriversLicense"],
        data["Defendants"]["DefAddress"],
        data["Defendants"]["DefUnit"],
        data["Defendants"]["DefCity"],
        data["Defendants"]["DefState"],
        data["Defendants"]["DefZip"],
        data["Defendants"]["DefendantNameSkip"],
        data["Plaintiffs"]["PltfNameInfo"],
        data["Plaintiffs"]["PltfName"],
        data["Plaintiffs"]["InCareOfName"],
        data["Plaintiffs"]["PltfAddress"],
        data["Plaintiffs"]["PltfCity"],
        data["Plaintiffs"]["PltfState"],
        data["Plaintiffs"]["PltfZip"],
        data["Plaintiffs"]["PltfPhone"],
        data["Plaintiffs"]["PltfCounty"],
        data["AttorneyName"],
        data["AttorneyPhone"],
        data["AttorneyAddress"],
        data["AttorneyCity"],
        data["AttorneyState"],
        data["AttorneyZip"],
        data["attorneycounty"],
    ]
