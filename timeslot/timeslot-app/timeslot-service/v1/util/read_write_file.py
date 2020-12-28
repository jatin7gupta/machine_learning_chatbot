import json
def write_to_file(file, content):
    with open(file, "w+") as s:
        s.write(json.dumps(content))


def read_from_file(file):
    with open(file, "r") as s:
        return json.loads(s.read())
