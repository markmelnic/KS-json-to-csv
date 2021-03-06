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
                for pload in gen_payload(data):
                    wr.writerow(pload)


def gen_payload(data: str) -> list:
    # General case data
    gen_data = gen_case(data)

    # Defendants data
    defs = gen_defendants(data)

    # Plaintiffs data
    plas = gen_plaintiffs(data)

    payload = []
    for defender in defs:
        data = []
        data.extend(gen_data)
        data.extend(defender)
        data.extend(plas[0])

        payload.append(data)
    return payload


def gen_case(data: str) -> list:
    # date
    try:
        date = data["FiledDate"]
    except KeyError:
        date = ""
    # case number
    case_number = data["CaseNumber"]
    # county
    try:
        county = data["County"]
    except KeyError:
        county = ""
    # precinct
    precinct = case_number[:2]
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
        disposition_amount = data["Disposition"]
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
    return [
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


def gen_defendants(data: str) -> list:
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

        adresplit = address.split(" ")
        # unit
        unit = ""
        for el in adresplit:
            if "apt" == el.lower():
                unit = adresplit[adresplit.index(el) + 1]
                address
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

        address = address.replace(city, '').replace(state, '').replace(zipc, '').replace(',', '').replace(" apt "+str(unit), '')
        defs.append([name, ssn, dob, dl, address, unit, city, state, zipc, name_skip])
        if "-" in name:
            defs.append(
                [
                    name.split("-")[0] + "," + name.split(",")[1],
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
    return defs


def gen_plaintiffs(data: str) -> list:
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

        address = address.replace(city, '').replace(state, '').replace(zipc, '').replace(',', '')
        plas.append(
            [name_info, name, care_of_name, address, city, state, zipc, phone, county]
        )
    return plas


if __name__ == "__main__":
    main()
