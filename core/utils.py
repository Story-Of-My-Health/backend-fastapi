import hashlib
import json
from typing import Dict, List

import numpy as np
import pandas as pd
from constants import SAMPLE_DATA, SYMPTOMS


def generate_signature(sample):
    json_string = json.dumps(sample)
    signature = hashlib.sha256(json_string.encode()).hexdigest()
    return signature


def create_sample_data(symptoms: List[str]) -> Dict[str, int]:
    sample_data = SAMPLE_DATA.copy()
    for symptom in symptoms:
        if symptom in np.array(SYMPTOMS):
            sample_data[symptom] = 1

    return sample_data
