import json 


def serialize_json(data:dict|list):
    if data:
        return json.dumps(data, default=str).encode("utf-8")
def deserialize_json(data):
    if data:
        return json.loads(data.decode("utf-8"))
