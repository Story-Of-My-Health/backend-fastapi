import math
from typing import Dict, List

import numpy as np
import pandas as pd
from utils import create_sample_data, generate_signature

file_path = "data/training_data.csv"
data = pd.read_csv(file_path)
symptomes = data.columns.to_list()[:-1]
disease = data["prognosis"].unique()


class DecisionNode:
    def __init__(self, attribut, value, branche):
        self.attribut = attribut
        self.value = value
        self.branche = branche or {}

    def is_leaf(self):
        return self.value is not None


def entropie(data, attr):
    # classes = np.unique(data[attr])
    size = data[attr].size
    occurence = data[attr].value_counts()

    entropie = 0
    for value, count in occurence.items():
        # print(f"La valeur {value} apparait {count} fois")
        p = count / size
        calc = -p * math.log2(p)
        # print(f"La probabilite de {value} est {p} ==> {calc}")
        entropie += -p * math.log2(p)

    return entropie


def infogain(data, attr, entropie_start, col):
    # print(f"Calcul de l'infogain de l'attribut {col}:")

    start_size = data[attr].size
    # Sepration de l'ensemble en sous ensemble
    data_col = data[col]
    value_possible = data_col.unique()

    # tmp = Somme de S[j] / S * Entropie (S[j])
    tmp_sum = 0
    for value in value_possible:
        filtred = data[data[col] == value]
        size_data_filtred = filtred[col].size
        tmp_sum += (size_data_filtred / start_size) * entropie(filtred, attr)
        # print(f"({size_data_filtred}/{start_size}) * {entropie(filtred, attr)} = {(size_data_filtred/start_size) * entropie(filtred, attr)}")

    # IG = Infogaine de l'attribut col
    IG = entropie_start - tmp_sum
    # print(f"{entropie_start} - {tmp_sum} = {IG}")
    # print(f"Info gain de l'attribut {col} est {IG}\n\n")
    return IG


def create_branch(data, attr, node):
    columns = data.columns

    # df_dropped = data.drop(attr, axis=1)
    entropie_start = entropie(data, attr)
    # print(f"L'entropie est {entropie_start}")

    current_attr = attr
    current_IG = 0

    for col in columns:
        if col != attr:
            IG = infogain(data, attr, entropie_start, col)
            if IG > current_IG:
                current_attr = col
                current_IG = IG

    cond = np.unique(data[attr])
    if cond.__len__() == 1:
        node.value = cond[0]
        # print("stop--------------")
        return cond[0]

    # print(f"Racine de l'arbre = {current_attr} avec un InfoGain de {current_IG}")
    node.attribut = current_attr
    # print(value_possible)

    value_possible = data[current_attr].unique()
    for value in value_possible:
        new_data = data[data[current_attr] == value].drop(current_attr, axis=1)
        np.unique(new_data[attr])
        # print(new_data)
        # print('\n')
        new_node = DecisionNode(attribut=None, value=None, branche={})
        node.branche[value] = new_node
        create_branch(new_data, attr, new_node)


def predict(node, sample):
    if node.is_leaf():
        return node.value

    attribut_value = sample[node.attribut]
    if attribut_value in node.branche:
        return predict(node.branche[attribut_value], sample)

    else:
        raise ValueError(f"Valeur inconnue '{attribut_value}")


symptoms = ["itching"]


principal_node = DecisionNode(attribut=None, value=None, branche={})
create_branch(data, "prognosis", principal_node)

sample = create_sample_data(symptoms)
print(predict(principal_node, sample))
