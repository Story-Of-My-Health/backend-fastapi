import hashlib
import json

from constants import SAMPLE_DATA


def generate_sample_signature(sample):
    json_string = json.dumps(sample)
    signature = hashlib.sha256(json_string.encode()).hexdigest()
    return signature
