import os, csv, json

FIRST_ROW = [
    "Filedate",
    "CaseNumber",
    "County",
    "Precinct",
    "Disposition",
    "DispoDate",
    "DispoAmount",
    "Prefix",
    "BaseCase",
    "Suffix",
    "DefendantName",
    "SSN",
    "Dob",
    "DriversLicense",
    "DefAddress",
    "DefUnit",
    "DefCity",
    "DefState",
    "DefZip",
    "DefendantNameSkip",
    "PltfNameInfo",
    "PltfName",
    "InCareOfName",
    "PltfAddress",
    "PltfCity",
    "PltfState",
    "PltfZip",
    "PltfPhone",
    "PltfCounty",
    "AttorneyName",
    "AttorneyPhone",
    "AttorneyAddress",
    "AttorneyCity",
    "AttorneyState",
    "AttorneyZip",
    "attorneycounty",
]


def main() -> None:
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
    # date
    date = data["FiledDate"]
    # case number
    case_number = data["CaseNumber"]
    # county
    county = data["County"]
    # precinct
    try:
        precinct = data["Precinct"]
    except KeyError:
        precinct = ""
    # disposition
    try:
        disposition = data["Disposition"]
    except KeyError:
        disposition = ""
    # disposition date
    try:
        disposition_date = data["Disposition"]
    except KeyError:
        disposition_date = ""
    # disposition amount
    try:
        disposition = data["Disposition"]
    except KeyError:
        disposition_amount = ""
    # prefix
    prefix = "-".join(case_number.split("-")[:-1]) + "-"
    for c in str(case_number.split("-")[-1]):
        if c == "0":
            prefix += "0"
        else:
            break
    # base case
    base_case = case_number.split("-")[-1]
    for c in base_case:
        if c == "0":
            base_case = base_case[1:]
        else:
            break
    # suffix
    try:
        suffix = data["Suffix"]
    except KeyError:
        suffix = ""

    # Defendants data
    defs = []
    for d in data["Defendants"]:
        # name
        name = d["Name"]
        # ssn
        try:
            ssn = d["SSn"]
        except KeyError:
            ssn = ""
        # dob
        try:
            dob = d["Dob"]
        except KeyError:
            dob = ""
        # drivers license
        try:
            dl = d["DriversLicense"]
        except KeyError:
            dl = ""
        # address
        address = d["FullAddress"]
        # unit
        try:
            unit = d["Unit"]
        except KeyError:
            unit = ""
        # city
        city = d["City"]
        # state
        state = d["State"]
        # zip code
        zipc = d["ZipCode"]
        # name skip
        try:
            name_skip = d["NameSkip"]
        except KeyError:
            name_skip = ""

        defs.append([name, ssn, dob, dl, address, unit, city, state, zipc, name_skip])
        if "-" in name:
            defs.append(
                [
                    name.split("-")[0],
                    ssn,
                    dob,
                    dl,
                    address,
                    unit,
                    city,
                    state,
                    zipc,
                    name_skip,
                ]
            )

    # Plaintiffs data

    payload = [
        date,
        case_number,
        county,
        precinct,
        disposition,
        disposition_date,
        disposition_amount,
        prefix,
        base_case,
        suffix,
        defs,
        # data["Plaintiffs"]["PltfNameInfo"],
        # data["Plaintiffs"]["PltfName"],
        # data["Plaintiffs"]["InCareOfName"],
        # data["Plaintiffs"]["PltfAddress"],
        # data["Plaintiffs"]["PltfCity"],
        # data["Plaintiffs"]["PltfState"],
        # data["Plaintiffs"]["PltfZip"],
        # data["Plaintiffs"]["PltfPhone"],
        # data["Plaintiffs"]["PltfCounty"],
        # data["AttorneyName"],
        # data["AttorneyPhone"],
        # data["AttorneyAddress"],
        # data["AttorneyCity"],
        # data["AttorneyState"],
        # data["AttorneyZip"],
        # data["attorneycounty"],
    ]
    return payload


if __name__ == "__main__":
    main()
