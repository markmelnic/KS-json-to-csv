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
    with open("out.csv", "w", newline="") as out_csv:
        wr = csv.writer(out_csv)
        wr.writerow(FIRST_ROW)
        for entry in os.scandir("./"):
            if ".json" in entry.name:
                with open(entry.name) as json_file:
                    data = json.load(json_file)
                # print(data)

                for pload in gen_payload(data):
                    print(pload)
                    wr.writerow(pload)
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
    for rec in data["Defendants"]:
        # name
        name = rec["Name"]
        # ssn
        try:
            ssn = rec["SSn"]
        except KeyError:
            ssn = ""
        # dob
        try:
            dob = rec["Dob"]
        except KeyError:
            dob = ""
        # drivers license
        try:
            dl = rec["DriversLicense"]
        except KeyError:
            dl = ""
        # address
        address = rec["FullAddress"]
        # unit
        try:
            unit = rec["Unit"]
        except KeyError:
            unit = ""
        # city
        city = rec["City"]
        # state
        state = rec["State"]
        # zip code
        zipc = rec["ZipCode"]
        # name skip
        try:
            name_skip = rec["NameSkip"]
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
    plas = []
    for rec in data["Plaintiffs"]:
        # name information
        try:
            name_info = rec["NameInfo"]
        except KeyError:
            name_info = ""
        # name
        name = rec["Name"]
        # ssn
        try:
            care_of_name = rec["InCareOfName"]
        except KeyError:
            care_of_name = ""
        # address
        address = rec["FullAddress"]
        # city
        city = rec["City"]
        # state
        state = rec["State"]
        # zip code
        zipc = rec["ZipCode"]
        # phone number
        try:
            phone = rec["Phone"]
        except KeyError:
            phone = ""
        # county
        try:
            county = rec["Phone"]
        except KeyError:
            county = ""

        plas.append(
            [name_info, name, care_of_name, address, city, state, zipc, phone, county]
        )

    for d in defs:
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
        ]
        for item in d:
            payload.append(item)
        for item in plas[0]:
            payload.append(item)
        yield payload


if __name__ == "__main__":
    main()
