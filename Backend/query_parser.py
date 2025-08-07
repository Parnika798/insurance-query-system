import re

def parse_query(query):
    try:
        # Extract policyholder's name
        name = re.search(r"(?:for|of) ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", query)
        name = name.group(1) if name else None

        # Extract date
        date = re.search(r"(?:on|dated) (\d{1,2}[a-z]{2}? \w+ \d{4})", query)
        date = date.group(1) if date else None

        # Extract hospital
        hospital = re.search(r"at ([A-Z][\w\s]+? Hospital)", query)
        hospital = hospital.group(1) if hospital else None

        # Extract location (improved for multi-word cities)
        location = re.search(r"in ([A-Z][a-z]+(?: [A-Z][a-z]+)*)", query)
        location = location.group(1) if location else None

        # Extract procedure (expanded patterns)
        procedure = re.search(r"(?:had|underwent|received) (?:a |an )?([\w\s]+?) (?:procedure|surgery|treatment)", query)
        procedure = procedure.group(1) if procedure else None

        return {
            "name": name,
            "date": date,
            "hospital": hospital,
            "location": location,
            "procedure": procedure
        }
    except Exception as e:
        print(f"Failed to parse query: {e}")
        return {
            "name": None,
            "date": None,
            "hospital": None,
            "location": None,
            "procedure": None
        }
