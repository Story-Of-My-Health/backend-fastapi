# import math
# import os

# import numpy as np
# import pandas as pd

# file_path = os.path.join(os.path.dirname(__file__), "training_data.csv")
# data = pd.read_csv(file_path)
# symptomes = data.columns.to_list()[:-1]
# disease = data["prognosis"].unique()


# class DecisionNode:
#     def __init__(self, attribut, value, branche):
#         self.attribut = attribut
#         self.value = value
#         self.branche = branche or {}

#     def is_leaf(self):
#         return self.value is not None


# def entropie(data, attr):
#     # classes = np.unique(data[attr])
#     size = data[attr].size
#     occurence = data[attr].value_counts()

#     entropie = 0
#     for value, count in occurence.items():
#         # print(f"La valeur {value} apparait {count} fois")
#         p = count / size
#         calc = -p * math.log2(p)
#         # print(f"La probabilite de {value} est {p} ==> {calc}")
#         entropie += -p * math.log2(p)

#     return entropie


# def infogain(data, attr, entropie_start, col):
#     # print(f"Calcul de l'infogain de l'attribut {col}:")

#     start_size = data[attr].size
#     # Sepration de l'ensemble en sous ensemble
#     data_col = data[col]
#     value_possible = data_col.unique()

#     # tmp = Somme de S[j] / S * Entropie (S[j])
#     tmp_sum = 0
#     for value in value_possible:
#         filtred = data[data[col] == value]
#         size_data_filtred = filtred[col].size
#         tmp_sum += (size_data_filtred / start_size) * entropie(filtred, attr)
#         # print(f"({size_data_filtred}/{start_size}) * {entropie(filtred, attr)} = {(size_data_filtred/start_size) * entropie(filtred, attr)}")

#     # IG = Infogaine de l'attribut col
#     IG = entropie_start - tmp_sum
#     # print(f"{entropie_start} - {tmp_sum} = {IG}")
#     # print(f"Info gain de l'attribut {col} est {IG}\n\n")
#     return IG


# def create_branch(data, attr, node):
#     columns = data.columns

#     # df_dropped = data.drop(attr, axis=1)
#     entropie_start = entropie(data, attr)
#     # print(f"L'entropie est {entropie_start}")

#     current_attr = attr
#     current_IG = 0

#     for col in columns:
#         if col != attr:
#             IG = infogain(data, attr, entropie_start, col)
#             if IG > current_IG:
#                 current_attr = col
#                 current_IG = IG

#     cond = np.unique(data[attr])
#     if cond.__len__() == 1:
#         node.value = cond[0]
#         # print("stop--------------")
#         return cond[0]

#     # print(f"Racine de l'arbre = {current_attr} avec un InfoGain de {current_IG}")
#     node.attribut = current_attr
#     # print(value_possible)

#     value_possible = data[current_attr].unique()
#     for value in value_possible:
#         new_data = data[data[current_attr] == value].drop(current_attr, axis=1)
#         np.unique(new_data[attr])
#         # print(new_data)
#         # print('\n')
#         new_node = DecisionNode(attribut=None, value=None, branche={})
#         node.branche[value] = new_node
#         create_branch(new_data, attr, new_node)


# def predict(node, sample):
#     if node.is_leaf():
#         return node.value

#     attribut_value = sample[node.attribut]
#     if attribut_value in node.branche:
#         return predict(node.branche[attribut_value], sample)

#     else:
#         raise ValueError(f"Valeur inconnue '{attribut_value}")


# def prediction_wrapper(sample):
#     principal_node = DecisionNode(attribut=None, value=None, branche={})
#     create_branch(data, "prognosis", principal_node)
#     prediction = predict(principal_node, sample)
#     return prediction

# Importing libraries
import numpy as np
import pandas as pd
import os
# from scipy.stats import mode
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy import stats

# Reading the train.csv by removing the
# last column since it's an empty column
DATA_PATH = os.path.join(os.path.dirname(__file__), "training_data.csv")
data = pd.read_csv(DATA_PATH).dropna(axis = 1)

# Encoding the target value into numerical
# value using LabelEncoder
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])

X = data.iloc[:,:-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test =train_test_split(
  X, y, test_size = 0.2, random_state = 24)


# Training and testing SVM Classifier
svm_model = SVC()
svm_model.fit(X_train, y_train)
preds = svm_model.predict(X_test)

print(f"Accuracy on train data by SVM Classifier\
: {accuracy_score(y_train, svm_model.predict(X_train))*100}")

print(f"Accuracy on test data by SVM Classifier\
: {accuracy_score(y_test, preds)*100}")
cf_matrix = confusion_matrix(y_test, preds)


# Training and testing Naive Bayes Classifier
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
preds = nb_model.predict(X_test)
print(f"Accuracy on train data by Naive Bayes Classifier\
: {accuracy_score(y_train, nb_model.predict(X_train))*100}")

print(f"Accuracy on test data by Naive Bayes Classifier\
: {accuracy_score(y_test, preds)*100}")
cf_matrix = confusion_matrix(y_test, preds)


# Training and testing Random Forest Classifier
rf_model = RandomForestClassifier(random_state=18)
rf_model.fit(X_train, y_train)
preds = rf_model.predict(X_test)
print(f"Accuracy on train data by Random Forest Classifier\
: {accuracy_score(y_train, rf_model.predict(X_train))*100}")

print(f"Accuracy on test data by Random Forest Classifier\
: {accuracy_score(y_test, preds)*100}")

cf_matrix = confusion_matrix(y_test, preds)


# Training the models on whole data
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
final_svm_model.fit(X, y)
final_nb_model.fit(X, y)
final_rf_model.fit(X, y)

# Reading the test data

DATA_TEST_PATH = os.path.join(os.path.dirname(__file__), "training_data.csv")
test_data = pd.read_csv(DATA_TEST_PATH).dropna(axis=1)

test_X = test_data.iloc[:, :-1]
test_Y = encoder.transform(test_data.iloc[:, -1])

# Making prediction by take mode of predictions
# made by all the classifiers
svm_preds = final_svm_model.predict(test_X)
nb_preds = final_nb_model.predict(test_X)
rf_preds = final_rf_model.predict(test_X)

final_preds = [stats.mode([i,j,k])[0] for i,j,k in zip(svm_preds, nb_preds, rf_preds)]

print(f"Accuracy on Test dataset by the combined model: {accuracy_score(test_Y, final_preds)*100}")

cf_matrix = confusion_matrix(test_Y, final_preds)

symptoms = X.columns.values

# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":encoder.classes_
}

def predictDisease(symptoms):
    symptoms = symptoms.split(",")

    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1,-1)

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    # making final prediction by taking mode of all predictions
    # Use statistics.mode instead of scipy.stats.mode
    import statistics
    final_prediction = statistics.mode([rf_prediction, nb_prediction, svm_prediction])
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction":final_prediction
    }
    return predictions

print(predictDisease("Itching,Shivering,Ulcers On Tongue"))

def prediction_wrapper(sample):
    def convertir_chaine(chaine):
        # Séparer les mots par '_', capitaliser chaque mot, puis les rejoindre avec des espaces
        mots = chaine.split('_')
        mots_capitalises = [mot.capitalize() for mot in mots]
        return ' '.join(mots_capitalises)
    
    tableau_converti = [convertir_chaine(chaine) for chaine in sample]
    
    print("tableu converti => ")
    print(tableau_converti)
    return "itching"
